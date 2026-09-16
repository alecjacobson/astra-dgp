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
