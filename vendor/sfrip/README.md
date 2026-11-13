<div align="center">

# sfrip

**Sketchfab models → one clean `.glb`.**

Geometry, PBR textures, rigs, skin weights and animation clips, carried across
intact from the same encrypted scene data Sketchfab's own viewer renders.

No browser extension. No screenshot. No 200 textureless OBJs.

```bash
npm install -g sfrip
sfrip <sketchfab-url-or-uid> [options]
```

</div>

---

## Contents

- [Install](#install)
- [What you get](#what-you-get)
- [Quick start](#quick-start)
- [Options](#options)
- [Merging](#merging)
- [Skeletons](#skeletons)
- [⚠️ Licensing — read this first](#-licensing--read-this-first)
- [How it works](#how-it-works)
- [Output](#output)
- [Limits](#limits)
- [Tests](#tests)

---

## Install

Needs **Node 18 or newer**. Nothing else — no API key, no build step, no
compiler.

> Replace `Corpocore` below with the GitHub account hosting this repo.

### macOS

```bash
brew install node                              # or the .pkg from nodejs.org
curl -fsSL https://raw.githubusercontent.com/Corpocore/sfrip/main/install.sh | sh
```

Node is also available as a signed installer from
[nodejs.org/download](https://nodejs.org/en/download) if you would rather not
add Homebrew.

### Linux

Node first, from your distro or from NodeSource if the packaged one is old:

| Distro | Node |
| :--- | :--- |
| Ubuntu 24.04+, Debian 13+ | `sudo apt install nodejs npm` — ships Node 18, new enough |
| Older Debian/Ubuntu | `curl -fsSL https://deb.nodesource.com/setup_lts.x \| sudo -E bash - && sudo apt install -y nodejs` |
| Fedora / RHEL | `sudo dnf install nodejs` |
| Arch | `sudo pacman -S nodejs npm` |
| openSUSE | `sudo zypper install nodejs npm` |

Then the tool:

```bash
curl -fsSL https://raw.githubusercontent.com/Corpocore/sfrip/main/install.sh | sh
```

### Windows

```powershell
winget install OpenJS.NodeJS.LTS
irm https://raw.githubusercontent.com/Corpocore/sfrip/main/install.ps1 | iex
```

The installer is also on [nodejs.org/download](https://nodejs.org/en/download)
if you prefer it to winget.

### WSL

Same as Linux, but **install Node inside the distribution**:

```bash
sudo apt install nodejs npm
curl -fsSL https://raw.githubusercontent.com/Corpocore/sfrip/main/install.sh | sh
```

On a stock WSL setup `node` may resolve to the *Windows* one through interop,
which works but writes Windows-style paths. Check with `which node` — if it
points into `/mnt/c`, you are running the Windows build.

### What the installers do

Both check your Node version first, install the CLI globally, and tell you if
the install location is missing from `PATH`. Re-running upgrades in place. They
honour a `SFRIP_REPO` environment variable, which overrides the default repo and
is handy for forks.

### Or just npm

```bash
npm install -g sfrip
```

Then, from anywhere:

```bash
sfrip https://sketchfab.com/3d-models/some-model-1234abcd5678
```

<details>
<summary>Other ways to run it</summary>

**Without installing**, if you just want to try it:

```bash
npx sfrip <url>
```

**From a clone**, if you want to read or change the code:

```bash
git clone https://github.com/Corpocore/sfrip
cd sfrip
npm install
node sfrip.mjs <url>
```

**From a local folder**, without publishing anywhere:

```powershell
npm install -g C:\path\to\sfrip
```

The tool has one runtime dependency (`jpeg-js`) and resolves its own WASM
relative to the script, so it works from any working directory.

</details>

<details>
<summary>If <code>npm install -g</code> fails on permissions</summary>

Global installs write to a shared location that some systems lock down. Point
npm at a folder you own, once, and elevation is never needed again:

```bash
npm config set prefix ~/.local
export PATH="$HOME/.local/bin:$PATH"   # add to your shell profile
npm install -g sfrip
```

On Windows the equivalent is a user-level prefix:

```powershell
npm config set prefix "$env:APPDATA\npm"
```

</details>

---

## What you get

One folder per model, and one file you usually care about:

```text
Sci_Fi_City_2020-9fe00d65/
├── Sci_Fi_City_2020.glb        ← open this
├── textures/                   loose PBR maps, for external-texture pipelines
├── model.gltf + model.bin      the same scene, textures kept external
├── file.osgjs, model_file.bin  the decrypted source, pre-conversion
├── info.json                   metadata and the full run log
└── README.txt
```

The GLB is the deliverable: textures embedded, materials bound, rig and clips
attached. The rest is there for pipelines that want loose files, or for anyone
who wants to inspect what came across.

### What survives the trip

<table>
<tr><th align="left">Channel</th><th align="left">Carried</th></tr>
<tr><td><b>Geometry</b></td><td>Every triangle, vertex colours, multiple UV sets, tangent frames, point clouds, authored lines</td></tr>
<tr><td><b>Materials</b></td><td>Base colour, normal, packed ORM, occlusion, emissive, clearcoat, sheen, opacity modes, double-sidedness, transmission glass</td></tr>
<tr><td><b>Textures</b></td><td>Resolved to the highest-quality unscrambled original Sketchfab serves</td></tr>
<tr><td><b>Rig</b></td><td>Skeletons, joints, inverse bind matrices, per-vertex weights</td></tr>
<tr><td><b>Animation</b></td><td>Named clips, including object animation on models with no rig at all</td></tr>
<tr><td><b>Morphs</b></td><td>Shape keys, including on skinned meshes</td></tr>
<tr><td><b>Lights</b></td><td>The scene's own punctual rig, when the viewer uses one</td></tr>
</table>

Two things are deliberately left behind, and [Limits](#limits) explains why.

---

## Quick start

```bash
sfrip https://sketchfab.com/3d-models/some-model-1234abcd5678
```

It reads the model, reports what it found, and **asks before downloading
anything**, so nothing lands on disk until you say so:

```text
Sci-Fi City
────────────────────
  by             Nicholas-3D
  geometry       467 parts · 1,722,036 verts · 1,009,798 tris
  materials      6
  rig            none
  animation      none
  textures       6 to download
  output         C:\Users\you\out\Sci-Fi_City-fd7092ff

  What next?

  ❯ Merge       off (467 meshes) · objects (284 meshes) · groups (284 meshes)
    Textures    download · skip
    Skeleton    keep · bake and drop
    Convert
    Cancel
```

Drive it with the arrow keys:

| Key | Does |
| :--- | :--- |
| `↑` `↓` | move between rows |
| `←` `→` | change the highlighted row's value |
| `1`-`9` | pick that option on the highlighted row |
| `enter` | advance, and **run** on `Convert` |
| `q`, `esc` | leave without converting |

Every option sits on screen at once, so a merge level is chosen by comparing its
mesh count against the others rather than by opening and closing a submenu.

### Or skip all of it

```bash
sfrip <url> --merge=groups --no-textures --yes
```

`--yes` runs immediately with whatever the flags said. That is the fast path,
and it is what a script or a piped run uses, since neither has anyone to ask.

### Common commands

```bash
# keep every part separate — best for editing a small scene
sfrip <url> --merge=off

# a huge city: fold it down until it imports
sfrip <url> --merge=groups

# a rigged character whose armature imports badly
sfrip <url> --no-bones

# geometry only, when the textures are already on hand
sfrip <url> --no-textures

# a batch, from a script — prints just the path
sfrip <url> --quiet
```

---

## Options

| Flag | Meaning |
| :--- | :--- |
| `-o, --out <dir>` | Output root. Default `./out` |
| `--merge[=<level>]` | How finely to split the scene. See [Merging](#merging) |
| `--no-merge` | Same as `--merge=off` |
| `--no-bones` | Bake the rest pose and drop the skeleton |
| `--no-textures` | Skip the texture download |
| `--max-edge <n>` | Cap texture resolution at `2048` or `4096` |
| `--concurrency <n>` | Parallel texture downloads. Default `3` |
| `--zip` | Also write a single `.zip` of the folder |
| `-y, --yes` | Skip the confirmation prompt |
| `-v, --verbose` | Show download and conversion detail |
| `-q, --quiet` | Print errors only; stdout becomes the GLB path |
| `--no-color` | Plain text, for logs |
| `-V, --version` | Show the version |
| `-h, --help` | Show usage |

Colour turns itself off when output is piped, so redirecting to a file or
another program gives clean text without needing `--no-color`.

A run prints a panel, a progress bar and a summary — around 20 lines. The
internal detail (decrypt offsets, per-material factors, descramble byte counts)
is written to `info.json` on every run, and to the terminal only under
`--verbose`.

---

## Merging

Importers choke on object count, not triangle count, so this is the setting that
decides whether a scene opens at all. Without merging the output has one mesh per
sub-part, and a 16,633-part city becomes 16,633 objects — Blender's importer runs
out of memory and exits with no error.

Measured on two real scenes:

| Level | `Future City HD 6` | `Sci-Fi City 2020` | Keeps |
| :--- | ---: | ---: | :--- |
| `off` | 16,633 | 248 | every part separate |
| **`objects`** *(default)* | **138** | **12** | authored objects |
| **`groups`** | **77** | **4** | top-level groups |
| `materials` | 2 | 1 | nothing — one mesh per material |
| `all` | 2 | 1 | nothing — one mesh |

`groups` is the level that matters for a scene too big to edit and too small to
flatten: it folds everything under one top-level branch together, which on
`Future City` is 138 meshes down to 77 without losing the major structure.

The objects are found **structurally**, not by name. Sketchfab nests a model
under a chain of single-child wrappers — a file node, a `RootNode`, sometimes a
container like `Whole` — and a named node that *branches* is an object, while a
named node that terminates in geometry is one of its mesh primitives. That
distinction is what keeps `Box16`, `Cylinder07` and `Sphere01` inside their
building instead of becoming objects of their own, which once regressed a scene
to 12,611 groups for 76 authored objects.

glTF meshes carry one primitive per material, so a building with 19 materials is
**one mesh with 19 primitives**, not 19 meshes.

Every level preserves geometry exactly — identical vertex, triangle and primitive
counts — and none of them merges skinned meshes or morph targets, since glTF
addresses those per node. A rigged model therefore reports the same mesh count at
every level, which is the intended answer rather than a bug.

> **On the `~`.** The `materials` count is marked approximate because material
> identity depends on texture filenames, and those resolve against downloads that
> have not happened yet. The other four levels are exact.

---

## Skeletons

`--no-bones` applies the rest pose to the vertices and removes the rig. The
result is the model exactly where the skeleton would have put it, with no
skeleton to import.

Deleting an armature by hand does **not** do this. The joints are what position a
skinned mesh, so removing them leaves the geometry at its bind-space coordinates
and the parts scatter across the origin. The product glTF evaluates per vertex is
computed once here instead:

$$\text{skinned} = \sum_i w_i \left( \text{jointWorld}_i \cdot \text{inverseBind}_i \right) p$$

Useful for a model whose rig imports badly, or for a scene where only the pose
matters. Animations are dropped, since nothing is left to drive them.

---

## ⚠️ Licensing — read this first

**This tool grants you no rights to a model. It only removes the technical
friction of getting the file.**

*sfrip itself is MIT licensed (see [LICENSE](LICENSE)). That covers this code
and nothing else — a model you download keeps whatever licence its author set,
regardless of how the file was obtained.*

- **Every model has a licence**, shown on its Sketchfab page: CC0, CC-BY, other
  Creative Commons variants, or *Standard* / *Editorial* for store items.
  Downloading does not change which one applies.
- **The paid path exists because the tool does not check.** It will happily rip a
  model you have not bought. **Do not use it that way.** Buying a model grants
  you the licence on its own terms; circumventing the store grants you nothing,
  and takes income directly from the artists this ecosystem runs on.
- **Personal use is not ownership.** If you did not author a model and did not
  buy a licence, treat the result as reference only — do not redistribute it,
  sell it, ship it inside a product, or publish it as your own.
- **CC-BY requires attribution.** Ship the author's name and the model page URL
  with the asset, or you are not compliant.
- **Keep `info.json`.** It records the model name, author and source URL so you
  can credit correctly later.

Want a model without these strings? Ask the author, or commission one. Artists
are generally generous when they are asked.

---

## How it works

Sketchfab's viewer does not serve glTF. It streams a proprietary, encrypted
`.binz` container, decrypts it in the browser through a WASM module, and parses
the result as an OSGJS scene graph. DOM-scraping userscripts only ever see the
meshes the viewer has already drawn, which is why they emit geometry with no
materials.

sfrip reimplements that pipeline outside the browser:

| # | Stage | File |
| :-: | :--- | :--- |
| 1 | Read public viewer data, extract the live decrypt key, resolve material channels and texture URLs | `lib/sf-api.js` |
| 2 | Decrypt the `.binz` buffers. The per-file `diter.b` blob drives the permutation | `lib/decrypt.js` + `lib/wasm/` |
| 3 | Reverse the pixel permutation on protected textures, recovering the original upload | `lib/descramble.js` |
| 4 | Decode OSGJS: varint and quantised attributes, skeletons, bind matrices, curves | `lib/osg-codec.js`, `lib/osg-scene.js`, `lib/skin.js` |
| 5 | Convert to glTF. Materials are matched to the viewer's own channel bindings by StateSet ordinal, because names match for barely a third of a model | `lib/osgjs2gltf.js` |
| 6 | Pack separate metalness + roughness maps into one metallicRoughness texture | `lib/orm.js` |

The decrypt key is read from the live bundle on every run, so it survives
Sketchfab rotating it. `decrypt.js` carries a known-good fallback for when that
read fails.

---

## Output

| File | Contents |
| :--- | :--- |
| `<name>.glb` | Self-contained glTF binary: geometry + textures + animations + rig |
| `textures/` | Loose PBR maps, for pipelines that want external textures |
| `model.gltf` + `model.bin` | External glTF referencing `textures/` |
| `file.osgjs`, `model_file.bin` | The decrypted raw scene, pre-conversion |
| `info.json` | Source metadata, counts, and the complete run log |
| `README.txt` | Per-rip manifest |

A run that hits a missing texture records it in `info.json` under
`textures_failed`, so a partial rip is distinguishable from a complete one.
Every fetch retries three times with backoff — Sketchfab's CDN resets
connections regularly, and before retries existed a single reset silently
dropped a texture from the export.

---

## Limits

Honest about what does not come across.

**The environment is not exported.** Sketchfab lights these models with an
image-based environment at intensity 3. glTF has no scene-environment concept, so
a metallic surface arrives with the correct `metallicFactor` and nothing to
reflect, which means black. **Set up a world environment in the target renderer**
and metals and glass resolve.

**The matcap is not exported.** Every material on the models tested carries a
`Matcap` entry, and the viewer's shader does use it — it replaces the base colour
with a sphere-mapped reflection. A matcap is indexed by the view-space normal
rather than a UV, which glTF cannot express. Baking it into vertex colours was
tried and removed: the maps are authored per surface (`skin_soft.png` for skin)
and applying one across a scene tinted every material, turning a city almost
black.

**Skinning is carried, axis conventions are the model's own.** A rig that stands
itself up along a non-Y axis keeps that convention, since glTF's Y-up rule is
enforced by the root node rather than by the skeleton.

---

## Tests

```bash
npm test
```

238 tests across 28 files, covering the decoder, the material resolver, the merge
rules, and the export. The ones worth naming are the cases that encode a bug found
in the wild:

| File | Guards against |
| :--- | :--- |
| `merge-levels.test.js` | Tier counts drifting from what each level actually builds |
| `rig-units.test.js` | A unit-scaled rig leaving a scaled armature that draws 4,000-unit bone shapes around a one-unit model |
| `object-animation.test.js` | A clip on an unrigged transform being flattened into a node that no longer exists |
| `morph.test.js` | Shape keys nested inside a `RigGeometry` going missing, producing a model with no geometry at all, reported as success |
| `lights.test.js` | Exporting lights the viewer deliberately leaves off because an environment does the work |
| `glass-geometry.test.js` | A material with an opacity factor but no opacity texture falling through to `OPAQUE` |
| `textures.test.js` | Preferring a re-encoded twin over the original upload, which is not the byte stream the permutation reverses |
| `materials.test.js` | A bare trailing `N` misread as anything but a normal map |

`test/i18n.test.js` was dropped: it asserts on the extension's `manifest.json`,
which means nothing for a CLI.

---

<div align="center">
<sub>Sketchfab's viewer is proprietary and this project is unofficial. It exists
because authored 3D work deserves to move between tools without a browser
extension in the way.</sub>
</div>
