"""Loopback-only adapter for the Firefox Tampermonkey download button."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import io
import json
import re
import shutil
import subprocess
import threading
import uuid
import zipfile
from convert_model import convert

ROOT = Path(__file__).resolve().parent
LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def send(self, status, payload, kind='application/json', filename=None):
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        if filename:
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == '/health':
            self.send(200, b'{"status":"ready"}')
        else:
            self.send(404, b'{"error":"Not found"}')

    def do_POST(self):
        # Custom header + JSON prevent ordinary web pages issuing a drive-by POST.
        # No CORS/preflight permission is granted; Tampermonkey uses its own API.
        if (self.path != '/download' or self.headers.get('X-Sketchfabdl') != '1'
                or self.headers.get_content_type() != 'application/json'):
            return self.send(403, b'{"error":"Use the Tampermonkey button"}')
        if not LOCK.acquire(blocking=False):
            return self.send(409, b'{"error":"A download is already running. Try again when it finishes."}')
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1024:
                raise ValueError('Invalid request size')
            uid = json.loads(self.rfile.read(length)).get('uid', '')
            if not isinstance(uid, str) or not re.fullmatch(r'[0-9a-f]{32}', uid):
                raise ValueError('Invalid model ID')
            output = ROOT / 'downloads' / (uid[:8] + '-' + uuid.uuid4().hex[:8])
            cmd = [shutil.which('node') or 'node', str(ROOT / 'vendor' / 'sfrip' / 'sfrip.mjs'),
                   uid, '--out', str(output), '--no-textures', '--no-bones', '--yes', '--no-color']
            run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=180,
                                 creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if run.returncode:
                raise RuntimeError((run.stderr or run.stdout)[-3000:])
            models = list(output.rglob('*.glb'))
            if len(models) != 1:
                raise RuntimeError('Downloader did not produce exactly one GLB')
            glb = models[0]
            report = convert(glb)
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as z:
                for file in [glb, glb.with_suffix('.stl'), glb.with_suffix('.obj'),
                             glb.with_name('mesh-report.json'), glb.with_name('info.json')]:
                    z.write(file, file.name)
                z.writestr('PRINTING.txt',
                    'STL and OBJ preserve the viewer coordinates. Confirm units and dimensions in your slicer.\n'
                    'See mesh-report.json for open/nonmanifold edges. A viewer mesh is not guaranteed print-ready.\n'
                    'Textures are omitted; GLB is included for inspection.\n')
            zip_path = glb.parent / (glb.stem + '.zip')
            zip_path.write_bytes(archive.getvalue())
            print(f'Saved {zip_path}; watertight={report["watertight"]}', flush=True)
            self.send(200, archive.getvalue(), 'application/zip', zip_path.name)
        except Exception as exc:
            self.send(400, json.dumps({'error': str(exc)}).encode())
        finally:
            LOCK.release()


if __name__ == '__main__':
    print('Sketchfab download helper: http://127.0.0.1:8765 (Ctrl+C to stop)', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
