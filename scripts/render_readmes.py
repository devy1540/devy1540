#!/usr/bin/env python3
"""Render the profile READMEs and explicit SVG locale selections."""

import argparse
import copy
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
SVG_LOCALES = {"en": "en", "ko": "ko", "ja": "ja", "zh-CN": "zh-Hans", "es": "es", "fr": "fr"}
ET.register_namespace("", SVG_NS)


def localized_svg(source):
    source = re.sub(
        r"  <!-- Locale overrides: start -->.*?  <!-- Locale overrides: end -->\n",
        "",
        source,
        flags=re.S,
    )
    source = re.sub(
        r"    /\* Locale overrides: start \*/.*?    /\* Locale overrides: end \*/\n",
        "",
        source,
        flags=re.S,
    )
    tree = ET.fromstring(source)
    switches = tree.findall(f"{{{SVG_NS}}}switch")
    groups = []
    for locale, svg_locale in SVG_LOCALES.items():
        group = ET.Element(f"{{{SVG_NS}}}g", {
            "id": f"locale-{locale}", "class": "locale-override", "lang": svg_locale,
        })
        for switch in switches:
            selected = next(child for child in switch if child.get("lang") == svg_locale)
            selected = copy.deepcopy(selected)
            selected.attrib.pop("systemLanguage", None)
            group.append(selected)
        ET.indent(group, space="  ")
        groups.append("\n".join("  " + line for line in ET.tostring(group, encoding="unicode").strip().splitlines()))
    block = "  <!-- Locale overrides: start -->\n" + "\n".join(groups) + "\n  <!-- Locale overrides: end -->\n"
    source = source.replace("  <switch>\n", block + "  <switch>\n", 1)
    css = (
        "    /* Locale overrides: start */\n"
        "    .locale-override { display: none; }\n"
        "    .locale-override:target { display: inline; }\n"
        "    .locale-override:target ~ switch { display: none; }\n"
        "    /* Locale overrides: end */\n"
    )
    before, after = source.split("</style>", 1)
    return before.rstrip() + "\n" + css + "  </style>" + after


def render(locale, shared, text, header, automatic=False):
    hero = ET.fromstring((ROOT / "assets/profile-hero-light.svg").read_text())
    switch = hero.find(f"{{{SVG_NS}}}switch")
    selected = next(child for child in switch if child.get("lang") == SVG_LOCALES[locale])
    copy_text = " ".join("".join(node.itertext()) for node in selected.iter(f"{{{SVG_NS}}}text"))
    alt = html.escape(f"Applied AI Engineer | Backend Engineer. {copy_text}", quote=True)
    header = re.sub(r'(<img[^>]+alt=")[^"]*(")', lambda match: match[1] + alt + match[2], header, count=1)
    if not automatic:
        header = re.sub(r"(\.svg)(?=[\"'])", rf"\1#locale-{locale}", header)
    navigation = " · ".join(
        f"<a href=\"./{filename}\" lang=\"{code}\">{html.escape(shared['locale_names'][code])}</a>"
        for code, filename in shared["readme_files"].items()
    )
    sections = [
        "<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->",
        f"<p align=\"center\">{navigation}</p>",
        header.strip(),
        f"## {text['headings'][0]}",
        "\n\n".join(text["about"]),
        f"## {text['headings'][1]}",
    ]
    experience = []
    for name, description, links in zip(text["experience_names"], text["experience"], shared["experience_links"], strict=True):
        references = " · ".join(f"[{text['link_names'][link['key']]}]({link['url']})" for link in links)
        experience.append(f"- **{name}** — {description} {references}")
    sections.extend([
        "\n\n".join(experience),
        f"## {text['headings'][2]}",
        "\n\n".join(
            f"- **[{project['name']}]({project['url']})** — {description}"
            for project, description in zip(shared["projects"], text["projects"], strict=True)
        ),
        f"## {text['headings'][3]}",
        f"{text['current_focus']} [{text['focus_link']}]({shared['current_focus_url']})",
        f"## {text['headings'][4]}",
        "\n".join(f"- {item}" for item in text["working_style"]),
        f"## {text['headings'][5]}",
        text["writing_note"],
        "\n".join(f"- [{title}]({url})" for title, url in zip(text["writing"], shared["writing_urls"], strict=True)),
        f"## {text['headings'][6]}",
    ])
    contact = shared["contact"]
    labels = text["contact_names"]
    sections.append(" · ".join([
        f"[{labels[0]}]({contact['portfolio']})",
        f"[{labels[1]}]({contact['blog']})",
        f"[{labels[2]}: {contact['email']}](mailto:{contact['email']})",
        f"[{labels[3]}]({contact['linkedin']})",
    ]))
    return "\n\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated files without writing them")
    args = parser.parse_args()
    content = json.loads((ROOT / "profile/content.json").read_text())
    shared, locales = content["shared"], content["locales"]
    if set(locales) != set(SVG_LOCALES) or set(shared["readme_files"]) != set(SVG_LOCALES):
        raise ValueError("Expected the same six locales in content and file mappings")
    header = (ROOT / "profile/header.html").read_text()
    files = {"README.md": render("en", shared, locales["en"], header, automatic=True)}
    for locale, filename in shared["readme_files"].items():
        if Path(filename).name != filename or not re.fullmatch(r"README\.[a-z]{2}(?:-[A-Z]{2})?\.md", filename):
            raise ValueError(f"Invalid README output: {filename}")
        text = locales[locale]
        if len(text["headings"]) != 7 or len(text["contact_names"]) != 4:
            raise ValueError(f"Incomplete headings or contacts: {locale}")
        files[filename] = render(locale, shared, text, header)
    for path in (ROOT / "assets").glob("profile-*.svg"):
        files[str(path.relative_to(ROOT))] = localized_svg(path.read_text())
    differences = []
    for name, expected in files.items():
        path = ROOT / name
        if not path.exists() or path.read_text() != expected:
            differences.append(name)
            if not args.check:
                path.write_text(expected)
    if args.check and differences:
        raise SystemExit("Generated files need updating: " + ", ".join(differences))
    print(f"{'Checked' if args.check else 'Rendered'} {len(files)} files; six languages")


if __name__ == "__main__":
    main()
