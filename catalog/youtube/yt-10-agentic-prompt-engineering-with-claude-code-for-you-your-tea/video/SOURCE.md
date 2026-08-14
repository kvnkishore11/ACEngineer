# Video source

- URL: https://www.youtube.com/watch?v=luqKnexhpFs
- ID: luqKnexhpFs
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-10-agentic-prompt-engineering-with-claude-code-for-you-your-tea.mp4" "https://www.youtube.com/watch?v=luqKnexhpFs"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
