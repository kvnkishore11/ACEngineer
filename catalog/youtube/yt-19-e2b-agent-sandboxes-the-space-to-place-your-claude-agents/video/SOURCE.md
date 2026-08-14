# Video source

- URL: https://www.youtube.com/watch?v=1ECn5zrVUB4
- ID: 1ECn5zrVUB4
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-19-e2b-agent-sandboxes-the-space-to-place-your-claude-agents.mp4" "https://www.youtube.com/watch?v=1ECn5zrVUB4"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
