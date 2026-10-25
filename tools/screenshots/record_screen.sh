#!/usr/bin/env bash
# Records the simulator screen for a fixed number of seconds, for clips driven by hand (the
# History clip on Home was recorded this way while its filters were tapped).
#
#   bash tools/screenshots/record_screen.sh <simulator name or udid> <seconds> <out.mp4>
set -euo pipefail

device="$1"; seconds="$2"; out="$3"

# recordVideo runs until it gets SIGINT, which is also what finalises the file.
xcrun simctl io "$device" recordVideo --codec=h264 --force "$out" >/dev/null 2>&1 &
recorder=$!
sleep "$seconds"
kill -INT "$recorder"
wait "$recorder" || true
echo "recorded ${seconds}s -> $out"
