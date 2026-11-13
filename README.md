# Sketchfab Print Download

A Firefox/Tampermonkey button that sends a public Sketchfab model to a local converter and downloads a ZIP containing **STL, OBJ and GLB** files. It uses the viewer assets without Sketchfab registration, login, API keys or browser cookies.

## Windows setup

1. Install Python 3.12 or newer, Node.js 18 or newer, and Tampermonkey in Firefox. Make sure Python and Node.js are on your PATH.
2. Download this repository as a ZIP and extract it, or clone it.
3. Double-click **Setup.cmd** and wait for setup to finish.
4. In Tampermonkey, choose **Create a new script**. Replace the template with the complete contents of [`sketchfab-print-download.user.js`](sketchfab-print-download.user.js), then save with **Ctrl+S**.
5. Double-click **Start Sketchfab Helper.cmd**. Keep the window open.
6. Open or reload a public Sketchfab model page. Click **Download STL / OBJ** at the bottom right. Allow Tampermonkey to connect to `127.0.0.1` if prompted.

The helper listens on `127.0.0.1:8765`. It processes one model at a time. Close its window or press Ctrl+C to stop it. No hosted service or GitHub account is required to run the tool.

## Output

Each ZIP contains:

- **STL** for a printing slicer.
- **OBJ** for mesh editors.
- **GLB** for scene inspection in Blender or a 3D viewer.
- `mesh-report.json` with dimensions, triangle count and mesh checks.
- `info.json` with source model metadata and conversion details.
- `PRINTING.txt` with printing notes.

Downloads are also retained locally under `downloads/`. Textures are omitted. Scene transforms are applied; matching vertices are welded and duplicate/degenerate triangles are removed. The tool does not fill holes or remesh the model.

## Printing limitations

A displayed model is not necessarily printable. Check wall thickness, open edges, intersections, orientation and scale in your slicer. STL has no unit metadata; the converter preserves the source coordinate values. Use the mesh report as a starting point, not a printability guarantee.

Public viewer geometry can differ from the creator's original project. Private/password-protected models are unsupported. Viewer changes, unusual scenes and large models may cause failures or timeouts.

## Validation

The reference mask was downloaded anonymously, decoded, converted and exported with 456,512 triangles. The local HTTP endpoint returned a valid ZIP, and the STL/OBJ/GLB exports were reopened to check their triangle counts. Userscript request/download/error handling was checked with a mocked DOM; installation in a real Firefox profile has not been verified.

## Credits and license

The converter is vendored from [Corpocore/sfrip](https://github.com/Corpocore/sfrip), commit `2bb0b7594aeea9f979af035eccb8c6ad29586633`, under its [MIT license](vendor/sfrip/LICENSE). Its upstream source credits the [Sketchfab downloader extension](https://github.com/seryi882/sketchfab-downloader-extension).

The local helper and userscript are MIT licensed. Downloaded models retain their creators' rights and licenses. No downloaded models are included in this repository.
