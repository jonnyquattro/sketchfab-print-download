# Sketchfab Print Download

**Experimental software for authorized reference, evaluation and interoperability work.** Intended for models you own or have explicit permission to export and use. Public visibility alone is not permission to download, reproduce, print or redistribute a model.

**Code provided as an experimental reference implementation. Designed to work with Tampermonkey in Firefox and the included local helper; it is not a standalone browser extension.**

A Firefox/Tampermonkey button that sends a public Sketchfab model to a local converter and downloads a ZIP containing **STL, OBJ and GLB** files. It uses the viewer assets without Sketchfab registration, login, API keys or browser cookies. That technical capability does not establish that a particular download is permitted.

## Disclaimer and user responsibility

This code is provided for reference and evaluation, **as is**, without warranties of any kind, under the [MIT license](LICENSE). Use, modification and execution are at your own risk. You are responsible for obtaining all necessary permissions, complying with applicable laws and platform terms, and verifying any downloaded files or printed results.

To the maximum extent permitted by applicable law, the authors, contributors and maintainers assume no responsibility or liability for use or misuse of this code, downloaded content, resulting prints, loss of data or other damages arising from its use. This notice does not exclude liability that cannot legally be excluded and does not authorize infringement or override third-party rights. Describing the code as a reference implementation does not change the permissions granted by the MIT license.

## Responsible use

- Use your own models or obtain permission from the relevant rights holders that covers export and your intended use. Keep a copy of the permission and the source model's license and attribution details.
- Prefer a creator-provided download, purchase or original project file when available. If permission or platform authorization is unclear, stop and ask the rights holder/platform before using this tool.
- Review the applicable [Sketchfab terms](https://sketchfab.com/terms). Permission to use a model does not necessarily authorize a particular method of obtaining it.
- Reference, research, evaluation, education, personal use and noncommercial use are descriptions of purpose, not automatic exemptions. Do not assume any of them establishes fair use or permission.
- Do not use the tool to obtain private, password-protected or paid content without authorization, defeat access restrictions, evade platform enforcement, or substitute for a required purchase.
- Do not reupload, redistribute, sell or print someone else's model unless the applicable permissions cover those actions. Preserve required attribution and license notices.

The converter processes the viewer's encoded/encrypted assets. This README does not resolve whether that processing is authorized in a particular case. The labels **experimental** and **reference only**, and the software's MIT license, do not prevent complaints, takedowns or cease-and-desist demands. No legal clearance or guarantee is provided. For a decision about publishing or using this tool in your circumstances, seek qualified legal advice.

See the [U.S. Copyright Office's permission and fair-use FAQ](https://www.copyright.gov/help/faq/faq-fairuse.html) and [GitHub's DMCA policy, including circumvention claims](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy). Rules and available exceptions differ by jurisdiction.

## Safe installation and operation

- Obtain [Python](https://www.python.org/downloads/), a currently supported [Node.js LTS release](https://nodejs.org/en/download), and [Tampermonkey](https://www.tampermonkey.net/) from their official sources. Review the scripts before running them; do not run unknown replacement installers or paste commands from model descriptions.
- Run the helper as a normal user. Administrator privileges are not needed. Setup creates a local Python environment and installs the declared Python/npm dependencies; it needs network access.
- Keep the helper bound to `127.0.0.1`. Do not expose port 8765 through a router, tunnel, reverse proxy or public hosting. It has no user authentication and is not designed as a network service. Its request header is not a secret or an authentication token.
- The userscript is scoped to Sketchfab and requests a connection to `127.0.0.1`. This tool does not require your Sketchfab password, API token or exported browser cookies. Do not provide those to a downloader.
- Run one model at a time and leave disk and memory headroom. Models are untrusted input, and large or malformed assets may fail or exhaust resources. The converter is not a sandbox. Keep Python, Node.js, mesh editors and slicers updated.
- Downloads and source metadata remain in the local `downloads/` folder as well as the browser's saved ZIP. Review metadata and logs before sharing them. Delete local copies you no longer need, and close the helper when finished.

## Windows setup

1. Install Python 3.12 or newer, a currently supported Node.js LTS release (converter minimum: Node.js 18), and Tampermonkey in Firefox. Make sure Python and Node.js are on your PATH.
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

Inspect the sliced layer preview before printing and follow your printer and material instructions. Do not rely on an exported reference mesh as certified protective equipment, a medical device or a load-bearing part.

Public viewer geometry can differ from the creator's original project. Private/password-protected models are unsupported. Viewer changes, unusual scenes and large models may cause failures or timeouts.

## Validation

The reference mask was downloaded anonymously, decoded, converted and exported with 456,512 triangles. The local HTTP endpoint returned a valid ZIP, and the STL/OBJ/GLB exports were reopened to check their triangle counts. Userscript request/download/error handling was checked with a mocked DOM; installation in a real Firefox profile has not been verified.

## Credits and license

The converter is vendored from [Corpocore/sfrip](https://github.com/Corpocore/sfrip), commit `2bb0b7594aeea9f979af035eccb8c6ad29586633`, under its [MIT license](vendor/sfrip/LICENSE). Its upstream source credits the [Sketchfab downloader extension](https://github.com/seryi882/sketchfab-downloader-extension).

The local helper and userscript are MIT licensed. Downloaded models retain their creators' rights and licenses. No downloaded models are included in this repository.

This is an independent project, not affiliated with or endorsed by Sketchfab or Epic Games. Their names identify the platform the tool works with.

## Rights concerns

For a concern about this repository, contact the maintainer through [GitHub Issues](https://github.com/jonnyquattro/sketchfab-print-download/issues). Identify the relevant repository paths and source work, explain the concern, and provide a way to follow up. Do not post private documents, identity records or confidential model files in a public issue. Formal copyright notices should follow [GitHub's published process](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy). This contact route does not replace that process or guarantee a particular legal outcome.
