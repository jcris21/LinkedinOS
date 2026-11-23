"""Frame-accurate capture of a CSS-animated poster, then Ken Burns via ffmpeg.

Usage:
  python3 render_anim.py <html> <out_prefix> [duration=6] [fps=25] [scale=1.5] [amp=0.10] [pan=15] [preview_t=]
If preview_t is given, only renders that single time (seconds) to <out_prefix>_t.png.
"""
import sys, os, subprocess, shutil
from playwright.sync_api import sync_playwright

html, prefix = sys.argv[1], sys.argv[2]
duration = float(sys.argv[3]) if len(sys.argv) > 3 else 6
fps = int(sys.argv[4]) if len(sys.argv) > 4 else 25
scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.5
amp = float(sys.argv[6]) if len(sys.argv) > 6 else 0.10
pan = float(sys.argv[7]) if len(sys.argv) > 7 else 15
preview = sys.argv[8] if len(sys.argv) > 8 else None

SET_T = """(t) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1220, 'height': 1520}, device_scale_factor=scale)
    page.goto(f'file://{os.path.abspath(html)}')
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    if preview is not None:
        for t in preview.split(','):
            page.evaluate(SET_T, float(t) * 1000)
            page.screenshot(path=f'{prefix}_t{t}.png')
        b.close()
        sys.exit(0)
    fdir = f'{prefix}_frames'
    shutil.rmtree(fdir, ignore_errors=True)
    os.makedirs(fdir)
    n = int(duration * fps)
    for i in range(n):
        page.evaluate(SET_T, i * 1000.0 / fps)
        page.screenshot(path=f'{fdir}/f_{i:04d}.jpg', type='jpeg', quality=93)
    b.close()

n = int(duration * fps)
z = f"1+{amp}*pow(sin(PI*on/{n}),2)"
y = f"ih/2-(ih/zoom/2)-{pan}*sin(PI*on/{n})"
cmd = (f'ffmpeg -y -framerate {fps} -i "{fdir}/f_%04d.jpg" -vf '
       f'"zoompan=z=\'{z}\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'{y}\':s=1080x1350:fps={fps},format=yuv420p" '
       f'-t {duration} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p "{prefix}_kenburns.mp4"')
subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('done', f'{prefix}_kenburns.mp4')
