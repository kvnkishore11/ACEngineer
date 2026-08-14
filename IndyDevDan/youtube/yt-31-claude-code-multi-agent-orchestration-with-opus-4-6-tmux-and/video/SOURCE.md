# Video source

- URL: https://www.youtube.com/watch?v=RpUTF_U4kiw
- ID: RpUTF_U4kiw
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-31-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and.mp4" "https://www.youtube.com/watch?v=RpUTF_U4kiw"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
