#!/usr/bin/env bash
# Records one game being played by the app's DEBUG auto-demo: the game opens straight from launch
# with no client selected (nothing is saved), and ~1.5 s after it appears the demo plays one real
# attempt through the game's own touch handling. The first trial of a round is always a make.
#
#   bash tools/screenshots/record_game.sh <simulator name or udid> <game id> <seed> <out.mp4> [seconds]
#
# The raw recording is the simulator framebuffer: portrait, with the landscape app sideways.
# tools/screenshots/make_clips.py turns it into the 5-second clip the site uses.
set -euo pipefail

device="$1"; game="$2"; seed="$3"; out="$4"; seconds="${5:-9}"
bundle=com.bananastandard.speechtherapy

xcrun simctl terminate "$device" "$bundle" >/dev/null 2>&1 || true
sleep 1

# recordVideo runs until it gets SIGINT, which is also what finalises the file.
xcrun simctl io "$device" recordVideo --codec=h264 --force "$out" >/dev/null 2>&1 &
recorder=$!
sleep 1.5

SIMCTL_CHILD_LAUNCH_STRAIGHT_TO_GAME=1 SIMCTL_CHILD_GAME_ID="$game" SIMCTL_CHILD_MARKING=2 \
  SIMCTL_CHILD_WORD_AUDIO=0 SIMCTL_CHILD_SESSION_SEED="$seed" SIMCTL_CHILD_AUTO_DEMO=1 \
  xcrun simctl launch "$device" "$bundle" >/dev/null

sleep "$seconds"
kill -INT "$recorder"
wait "$recorder" || true
echo "recorded $game -> $out"
