import re

def fix_spacing(text):
    """dnd5eapi's 2024 /traits/ endpoint sometimes returns letter-spaced text
    (e.g. 'Y o u   h a v e' where single-space separates letters and 2+ spaces
    separate words). Detect and repair; leave normal text untouched."""
    if not text:
        return text
    tokens = text.split(' ')
    if not tokens:
        return text
    single_char_ratio = sum(1 for t in tokens if len(t) <= 1) / len(tokens)
    if single_char_ratio < 0.6:
        return text
    words = re.split(r' {2,}', text)
    return ' '.join(w.replace(' ', '') for w in words)
