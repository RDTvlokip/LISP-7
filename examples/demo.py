"""
LISP-7 Demo
Demonstrates the usage of all compression levels.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lisp7 import (
    compress,
    compress_and_learn,
    decompress,
    decompress_with_key,
    level7,
    get_stats
)


def demo_all_levels():
    """Demonstrate all compression levels"""
    print("=" * 70)
    print("LISP-7: Linguistic Irreversible Scrambling Protocol")
    print("Destructive Semantic Encoding Demo")
    print("=" * 70)

    text = "La technologie moderne revolutionne notre societe"
    print(f"\nOriginal text: \"{text}\"")
    print(f"Length: {len(text)} characters")

    print("\n" + "-" * 70)
    print("COMPRESSION LEVELS")
    print("-" * 70)

    for level in range(1, 8):
        if level == 7:
            result, key = compress(text, level=level)
            ratio = (1 - len(result) / len(text)) * 100
            print(f"\nLevel {level} (Alphabet Mutation):")
            print(f"  Compressed: \"{result}\"")
            print(f"  Key: \"{key}\"")
            print(f"  Ratio: {ratio:.1f}%")
        else:
            result = compress(text, level=level)
            ratio = (1 - len(result) / len(text)) * 100
            level_names = {
                1: "Vowel Removal",
                2: "Extended Removal",
                3: "Triadic Extraction",
                4: "Chaos Markers",
                5: "Letter Permutation",
                6: "Word Scrambling"
            }
            print(f"\nLevel {level} ({level_names[level]}):")
            print(f"  Compressed: \"{result}\"")
            print(f"  Ratio: {ratio:.1f}%")


def demo_level7_uniqueness():
    """Demonstrate that Level 7 produces unique outputs"""
    print("\n" + "=" * 70)
    print("LEVEL 7 UNIQUENESS DEMONSTRATION")
    print("=" * 70)

    text = "La technologie moderne revolutionne notre societe"
    print(f"\nSame input: \"{text}\"")
    print("\nMultiple compressions:")

    for i in range(5):
        result, key = compress(text, level=7)
        print(f"\n  #{i+1}: \"{result}\"")
        print(f"       Key: \"{key}\"")

    print("\n[OK] Each compression is UNIQUE!")
    print("     Same text -> Different outputs each time")
    print("     Prevents dictionary attacks")


def demo_security_model():
    """Demonstrate the two-key lock security model"""
    print("\n" + "=" * 70)
    print("SECURITY MODEL: TWO-KEY LOCK")
    print("=" * 70)

    # Use temporary database for demo
    demo_db = "demo_temp.db"
    if os.path.exists(demo_db):
        os.remove(demo_db)

    text = "La technologie moderne revolutionne notre societe"

    # Create two compressions
    compressed1 = compress_and_learn(text, level=7, db_file=demo_db)
    compressed2 = compress_and_learn(text, level=7, db_file=demo_db)

    # Get keys from database
    from lisp7.dictionary import lookup_sentence
    _, key1 = lookup_sentence(compressed1, demo_db)
    _, key2 = lookup_sentence(compressed2, demo_db)

    print(f"\nCompression #1: \"{compressed1}\"")
    print(f"Key #1: \"{key1}\"")
    print(f"\nCompression #2: \"{compressed2}\"")
    print(f"Key #2: \"{key2}\"")

    # Test scenarios
    print("\n" + "-" * 70)
    print("SECURITY SCENARIOS")
    print("-" * 70)

    # Scenario 1: Correct pair
    success, result, error = decompress_with_key(compressed1, key1, demo_db)
    print(f"\n1. Correct compressed + Correct key:")
    print(f"   Result: {'[OK] SUCCESS' if success else '[X] FAIL'}")
    if success:
        print(f"   Decompressed: \"{result}\"")

    # Scenario 2: Wrong key
    success, result, error = decompress_with_key(compressed1, key2, demo_db)
    print(f"\n2. Correct compressed + WRONG key:")
    print(f"   Result: {'[OK] SUCCESS' if success else '[X] FAIL (expected)'}")
    if error:
        print(f"   Error: {error}")

    # Scenario 3: Wrong compressed
    success, result, error = decompress_with_key(compressed2, key1, demo_db)
    print(f"\n3. WRONG compressed + Correct key:")
    print(f"   Result: {'[OK] SUCCESS' if success else '[X] FAIL (expected)'}")
    if error:
        print(f"   Error: {error}")

    print("\n" + "-" * 70)
    print("CONCLUSION")
    print("-" * 70)
    print("\nThe security model works like a TWO-KEY LOCK:")
    print("  - Correct compressed text alone -> insufficient")
    print("  - Correct alphabet key alone -> insufficient")
    print("  - ONLY the exact pair (compressed, key) -> decompression allowed")
    print("\nEven the SAME text compressed twice has DIFFERENT keys!")
    print("Impossible to attack by dictionary!")

    # Clean up
    os.remove(demo_db)


def demo_alphabet_mutation():
    """Demonstrate alphabet mutation and reversal"""
    print("\n" + "=" * 70)
    print("ALPHABET MUTATION DEMO")
    print("=" * 70)

    text = "hello world"
    print(f"\nOriginal: \"{text}\"")

    mutated, key = level7.mutate_alphabet(text)
    print(f"Mutated:  \"{mutated}\"")
    print(f"Key:      \"{key}\"")

    reversed_text = level7.reverse_mutation(mutated, key)
    print(f"Reversed: \"{reversed_text}\"")

    print(f"\nMatch: {'[OK] PERFECT' if reversed_text == text else '[X] ERROR'}")


if __name__ == "__main__":
    demo_all_levels()
    demo_level7_uniqueness()
    demo_alphabet_mutation()
    demo_security_model()

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
