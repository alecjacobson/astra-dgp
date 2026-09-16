# Independent delivery review: R13 exact-video comparisons

Reviewed all six 1440×810 renders against the decoded source at 00:30, 03:30, 06:30, 07:30, 14:30 and 14:52. Comparisons account for the source's 1280×720 resolution. This is a visual review of the actual outputs, not a scene-statistics check.

## Delivery decision

The model is deliverable as a **source-guided architectural approximation with rendered comparisons**. Room2133 is the strongest matched local view. The illuminated stair now has the correct image direction, approximately aligned near handrail endpoints, a connected bottom arrival, dark closed risers with lights, round rails, a real adjacent opening and blue lower guard. Earlier primary blockers of reversed perspective, a floating stair foot and unrelated geometry hiding2133 are resolved in these views.

Do not claim all six cameras or the whole building are geometrically matched. The entrance atrium is still a substantial perspective/layout mismatch. Exact global placement, dimensions, repeated upper-floor layouts, core radius and turning-flight plan remain inferred from incomplete visual evidence.

## Concrete remaining defect to inspect

**Lecture hall aisle,06:30:** a dark slit/band crosses a near aisle step. The script places full-width raked platforms and aisle steps partly coplanar/overlapping. This is a plausible cause of the artifact; it should be inspected and corrected by separating platform/aisle footprints or otherwise eliminating coplanar surfaces. The screenshot alone does not establish an actual floor hole. No other conspicuous floating piece or solid-object collision was found in these six selected renders. This is not a certification of all hidden geometry.

## Remaining source differences

| Frame | Judgment | Material residual difference |
|---|---|---|
|14:52|Pass as local architectural approximation.|Monitor remains a little low/right and hardware darker than source. Poster/screen contents are abstracted. No blocker.|
|14:30|Acceptable source-guided assembly, partial perspective match.|Sloping guard is overly reflective/opaque, while source glass is clear. The projecting ceiling slab dominates more than the source's dark framed overhead zone. Rear noticeboard/bin wall is too distant; room2133 is visible much farther to the right than this source composition establishes. These limit fidelity but are not new structural collisions.|
|00:30|Recognizable street frontage; entry-door blocker resolved.|Four entrance leaves/canopy are now legible. Source glazing is darker/more transparent, louvre bay narrower relative to its height, banner darker purple. Scene lacks street context and camera does not precisely match.|
|03:30|Approximate entrance atrium; **not a matched view**.|Foreground column is present but stair remains a dominant frontal central object. Source stair recedes along the right behind the column, leaving a broad unobstructed central axis. Source bridges are farther away and mat has a curved right perimeter. Heritage window proportions/grid are simplified. This is the largest remaining architectural/camera mismatch.|
|06:30|Source-backed lecture seating assembly; improved composition.|Rounded white chair backs, continuous desks, filled tiers and aisle now read correctly. Camera remains more oblique and source has darker brown finishes. Inspect the aisle artifact noted above.|
|07:30|Recognizable board-wall feature.|Three paired sliding boards and silver frames are present. Bright overhead recess and tight source crop remain different. No apparent collision/floating defect.|

Further improvements should prioritize the03:30 stair/column/camera relationship and14:30 clear glass/background depth. Those are fidelity revisions, separate from the delivery's admitted uncertainty about the unseen floor plan.
