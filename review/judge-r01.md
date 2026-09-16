# Independent render review — R01

Judged actual `r01-atrium_east.png`, `r01-atrium_west.png`, and `r01-exterior.png` against official photographs `references/judge/events-3.jpg`, `events-4.jpg`, `events-6.jpg`, the requested video's thumbnail, and recovered public previews `video-sd1.jpg` through `video-sd3.jpg`. These previews are not a decoded tour sequence and do not prove the requested timestamp has been recovered.

Overall: the model already communicates the distinctive heritage/modern atrium contrast, free concrete columns, louvres, bridges, glass guards, and curved glazing. It is an architectural approximation with visibly unresolved geometry and rendering artifacts. The following fixes will produce a much larger gain than adding small furniture.

## Ranked changes

1. **Remove the visible white light disc.** `atrium_east` contains a giant circular white disc behind the entrance curtain wall. It is a lighting artifact, not architecture, and dominates the entire composition. Disable camera/transmission visibility for the fill light if supported, relocate it above/outside the view, or replace its fill contribution with a suitably hidden source. Verify through glass with an actual follow-up render.

2. **Rebuild the heritage window surrounds as brick-dominant.** Both interior renders show giant pale stone rectangular frames and broad projecting lintels. `events-3` has an ochre/yellow-brick wall, brick reveals/pilasters, much less conspicuous pale stone sills, dark barred lower windows, and occasional pale arch-shaped infill. Change deep reveals and most lintels to masonry, reduce stone projection/brightness, add dark narrow window grilles, and make base stone warmer/darker. The reference wall's brick detail should remain the dominant texture. The current treatment changes the apparent architectural period and material identity.

3. **Correct the east stair placement and approach clearance.** In `atrium_east` the large stair occupies the central foreground of the entrance glass, with a projecting intermediate landing. In `events-3`, stair flights remain tightly along the modern side and the broad door bank and central walking route stay open. Move the stair toward the modern wall, re-check its run direction against the reference and landing thumbnail, and compose a matching eye-level image. Exact handedness is not established from all previews alone; do not claim a measured stair plan.

4. **Simplify the entrance glazing grid and strengthen its doorway surround.** Current grid has roughly seven narrow columns and many equal horizontal tiers, creating a dense office curtain-wall appearance. `events-3` has three broad principal vertical glazing bays and a few major horizontal divisions above a substantial pale portal surrounding a bank of doors. Make those coarse structural divisions visible and keep the door hardware as secondary detail.

5. **Replace stretched concrete grain with subtle isotropic variation.** The R01 columns look heavily streaked/granular along their height. Official photos have smooth cast concrete with restrained mottling, occasional form marks and ring joints. Use object/world-scale noise so tall cylinders do not stretch noise longitudinally, reduce bump substantially, and retain readable joint rings. The current bright blocklike capitals also need less contrast and slightly restrained size.

6. **Make the terrazzo read as a continuous surface.** Current floor is dominated by frequent, dark, large-format rectangular tile seams. Official floor shows fine black/white aggregate and only occasional subtle joints. Reduce seam density and contrast; keep fine aggregate and broad, soft reflections. Avoid adding stronger mirror reflections.

7. **Match louvre panel vertical reach.** References show large dark screens descending toward the ground-storey heads, including a few widely separated bottom slats and visible transparent areas behind. Current screens appear as compact, nearly identical bands neatly centered on each upper floor. Extend selected screens downward, vary the last few gaps, darken the timber slightly, and preserve visible depth. This is more useful than adding more identical panels.

8. **Treat exterior as schematic until independently verified.** `r01-exterior` exposes the interior gallery facade at roof level; the huge circular glazed tower, roof heights, flat heritage context block and surrounding wings are not established by the images inspected in this review. The model's exterior is coherent as an explanatory massing/cutaway image, but cannot yet be called a faithful exterior reconstruction. Keep the roofline complete or explicitly caption as an architectural cutaway; check the street-level glazed bay and incorporated house against `university-3/4` with a street camera.

## Video-preview details to preserve

- `thumb.jpg`: pale blue frosted guards, gray metal posts, dark wood handrail, dark door wall behind the landing, large round column to right, left stair and horizontal louvres.
- `video-sd1.jpg`: dark timber continuous built-in seat with tall back, white wall piers, dark skirting, terrazzo floor.
- `video-sd2.jpg`: purple-gray horizontal fascia above white wall, dark horizontal guardrail over an opening, a large jointed cylindrical column and timber bench.
- `video-sd3.jpg`: gray double doors with narrow dark windows and vertical handles, pale stairwell walls, red EXIT sign and red rectangular indicator; a brick wall is visible beyond the high glazing.

## Next render acceptance

Re-render the same east/west cameras after fixes 1–6 so changes can be compared directly. Add a thumbnail-like landing view and a modern-side atrium view that shows the curved glass volume, void railing, fascia and bench. Do not use a numerical similarity score: cameras, dates and available evidence differ. Record fixes individually and retain these R01 images as the before state.
