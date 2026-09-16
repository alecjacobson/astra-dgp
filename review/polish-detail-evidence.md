# Detail evidence for final polish

## Monitor, door and noticeboard

Actual source frames inspected:892,900,905,910,915,920 and925seconds.

- **Readable monitor headline:** “First Year Fridays: Writing Under Pressure”. Clearest in `references/decoded/00900.00s.jpg` and `references/judge-route/0905.jpg`. It wraps over two lines, left aligned, bold white. Background grades from saturated blue-purple at top to pink/lilac near bottom. A smaller left-aligned date/location line follows, then approximately four to five lines of smaller body copy. Tiny white mark/footer at bottom-left. I cannot confidently transcribe the date/location/body and recommend a source crop or illegible-density treatment, not guessed wording. The existing “Department of Computer Science / News and Events” heading is unsupported.
- **Monitor construction:** thick black rectangular bezel, visibly projects from wall and is slightly angled; the source892crop cuts its top edge. Screen is bright enough to remain distinctly purple under the room lighting.
- **Cream2133 door hardware:** tall bright silver/chrome rounded rectangular backplate, a dark inset reader area, a small circular feature near its upper end and smaller details low on the plate. A rounded projecting neck carries a short left-pointing lever with a flattened/rounded grip. The large U-shaped feature underneath in the video is a cast shadow, not another piece of hardware. Keep the narrow reveal and matching cream frame subtle. Source925provides the cleanest oblique hardware silhouette.
- **Adjacent plaque correction:** the plaque between the timber door and cream2133 reads **2139**, clearly visible at925s. My earlier recommendation to remove the unsupported duplicate2133 was correct about the number, but the plaque itself is real. Restore a silver/gray room plaque with2139 near its top, rather than a blank plaque or duplicated2133. The dark timber door has its own simple silver lever and a separate small circular lock above it.
- **Noticeboard density:** at892/905the visible right-hand strip is almost completely covered by overlapping sheets, with only narrow areas of black backing. Most papers are white/off-white with varied black headings and imagery; there are a few orange/pink/colored flyers. The orange exam flyer visibly stacks “LSAT / MCAT / GMAT”. Papers overlap, have different sizes and some curled/protruding edges. Do not make the board primarily a scattering of clean pastel rectangles with identical ruled text. Exact total sheet count cannot be established from the cropped view.

## Interior core versus exterior enclosure

Actual source980and1005seconds, plus university event photos `events-4.jpg` and `events-5.jpg`, establish that the curved glazed surface is an **interior room/frontage**. The stair occupies the atrium outside that curved room; galleries and another interior facade lie across the void. At1005the landing joins a warm-lit interior gallery with cylindrical pendants and a timber door. Neither frame supplies a surveyed exterior enclosure plane.

Additional primary photographic evidence: [Terri Meyer Boake, University of Waterloo architecture teaching gallery](https://www.tboake.com/sustain_casestudies/bahen_gallery.html), photographs credited there to Nathaniel Lloyd. Downloaded `references/judge/boake-10a.jpg` shows the curved wall clearly: vertically ribbed/translucent cast/channel-glass strips enclosing a room with a ceiling and concrete column. It is not a clear exterior curtainwall. `boake-08b.jpg` shows a tall interior atrium with transom/floor bands and skylight above; `boake-11a.jpg` shows the long enclosed atrium. Use these as evidence, keeping source-image credit if reproduced. The gallery allows educational copying with credit and requires permission for commercial reproduction.

**Geometry recommendation, explicitly inferred within the current model:** keep the curved room wall within a separate rectilinear atrium envelope. The current high skylight spans onlyy≈-5to6, whereas the curved room extends south toy≈-12.8. Therefore the exposed circulation stack is not just missing a front glass pane; it also projects beyond the existing high roof footprint. A coherent provisional enclosure could span from the west-wing inner edgex≈-20.5 to the existing east clerestoryx≈0.5, with its south closing plane aroundy≈-14.5to-15and upper roof atz≈33.8; extend the east return fromy≈-14.5to-4.5and extend the skylight over this added atrium width. This leaves clearance outside the curved room and connects to the existing high roof. Its lower edge must connect to the actual cafe/podium shell, with existing floor intersections inspected rather than merely covered.

Those coordinates are a bounded coherence fix for the current registration, **not measurements recovered from the video**. Existing source evidence supports a roofed atrium enclosing the core/stair, translucent curved interior rooms, and rectilinear wings; it does not establish those exact dimensions or facade bay counts. Tag the new closing surfaces for cutaway mode so the fully enclosed and deliberately open views remain distinct.

## Texture extraction coordinates

All coordinates are in original1280×720 pixel space, ordered top-left, top-right, bottom-right, bottom-left. New raw samples were decoded directly from `tour.mp4` without editing.

| Object | Raw frame | Four source corners | Limit |
|---|---|---|---|
|Monitor active screen|`references/judge-route/detail-0898.00.jpg`|`[(910,20),(1179,69),(1169,254),(898,229)]`|Full active image visible, black bezel excluded. Preserve its two-line headline and gradient.|
|Room2133 noticeboard texture patch|`references/judge-route/detail-0891.30.jpg`|`[(1068,24),(1235,62),(1221,503),(1037,549)]`|Complete unobstructed paper grouping; camera-motion blur. Includes overhanging sheets and narrow wall margin below/along edges, not just the black backing rectangle.|
|14:30 lobby board partial texture|`references/judge-route/detail-0885.50.jpg`|`[(596,108),(726,101),(722,254),(595,258)]`|Sharp partial patch on left backing, above horizontal rail and left of thick upright; does not recover the complete board.|

I could not find an unobstructed whole14:30board: the foreground steel grid and guard remain across it. `detail-0886.00.jpg` reveals more of the full board, but a full projection from that frame would incorrectly bake the foreground post/rail into the board texture. The partial patch above is a cleaner local material source.

R15 backdrop note: moving the too-near wall/board/bin plane away is consistent with source perspective, but keep the source bin's apparent width:height near1.5. If its height is enlarged after moving, enlarge width proportionally. A thin table appears on each side of the bin; a small wall directory sits immediately right of the noticeboard. Preserve the rightmost dark-grid post's approximate normalizedx790–810 anchor while adjusting depth.
