# Video source

- URL: https://www.youtube.com/watch?v=SEI_qIW4o2c
- ID: SEI_qIW4o2c
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-57-engineers-your-software-factory-needs-agent-sandboxes-to-sca.mp4" "https://www.youtube.com/watch?v=SEI_qIW4o2c"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
