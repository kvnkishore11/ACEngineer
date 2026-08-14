# Video source

- URL: https://www.youtube.com/watch?v=yBcmIoA-vGs
- ID: yBcmIoA-vGs
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-44-engineers-delete-the-bash-tool-agentic-security-for-pi-agent.mp4" "https://www.youtube.com/watch?v=yBcmIoA-vGs"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
