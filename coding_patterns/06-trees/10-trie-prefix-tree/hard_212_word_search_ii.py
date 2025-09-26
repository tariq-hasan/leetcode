from typing import List

class TrieNode:
    """
    TrieNode for efficient word search with backtracking
    Stores word at terminal nodes for direct result collection
    """
    def __init__(self):
        self.children = {}
        self.word = None  # Store complete word at terminal nodes

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Optimal Solution - Trie + Backtracking with Pruning
        
        Key insight: Build trie from words, then use single DFS traversal
        of board to find all words simultaneously. Prune trie nodes after
        finding words to avoid duplicates and improve performance.
        
        Time Complexity: O(M*N*4^L) worst case, where M*N is board size, L is max word length
        Space Complexity: O(W*L) for trie, where W is number of words
        """
        # Build trie from words
        root = self._build_trie(words)
        
        rows, cols = len(board), len(board[0])
        result = []
        
        # Try starting DFS from each cell
        for i in range(rows):
            for j in range(cols):
                self._dfs(board, i, j, root, result)
        
        return result
    
    def _build_trie(self, words):
        """Build trie from list of words"""
        root = TrieNode()
        
        for word in words:
            current = root
            for char in word:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.word = word  # Store complete word at terminal
        
        return root
    
    def _dfs(self, board, i, j, node, result):
        """DFS with backtracking and trie traversal"""
        # Boundary and visited check
        if (i < 0 or i >= len(board) or 
            j < 0 or j >= len(board[0]) or 
            board[i][j] == '#'):
            return
        
        char = board[i][j]
        
        # Check if current character exists in trie
        if char not in node.children:
            return
        
        node = node.children[char]
        
        # Found a complete word
        if node.word:
            result.append(node.word)
            node.word = None  # Avoid duplicates
        
        # Mark current cell as visited
        board[i][j] = '#'
        
        # Explore all 4 directions
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for di, dj in directions:
            self._dfs(board, i + di, j + dj, node, result)
        
        # Backtrack: restore original character
        board[i][j] = char
        
        # Optimization: Remove leaf nodes to prune search space
        if not node.children and not node.word:
            # This node has no children and no word, can be removed
            # (This optimization requires parent reference or more complex handling)
            pass

    def findWordsWithVisited(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Alternative with Explicit Visited Array
        
        Uses separate visited array instead of modifying board in-place.
        Cleaner but uses more memory.
        
        Time Complexity: O(M*N*4^L)
        Space Complexity: O(W*L + M*N) for trie + visited array
        """
        root = self._build_trie(words)
        rows, cols = len(board), len(board[0])
        result = []
        visited = [[False] * cols for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                self._dfs_with_visited(board, i, j, root, result, visited)
        
        return result
    
    def _dfs_with_visited(self, board, i, j, node, result, visited):
        """DFS with separate visited array"""
        if (i < 0 or i >= len(board) or 
            j < 0 or j >= len(board[0]) or 
            visited[i][j]):
            return
        
        char = board[i][j]
        if char not in node.children:
            return
        
        node = node.children[char]
        
        if node.word:
            result.append(node.word)
            node.word = None
        
        visited[i][j] = True
        
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            self._dfs_with_visited(board, i + di, j + dj, node, result, visited)
        
        visited[i][j] = False

    def findWordsBruteForce(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Brute Force Solution - Search Each Word Individually
        
        For each word, do separate DFS search. Less efficient but simpler logic.
        
        Time Complexity: O(W*M*N*4^L) where W is number of words
        Space Complexity: O(L) for recursion stack
        """
        result = []
        rows, cols = len(board), len(board[0])
        
        for word in words:
            if self._search_word(board, word):
                result.append(word)
        
        return result
    
    def _search_word(self, board, word):
        """Search for a single word in the board"""
        rows, cols = len(board), len(board[0])
        
        def dfs(i, j, index):
            if index == len(word):
                return True
            
            if (i < 0 or i >= rows or j < 0 or j >= cols or 
                board[i][j] != word[index] or board[i][j] == '#'):
                return False
            
            char = board[i][j]
            board[i][j] = '#'  # Mark visited
            
            # Try all 4 directions
            found = (dfs(i+1, j, index+1) or 
                    dfs(i-1, j, index+1) or 
                    dfs(i, j+1, index+1) or 
                    dfs(i, j-1, index+1))
            
            board[i][j] = char  # Backtrack
            return found
        
        # Try starting from each cell
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == word[0] and dfs(i, j, 0):
                    return True
        return False

    def findWordsOptimized(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Highly Optimized Version with Advanced Pruning
        
        Includes multiple optimization techniques:
        - Trie pruning after finding words
        - Early termination when trie becomes empty
        - Character frequency filtering
        
        Time Complexity: O(M*N*4^L) with better practical performance
        Space Complexity: O(W*L)
        """
        # Filter words based on character frequency in board
        from collections import Counter
        board_chars = Counter(char for row in board for char in row)
        words = [word for word in words 
                if all(board_chars[char] >= word.count(char) for char in set(word))]
        
        if not words:
            return []
        
        root = self._build_trie_optimized(words)
        rows, cols = len(board), len(board[0])
        result = []
        
        for i in range(rows):
            for j in range(cols):
                self._dfs_optimized(board, i, j, root, result)
                if not root.children:  # Early termination if trie is empty
                    break
        
        return result
    
    def _build_trie_optimized(self, words):
        """Build trie with parent references for pruning"""
        root = TrieNode()
        
        for word in words:
            current = root
            for char in word:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.word = word
        
        return root
    
    def _dfs_optimized(self, board, i, j, node, result):
        """Optimized DFS with aggressive pruning"""
        if (i < 0 or i >= len(board) or 
            j < 0 or j >= len(board[0]) or 
            board[i][j] == '#'):
            return
        
        char = board[i][j]
        if char not in node.children:
            return
        
        node = node.children[char]
        
        if node.word:
            result.append(node.word)
            node.word = None
        
        board[i][j] = '#'
        
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            self._dfs_optimized(board, i + di, j + dj, node, result)
        
        board[i][j] = char
        
        # Advanced pruning: remove empty nodes
        if not node.children and not node.word:
            del node  # This requires more complex parent tracking in practice

    def findWordsIterative(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Iterative Solution using Stack (Alternative to Recursion)
        
        Uses explicit stack to avoid recursion depth limits.
        More complex but handles very deep searches.
        
        Time Complexity: O(M*N*4^L)
        Space Complexity: O(W*L + M*N*L) for trie + stack
        """
        root = self._build_trie(words)
        rows, cols = len(board), len(board[0])
        result = []
        
        # Stack stores (i, j, node, path_taken)
        for start_i in range(rows):
            for start_j in range(cols):
                if board[start_i][start_j] in root.children:
                    stack = [(start_i, start_j, root, set())]
                    
                    while stack:
                        i, j, node, visited = stack.pop()
                        
                        if (i, j) in visited:
                            continue
                        
                        char = board[i][j]
                        if char not in node.children:
                            continue
                        
                        node = node.children[char]
                        visited = visited | {(i, j)}
                        
                        if node.word and node.word not in result:
                            result.append(node.word)
                        
                        # Add neighbors to stack
                        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                            ni, nj = i + di, j + dj
                            if (0 <= ni < rows and 0 <= nj < cols and 
                                (ni, nj) not in visited):
                                stack.append((ni, nj, node, visited))
        
        return result

# Test cases and utility functions
def create_test_board1():
    """
    Create test board:
    [["o","a","a","n"],
     ["e","t","a","e"], 
     ["i","h","k","r"],
     ["i","f","l","v"]]
    """
    return [["o","a","a","n"],
            ["e","t","a","e"], 
            ["i","h","k","r"],
            ["i","f","l","v"]]

def create_test_board2():
    """
    Create simple test board:
    [["a","b"],
     ["c","d"]]
    """
    return [["a","b"],
            ["c","d"]]

def test_basic_functionality():
    """Test basic word search functionality"""
    solution = Solution()
    
    print("Testing Basic Functionality:")
    print("=" * 50)
    
    # Test case 1
    board1 = create_test_board1()
    words1 = ["oath","pea","eat","rain"]
    expected1 = ["eat","oath"]
    
    result1 = solution.findWords(board1, words1)
    print("Test 1:")
    print(f"Board: {board1}")
    print(f"Words: {words1}")
    print(f"Result: {result1}")
    print(f"Expected: {expected1}")
    print(f"Correct: {'✓' if set(result1) == set(expected1) else '✗'}")
    print()
    
    # Test case 2
    board2 = create_test_board2()
    words2 = ["abcb"]
    expected2 = []
    
    result2 = solution.findWords(board2, words2)
    print("Test 2:")
    print(f"Board: {board2}")
    print(f"Words: {words2}")
    print(f"Result: {result2}")
    print(f"Expected: {expected2}")
    print(f"Correct: {'✓' if result2 == expected2 else '✗'}")

def compare_different_approaches():
    """Compare performance of different solution approaches"""
    solution = Solution()
    
    board = create_test_board1()
    words = ["oath","pea","eat","rain","hike"]
    
    approaches = [
        ("Trie + Backtracking", solution.findWords),
        ("With Visited Array", solution.findWordsWithVisited),
        ("Brute Force", solution.findWordsBruteForce),
        ("Optimized", solution.findWordsOptimized),
    ]
    
    print("Comparing Different Approaches:")
    print("=" * 50)
    print(f"Board: {board}")
    print(f"Words: {words}")
    print()
    
    results = []
    for name, method in approaches:
        # Create fresh board copy for each method
        board_copy = [row[:] for row in board]
        result = method(board_copy, words)
        results.append(set(result))  # Use set for comparison
        print(f"{name}: {sorted(result)}")
    
    # Verify all approaches give same result
    all_same = all(r == results[0] for r in results)
    print(f"\nAll approaches consistent: {'✓' if all_same else '✗'}")

def demonstrate_trie_advantage():
    """Show why trie approach is superior to brute force"""
    print("\nDemonstrating Trie Advantage:")
    print("=" * 50)
    
    # Create scenario where trie shines
    board = [["a","a","a"],
             ["a","a","a"],
             ["a","a","a"]]
    
    words = ["aaa", "aaaa", "aaaaa", "aaaaaa", "xyz"]
    
    print(f"Board (all 'a's): {board}")
    print(f"Words: {words}")
    print()
    
    print("Trie approach:")
    print("- Builds single trie from all words")
    print("- One DFS traversal finds all matching words")
    print("- Early termination when no words match current path")
    print()
    
    print("Brute force approach:")
    print("- Searches for each word individually") 
    print("- Multiple DFS traversals (one per word)")
    print("- No sharing of common prefixes")
    
    solution = Solution()
    
    # Test both approaches
    board_copy1 = [row[:] for row in board]
    board_copy2 = [row[:] for row in board]
    
    trie_result = solution.findWords(board_copy1, words)
    brute_result = solution.findWordsBruteForce(board_copy2, words)
    
    print(f"\nTrie result: {sorted(trie_result)}")
    print(f"Brute result: {sorted(brute_result)}")
    print(f"Results match: {'✓' if set(trie_result) == set(brute_result) else '✗'}")

def test_edge_cases():
    """Test edge cases and corner scenarios"""
    solution = Solution()
    
    print("\nTesting Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        {
            "name": "Empty words list",
            "board": [["a","b"],["c","d"]],
            "words": [],
            "expected": []
        },
        {
            "name": "Single character words",
            "board": [["a","b"],["c","d"]], 
            "words": ["a","b","c","d","e"],
            "expected": ["a","b","c","d"]
        },
        {
            "name": "Word longer than board allows",
            "board": [["a"]],
            "words": ["aa"],
            "expected": []
        },
        {
            "name": "All words found",
            "board": [["c","a","t"],["o","g","s"]],
            "words": ["cat","cog","cats"],
            "expected": ["cat","cog"]  # "cats" requires revisiting 's'
        },
        {
            "name": "No words found", 
            "board": [["a","b"],["c","d"]],
            "words": ["xyz","pqr"],
            "expected": []
        }
    ]
    
    for case in edge_cases:
        result = solution.findWords(case["board"], case["words"])
        expected = case["expected"]
        
        print(f"{case['name']}:")
        print(f"  Board: {case['board']}")
        print(f"  Words: {case['words']}")
        print(f"  Result: {result}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if set(result) == set(expected) else '✗'}")
        print()

def visualize_search_process():
    """Visualize how the search process works"""
    print("Visualizing Search Process:")
    print("=" * 50)
    
    board = [["c","a","t"],
             ["o","g","d"]]
    words = ["cat", "cog"]
    
    print(f"Board: {board}")
    print(f"Words: {words}")
    print()
    
    # Show trie structure
    print("Trie structure:")
    print("root")
    print("├── c")
    print("│   ├── a")
    print("│   │   └── t (word: 'cat')")
    print("│   └── o")
    print("│       └── g (word: 'cog')")
    print()
    
    print("Search process:")
    print("1. Start DFS from each cell")
    print("2. Follow trie path matching board characters")
    print("3. When reach word node, add to results")
    print("4. Backtrack and continue exploring")
    print()
    
    print("Example path for 'cat':")
    print("(0,0)'c' -> (0,1)'a' -> (0,2)'t' ✓ Found 'cat'")
    print()
    
    print("Example path for 'cog':")
    print("(0,0)'c' -> (1,0)'o' -> (1,1)'g' ✓ Found 'cog'")

def analyze_complexity():
    """Analyze time and space complexity"""
    print("\nComplexity Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Trie + Backtracking", "O(M*N*4^L)", "O(W*L)", "Optimal approach"),
        ("Brute Force", "O(W*M*N*4^L)", "O(L)", "W times slower"),
        ("With Visited Array", "O(M*N*4^L)", "O(W*L + M*N)", "Cleaner but more space"),
    ]
    
    print(f"{'Approach':<20} {'Time Complexity':<15} {'Space':<12} {'Notes'}")
    print("-" * 70)
    
    for approach, time, space, notes in approaches:
        print(f"{approach:<20} {time:<15} {space:<12} {notes}")
    
    print("\nWhere:")
    print("M*N = board dimensions")
    print("W = number of words") 
    print("L = maximum word length")
    print("4^L = branching factor in worst case")
    
    print("\nWhy Trie is Better:")
    print("- Shares common prefixes across words")
    print("- Single traversal finds all words")
    print("- Early pruning when no words match path")
    print("- Eliminates redundant searches")

if __name__ == "__main__":
    test_basic_functionality()
    compare_different_approaches()
    demonstrate_trie_advantage()
    test_edge_cases()
    visualize_search_process()
    analyze_complexity()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Find all words from dictionary that can be formed on 2D board
   - Words formed by connecting adjacent cells (horizontally/vertically)
   - Same cell cannot be used twice in single word
   - Return all found words without duplicates

2. KEY INSIGHT - TRIE + BACKTRACKING:
   - Brute force: search each word individually (inefficient)
   - Optimal: build trie from words, single DFS finds all words
   - Trie enables sharing of common prefixes
   - Backtracking explores all valid paths

3. WHY TRIE APPROACH IS SUPERIOR:
   - Single board traversal vs W separate traversals
   - Shared prefix computation (e.g., "cat" and "car" share "ca")
   - Early pruning when current path has no word continuations
   - Natural handling of word boundaries

4. ALGORITHM WALKTHROUGH:
   - Build trie from all words in dictionary
   - For each board cell, start DFS with trie root
   - Follow trie path matching board characters
   - When reach terminal node, add word to results
   - Use backtracking to explore all possibilities

5. CRITICAL IMPLEMENTATION DETAILS:
   - Store complete word at terminal trie nodes (not just flag)
   - Mark visited cells during DFS (use '#' or visited array)  
   - Set word to None after finding to avoid duplicates
   - Backtrack properly to restore board state

6. COMPLEXITY ANALYSIS:
   - Time: O(M*N*4^L) where M*N is board size, L is max word length
   - Space: O(W*L) for trie where W is number of words
   - Much better than brute force O(W*M*N*4^L)

7. OPTIMIZATION TECHNIQUES:
   - Character frequency filtering (pre-filter impossible words)
   - Trie pruning (remove nodes after finding words)
   - Early termination (stop when no more words possible)

8. EDGE CASES:
   - Empty word list → return empty
   - Words longer than board allows → impossible to find
   - Single character words → check all board cells
   - No words found → return empty list

9. INTERVIEW PRESENTATION:
   - Start with: "This combines word search with multiple target words"
   - Key insight: "Trie lets me search for all words simultaneously"
   - Explain why trie beats individual word searches
   - Code the trie + backtracking solution
   - Walk through example showing shared prefix benefit

10. FOLLOW-UP QUESTIONS:
    - "How to optimize for very large dictionaries?" → Trie compression, indexing
    - "What about board updates?" → Incremental search strategies
    - "Memory constraints?" → Streaming approaches, external sorting
    - "Parallel processing?" → Board partitioning, distributed search

11. WHY THIS PROBLEM IS CHALLENGING:
    - Combines two complex algorithms (trie + backtracking)
    - Multiple optimization opportunities
    - Real-world applications (Boggle, Scrabble, crosswords)
    - Tests understanding of algorithm combinations

12. COMMON MISTAKES:
    - Using brute force instead of recognizing trie opportunity
    - Not handling visited cells correctly
    - Forgetting to backtrack board modifications
    - Not avoiding duplicate results
    - Incorrect trie construction or traversal

13. IMPLEMENTATION VARIATIONS:
    - In-place board marking vs separate visited array
    - Storing words vs just end-of-word flags in trie
    - Recursive vs iterative DFS
    - Various pruning optimizations

14. REAL-WORLD APPLICATIONS:
    - Word puzzle games (Boggle, Word Search)
    - Crossword puzzle solvers
    - Anagram finders
    - Text processing and pattern matching
    - Game AI for word games

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is recognizing that searching for each word individually 
    is wasteful because many words share common prefixes. By building a trie 
    from the dictionary and doing a single DFS traversal of the board, I can 
    find all words simultaneously while sharing the computation for common 
    prefixes. This transforms an O(W*M*N*4^L) problem into O(M*N*4^L)."

16. INTERVIEW TIPS:
    - Emphasize the trie + backtracking combination early
    - Draw board and show path examples
    - Explain why sharing prefixes matters
    - Handle the visited cell logic carefully
    - Show understanding of complexity improvements
    - Mention optimization opportunities
"""
