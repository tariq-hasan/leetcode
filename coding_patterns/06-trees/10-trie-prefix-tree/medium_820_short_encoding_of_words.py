from typing import List

class TrieNode:
    """
    TrieNode for suffix-based trie (reverse trie)
    Used to detect which words are suffixes of other words
    """
    def __init__(self):
        self.children = {}
        self.is_word = False

class Solution:
    def minimumLengthEncoding(self, words: List[str]) -> int:
        """
        Optimal Solution - Reverse Trie (Suffix Tree)
        
        Key insight: A word can be eliminated if it's a suffix of another word.
        Use reverse trie to detect suffix relationships efficiently.
        
        Time Complexity: O(N * M) where N is number of words, M is max word length
        Space Complexity: O(N * M) for the trie
        """
        # Remove duplicates and sort by length (optimization)
        words = list(set(words))
        
        # Build reverse trie (insert words backwards)
        root = TrieNode()
        
        for word in words:
            current = root
            for char in reversed(word):
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_word = True
        
        # Find words that are not suffixes of other words
        encoding_length = 0
        
        for word in words:
            if self._is_leaf_word(root, word):
                encoding_length += len(word) + 1  # +1 for '#' delimiter
        
        return encoding_length
    
    def _is_leaf_word(self, root, word):
        """Check if word ends at a leaf or has no other words as extensions"""
        current = root
        for char in reversed(word):
            current = current.children[char]
        
        # Word contributes to encoding if it's at a leaf (no extensions)
        return len(current.children) == 0

    def minimumLengthEncodingSetBased(self, words: List[str]) -> int:
        """
        Set-Based Solution (More Intuitive)
        
        Key insight: Remove words that are suffixes of other words.
        Use set operations to efficiently find non-suffix words.
        
        Time Complexity: O(N * M^2) where N is number of words, M is max length
        Space Complexity: O(N * M) for storing all suffixes
        """
        # Convert to set to remove duplicates
        word_set = set(words)
        
        # Remove words that are suffixes of other words
        for word in words:
            # Check all proper suffixes of current word
            for i in range(1, len(word)):
                suffix = word[i:]
                word_set.discard(suffix)  # Remove if exists
        
        # Calculate encoding length
        return sum(len(word) + 1 for word in word_set)

    def minimumLengthEncodingSorting(self, words: List[str]) -> int:
        """
        Sorting-Based Solution
        
        Sort words by length (descending), then check if each word is 
        a suffix of any previously processed longer word.
        
        Time Complexity: O(N * M^2 + N log N) for sorting and suffix checking
        Space Complexity: O(N * M) for storing words
        """
        # Remove duplicates and sort by length (longest first)
        words = sorted(set(words), key=len, reverse=True)
        
        encoding = []
        
        for word in words:
            # Check if current word is suffix of any word in encoding
            is_suffix = False
            for encoded_word in encoding:
                if encoded_word.endswith(word):
                    is_suffix = True
                    break
            
            if not is_suffix:
                encoding.append(word)
        
        return sum(len(word) + 1 for word in encoding)

    def minimumLengthEncodingDFS(self, words: List[str]) -> int:
        """
        DFS-Based Solution with Reverse Trie
        
        Build reverse trie then use DFS to find all leaf words
        More explicit about the tree traversal
        
        Time Complexity: O(N * M)
        Space Complexity: O(N * M)
        """
        # Build reverse trie
        root = TrieNode()
        word_to_node = {}
        
        for word in set(words):
            current = root
            for char in reversed(word):
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_word = True
            word_to_node[word] = current
        
        # Find leaf words using DFS
        def dfs(node, depth):
            """Return encoding length for subtree rooted at node"""
            if not node.children:  # Leaf node
                return depth + 1  # +1 for delimiter
            
            # Internal node: sum of all subtrees
            total = 0
            for child in node.children.values():
                total += dfs(child, depth + 1)
            return total
        
        return dfs(root, 0)

    def minimumLengthEncodingHashMap(self, words: List[str]) -> int:
        """
        HashMap-Based Solution (Alternative Approach)
        
        Use suffix counting to determine which words can be eliminated
        
        Time Complexity: O(N * M^2)
        Space Complexity: O(N * M)
        """
        from collections import defaultdict
        
        # Count occurrences of each suffix
        suffix_count = defaultdict(int)
        
        for word in words:
            for i in range(len(word) + 1):
                suffix = word[i:]
                suffix_count[suffix] += 1
        
        # Words that appear as suffixes of other words don't contribute
        encoding_length = 0
        
        for word in set(words):
            # Check if word is only present as itself (not as suffix of others)
            is_only_self = True
            for i in range(len(word)):
                suffix = word[i:]
                if suffix in suffix_count and suffix_count[suffix] > suffix_count[word]:
                    is_only_self = False
                    break
            
            if is_only_self:
                encoding_length += len(word) + 1
        
        return encoding_length

    def minimumLengthEncodingBruteForce(self, words: List[str]) -> int:
        """
        Brute Force Solution (For Understanding)
        
        Check every pair of words to see if one is suffix of another
        Not efficient but demonstrates the core logic clearly
        
        Time Complexity: O(N^2 * M)
        Space Complexity: O(N)
        """
        words = list(set(words))  # Remove duplicates
        keep = [True] * len(words)
        
        # Check every pair
        for i in range(len(words)):
            for j in range(len(words)):
                if i != j and words[j].endswith(words[i]):
                    keep[i] = False  # words[i] is suffix of words[j]
                    break
        
        # Sum lengths of words we keep
        return sum(len(words[i]) + 1 for i in range(len(words)) if keep[i])

# Test cases and utility functions
def test_basic_cases():
    """Test basic functionality with simple examples"""
    solution = Solution()
    
    test_cases = [
        (["time", "me", "bell"], 10),  # "time#bell#" -> "me" is suffix of "time"
        (["t"], 2),                    # "t#"
        (["me", "time"], 5),          # "time#" -> "me" is suffix of "time"
        (["time", "atime"], 10),      # "time#atime#" -> no suffixes
        (["abc", "bc", "c"], 4),      # "abc#" -> "bc" and "c" are suffixes
    ]
    
    print("Testing Basic Cases:")
    print("=" * 50)
    
    for i, (words, expected) in enumerate(test_cases):
        result = solution.minimumLengthEncoding(words)
        status = "✓" if result == expected else "✗"
        print(f"Test {i+1}: {words}")
        print(f"  Result: {result}, Expected: {expected} {status}")
        print()

def test_different_approaches():
    """Compare different solution approaches"""
    solution = Solution()
    
    test_words = ["time", "me", "bell", "t", "atime"]
    
    approaches = [
        ("Reverse Trie", solution.minimumLengthEncoding),
        ("Set-Based", solution.minimumLengthEncodingSetBased),
        ("Sorting", solution.minimumLengthEncodingSorting),
        ("DFS", solution.minimumLengthEncodingDFS),
        ("Brute Force", solution.minimumLengthEncodingBruteForce),
    ]
    
    print("Comparing Different Approaches:")
    print("=" * 50)
    print(f"Input: {test_words}")
    print()
    
    results = []
    for name, method in approaches:
        result = method(test_words)
        results.append(result)
        print(f"{name:<15}: {result}")
    
    # Verify all approaches give same result
    all_same = all(r == results[0] for r in results)
    print(f"\nAll approaches consistent: {'✓' if all_same else '✗'}")

def demonstrate_suffix_relationships():
    """Show how suffix relationships work"""
    print("\nDemonstrating Suffix Relationships:")
    print("=" * 50)
    
    examples = [
        (["time", "me"], "me is suffix of time"),
        (["abc", "bc", "c"], "bc is suffix of abc, c is suffix of bc and abc"),
        (["bell", "ell", "ll", "l"], "each is suffix of the previous"),
        (["cat", "dog"], "no suffix relationships"),
    ]
    
    solution = Solution()
    
    for words, explanation in examples:
        result = solution.minimumLengthEncoding(words)
        set_result = solution.minimumLengthEncodingSetBased(words)
        
        print(f"Words: {words}")
        print(f"Explanation: {explanation}")
        print(f"Encoding length: {result}")
        print(f"Set-based result: {set_result}")
        print()

def visualize_trie_building():
    """Visualize how the reverse trie is built"""
    print("Visualizing Reverse Trie Construction:")
    print("=" * 50)
    
    words = ["time", "me", "bell"]
    print(f"Building reverse trie for: {words}")
    print()
    
    # Build trie step by step
    root = TrieNode()
    
    for word in words:
        print(f"Inserting '{word}' (reversed: '{''.join(reversed(word))}')")
        current = root
        path = "root"
        
        for char in reversed(word):
            if char not in current.children:
                current.children[char] = TrieNode()
                print(f"  Created new node for '{char}' at {path}")
            current = current.children[char]
            path += f" -> {char}"
        
        current.is_word = True
        print(f"  Marked end of word at {path}")
        print()
    
    # Show which words are at leaves
    def find_leaf_words(node, depth, word_so_far):
        if node.is_word and not node.children:
            print(f"Leaf word: {''.join(reversed(word_so_far))} (depth {depth})")
        
        for char, child in node.children.items():
            find_leaf_words(child, depth + 1, word_so_far + [char])
    
    print("Words at leaf positions (contribute to encoding):")
    find_leaf_words(root, 0, [])

def analyze_complexity():
    """Analyze time and space complexity of different approaches"""
    print("\nComplexity Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Reverse Trie", "O(N*M)", "O(N*M)", "Optimal for most cases"),
        ("Set-Based", "O(N*M²)", "O(N*M)", "Simple but less efficient"),
        ("Sorting", "O(N*M² + N log N)", "O(N*M)", "Good for sorted input"),
        ("Brute Force", "O(N²*M)", "O(N)", "Clear logic but inefficient"),
    ]
    
    print(f"{'Approach':<15} {'Time':<15} {'Space':<10} {'Notes'}")
    print("-" * 60)
    
    for approach, time, space, notes in approaches:
        print(f"{approach:<15} {time:<15} {space:<10} {notes}")
    
    print("\nWhere N = number of words, M = maximum word length")
    print("\nRecommendation: Use reverse trie for optimal performance")

def demonstrate_edge_cases():
    """Test edge cases and corner scenarios"""
    solution = Solution()
    
    print("\nTesting Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        ([], 0, "Empty list"),
        (["a"], 2, "Single character"),
        (["a", "a"], 2, "Duplicates"),
        (["abc", "def"], 8, "No relationships"),
        (["a", "aa", "aaa"], 4, "Nested suffixes"),
        (["abcd", "cd", "bcd"], 6, "Multiple suffix patterns"),
    ]
    
    for words, expected, description in edge_cases:
        result = solution.minimumLengthEncoding(words)
        status = "✓" if result == expected else "✗"
        print(f"{description}: {words}")
        print(f"  Result: {result}, Expected: {expected} {status}")

if __name__ == "__main__":
    test_basic_cases()
    test_different_approaches()
    demonstrate_suffix_relationships()
    visualize_trie_building()
    analyze_complexity()
    demonstrate_edge_cases()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Encode words using shortest string where words end with '#'
   - Words can share common suffixes in encoding
   - Example: ["time", "me"] -> "time#" (6 chars) since "me" is suffix of "time"
   - Goal: Find minimum length of encoded string

2. KEY INSIGHT - SUFFIX ELIMINATION:
   - A word can be omitted if it's a suffix of another word
   - Only need to keep words that are NOT suffixes of other words
   - Example: in ["time", "me"], "me" is suffix of "time", so omit "me"

3. OPTIMAL APPROACH - REVERSE TRIE:
   - Build trie with words inserted backwards (suffixes become prefixes)
   - Words at leaf positions are not suffixes of other words
   - These leaf words contribute to final encoding length

4. WHY REVERSE TRIE WORKS:
   - Inserting "time" backwards: e->m->i->t
   - Inserting "me" backwards: e->m (stops here, doesn't reach leaf)
   - Only "time" reaches leaf position, so only it contributes

5. ALGORITHM WALKTHROUGH:
   - Build reverse trie by inserting each word backwards
   - Mark word endings in trie
   - Find words that end at leaf positions (no extensions)
   - Sum: length of each leaf word + 1 (for delimiter)

6. ALTERNATIVE APPROACHES:

   APPROACH 1 - Reverse Trie (RECOMMENDED):
   - Most efficient: O(N*M) time and space
   - Elegant use of trie data structure
   - Clear separation of suffix relationships

   APPROACH 2 - Set-based Elimination:
   - More intuitive: remove words that are suffixes
   - O(N*M²) time complexity
   - Good for explanation but less efficient

   APPROACH 3 - Sorting + Checking:
   - Sort by length, check if each word is suffix of longer words
   - O(N*M² + N log N) time complexity
   - Natural approach but not optimal

7. COMPLEXITY ANALYSIS:
   - Reverse Trie: O(N*M) time, O(N*M) space
   - Set-based: O(N*M²) time, O(N*M) space
   - Where N = number of words, M = max word length

8. EDGE CASES:
   - Empty input → 0
   - Single word → len(word) + 1
   - No suffix relationships → sum of all lengths + N
   - Duplicate words → handle with set deduplication
   - Nested suffixes: "a", "aa", "aaa" → only "aaa" contributes

9. INTERVIEW PRESENTATION:
   - Start with: "I need to eliminate words that are suffixes of others"
   - Key insight: "Reverse trie makes suffix detection efficient"
   - Explain why backwards insertion works
   - Code the reverse trie solution
   - Walk through example showing leaf detection

10. FOLLOW-UP QUESTIONS:
    - "Can you optimize space?" → Discuss trie compression techniques
    - "What if words are very long?" → Mention suffix array alternatives
    - "How to handle updates?" → Dynamic trie maintenance
    - "Multiple delimiters?" → Extend algorithm for different separators

11. WHY THIS PROBLEM IS CLEVER:
    - Tests understanding of suffix relationships
    - Creative use of reverse trie data structure
    - Shows optimization through data structure choice
    - Real-world relevance (data compression, dictionary storage)

12. COMMON MISTAKES:
    - Not recognizing the suffix elimination insight
    - Using forward trie instead of reverse trie
    - Forgetting to add delimiter length to final answer
    - Not handling duplicates properly
    - Inefficient suffix checking (O(N²) approaches)

13. IMPLEMENTATION DETAILS:
    - Use set() to remove duplicates early
    - Insert words backwards into trie
    - Check if word ends at leaf position (no children)
    - Add 1 for delimiter when calculating lengths

14. OPTIMIZATION INSIGHTS:
    - Reverse trie is key optimization over brute force
    - Set deduplication reduces unnecessary work
    - Early termination in suffix checking
    - Memory-efficient trie representation

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is recognizing that words appearing as suffixes of 
    other words can be eliminated from the encoding. Using a reverse trie 
    (inserting words backwards) transforms the suffix detection problem 
    into a simple leaf identification problem, giving us optimal O(N*M) 
    performance."

16. REAL-WORLD APPLICATIONS:
    - Dictionary compression
    - URL shortening systems
    - Database index compression
    - Text compression algorithms
    - Autocomplete data structures

17. INTERVIEW TIPS:
    - Start with brute force to show understanding
    - Explain the suffix elimination insight clearly
    - Show why reverse trie is better than other approaches
    - Walk through trie construction with example
    - Mention complexity improvements over naive solutions
"""
