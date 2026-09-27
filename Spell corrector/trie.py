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