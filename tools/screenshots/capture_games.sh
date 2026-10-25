#!/usr/bin/env bash
# Captures every game in the FUNunciation app into src/assets/captures/games/<game id>.jpg.
#
# Uses the app's DEBUG straight-to-game launch (RootView: LAUNCH_STRAIGHT_TO_GAME), which starts a
# B session with no client selected, so nothing is saved to anyone's history. Needs a Debug build
# installed on the simulator, and Python with Pillow for the crop.
#
#   tools/screenshots/capture_games.sh <simulator name or udid>
set -euo pipefail

device="${1:?usage: capture_games.sh <simulator name or udid>}"
bundle=com.bananastandard.speechtherapy
out="$(cd "$(dirname "$0")/../.." && pwd)/src/assets/captures/games"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$out"

games=(basketball balloon-rainbow balloon-friends feed skyline rain-garden toy-train firefly-pond
       explorer runway photo-booth pizza food-truck)

seed=11
for game in "${games[@]}"; do
  xcrun simctl terminate "$device" "$bundle" >/dev/null 2>&1 || true
  sleep 1
  # MARKING=2 shows the ✓ ≈ − strip; a different seed per game varies the word on the card.
  SIMCTL_CHILD_LAUNCH_STRAIGHT_TO_GAME=1 SIMCTL_CHILD_GAME_ID="$game" SIMCTL_CHILD_MARKING=2 \
    SIMCTL_CHILD_WORD_AUDIO=0 SIMCTL_CHILD_SESSION_SEED="$seed" \
    xcrun simctl launch "$device" "$bundle" >/dev/null
  sleep 6
  # simctl returns the landscape app sideways in a portrait framebuffer; turn it upright.
  xcrun simctl io "$device" screenshot "$tmp/$game.png" >/dev/null 2>&1
  sips -r 90 "$tmp/$game.png" >/dev/null
  echo "captured $game"
  seed=$((seed + 7))
done

# Drop the status bar, keep exactly 4:3, and save a 1600 px JPEG.
python3 -I - "$tmp" "$out" <<'EOF'
import os, sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
for name in sorted(os.listdir(src)):
    im = Image.open(os.path.join(src, name)).convert('RGB')
    top = round(im.height * 0.027)
    h = im.height - top
    w = round(h * 4 / 3)
    x = (im.width - w) // 2
    im = im.crop((x, top, x + w, im.height)).resize((1600, 1200), Image.LANCZOS)
    im.save(os.path.join(out, name.replace('.png', '.jpg')), quality=88, optimize=True, progressive=True)
EOF

# Back to a normal launch.
xcrun simctl terminate "$device" "$bundle" >/dev/null 2>&1 || true
xcrun simctl launch "$device" "$bundle" >/dev/null
echo "saved to $out"
