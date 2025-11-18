"""
LISP-7 Dictionary Management
Handles database operations for word and sentence storage.
"""

import sqlite3
import os

DB_FILE = "data.db"


def get_db_connection(db_file=None):
    """Get a database connection."""
    conn = sqlite3.connect(db_file or DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_file=None):
    """Initialize the database with required tables."""
    db_path = db_file or DB_FILE

    if not os.path.exists(db_path):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_dict (
                compressed TEXT PRIMARY KEY,
                original TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentence_dict (
                compressed TEXT PRIMARY KEY,
                original TEXT,
                alphabet_key TEXT
            )
        ''')

        conn.commit()
        conn.close()
    else:
        # Migration: Add alphabet_key column if it doesn't exist
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(sentence_dict)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'alphabet_key' not in columns:
            cursor.execute("ALTER TABLE sentence_dict ADD COLUMN alphabet_key TEXT")
            conn.commit()

        conn.close()


def learn_word(original, compressed, db_file=None):
    """
    Learn a word mapping (compressed -> original).

    Args:
        original: Original word
        compressed: Compressed word
        db_file: Optional database file path

    Returns:
        bool: True if learned, False if already exists
    """
    if not original or not compressed:
        return False

    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    compressed_lower = compressed.lower()
    original_lower = original.lower()

    cursor.execute("SELECT 1 FROM word_dict WHERE compressed = ?", (compressed_lower,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(
            "INSERT OR REPLACE INTO word_dict (compressed, original) VALUES (?, ?)",
            (compressed_lower, original_lower)
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def learn_sentence(original, compressed, alphabet_key=None, db_file=None):
    """
    Learn a sentence mapping (compressed -> original).

    Args:
        original: Original sentence
        compressed: Compressed sentence
        alphabet_key: Optional alphabet key for Level 7
        db_file: Optional database file path

    Returns:
        bool: True if learned, False if already exists
    """
    if not original or not compressed:
        return False

    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sentence_dict WHERE compressed = ?", (compressed,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(
            "INSERT OR REPLACE INTO sentence_dict (compressed, original, alphabet_key) VALUES (?, ?, ?)",
            (compressed, original, alphabet_key)
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def lookup_sentence(compressed, db_file=None):
    """
    Look up a sentence by its compressed form.

    Args:
        compressed: Compressed sentence
        db_file: Optional database file path

    Returns:
        tuple: (original, alphabet_key) or (None, None) if not found
    """
    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original, alphabet_key FROM sentence_dict WHERE compressed = ?",
        (compressed,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return row['original'], row['alphabet_key']
    return None, None


def lookup_word(compressed, db_file=None):
    """
    Look up a word by its compressed form.

    Args:
        compressed: Compressed word
        db_file: Optional database file path

    Returns:
        str: Original word or None if not found
    """
    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original FROM word_dict WHERE compressed = ?",
        (compressed.lower(),)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return row['original']
    return None


def get_stats(db_file=None):
    """
    Get dictionary statistics.

    Returns:
        dict: Statistics about the dictionary
    """
    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM word_dict")
    word_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sentence_dict")
    sentence_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sentence_dict WHERE alphabet_key IS NOT NULL")
    level7_count = cursor.fetchone()[0]

    conn.close()

    return {
        'words': word_count,
        'sentences': sentence_count,
        'level7_sentences': level7_count
    }
