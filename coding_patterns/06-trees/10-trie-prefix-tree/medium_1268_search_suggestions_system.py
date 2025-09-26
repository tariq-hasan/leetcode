from typing import List
import bisect

class TrieNode:
    """
    TrieNode with suggestions storage for efficient retrieval
    Stores up to 3 lexicographically smallest suggestions at each node
    """
    def __init__(self):
        self.children = {}
        self.suggestions = []  # Store up to 3 suggestions at this prefix

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Optimal Solution - Trie with Stored Suggestions
        
        Key insight: Build trie where each node stores up to 3 lexicographically
        smallest words with that prefix. This allows O(1) suggestion retrieval.
        
        Time Complexity: O(N*M + S) where N=products, M=avg length, S=searchWord length
        Space Complexity: O(N*M) for trie storage
        """
        # Build trie with suggestions
        root = self._build_trie_with_suggestions(products)
        
        result = []
        current = root
        
        for char in searchWord:
            if current and char in current.children:
                current = current.children[char]
                result.append(current.suggestions[:])  # Copy suggestions
            else:
                current = None  # No valid prefix anymore
                result.append([])  # No suggestions possible
        
        return result
    
    def _build_trie_with_suggestions(self, products):
        """Build trie where each node stores up to 3 best suggestions"""
        root = TrieNode()
        
        # Sort products to ensure lexicographic order
        products.sort()
        
        for product in products:
            current = root
            for char in product:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
                
                # Add this product to suggestions if we have room
                if len(current.suggestions) < 3:
                    current.suggestions.append(product)
        
        return root

    def suggestedProductsBinarySearch(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Binary Search Solution (Simple and Efficient)
        
        Key insight: Sort products, then for each prefix use binary search
        to find starting position and take next 3 items.
        
        Time Complexity: O(N log N + S*log N + S*M) for sorting + binary search + validation
        Space Complexity: O(1) extra space (not counting output)
        """
        products.sort()  # Sort for lexicographic order
        result = []
        prefix = ""
        
        for char in searchWord:
            prefix += char
            
            # Binary search for first product starting with prefix
            start_idx = bisect.bisect_left(products, prefix)
            
            suggestions = []
            # Take up to 3 products starting from start_idx that match prefix
            for i in range(start_idx, min(start_idx + 3, len(products))):
                if products[i].startswith(prefix):
                    suggestions.append(products[i])
                else:
                    break  # No more products with this prefix
            
            result.append(suggestions)
        
        return result

    def suggestedProductsTrieStandard(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Standard Trie + DFS Solution (Most Educational)
        
        Build standard trie, then for each prefix do DFS to find suggestions.
        Less optimal but shows the core trie + search pattern clearly.
        
        Time Complexity: O(N*M + S*3*M) for trie building + DFS searches
        Space Complexity: O(N*M) for trie
        """
        # Build standard trie
        root = TrieNode()
        
        for product in products:
            current = root
            for char in product:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            # Mark end of word (could use is_word flag)
        
        result = []
        prefix = ""
        
        for char in searchWord:
            prefix += char
            
            # Find trie node for current prefix
            current = root
            valid_prefix = True
            
            for p_char in prefix:
                if p_char in current.children:
                    current = current.children[p_char]
                else:
                    valid_prefix = False
                    break
            
            if valid_prefix:
                # DFS to find up to 3 suggestions
                suggestions = []
                self._dfs_suggestions(current, prefix, suggestions, products)
                result.append(sorted(suggestions)[:3])
            else:
                result.append([])
        
        return result
    
    def _dfs_suggestions(self, node, current_prefix, suggestions, products):
        """DFS to collect suggestions from trie node"""
        if len(suggestions) >= 3:
            return
        
        # Check if current prefix is a valid product
        if current_prefix in products:
            suggestions.append(current_prefix)
        
        # Explore children in lexicographic order
        for char in sorted(node.children.keys()):
            if len(suggestions) >= 3:
                break
            self._dfs_suggestions(node.children[char], 
                                current_prefix + char, suggestions, products)

    def suggestedProductsBruteForce(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Brute Force Solution (For Understanding)
        
        For each prefix, scan all products to find matches.
        Inefficient but demonstrates the core logic clearly.
        
        Time Complexity: O(S * N * M) where S=searchWord, N=products, M=avg length
        Space Complexity: O(1) extra space
        """
        result = []
        
        for i in range(len(searchWord)):
            prefix = searchWord[:i+1]
            
            # Find all products starting with prefix
            matches = []
            for product in products:
                if product.startswith(prefix):
                    matches.append(product)
            
            # Sort and take first 3
            matches.sort()
            result.append(matches[:3])
        
        return result

    def suggestedProductsOptimizedBinarySearch(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Optimized Binary Search (Advanced)
        
        Uses the fact that prefixes get longer, so search space narrows.
        Maintains window of valid products instead of searching entire array.
        
        Time Complexity: O(N log N + S*log N) amortized better performance
        Space Complexity: O(1) extra space
        """
        products.sort()
        result = []
        
        # Keep track of valid range
        left, right = 0, len(products) - 1
        
        for i, char in enumerate(searchWord):
            prefix = searchWord[:i+1]
            
            # Narrow down left boundary
            while left <= right and (len(products[left]) <= i or 
                                   products[left][i] < char):
                left += 1
            
            # Narrow down right boundary  
            while left <= right and (len(products[right]) <= i or 
                                   products[right][i] > char):
                right -= 1
            
            # Collect suggestions from valid range
            suggestions = []
            for j in range(left, min(left + 3, right + 1)):
                if j < len(products) and products[j].startswith(prefix):
                    suggestions.append(products[j])
            
            result.append(suggestions)
            
            # If no valid products, break early
            if left > right:
                # Add empty results for remaining characters
                result.extend([[] for _ in range(len(searchWord) - i - 1)])
                break
        
        return result

# Test cases and utility functions
def test_basic_functionality():
    """Test basic search suggestions functionality"""
    solution = Solution()
    
    test_cases = [
        {
            "products": ["mobile","mouse","moneypot","monitor","mousepad"],
            "searchWord": "mouse",
            "expected": [
                ["mobile","moneypot","monitor"],
                ["mobile","moneypot","monitor"], 
                ["mouse","mousepad"],
                ["mouse","mousepad"],
                ["mouse","mousepad"]
            ]
        },
        {
            "products": ["havana"],
            "searchWord": "havana", 
            "expected": [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
        },
        {
            "products": ["bags","baggage","banner","box","cloths"],
            "searchWord": "bags",
            "expected": [["baggage","bags","banner"],["baggage","bags","banner"],["baggage","bags"],["bags"]]
        }
    ]
    
    print("Testing Basic Functionality:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases):
        products = test_case["products"]
        searchWord = test_case["searchWord"]
        expected = test_case["expected"]
        
        result = solution.suggestedProducts(products, searchWord)
        
        print(f"Test {i+1}:")
        print(f"  Products: {products}")
        print(f"  SearchWord: '{searchWord}'")
        print(f"  Result: {result}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if result == expected else '✗'}")
        print()

def compare_different_approaches():
    """Compare performance of different solution approaches"""
    solution = Solution()
    
    products = ["mobile","mouse","moneypot","monitor","mousepad","map","mars"]
    searchWord = "mouse"
    
    approaches = [
        ("Trie with Suggestions", solution.suggestedProducts),
        ("Binary Search", solution.suggestedProductsBinarySearch),
        ("Standard Trie + DFS", solution.suggestedProductsTrieStandard),
        ("Brute Force", solution.suggestedProductsBruteForce),
        ("Optimized Binary Search", solution.suggestedProductsOptimizedBinarySearch),
    ]
    
    print("Comparing Different Approaches:")
    print("=" * 50)
    print(f"Products: {products}")
    print(f"Search Word: '{searchWord}'")
    print()
    
    results = []
    for name, method in approaches:
        result = method(products, searchWord)
        results.append(result)
        print(f"{name}:")
        for j, suggestions in enumerate(result):
            prefix = searchWord[:j+1]
            print(f"  '{prefix}': {suggestions}")
        print()
    
    # Verify all approaches give same result
    all_same = all(r == results[0] for r in results)
    print(f"All approaches consistent: {'✓' if all_same else '✗'}")

def demonstrate_edge_cases():
    """Test edge cases and corner scenarios"""
    solution = Solution()
    
    print("Testing Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        {
            "name": "No matching products",
            "products": ["cat", "dog", "bird"], 
            "searchWord": "mouse",
            "description": "Search word has no matches"
        },
        {
            "name": "Single character products",
            "products": ["a", "b", "c"], 
            "searchWord": "a",
            "description": "Very short products"
        },
        {
            "name": "Empty products list",
            "products": [], 
            "searchWord": "test",
            "description": "No products available"
        },
        {
            "name": "Single character search",
            "products": ["apple", "application", "apply"],
            "searchWord": "a", 
            "description": "Single character search"
        },
        {
            "name": "Exact match only",
            "products": ["test"], 
            "searchWord": "test",
            "description": "Only one exact match"
        },
        {
            "name": "More than 3 matches",
            "products": ["aa", "ab", "ac", "ad", "ae"],
            "searchWord": "a",
            "description": "Should return only first 3"
        }
    ]
    
    for case in edge_cases:
        result = solution.suggestedProducts(case["products"], case["searchWord"])
        print(f"{case['name']}:")
        print(f"  Description: {case['description']}")
        print(f"  Products: {case['products']}")
        print(f"  Search: '{case['searchWord']}'")
        print(f"  Result: {result}")
        print()

def analyze_performance():
    """Analyze time and space complexity of different approaches"""
    print("Performance Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Trie + Suggestions", "O(N*M + S)", "O(N*M)", "Best for multiple queries"),
        ("Binary Search", "O(N log N + S*log N)", "O(1)", "Good balance, simple"),
        ("Standard Trie", "O(N*M + S*3*M)", "O(N*M)", "Educational, not optimal"),
        ("Brute Force", "O(S*N*M)", "O(1)", "Simple but inefficient"),
        ("Optimized Binary", "O(N log N + S*log N)", "O(1)", "Best for single query"),
    ]
    
    print(f"{'Approach':<20} {'Time Complexity':<20} {'Space':<10} {'Best For'}")
    print("-" * 75)
    
    for approach, time, space, best_for in approaches:
        print(f"{approach:<20} {time:<20} {space:<10} {best_for}")
    
    print("\nWhere:")
    print("N = number of products, M = average product length, S = search word length")
    print("\nRecommendation:")
    print("- Binary Search: Best general-purpose solution")
    print("- Trie + Suggestions: Best for systems with many repeated queries")
    print("- Optimized Binary: Best for single queries with performance focus")

def demonstrate_real_world_usage():
    """Show real-world autocomplete scenarios"""
    print("\nReal-world Usage Examples:")
    print("=" * 50)
    
    # E-commerce product search
    print("1. E-commerce Product Search:")
    ecommerce_products = [
        "iphone 12", "iphone 13", "iphone case", "ipad", "ipad pro", 
        "macbook", "macbook air", "mouse", "mousepad", "monitor"
    ]
    
    solution = Solution()
    user_queries = ["ip", "iph", "mac", "mo"]
    
    for query in user_queries:
        suggestions = solution.suggestedProducts(ecommerce_products, query)
        print(f"  User types '{query}': {suggestions[-1]}")  # Show final suggestions
    
    # Search engine suggestions
    print("\n2. Search Engine Query Suggestions:")
    search_queries = [
        "python tutorial", "python programming", "python snake", 
        "javascript", "java programming", "machine learning"
    ]
    
    user_input = "py"
    suggestions = solution.suggestedProducts(search_queries, user_input)
    print(f"  User types '{user_input}': {suggestions[-1]}")
    
    # File system autocomplete
    print("\n3. File System Autocomplete:")
    file_paths = [
        "/home/user/documents", "/home/user/downloads", "/home/user/desktop",
        "/etc/config", "/var/log", "/usr/bin"
    ]
    
    user_path = "/ho"
    suggestions = solution.suggestedProducts(file_paths, user_path)
    print(f"  User types '{user_path}': {suggestions[-1]}")

def visualize_trie_building():
    """Visualize how trie with suggestions is built"""
    print("\nVisualizing Trie Construction with Suggestions:")
    print("=" * 50)
    
    products = ["cat", "car", "card", "care", "dog"]
    print(f"Building trie for products: {products}")
    print()
    
    # Build trie step by step (simplified visualization)
    root = TrieNode()
    products.sort()  # Ensure lexicographic order
    
    print("Trie construction process:")
    for product in products:
        print(f"\nInserting '{product}':")
        current = root
        prefix = ""
        
        for char in product:
            prefix += char
            if char not in current.children:
                current.children[char] = TrieNode()
                print(f"  Created node for prefix '{prefix}'")
            current = current.children[char]
            
            if len(current.suggestions) < 3:
                current.suggestions.append(product)
                print(f"  Added '{product}' to suggestions at prefix '{prefix}'")
                print(f"    Current suggestions: {current.suggestions}")

if __name__ == "__main__":
    test_basic_functionality()
    compare_different_approaches()
    demonstrate_edge_cases()
    analyze_performance()
    demonstrate_real_world_usage()
    visualize_trie_building()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Build autocomplete/search suggestion system
   - For each prefix of searchWord, return up to 3 lexicographically smallest products
   - Products must start with the current prefix
   - Return suggestions for each character typed

2. KEY INSIGHTS:

   INSIGHT 1: Prefix-based Search
   - Each character adds to prefix, narrowing search space
   - Need efficient prefix matching for large product catalogs
   - Lexicographic ordering requirement

   INSIGHT 2: Multiple Solution Approaches
   - Trie: Best for repeated queries, stores suggestions at nodes
   - Binary Search: Simple and efficient for single queries
   - Brute Force: Straightforward but inefficient

3. OPTIMAL APPROACHES:

   APPROACH 1 - Trie with Stored Suggestions (BEST for multiple queries):
   - Build trie where each node stores up to 3 best suggestions
   - O(1) suggestion retrieval per prefix
   - Higher memory usage but excellent query performance

   APPROACH 2 - Binary Search (RECOMMENDED for interviews):
   - Sort products once, use binary search for each prefix
   - Simple to implement and understand
   - Good balance of time/space complexity

   APPROACH 3 - Standard Trie + DFS:
   - Educational approach showing trie traversal
   - Less efficient but demonstrates core concepts

4. WHY BINARY SEARCH IS OFTEN BEST:
   - Simple implementation, easy to explain
   - O(N log N + S*log N) time complexity
   - O(1) extra space (very memory efficient)
   - Handles edge cases naturally

5. ALGORITHM WALKTHROUGH (Binary Search):
   - Sort products lexicographically
   - For each prefix, use binary search to find starting position
   - Take next 3 products that start with prefix
   - Handle case where no products match prefix

6. COMPLEXITY ANALYSIS:
   - Binary Search: O(N log N + S*log N) time, O(1) space
   - Trie + Suggestions: O(N*M + S) time, O(N*M) space
   - Brute Force: O(S*N*M) time, O(1) space

7. EDGE CASES:
   - No products match prefix → return empty list
   - Fewer than 3 matches → return all available
   - Empty product list → return empty lists
   - Single character search/products

8. INTERVIEW PRESENTATION:
   - Start with: "This is an autocomplete system - classic trie or binary search problem"
   - Explain lexicographic ordering requirement
   - Choose binary search for simplicity
   - Walk through example showing prefix progression
   - Mention trie approach as optimization for repeated queries

9. FOLLOW-UP QUESTIONS:
   - "How to handle millions of products?" → Discuss distributed systems, caching
   - "Real-time product updates?" → Discuss incremental updates vs rebuilding
   - "Fuzzy matching?" → Edit distance, phonetic matching
   - "Personalized suggestions?" → User history, collaborative filtering

10. WHY THIS PROBLEM IS IMPORTANT:
    - Real-world autocomplete systems (Google, Amazon, etc.)
    - Tests understanding of prefix matching algorithms
    - Multiple valid approaches with different trade-offs
    - Scales to production-level requirements

11. COMMON MISTAKES:
    - Not sorting products for lexicographic order
    - Inefficient prefix matching (scanning all products)
    - Not handling case where no products match prefix
    - Forgetting to limit to 3 suggestions

12. IMPLEMENTATION DETAILS:
    - Use bisect module for binary search in Python
    - Sort products once at beginning
    - Use startswith() for prefix checking
    - Handle edge cases gracefully

13. OPTIMIZATION OPPORTUNITIES:
    - Trie with suggestions for repeated queries
    - Caching for frequently searched prefixes
    - Parallel processing for large product catalogs
    - Prefix compression for memory efficiency

14. REAL-WORLD APPLICATIONS:
    - E-commerce search suggestions
    - Search engine autocomplete
    - IDE code completion
    - File system path completion
    - Database query suggestions

15. KEY INSIGHT TO ARTICULATE:
    "This is a classic autocomplete problem that can be solved efficiently with 
    binary search on sorted data. The key insight is that each character narrows 
    the search space, and binary search gives us O(log N) lookup for each prefix. 
    For systems with many repeated queries, a trie with pre-stored suggestions 
    would be more efficient."

16. INTERVIEW TIPS:
    - Lead with binary search approach (simple and efficient)
    - Explain why sorting is necessary
    - Show understanding of trie alternative
    - Discuss real-world scaling considerations
    - Handle edge cases in your implementation
"""
