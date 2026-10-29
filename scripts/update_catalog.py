#!/usr/bin/env python3
"""Render the bilingual catalog from data/resources.json using only the stdlib."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ("foundations", "agents", "embodied")
LABELS = {
    "en": {"official": "Official", "paper": "Paper", "project": "Project", "demo": "Demo", "proposal": "Proposal", "background": "Background"},
    "zh": {"official": "官方资料", "paper": "论文", "project": "项目", "demo": "演示", "proposal": "设想", "background": "背景工作"},
}


def cell(value):
    return value.replace("|", "&#124;").replace("\n", " ")


def render_table(resources, track, lang):
    headers = ["Resource", "Role / takeaway", "Evidence and scope"] if lang == "en" else ["资源", "作用与要点", "证据及适用范围"]
    rows = ["| " + " | ".join(headers) + " |", "| --- | --- | --- |"]
    for item in resources:
        if item["track"] != track:
            continue
        labels = " / ".join(LABELS[lang][label] for label in item["evidence"])
        rows.append(f'| [{cell(item["title"])}]({item["url"]}) | {cell(item["summary"][lang])} | **{labels}** · {cell(item["scope"][lang])} |')
    return "\n".join(rows)


def update(text, key, content):
    pattern = rf"(<!-- BEGIN {key} -->\n).*?(<!-- END {key} -->)"
    output, count = re.subn(pattern, lambda m: m[1] + content + "\n" + m[2], text, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one block for {key}, found {count}")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed tables differ from the catalog")
    args = parser.parse_args()
    resources = json.loads((ROOT / "data/resources.json").read_text())["resources"]
    stale = []
    for lang, filename in (("en", "README.md"), ("zh", "README_zh.md")):
        path = ROOT / filename
        original = path.read_text()
        output = original
        counts = [sum(r["track"] == t for r in resources) for t in TRACKS]
        summary = (f"**{len(resources)} curated resources** · Foundations {counts[0]} · Agents {counts[1]} · Embodied AI {counts[2]}"
                   if lang == "en" else f"**{len(resources)} 项精选资源** · 模型基础 {counts[0]} · Agent 应用 {counts[1]} · 具身智能 {counts[2]}")
        output = update(output, "COUNTS", summary)
        for track in TRACKS:
            output = update(output, track.upper(), render_table(resources, track, lang))
        if output != original:
            stale.append(filename)
            if not args.check:
                path.write_text(output)
    if stale and args.check:
        raise SystemExit("Stale generated tables: " + ", ".join(stale))
    print(f"Catalog {'checked' if args.check else 'generated'}: {len(resources)} resources, two languages.")


if __name__ == "__main__":
    main()
