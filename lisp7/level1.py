"""
LISP-7 Level 1: Vowel Removal
Removes all vowels except the first letter of each word.
"""


def compress(text):
    """
    Compress text using Level 1 (vowel removal).

    Args:
        text: Input text to compress

    Returns:
        str: Compressed text with vowels removed
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

        compressed = ""
        for i, char in enumerate(clean_word):
            if i == 0:
                compressed += char
            elif char not in "aeiouy":
                if not (compressed and compressed[-1] == char):
                    compressed += char

        if not compressed:
            compressed = clean_word[0] if clean_word else ""

        if word[0].isupper():
            compressed = compressed.capitalize()

        result.append(compressed + punct)

    return " ".join(result)
