# Video source

- URL: https://www.youtube.com/watch?v=RvowJ_hmLps
- ID: RvowJ_hmLps
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-40-the-first-unshipped-model-claude-mythos-senior-engineer-brea.mp4" "https://www.youtube.com/watch?v=RvowJ_hmLps"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
