"""
LISP-7 Level 3: Triadic Extraction
Extracts first, middle, and last letter of each word.
"""


def compress(text):
    """
    Compress text using Level 3 (triadic extraction).

    Args:
        text: Input text to compress

    Returns:
        str: Compressed text with triadic extraction
    """
    if not text:
        return ""

    result = []
    words = text.split()

    for word in words:
        if len(word) == 0:
            continue

        clean_word = word.lower()
        punct = ""
        if clean_word and not clean_word[-1].isalpha():
            punct = clean_word[-1]
            clean_word = clean_word[:-1]

        if not clean_word:
            continue

        if len(clean_word) == 1:
            compressed = clean_word
        elif len(clean_word) == 2:
            compressed = clean_word[0]
        elif len(clean_word) == 3:
            compressed = clean_word
        else:
            first = clean_word[0]
            middle_index = len(clean_word) // 2
            middle = clean_word[middle_index]
            last = clean_word[-1]
            compressed = first + middle + last

        if not compressed:
            compressed = clean_word[0] if clean_word else ""

        if word[0].isupper():
            compressed = compressed.capitalize()

        result.append(compressed + punct)

    return " ".join(result)
