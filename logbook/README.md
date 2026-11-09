# LOGBOOK — MVP 0.1

A minimal, private-first life log that combines notes, voice recordings, image collages, links that require an observation, and tasks. Designed primarily for iPhone Safari, with automatic local saving in IndexedDB.

## Start

Upload the entire contents of this folder into a web-accessible directory (for example GitHub Pages under `/logbook/`), or run a local HTTP server in the folder (`python -m http.server 8000`). On iPhone, open the secure URL in Safari and choose Share → Add to Home Screen.

## What works

- Write text notes; quick capture bar, with draft recovery.
- Attach up to 20 images; automatic editorial layouts; originals stored as blobs.
- Record audio when the browser provides `MediaRecorder` and microphone permission; recordings are saved locally. **Automatic transcription is not included**; iPhone keyboard dictation can be used for text notes.
- Tasks, pins, subtasks, timestamps, project labels, completion.
- Save inspiration only after entering a valid URL and an original observation or connection.
- One chronological archive and text search.
- Light and dark themes (System follows device preference).
- Five-source feed reader: headlines are gathered via the GitHub Actions workflow into `feeds.json`, *not* fetched from arbitrary remote RSS servers by the phone.
- Offline app-shell service worker after first load (fonts may fall back to the system font offline).
- Full ZIP backup/restore including original image/audio blobs, using a stored (uncompressed) ZIP format. Archive import intentionally replaces existing entries after a confirmation.
- One-tap import of original To Do tasks in `localStorage['minimal-todo-v1']`, if hosted under the same browser origin. The original To Do app remains untouched.

## Important limits

- Data is **per browser installation**, not shared across devices. Back up routinely, especially before iOS storage cleanup or device replacement.
- Photo/audio files can make the ZIP very large. A 350 MB restore limit helps avoid iPhone memory exhaustion.
- The feed updater needs GitHub Actions enabled with `contents: write` permissions. Scheduled runs may be delayed; defaults are public sources that can be changed in `scripts/refresh_feeds.py`.
- The MVP does not implement social publishing, Studio Visit import, automatic transcription, multi-device sync, or arbitrary feed subscription editing.
- The current typography uses Instrument Sans online (Google Fonts) with iOS system font fallback. For a future fully offline release, bundle a properly licensed copy of the font.
- No personal entry data is ever written into the public GitHub repository or sent to the feed updater.