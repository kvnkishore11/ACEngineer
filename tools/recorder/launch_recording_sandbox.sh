#!/usr/bin/env bash
set -euo pipefail

# Dedicated, isolated Chrome sandbox for AgenticEngineer course recording.
# Purpose: keep recordings immune to user's normal Chrome tabs, notifications,
# external app link-open events, and accidental clicks/pauses.

PORT="${PORT:-9223}"
PROFILE_DIR="${PROFILE_DIR:-/Users/kvnkishore/WebstormProjects/AgenticEngineer/.recording-chrome-profile}"
START_URL="${1:-about:blank}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOG="/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos/recording-sandbox-chrome.log"

mkdir -p "$PROFILE_DIR/Default" "$(dirname "$LOG")"

# Block browser-level notifications/popups in this profile. CDP screenshot capture
# only captures page pixels, but site notifications/popups/tabs can still disturb
# the page state; keep this profile quiet by default.
python3 - <<PY
import json
from pathlib import Path
prefs_path = Path('$PROFILE_DIR') / 'Default' / 'Preferences'
prefs = {}
if prefs_path.exists():
    try:
        prefs = json.loads(prefs_path.read_text())
    except Exception:
        prefs = {}
profile = prefs.setdefault('profile', {})
content = profile.setdefault('default_content_setting_values', {})
content.update({
    'notifications': 2,
    'popups': 2,
    'geolocation': 2,
    'media_stream_mic': 2,
    'media_stream_camera': 2,
    'automatic_downloads': 2,
})
prefs.setdefault('browser', {})['check_default_browser'] = False
prefs.setdefault('credentials_enable_service', False)
prefs.setdefault('profile', {})['password_manager_enabled'] = False
prefs_path.write_text(json.dumps(prefs, indent=2, sort_keys=True))
PY

# If something is already serving the sandbox port, leave it alone and report it.
if python3 - <<PY >/dev/null 2>&1
import urllib.request
urllib.request.urlopen('http://127.0.0.1:$PORT/json/version', timeout=1).read()
PY
then
  echo "Recording sandbox already running on CDP port $PORT"
  python3 - <<PY
import json, urllib.request
pages=json.load(urllib.request.urlopen('http://127.0.0.1:$PORT/json/list', timeout=2))
for p in pages:
    if p.get('type') == 'page':
        print(f"- {p.get('title')} {p.get('url')}")
PY
  exit 0
fi

# Launch separate Chrome instance with isolated user-data-dir. Do not use the
# user's normal Chrome profile; this prevents external links/new tabs from landing
# in the recording browser.
nohup "$CHROME" \
  --user-data-dir="$PROFILE_DIR" \
  --remote-debugging-port="$PORT" \
  --no-first-run \
  --no-default-browser-check \
  --disable-notifications \
  --disable-popup-blocking=false \
  --disable-features=Translate,MediaRouter,AutofillServerCommunication,OptimizationHints \
  --disable-background-networking \
  --autoplay-policy=no-user-gesture-required \
  --new-window "$START_URL" \
  >>"$LOG" 2>&1 &

for _ in {1..80}; do
  if python3 - <<PY >/dev/null 2>&1
import urllib.request
urllib.request.urlopen('http://127.0.0.1:$PORT/json/version', timeout=1).read()
PY
  then
    echo "Recording sandbox ready on CDP port $PORT"
    echo "Profile: $PROFILE_DIR"
    echo "Log: $LOG"
    exit 0
  fi
  sleep 0.25
done

echo "Recording sandbox failed to start on port $PORT. See: $LOG" >&2
exit 1
