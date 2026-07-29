#!/usr/bin/env python3
"""Generate the theme-aware GitHub profile banner and project panel.

The script deliberately keeps the visual source of truth in the repository.
It downloads the public GitHub avatar unless --avatar points to a local image.

Usage:
    python3 scripts/generate_profile_assets.py
    python3 scripts/generate_profile_assets.py --avatar /path/to/photo.png
"""

from __future__ import annotations

import argparse
import collections
import datetime
import html
import io
import json
import math
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


WIDTH = 1180
HEIGHT = 610
GRID_WIDTH = 300
GRID_HEIGHT = 340
PORTRAIT_DOTS = 17_000
TRAVELLER_DOTS = 720
INTRO_GROUPS = 60
LOOP_SECONDS = 14.2
LOOP_BEGIN_SECONDS = 3.2
AVATAR_URL = "https://github.com/devy1540.png?size=1200"
PROFILE_API_URL = "https://api.github.com/users/devy1540"
REPOS_API_URL = "https://api.github.com/users/devy1540/repos?per_page=100&sort=updated"
REPO_ROOT = Path(__file__).resolve().parents[1]


THEMES = {
    "dark": {
        "background": "#0A101F",
        "panel": "#0D1526",
        "line": "#22314D",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "subtle": "#64748B",
        "chrome": "#22D3EE",
        "portrait": "#A78BFA",
        "accent": "#10B981",
        "pill": "#4C1D95",
        "pill_text": "#F5F3FF",
        "border_a": "#7C3AED",
        "border_b": "#22D3EE",
    },
    "light": {
        "background": "#FFFFFF",
        "panel": "#F8FAFC",
        "line": "#CBD5E1",
        "text": "#0F172A",
        "muted": "#475569",
        "subtle": "#94A3B8",
        "chrome": "#0891B2",
        "portrait": "#7C3AED",
        "accent": "#059669",
        "pill": "#EDE9FE",
        "pill_text": "#6D28D9",
        "border_a": "#7C3AED",
        "border_b": "#0891B2",
    },
}


PROJECTS = [
    (
        "devy1540.github.io",
        "Technical archive for backend and platform engineering",
        ("React", "TypeScript", "Vite"),
    ),
    (
        "toard",
        "Self-hosted AI coding-tool usage and cost platform",
        ("Next.js", "PostgreSQL", "Rust"),
    ),
    (
        "fcp",
        "Lightweight AWS and Google Cloud emulator for local tests",
        ("Go", "AWS", "Google Cloud"),
    ),
    (
        "ltm-wiki",
        "Portable long-term memory wiki for AI agents",
        ("Markdown", "Skills", "Obsidian"),
    ),
    (
        "claude-pulse",
        "Fast Rust statusline HUD for Claude Code",
        ("Rust", "CLI", "Observability"),
    ),
    (
        "jvm-concurrency-benchmark",
        "Platform thread vs virtual thread vs coroutine",
        ("Java", "Kotlin", "Grafana"),
    ),
]


def xml(value: str) -> str:
    return html.escape(value, quote=True)


def load_avatar(source: str) -> Image.Image:
    if source.startswith(("http://", "https://")):
        request = urllib.request.Request(
            source,
            headers={"User-Agent": "devy1540-profile-asset-generator"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    return Image.open(source).convert("RGB")


def fetch_json(url: str) -> dict | list:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "devy1540-profile-asset-generator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def subject_mask() -> Image.Image:
    """A conservative silhouette for the current public head-and-shoulders avatar."""
    mask = Image.new("L", (GRID_WIDTH, GRID_HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(
        [
            (84, 112),
            (84, 68),
            (99, 31),
            (127, 10),
            (171, 8),
            (203, 30),
            (219, 68),
            (216, 112),
            (199, 156),
            (220, 174),
            (253, 197),
            (286, 234),
            (299, 340),
            (1, 340),
            (10, 282),
            (34, 238),
            (64, 207),
            (105, 176),
            (111, 151),
        ],
        fill=255,
    )
    draw.ellipse((91, 13, 219, 170), fill=255)
    return mask.filter(ImageFilter.MaxFilter(5))


def floyd_steinberg(density: np.ndarray, allowed: np.ndarray) -> np.ndarray:
    """Apply 1-bit serpentine Floyd-Steinberg diffusion inside the subject mask."""
    work = density.astype(np.float64).copy()
    result = np.zeros_like(work, dtype=bool)
    height, width = work.shape

    for y in range(height):
        left_to_right = y % 2 == 0
        xs = range(width) if left_to_right else range(width - 1, -1, -1)
        direction = 1 if left_to_right else -1
        for x in xs:
            if not allowed[y, x]:
                work[y, x] = 0
                continue
            old = work[y, x]
            new = 1.0 if old >= 0.5 else 0.0
            result[y, x] = bool(new)
            error = old - new
            neighbours = (
                (x + direction, y, 7 / 16),
                (x - direction, y + 1, 3 / 16),
                (x, y + 1, 5 / 16),
                (x + direction, y + 1, 1 / 16),
            )
            for nx, ny, weight in neighbours:
                if 0 <= nx < width and 0 <= ny < height and allowed[ny, nx]:
                    work[ny, nx] += error * weight
    return result


def portrait_points(avatar: Image.Image, seed: int, mode: str) -> np.ndarray:
    fitted = ImageOps.fit(
        avatar,
        (GRID_WIDTH, GRID_HEIGHT),
        method=Image.Resampling.LANCZOS,
        centering=(0.52, 0.45),
    )
    gray = ImageOps.grayscale(fitted)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    gray = ImageEnhance.Contrast(gray).enhance(1.3)

    allowed = np.asarray(subject_mask(), dtype=np.uint8) > 127
    brightness = np.asarray(gray, dtype=np.float64) / 255.0
    tone = brightness if mode == "dark" else 1.0 - brightness
    base_density = 0.16 if mode == "dark" else 0.04
    density = (base_density + 0.70 * np.power(tone, 1.2)) * allowed
    dithered = floyd_steinberg(density, allowed)
    points = np.argwhere(dithered)[:, [1, 0]]

    rng = np.random.default_rng(seed)
    if len(points) > PORTRAIT_DOTS:
        points = points[rng.choice(len(points), PORTRAIT_DOTS, replace=False)]
    return points.astype(np.float64)


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


def sample_mask_points(mask: Image.Image, count: int, seed: int) -> np.ndarray:
    candidates = np.argwhere(np.asarray(mask) > 96)[:, [1, 0]]
    rng = np.random.default_rng(seed)
    replace = len(candidates) < count
    selected = candidates[rng.choice(len(candidates), count, replace=replace)]
    return selected.astype(np.float64)


def sample_mask_points_even(mask: Image.Image, count: int, seed: int) -> np.ndarray:
    """Choose well-spaced icon dots so thin strokes stay recognizable."""
    candidates = np.argwhere(np.asarray(mask) > 96)[:, [1, 0]].astype(np.float64)
    if len(candidates) <= count:
        return sample_mask_points(mask, count, seed)

    rng = np.random.default_rng(seed)
    selected_indices = np.empty(count, dtype=np.int64)
    selected_indices[0] = int(rng.integers(len(candidates)))
    minimum_distance = np.full(len(candidates), np.inf)
    for index in range(1, count):
        previous = candidates[selected_indices[index - 1]]
        delta = candidates - previous
        minimum_distance = np.minimum(
            minimum_distance,
            np.einsum("ij,ij->i", delta, delta),
        )
        minimum_distance[selected_indices[:index]] = -1
        selected_indices[index] = int(np.argmax(minimum_distance))
    return candidates[selected_indices]


def text_target_points(label: str, count: int, seed: int) -> np.ndarray:
    mask = Image.new("L", (GRID_WIDTH, GRID_HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    font_size = 88 if len(label) <= 3 else 76
    font = font_for_size(font_size)
    bbox = draw.textbbox((0, 0), label, font=font, stroke_width=1)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (
        (GRID_WIDTH - text_width) / 2 - bbox[0],
        (GRID_HEIGHT - text_height) / 2 - bbox[1],
    )
    draw.text(position, label, fill=255, font=font, stroke_width=1)
    return sample_mask_points_even(mask, count, seed)


def java_icon_target_points(count: int, seed: int) -> np.ndarray:
    """Build a Java-style steaming coffee cup silhouette."""
    mask = Image.new("L", (GRID_WIDTH, GRID_HEIGHT), 0)
    draw = ImageDraw.Draw(mask)

    for index, center_x in enumerate((118, 150, 182)):
        phase = index * 0.8
        steam = []
        for step in range(45):
            progress = step / 44
            x = center_x + 11 * math.sin(progress * math.pi * 2 + phase)
            y = 58 + progress * 92
            steam.append((x, y))
        draw.line(steam, fill=255, width=8, joint="curve")

    draw.rounded_rectangle((78, 158, 208, 224), radius=22, fill=255)
    draw.rectangle((78, 158, 208, 175), fill=0)
    draw.line((88, 164, 198, 164), fill=255, width=8)
    draw.ellipse((190, 170, 244, 215), fill=255)
    draw.ellipse((201, 179, 232, 206), fill=0)
    draw.ellipse((62, 220, 238, 246), fill=255)
    draw.ellipse((84, 224, 216, 237), fill=0)
    return sample_mask_points(mask, count, seed)


def kubernetes_icon_target_points(count: int, seed: int) -> np.ndarray:
    """Build the seven-sided wheel silhouette associated with Kubernetes."""
    mask = Image.new("L", (GRID_WIDTH, GRID_HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    center_x, center_y = 150, 170

    def polygon(radius: float) -> list[tuple[float, float]]:
        return [
            (
                center_x + radius * math.cos(-math.pi / 2 + index * 2 * math.pi / 7),
                center_y + radius * math.sin(-math.pi / 2 + index * 2 * math.pi / 7),
            )
            for index in range(7)
        ]

    draw.polygon(polygon(106), fill=255)
    draw.polygon(polygon(82), fill=0)
    for index in range(7):
        angle = -math.pi / 2 + index * 2 * math.pi / 7
        inner = (
            center_x + 34 * math.cos(angle),
            center_y + 34 * math.sin(angle),
        )
        outer = (
            center_x + 72 * math.cos(angle),
            center_y + 72 * math.sin(angle),
        )
        draw.line((inner, outer), fill=255, width=16)
        draw.ellipse(
            (
                outer[0] - 11,
                outer[1] - 11,
                outer[0] + 11,
                outer[1] + 11,
            ),
            fill=255,
        )
    draw.ellipse((113, 133, 187, 207), fill=255)
    draw.ellipse((135, 155, 165, 185), fill=0)
    return sample_mask_points_even(mask, count, seed)


def greedy_match(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Match each source dot to a nearby target dot with deterministic greedy transport."""
    matched = np.empty_like(source)
    available = np.ones(len(target), dtype=bool)
    band = 12
    order = sorted(
        range(len(source)),
        key=lambda i: (
            int(source[i, 1]) // band,
            source[i, 0]
            if (int(source[i, 1]) // band) % 2 == 0
            else -source[i, 0],
        ),
    )
    for source_index in order:
        delta = target - source[source_index]
        distance = np.einsum("ij,ij->i", delta, delta)
        distance[~available] = np.inf
        target_index = int(np.argmin(distance))
        matched[source_index] = target[target_index]
        available[target_index] = False
    return matched


def dot_path(points: np.ndarray) -> str:
    return "".join(
        f"M{int(x)} {int(y)}h.76v.76h-.76z"
        for x, y in sorted(points, key=lambda point: (point[1], point[0]))
    )


def distribute_intro_groups(
    points: np.ndarray,
    seed: int,
) -> list[np.ndarray]:
    """Distribute every spatial cell across all intro groups."""
    rng = np.random.default_rng(seed)
    groups: list[list[np.ndarray]] = [[] for _ in range(INTRO_GROUPS)]
    cells = 8
    cell_width = GRID_WIDTH / cells
    cell_height = GRID_HEIGHT / cells
    for cell_y in range(cells):
        for cell_x in range(cells):
            in_cell = points[
                (points[:, 0] >= cell_x * cell_width)
                & (points[:, 0] < (cell_x + 1) * cell_width)
                & (points[:, 1] >= cell_y * cell_height)
                & (points[:, 1] < (cell_y + 1) * cell_height)
            ]
            if not len(in_cell):
                continue
            shuffled = in_cell[rng.permutation(len(in_cell))]
            offset = int(rng.integers(INTRO_GROUPS))
            for index, point in enumerate(shuffled):
                groups[(offset + index) % INTRO_GROUPS].append(point)
    return [
        np.asarray(group, dtype=np.float64).reshape((-1, 2))
        for group in groups
    ]


def grouped_portrait_paths(points: np.ndarray, theme: dict[str, str], seed: int) -> str:
    groups = distribute_intro_groups(points, seed)
    loop_values = "1;1;0;0;0;0;0;0;1"
    key_times = "0;0.211;0.303;0.444;0.535;0.676;0.768;0.908;1"
    chunks = []
    for index, group in enumerate(groups):
        begin = 0.18 + index * 0.025
        duration = 0.62 + (index % 7) * 0.065
        chunks.append(
            f'<path d="{dot_path(group)}" fill="{theme["portrait"]}" '
            'shape-rendering="crispEdges" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.3f}s" '
            f'dur="{duration:.3f}s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="{loop_values}" '
            f'keyTimes="{key_times}" begin="{LOOP_BEGIN_SECONDS}s" '
            f'dur="{LOOP_SECONDS}s" repeatCount="indefinite"/>'
            "</path>"
        )
    return "".join(chunks)


def traveller_circles(points: np.ndarray, theme: dict[str, str], seed: int) -> str:
    rng = np.random.default_rng(seed)
    start = points[rng.choice(len(points), TRAVELLER_DOTS, replace=False)]
    java = greedy_match(start, java_icon_target_points(TRAVELLER_DOTS, seed + 1))
    code = greedy_match(java, text_target_points("</>", TRAVELLER_DOTS, seed + 2))
    kubernetes = greedy_match(
        code,
        kubernetes_icon_target_points(TRAVELLER_DOTS, seed + 3),
    )

    key_times = "0;0.211;0.303;0.444;0.535;0.676;0.768;0.908;1"
    opacity = "0;0;1;1;1;1;1;1;0"
    fill_values = (
        f'{theme["accent"]};{theme["accent"]};#F89820;#F89820;'
        f'{theme["accent"]};{theme["accent"]};#326CE5;#326CE5;'
        f'{theme["accent"]}'
    )
    chunks = []
    for index in range(TRAVELLER_DOTS):
        xs = ";".join(
            f"{value:.1f}"
            for value in (
                start[index, 0],
                start[index, 0],
                java[index, 0],
                java[index, 0],
                code[index, 0],
                code[index, 0],
                kubernetes[index, 0],
                kubernetes[index, 0],
                start[index, 0],
            )
        )
        ys = ";".join(
            f"{value:.1f}"
            for value in (
                start[index, 1],
                start[index, 1],
                java[index, 1],
                java[index, 1],
                code[index, 1],
                code[index, 1],
                kubernetes[index, 1],
                kubernetes[index, 1],
                start[index, 1],
            )
        )
        chunks.append(
            f'<circle cx="{start[index, 0]:.1f}" cy="{start[index, 1]:.1f}" '
            'r="1.0" opacity="0">'
            f'<animate attributeName="cx" values="{xs}" keyTimes="{key_times}" '
            f'begin="{LOOP_BEGIN_SECONDS}s" dur="{LOOP_SECONDS}s" '
            'repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{ys}" keyTimes="{key_times}" '
            f'begin="{LOOP_BEGIN_SECONDS}s" dur="{LOOP_SECONDS}s" '
            'repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{opacity}" '
            f'keyTimes="{key_times}" begin="{LOOP_BEGIN_SECONDS}s" '
            f'dur="{LOOP_SECONDS}s" repeatCount="indefinite"/>'
            "</circle>"
        )
    return (
        f'<g fill="{theme["accent"]}">'
        f'<animate attributeName="fill" values="{fill_values}" '
        f'keyTimes="{key_times}" begin="{LOOP_BEGIN_SECONDS}s" '
        f'dur="{LOOP_SECONDS}s" repeatCount="indefinite"/>'
        f'{"".join(chunks)}'
        "</g>"
    )


def row(label: str, value: str, y: int, theme: dict[str, str]) -> str:
    label_width = len(label) * 8.15
    value_length = max(40.0, len(value) * 8.2)
    line_start = 470 + label_width + 13
    line_end = 1125 - value_length - 13
    leader = ""
    if line_end > line_start:
        leader = (
            f'<line x1="{line_start:.1f}" y1="{y - 4}" x2="{line_end:.1f}" '
            f'y2="{y - 4}" stroke="{theme["subtle"]}" stroke-width="1" '
            'stroke-dasharray="2 5" opacity=".62"/>'
        )
    return (
        f'<text x="470" y="{y}" fill="{theme["chrome"]}" '
        f'font-size="14">{xml(label)}</text>'
        f"{leader}"
        f'<text x="1125" y="{y}" fill="{theme["text"]}" font-size="14" '
        f'font-weight="650" text-anchor="end" textLength="{value_length:.1f}" '
        f'lengthAdjust="spacingAndGlyphs">{xml(value)}</text>'
    )


def corner_frame(theme: dict[str, str]) -> str:
    return (
        f'<path d="M36 151v-24h24 M412 127h24v24 M36 533v24h24 '
        f'M412 557h24v-24" fill="none" stroke="{theme["chrome"]}" '
        'stroke-width="3" stroke-linecap="square"/>'
        f'<rect x="36" y="127" width="400" height="430" rx="6" fill="none" '
        f'stroke="{theme["chrome"]}" stroke-width="1" opacity=".55" '
        'filter="url(#glow)"/>'
    )


def render_banner(
    mode: str,
    points: np.ndarray,
    seed: int,
) -> str:
    theme = THEMES[mode]
    rows = [
        ("Subject", "Hyukjun Yoon", 166),
        ("Role", "Backend / Platform Engineer", 189),
        ("Origin", "Seoul, South Korea", 212),
        ("Focus", "Reliable systems / clear APIs", 235),
        ("Status", "Building practical developer tools", 258),
        ("ToolChain", "Git, Actions, Docker, Kubernetes", 281),
        ("Core.Lang", "Java, Kotlin, TypeScript", 318),
        ("Core.Tools", "Python, Rust", 341),
        ("Core.Backend", "Spring Boot / JVM", 364),
        ("Core.Database", "PostgreSQL", 387),
        ("Core.Infra", "Kubernetes, Prometheus, Grafana", 410),
        ("Grid.Blog", "devy1540.dev", 459),
        ("Grid.GitHub", "@devy1540", 482),
        ("Grid.Company", "Day1Company Lemonade", 505),
    ]
    row_markup = "".join(row(*item, theme) for item in rows)
    portrait = grouped_portrait_paths(points, theme, seed)
    travellers = traveller_circles(points, theme, seed + 100)
    pill_width = 170

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Hyukjun Yoon - backend and platform engineer">
  <title>Hyukjun Yoon - profile.sh --live</title>
  <defs>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{theme["border_a"]}"/>
      <stop offset="1" stop-color="{theme["border_b"]}"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="portrait-clip"><rect width="{GRID_WIDTH}" height="{GRID_HEIGHT}" rx="4"/></clipPath>
  </defs>

  <rect x="2" y="2" width="1176" height="606" rx="22" fill="{theme["background"]}" stroke="url(#border)" stroke-width="3"/>
  <path d="M3 72h1174" stroke="{theme["line"]}" stroke-width="1"/>
  <circle cx="42" cy="38" r="9" fill="#FF5F57"/>
  <circle cx="72" cy="38" r="9" fill="#FEBB2E"/>
  <circle cx="102" cy="38" r="9" fill="#28C840"/>
  <text x="615" y="45" fill="{theme["muted"]}" font-size="17" text-anchor="middle" letter-spacing=".7">devy1540@github.com - % ./profile.sh --live</text>

  <text x="38" y="113" fill="{theme["subtle"]}" font-size="13" letter-spacing="6">VISUAL.MAP</text>
  {corner_frame(theme)}
  <g transform="translate(50 132) scale(1.24)" clip-path="url(#portrait-clip)">
    {portrait}
    {travellers}
  </g>

  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin=".45s" dur=".7s" fill="freeze"/>
    <text x="470" y="107" fill="{theme["chrome"]}" font-size="18" font-weight="700" letter-spacing="3">SYSTEM.INFO</text>
    <line x1="619" y1="101" x2="1125" y2="101" stroke="{theme["line"]}" stroke-width="1"/>
    <circle cx="1083" cy="101" r="4" fill="#F87171">
      <animate attributeName="opacity" values="1;.25;1" dur="1.7s" repeatCount="indefinite"/>
    </circle>
    <text x="1095" y="106" fill="#F87171" font-size="12">LIVE</text>
    <rect x="470" y="120" width="{pill_width}" height="24" rx="5" fill="{theme["pill"]}"/>
    <text x="482" y="137" fill="{theme["pill_text"]}" font-size="14" font-weight="700">devy1540@seoul</text>

    {row_markup}

    <line x1="470" y1="431" x2="1125" y2="431" stroke="{theme["line"]}" stroke-width="1"/>
    <text x="470" y="436" fill="{theme["muted"]}" font-size="12">- Public grid</text>
    <text x="470" y="570" fill="{theme["muted"]}" font-size="13">&gt; More projects and engineering notes below in README</text>
    <rect x="902" y="558" width="8" height="15" fill="{theme["chrome"]}" opacity=".7">
      <animate attributeName="opacity" values=".15;1;.15" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
"""


def pill(x: int, y: int, label: str) -> tuple[str, int]:
    width = max(56, 18 + len(label) * 7)
    markup = (
        f'<rect x="{x}" y="{y}" width="{width}" height="22" rx="11" '
        'fill="#241B47" stroke="#6D5BAE" stroke-width="1"/>'
        f'<text x="{x + width / 2:.1f}" y="{y + 15}" fill="#C4B5FD" '
        f'font-size="11" text-anchor="middle">{xml(label)}</text>'
    )
    return markup, width


def render_projects() -> str:
    cards = []
    for index, (name, description, tags) in enumerate(PROJECTS):
        column = index % 2
        row_index = index // 2
        x = 28 + column * 574
        y = 92 + row_index * 139
        card_width = 550
        tag_x = x + 24
        tag_markup = []
        for tag in tags:
            current, width = pill(tag_x, y + 96, tag)
            tag_markup.append(current)
            tag_x += width + 8
        cards.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{0.25 + index * 0.12:.2f}s" dur=".55s" fill="freeze"/>'
            f'<rect x="{x}" y="{y}" width="{card_width}" height="124" rx="12" fill="#0D1526" stroke="#22314D"/>'
            f'<path d="M{x} {y + 34}h{card_width}" stroke="#22314D"/>'
            f'<circle cx="{x + 18}" cy="{y + 17}" r="3" fill="#22D3EE"/>'
            f'<text x="{x + 28}" y="{y + 21}" fill="#94A3B8" font-size="11">devy1540/{xml(name)}</text>'
            f'<circle cx="{x + card_width - 18}" cy="{y + 17}" r="4" fill="#10B981"/>'
            f'<text x="{x + 24}" y="{y + 61}" fill="#F8FAFC" font-size="18" font-weight="700">{xml(name)}</text>'
            f'<text x="{x + 24}" y="{y + 82}" fill="#94A3B8" font-size="12">{xml(description)}</text>'
            f'{"".join(tag_markup)}'
            "</g>"
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="520" viewBox="0 0 1180 520" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Selected public projects by devy1540">
  <title>Selected public projects</title>
  <rect width="1180" height="520" rx="18" fill="#0A101F"/>
  <text x="28" y="42" fill="#22D3EE" font-size="16" letter-spacing="3">PROJECTS.LIST</text>
  <text x="220" y="42" fill="#64748B" font-size="15">./projects.sh --public</text>
  <line x1="28" y1="62" x2="1152" y2="62" stroke="#22314D"/>
  {"".join(cards)}
</svg>
"""


def render_stats_card(
    mode: str,
    user: dict,
    repos: list[dict],
    generated_date: str,
) -> str:
    theme = THEMES[mode]
    metrics = (
        ("PUBLIC REPOS", int(user["public_repos"])),
        ("STARS EARNED", sum(int(repo["stargazers_count"]) for repo in repos)),
        ("FOLLOWERS", int(user["followers"])),
    )
    metric_markup = []
    for index, (label, value) in enumerate(metrics):
        x = 24 + index * 178
        metric_markup.append(
            f'<rect x="{x}" y="78" width="160" height="92" rx="10" '
            f'fill="{theme["panel"]}" stroke="{theme["line"]}"/>'
            f'<text x="{x + 16}" y="119" fill="{theme["text"]}" '
            f'font-size="28" font-weight="700">{value}</text>'
            f'<text x="{x + 16}" y="146" fill="{theme["muted"]}" '
            f'font-size="11" letter-spacing="1.2">{label}</text>'
        )
    created_year = str(user["created_at"])[:4]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="210" viewBox="0 0 560 210" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="devy1540 public GitHub activity">
  <title>devy1540 public GitHub activity</title>
  <rect x="1" y="1" width="558" height="208" rx="14" fill="{theme["background"]}" stroke="{theme["line"]}"/>
  <text x="24" y="34" fill="{theme["chrome"]}" font-size="15" font-weight="700" letter-spacing="2">PUBLIC.ACTIVITY</text>
  <text x="24" y="57" fill="{theme["muted"]}" font-size="11">github.com/devy1540 - since {created_year}</text>
  {"".join(metric_markup)}
  <text x="24" y="194" fill="{theme["subtle"]}" font-size="10">GitHub public API - generated {generated_date}</text>
</svg>
"""


def render_languages_card(
    mode: str,
    repos: list[dict],
    generated_date: str,
) -> str:
    theme = THEMES[mode]
    counter = collections.Counter(
        repo.get("language") or "Other"
        for repo in repos
        if not repo.get("fork")
    )
    total = sum(counter.values())
    top = counter.most_common(3)
    remaining = total - sum(count for _, count in top)
    if remaining:
        top.append(("Go / Rust / Kotlin", remaining))
    colours = (theme["portrait"], theme["chrome"], theme["accent"], "#F59E0B")
    bar_markup = []
    for index, ((label, count), colour) in enumerate(zip(top, colours)):
        y = 79 + index * 27
        percentage = (count / total * 100) if total else 0
        bar_width = max(3.0, 300 * percentage / 100)
        bar_markup.append(
            f'<text x="24" y="{y + 11}" fill="{theme["text"]}" '
            f'font-size="11">{xml(label)}</text>'
            f'<rect x="175" y="{y}" width="300" height="12" rx="6" '
            f'fill="{theme["panel"]}" stroke="{theme["line"]}"/>'
            f'<rect x="175" y="{y}" width="{bar_width:.1f}" height="12" rx="6" '
            f'fill="{colour}"/>'
            f'<text x="492" y="{y + 11}" fill="{theme["muted"]}" '
            f'font-size="10">{count} repos</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="210" viewBox="0 0 560 210" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Primary languages across public repositories">
  <title>Primary languages across public repositories</title>
  <rect x="1" y="1" width="558" height="208" rx="14" fill="{theme["background"]}" stroke="{theme["line"]}"/>
  <text x="24" y="34" fill="{theme["chrome"]}" font-size="15" font-weight="700" letter-spacing="2">PRIMARY.LANGUAGES</text>
  <text x="24" y="57" fill="{theme["muted"]}" font-size="11">{total} owned public repositories - primary language count</text>
  {"".join(bar_markup)}
  <text x="24" y="194" fill="{theme["subtle"]}" font-size="10">GitHub public API - generated {generated_date}</text>
</svg>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--avatar",
        default=AVATAR_URL,
        help="Public image URL or local image path",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT,
        help="Directory for dark.svg, light.svg, and projects.svg",
    )
    parser.add_argument("--seed", type=int, default=1540)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    avatar = load_avatar(args.avatar)
    user = fetch_json(PROFILE_API_URL)
    repos = fetch_json(REPOS_API_URL)
    if not isinstance(user, dict) or not isinstance(repos, list):
        raise RuntimeError("GitHub public API returned an unexpected payload")
    generated_date = datetime.datetime.now(datetime.UTC).date().isoformat()
    point_counts = []
    for mode in ("dark", "light"):
        points = portrait_points(avatar, args.seed, mode)
        if len(points) < TRAVELLER_DOTS:
            raise RuntimeError(f"{mode} portrait produced too few dots: {len(points)}")
        point_counts.append(f"{mode}={len(points)}")
        output = args.output_dir / f"{mode}.svg"
        output.write_text(render_banner(mode, points, args.seed), encoding="utf-8")
        (args.output_dir / f"stats-{mode}.svg").write_text(
            render_stats_card(mode, user, repos, generated_date),
            encoding="utf-8",
        )
        (args.output_dir / f"languages-{mode}.svg").write_text(
            render_languages_card(mode, repos, generated_date),
            encoding="utf-8",
        )
    (args.output_dir / "projects.svg").write_text(render_projects(), encoding="utf-8")

    print(f"portrait dots: {', '.join(point_counts)}")
    for name in (
        "dark.svg",
        "light.svg",
        "stats-dark.svg",
        "stats-light.svg",
        "languages-dark.svg",
        "languages-light.svg",
        "projects.svg",
    ):
        path = args.output_dir / name
        print(f"{name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
