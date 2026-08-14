# Video source

- URL: https://www.youtube.com/watch?v=zTcDwqopvKE
- ID: zTcDwqopvKE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-23-agent-experts-finally-agents-that-actually-learn.mp4" "https://www.youtube.com/watch?v=zTcDwqopvKE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
