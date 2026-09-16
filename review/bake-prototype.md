# Viewer lighting prototype

The existing browser lights are a useful navigation aid but cannot reproduce the native Cycles render: the viewer has no indirect illumination or contact shadows. `scripts/bake_viewer.py` adds an actual Cycles illumination bake for opaque, nonmetal surfaces; glass, metals and plain molded white chairs retain PBR shaders.

The script never changes the native source file. Run it with Blender's `-b source.blend -P scripts/bake_viewer.py -- ...` interface. It evaluates geometry, preserves original Object and Generated texture coordinates as point attributes, groups compatible meshes by source collection / floor / wing / cutaway status, smart-projects independent UV atlases, bakes diffuse direct and indirect lighting plus emission, and embeds the resulting atlas images in a separate GLB. Original shaders remain active until every group has been baked, avoiding light feedback between atlas passes.

## Browser integration

- Set `material.toneMapped = false` for material names beginning `Baked / `. The textures already contain the native AgX display transform. Applying the existing ACES transform again would wash them out.
- Preserve layer parents and `cutaway_shell` extras, which the prototype exports.
- Keep ordinary lighting/environment for the remaining glass and metal PBR materials.
- Camera exposures do not apply to the baked materials. Choose one consistent bake exposure; the prototype uses -1.1 stops for the central stair.

## Limits to assess before adoption

This is a fixed lighting condition. Moving a wall or changing a lamp requires rebaking. Cutaway views retain the shadows cast by the intact enclosure. Baked diffuse materials lack view-dependent reflections; reflective metal and glass are therefore excluded. Very small typography should keep its original image/text mesh material if an atlas would reduce readability. Final atlas density needs visual inspection at the closest preset cameras.

Prototype timing, actual visual inspection, and output sizes are being measured against the R14 scene in `/tmp`, without replacing production assets.


## Measured first prototype

R14, 24 Cycles samples, OptiX, two 2048² atlases:

- 239 central components / 31,061 polygons: 51.29 seconds, 2.08 MB PNG.
- Two ceiling objects / 12 polygons: 62.82 seconds, 0.97 MB PNG.
- Complete evaluation, both bakes, preview render and GLB export: 218.46 seconds.
- GLB: 42.62 MB, including both images. Source native file was untouched.
- Native debug render: `/tmp/bahen-baked-prototype.png`.
- Actual Three.js browser screenshot: `/tmp/bahen-baked-browser.png`.

The browser screenshot confirms that the stair treads, wood rails, walls and floor retain real shadows and indirect gradients instead of the original flat browser light. The remaining mismatch is ordinary glass/metal shading, which this bake intentionally preserves as PBR. This is a feasible improvement for delivery, subject to final-scene rebaking and close-up atlas review.

The script now pre-batches all scene geometry by compatible source layers and materials before any bake, preserving procedural coordinates in attributes. This avoids the major first-prototype cost: resynchronizing thousands of scene objects per atlas. Hero central floors use 4096² atlases in full mode. Fonts, `source_texture` materials and `preserve_uv` objects keep their original shader/texture detail. Optional `--exposure-map` accepts a JSON map from layer prefix to exposure, while the default uniform exposure avoids seams where adjacent surfaces meet. The exported asset extras retain `source_components` for honest UI statistics after batching.

Blender exports a bare Emission shader as black PBR plus an emissive map. The script converts that explicit material subset to standards-compliant `KHR_materials_unlit`, preserving embedded textures and all binary buffer offsets.

For full delivery, JPEG quality 95 is the default atlas format (`--texture-format PNG` remains available). The first two prototype atlases shrink from 3.04 MB PNG to 0.94 MB JPEG; original source monitor and notice images remain untouched.


## Final R20 bake

The final frozen native snapshot has 7,511 objects / 7,417 mesh objects and SHA-256 `bbd5bbdf6614cbc4fb58709ba55f3de85986f53a48d63c7ec3d1900b56691f72`. Evaluation includes fonts/curves and yields 7,456 renderable source components. Batching retains all geometry in 140 source mesh groups and partitions baked surfaces into 98 independent atlas regions.

Final quality allocation is 4096² for the primary central stair/corridor floors and lecture theatre, 1024² for other regions, and 512² for nonhero groups of at most 2 m². All use 32 Cycles samples and quality-95 JPEG. This concentrates texture detail at the close-up comparison cameras and keeps the portable package within GitHub's individual-file size limit. Two already completed 2048² site atlases are reused rather than discarded.

The `--resume` option validates the frozen native SHA, samples, format and exposure settings against `/tmp/bahen-r20-atlases/bake-manifest.json`. Existing atlases are reused only when their dimensions meet or exceed the requested resolution. UV generation remains deterministic across those resolution changes. Exposure is -1.1 stops for central circulation, -.75 for the theatre and -.5 elsewhere. Source monitor, noticeboard and recycling-label texture data remains separate, and the monitor exports as an actual unlit image material.


## Completed delivery asset

The complete adaptive GI run took 1,482 seconds (24.7 minutes), with a second worker supplying the theatre atlases through the validated cache. Browser inspection then caught black theatre backrests: 207 closed chair-back meshes had inward winding. A signed-volume audit checked all 7,395 closed evaluated meshes and found no other inverted shapes; 61 open meshes were left untouched. The exporter now repairs only closed meshes with proven negative volume, preserving vertex positions and the frozen native file.

Plain white chair backrests and seat pans retain their original PBR material. This avoids unnecessary atlas seams on small beveled surfaces and preserves live highlights. The final scoped rebuild reused 97 atlases and regenerated only the shared theatre desk/floor atlas, completing in 144 seconds.

The final lit GLB is **59,593,116 bytes (56.83 MiB)**. It contains 141 mesh groups representing all 7,456 source components, 98 embedded lighting atlases (87 at 1024², nine at 4096², and two retained 2048² site maps), and all four original Source image materials. Glass, metal, typography, source notices and molded white chairs remain live PBR; the Source monitor exports as a true unlit image.

Structural verification decoded every image, checked all GLB buffer ranges and floating-point accessors, confirmed all 98 baked materials use `KHR_materials_unlit`, confirmed the Source monitor retains its texture, and verified 15 cutaway nodes. The asset extras identify revision r20, 7,456 source components and the frozen native source SHA. The detailed report records all 207 export-only normal repairs.

Final GLB SHA-256: `bad12eded02c5eb55a14f3f5446eeb2f802c67658b0c00e725b908967a9ac37e`.

Machine-readable export data: `viewer/bahen-lit.json`. Independent audit: `/tmp/baked-glb-audit.json`. Browser validation uses the regenerated real viewer page and the actual exported asset; final screenshots are `/tmp/bahen-final-lit-theatre.png` and `/tmp/bahen-final-lit-landing.png`.

Final actual-page browser verification passed with no JavaScript errors. The exported model loaded in 23.21 seconds under headless Chrome/SwiftShader. Visual inspection confirmed clean white theatre chairs without atlas seams or mottling, and preserved the central stair lighting. The viewer reported 141 mesh groups and all 7,456 source components.
