"""Rasterise site/vendor/flags/*.svg to small PNGs in scripts/flags_png, for the share cards (Pillow cannot read SVG).

Run by hand when a flag changes: python scripts/make_flag_pngs.py. It needs Chrome or Edge (headless) and Pillow; the
build itself only reads the PNGs, so it needs neither. Each flag is drawn to fit a 192x128 box at its own aspect ratio.
"""
import subprocess, sys, tempfile, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "site" / "vendor" / "flags", Path(__file__).resolve().parent / "flags_png"
CW, CH, COLS = 200, 136, 8
BROWSERS = ["C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "google-chrome", "chromium", "msedge"]


def main():
    svgs = sorted(SRC.glob("*.svg"))
    rows = -(-len(svgs) // COLS)
    cells = "".join(f'<div class="c"><img src="{s.as_uri()}"></div>' for s in svgs)
    html = (f"<style>html,body{{margin:0;background:transparent}}body{{display:grid;grid-template-columns:repeat({COLS},{CW}px)}}"
            f".c{{width:{CW}px;height:{CH}px;display:flex;align-items:center;justify-content:center}}"
            f"img{{max-width:192px;max-height:128px;display:block}}</style>{cells}")
    tmp = Path(tempfile.mkdtemp())
    page, shot = tmp / "flags.html", tmp / "flags.png"
    page.write_text(html, encoding="utf-8")
    exe = next((b for b in BROWSERS if Path(b).exists() or shutil.which(b)), None)
    if not exe:
        sys.exit("Chrome or Edge is needed")
    subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                    f"--window-size={COLS * CW},{rows * CH}", f"--screenshot={shot}", "--force-device-scale-factor=1", page.as_uri()],
                   check=True, capture_output=True, timeout=120)
    sheet = Image.open(shot).convert("RGBA")
    OUT.mkdir(exist_ok=True)
    for i, s in enumerate(svgs):
        x, y = (i % COLS) * CW, (i // COLS) * CH
        cell = sheet.crop((x, y, x + CW, y + CH))
        box = cell.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if box:
            cell.crop(box).save(OUT / f"{s.stem}.png", optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{len(svgs)} flags -> {OUT}")


if __name__ == "__main__":
    main()
