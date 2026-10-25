"""Turns raw simulator recordings into the site's game clips.

    python3 -I tools/screenshots/make_clips.py <raw dir> <out dir> [game id ...]
    python3 -I tools/screenshots/make_clips.py --cut <raw.mp4> <start seconds> <out.mp4> <still.jpg>

The first form takes auto-demo recordings (tools/screenshots/record_game.sh): for each
<game id>-raw.mp4 it finds the moment the game appears (the first frame after the cream launch
screen), cuts CLIP seconds starting LEAD seconds later, turns the frame upright, drops the status
bar, crops to 4:3 and writes <out dir>/<game id>.mp4 (H.264, no audio, 1280×960) plus a review
strip, <raw dir>/<game id>-strip.png, one frame a second.

The second form cuts a hand-played recording (tools/screenshots/record_screen.sh) from a start
you chose, and writes the clip's first frame as the slide's still (1600×1200), so the still and the
clip match. Rain Garden (rain on a planted bed) and Toy Train (a circus drop-off with five friends
aboard) were made this way.
"""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

LEAD = 0.5        # seconds after the game appears; the auto-demo fires about a second later
CLIP = 5.0        # the site's limit
STATUS_BAR = 56   # px, in the 2752×2064 upright frame
CREAM = np.array([251, 242, 238])


def game_appears_at(raw):
    """Seconds into the recording when the last launch-screen frame gives way to the game."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['ffmpeg', '-v', 'error', '-i', raw, '-vf', 'fps=10,transpose=1,scale=128:96',
                        os.path.join(tmp, '%04d.png')], check=True)
        frames = sorted(os.listdir(tmp))
        last_launch = None
        for i, name in enumerate(frames):
            px = np.asarray(Image.open(os.path.join(tmp, name)).convert('RGB'), dtype=float).reshape(-1, 3)
            flat_cream = np.abs(px.mean(0) - CREAM).max() < 12 and px.std(0).max() < 22
            if flat_cream:
                last_launch = i
        if last_launch is None:
            raise SystemExit(f'{raw}: no launch screen found')
        return (last_launch + 1) / 10


def cut(raw, out, start):
    upright = (f'transpose=1,crop=2676:{2064 - STATUS_BAR}:38:{STATUS_BAR},'
               'scale=1280:960:flags=lanczos,fps=30,format=yuv420p')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.2f}', '-i', raw, '-t', str(CLIP),
                    '-vf', upright, '-c:v', 'libx264', '-preset', 'slow', '-crf', '27',
                    '-profile:v', 'high', '-movflags', '+faststart', '-an', out], check=True)


def strip(clip, png):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', clip, '-vf', 'fps=1,scale=320:-1,tile=5x1',
                    '-frames:v', '1', png], check=True)


def still(raw, start, jpg):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.2f}', '-i', raw, '-frames:v', '1', '-vf',
                    f'transpose=1,crop=2676:{2064 - STATUS_BAR}:38:{STATUS_BAR},scale=1600:1200:flags=lanczos',
                    '-q:v', '3', jpg], check=True)


if sys.argv[1] == '--cut':
    raw, start, out, jpg = sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
    cut(raw, out, start)
    still(raw, start, jpg)
    strip(out, os.path.splitext(raw)[0] + '-strip.png')
    print(f'{out}: {start:.1f}–{start + CLIP:.1f}s, {os.path.getsize(out) // 1024} KB; still {jpg}')
    sys.exit()

raw_dir, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
games = sys.argv[3:] or sorted(f[:-len('-raw.mp4')] for f in os.listdir(raw_dir) if f.endswith('-raw.mp4'))
for game in games:
    raw = os.path.join(raw_dir, f'{game}-raw.mp4')
    t0 = game_appears_at(raw)
    out = os.path.join(out_dir, f'{game}.mp4')
    cut(raw, out, t0 + LEAD)
    strip(out, os.path.join(raw_dir, f'{game}-strip.png'))
    print(f'{game}: appears at {t0:.1f}s, clip {t0 + LEAD:.1f}–{t0 + LEAD + CLIP:.1f}s, '
          f'{os.path.getsize(out) // 1024} KB')
