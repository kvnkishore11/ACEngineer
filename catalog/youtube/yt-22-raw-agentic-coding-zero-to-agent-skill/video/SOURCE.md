# Video source

- URL: https://www.youtube.com/watch?v=X2ciJedw2vU
- ID: X2ciJedw2vU
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-22-raw-agentic-coding-zero-to-agent-skill.mp4" "https://www.youtube.com/watch?v=X2ciJedw2vU"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
