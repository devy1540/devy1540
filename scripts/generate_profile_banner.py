#!/usr/bin/env python3
"""Generate light and dark terminal-style profile banners.

The portrait is converted to a compact Floyd-Steinberg dither and emitted as
SVG path runs. The SVGs remain readable without animation and respect the
visitor's reduced-motion preference.
"""

from __future__ import annotations

import argparse
import html
import math
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "assets" / "profile-portrait.jpg"
GRID_SIZE = 144
GROUP_COUNT = 24


THEMES = {
    "dark": {
        "background": "#0A101F",
        "panel": "#111827",
        "panel_alt": "#0F172A",
        "border": "#22D3EE",
        "portrait": "#A78BFA",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "accent": "#10B981",
        "danger": "#FB7185",
        "grid": "#1E293B",
    },
    "light": {
        "background": "#F8FAFC",
        "panel": "#FFFFFF",
        "panel_alt": "#EEF2FF",
        "border": "#0891B2",
        "portrait": "#7C3AED",
        "text": "#0F172A",
        "muted": "#475569",
        "accent": "#059669",
        "danger": "#E11D48",
        "grid": "#CBD5E1",
    },
}


def build_subject_mask(image: Image.Image) -> Image.Image:
    """Estimate the subject against the intentionally uniform source backdrop."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    border = []
    step = max(1, width // 64)

    for x in range(0, width, step):
        border.append(rgb.getpixel((x, 0)))
        border.append(rgb.getpixel((x, height - 1)))
    for y in range(0, height, step):
        border.append(rgb.getpixel((0, y)))
        border.append(rgb.getpixel((width - 1, y)))

    background = tuple(sorted(pixel[channel] for pixel in border)[len(border) // 2] for channel in range(3))
    mask = Image.new("L", rgb.size, 0)
    source = rgb.load()
    target = mask.load()

    for y in range(height):
        for x in range(width):
            red, green, blue = source[x, y]
            distance = math.sqrt(
                (red - background[0]) ** 2
                + (green - background[1]) ** 2
                + (blue - background[2]) ** 2
            )
            target[x, y] = 255 if distance > 25 else 0

    mask = mask.filter(ImageFilter.MaxFilter(11))
    mask = mask.filter(ImageFilter.MinFilter(7))
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    return mask.point(lambda value: 255 if value > 96 else 0)


def prepare_dither(source: Path, mode: str) -> list[tuple[int, int]]:
    image = Image.open(source).convert("RGB")
    size = min(image.size)
    left = (image.width - size) // 2
    top = (image.height - size) // 2
    image = image.crop((left, top, left + size, top + size))
    mask = build_subject_mask(image)

    grayscale = ImageOps.grayscale(image)
    grayscale = ImageOps.autocontrast(grayscale, cutoff=1)
    grayscale = ImageEnhance.Contrast(grayscale).enhance(1.3)
    grayscale = ImageEnhance.Brightness(grayscale).enhance(0.82)
    grayscale = grayscale.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=2))

    grayscale = grayscale.resize((GRID_SIZE, GRID_SIZE), Image.Resampling.LANCZOS)
    mask = mask.resize((GRID_SIZE, GRID_SIZE), Image.Resampling.LANCZOS)
    binary = grayscale.convert("1", dither=Image.Dither.FLOYDSTEINBERG)

    points: list[tuple[int, int]] = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if mask.getpixel((x, y)) < 128:
                continue
            ink = binary.getpixel((x, y)) == 0
            if ink:
                points.append((x, y))
    return points


def group_paths(points: list[tuple[int, int]], origin_x: float, origin_y: float) -> list[str]:
    cell = 2.45
    dot = 1.78
    groups = [[] for _ in range(GROUP_COUNT)]

    for x, y in points:
        group = ((x * 73) ^ (y * 151) ^ (x * y * 17)) % GROUP_COUNT
        px = origin_x + x * cell
        py = origin_y + y * cell
        groups[group].append(f"M{px:.2f},{py:.2f}h{dot:.2f}v{dot:.2f}h-{dot:.2f}z")

    return ["".join(group) for group in groups]


def text(x: int, y: int, value: str, css_class: str, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" class="{css_class}" text-anchor="{anchor}">'
        f"{html.escape(value)}</text>"
    )


def render_svg(mode: str, points: list[tuple[int, int]]) -> str:
    theme = THEMES[mode]
    paths = group_paths(points, origin_x=72, origin_y=113)
    portrait_groups = "\n".join(
        f'<path class="portrait-dots dots-{index}" d="{path}"/>'
        for index, path in enumerate(paths)
        if path
    )

    rows = [
        ("SUBJECT", "YOON HYEOKJUN"),
        ("ROLE", "BACKEND · PLATFORM ENGINEER"),
        ("FOCUS", "RELIABLE SYSTEMS · AI DEVTOOLS"),
        ("STACK", "JVM · GO · TYPESCRIPT · K8S"),
        ("BUILDING", "TOARD · FCP · LTM WIKI"),
        ("WRITING", "DEVY1540.DEV"),
    ]
    row_svg = []
    for index, (label, value) in enumerate(rows):
        y = 218 + index * 42
        row_svg.append(text(532, y, label, "label"))
        row_svg.append(
            f'<line x1="628" y1="{y - 4}" x2="756" y2="{y - 4}" class="leader"/>'
        )
        row_svg.append(text(782, y, value, "value"))

    delays = "\n".join(
        f".dots-{index} {{ animation-delay: {index * 0.028:.3f}s; }}"
        for index in range(GROUP_COUNT)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="520" viewBox="0 0 1200 520" role="img" aria-labelledby="title desc">
  <title id="title">devy1540 - backend and platform engineer</title>
  <desc id="desc">Terminal-style profile banner with a dithered portrait and current engineering focus.</desc>
  <style>
    :root {{
      color-scheme: {mode};
    }}
    text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}
    .chrome {{ fill: {theme["muted"]}; font-size: 14px; letter-spacing: .6px; }}
    .title {{ fill: {theme["text"]}; font-size: 30px; font-weight: 700; letter-spacing: 1px; }}
    .subtitle {{ fill: {theme["border"]}; font-size: 15px; letter-spacing: 1.5px; }}
    .section {{ fill: {theme["border"]}; font-size: 13px; font-weight: 700; letter-spacing: 2px; }}
    .label {{ fill: {theme["muted"]}; font-size: 13px; letter-spacing: 1px; }}
    .value {{ fill: {theme["text"]}; font-size: 14px; font-weight: 600; }}
    .leader {{ stroke: {theme["grid"]}; stroke-width: 1; stroke-dasharray: 2 5; }}
    .portrait-dots {{
      fill: {theme["portrait"]};
      animation: dots-in .9s cubic-bezier(.2,.8,.2,1) both;
    }}
    .live-dot {{
      fill: {theme["danger"]};
      transform-origin: 1102px 45px;
      animation: pulse 1.8s ease-in-out infinite;
    }}
    .cursor {{ animation: blink 1.15s steps(1,end) infinite; }}
    .float-mark {{
      transform-origin: 418px 116px;
      animation: float 7s ease-in-out infinite;
    }}
    {delays}
    @keyframes dots-in {{
      from {{ opacity: 0; transform: translateY(3px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: .5; transform: scale(.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    @keyframes blink {{ 0%, 48% {{ opacity: 1; }} 49%, 100% {{ opacity: 0; }} }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0) rotate(-2deg); }}
      50% {{ transform: translateY(-8px) rotate(2deg); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .portrait-dots, .live-dot, .cursor, .float-mark {{
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
      }}
    }}
  </style>

  <rect width="1200" height="520" rx="22" fill="{theme["background"]}"/>
  <rect x="14" y="14" width="1172" height="492" rx="16" fill="{theme["panel"]}" stroke="{theme["border"]}" stroke-width="1.5"/>
  <rect x="14" y="14" width="1172" height="62" rx="16" fill="{theme["panel_alt"]}"/>
  <path d="M14 60h1172v16H14z" fill="{theme["panel_alt"]}"/>
  <circle cx="42" cy="45" r="6" fill="#FB7185"/>
  <circle cx="64" cy="45" r="6" fill="#FBBF24"/>
  <circle cx="86" cy="45" r="6" fill="#34D399"/>
  {text(112, 50, "profile.sh --live", "chrome")}
  <circle cx="1102" cy="45" r="6" class="live-dot"/>
  {text(1118, 50, "LIVE", "chrome")}

  <rect x="42" y="96" width="396" height="382" rx="12" fill="{theme["panel_alt"]}" stroke="{theme["grid"]}"/>
  {text(66, 126, "VISUAL.MAP", "section")}
  <g class="float-mark">
    <rect x="374" y="94" width="88" height="42" rx="10" fill="{theme["background"]}" stroke="{theme["border"]}"/>
    {text(418, 121, "</>", "subtitle", "middle")}
  </g>
  <clipPath id="portrait-clip"><rect x="58" y="104" width="362" height="354" rx="8"/></clipPath>
  <g clip-path="url(#portrait-clip)">
    {portrait_groups}
  </g>

  {text(506, 124, "SYSTEM.INFO", "section")}
  {text(506, 170, "devy1540", "title")}
  {text(672, 170, "_", "title cursor")}
  {"".join(row_svg)}

  <rect x="506" y="448" width="642" height="34" rx="17" fill="{theme["panel_alt"]}" stroke="{theme["grid"]}"/>
  <circle cx="530" cy="465" r="5" fill="{theme["accent"]}"/>
  {text(546, 470, "BUILDING SYSTEMS THAT STAY UNDERSTANDABLE IN PRODUCTION", "chrome")}
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for mode in THEMES:
        points = prepare_dither(args.source, mode)
        output = args.output_dir / f"profile-banner-{mode}.svg"
        output.write_text(render_svg(mode, points), encoding="utf-8")
        print(f"{output.relative_to(ROOT)}: {len(points):,} portrait dots")


if __name__ == "__main__":
    main()
