# Video source

- URL: https://www.youtube.com/watch?v=9ijnN985O_c
- ID: 9ijnN985O_c
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-01-i-can-see-everything-claude-code-hooks-for-multi-agent-obser.mp4" "https://www.youtube.com/watch?v=9ijnN985O_c"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
