# Render / judge / refine record

All renders are generated from actual editable Blender geometry. No generated image is used as a substitute for a model render. References are linked in sources.json and retained locally, outside the public repository.

| Pass | Evidence / finding | Geometry or rendering change | Follow-up |
| --- | --- | --- | --- |
| R01 | University east atrium, video thumbnail and preview frames. Independent judge found visible light disc, oversized pale window surrounds, dense entrance glazing, central stair obstruction, noisy concrete, dark floor grid. | Initial shell, galleries, historic wall, circular stair, screens, campus context. | R02 |
| R02 | Direct comparison exposed excessive low-atrium height, overclose stair camera and unfinished wing shell. | Suppress light emitter camera/transmission visibility; reduce heritage stone trim; brick reveals; broad glass bays; hollow wing construction; metric concrete noise. | R03 |
| R03 | Entrance now reads as three-storey atrium; landing camera still looked into screens. Exterior revealed open upper wing. | Lower eastern skylight and heritage facade; reduce concrete contrast; adjust cameras; create actual upper landing and doors; move louvres clear of access. | R04 |
| R04 | Independent judge found stair crossing the landing door approach, floating contextual heritage roof, raised fascia strip. | Enclose upper wing; build contextual east windows; refine floor vents and heritage grilles. | R05/R06 |
| R05 | Local geometry inspection and camera reframing. | Move ascending second flight to west/left; connect upper landing; triplanar brick mapping; neutral world backdrop. | R06 |
| R06 | Independent final review and portable/browser checks. | Keep heritage contextual roof/walls at same height; flush gallery fascia below landing; extend and reframe landing to reduce apparent column width. | Final renders and judge-final.md |

R05 was an intermediate scene build; it was followed by R06 before another render set. Published ten-minute checkpoints record actual timestamps and rendered views in ../progress/history.md.

## Evidence limits

Three public preview stills and a larger stair-landing thumbnail were recovered from the requested video. Their timestamps are unknown. YouTube required login/bot verification for full video extraction; the exact 14:52 view could not be decoded. Supplemental visual evidence comes from official University of Toronto exterior, atrium and event-space photographs. Exact footprint, floor heights, feature counts/placement, tower dimensions, hidden construction and room layouts are inferred. This is not a measured or photogrammetric model.

The browser uses simplified transparent glazing and environment lighting; the native Cycles scene is the rendering reference. Camera comparisons are qualitative, not pixel-registered or calibrated.

Final packaging closed a 3 m skylight transition gap, set explicit metric display units, and saved a compressed native scene. Final exact-file checks passed for the GLB, offline viewer, and public GitHub Pages viewer; hashes are in delivery-check.json. Browser controls were tested against the preceding R06 export, then the final exported scene was loaded separately online/offline and its landing view checked.

## Video-driven rebuild, R07–R14

The full original MP4 was recovered17:40UTC on2026-09-16 after direct yt-dlp attempts failed. This supersedes the preview-only evidence above.135 frames were decoded across43:01.6; exact892s is frame26760. Independent review traced second-floor2133 → illuminated stair → third-floor Great Hall, and later floors through8.

- **R07:** rebuilt2133 cream/dark door pair, monitor/noticeboard, illuminated stair, curved glazing. First renders exposed collisions with inherited columns/guards and reversed screen convergence of the stair.
- **R08–R09:** removed legacy collisions, replaced21-riser full-storey run with two straight flights and a turn, corrected door crop and room number. Initial global registrations remain inferred.
- **R10:** changed stair camera side/yaw; matched the source's up-left ascent. Adjusted2133 numeral, handle height, projecting screen and dark adjacent door. Joined approach floor to stair foot.
- **R11:** added street louvre bay, punched windows, raked lecture theatre and three banks of sliding chalkboards. Changed horizontal guard direction to follow the source opening.
- **R12:** lowered central-stair camera aim, corrected floor openings, moved lobby background closer, added outer entry door bank and metal-collared columns. Corrected lecture tier height and added repeated upper circulation as inferred geometry.
- **R13:** blue lower guard with clear extension; actual glass thickness; rounded theatre chair profiles; bright aluminum board tracks; low lobby ceiling. Independent judge accepted the14:30/14:52 assemblies as source-guided approximations. Selected720p anchor errors were7–16.4pixels, a local diagnostic only.
- **R14:** separated theatre tiers around the aisle to remove coplanar overlap; moved entrance-side stairs behind the foreground column with true gallery openings; restored exterior roof/enclosure context after the central rebuild; reduced glass roughness. Re-rendered all six video comparison cameras and overall views.

Limits retained explicitly: no measured dimensions, no full camera calibration, concealed rooms and overall footprint are inferred. Some video frames are much more closely reproduced than others. The source presenter is excluded from architectural matching; text on notices/monitor is abstracted. Browser materials/lighting are simplified relative to Cycles.

The final browser screenshot caught an additional export issue: glTF had substituted white for unsupported procedural colors on the central timber rails and theatre desks. Export now converts unsupported procedural colors to their authored palette swatches, while retaining the seven tiled materials. The GLB audit explicitly checks the three dark fallback materials. This changes only portable material export, not the reviewed native geometry.
