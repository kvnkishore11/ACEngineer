# Video source

- URL: https://www.youtube.com/watch?v=D1BHGv4gB6c
- ID: D1BHGv4gB6c
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-49-claude-fable-5-banned-the-first-model-agentic-engineers-dont.mp4" "https://www.youtube.com/watch?v=D1BHGv4gB6c"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
