# Bahen Centre — reconstruction from the video tour

[**Explore the 3D model**](https://alecjacobson.github.io/astra-dgp/viewer/) · [**Video/render comparisons**](https://alecjacobson.github.io/astra-dgp/gallery.html) · [Offline viewer](bahen-centre-viewer.html) · [GLB](bahen-centre.glb) · [Blender scene](bahen-centre.blend)

![Exact 14:52 video frame and reconstructed room 2133](renders/comparison-1452.png)

The complete **43:01.6, 720p source MP4** is now available locally and drives the revised model. Direct yt-dlp requests were blocked; the original Googlevideo track was recovered from an Internet Archive capture. **135 timestamped frames** were decoded across the full tour, including the requested **14:52 / frame 26760**. [Acquisition record](review/VIDEO_ACQUISITION.md) · [SHA256 and frame catalog](review/frame-catalog.json).

The video corrected major first-draft assumptions. Room2133 is a cream door along the second-floor gallery. The illuminated central stairs are straight flights beside curved glazing; the old continuous spiral was removed. Revisions add the door's hardware, purple monitor and noticeboard; closed illuminated risers; round timber rails; blue lower guards with clear upper extensions; actual floor openings; the street's large louvre bay and entrance doors; and the raked lecture theatre with white seats and sliding chalkboards.

**This is a source-guided architectural approximation.** Selected local camera anchors align closely, especially at 14:30 and 14:52. Dimensions, global registration of rooms, hidden spaces, repeated upper floors, exterior massing and the overall footprint remain inferred. It is not a measured survey or photogrammetric recovery. The comparison gallery makes residual differences visible; the presenter is intentionally omitted from the architecture.

![Reconstructed illuminated central stair](renders/final-video_1430.png)

## Explore and download

- **Online:** orbit/pan/zoom, jump to timestamped views, open the shell, hide landscape and save screenshots. WASD moves horizontally; Q/E vertically, without collision detection.
- **Offline:** download `bahen-centre-viewer.html` using GitHub's download button. Open it directly; Three.js and the complete model are embedded.
- **Blender:** editable named objects, procedural materials, lights and review cameras. Blender 4.5; metres; Z up.
- **GLB:** embedded textures, standard glTF 2.0, named construction groups; Y up. Browser lighting and glass are simplified for responsiveness, so Cycles renders are the visual comparison standard.

## Render, compare, revise

The first six revisions were guided by preview photographs. The video-driven R07–R14 series replaces that limited evidence with actual decoded frames and an independent judging agent. Corrections were tested by rendering the same 16:9 view repeatedly and comparing source anchors, occlusion, stair direction, floor connectivity, materials and background geometry.

[Comparison gallery](https://alecjacobson.github.io/astra-dgp/gallery.html) · [Video route and certainty](review/video-route.md) · [Independent R14 review](review/judge-video-r14.md) · [Selected camera-anchor check](review/camera-anchor-check.json) · [Iteration record](review/ITERATIONS.md) · [Progress screenshots](progress/history.md).

Screenshots are committed about every ten minutes during active work. The full source MP4 and bulk decoded frames stay local; selected source frames appear in clearly attributed side-by-side comparisons.

## Reproduce

Requires Blender 4.5, Python with OpenCV/Pillow/NumPy/requests/yt-dlp, and Node.js to rebuild the viewer. The source geometry can be rebuilt without downloading reference media.

```sh
python scripts/acquire_video.py
python scripts/extract_video_frames.py references/tour.mp4
BAHEN_REV=rebuilt blender -b --python scripts/build_model.py
BAHEN_REV=rebuilt blender -b bahen-centre.blend --python scripts/render_views.py -- video_1430 video_1452 video_0030 video_0330 video_0630 video_0730 exterior
python scripts/make_textures.py
blender -b bahen-centre.blend --python scripts/export_model.py
cd viewer
npm install
npm run build
cd ..
python scripts/assemble_viewer.py
```

Serve with `python -m http.server 8766` and open `http://localhost:8766/viewer/`. `scripts/test_viewer.py` checks model loading, view presets, controls, screenshots, keyboard movement, mobile layout and offline loading. `scripts/audit_glb.py` checks embedded assets and geometry. `scripts/check_camera_anchors.py` projects a small set of manually identified source points; it does not certify full-image similarity. Set `BAHEN_WIDTH`, `BAHEN_SAMPLES` and `BAHEN_CHROME` as needed.

## Sources and credits

- [APS162: Form versus Function — A Tour of the Bahen Centre](https://www.youtube.com/watch?v=GGaJsGu_5zA&t=892s), University of Toronto Faculty of Applied Science & Engineering. Actual timestamps00:30,03:30,06:30,07:30,14:30 and 14:52 drive the published comparisons. [Full source record](review/sources.json).
- [University Planning, Design & Construction](https://updc.utoronto.ca/project/bahen-centre/), supplementary architectural photographs; credits include Roberta Baker and Makeda Marc-Ali.
- [University of Toronto Campus Events](https://campusevents.utoronto.ca/event-spaces/centrally-shared-spaces/bahen-centre/), supplementary atrium photographs and event-space plan.

The workflow and geometry helpers draw on the adjacent `astra-house` project. Material tiles and noticeboard graphics are authored approximations. The architecture is actual editable 3D geometry; no reference photographs are used as geometry substitutes. Three.js uses the [MIT license](licenses/THREE-LICENSE.txt).
