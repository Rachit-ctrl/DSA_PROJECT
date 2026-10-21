from edit_distance import levenshtein_distance

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

        # Store the best 10 suggestions for this prefix
        self.top_suggestions = []


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word, frequency=0):
        current = self.root

        for char in word.lower():
            if char not in current.children:
                current.children[char] = TrieNode()

            current = current.children[char]

        if not current.is_end_of_word:
            self.word_count += 1

        current.is_end_of_word = True
        current.frequency = frequency

    def search(self, word):
        current = self.root

        for char in word.lower():
            if char not in current.children:
                return False

            current = current.children[char]

        return current.is_end_of_word

    def starts_with(self, prefix):
        current = self.root

        for char in prefix.lower():
            if char not in current.children:
                return False

            current = current.children[char]

        return True

    def _collect_words(self, node, current_word, results):
        if node.is_end_of_word:
            results.append((current_word, node.frequency))

        for char, child in node.children.items():
            self._collect_words(
                child,
                current_word + char,
                results
            )

    def autocomplete(self, prefix, limit=10):
        current = self.root

        for char in prefix.lower():
            if char not in current.children:
                return []

            current = current.children[char]

        # Use precomputed suggestions when available
        if current.top_suggestions:
            return [
                word
                for word, frequency in current.top_suggestions[:limit]
            ]

        # Fallback for a Trie built using insert()
        results = []

        self._collect_words(
            current,
            prefix.lower(),
            results
        )

        results.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return [
            word
            for word, frequency in results[:limit]
        ]

    def build_from_dictionary(self, dictionary):
        """
        Builds the Trie using B3's Dictionary interface.
        Uses precomputed Top-10 suggestions for fast autocomplete.
        """

        for word in dictionary.get_all_words():
            frequency = dictionary.get_frequency(word)

            current = self.root

            for char in word.lower():

                if char not in current.children:
                    current.children[char] = TrieNode()

                current = current.children[char]

                # Add this word to the prefix's Top-10 candidates
                current.top_suggestions.append(
                    (word, frequency)
                )

                current.top_suggestions.sort(
                    key=lambda item: item[1],
                    reverse=True
                )

                if len(current.top_suggestions) > 10:
                    current.top_suggestions.pop()

            if not current.is_end_of_word:
                self.word_count += 1

            current.is_end_of_word = True
            current.frequency = frequency

    def count_words_with_prefix(self, prefix):
        current = self.root

        for char in prefix.lower():
            if char not in current.children:
                return 0

            current = current.children[char]

        results = []

        self._collect_words(
            current,
            prefix.lower(),
            results
        )

        return len(results)

    def get_trie_statistics(self):
        node_count = 0
        suggestion_entries = 0

        stack = [self.root]

        while stack:
            node = stack.pop()

            node_count += 1
            suggestion_entries += len(node.top_suggestions)

            for child in node.children.values():
                stack.append(child)

        return node_count, suggestion_entries

    
    def generate_candidates(self, query, max_distance=2):
        """
        Generate words within max_distance using Trie-based
        Levenshtein search with branch pruning.

        Returns:
            List of (word, edit_distance) tuples, sorted by
            distance and then alphabetically.
        """
        query = query.lower()

        if max_distance < 0:
            raise ValueError("max_distance must be non-negative")

        candidates = []
        query_length = len(query)

        # Initial DP row: distance from empty word to query prefixes.
        initial_row = list(range(query_length + 1))

        def search(node, current_word, previous_row):
            # Record a complete word if its distance is acceptable.
            if node.is_end_of_word:
                distance = previous_row[query_length]
                if distance <= max_distance:
                    candidates.append((current_word, distance))

            # Explore each child while updating the DP row.
            for char, child_node in node.children.items():
                current_row = [previous_row[0] + 1]

                for column in range(1, query_length + 1):
                    insert_cost = current_row[column - 1] + 1
                    delete_cost = previous_row[column] + 1
                    replace_cost = previous_row[column - 1] + (
                        0 if query[column - 1] == char else 1
                    )

                    current_row.append(
                        min(insert_cost, delete_cost, replace_cost)
                    )

                # If no prefix can be within the limit, prune this branch.
                if min(current_row) <= max_distance:
                    search(
                        child_node,
                        current_word + char,
                        current_row
                    )

        search(self.root, "", initial_row)

        candidates.sort(key=lambda item: (item[1], item[0]))
        return candidates
