"""
LISP-7 Level 5: Letter Permutation
Triadic extraction with deterministic letter shuffling.
"""

import hashlib
import random


def _shuffle_letters(word, original_word):
    """Shuffle letters deterministically based on word hash."""
    if len(word) <= 1:
        return word

    word_hash = int(hashlib.md5(original_word.encode()).hexdigest(), 16)
    rng = random.Random(word_hash)

    letters = list(word)
    rng.shuffle(letters)

    return ''.join(letters)


def compress(text):
    """
    Compress text using Level 5 (letter permutation).

    Args:
        text: Input text to compress

    Returns:
        str: Compressed text with letter permutation
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
            level3_compressed = first + middle + last
            compressed = _shuffle_letters(level3_compressed, clean_word)

        if not compressed:
            compressed = clean_word[0] if clean_word else ""

        if word[0].isupper():
            compressed = compressed.capitalize()

        result.append(compressed + punct)

    return " ".join(result)
