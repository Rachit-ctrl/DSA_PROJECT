"""
Module: B3 - Dataset + Dictionary Data Layer
Interface: load_dictionary(), contains_word(), get_frequency(), get_all_words()
"""

import csv
from typing import Iterable


class Dictionary:
    def __init__(self, file_path: str = "data/unigram_freq.csv"):
        self.file_path = file_path
        self._vocab = {}
        self.is_loaded = False
        
        # Dataset stats required for project evaluation
        self.stats = {
            "total_lines_read": 0,
            "valid_words_loaded": 0,
            "duplicates_merged": 0,
            "invalid_tokens_skipped": 0,
            "min_frequency": 0,
            "max_frequency": 0
        }

    def load_dictionary(self) -> None:
        """Loads and cleans the dataset into memory once."""
        if self.is_loaded:
            return  # Do not read from disk if already loaded

        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header row

            for row in reader:
                self.stats["total_lines_read"] += 1
                if not row or len(row) < 2:
                    self.stats["invalid_tokens_skipped"] += 1
                    continue

                raw_word = row[0].strip().lower()
                raw_count = row[1].strip()

                # Clean: keep only letters (a-z)
                if not raw_word.isalpha():
                    self.stats["invalid_tokens_skipped"] += 1
                    continue

                # Safely parse count
                try:
                    count = int(raw_count)
                except ValueError:
                    self.stats["invalid_tokens_skipped"] += 1
                    continue

                # Store word; keep maximum count if duplicate appears
                if raw_word in self._vocab:
                    self.stats["duplicates_merged"] += 1
                    self._vocab[raw_word] = max(self._vocab[raw_word], count)
                else:
                    self._vocab[raw_word] = count

        self.is_loaded = True
        self.stats["valid_words_loaded"] = len(self._vocab)
        if self._vocab:
            self.stats["min_frequency"] = min(self._vocab.values())
            self.stats["max_frequency"] = max(self._vocab.values())

        print(f"[B3] Loaded {self.stats['valid_words_loaded']} words into memory.")

    # --- Agreed Public Interfaces for B2 & B4 ---

    def contains_word(self, word: str) -> bool:
        """Returns True if the word exists. Consumed by B4."""
        if not self.is_loaded:
            self.load_dictionary()
        return word.strip().lower() in self._vocab

    def get_frequency(self, word: str) -> int:
        """Returns the word frequency count, or 0. Consumed by B4."""
        if not self.is_loaded:
            self.load_dictionary()
        return self._vocab.get(word.strip().lower(), 0)

    def get_all_words(self) -> Iterable[str]:
        """Provides an iterable of all words. Consumed by B2."""
        if not self.is_loaded:
            self.load_dictionary()
        return self._vocab.keys()
    