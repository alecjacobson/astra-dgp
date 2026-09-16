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
