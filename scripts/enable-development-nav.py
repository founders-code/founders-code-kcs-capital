#!/usr/bin/env python3
"""Enable live 4orm Finance / 4ormEx links in Development nav dropdown."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_DEV_BLOCK = re.compile(
    r'<li class="nav-drop">\s*'
    r'<a\s+href="#"\s+class="nav-drop-trigger"[^>]*>Development</a>\s*'
    r'<ul class="nav-drop-menu">\s*'
    r'<li><a\s+href="javascript:void\(0\)"\s+class="nav-drop-coming"[^>]*>'
    r'4orm Finance\s*<span class="nav-drop-soon">Coming soon</span></a></li>\s*'
    r'<li><a\s+href="javascript:void\(0\)"\s+class="nav-drop-coming"[^>]*>'
    r'4ormEx\s*<span class="nav-drop-sub">\(Exchange\)</span>\s*'
    r'<span class="nav-drop-soon">Coming soon</span></a></li>\s*'
    r'</ul>\s*</li>',
    re.DOTALL,
)

NEW_DEV_COMPACT = (
    '<li class="nav-drop">'
    '<a href="#" class="nav-drop-trigger" aria-haspopup="true" aria-expanded="false" tabindex="0">Development</a>'
    '<ul class="nav-drop-menu">'
    '<li><a href="https://www.4ormfinance.com" target="_blank" rel="noopener">4orm Finance</a></li>'
    '<li><a href="https://www.4ormex.com" target="_blank" rel="noopener">'
    '4ormEx <span class="nav-drop-sub">(Exchange)</span></a></li>'
    '</ul></li>'
)

INSERT_BEFORE_CTA = re.compile(
    r'(<li><a href="/contact" class="nav-cta">Contact Us</a></li>)'
)

CSS_OLD = re.compile(r'/styles\.css(?:\?v=\d+)?')
CSS_NEW = '/styles.css?v=20260611'


def process(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    original = text
    action = 'skipped'

    if OLD_DEV_BLOCK.search(text):
        text = OLD_DEV_BLOCK.sub(NEW_DEV_COMPACT, text, count=1)
        action = 'replaced'
    elif 'nav-drop-coming' not in text and INSERT_BEFORE_CTA.search(text):
        text = INSERT_BEFORE_CTA.sub(NEW_DEV_COMPACT + r'\1', text, count=1)
        action = 'inserted'
    elif 'nav-drop-coming' in text:
        action = 'unmatched'

    text = CSS_OLD.sub(CSS_NEW, text)

    if text != original:
        path.write_text(text, encoding='utf-8')
    elif action == 'skipped' and CSS_OLD.search(original):
        path.write_text(text, encoding='utf-8')
    return action


def main() -> None:
    changed = []
    inserted = []
    skipped = []
    unmatched = []

    for path in sorted(ROOT.glob('*.html')):
        action = process(path)
        if action == 'replaced':
            changed.append(path.name)
        elif action == 'inserted':
            inserted.append(path.name)
        elif action == 'unmatched':
            unmatched.append(path.name)
        else:
            skipped.append(path.name)

    print('REPLACED:', len(changed))
    for n in changed:
        print(f'  {n}')
    print('INSERTED:', len(inserted))
    for n in inserted:
        print(f'  {n}')
    print('SKIPPED:', len(skipped))
    for n in skipped:
        print(f'  {n}')
    if unmatched:
        print('UNMATCHED:', len(unmatched))
        for n in unmatched:
            print(f'  {n}')


if __name__ == '__main__':
    main()
