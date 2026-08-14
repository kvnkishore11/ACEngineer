# Video source

- URL: https://www.youtube.com/watch?v=TqjmTZRL31E
- ID: TqjmTZRL31E
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-37-pi-ceo-agents-claude-1m-context-multi-agent-teams.mp4" "https://www.youtube.com/watch?v=TqjmTZRL31E"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
