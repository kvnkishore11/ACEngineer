# Video source

- URL: https://www.youtube.com/watch?v=u-SQ0Jsv4mI
- ID: u-SQ0Jsv4mI
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-24-top-2-engineering-plan-2026.mp4" "https://www.youtube.com/watch?v=u-SQ0Jsv4mI"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
