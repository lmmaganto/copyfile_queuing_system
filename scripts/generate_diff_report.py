import sys
import json
import re
import difflib
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output for Windows/GitHub Action environments
sys.stdout.reconfigure(encoding='utf-8')

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
                'changes': []
            })
            continue
            
        if cell['cell_type'] != 'code':
            continue
            
        source = ''.join(cell['source'])
        if not source.strip():
            continue

        source_cite = None
        changes = []
        code_lines = []
        
        for line in source.splitlines():
            # Extract Citation
            if re.search(r'#\s*SOURCE:', line, re.IGNORECASE):
                source_cite = re.sub(r'#\s*SOURCE:\s*', '', line, flags=re.IGNORECASE).strip()
                code_lines.append(line)
            # Extract Changes
            else:
                match = re.search(r'#\s*CHANGED:\s*(.*)', line, re.IGNORECASE)
                if match:
                    reason = match.group(1).strip()
                    code_part = line[:match.start()].rstrip()
                    
                    if code_part.strip():
                        changes.append({'line': code_part.strip(), 'reason': reason})
                        code_lines.append(line) # Keep the full line for diffing
                    else:
                        # Reason is above the code, mark it for the next line
                        changes.append({'line': None, 'reason': reason})
                        code_lines.append(line)
                else:
                    # Attach previous 'above-line' reason if it exists
                    if changes and changes[-1]['line'] is None:
                        changes[-1]['line'] = line.strip()
                    code_lines.append(line)

        cells.append({
            'index': i,
            'type': 'code',
            'source': source,
            'code': '\n'.join(code_lines).strip(),
            'source_cite': source_cite,
            'changes': changes
        })
    return cells

def parse_metadata(path):
    with open(path, 'r', encoding='utf-8') as f:
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
        print(f'Error: review_metadata.yml not found in {folder}')
        return

    meta = parse_metadata(meta_path)
    original_name = meta.get('original_notebook', '').strip()
    review_name = meta.get('review_copy_notebook', '').strip()
    reviewer = meta.get('reviewer', 'unknown').strip()

    original_path = folder / 'original' / original_name
    review_path = folder / 'review-copy' / review_name

    if not original_path.exists() or not review_path.exists():
        print(f'Missing notebooks in {folder}')
        return

    r1_cells = parse_notebook(original_path)
    r2_cells = parse_notebook(review_path)

    r1_meta = extract_markdown_fields(r1_cells[0]['source']) if r1_cells else {}
    r2_meta = extract_markdown_fields(r2_cells[0]['source']) if r2_cells else {}

    curator = r1_meta.get('Curator', 'unknown')
    title = r1_meta.get('Title', 'Unknown paper')
    
    agreed = []
    disagreed = []
    
    r1_code = [c for c in r1_cells if c['type'] == 'code']
    r2_code = [c for c in r2_cells if c['type'] == 'code']

    for c1, c2 in zip(r1_code, r2_code):
        if c1['code'] == c2['code']:
            agreed.append(c1)
        else:
            disagreed.append({
                'cell': c1['index'],
                'cite': c1['source_cite'] or c2['source_cite'] or 'No Citation',
                'r1': c1['code'],
                'r2': c2['code'],
                'changes': c2['changes']
            })

    # Build Markdown
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        f'# 📝 Diff Report: {title}',
        f'\n**Curator:** @{curator} | **Reviewer:** @{reviewer}',
        f'\n**Generated:** {now}',
        '\n---\n',
        '## 📊 Summary',
        f'\n| Metric | Count |',
        f'| :--- | :--- |',
        f'| Cells Matched | {len(agreed)} |',
        f'| Cells Flagged | {len(disagreed)} |',
        f'| **Total Changes** | **{sum(len(d["changes"]) for d in disagreed)}** |',
        '\n---'
    ]

    if not disagreed:
        lines.append('\n✅ **Perfect Match:** No differences found between Curator and Reviewer.')
    else:
        lines.append('\n## 🔍 Detected Differences\n')
        for d in disagreed:
            lines.append(f"### 📍 Cell {d['cell']} — {d['cite']}")
            lines.append('\n| Side | Line Content |')
            lines.append('| :--- | :--- |')
            
            diff = difflib.ndiff(d['r1'].splitlines(), d['r2'].splitlines())
            for line in diff:
                if line.startswith('- '):
                    lines.append(f'| ~~Original~~ | ` {line[2:].strip()} ` |')
                elif line.startswith('+ '):
                    clean_line = line[2:].strip()
                    display = f'**`{clean_line}`**' if "#CHANGED:" in clean_line else f'`{clean_line}`'
                    lines.append(f'| **Reviewer** | {display} |')
            
            if d['changes']:
                lines.append('\n**Reasoning:**')
                for c in d['changes']:
                    lines.append(f"- {c['reason']}")
            lines.append('\n---')

    # Footer for Curator
    lines += [
        '\n## 🔔 Curator Notification',
        f'@{curator}: Please review the changes highlighted above by @{reviewer}.'
    ]

    report_path = folder / 'DIFF_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Report successfully generated at {report_path}')

if __name__ == '__main__':
    # Usage: python script.py path/to/folder
    folder_arg = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_report(folder_arg)