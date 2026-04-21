import sys
import json
import re
from pathlib import Path
from datetime import datetime


def parse_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    cells = []
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and i == 0:
            source = ''.join(cell['source'])
            cells.append({
                'index': i,
                'type': 'markdown',
                'source': source,
                'code': None,
                'source_cite': None,
                'changed_reason': None
            })
            continue
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        if not source.strip():
            continue
        source_cite = None
        changed_reasons = []
        code_lines = []
        for line in source.splitlines():
            if line.strip().startswith('# SOURCE:'):
                source_cite = line.replace('# SOURCE:', '').strip()
            else:
                match = re.search(r'#\s*CHANGED:\s*(.*)', line, re.IGNORECASE)
                if match:
                    reason = match.group(1).strip()
                    if reason:
                        changed_reasons.append(reason)
                    code_part = line[:re.search(r'#\s*CHANGED:', line, re.IGNORECASE).start()].rstrip()
                    if code_part.strip():
                        code_lines.append(code_part)
                else:
                    code_lines.append(line)
        changed_reason = ' | '.join(changed_reasons) if changed_reasons else None
        cells.append({
            'index': i,
            'type': 'code',
            'source': source,
            'code': '\n'.join(code_lines).strip(),
            'source_cite': source_cite,
            'changed_reason': changed_reason
        })
    return cells


def parse_metadata(path):
    with open(path, 'r') as f:
        content = f.read()
    meta = {}
    for line in content.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip().strip('"')
    return meta


def extract_markdown_fields(source):
    fields = {}
    for line in source.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip()
    return fields


def generate_report(folder_path):
    folder = Path(folder_path)
    meta_path = folder / 'review_metadata.yml'

    if not meta_path.exists():
        print(f'No review_metadata.yml found in {folder}')
        return

    meta = parse_metadata(meta_path)
    original_name = meta.get('original_notebook', '').strip()
    review_name = meta.get('review_copy_notebook', '').strip()
    reviewer = meta.get('reviewer', 'unknown').strip()

    original_path = folder / 'original' / original_name
    review_path = folder / 'review-copy' / review_name

    if not original_path.exists():
        print(f'Original notebook not found: {original_path}')
        return
    if not review_path.exists():
        print(f'Review notebook not found: {review_path}')
        return

    r1_cells = parse_notebook(original_path)
    r2_cells = parse_notebook(review_path)

    r1_meta = {}
    r2_meta = {}
    if r1_cells and r1_cells[0]['type'] == 'markdown':
        r1_meta = extract_markdown_fields(r1_cells[0]['source'])
    if r2_cells and r2_cells[0]['type'] == 'markdown':
        r2_meta = extract_markdown_fields(r2_cells[0]['source'])

    curator = r1_meta.get('Curator', 'unknown')
    title = r1_meta.get('Title', 'Unknown paper')
    doi = r1_meta.get('DOI', '')
    figure = r1_meta.get('Figure', '')
    r1_outcome = r1_meta.get('Outcome', '')
    r2_outcome = r2_meta.get('Outcome', '')
    r1_notes = r1_meta.get('Notes', '')
    r2_notes = r2_meta.get('Notes', '')

    r1_code = [c for c in r1_cells if c['type'] == 'code']
    r2_code = [c for c in r2_cells if c['type'] == 'code']

    agreed = []
    disagreed = []

    for c1, c2 in zip(r1_code, r2_code):
        if c1['code'] == c2['code']:
            agreed.append(c1)
        else:
            disagreed.append({
                'cell': c1['index'],
                'source_cite': c1['source_cite'] or c2['source_cite'] or 'no citation',
                'r1_code': c1['code'],
                'r2_code': c2['code'],
                'changed_reason': c2['changed_reason']
            })

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        f'# Diff report — {title}',
        f'',
        f'**Curator:** @{curator}  ',
        f'**Reviewer:** @{reviewer}  ',
        f'**DOI:** {doi}  ',
        f'**Figure:** {figure}  ',
        f'**Generated:** {now}  ',
        f'',
        f'---',
        f'',
        f'## Summary',
        f'',
        f'| | Count |',
        f'|---|---|',
        f'| Cells compared | {len(r1_code)} |',
        f'| Agreed | {len(agreed)} |',
        f'| Differences | {len(disagreed)} |',
        f'',
    ]

    if r1_outcome != r2_outcome or r1_notes != r2_notes:
        lines += [
            f'## Metadata changes',
            f'',
            f'| Field | Curator | Reviewer |',
            f'|---|---|---|',
            f'| Outcome | {r1_outcome} | {r2_outcome} |',
            f'| Notes | {r1_notes} | {r2_notes} |',
            f'',
            f'---',
            f'',
        ]

    lines += [f'## Agreements ({len(agreed)})', f'']
    if agreed:
        lines.append('The following cells matched exactly between curator and reviewer.')
        lines.append('')
    else:
        lines.append('No agreements found.')
        lines.append('')

    lines += [f'---', f'', f'## Differences ({len(disagreed)})', f'']
    for d in disagreed:
        lines += [
            f"### Cell {d['cell']} — {d['source_cite']}",
            f'',
            f'**Curator:**',
            f'```python',
            d['r1_code'],
            f'```',
            f'',
            f'**Reviewer:**',
            f'```python',
            d['r2_code'],
            f'```',
            f'',
        ]
        if d['changed_reason']:
            lines += [f"**Reason:** {d['changed_reason']}", f'']
        else:
            lines += [f'**Reason:** not provided', f'']

    report_path = folder / 'DIFF_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Report written to {report_path}')
    print(f'{len(agreed)} agreements, {len(disagreed)} differences')


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else 'reviews/completed/10_1007s00332.023_copy'
    generate_report(folder)