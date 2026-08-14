# Video source

- URL: https://www.youtube.com/watch?v=fop_yxV-mPo
- ID: fop_yxV-mPo
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-25-the-codebase-singularity-my-agents-run-my-codebase-better-th.mp4" "https://www.youtube.com/watch?v=fop_yxV-mPo"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
