# Video source

- URL: https://www.youtube.com/watch?v=nGhsgdQplHw
- ID: nGhsgdQplHw
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-13-claude-code-2-0-agentic-coding-no-other-agents-arent-even-cl.mp4" "https://www.youtube.com/watch?v=nGhsgdQplHw"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
