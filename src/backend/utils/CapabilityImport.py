"""
One-time bulk import of the business capability hierarchy from a Word
document (F12), per the requirements' Key Decision: the source document
uses Word's built-in Heading 1-4 styles for hierarchy *and* literal numbered
text (e.g. "1.2.3") in the same paragraph for the reference code — so no
Word auto-numbering XML needs parsing, just the paragraph style and a
leading "\\d+(\\.\\d+)*" token.
"""

import re

from docx import Document

_HEADING_LEVEL_RE = re.compile(r'^Heading (\d)$')
_REF_CODE_RE = re.compile(r'^(\d+(?:\.\d+)*)')


def parse_capability_document(file_obj):
    """
    Parse an uploaded .docx into a flat, ordered list of capability dicts
    (refCode, level, name, parentRefCode, order), ready for bulk insert.
    Parent linkage is inferred from the most recently seen heading at the
    next level up.
    """
    document = Document(file_obj)
    capabilities = []
    ancestor_ref_code_by_level = {}
    order = 0

    for paragraph in document.paragraphs:
        level = _heading_level(paragraph.style.name if paragraph.style else None)
        text = paragraph.text.strip()
        if level is None or not text:
            continue

        ref_code, name = _split_ref_code(text)
        if not name:
            continue
        if ref_code is None:
            # No literal numbering on this heading; synthesise a stable
            # placeholder so the row still imports rather than being dropped.
            ref_code = 'L{}-{}'.format(level, order)

        order += 1
        capabilities.append({
            'refCode': ref_code,
            'level': level,
            'name': name,
            'parentRefCode': ancestor_ref_code_by_level.get(level - 1),
            'order': order,
        })

        ancestor_ref_code_by_level[level] = ref_code
        for deeper_level in [lvl for lvl in ancestor_ref_code_by_level if lvl > level]:
            del ancestor_ref_code_by_level[deeper_level]

    return capabilities


def _heading_level(style_name):
    match = _HEADING_LEVEL_RE.match(style_name or '')
    if not match:
        return None
    level = int(match.group(1))
    return level if 1 <= level <= 4 else None


def _split_ref_code(text):
    match = _REF_CODE_RE.match(text)
    if not match:
        return None, text
    ref_code = match.group(1)
    name = text[match.end():].strip(' .-:\t')
    return ref_code, name
