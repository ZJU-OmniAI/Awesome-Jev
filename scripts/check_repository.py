#!/usr/bin/env python3
"""Check catalog parity, local links, anchors, example structure, and publishable text.

Run --online for an optional HTTP audit. Network failures are reported distinctly
from missing local files; no model service is invoked and no credentials are read.
"""
import argparse
import concurrent.futures
import datetime
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)|(?:src|href)="([^"]+)"')


def anchors(path):
    content = path.read_text()
    result = set(re.findall(r'<a\s+id="([^"]+)"', content))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$', content, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(slug + (f'-{count}' if count else ''))
    return result


def check():
    errors = []
    data = json.loads((ROOT / 'data/resources.json').read_text())
    items = data['resources']
    ids, urls = set(), set()
    for item in items:
        rid = item['id']
        if rid in ids:
            errors.append(f'Duplicate resource ID: {rid}')
        if item['url'] in urls:
            errors.append(f'Duplicate primary URL: {rid}')
        ids.add(rid)
        urls.add(item['url'])
        if item['track'] not in ('foundations', 'agents', 'embodied'):
            errors.append(f'Unknown track: {rid}')
        if not item['url'].startswith('https://'):
            errors.append(f'Primary URL must use HTTPS: {rid}')
        if not item['evidence'] or not set(item['evidence']) <= {'official', 'paper', 'project', 'demo', 'proposal', 'background'}:
            errors.append(f'Unknown evidence label: {rid}')
        for field in ('summary', 'scope'):
            if set(item[field]) != {'en', 'zh'} or not all(item[field].values()):
                errors.append(f'Missing bilingual {field}: {rid}')
        datetime.date.fromisoformat(item['reviewed_on'])
        if not item.get('source_snapshot'):
            errors.append(f'Missing snapshot note: {rid}')
    checked_links = 0
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        content = path.read_text()
        if re.search(r'/Users/|/home/|file://|http://(?:localhost|127\.0\.0\.1)', content):
            errors.append(f'Nonportable private path: {path.relative_to(ROOT)}')
        for match in LINK.finditer(content):
            target = match[1] or match[2]
            parsed = urllib.parse.urlsplit(target)
            if parsed.scheme:
                continue
            local = (path.parent / urllib.parse.unquote(parsed.path)).resolve() if parsed.path else path
            if not local.is_relative_to(ROOT):
                errors.append(f'Link escapes repository: {path.relative_to(ROOT)} -> {target}')
            elif not local.exists():
                errors.append(f'Missing local link: {path.relative_to(ROOT)} -> {target}')
            elif parsed.fragment and local.suffix == '.md' and urllib.parse.unquote(parsed.fragment) not in anchors(local):
                errors.append(f'Missing anchor: {path.relative_to(ROOT)} -> {target}')
            checked_links += 1
    for name in ('report', 'foundations', 'multimodal', 'community-models', 'agents', 'embodied', 'evaluation', 'roadmap'):
        for suffix in ('', '_zh'):
            if not (ROOT / f'docs/{name}{suffix}.md').is_file():
                errors.append(f'Missing language counterpart: {name}{suffix}')
    example = json.loads((ROOT / 'examples/decision_request.json').read_text())
    if {q['type'] for q in example['questions'].values()} != {'choice', 'score', 'noul'}:
        errors.append('Example must cover the three documented primitives')
    if not isinstance(example['state'], dict) or not example.get('model'):
        errors.append('Example requires a model and structured state')
    multimodal = json.loads((ROOT / 'examples/multimodal_request.json').read_text())
    if {q['type'] for q in multimodal['questions'].values()} != {'choice', 'score', 'noul', 'box'}:
        errors.append('Multimodal example must cover all four question types')
    if multimodal['state']['photo'] not in multimodal.get('assets', {}):
        errors.append('Multimodal image reference has no corresponding asset')
    for question in multimodal['questions'].values():
        if question['type'] == 'box' and 'criteria' in question:
            errors.append('Box questions must not include criteria')
    for path in (ROOT / 'data').glob('*.json'):
        json.loads(path.read_text())
    for path in (ROOT / 'assets').glob('*.svg'):
        ET.parse(path)
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or path.suffix not in ('.md', '.json', '.py', '.yml', '.cff'):
            continue
        if re.search(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,})\b', path.read_text()):
            errors.append(f'Possible credential in {path.relative_to(ROOT)}')
    if errors:
        raise SystemExit('\n'.join(errors))
    subprocess.run([sys.executable, str(ROOT / 'scripts/update_catalog.py'), '--check'], check=True)
    print(f'PASS: {len(items)} resources, bilingual guides, '
          f'{checked_links} local links/anchors, SVG and examples.')


def probe(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Awesome-Jev-Link-Audit/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            # Read a bounded prefix to verify that the server responds, without archiving content.
            response.read(1024)
            return {'url': url, 'status': response.status, 'final_url': response.url}
    except urllib.error.HTTPError as exc:
        return {'url': url, 'status': exc.code, 'error': str(exc)}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {'url': url, 'status': None, 'error': str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--online', action='store_true', help='Also audit all primary catalog URLs')
    parser.add_argument('--report', type=Path, help='Write the online audit as JSON to this explicit path')
    args = parser.parse_args()
    check()
    if args.online:
        items = json.loads((ROOT / 'data/resources.json').read_text())['resources']
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(probe, [i['url'] for i in items]))
        for result in results:
            print(f'{result["status"] or "NETWORK_ERROR"}: {result["url"]}')
        if args.report:
            args.report.write_text(json.dumps({'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'results': results}, indent=2) + '\n')
        if any(r['status'] is None or r['status'] >= 400 for r in results):
            raise SystemExit('Some remote links could not be verified; inspect the HTTP/network status above.')


if __name__ == '__main__':
    main()
