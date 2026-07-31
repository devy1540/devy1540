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
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "assets" / "profile-portrait.jpg"
GRID_SIZE = 144
GROUP_COUNT = 24
TRAVELLER_DOTS = 1200
TRAVELLER_RADIUS = 1.25
CODE_STROKE_WIDTH = 3
CELL_SIZE = 2.45
PORTRAIT_ORIGIN = (72.0, 113.0)
LOOP_SECONDS = 14.2
LOOP_BEGIN_SECONDS = 3.2


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


def sample_mask_points(mask: Image.Image, count: int, seed: int) -> list[tuple[int, int]]:
    candidates = [
        (x, y)
        for y in range(mask.height)
        for x in range(mask.width)
        if mask.getpixel((x, y)) > 96
    ]
    if len(candidates) < count:
        raise RuntimeError(
            f"Icon mask produced {len(candidates)} pixels; {count} required"
        )

    rng = random.Random(seed)
    selected_indices = [rng.randrange(len(candidates))]
    minimum_distance = [math.inf] * len(candidates)
    for _ in range(1, count):
        previous_x, previous_y = candidates[selected_indices[-1]]
        for index, (x, y) in enumerate(candidates):
            distance = (x - previous_x) ** 2 + (y - previous_y) ** 2
            if distance < minimum_distance[index]:
                minimum_distance[index] = distance
        for selected_index in selected_indices:
            minimum_distance[selected_index] = -1
        selected_indices.append(
            max(range(len(candidates)), key=minimum_distance.__getitem__)
        )
    return [candidates[index] for index in selected_indices]


def font_for_size(size: int) -> ImageFont.FreeTypeFont:
    candidates = (
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    raise RuntimeError("No supported monospaced TrueType font was found")


def code_target_points(count: int, seed: int) -> list[tuple[int, int]]:
    mask = Image.new("L", (GRID_SIZE, GRID_SIZE), 0)
    draw = ImageDraw.Draw(mask)
    font = font_for_size(44)
    bbox = draw.textbbox(
        (0, 0),
        "</>",
        font=font,
        stroke_width=CODE_STROKE_WIDTH,
    )
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    position = (
        (GRID_SIZE - width) / 2 - bbox[0],
        (GRID_SIZE - height) / 2 - bbox[1],
    )
    draw.text(
        position,
        "</>",
        fill=255,
        font=font,
        stroke_width=CODE_STROKE_WIDTH,
    )
    return sample_mask_points(mask, count, seed)


def java_icon_target_points(count: int, seed: int) -> list[tuple[int, int]]:
    """Build a Java-style steaming coffee cup silhouette."""
    mask = Image.new("L", (GRID_SIZE, GRID_SIZE), 0)
    draw = ImageDraw.Draw(mask)

    for index, center_x in enumerate((56, 72, 88)):
        phase = index * 0.8
        steam = []
        for step in range(36):
            progress = step / 35
            x = center_x + 6 * math.sin(progress * math.pi * 2 + phase)
            y = 16 + progress * 44
            steam.append((x, y))
        draw.line(steam, fill=255, width=5, joint="curve")

    draw.rounded_rectangle((34, 68, 101, 106), radius=12, fill=255)
    draw.rectangle((34, 68, 101, 77), fill=0)
    draw.line((40, 72, 96, 72), fill=255, width=5)
    draw.ellipse((91, 76, 124, 102), fill=255)
    draw.ellipse((99, 82, 117, 97), fill=0)
    draw.ellipse((25, 103, 121, 120), fill=255)
    draw.ellipse((39, 106, 108, 114), fill=0)
    return sample_mask_points(mask, count, seed)


def kubernetes_icon_target_points(count: int, seed: int) -> list[tuple[int, int]]:
    """Build the seven-sided Kubernetes wheel silhouette."""
    mask = Image.new("L", (GRID_SIZE, GRID_SIZE), 0)
    draw = ImageDraw.Draw(mask)
    center_x = center_y = GRID_SIZE / 2

    def polygon(radius: float) -> list[tuple[float, float]]:
        return [
            (
                center_x
                + radius * math.cos(-math.pi / 2 + index * 2 * math.pi / 7),
                center_y
                + radius * math.sin(-math.pi / 2 + index * 2 * math.pi / 7),
            )
            for index in range(7)
        ]

    draw.polygon(polygon(53), fill=255)
    draw.polygon(polygon(41), fill=0)
    for index in range(7):
        angle = -math.pi / 2 + index * 2 * math.pi / 7
        inner = (
            center_x + 17 * math.cos(angle),
            center_y + 17 * math.sin(angle),
        )
        outer = (
            center_x + 36 * math.cos(angle),
            center_y + 36 * math.sin(angle),
        )
        draw.line((inner, outer), fill=255, width=8)
        draw.ellipse(
            (
                outer[0] - 6,
                outer[1] - 6,
                outer[0] + 6,
                outer[1] + 6,
            ),
            fill=255,
        )
    draw.ellipse((53, 53, 91, 91), fill=255)
    draw.ellipse((65, 65, 79, 79), fill=0)
    return sample_mask_points(mask, count, seed)


def greedy_match(
    source: list[tuple[int, int]],
    target: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Match source dots to nearby target dots with deterministic transport."""
    available = set(range(len(target)))
    matched = []
    for source_x, source_y in source:
        target_index = min(
            available,
            key=lambda index: (
                (target[index][0] - source_x) ** 2
                + (target[index][1] - source_y) ** 2
            ),
        )
        matched.append(target[target_index])
        available.remove(target_index)
    return matched


def svg_point(point: tuple[int, int]) -> tuple[float, float]:
    return (
        PORTRAIT_ORIGIN[0] + point[0] * CELL_SIZE,
        PORTRAIT_ORIGIN[1] + point[1] * CELL_SIZE,
    )


def traveller_circles(
    start: list[tuple[int, int]],
    theme: dict[str, str],
    seed: int,
) -> str:
    java = greedy_match(start, java_icon_target_points(TRAVELLER_DOTS, seed + 1))
    code = greedy_match(java, code_target_points(TRAVELLER_DOTS, seed + 2))
    kubernetes = greedy_match(
        code,
        kubernetes_icon_target_points(TRAVELLER_DOTS, seed + 3),
    )

    key_times = "0;0.211;0.303;0.444;0.535;0.676;0.768;0.908;1"
    fill_values = (
        f'{theme["portrait"]};{theme["portrait"]};#F89820;#F89820;'
        f'{theme["border"]};{theme["border"]};#326CE5;#326CE5;'
        f'{theme["portrait"]}'
    )
    circles = []
    for index in range(TRAVELLER_DOTS):
        states = (
            start[index],
            start[index],
            java[index],
            java[index],
            code[index],
            code[index],
            kubernetes[index],
            kubernetes[index],
            start[index],
        )
        svg_states = [svg_point(point) for point in states]
        xs = ";".join(f"{point[0]:.2f}" for point in svg_states)
        ys = ";".join(f"{point[1]:.2f}" for point in svg_states)
        start_x, start_y = svg_states[0]
        circles.append(
            f'<circle cx="{start_x:.2f}" cy="{start_y:.2f}" '
            f'r="{TRAVELLER_RADIUS:.2f}">'
            f'<animate attributeName="cx" values="{xs}" keyTimes="{key_times}" '
            f'begin="{LOOP_BEGIN_SECONDS}s" dur="{LOOP_SECONDS}s" '
            'repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{ys}" keyTimes="{key_times}" '
            f'begin="{LOOP_BEGIN_SECONDS}s" dur="{LOOP_SECONDS}s" '
            'repeatCount="indefinite"/>'
            "</circle>"
        )
    return (
        f'<g class="traveller-layer" fill="{theme["portrait"]}">'
        f'<animate attributeName="fill" values="{fill_values}" '
        f'keyTimes="{key_times}" begin="{LOOP_BEGIN_SECONDS}s" '
        f'dur="{LOOP_SECONDS}s" repeatCount="indefinite"/>'
        f'{"".join(circles)}'
        "</g>"
    )


def group_paths(points: list[tuple[int, int]], origin_x: float, origin_y: float) -> list[str]:
    cell = CELL_SIZE
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


def render_svg(mode: str, points: list[tuple[int, int]], seed: int) -> str:
    theme = THEMES[mode]
    traveller_points = random.Random(seed).sample(points, TRAVELLER_DOTS)
    traveller_point_set = set(traveller_points)
    stationary_points = [
        point for point in points if point not in traveller_point_set
    ]
    paths = group_paths(stationary_points, origin_x=72, origin_y=113)
    portrait_groups = "\n".join(
        f'<path class="portrait-dots dots-{index}" d="{path}"/>'
        for index, path in enumerate(paths)
        if path
    )
    full_portrait_paths = group_paths(points, origin_x=72, origin_y=113)
    reduced_portrait_groups = "\n".join(
        f'<path class="reduced-portrait-dots" d="{path}"/>'
        for path in full_portrait_paths
        if path
    )
    travellers = traveller_circles(traveller_points, theme, seed)

    rows = [
        ("SUBJECT", "YOON HYEOKJUN"),
        ("ROLE", "BACKEND · PLATFORM ENGINEER"),
        ("FOCUS", "RELIABLE SYSTEMS · AI DEVTOOLS"),
        ("STACK", "JAVA · GO · TYPESCRIPT · KUBERNETES"),
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
    .portrait-cycle {{
      animation: portrait-cycle {LOOP_SECONDS}s linear {LOOP_BEGIN_SECONDS}s infinite;
    }}
    .traveller-layer {{
      animation: dots-in .9s cubic-bezier(.2,.8,.2,1) both;
    }}
    .reduced-portrait {{ display: none; }}
    .reduced-portrait-dots {{ fill: {theme["portrait"]}; }}
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
    @keyframes portrait-cycle {{
      0%, 21.1% {{ opacity: 1; }}
      30.3%, 90.8% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
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
      .portrait-dots, .portrait-cycle, .traveller-layer,
      .live-dot, .cursor, .float-mark {{
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
      }}
      .portrait-cycle, .traveller-layer {{ display: none !important; }}
      .reduced-portrait {{ display: inline !important; }}
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
    <g class="portrait-cycle">
      {portrait_groups}
    </g>
    <g class="reduced-portrait">
      {reduced_portrait_groups}
    </g>
    {travellers}
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
    parser.add_argument("--seed", type=int, default=1540)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for mode in THEMES:
        points = prepare_dither(args.source, mode)
        output = args.output_dir / f"profile-banner-{mode}.svg"
        output.write_text(render_svg(mode, points, args.seed), encoding="utf-8")
        try:
            display_path = output.relative_to(ROOT)
        except ValueError:
            display_path = output
        print(f"{display_path}: {len(points):,} portrait dots")


if __name__ == "__main__":
    main()
