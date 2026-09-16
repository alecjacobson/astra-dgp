# Actual-video comparison targets

Prepared from `scripts/build_model.py` before inspecting decoded tour frames. Values below are existing modeling assumptions in metres; they are **not measured facts about Bahen**. The parent agent is downloading the exact video's archived media via `https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/GGaJsGu_5zA`. The earlier Archive.org advanced-search result was only an empty search index result and does not contradict this successful media route.

## Bounded priority list

| Priority | Hard-coded model relationship | Compare against the decoded tour |
| --- | --- | --- |
| 1 | Eight-storey circular glazed lantern centered at (-10,-10), outer radius 6.85 m, inner glass core radius 4.2 m, rising to 33.75 m; every level contains a 4.8-radian (~275°) curved stair of 28 treads. | Determine whether tour actually shows a full cylindrical tower, a partial curved volume, or several distinct rounded elements. Count visible floors, identify what is inside the glazing, and verify whether this repeated spiral-stair interpretation has any support. This is the largest unverified shape. |
| 1 | Long atrium floor 65 × 11 m, straight X-axis; modern wall at y≈6, heritage wall at y≈-5.45 over x=9…33. | Track the walk: straight vs turning axes, wall-side changes, and how much of the heritage wall continues. Compare width/height ratios and column spacing using multiple frames before changing overall scale. |
| 1 | Floor increments uniformly 4.2 m. East atrium roof at 12.9 m; west roof at 33.8 m with abrupt vertical glazed transition near x=0.5. | Count storeys and roof transitions visible along the route. Test whether the dramatic 20.9 m roof-height step exists, and whether the tour passes into separate spaces rather than one continuous canyon. |
| 1 | Lower east stair starts (27,2.3,0), runs -7 m along X and rises 4.2 m; second starts (17.6,2.3,4.2), also runs -7 m and rises 4.2 m. Both are 1.85 m wide, 25 treads (0.168 m rise / 0.28 m going). | Establish correct handedness and whether flights continue straight, reverse, or turn. Identify actual landing-column-door relations from moving frames, not just the thumbnail. Count tread groups and intermediate platforms if visible. |
| 1 | Transverse bridges at x=7 on z=4.2/8.4, and x=-19 on z=4.2/8.4/12.6. Each 2.4 m wide, 8.8 m span, 0.34 m slab. Additional landing connection at x=18.8 spans 8.7 m. | Count crossings seen from both directions and relate them to stairs and curved glass. Current east camera looks directly under the added landing connection; check that this overhead slab is actually present at a matched tour location. |
| 2 | Two column lines at y=3.3 and y=-3.45; X spacing 8 m; 0.76 m diameter. South row exists only x<8. Capitals are 1.05 × 0.94 × 0.52 m. | Compare bay counts and diameter-to-door/person ratios. Determine which shafts have capitals and which are continuous plain cylinders. Avoid solving camera-distance mismatches by blindly changing diameter. |
| 2 | Landing walkway centered x=18.8, 2.4 m wide; upper floor at z=4.2. Door wall at y=6.05 has three 0.9 × 2.7 m doors at x=16.8,19.6,20.6 and broad plaster piers. Guards 1.15 m high. | Match an unobstructed landing frame, then verify actual number of doors, single/double-door arrangement, exit-sign location, adjacent louvre/void, overhead fascia and luminaire spacing. Door labels in model are fabricated from coordinate values and require replacement if readable. |
| 2 | Heritage masonry original geometry scaled vertically by 0.83: base ≈1.0 m, main window rows roughly z=1.66…4.565 / 5.478…8.383 / 9.296…11.786. Six window bays at x=12,16,20,24,28,31.2, mostly 2.5 m wide. | Verify actual number of storeys/bays and relative window sizes. Look for arched blank openings, copper ledges and grille placement. Current uniform rectangular fenestration is simplified. |
| 2 | Modern louvres are identical 6.6 m panels every 8 m, 18 slats each, 0.13 m vertical pitch; two rows starting z=4.9/9.1. Purple fascia and fluted glazing occur on west/south side. | Count occupied bays and compare screen vertical extent, missing bays near stairs, slat openness and whether purple fascia/fluted glazing face the modeled direction. |
| 3 | Exterior shells: north main wing 68 × 22 m, 21 m roof; upper block 30 × 22 m, 33.8 m roof; west wing 15 × 18 m, 29 m roof; Koffler context 24 × 21.8 m, 12.3 m roof; retained house 6 × 7 m with ridge at 13.5 m. | Only revise these with actual exterior tour coverage. Check relative masses and continuity; do not infer whole-building accuracy from interior frames. |

## Current camera assumptions

| Camera | Position → target | Lens | Issue to resolve with actual video |
| --- | --- | --- | --- |
| atrium_east | (12,-0.8,1.75) → (32.6,0.1,4.9) | 25 mm | Elevated aim and close overhead crossing can differ substantially from tour framing. |
| atrium_west | (16,-0.7,1.8) → (-12,0,5.3) | 26 mm | Match identifiable column/bridge occlusions before judging depth. |
| landing | (18.8,-2.1,5.85) → (18.6,6.05,5.7) | 23 mm | Eye height is 1.65 m above landing; broad FOV and foreground column scale must be matched. |
| lantern | (-1,-1,2) → (-12,-7,16) | 20 mm | Strong upward wide-angle composition can exaggerate the unverified tower interpretation. |
| exterior | (84,-87,62) → (-1,1,12) | 47 mm | Presentation aerial; not an evidence-matched camera. |

## Comparison process after decode

1. Verify duration and extract the exact 892-second frame plus nearby frames; preserve timestamps and original aspect ratio.
2. Inspect full-video contact sheets to identify actual spatial sequence and exterior coverage. Select clear, repeated anchors: a door bank, column joint, bridge edge, heritage sill or glazing corner.
3. For each selected timestamp, create a camera-matched model render. Match aspect ratio, camera height, aim and approximate FOV before treating projection differences as geometry errors.
4. Review side-by-side pairs for structural correspondence first: occlusion order, floor count, stairs/door connections, bridges, curved mass and roofline. Record specific evidence-supported changes.
5. Use fixed cameras for before/after renders. Material polish follows topology and proportions. Do not count successful decoding as a successful reconstruction comparison.

Update stale scene metadata (`scene['evidence']` currently says exact 14:52 unavailable) only after the local video and timestamp frames are verified. Preserve the earlier preview-only reviews as historical iterations, not current full-video validation.
