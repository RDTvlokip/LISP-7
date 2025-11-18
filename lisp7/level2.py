"""
LISP-7 Level 2: Extended Removal
Removes vowels and weak consonants (h, w, y).
"""


def compress(text):
    """
    Compress text using Level 2 (extended removal).

    Args:
        text: Input text to compress

    Returns:
        str: Compressed text with vowels and weak consonants removed
    """
    if not text:
        return ""

    result = []
    words = text.split()

    vowels = "aeiouyàâäéèêëïîôùûüÿæœ"
    weak_consonants = "hwy"

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

        compressed = ""
        for char in clean_word:
            if char in vowels:
                continue
            if char in weak_consonants:
                continue
            if not (compressed and compressed[-1] == char):
                compressed += char

        if not compressed:
            compressed = clean_word[0] if clean_word else ""

        if word[0].isupper():
            compressed = compressed.capitalize()

        result.append(compressed + punct)

    return " ".join(result)
