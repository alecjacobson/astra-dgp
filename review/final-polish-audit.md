# Final-polish audit: R14 is still an intermediate visual result

This audit applies the user's higher quality bar, replacing the earlier decision that R14 was merely deliverable as an approximation. I inspected the six current comparison sheets, `final-exterior.png`, and browser exterior, central-stair, room2133, east-atrium and theatre screenshots against the actual video frames. The geometry fixes are real, but absence of broken geometry is not sufficient for a polished reconstruction.

## Five highest-impact deficits, ranked

### 1. Reconstruct the14:30 background as a coherent local space

**Evidence:** The source places a dense dark steel/transom grid directly behind the stair, with paper-covered boards near centre-right, a pale wall and a purple-topped recycling station at the right. Its ceiling is a comparatively shallow overhead zone. R14 instead shows a huge projecting tan ceiling wedge, an empty deep hall, the2133 room frontage far to the right, and a small/occluded bin behind the foreground guard. This changes the architecture more than a small stair-camera adjustment could fix.

**Fix:** Establish the depth of the rear wall, screen and guard using the14:30–14:50 moving sequence, then bring the screen/board/bin composition into the source's near-background plane. Shorten/reposition the local ceiling so its leading edge does not become the dominant diagonal across the image. Preserve the observed path onward to2133, but do not place its monitor and doorway prominently in this shot just because they exist in the model. Resolve the locally visible source relationships before propagating them to upper floors.

**Acceptance:** In a normalized1280×720 comparison, the upper field is primarily dark structural framing with the pale lit ceiling behind; no giant tan slab dominates it. A clearly recognizable purple-topped bin is visible against the right wall, rather than hidden by the near guard. The noticeboard and pale wall sit at comparable apparent depth to the source. Main stair caps and bottom contact remain within roughly20px of their established source anchors. A second nearby camera from14:42 or14:50 must show continuous geometry, not a one-view backdrop.

### 2. Replace the global sunlight/olive wash with source-like interior light and material response

**Evidence:** R14's14:30 stair has a harsh diagonal sunlight boundary, nearly black lower half and speckled carpet-like floor. Source light is softer and cooler, and individual riser lamps produce conspicuous localized gleams on polished treads. At14:52 the render wall is dull olive and the lock/lever is dark plastic-like; the source has neutral cream wall/leaf and bright silver hardware. The browser goes to the opposite extreme: flat white walls and floor with little depth.

**Fix:** Use the actual enclosure to control sunlight, then build restrained interior ambient light and visible pendant contribution. Preserve contrast around the riser emitters without crushing the lower stair. Give terrazzo a fine aggregate, smooth overall surface and believable rough reflection; use much quieter variation on the pale lobby floor. Separate aluminum/steel reflection from painted surfaces. Adjust neutral balance through lighting and plausible materials together, rather than applying unrelated per-camera exposure until one image looks acceptable.

**Acceptance:** Treads, risers, newels and wall remain distinguishable across the entire stair; no dominant unexplained hard sun stripe divides it. At least several riser lights create visible soft highlights on adjacent treads. The floor reads as smooth stone/terrazzo at full resolution, not dense uniform gravel.2133 reads as cream under neutral light; silver lever has a light-catching edge and reflection. Adjacent views retain compatible material colors and lighting.

### 3. Replace placeholder close-up details in the user-requested2133 view

**Evidence:** The door framing is now credible, but the monitor is a generic centered heading plus five thick rules; posters are pastel rectangles covered with repeated black bars. The source screen has left-aligned white text on a purple gradient, and the noticeboard has varied densely overlapping printed sheets. The render monitor is too low/right and not cropped by the top edge. The door handle and blank adjacent plaque remain conspicuously simplified at this camera distance.

**Fix:** Use perspective-corrected crops from the supplied video for the screen/noticeboard where the image is unobstructed, or recreate their actual layout at similar visual density. These should be local textures on modeled objects, not a full-frame projection that hides geometry errors. Give the monitor its source tilt/projection and black bezel. Refine the narrow door reveal, frame profile, brushed-silver lock plate and curved lever/neck. Remove the invented blank plaque if its exact position cannot be supported by a nearby source frame.

**Acceptance:** At1280×720 the monitor's source bounds are approximatelyx900–1170 with its top cropped and lower edge near220; door numeral remains aroundx372,y279 and jamb nearx493. The poster area reads as printed notices at normal viewing size, not a repeated procedural pattern. No visible floating text, hard-edged pseudo-text bars or dark plastic hardware. Render at a slightly shifted camera to confirm all details attach correctly to their objects.

### 4. Make the exterior and secondary spaces visually coherent, with clear separation of enclosed building and cutaway

**Evidence:** `final-exterior.png` exposes the entire repeated interior stair stack as though it were an outdoor facade even while the view is called exterior. Roof ends, white slabs and generic repeated window bands read as an assembled massing study. The browser exterior reinforces this with an almost wireframe glass appearance. The00:30 frontage has useful recognizable elements but still frosted-looking glazing, an overly wide louvre field and an undersized/light banner.03:30 has the correct broad stair/column relationship but over-wide heritage windows, overly regular clean masonry and a pointed polygonal mat in place of the source's smooth curved edge.06:30 has the desk/chair motif, but cool gray room finishes replace the source's dark brown enclosure;07:30 misses the principal bright ceiling recess.

**Fix:** Resolve which atrium surfaces form the real exterior enclosure from the video/public reference evidence; use an explicit cutaway state for deliberately removed shell surfaces. A polished exterior should have continuous credible envelope edges, recessed openings and termination details. Refine the source-supported street face before spending effort on uncertain roofs. In the secondary interiors, correct high-area material/shape differences: heritage openings, curved mat, wood-toned lecture enclosure, and illuminated board-wall recess. These matter more than increasing component count.

**Acceptance:** Closed exterior and cutaway views look intentionally different; the closed view does not accidentally expose indoor circulation as an unenclosed outdoor staircase. Roof/glazing interfaces have believable connections.00:30 glass reveals depth and reflections rather than reading as opaque gray panels.03:30 mat has a smooth curved boundary and heritage openings resemble the source proportions.07:30 has the source's bright recess as a clear architectural feature. Unverified massing stays explicitly described as inferred; visual polish must not imply measured accuracy.

### 5. Bring the interactive presentation to the same finish as the rendered model

**Evidence:** Browser room2133, central-stair and lecture screenshots are flat and very bright compared with the offline renders. The fixed control panel covers much of the very architecture selected by the camera; in the stair screenshot it hides the left rail and stair edge, and in room2133 it hides the adjacent-door context. Thin structural lines shimmer/alias, and procedural-material details do not consistently survive export. The theatre camera remains more oblique than the source, while the board camera includes a large empty left wall and foreground desk absent from the source framing.

**Fix:** Give the viewer reliable environment illumination, contact/depth cues and restrained exposure; ensure glass and metallic materials survive GLB export with intentional appearance. Bake or otherwise carry the important material textures needed for the close views. Frame camera presets inside the actual unobscured viewport, or collapse controls when selecting a cinematic view. Match theatre/board presets to the source before saving final screenshots. Make the initial hero a finished source-supported composition, with an easy route to the full building overview.

**Acceptance:** At desktop and mobile widths, the principal stair, door or board feature is visible without manually hiding a panel. Browser walls/floors preserve readable depth, glass is transparent with controlled reflections, and metal looks distinct from painted surfaces. A screenshot from each preset has no overlay-obscured focal feature, clipping through walls, missing textures or obvious aliasing at normal display size. Viewer and offline materials have compatible colors even if they use different rendering techniques.

## Quality gate

Do not stop after increasing resolution or sample count. Re-render the two primary pairs after items1–3, judge them at equal scale without reading their labels, then verify one adjacent camera for each. Follow with the six comparison sheets and a browser check after items4–5. The final should read as an intentionally finished architectural reconstruction whose uncertain dimensions are candidly stated—not as procedural blockout geometry made acceptable by the word “approximate.”

The current known floor-gap, stair-foot and lecture-aisle defects remain resolved. They should not be reopened merely for further iteration; new work should address the visual deficits above.
