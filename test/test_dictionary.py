import os
import sys
sys.path.append("Spell corrector")

from dictionary import Dictionary


def test_b3():
    print("--- STARTING VERIFICATION AUDIT ---")

    # Locate dataset path
    data_path = "data/unigram_freq.csv" if os.path.exists("data/unigram_freq.csv") else "unigram_freq.csv"
    d = Dictionary(data_path)
    d.load_dictionary()

    # 1. Exact lookup & case insensitivity
    assert d.contains_word("apple") is True
    assert d.contains_word("APPLE") is True
    assert d.contains_word("notarealwordxyz") is False

    # 2. Frequency lookups
    assert d.get_frequency("apple") > 0
    assert d.get_frequency("notarealwordxyz") == 0

    # 3. Preservation of edge-case words ("null", "nan")
    assert d.contains_word("null") is True
    assert d.contains_word("nan") is True

    # 4. Iterable interface for B2
    words = list(d.get_all_words())
    assert len(words) > 300000

    print("--- ALL TESTS PASSED SUCCESSFULLY ---")
    print("Dataset Stats:", d.stats)


if __name__ == "__main__":
    test_b3()
