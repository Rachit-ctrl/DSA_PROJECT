
import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Spell corrector")
    )
)

from trie import Trie


class TestCandidateGeneration(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        words = ["apple", "apply", "ample", "maple", "banana"]

        for word in words:
            self.trie.insert(word)

    def test_candidates_within_distance(self):
        candidates = self.trie.generate_candidates("aple", 1)

        self.assertEqual(
            candidates,
            [("ample", 1), ("apple", 1), ("maple", 1)]
        )

    def test_exact_match(self):
        candidates = self.trie.generate_candidates("apple", 0)

        self.assertEqual(candidates, [("apple", 0)])

    def test_no_candidates_at_zero_distance(self):
        candidates = self.trie.generate_candidates("aple", 0)

        self.assertEqual(candidates, [])

    def test_results_sorted_by_distance(self):
        candidates = self.trie.generate_candidates("aple", 2)
        distances = [distance for word, distance in candidates]

        self.assertEqual(distances, sorted(distances))

    def test_empty_trie(self):
        empty_trie = Trie()

        self.assertEqual(empty_trie.generate_candidates("hello", 2), [])

    def test_negative_distance_rejected(self):
        with self.assertRaises(ValueError):
            self.trie.generate_candidates("aple", -1)


if __name__ == "__main__":
    unittest.main()
