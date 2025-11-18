"""
LISP-7 Level 7: Alphabet Mutation
Maximum security with truly random alphabet substitution.
Each compression generates a unique 26-character permutation key.
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


def mutate_alphabet(text, alphabet_key=None):
    """
    Mutate text using alphabet substitution.

    Args:
        text: Text to mutate
        alphabet_key: Optional pre-defined alphabet permutation (26 chars).
                     If None, generates a truly random one.

    Returns:
        tuple: (mutated_text, alphabet_key_used)
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    if alphabet_key is None:
        # TRULY RANDOM - different each time!
        shuffled_alphabet = list(alphabet)
        random.shuffle(shuffled_alphabet)
        alphabet_key = ''.join(shuffled_alphabet)
    else:
        shuffled_alphabet = list(alphabet_key)

    mutation_map = dict(zip(alphabet, shuffled_alphabet))

    result = []
    for char in text:
        if char.lower() in mutation_map:
            mutated = mutation_map[char.lower()]
            if char.isupper():
                mutated = mutated.upper()
            result.append(mutated)
        else:
            result.append(char)

    return ''.join(result), alphabet_key


def reverse_mutation(mutated_text, alphabet_key):
    """
    Reverse alphabet mutation using the stored key.

    Args:
        mutated_text: Text with mutated alphabet
        alphabet_key: The alphabet permutation used (26 chars)

    Returns:
        str: Original text with alphabet restored
    """
    if not alphabet_key or len(alphabet_key) != 26:
        return mutated_text

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    reverse_map = dict(zip(alphabet_key, alphabet))

    result = []
    for char in mutated_text:
        if char.lower() in reverse_map:
            original = reverse_map[char.lower()]
            if char.isupper():
                original = original.upper()
            result.append(original)
        else:
            result.append(char)

    return ''.join(result)


def compress(text, alphabet_key=None):
    """
    Compress text using Level 7 (alphabet mutation).

    Args:
        text: Input text to compress
        alphabet_key: Optional pre-defined key (for testing)

    Returns:
        tuple: (compressed_text, alphabet_key)
    """
    if not text:
        return "", None

    words = text.split()
    compressed_words = []

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

        compressed_words.append(compressed + punct)

    # Shuffle word order deterministically
    text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
    rng = random.Random(text_hash)
    rng.shuffle(compressed_words)

    level6_result = " ".join(compressed_words)

    # Apply truly random alphabet mutation
    mutated_text, key = mutate_alphabet(level6_result, alphabet_key)

    return mutated_text, key
