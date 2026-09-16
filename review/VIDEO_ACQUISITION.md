# Full-video acquisition — second pass

The user requires actual video frames and render comparisons, not preview thumbnails. The existing model remains a first draft until that comparison is performed.

On 2026-09-16 the downloader was upgraded with the default dependency group (`yt-dlp` 2026.08.19, EJS 0.8.0). The original Node 20 runtime was below the solver's current minimum; Node 24.21.0 was installed and explicitly selected. FFmpeg 7.0.2 is available locally.

Tests so far:

- Default downloader with supported runtime: YouTube `LOGIN_REQUIRED`, “Sign in to confirm you're not a bot”.
- Chrome cookie import: no browser cookie database available.
- Android VR, iOS, TV, Safari, embedded and alternate TV clients: login challenge or unavailable player response.
- Actual Chrome playback: same login challenge; video has no streaming URL.
- Mobile web with the documented proof-of-origin provider, including a successfully generated player token: same login challenge.
- IPv6: unavailable in this environment.
- Clean GitHub Actions runner, Python 3.12 / Node 24 / FFmpeg: same login challenge. [Attempt log](https://github.com/alecjacobson/astra-dgp/actions/runs/35128273456).
- Independent agent checked official course/instructor hosting: no verified alternate video file. See judge-video-source-search.md.

No downloaded full video or timestamped decoded frames are claimed by this record. `scripts/extract_video_frames.py` will decode a supplied video, require that it contains 14:52, verify frame indices and produce timestamped contact sheets. Reference images remain local by default.

## Resolved: complete original video acquired, 2026-09-16 17:40 UTC

After the yt-dlp, browser, PO-token and clean-runner attempts above, the Internet Archive's direct YouTube-media endpoint returned the archived MP4 for this exact ID:
`https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/GGaJsGu_5zA`.
It resolves to a 2026-04-25 capture of Googlevideo itag136, video_id=GGaJsGu_5zA. Downloaded with Python requests streaming to local `references/tour.mp4` (288,339,080 bytes). This is the video-only 720p track; audio is unnecessary for frame reconstruction. OpenCV decodes 77,447 frames at30fps, 2581.5667 seconds. `scripts/extract_video_frames.py` successfully decoded135 timestamped frames spanning the entire file, including exact892s frame26760. Full hash and frame metadata are in `review/frame-catalog.json`. The full movie stays local; published comparisons cite short reference frames.

The earlier failure records above are historical and superseded by this successful acquisition.

Reproduction: `python scripts/acquire_video.py` first tries yt-dlp and then the archive media endpoint. An existing complete local MP4 is preserved and its SHA256 reported. The successful local file hashes to `fdb1b1d7fcfa29512ef56a0d6b944976d5178c36e6d563b3dc69018a3fac5d5f`.
