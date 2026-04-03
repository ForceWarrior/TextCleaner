import re
import unicodedata
import Config


def _build_mapping():
    mapping = {}

    if Config.ENABLE_CYRILLIC:
        cyrillic = {
            "а": "a", "е": "e", "о": "o", "р": "p", "с": "c",
            "у": "y", "х": "x", "А": "A", "В": "B", "Е": "E",
            "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P",
            "С": "C", "Т": "T", "Х": "X",
            "і": "i", "І": "I",
            "ѕ": "s", "Ѕ": "S",
            "ј": "j", "Ј": "J",
            "ӏ": "l",
            "ԁ": "d",
            "һ": "h", "Һ": "H",
            "ӧ": "o", "Ӧ": "O",
        }
        mapping.update(cyrillic)

    if Config.ENABLE_GREEK:
        greek = {
            "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e",
            "ζ": "z", "η": "h", "θ": "th", "ι": "i", "κ": "k",
            "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
            "π": "p", "ρ": "r", "σ": "s", "τ": "t", "υ": "u",
            "φ": "ph", "χ": "ch", "ψ": "ps", "ω": "o",
            "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H",
            "Ι": "I", "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O",
            "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
        }
        mapping.update(greek)

    if Config.ENABLE_FULLWIDTH:
        fullwidth = {}
        for i in range(26):
            fullwidth[chr(0xFF21 + i)] = chr(ord("A") + i)
            fullwidth[chr(0xFF41 + i)] = chr(ord("a") + i)
        for i in range(10):
            fullwidth[chr(0xFF10 + i)] = chr(ord("0") + i)
        mapping.update(fullwidth)

    return mapping


def _clean_specials(text: str):
    changes = []

    space_like = {
        "\u00A0",  # NO-BREAK SPACE
        "\u1680",  # OGHAM SPACE MARK
        "\u2000", "\u2001", "\u2002", "\u2003",
        "\u2004", "\u2005", "\u2006", "\u2007",
        "\u2008", "\u2009", "\u200A",
        "\u202F",  # NARROW NO-BREAK SPACE
        "\u205F",  # MEDIUM MATHEMATICAL SPACE
        "\u3000",  # IDEOGRAPHIC SPACE
    }

    remove_always = {
        "\u00AD",  # SOFT HYPHEN
        "\u034F",  # COMBINING GRAPHEME JOINER
        "\u061C",  # ARABIC LETTER MARK
        "\u180E",  # MONGOLIAN VOWEL SEPARATOR

        "\u200B",  # ZERO WIDTH SPACE
        "\u200C",  # ZERO WIDTH NON-JOINER
        "\u200D",  # ZERO WIDTH JOINER
        "\u200E",  # LEFT-TO-RIGHT MARK
        "\u200F",  # RIGHT-TO-LEFT MARK

        "\u202A",  # LEFT-TO-RIGHT EMBEDDING
        "\u202B",  # RIGHT-TO-LEFT EMBEDDING
        "\u202C",  # POP DIRECTIONAL FORMATTING
        "\u202D",  # LEFT-TO-RIGHT OVERRIDE
        "\u202E",  # RIGHT-TO-LEFT OVERRIDE

        "\u2060",  # WORD JOINER
        "\u2061",  # FUNCTION APPLICATION
        "\u2062",  # INVISIBLE TIMES
        "\u2063",  # INVISIBLE SEPARATOR
        "\u2064",  # INVISIBLE PLUS
        "\u2066",  # LEFT-TO-RIGHT ISOLATE
        "\u2067",  # RIGHT-TO-LEFT ISOLATE
        "\u2068",  # FIRST STRONG ISOLATE
        "\u2069",  # POP DIRECTIONAL ISOLATE

        "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE / BOM

        "\u115F",  # HANGUL CHOSEONG FILLER
        "\u1160",  # HANGUL JUNGSEONG FILLER
        "\u3164",  # HANGUL FILLER
        "\uFFA0",  # HALFWIDTH HANGUL FILLER

        "\u2800",  # BRAILLE PATTERN BLANK
    }

    out = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        cat = unicodedata.category(ch)

        if ch in space_like:
            out.append(" ")
            changes.append(f"special space U+{cp:04X} -> ' ' (pos {i})")
            continue

        if ch in remove_always:
            changes.append(f"removed invisible U+{cp:04X} (pos {i})")
            continue

        if cat == "Cf":
            changes.append(f"removed format char U+{cp:04X} (pos {i})")
            continue

        if cat == "Cc" and ch not in ("\n", "\r", "\t"):
            changes.append(f"removed control char U+{cp:04X} (pos {i})")
            continue

        out.append(ch)

    text = "".join(out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\r?\n *", "\n", text)

    return text.strip(), changes


def normalize(text: str):
    text = unicodedata.normalize("NFKC", text)

    mapping = _build_mapping()
    changes = []
    result_chars = []

    for i, char in enumerate(text):
        if char in mapping:
            replacement = mapping[char]
            changes.append(f"'{char}' -> '{replacement}' (pos {i})")
            result_chars.append(replacement)
        else:
            result_chars.append(char)

    result = "".join(result_chars)

    if Config.ENABLE_SPECIALS:
        result, special_changes = _clean_specials(result)
        changes.extend(special_changes)
    else:
        result = result.strip()

    return result, changes