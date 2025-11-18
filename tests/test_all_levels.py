"""
LISP-7 Test Suite
Tests all compression levels and dictionary functionality.
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
    init_db,
    get_stats
)

# Test database
TEST_DB = "test_lisp7.db"


def test_level1():
    """Test Level 1: Vowel Removal"""
    text = "La technologie moderne"
    result = compress(text, level=1)
    print(f"Level 1: '{text}' -> '{result}'")
    assert len(result) < len(text), "Level 1 should reduce text length"
    return True


def test_level2():
    """Test Level 2: Extended Removal"""
    text = "La technologie moderne"
    result = compress(text, level=2)
    print(f"Level 2: '{text}' -> '{result}'")
    assert len(result) < len(text), "Level 2 should reduce text length"
    return True


def test_level3():
    """Test Level 3: Triadic Extraction"""
    text = "La technologie moderne"
    result = compress(text, level=3)
    print(f"Level 3: '{text}' -> '{result}'")
    # Each word should be max 3 chars
    words = result.split()
    for word in words:
        clean = word.strip(".,!?")
        assert len(clean) <= 3, f"Word '{clean}' should be max 3 chars"
    return True


def test_level4():
    """Test Level 4: Chaos Markers"""
    text = "La technologie moderne"
    result = compress(text, level=4)
    print(f"Level 4: '{text}' -> '{result}'")
    return True


def test_level5():
    """Test Level 5: Letter Permutation"""
    text = "La technologie moderne"
    result = compress(text, level=5)
    print(f"Level 5: '{text}' -> '{result}'")
    return True


def test_level6():
    """Test Level 6: Word Scrambling"""
    text = "La technologie moderne"
    result = compress(text, level=6)
    print(f"Level 6: '{text}' -> '{result}'")
    # Words should be scrambled
    return True


def test_level7():
    """Test Level 7: Alphabet Mutation"""
    text = "La technologie moderne"
    result, key = compress(text, level=7)
    print(f"Level 7: '{text}' -> '{result}'")
    print(f"  Key: '{key}'")
    assert len(key) == 26, "Alphabet key should be 26 characters"
    assert len(set(key)) == 26, "Alphabet key should have 26 unique characters"
    return True


def test_level7_uniqueness():
    """Test that Level 7 produces unique outputs for same input"""
    text = "La technologie moderne revolutionne notre societe"
    results = set()

    for i in range(5):
        result, key = compress(text, level=7)
        results.add(result)

    print(f"Level 7 Uniqueness: {len(results)}/5 unique compressions")
    assert len(results) == 5, "Each Level 7 compression should be unique"
    return True


def test_level7_reversal():
    """Test alphabet mutation reversal"""
    text = "test message"
    mutated, key = level7.mutate_alphabet(text)
    reversed_text = level7.reverse_mutation(mutated, key)

    print(f"Mutation: '{text}' -> '{mutated}' -> '{reversed_text}'")
    assert reversed_text == text, "Reversal should restore original text"
    return True


def test_compress_and_learn():
    """Test compression with dictionary learning"""
    # Clean up test database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    text = "La technologie moderne revolutionne notre societe"

    # Level 3
    compressed = compress_and_learn(text, level=3, db_file=TEST_DB)
    decompressed = decompress(compressed, db_file=TEST_DB)
    print(f"Learn L3: '{text[:30]}...' -> '{compressed}'")
    assert decompressed == text, "Decompression should match original"

    # Level 7
    compressed7 = compress_and_learn(text, level=7, db_file=TEST_DB)
    decompressed7 = decompress(compressed7, db_file=TEST_DB)
    print(f"Learn L7: '{text[:30]}...' -> '{compressed7}'")
    assert decompressed7 == text, "Level 7 decompression should match original"

    # Clean up
    os.remove(TEST_DB)
    return True


def test_key_verification():
    """Test that Level 7 requires correct key"""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    text = "La technologie moderne"

    # Compress and learn
    compressed = compress_and_learn(text, level=7, db_file=TEST_DB)

    # Get the correct key from database
    from lisp7.dictionary import lookup_sentence
    _, correct_key = lookup_sentence(compressed, TEST_DB)

    # Test with correct key
    success, result, error = decompress_with_key(compressed, correct_key, TEST_DB)
    print(f"Correct key: success={success}")
    assert success, "Should succeed with correct key"
    assert result == text, "Should return original text"

    # Test with wrong key
    wrong_key = "zyxwvutsrqponmlkjihgfedcba"
    success, result, error = decompress_with_key(compressed, wrong_key, TEST_DB)
    print(f"Wrong key: success={success}, error='{error}'")
    assert not success, "Should fail with wrong key"

    # Clean up
    os.remove(TEST_DB)
    return True


def test_stats():
    """Test dictionary statistics"""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    init_db(TEST_DB)
    stats = get_stats(TEST_DB)
    print(f"Stats: {stats}")
    assert 'words' in stats
    assert 'sentences' in stats
    assert 'level7_sentences' in stats

    # Clean up
    os.remove(TEST_DB)
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("LISP-7 TEST SUITE")
    print("=" * 60)

    tests = [
        ("Level 1", test_level1),
        ("Level 2", test_level2),
        ("Level 3", test_level3),
        ("Level 4", test_level4),
        ("Level 5", test_level5),
        ("Level 6", test_level6),
        ("Level 7", test_level7),
        ("Level 7 Uniqueness", test_level7_uniqueness),
        ("Level 7 Reversal", test_level7_reversal),
        ("Compress & Learn", test_compress_and_learn),
        ("Key Verification", test_key_verification),
        ("Statistics", test_stats),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            if test_func():
                print(f"[OK] {name}")
                passed += 1
            else:
                print(f"[FAIL] {name}")
                failed += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
