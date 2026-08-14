# AgenticEngineer Course Videos — Manifest
*Auto-generated while you slept*

## Completed Work (This Session)

### 1. TAC-3 Video Assembled ✅
- **File:** `tac-3/tac-3-combined.mp4`
- **Duration:** 46.7 minutes
- **Resolution:** 1920×1080
- **Size:** 74 MB
- **Source:** 2,861 frames @ 1fps + success-is-planned_audio.aac

### 2. TAC-4 Frames Extracted ✅
- **Directory:** `tac-4/frames/`
- **Frames:** 1,469 frames extracted from existing `afk-agents.mp4`
- **Note:** The existing MP4 is only 24.5 min (audio is 46:24). The video download was incomplete.

### 3. Batch Processing Script Created ✅
- **File:** `process_media.sh`
- **Usage:** `cd videos/tac-X && ../process_media.sh .`
- **Features:**
  - Auto-extracts frames from any MP4 at 1fps
  - Combines frames + audio into a combined MP4 (if frames ≥ audio duration)

## Current Media Inventory

| Lesson | Audio | Video | Frames | Combined Video | Status |
|--------|-------|-------|--------|----------------|--------|
| TAC-1 Hello Agentic Coding | ✅ 21:51 | ❌ | ❌ 0 | ❌ | Audio only |
| TAC-2 12 Leverage Points | ✅ 47:12 | ❌ | ⚠️ 105 | ❌ | Audio + partial frames |
| TAC-3 Success is Planned | ✅ 46:30 | ❌ | ✅ 2,861 | ✅ **Done** | **Full video created** |
| TAC-4 AFK Agents | ✅ 46:24 | ⚠️ 24:5 min | ✅ 1,469 | ❌ | Partial video + frames |
| TAC-5 Close the Loops | ✅ 53:36 | ❌ | ⚠️ 773 | ❌ | Audio + partial frames |
| TAC-6 Let Your Agents Focus | ❌ | ❌ | ❌ | ❌ | Transcript only |
| TAC-7 ZTE Secret | ❌ | ❌ | ❌ | ❌ | Transcript only |
| TAC-8 The Agentic Layer | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-1 Elite Context Engineering | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-2 Agentic Prompt Engineering | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-3 Building Specialized Agents | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-4 Multi-Agent Orchestration | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-5 Agent Experts | ❌ | ❌ | ❌ | ❌ | Transcript only |
| AH-6 Building Agentic Layers | ❌ | ❌ | ❌ | ❌ | Transcript only |

## Blockers

### Video Download (Lessons 6–14)
- **Issue:** agenticengineer.com requires authenticated session
- **Attempted:** Chrome CDP on port 9223 (blocked by "Allow remote debugging" permission prompt)
- **Attempted:** browser-harness (requires Python 3.11+ — installed, but daemon can't handshake due to prompt)
- **Cannot proceed without:** You clicking "Allow" in Chrome for remote debugging, OR providing a fresh auth session

### TAC-1, TAC-2, TAC-5 Combined Videos
- **Issue:** Incomplete frame sets (0, 105, 773 frames respectively)
- **Need:** Full video downloads to extract complete frame sets, OR another source of frames

## What You Can Do Next

1. **Approve CDP prompt** → I can connect to your Chrome and extract remaining video URLs for yt-dlp download
2. **Provide yt-dlp commands** → If you know the working download command from your earlier tests, I can batch-download the rest
3. **Use the batch script** → Drop any new MP4s into the lesson directories and run `process_media.sh`
4. **TAC-3 is ready to watch** → `tac-3-combined.mp4` is a full 46-minute 1080p video

## Transcripts (All 14 Lessons Available)
- **Location:** `~/Downloads/tac-transcripts/`
- **Format:** WebVTT (consolidated, high-quality)
- **Deep-dive analyses:** Already exist in `~/WebstormProjects/AgenticEngineer/output/`
