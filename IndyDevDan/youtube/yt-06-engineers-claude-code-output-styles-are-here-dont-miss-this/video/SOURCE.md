# Video source

- URL: https://www.youtube.com/watch?v=mJhsWrEv-Go
- ID: mJhsWrEv-Go
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-06-engineers-claude-code-output-styles-are-here-dont-miss-this.mp4" "https://www.youtube.com/watch?v=mJhsWrEv-Go"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
