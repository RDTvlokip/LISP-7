"""
LISP-7 Level 4: Chaos Markers
Triadic extraction with deterministic scrambling and noise insertion.
"""

import hashlib
import random


def _scramble(word, original_word):
    """Apply chaos scrambling to a word."""
    if len(word) <= 2:
        return word

    word_hash = int(hashlib.md5(original_word.encode()).hexdigest(), 16)
    rng = random.Random(word_hash)

    first = word[0]
    last = word[-1]
    middle = list(word[1:-1])

    if len(middle) > 0:
        rng.shuffle(middle)

    scrambled = first + ''.join(middle) + last

    noise_chars = "bcdfghjklmnpqrstvwxz"
    rand_val = word_hash % 100

    if rand_val < 20 and len(scrambled) > 1:
        insert_pos = rng.randint(1, len(scrambled) - 1)
        noise_char = rng.choice(noise_chars)
        scrambled = scrambled[:insert_pos] + noise_char + scrambled[insert_pos:]
    elif rand_val >= 20 and rand_val < 35 and len(scrambled) > 3:
        remove_pos = rng.randint(1, len(scrambled) - 2)
        scrambled = scrambled[:remove_pos] + scrambled[remove_pos + 1:]

    return scrambled


def compress(text):
    """
    Compress text using Level 4 (chaos markers).

    Args:
        text: Input text to compress

    Returns:
        str: Compressed text with chaos scrambling
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
            compressed = _scramble(level3_compressed, clean_word)

        if not compressed:
            compressed = clean_word[0] if clean_word else ""

        if word[0].isupper():
            compressed = compressed.capitalize()

        result.append(compressed + punct)

    return " ".join(result)
