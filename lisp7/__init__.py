"""
LISP-7: Linguistic Irreversible Scrambling Protocol
A new paradigm: Destructive Semantic Encoding (DSE)

Author: Theo Charlet (RDTvlokip)
"""

__version__ = "1.0.0"
__author__ = "Theo Charlet (RDTvlokip)"

from . import level1
from . import level2
from . import level3
from . import level4
from . import level5
from . import level6
from . import level7
from . import dictionary

from .dictionary import (
    init_db,
    learn_word,
    learn_sentence,
    lookup_sentence,
    lookup_word,
    get_stats
)

from .level7 import (
    mutate_alphabet,
    reverse_mutation
)


def compress(text, level=2):
    """
    Compress text using specified LISP-7 level.

    Args:
        text: Input text to compress
        level: Compression level (1-7)

    Returns:
        str: Compressed text (for levels 1-6)
        tuple: (compressed_text, alphabet_key) for level 7
    """
    if level == 1:
        return level1.compress(text)
    elif level == 2:
        return level2.compress(text)
    elif level == 3:
        return level3.compress(text)
    elif level == 4:
        return level4.compress(text)
    elif level == 5:
        return level5.compress(text)
    elif level == 6:
        return level6.compress(text)
    elif level == 7:
        return level7.compress(text)
    else:
        raise ValueError(f"Invalid level: {level}. Must be 1-7.")


def compress_and_learn(text, level=2, db_file=None):
    """
    Compress text and learn the mapping in the dictionary.

    Args:
        text: Input text to compress
        level: Compression level (1-7)
        db_file: Optional database file path

    Returns:
        str: Compressed text
    """
    if level == 7:
        compressed, alphabet_key = level7.compress(text)
        learn_sentence(text, compressed, alphabet_key, db_file)
    else:
        compressed = compress(text, level)
        learn_sentence(text, compressed, None, db_file)

    # Learn individual words
    words = text.split()
    compressed_words = compressed.split()

    for original_word, compressed_word in zip(words, compressed_words):
        clean_original = original_word.lower().strip(".,!?;:")
        clean_compressed = compressed_word.lower().strip(".,!?;:")
        if clean_original and clean_compressed:
            learn_word(clean_original, clean_compressed, db_file)

    return compressed


def decompress(compressed_text, db_file=None):
    """
    Decompress text using dictionary lookup.

    Args:
        compressed_text: Compressed text
        db_file: Optional database file path

    Returns:
        str: Decompressed text or None if not found
    """
    original, _ = lookup_sentence(compressed_text, db_file)
    return original


def decompress_with_key(compressed_text, alphabet_key, db_file=None):
    """
    Decompress Level 7 text with alphabet key verification.

    Args:
        compressed_text: Compressed text
        alphabet_key: Provided alphabet key
        db_file: Optional database file path

    Returns:
        tuple: (success, original_text, error_message)
    """
    original, stored_key = lookup_sentence(compressed_text, db_file)

    if original is None:
        return False, None, "Text not found in database"

    if stored_key:  # Level 7
        if alphabet_key == stored_key:
            return True, original, None
        else:
            return False, None, "Alphabet key does not match"
    else:
        # Not Level 7, return directly
        return True, original, None


# Convenience exports
__all__ = [
    # Main functions
    'compress',
    'compress_and_learn',
    'decompress',
    'decompress_with_key',

    # Level 7 specific
    'mutate_alphabet',
    'reverse_mutation',

    # Dictionary functions
    'init_db',
    'learn_word',
    'learn_sentence',
    'lookup_sentence',
    'lookup_word',
    'get_stats',

    # Level modules
    'level1',
    'level2',
    'level3',
    'level4',
    'level5',
    'level6',
    'level7',
    'dictionary',

    # Metadata
    '__version__',
    '__author__'
]
