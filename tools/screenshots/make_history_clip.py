"""Builds the History clip on Home from one hand-driven recording (tools/screenshots/record_screen.sh).

    python3 -I tools/screenshots/make_history_clip.py <history-raw.mp4> <out.mp4> <poster.jpg>

The recording: Leo's History at "All sessions", then Last 30 days, then K · Initial, then K · Final
(filters combine), a scroll down to the sessions table and back up. The times below were read off
that recording (the moments the screen changes); re-read them if you record it again.

Between actions the screen is still, so the waits are cut out at those still moments and the joins
don't show. The simulator doesn't record touches, so a marker is drawn where each tap and swipe was.
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

raw, out, poster = sys.argv[1], sys.argv[2], sys.argv[3]

W, H = 1600, 1168               # 2752×2008 upright frame (status bar off), scaled
SCALE = W / 2752


def px(x_pt, y_pt):
    """A point in the app's landscape coordinates → the clip's pixels."""
    return x_pt * 2 * SCALE, (y_pt * 2 - 56) * SCALE


# (start, end, from point, to point) in the recording's timeline; a tap has the same from and to.
TOUCHES = [
    (4.72, 5.15, (372, 170), (372, 170)),       # Last 30 days
    (9.32, 9.75, (1250, 878), (1250, 878)),     # K · Initial
    (14.05, 14.48, (1250, 810), (1250, 810)),   # K · Final
    (20.30, 20.95, (676, 820), (676, 380)),     # scroll down
    (26.66, 27.30, (676, 380), (676, 900)),     # scroll back up
]
# Kept stretches of the recording, each starting and ending while the screen is still.
SEGMENTS = [(3.6, 6.4), (8.6, 11.0), (13.3, 15.7), (19.9, 23.1), (26.3, 28.9)]
LOOP_FADE = 0.5  # crossfade from the last frame back to the first, so the loop has no jump

with tempfile.TemporaryDirectory() as tmp:
    # The marker: a soft navy disc with a navy ring.
    d = 76
    dot = Image.new('RGBA', (d, d), (0, 0, 0, 0))
    ImageDraw.Draw(dot).ellipse((3, 3, d - 4, d - 4), fill=(31, 50, 71, 70), outline=(31, 50, 71, 170), width=4)
    dot_path = os.path.join(tmp, 'dot.png')
    dot.save(dot_path)

    chain, last = [], '0:v'
    chain.append(f'[{last}]transpose=1,crop=2752:2008:0:56,scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p[base]')
    last = 'base'
    for i, (t0, t1, a, b) in enumerate(TOUCHES):
        (ax, ay), (bx, by) = px(*a), px(*b)
        f = f'(t-{t0})/{t1 - t0}'
        x = f'{ax - d / 2:.1f}+({bx - ax:.1f})*{f}'
        y = f'{ay - d / 2:.1f}+({by - ay:.1f})*{f}'
        chain.append(f"[{last}][1:v]overlay=x='{x}':y='{y}':eval=frame:enable='between(t,{t0},{t1})'[m{i}]")
        last = f'm{i}'
    chain.append(f'[{last}]split={len(SEGMENTS)}' + ''.join(f'[s{i}]' for i in range(len(SEGMENTS))))
    for i, (a, b) in enumerate(SEGMENTS):
        chain.append(f'[s{i}]trim={a}:{b},setpts=PTS-STARTPTS[c{i}]')
    chain.append(''.join(f'[c{i}]' for i in range(len(SEGMENTS))) + f'concat=n={len(SEGMENTS)}:v=1:a=0[joined]')
    filtered = os.path.join(tmp, 'joined.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-loop', '1', '-i', dot_path,
                    '-filter_complex', ';'.join(chain), '-map', '[joined]', '-shortest',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', filtered], check=True)

    # Loop seam: hold the last frame, crossfade it into the first, and append that.
    duration = sum(b - a for a, b in SEGMENTS)
    first, lastf = os.path.join(tmp, 'first.png'), os.path.join(tmp, 'last.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', filtered, '-frames:v', '1', first], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.1', '-i', filtered, '-frames:v', '1', lastf], check=True)
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', filtered,
        '-loop', '1', '-t', str(LOOP_FADE + 0.1), '-i', lastf,
        '-loop', '1', '-t', str(LOOP_FADE + 0.1), '-i', first,
        '-filter_complex',
        f'[1:v]fps=30,format=yuv420p[l];[2:v]fps=30,format=yuv420p[f];'
        f'[l][f]xfade=transition=fade:duration={LOOP_FADE}:offset=0.05[seam];'
        f'[0:v][seam]concat=n=2:v=1:a=0,format=yuv420p[v]',
        '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-profile:v', 'high',
        '-movflags', '+faststart', '-an', out], check=True)
    Image.open(first).convert('RGB').save(poster, quality=88, optimize=True, progressive=True)
    print(f'{out}: {duration + LOOP_FADE + 0.1:.1f}s, {os.path.getsize(out) // 1024} KB; poster {poster}')
