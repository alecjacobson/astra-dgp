# Final polish judgment — R20 native renders

**Final visual verdict: PASS — native R20 renders and final browser presentation.**

Final browser approval was completed at 19:49 UTC after the theatre material correction and scoped cutaway improvement. Earlier pending verdicts below document the render-loop history; the final verdict supersedes them.

I inspected all eleven1920-pixel R20 renders: the14:30 stair,14:52 room2133, offset door, alternate lobby, lecture seating, chalkboards, street entrance, entrance atrium, overall exterior and both general atrium views. The native set satisfies the finite polish gate established in `judge-polish-r17.md`. I found no remaining native visual defect that warrants another geometry revision before delivery.

## Verified improvements

- The illuminated stair meets its arrival floor, with the unintended foreground gap filled and the intentional adjacent void retained. Fine terrazzo aggregate and localized lamp reflections are now visible. Soft lighting preserves the stair's form without the earlier harsh sunlight divide. The blue lower guard, clear upper/sloping glass, round rails and near-background board/bin/screen hierarchy form a coherent architectural scene.
- The2133 frontage and its offset view have consistent door depth and continuous dark rebates. The earlier conspicuous dotted/zipper artifact is no longer a material distraction. Silver hardware, the corrected2139 plaque, actual monitor content and source-derived notice textures are attached and readable as modeled objects. The offset views do not expose a one-camera facade trick.
- Lecture seating now dominates the06:30 composition, with a clean continuous side aisle and dark timber enclosure. The previous black aisle band and excessive empty upper wall are resolved. The board-wall view has controlled patina, silver frames and a strong illuminated ceiling recess.
- The entrance atrium retains its open central axis, stair behind the right column and curved mat boundary. Street entry doors/canopy are legible. The overall exterior now places the core/stair behind a distinct glazed enclosure and roof rather than presenting the interior stair as an open-air stack.
- General atrium views show coherent floor, gallery, column and guard relationships without a newly conspicuous collision, floating object or missing foreground surface in the reviewed images.

## Remaining limits to disclose, not reasons for another native iteration

This is an architectural reconstruction from moving video and supplemental visual evidence. Whole-building dimensions, some envelope planes, upper-floor repetition and unseen room registration remain inferred. Several cameras are close source-guided compositions rather than exact camera solves. Fine printed details retain the source video's resolution and motion blur; the lobby noticeboard texture is a documented partial source composite. Native monitor colors remain somewhat less saturated than the original screen image. Those limitations should remain in the delivery notes.

The native result is visually finished enough to deliver under that stated scope. Increasing samples or making further small landmark adjustments is unlikely to provide material benefit at this stage. Keep the geometry frozen unless export/browser inspection exposes a real new defect.

## Final pending gate

Inspect the baked/exported browser presentation once available, specifically:

1. Main stair and door retain material depth and source textures without bake seams, black patches or lost transparency.
2. UI does not obscure the focal architecture at the preset cameras, including mobile layout.
3. Closed enclosure and deliberate cutaway are distinguishable, with no accidental missing-shell state.
4. Camera navigation and screenshot output show the approved scene rather than an obsolete asset.

A browser pass can be appended here without reopening the native visual work. Functional file/GLB checks remain the main agent's separate validation responsibility.

## Browser inspection — 19:34–19:37 UTC captures

Inspected desktop stair, room 2133, chalkboards, exterior, street, east atrium and cutaway, plus both 390 × 844 mobile stair/room captures. The browser retains the finished stair geometry, material depth, clear glass and source-derived notices. The monitor now preserves the original purple screen colors. The desktop controls occupy their own sidebar and the mobile controls collapse below the view; neither covers the focal stair or room entry. The closed exterior and explicitly selected open cutaway are visibly distinct.

The initially exported lecture chairs are black where the native/source chairs are white. This is a material browser blocker, independently visible in the 19:35 theatre screenshot; the main team is correcting the scoped bake/export defect. **Browser verdict remains pending that corrected theatre capture.** No other inspected view currently requires a new geometry iteration.

Minor export limitations remain: thin edge/bake streaks around the room's pale frame are more visible in the mobile crop, and the cutaway retains dark floor shading baked with the shell closed. The latter makes the cutaway less legible than a separately lit presentation. These do not invalidate the primary source-matched views.

### Cutaway correction — 19:42 UTC preview

Inspected `/tmp/bahen-cutaway-neutral.png`. **Cutaway presentation: PASS.** The scoped neutral matte site/foundation treatment removes the large black rectangles while preserving the baked architecture, core, flights, galleries and heritage-wall detail. The pale site reads as a deliberate diagram and clearly improves the open-shell view. The earlier cutaway lighting concern is resolved for this presentation. The corrected theatre chair capture is the only remaining browser visual gate.

### Theatre correction check — 19:43 UTC preview

The repaired chair normals restore white chair backs in `/tmp/bahen-final-lit-theatre.png`, resolving the initial black-surface failure. However, the nearest backs show conspicuous cloudy atlas shading and repeated dark/pink triangular corner seams at normal viewing scale. These are export artifacts rather than source upholstery detail. Recommended the available scoped ordinary-PBR fallback for chair backs, followed by one confirming capture; the rest of the theatre composition passes. Browser approval remains pending that material correction.

## Final browser verdict — 19:49 UTC

**PASS.** Inspected the fresh `/tmp/bahen-final-lit-theatre.png` after ordinary PBR materials replaced the chair-back atlas shading. The chair backs are clean white with legible thickness; the black surfaces, cloudy patches and repeated dark/pink corner seams are gone. Simple close-up edge faceting remains, but no material export defect prevents delivery. The timber enclosure, continuous aisle and tiered seating retain the approved composition.

Together with the previously inspected desktop/mobile primary views and the approved scoped cutaway treatment, this closes the finite visual quality gate. No further geometry or material revision is requested. Functional tests remain the main agent's separate responsibility.

The delivery should still describe the work as a video-guided architectural reconstruction: source-matched focal spaces are better constrained than whole-building dimensions and hidden room registration. Low-resolution source notices, simplified distant geometry and modest residual edge artifacts are visible limits; this review does not certify survey accuracy or photographic equivalence.

Published final browser captures: [theatre](../renders/browser-theatre.png), [cutaway](../renders/browser-cutaway.png), [central stair](../renders/browser-landing.png), [room 2133](../renders/browser-room2133.png), [mobile stair](../renders/browser-mobile-stair.png). Temporary paths above identify historical review captures; these links show the delivered result.
