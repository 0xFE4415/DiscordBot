import unicodedata

from rapidfuzz import fuzz, process


def normalize_text(text: str) -> str:
    cyrillic_to_human_letter_map = {
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
        "+": "t",
        "|": "i",
    }

    translation_table = str.maketrans(cyrillic_to_human_letter_map)
    text = text.translate(translation_table)

    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def is_autism_variant(text: str) -> bool:

    normalized = normalize_text(text)

    cleaned = "".join(c for c in normalized if c.isalpha()).lower()
    if len(cleaned) < 5:
        return False
    targets = ["autism", "autyzm", "autistic", "lubiepociagi"]

    result = process.extractOne(cleaned, targets, scorer=fuzz.partial_ratio)
    return result is not None and result[1] >= 92

def is_meow_variant(text: str) -> bool:

    normalized = normalize_text(text)

    cleaned = "".join(c for c in normalized if c.isalpha()).lower()
    if len(cleaned) < 5:
        return False
    targets = ["meow", "miau", "nya"]

    result = process.extractOne(cleaned, targets, scorer=fuzz.partial_ratio)
    return result is not None and result[1] >= 92

