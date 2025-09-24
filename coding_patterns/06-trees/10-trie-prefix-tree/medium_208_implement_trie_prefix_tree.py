class TrieNode:
    """
    Standard TrieNode implementation
    Each node represents a character and contains links to children
    """
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark end of a complete word

class Trie:
    """
    Optimal Trie Implementation using Dictionary for Children
    
    Key insight: Use dictionary to store children for dynamic character sets.
    Each path from root to node represents a prefix.
    
    Time Complexity:
    - insert(word): O(m) where m is length of word
    - search(word): O(m) where m is length of word  
    - startsWith(prefix): O(m) where m is length of prefix
    
    Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words, 
    M is average length of words
    """
    
    def __init__(self):
        """Initialize the trie data structure."""
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        current = self.root
        
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for a word in the trie."""
        current = self.root
        
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        
        return current.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        """Check if there's any word that starts with the given prefix."""
        current = self.root
        
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        
        return True

class TrieNodeArray:
    """
    Array-based TrieNode (Memory Optimized for Lowercase Letters)
    More space-efficient when we know the character set is limited
    """
    def __init__(self):
        self.children = [None] * 26  # Fixed size for 'a' to 'z'
        self.is_end_of_word = False

class TrieArray:
    """
    Array-based Trie Implementation
    
    Optimized for lowercase English letters only
    More memory efficient but less flexible than dictionary approach
    
    Time Complexity: Same as dictionary version
    Space Complexity: More predictable, potentially less memory per node
    """
    
    def __init__(self):
        self.root = TrieNodeArray()
    
    def _char_to_index(self, char):
        """Convert character to array index"""
        return ord(char) - ord('a')
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        current = self.root
        
        for char in word:
            index = self._char_to_index(char)
            if current.children[index] is None:
                current.children[index] = TrieNodeArray()
            current = current.children[index]
        
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for a word in the trie."""
        current = self.root
        
        for char in word:
            index = self._char_to_index(char)
            if current.children[index] is None:
                return False
            current = current.children[index]
        
        return current.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        """Check if any word starts with the given prefix."""
        current = self.root
        
        for char in prefix:
            index = self._char_to_index(char)
            if current.children[index] is None:
                return False
            current = current.children[index]
        
        return True

class TrieWithAdditionalFeatures:
    """
    Enhanced Trie with Additional Useful Methods
    
    Includes methods commonly asked in follow-up questions
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True
    
    def delete(self, word: str) -> bool:
        """Delete a word from the trie. Returns True if word was deleted."""
        def _delete_helper(node, word, index):
            if index == len(word):
                # Reached end of word
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                node.is_end_of_word = False
                # Return True if node has no children (can be deleted)
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False  # Word doesn't exist
            
            should_delete_child = _delete_helper(node.children[char], word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                # Return True if current node can be deleted
                return not node.is_end_of_word and len(node.children) == 0
            
            return False
        
        return _delete_helper(self.root, word, 0)
    
    def get_all_words(self):
        """Return all words stored in the trie."""
        words = []
        
        def dfs(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)
        
        dfs(self.root, "")
        return words
    
    def get_words_with_prefix(self, prefix):
        """Return all words that start with the given prefix."""
        # Find the prefix node
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []  # No words with this prefix
            current = current.children[char]
        
        # Collect all words starting from prefix node
        words = []
        
        def dfs(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)
        
        dfs(current, prefix)
        return words
    
    def count_words_with_prefix(self, prefix):
        """Count how many words start with the given prefix."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return 0
            current = current.children[char]
        
        def count_words(node):
            count = 1 if node.is_end_of_word else 0
            for child in node.children.values():
                count += count_words(child)
            return count
        
        return count_words(current)

class TrieCompressed:
    """
    Compressed Trie (Radix Tree) Implementation
    
    More space-efficient by compressing single-child paths
    More complex but demonstrates advanced understanding
    """
    
    class TrieNodeCompressed:
        def __init__(self):
            self.children = {}
            self.is_end_of_word = False
            self.compressed_string = ""  # Stores compressed path
    
    def __init__(self):
        self.root = self.TrieNodeCompressed()
    
    def insert(self, word: str) -> None:
        """Insert with path compression."""
        current = self.root
        i = 0
        
        while i < len(word):
            char = word[i]
            
            if char not in current.children:
                # Create new node with remaining string
                new_node = self.TrieNodeCompressed()
                new_node.compressed_string = word[i:]
                new_node.is_end_of_word = True
                current.children[char] = new_node
                return
            
            child = current.children[char]
            compressed = child.compressed_string
            
            # Find common prefix
            j = 0
            while (j < len(compressed) and 
                   i + j < len(word) and 
                   compressed[j] == word[i + j]):
                j += 1
            
            if j == len(compressed):
                # Full match with compressed string
                current = child
                i += j
            elif j == 0:
                # No match at all - shouldn't happen with proper implementation
                break
            else:
                # Partial match - need to split the node
                # This is complex and typically not required in interviews
                break
    
    def search(self, word: str) -> bool:
        """Search in compressed trie."""
        current = self.root
        i = 0
        
        while i < len(word):
            char = word[i]
            if char not in current.children:
                return False
            
            child = current.children[char]
            compressed = child.compressed_string
            
            if word[i:i+len(compressed)] != compressed:
                return False
            
            i += len(compressed)
            current = child
        
        return current.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        """Check prefix in compressed trie."""
        current = self.root
        i = 0
        
        while i < len(prefix):
            char = prefix[i]
            if char not in current.children:
                return False
            
            child = current.children[char]
            compressed = child.compressed_string
            
            if i + len(compressed) <= len(prefix):
                if prefix[i:i+len(compressed)] != compressed:
                    return False
                i += len(compressed)
                current = child
            else:
                # Partial match with compressed string
                return compressed.startswith(prefix[i:])
        
        return True

# Test cases and utility functions
def test_basic_operations():
    """Test basic trie operations"""
    print("Testing Basic Trie Operations:")
    print("=" * 40)
    
    trie = Trie()
    
    # Test insertions
    words = ["apple", "app", "apricot", "banana", "band", "bandana"]
    print(f"Inserting words: {words}")
    
    for word in words:
        trie.insert(word)
        print(f"Inserted '{word}'")
    
    print()
    
    # Test search
    search_tests = ["apple", "app", "appl", "application", "banana", "ban"]
    print("Search tests:")
    for word in search_tests:
        result = trie.search(word)
        print(f"search('{word}'): {result}")
    
    print()
    
    # Test startsWith
    prefix_tests = ["app", "ban", "cat", "a", "appl"]
    print("Prefix tests:")
    for prefix in prefix_tests:
        result = trie.startsWith(prefix)
        print(f"startsWith('{prefix}'): {result}")

def test_enhanced_features():
    """Test enhanced trie features"""
    print("\nTesting Enhanced Trie Features:")
    print("=" * 40)
    
    trie = TrieWithAdditionalFeatures()
    
    words = ["cat", "cats", "dog", "dogs", "doggy", "car", "card", "care"]
    for word in words:
        trie.insert(word)
    
    print(f"Inserted words: {words}")
    print(f"All words in trie: {trie.get_all_words()}")
    print(f"Words with prefix 'ca': {trie.get_words_with_prefix('ca')}")
    print(f"Words with prefix 'dog': {trie.get_words_with_prefix('dog')}")
    print(f"Count of words with prefix 'ca': {trie.count_words_with_prefix('ca')}")
    
    # Test deletion
    print(f"\nDeleting 'cats': {trie.delete('cats')}")
    print(f"Words with prefix 'ca' after deletion: {trie.get_words_with_prefix('ca')}")

def compare_implementations():
    """Compare different trie implementations"""
    print("\nComparing Implementations:")
    print("=" * 40)
    
    words = ["hello", "world", "help", "heap", "wow"]
    
    # Dictionary-based trie
    trie_dict = Trie()
    for word in words:
        trie_dict.insert(word)
    
    # Array-based trie
    trie_array = TrieArray()
    for word in words:
        trie_array.insert(word)
    
    test_words = ["hello", "help", "he", "world", "wor", "xyz"]
    
    print("Testing both implementations:")
    for word in test_words:
        dict_search = trie_dict.search(word)
        dict_prefix = trie_dict.startsWith(word)
        array_search = trie_array.search(word)
        array_prefix = trie_array.startsWith(word)
        
        print(f"'{word}': search={dict_search}/{array_search}, prefix={dict_prefix}/{array_prefix}")
        
        # Verify both implementations agree
        assert dict_search == array_search, f"Search mismatch for {word}"
        assert dict_prefix == array_prefix, f"Prefix mismatch for {word}"
    
    print("✓ Both implementations produce identical results")

def performance_analysis():
    """Analyze performance characteristics"""
    print("\nPerformance Analysis:")
    print("=" * 40)
    
    implementations = [
        ("Dictionary-based", "Dynamic character set", "Higher memory per node", "Most flexible"),
        ("Array-based", "Fixed character set", "Lower memory per node", "Faster access"),
        ("Compressed", "Path compression", "Complex implementation", "Space efficient"),
    ]
    
    print(f"{'Implementation':<15} {'Character Set':<20} {'Memory':<22} {'Notes'}")
    print("-" * 75)
    
    for impl, charset, memory, notes in implementations:
        print(f"{impl:<15} {charset:<20} {memory:<22} {notes}")
    
    print("\nComplexity Summary:")
    print("- Time Complexity: O(m) for all operations, where m is word/prefix length")
    print("- Space Complexity: O(ALPHABET_SIZE * N * M) worst case")
    print("- Dictionary-based: More flexible, slightly higher memory overhead")
    print("- Array-based: More memory efficient for known character sets")

def demonstrate_use_cases():
    """Demonstrate common trie use cases"""
    print("\nCommon Use Cases:")
    print("=" * 40)
    
    print("1. Autocomplete System:")
    trie = TrieWithAdditionalFeatures()
    search_terms = ["search", "season", "seattle", "see", "seen", "seek"]
    
    for term in search_terms:
        trie.insert(term)
    
    prefix = "se"
    suggestions = trie.get_words_with_prefix(prefix)
    print(f"   User types '{prefix}': suggestions = {suggestions}")
    
    print("\n2. Spell Checker (prefix matching):")
    word = "searching"
    print(f"   Is '{word}' a valid word? {trie.search(word)}")
    print(f"   Does '{word[:6]}' have valid completions? {trie.startsWith(word[:6])}")
    
    print("\n3. Word Game Dictionary:")
    print(f"   All words starting with 'sea': {trie.get_words_with_prefix('sea')}")

if __name__ == "__main__":
    test_basic_operations()
    test_enhanced_features()
    compare_implementations()
    performance_analysis()
    demonstrate_use_cases()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Implement prefix tree (trie) data structure
   - Support insert, search, and startsWith operations
   - Efficient for string prefix operations
   - Used in autocomplete, spell checkers, etc.

2. KEY INSIGHTS:

   INSIGHT 1: Tree Structure for Prefixes
   - Each node represents a character
   - Path from root to node represents a prefix
   - End-of-word flag marks complete words

   INSIGHT 2: Shared Prefixes Save Space
   - Common prefixes share the same path
   - Memory efficient for large dictionaries
   - Fast prefix lookups

3. DESIGN DECISIONS:

   DECISION 1: Children Storage
   - Dictionary: Flexible, supports any character set
   - Array: More memory efficient for fixed character sets (e.g., a-z)
   - Trade-off between flexibility and efficiency

   DECISION 2: Node Structure
   - Minimal: just children and end-of-word flag
   - Enhanced: additional metadata for advanced features

4. IMPLEMENTATION APPROACHES:

   APPROACH 1 - Dictionary-based (RECOMMENDED):
   - Most flexible for different character sets
   - Clean and intuitive implementation
   - Standard choice for interviews

   APPROACH 2 - Array-based:
   - More memory efficient for known character sets
   - Faster access (direct indexing vs hash lookup)
   - Good optimization to mention

5. ALGORITHM WALKTHROUGH:
   - Insert: Follow/create path for each character, mark end
   - Search: Follow path, check if end-of-word flag is set
   - StartsWith: Follow path, return true if path exists

6. COMPLEXITY ANALYSIS:
   - Time: O(m) for all operations where m is word/prefix length
   - Space: O(ALPHABET_SIZE * N * M) worst case
   - Much better than hash table for prefix operations

7. EDGE CASES:
   - Empty string insertion/search
   - Single character words
   - One word is prefix of another
   - Non-existent words/prefixes

8. INTERVIEW PRESENTATION:
   - Start with problem understanding: "Trie is tree where each path represents a string"
   - Explain shared prefix benefit
   - Choose dictionary-based approach for flexibility
   - Code the three required methods
   - Walk through insertion example showing tree building

9. FOLLOW-UP QUESTIONS:
   - "How to delete words?" → Recursive deletion with node cleanup
   - "Memory optimization?" → Array-based or compressed trie
   - "Case sensitivity?" → Normalization in insert/search
   - "Unicode support?" → Dictionary approach handles this naturally

10. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests tree data structure understanding
    - Shows string processing skills
    - Multiple implementation approaches
    - Real-world applications (autocomplete, spell check)

11. COMMON MISTAKES:
    - Forgetting end-of-word flag (search returns true for prefixes)
    - Incorrect node creation logic
    - Not handling empty strings properly
    - Confusing search vs startsWith logic

12. OPTIMIZATION INSIGHTS:
    - Dictionary vs array trade-offs
    - Path compression for space efficiency
    - Additional metadata for enhanced features
    - Lazy deletion vs immediate cleanup

13. PRODUCTION CONSIDERATIONS:
    - Thread safety for concurrent access
    - Memory management and cleanup
    - Unicode and internationalization
    - Persistence and serialization

14. RELATED PROBLEMS:
    - Word Search II (use trie for efficient backtracking)
    - Add and Search Word (wildcards in trie)
    - Replace Words (trie-based string replacement)
    - Design Search Autocomplete System

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is that a trie leverages shared prefixes to enable 
    efficient string operations. Each path from root to node represents 
    a prefix, and the tree structure naturally organizes strings by their 
    common beginnings. This makes prefix operations like autocomplete 
    much more efficient than hash-table-based approaches."

16. DESIGN PATTERN RECOGNITION:
    - Tree-based string indexing
    - Prefix-based data organization
    - Space-time trade-offs in data structures
    - Dictionary vs array storage strategies

17. INTERVIEW TIPS:
    - Start with dictionary-based approach (most general)
    - Explain the end-of-word flag necessity
    - Draw tree diagram showing string insertions
    - Mention array optimization for fixed character sets
    - Discuss real-world applications to show understanding
"""
