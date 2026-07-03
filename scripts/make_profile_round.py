from PIL import Image, ImageDraw
import base64
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "images" / "profile.png"
out_png = ROOT / "images" / "profile-round.png"
out_svg = ROOT / "assets" / "profile-avatar.svg"

size = 200
img = Image.open(src).convert("RGBA")
w, h = img.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
img = img.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)

mask = Image.new("L", (size, size), 0)
ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
img.putalpha(mask)

# cyan gradient-style ring on transparent canvas
out_size = 220
canvas = Image.new("RGBA", (out_size, out_size), (0, 0, 0, 0))
canvas.paste(img, ((out_size - size) // 2, (out_size - size) // 2), img)
ring = ImageDraw.Draw(canvas)
ring.ellipse((8, 8, out_size - 9, out_size - 9), outline=(0, 245, 255, 255), width=4)
canvas.save(out_png, "PNG")

buf = BytesIO()
img.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode("ascii")

svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <defs>
    <clipPath id="c"><circle cx="60" cy="60" r="52"/></clipPath>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="50%" stop-color="#ff00ff"/>
      <stop offset="100%" stop-color="#39ff14"/>
    </linearGradient>
  </defs>
  <circle cx="60" cy="60" r="56" fill="none" stroke="url(#g)" stroke-width="3"/>
  <image href="data:image/png;base64,{b64}" x="8" y="8" width="104" height="104" clip-path="url(#c)" preserveAspectRatio="xMidYMid slice"/>
</svg>
"""

out_svg.write_text(svg, encoding="utf-8")
print("Created", out_png.name, "and", out_svg.name)
