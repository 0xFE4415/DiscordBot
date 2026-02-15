import re
import unicodedata

from rapidfuzz import fuzz, process

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def normalize_text(text: str) -> str:
    letter_map = {
        "а": "a",
        "А": "A",
        "в": "b",
        "В": "B",
        "е": "e",
        "Е": "E",
        "к": "k",
        "К": "K",
        "м": "m",
        "М": "M",
        "н": "h",
        "Н": "H",
        "о": "o",
        "О": "O",
        "р": "p",
        "Р": "P",
        "с": "c",
        "С": "C",
        "т": "t",
        "Т": "T",
        "у": "y",
        "У": "Y",
        "х": "x",
        "Х": "X",
        "і": "i",
        "І": "I",
        "α": "a",
        "ο": "o",
        "ρ": "p",
        "ν": "v",
        "и": "n",
        "µ": "u",
        "¡": "i",
        "|": "i",
    }

    translation_table = str.maketrans(letter_map)
    text = text.translate(translation_table)

    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def is_text_variant(text: str, target: str | list[str], threshold: int = 92, verbose: bool = False) -> bool:

    if isinstance(target, str):
        targets = [t.lower() for t in [target]]
    else:
        targets = [t.lower() for t in target]

    normalized = normalize_text(text)
    cleaned = "".join(c for c in normalized if c.isalnum()).lower()
    result = process.extractOne(cleaned, targets, scorer=fuzz.partial_ratio)

    if result and result[1] >= threshold:
        if verbose:
            print(f"DEBUG: {GREEN}[Match]{RESET} '{text}' {RED}[for any]{RESET} {targets}")
            print(f"DEBUG: \t {YELLOW}[best: '{result[0]}' with score {result[1] if result else 'N/A'}]{RESET}")

        matched = result[0]

        core_pattern = r"[^a-zA-Z0-9]*".join([f"{re.escape(c)}+" for c in matched])
        core_pattern_dyslectic = r"[^a-zA-Z0-9]*".join([f"{re.escape(c)}+" for c in matched[1:-1]])

        validation_pattern = rf"(?<![a-zA-Z0-9]){core_pattern}(?![a-zA-Z0-9])"
        validation_pattern_dyslectic = rf"(?<![a-zA-Z0-9]){core_pattern_dyslectic}(?![a-zA-Z0-9])"

        if verbose:
            print(f"DEBUG: \t {BLUE}[Validation]{RESET} '{matched}' {BLUE}[in]{RESET} '{normalized}'")

        match_obj = re.search(validation_pattern, normalized, re.IGNORECASE)

        if not match_obj and len(matched) > 5:
            match_obj = re.search(validation_pattern_dyslectic, normalized, re.IGNORECASE)

        if match_obj:
            start, end_idx = match_obj.span()

            debug_start = max(0, start - 5)
            debug_end = min(len(normalized), end_idx + 5)

            snippet = normalized[debug_start:debug_end]

            if verbose:
                print(f"DEBUG: \t {BLUE}[Matched]{RESET} '{matched}' {BLUE}[in]{RESET} '{normalized}' {BLUE}[by snippet]{RESET} '{snippet}'")
                print(f"DEBUG: \t {GREEN}[Validation Passed]{RESET}")

            return True

        if verbose:
            print(f"DEBUG: \t {RED}[Validation Failed]{RESET}")
        return False

    if verbose:
        print(f"DEBUG: {RED}[No Match]{RESET} '{text}' {RED}[for any]{RESET} {targets}")
        print(f"DEBUG: \t {YELLOW}[best: '{result[0]}' with score {result[1] if result else 'N/A'}]{RESET}")

    return False
