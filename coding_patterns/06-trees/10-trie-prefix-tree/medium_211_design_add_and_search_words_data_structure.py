class TrieNode:
    """
    TrieNode for wildcard-enabled word search
    Standard trie node with children dictionary and end-of-word marker
    """
    def __init__(self):
        self.children = {}  # Dictionary mapping char -> TrieNode
        self.is_end_of_word = False  # Marks complete words

class WordDictionary:
    """
    Optimal Solution - Trie with Backtracking for Wildcard Search
    
    Key insight: Use trie for efficient prefix matching, add backtracking 
    for wildcard '.' character that can match any single character.
    
    Time Complexity:
    - addWord(word): O(m) where m is length of word
    - search(word): O(n) worst case where n is total nodes (for "...")
                    O(m) best case for no wildcards
    
    Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words
    """
    
    def __init__(self):
        """Initialize the data structure."""
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """Add a word to the data structure."""
        current = self.root
        
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """
        Search for a word. Word may contain '.' as wildcard for any letter.
        """
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        """
        Recursive helper for wildcard search with backtracking
        
        Args:
            word: search string (may contain '.')
            index: current position in word
            node: current trie node
        
        Returns:
            True if word can be found starting from current node/index
        """
        # Base case: reached end of word
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            # Wildcard: try all possible children
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            # Regular character: exact match required
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])

class WordDictionaryIterative:
    """
    Iterative Solution using Stack (Alternative Approach)
    
    Uses explicit stack to simulate recursion for wildcard handling
    More complex but avoids recursion stack limitations
    
    Time Complexity: Same as recursive version
    Space Complexity: O(h) for stack where h is word length
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """Add word using standard trie insertion"""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Iterative search with explicit stack for backtracking"""
        # Stack contains (node, word_index) pairs
        stack = [(self.root, 0)]
        
        while stack:
            node, index = stack.pop()
            
            # Reached end of word
            if index == len(word):
                if node.is_end_of_word:
                    return True
                continue
            
            char = word[index]
            
            if char == '.':
                # Add all children to stack
                for child_node in node.children.values():
                    stack.append((child_node, index + 1))
            else:
                # Add specific child if exists
                if char in node.children:
                    stack.append((node.children[char], index + 1))
        
        return False

class WordDictionaryOptimized:
    """
    Memory-Optimized Version with Array-based Nodes
    
    Uses arrays for children when character set is known (e.g., lowercase a-z)
    More memory efficient but less flexible
    
    Time Complexity: Same as dictionary version
    Space Complexity: More predictable per-node memory usage
    """
    
    class TrieNodeArray:
        def __init__(self):
            self.children = [None] * 26  # for 'a' to 'z'
            self.is_end_of_word = False
    
    def __init__(self):
        self.root = self.TrieNodeArray()
    
    def _char_to_index(self, char):
        """Convert character to array index"""
        return ord(char) - ord('a')
    
    def addWord(self, word: str) -> None:
        """Add word using array-based trie"""
        current = self.root
        for char in word:
            index = self._char_to_index(char)
            if current.children[index] is None:
                current.children[index] = self.TrieNodeArray()
            current = current.children[index]
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search with array-based backtracking"""
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word: str, index: int, node) -> bool:
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            # Try all non-null children
            for child_node in node.children:
                if child_node is not None:
                    if self._search_helper(word, index + 1, child_node):
                        return True
            return False
        else:
            char_index = self._char_to_index(char)
            if node.children[char_index] is None:
                return False
            return self._search_helper(word, index + 1, node.children[char_index])

class WordDictionaryWithStats:
    """
    Enhanced Version with Statistics and Additional Features
    
    Includes methods for debugging and performance analysis
    """
    
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
        self.search_count = 0
    
    def addWord(self, word: str) -> None:
        """Add word and update statistics"""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        if not current.is_end_of_word:
            current.is_end_of_word = True
            self.word_count += 1
    
    def search(self, word: str) -> bool:
        """Search with statistics tracking"""
        self.search_count += 1
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])
    
    def get_all_words(self):
        """Return all words in the dictionary"""
        words = []
        
        def dfs(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)
        
        dfs(self.root, "")
        return sorted(words)
    
    def get_words_matching_pattern(self, pattern):
        """Get all words matching a pattern with wildcards"""
        words = []
        
        def find_matches(node, pattern_index, current_word):
            if pattern_index == len(pattern):
                if node.is_end_of_word:
                    words.append(current_word)
                return
            
            char = pattern[pattern_index]
            
            if char == '.':
                for next_char, child_node in node.children.items():
                    find_matches(child_node, pattern_index + 1, 
                               current_word + next_char)
            else:
                if char in node.children:
                    find_matches(node.children[char], pattern_index + 1,
                               current_word + char)
        
        find_matches(self.root, 0, "")
        return sorted(words)
    
    def get_statistics(self):
        """Return dictionary statistics"""
        return {
            'word_count': self.word_count,
            'search_count': self.search_count,
            'avg_searches_per_word': self.search_count / max(1, self.word_count)
        }

class WordDictionaryLengthIndexed:
    """
    Length-Indexed Optimization for Better Performance
    
    Groups words by length to reduce search space for wildcards
    Significant performance improvement for queries with many wildcards
    """
    
    def __init__(self):
        self.tries_by_length = {}  # length -> trie root
    
    def addWord(self, word: str) -> None:
        """Add word to length-specific trie"""
        length = len(word)
        
        if length not in self.tries_by_length:
            self.tries_by_length[length] = TrieNode()
        
        current = self.tries_by_length[length]
        
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        current.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search only in trie of matching length"""
        length = len(word)
        
        if length not in self.tries_by_length:
            return False
        
        return self._search_helper(word, 0, self.tries_by_length[length])
    
    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])

# Test cases and utility functions
def test_basic_functionality():
    """Test basic add and search operations"""
    print("Testing Basic Functionality:")
    print("=" * 40)
    
    wd = WordDictionary()
    
    # Add words
    words = ["bad", "dad", "mad"]
    for word in words:
        wd.addWord(word)
        print(f"Added '{word}'")
    
    print()
    
    # Test searches
    search_tests = [
        ("pad", False),    # doesn't exist
        ("bad", True),     # exact match
        (".ad", True),     # wildcard matches 'b', 'd', 'm'
        ("b..", True),     # wildcard matches "bad"
        ("...", True),     # all wildcards, should match any 3-letter word
        ("....", False),   # no 4-letter words
        ("b.d", True),     # should match "bad"
        ("..d", True),     # should match "bad", "dad", "mad"
    ]
    
    print("Search tests:")
    for query, expected in search_tests:
        result = wd.search(query)
        status = "✓" if result == expected else "✗"
        print(f"search('{query}'): {result} {status} (expected {expected})")

def test_edge_cases():
    """Test edge cases and corner scenarios"""
    print("\nTesting Edge Cases:")
    print("=" * 40)
    
    wd = WordDictionary()
    
    # Edge case 1: Single character words
    wd.addWord("a")
    print("Added single char 'a'")
    print(f"search('a'): {wd.search('a')}")
    print(f"search('.'): {wd.search('.')}")
    
    # Edge case 2: Empty search (if allowed)
    # Note: Problem typically guarantees non-empty words
    
    # Edge case 3: All wildcards
    wd.addWord("test")
    print(f"search('....'): {wd.search('....')}")  # Should match "test"
    
    # Edge case 4: Mixed wildcards and regular chars
    wd.addWord("hello")
    print(f"search('h.ll.'): {wd.search('h.ll.')}")  # Should match "hello"
    print(f"search('h.llo'): {wd.search('h.llo')}")  # Should match "hello"

def test_performance_scenarios():
    """Test different performance scenarios"""
    print("\nTesting Performance Scenarios:")
    print("=" * 40)
    
    # Scenario 1: Many words with common prefixes
    wd1 = WordDictionary()
    prefixes = ["test", "testing", "tester", "tests", "testament"]
    for word in prefixes:
        wd1.addWord(word)
    
    print("Scenario 1: Common prefixes")
    print(f"search('test'): {wd1.search('test')}")
    print(f"search('test.'): {wd1.search('test.')}")  # Should match "tests"
    print(f"search('test...'): {wd1.search('test...')}")  # Should match "testing", "tester"
    
    # Scenario 2: Length-based optimization
    wd2 = WordDictionaryLengthIndexed()
    for word in prefixes:
        wd2.addWord(word)
    
    print("\nScenario 2: Length-indexed optimization")
    print(f"search('test'): {wd2.search('test')}")
    print(f"search('.....'): {wd2.search('.....')}")  # 5-letter words only

def compare_implementations():
    """Compare different implementation approaches"""
    print("\nComparing Implementations:")
    print("=" * 40)
    
    words = ["word", "world", "work", "wow", "wonder"]
    implementations = [
        ("Standard Recursive", WordDictionary),
        ("Iterative Stack", WordDictionaryIterative),
        ("Array Optimized", WordDictionaryOptimized),
        ("Length Indexed", WordDictionaryLengthIndexed),
    ]
    
    test_queries = ["word", "w..d", "wo..", "...."]
    
    print("Adding words:", words)
    print()
    
    results = {}
    for name, impl_class in implementations:
        wd = impl_class()
        for word in words:
            wd.addWord(word)
        
        print(f"{name}:")
        for query in test_queries:
            result = wd.search(query)
            print(f"  search('{query}'): {result}")
            
            # Store for consistency checking
            if query not in results:
                results[query] = result
            else:
                assert results[query] == result, f"Inconsistent result for {query}"
        print()
    
    print("✓ All implementations produce consistent results")

def analyze_complexity():
    """Analyze time and space complexity"""
    print("\nComplexity Analysis:")
    print("=" * 40)
    
    scenarios = [
        ("addWord", "O(m)", "m = word length", "Standard trie insertion"),
        ("search (no wildcards)", "O(m)", "m = word length", "Direct path traversal"),
        ("search (all wildcards)", "O(n)", "n = total nodes", "Must explore all paths"),
        ("search (mixed)", "O(k^w * m)", "k=alphabet size, w=wildcards", "Exponential in wildcards"),
    ]
    
    print(f"{'Operation':<20} {'Time':<12} {'Parameters':<20} {'Description'}")
    print("-" * 70)
    
    for operation, time_complexity, params, description in scenarios:
        print(f"{operation:<20} {time_complexity:<12} {params:<20} {description}")
    
    print("\nSpace Complexity: O(ALPHABET_SIZE * N * M)")
    print("Where N = number of words, M = average word length")
    
    print("\nOptimization Strategies:")
    print("1. Length indexing: Reduces search space significantly")
    print("2. Array-based nodes: Better memory efficiency for known alphabets")
    print("3. Early termination: Stop search as soon as match found")

def demonstrate_real_world_usage():
    """Demonstrate real-world applications"""
    print("\nReal-world Applications:")
    print("=" * 40)
    
    # Application 1: Pattern matching in text processing
    print("1. Pattern Matching in Text Processing:")
    wd = WordDictionaryWithStats()
    
    text_words = ["the", "quick", "brown", "fox", "jumps"]
    for word in text_words:
        wd.addWord(word)
    
    patterns = ["t.e", "qu..k", "....n"]
    for pattern in patterns:
        matches = wd.get_words_matching_pattern(pattern)
        print(f"   Pattern '{pattern}' matches: {matches}")
    
    # Application 2: Spell checking with wildcards
    print("\n2. Spell Checking with Wildcards:")
    dictionary = ["hello", "world", "help", "held", "hero"]
    wd2 = WordDictionary()
    
    for word in dictionary:
        wd2.addWord(word)
    
    user_input = "h.l."  # User typed with some uncertainty
    found = wd2.search(user_input)
    print(f"   User typed '{user_input}': {'Found matches' if found else 'No matches'}")

if __name__ == "__main__":
    test_basic_functionality()
    test_edge_cases()
    test_performance_scenarios()
    compare_implementations()
    analyze_complexity()
    demonstrate_real_world_usage()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Design data structure supporting addWord and search operations
   - search() must handle '.' wildcard matching any single character
   - Build on standard Trie but add backtracking for wildcards
   - Must be efficient for both exact matches and wildcard searches

2. KEY INSIGHTS:

   INSIGHT 1: Trie + Backtracking
   - Standard trie handles exact character matching
   - Backtracking handles wildcard exploration
   - Combine both approaches in recursive search

   INSIGHT 2: Wildcard Complexity
   - No wildcards: O(m) search time (m = word length)
   - All wildcards: O(n) search time (n = total nodes)
   - Mixed wildcards: exponential in number of wildcards

3. ALGORITHM STRATEGY:
   - addWord: Standard trie insertion
   - search: Recursive function with two cases:
     * Regular char: follow specific child
     * Wildcard '.': try all possible children

4. WHY BACKTRACKING IS NECESSARY:
   - Wildcard '.' can match any character
   - Must explore all possible paths at wildcard positions
   - Return true if ANY path leads to valid word

5. IMPLEMENTATION APPROACHES:

   APPROACH 1 - Recursive Backtracking (RECOMMENDED):
   - Clean and intuitive recursive structure
   - Natural handling of wildcards
   - Easy to understand and implement

   APPROACH 2 - Iterative with Stack:
   - Avoids recursion depth limitations
   - More complex state management
   - Good alternative if recursion discouraged

6. COMPLEXITY ANALYSIS:
   - addWord: O(m) where m is word length
   - search: O(m) best case, O(n) worst case (all wildcards)
   - Space: O(ALPHABET_SIZE * N * M) for trie storage

7. OPTIMIZATION OPPORTUNITIES:
   - Length indexing: separate tries by word length
   - Array-based nodes: memory efficiency for known alphabets
   - Early termination: return as soon as match found

8. EDGE CASES:
   - All wildcards: "..." matches any word of that length
   - Single character: both '.' and regular chars
   - Mixed patterns: "a.c" style searches
   - No matches: wildcard patterns with no valid completions

9. INTERVIEW PRESENTATION:
   - Start with: "I'll extend a trie to handle wildcards using backtracking"
   - Explain the two-case search logic clearly
   - Code the recursive solution
   - Walk through example with wildcards
   - Discuss complexity implications of wildcards

10. FOLLOW-UP QUESTIONS:
    - "How to optimize for many wildcards?" → Length indexing, pruning
    - "Memory optimization?" → Array-based nodes
    - "Multiple wildcards?" → Explain exponential complexity
    - "Real-world applications?" → Pattern matching, spell checking

11. WHY THIS PROBLEM IS CHALLENGING:
    - Combines trie data structure with backtracking algorithm
    - Tests understanding of wildcard complexity
    - Requires careful handling of recursion termination
    - Real-world relevance (pattern matching, search engines)

12. COMMON MISTAKES:
    - Not implementing proper backtracking for wildcards
    - Forgetting end-of-word check (accepting prefixes as matches)
    - Inefficient wildcard handling (not pruning impossible paths)
    - Not considering complexity implications of wildcard patterns

13. IMPLEMENTATION DETAILS:
    - Recursive helper function with node and index parameters
    - Base case: reached end of word, check end-of-word flag
    - Wildcard case: try all children recursively
    - Regular case: follow specific child if exists

14. PERFORMANCE CONSIDERATIONS:
    - Wildcard searches can be exponential in worst case
    - Length-based optimization significantly helps
    - Consider limiting wildcard patterns in production
    - Memory usage grows with vocabulary size

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is combining trie efficiency for exact matches with 
    backtracking for wildcard exploration. When encountering '.', I must 
    explore all possible children recursively, but I can still leverage 
    the trie structure to prune impossible paths early."

16. REAL-WORLD APPLICATIONS:
    - Search engines with wildcard queries
    - Pattern matching in text processing
    - Spell checkers with approximate matching
    - Database wildcard searches
    - Regular expression engines (simplified)

17. INTERVIEW TIPS:
    - Emphasize the backtracking aspect for wildcards
    - Draw tree showing wildcard exploration
    - Explain complexity trade-offs clearly
    - Show understanding of when wildcards make search expensive
    - Mention optimization strategies for production systems
"""
