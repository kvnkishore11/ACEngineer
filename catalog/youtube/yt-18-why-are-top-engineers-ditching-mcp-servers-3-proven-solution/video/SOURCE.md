# Video source

- URL: https://www.youtube.com/watch?v=OIKTsVjTVJE
- ID: OIKTsVjTVJE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-18-why-are-top-engineers-ditching-mcp-servers-3-proven-solution.mp4" "https://www.youtube.com/watch?v=OIKTsVjTVJE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
