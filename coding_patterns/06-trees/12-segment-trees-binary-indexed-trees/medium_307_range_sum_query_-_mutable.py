from typing import List

class NumArraySegmentTree:
    """
    Optimal Solution - Segment Tree Implementation
    
    Key insight: Use segment tree for O(log n) updates and queries.
    Each node stores sum of its range, enabling efficient range operations.
    
    Time Complexity:
    - __init__: O(n)
    - update: O(log n)
    - sumRange: O(log n)
    
    Space Complexity: O(n) for tree storage
    """
    
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        if self.n == 0:
            return
        
        # Segment tree array - tree[1] is root
        # Left child of node i is at 2*i, right child at 2*i+1
        self.tree = [0] * (4 * self.n)  # 4*n is safe upper bound
        self.build(nums, 1, 0, self.n - 1)
    
    def build(self, nums, node, start, end):
        """Build segment tree recursively"""
        if start == end:
            # Leaf node
            self.tree[node] = nums[start]
        else:
            mid = (start + end) // 2
            # Build left and right subtrees
            self.build(nums, 2 * node, start, mid)
            self.build(nums, 2 * node + 1, mid + 1, end)
            # Internal node stores sum of children
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def update(self, index: int, val: int) -> None:
        """Update value at index"""
        if self.n == 0:
            return
        self._update(1, 0, self.n - 1, index, val)
    
    def _update(self, node, start, end, idx, val):
        """Helper for recursive update"""
        if start == end:
            # Leaf node - update value
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                # Update left subtree
                self._update(2 * node, start, mid, idx, val)
            else:
                # Update right subtree
                self._update(2 * node + 1, mid + 1, end, idx, val)
            
            # Update current node
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def sumRange(self, left: int, right: int) -> int:
        """Query sum of range [left, right]"""
        if self.n == 0:
            return 0
        return self._query(1, 0, self.n - 1, left, right)
    
    def _query(self, node, start, end, l, r):
        """Helper for recursive range query"""
        if r < start or end < l:
            # Range completely outside
            return 0
        
        if l <= start and end <= r:
            # Range completely inside
            return self.tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, l, r)
        right_sum = self._query(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum

class NumArrayBIT:
    """
    Binary Indexed Tree (Fenwick Tree) Solution
    
    Key insight: Use BIT for efficient prefix sum queries and updates.
    More space-efficient than segment tree, slightly trickier implementation.
    
    Time Complexity:
    - __init__: O(n log n)
    - update: O(log n)  
    - sumRange: O(log n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        if self.n == 0:
            return
            
        self.nums = nums[:]  # Keep original array
        self.bit = [0] * (self.n + 1)  # BIT is 1-indexed
        
        # Build BIT
        for i in range(self.n):
            self._add(i + 1, nums[i])
    
    def _add(self, i, delta):
        """Add delta to position i in BIT (1-indexed)"""
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)  # Add last set bit
    
    def _prefix_sum(self, i):
        """Get prefix sum up to position i (1-indexed)"""
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & (-i)  # Remove last set bit
        return result
    
    def update(self, index: int, val: int) -> None:
        """Update value at index"""
        if self.n == 0:
            return
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)
    
    def sumRange(self, left: int, right: int) -> int:
        """Query sum of range [left, right]"""
        if self.n == 0:
            return 0
        return self._prefix_sum(right + 1) - self._prefix_sum(left)

class NumArraySqrtDecomposition:
    """
    Square Root Decomposition Solution
    
    Key insight: Divide array into sqrt(n) blocks, precompute block sums.
    Balance between array and segment tree approaches.
    
    Time Complexity:
    - __init__: O(n)
    - update: O(1)
    - sumRange: O(sqrt(n))
    
    Space Complexity: O(sqrt(n)) for block sums
    """
    
    def __init__(self, nums: List[int]):
        self.nums = nums[:]
        self.n = len(nums)
        if self.n == 0:
            return
            
        import math
        self.block_size = int(math.sqrt(self.n)) + 1
        self.block_count = (self.n + self.block_size - 1) // self.block_size
        self.blocks = [0] * self.block_count
        
        # Precompute block sums
        for i in range(self.n):
            self.blocks[i // self.block_size] += nums[i]
    
    def update(self, index: int, val: int) -> None:
        """Update value at index"""
        if self.n == 0:
            return
        block_idx = index // self.block_size
        self.blocks[block_idx] += val - self.nums[index]
        self.nums[index] = val
    
    def sumRange(self, left: int, right: int) -> int:
        """Query sum of range [left, right]"""
        if self.n == 0:
            return 0
            
        result = 0
        left_block = left // self.block_size
        right_block = right // self.block_size
        
        if left_block == right_block:
            # Range within single block
            for i in range(left, right + 1):
                result += self.nums[i]
        else:
            # Range spans multiple blocks
            
            # Sum partial left block
            for i in range(left, (left_block + 1) * self.block_size):
                if i < self.n:
                    result += self.nums[i]
            
            # Sum complete middle blocks
            for block in range(left_block + 1, right_block):
                result += self.blocks[block]
            
            # Sum partial right block
            for i in range(right_block * self.block_size, right + 1):
                if i < self.n:
                    result += self.nums[i]
        
        return result

class NumArraySimple:
    """
    Simple Array Solution (Baseline for Comparison)
    
    Straightforward implementation without optimization.
    Good for small datasets or when updates are rare.
    
    Time Complexity:
    - __init__: O(n)
    - update: O(1)
    - sumRange: O(n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, nums: List[int]):
        self.nums = nums[:]
    
    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
    
    def sumRange(self, left: int, right: int) -> int:
        return sum(self.nums[left:right+1])

class NumArrayPrefixSum:
    """
    Prefix Sum Solution (Good for Query-Heavy Workloads)
    
    Precompute prefix sums, rebuild on updates.
    Excellent for many queries, few updates.
    
    Time Complexity:
    - __init__: O(n)
    - update: O(n) - needs to rebuild prefix sums
    - sumRange: O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, nums: List[int]):
        self.nums = nums[:]
        self._build_prefix()
    
    def _build_prefix(self):
        """Build prefix sum array"""
        self.n = len(self.nums)
        if self.n == 0:
            return
        self.prefix = [0] * (self.n + 1)
        for i in range(self.n):
            self.prefix[i + 1] = self.prefix[i] + self.nums[i]
    
    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        self._build_prefix()  # Rebuild prefix sums
    
    def sumRange(self, left: int, right: int) -> int:
        if self.n == 0:
            return 0
        return self.prefix[right + 1] - self.prefix[left]

class NumArrayLazy:
    """
    Lazy Propagation Segment Tree (Advanced)
    
    Optimized for range updates (not needed for this problem but shows advanced knowledge)
    Includes range update capability for educational purposes.
    
    Time Complexity: O(log n) for all operations
    Space Complexity: O(n)
    """
    
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        if self.n == 0:
            return
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(nums, 1, 0, self.n - 1)
    
    def build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
        else:
            mid = (start + end) // 2
            self.build(nums, 2 * node, start, mid)
            self.build(nums, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def push(self, node, start, end):
        """Push lazy updates down"""
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0
    
    def update(self, index: int, val: int) -> None:
        # Convert point update to range update of size 1
        self.range_update(index, index, val - self.point_query(index))
    
    def point_query(self, index):
        """Get value at specific index"""
        return self._point_query(1, 0, self.n - 1, index)
    
    def _point_query(self, node, start, end, idx):
        self.push(node, start, end)
        if start == end:
            return self.tree[node]
        mid = (start + end) // 2
        if idx <= mid:
            return self._point_query(2 * node, start, mid, idx)
        else:
            return self._point_query(2 * node + 1, mid + 1, end, idx)
    
    def range_update(self, l, r, val):
        """Update range [l, r] by adding val"""
        self._range_update(1, 0, self.n - 1, l, r, val)
    
    def _range_update(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if start > r or end < l:
            return
        if start >= l and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self._range_update(2 * node, start, mid, l, r, val)
        self._range_update(2 * node + 1, mid + 1, end, l, r, val)
        
        self.push(2 * node, start, mid)
        self.push(2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def sumRange(self, left: int, right: int) -> int:
        if self.n == 0:
            return 0
        return self._query(1, 0, self.n - 1, left, right)
    
    def _query(self, node, start, end, l, r):
        if start > r or end < l:
            return 0
        self.push(node, start, end)
        if start >= l and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self._query(2 * node, start, mid, l, r) + 
                self._query(2 * node + 1, mid + 1, end, l, r))

# Test cases and utility functions
def test_basic_functionality():
    """Test basic update and query operations"""
    print("Testing Basic Functionality:")
    print("=" * 50)
    
    test_array = [1, 3, 5, 7, 9, 11]
    
    implementations = [
        ("Segment Tree", NumArraySegmentTree),
        ("Binary Indexed Tree", NumArrayBIT),
        ("Square Root Decomp", NumArraySqrtDecomposition),
        ("Simple Array", NumArraySimple),
    ]
    
    print(f"Initial array: {test_array}")
    print()
    
    for name, implementation in implementations:
        print(f"{name}:")
        num_array = implementation(test_array)
        
        # Test queries
        queries = [(0, 2), (2, 5), (0, 5), (1, 3)]
        for left, right in queries:
            result = num_array.sumRange(left, right)
            expected = sum(test_array[left:right+1])
            print(f"  sumRange({left}, {right}): {result} (expected: {expected})")
        
        # Test update
        num_array.update(1, 10)
        result = num_array.sumRange(0, 2)
        expected = test_array[0] + 10 + test_array[2]  # 1 + 10 + 5 = 16
        print(f"  After update(1, 10), sumRange(0, 2): {result} (expected: {expected})")
        print()

def performance_comparison():
    """Compare performance characteristics of different approaches"""
    print("Performance Comparison:")
    print("=" * 50)
    
    approaches = [
        ("Segment Tree", "O(log n)", "O(log n)", "O(n)", "Balanced, most versatile"),
        ("Binary Indexed Tree", "O(log n)", "O(log n)", "O(n)", "Space efficient, faster constants"),
        ("Sqrt Decomposition", "O(1)", "O(√n)", "O(√n)", "Simple, good for teaching"),
        ("Simple Array", "O(1)", "O(n)", "O(n)", "Simplest, good for small data"),
        ("Prefix Sum", "O(n)", "O(1)", "O(n)", "Great for query-heavy workloads"),
    ]
    
    print(f"{'Approach':<20} {'Update':<10} {'Query':<10} {'Space':<8} {'Notes'}")
    print("-" * 75)
    
    for approach, update, query, space, notes in approaches:
        print(f"{approach:<20} {update:<10} {query:<10} {space:<8} {notes}")
    
    print("\nRecommendations:")
    print("- Segment Tree: Best general-purpose choice")
    print("- BIT: When space is critical and only sum queries needed")
    print("- Sqrt Decomp: Good balance for moderate-sized arrays")
    print("- Prefix Sum: When updates are rare, queries frequent")

def demonstrate_segment_tree_build():
    """Visualize segment tree construction"""
    print("\nSegment Tree Construction Visualization:")
    print("=" * 50)
    
    nums = [1, 3, 5, 7, 9, 11]
    print(f"Array: {nums}")
    print()
    
    print("Segment Tree Structure (sum of ranges):")
    print("                  36[0-5]")
    print("               /           \\")
    print("          9[0-2]             27[3-5]")
    print("         /     \\           /       \\")
    print("    4[0-1]     5[2]   16[3-4]     11[5]")
    print("   /     \\              /    \\")
    print("1[0]     3[1]       7[3]      9[4]")
    print()
    
    print("Tree array representation (1-indexed):")
    st = NumArraySegmentTree(nums)
    print("Index:  1   2   3   4   5   6   7   8   9  10  11  12")
    print("Value:", end="")
    for i in range(1, 13):
        print(f"{st.tree[i]:4}", end="")
    print()
    print()
    
    print("Query process for sumRange(1, 4):")
    print("1. Start at root [0-5]")
    print("2. Partial overlap, go to children")
    print("3. Left child [0-2]: partial overlap, go deeper")
    print("4. Right child [3-5]: partial overlap, go deeper")
    print("5. Collect sums: 3 + 5 + 7 + 9 = 24")

def demonstrate_bit_operations():
    """Show BIT index manipulation operations"""
    print("\nBinary Indexed Tree Operations:")
    print("=" * 50)
    
    print("BIT index operations (key insight):")
    print("- To go to parent: i += i & (-i)")
    print("- To go to next: i -= i & (-i)")
    print()
    
    print("Example with index 6 (binary: 110):")
    i = 6
    print(f"Starting index: {i} (binary: {bin(i)})")
    
    print("\nGoing up (update path):")
    path = []
    temp_i = i
    for _ in range(4):  # Show a few steps
        if temp_i > 8:  # Limit for demonstration
            break
        path.append(temp_i)
        temp_i += temp_i & (-temp_i)
    print(f"Update path: {path}")
    
    print("\nGoing down (query path):")
    path = []
    temp_i = i
    for _ in range(4):
        if temp_i <= 0:
            break
        path.append(temp_i)
        temp_i -= temp_i & (-temp_i)
    print(f"Query path: {path}")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\nTesting Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        {
            "name": "Single element",
            "array": [42],
            "operations": [("sumRange", 0, 0), ("update", 0, 100), ("sumRange", 0, 0)]
        },
        {
            "name": "Two elements",
            "array": [1, 2],
            "operations": [("sumRange", 0, 1), ("update", 0, 5), ("sumRange", 0, 1)]
        },
        {
            "name": "All zeros",
            "array": [0, 0, 0, 0],
            "operations": [("sumRange", 0, 3), ("update", 2, 7), ("sumRange", 1, 3)]
        },
        {
            "name": "Negative numbers",
            "array": [-1, -2, -3],
            "operations": [("sumRange", 0, 2), ("update", 1, 5), ("sumRange", 0, 2)]
        }
    ]
    
    for case in edge_cases:
        print(f"{case['name']}:")
        print(f"  Array: {case['array']}")
        
        # Test with segment tree
        num_array = NumArraySegmentTree(case["array"])
        
        for op in case["operations"]:
            if op[0] == "sumRange":
                result = num_array.sumRange(op[1], op[2])
                print(f"  {op[0]}({op[1]}, {op[2]}): {result}")
            else:  # update
                num_array.update(op[1], op[2])
                print(f"  {op[0]}({op[1]}, {op[2]}): updated")
        print()

def analyze_real_world_usage():
    """Discuss real-world applications"""
    print("Real-world Applications:")
    print("=" * 50)
    
    applications = [
        {
            "domain": "Database Systems",
            "use_case": "Range aggregation queries",
            "example": "SUM(salary) WHERE department_id BETWEEN 10 AND 20"
        },
        {
            "domain": "Financial Systems",
            "use_case": "Portfolio value calculations",
            "example": "Calculate total value of stocks in price range"
        },
        {
            "domain": "Game Development",
            "use_case": "Leaderboard range queries",
            "example": "Find sum of scores for players ranked 100-200"
        },
        {
            "domain": "Time Series Analytics",
            "use_case": "Window aggregations",
            "example": "Calculate moving averages over time windows"
        },
        {
            "domain": "Computational Geometry",
            "use_case": "Range tree queries",
            "example": "Find sum of values in 2D rectangular regions"
        }
    ]
    
    for app in applications:
        print(f"{app['domain']}:")
        print(f"  Use case: {app['use_case']}")
        print(f"  Example: {app['example']}")
        print()
    
    print("Choosing the Right Data Structure:")
    print("- High update frequency: Segment Tree or BIT")
    print("- Query-heavy workload: Prefix Sum Array")
    print("- Memory constraints: BIT > Segment Tree")
    print("- Simplicity required: Square Root Decomposition")
    print("- Need range updates: Lazy Propagation Segment Tree")

if __name__ == "__main__":
    test_basic_functionality()
    performance_comparison()
    demonstrate_segment_tree_build()
    demonstrate_bit_operations()
    test_edge_cases()
    analyze_real_world_usage()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Need data structure supporting both point updates and range sum queries
   - Multiple operations with efficiency requirements
   - Classic trade-off between query and update performance
   - Must handle dynamic array modifications

2. KEY INSIGHTS:

   INSIGHT 1: Multiple Valid Approaches
   - Simple array: O(1) update, O(n) query
   - Prefix sum: O(n) update, O(1) query  
   - Advanced structures: O(log n) for both operations

   INSIGHT 2: Segment Tree is Optimal
   - Balanced O(log n) complexity for both operations
   - Natural tree structure for range operations
   - Most versatile for extensions (range updates, min/max, etc.)

3. OPTIMAL APPROACH - SEGMENT TREE:
   - Build tree with internal nodes storing range sums
   - Update: recursively update path from leaf to root
   - Query: recursively combine overlapping ranges
   - O(log n) for both operations, O(n) space

4. ALTERNATIVE - BINARY INDEXED TREE:
   - More space-efficient than segment tree
   - Clever bit manipulation for parent/child navigation
   - Slightly better constants, but less intuitive
   - Perfect for sum-only queries

5. ALGORITHM WALKTHROUGH (Segment Tree):
   - Build: recursively construct tree with range sums
   - Update: find leaf node, update ancestors
   - Query: combine results from overlapping segments

6. COMPLEXITY ANALYSIS:
   - Segment Tree: O(log n) update/query, O(n) space
   - BIT: O(log n) update/query, O(n) space, better constants
   - Sqrt Decomposition: O(1) update, O(√n) query

7. EDGE CASES:
   - Single element array
   - Empty ranges (though problem guarantees valid ranges)
   - Negative numbers in array
   - Updates to same index multiple times

8. INTERVIEW PRESENTATION:
   - Start with: "This is a classic range query problem"
   - Present trade-offs: simple vs optimal approaches
   - Choose segment tree for balanced complexity
   - Walk through tree construction and operations
   - Mention BIT as space-efficient alternative

9. FOLLOW-UP QUESTIONS:
   - "What about range updates?" → Lazy propagation
   - "Memory constraints?" → BIT or sqrt decomposition
   - "Other operations (min, max)?" → Segment tree easily extends
   - "2D version?" → 2D segment tree or range tree

10. WHY SEGMENT TREE IS PREFERRED:
    - Optimal O(log n) complexity for both operations
    - Easy to extend to other operations
    - Intuitive recursive structure
    - Industry standard for range query problems

11. COMMON MISTAKES:
    - Using simple array without recognizing efficiency need
    - Incorrect segment tree indexing (0-based vs 1-based)
    - Not handling tree boundaries correctly
    - Forgetting to update parent nodes during updates

12. IMPLEMENTATION DETAILS:
    - Use 1-based indexing for cleaner parent-child relationships
    - Allocate 4*n space for safety (tight bound is 2*n-1)
    - Recursive build, update, and query functions
    - Proper range boundary checking

13. OPTIMIZATION OPPORTUNITIES:
    - Iterative vs recursive implementation
    - Memory layout optimization for cache efficiency  
    - Lazy propagation for range updates
    - Persistent segment trees for version control

14. KEY INSIGHT TO ARTICULATE:
    "The key insight is recognizing this as a dynamic range query problem
    that requires balancing update and query performance. A segment tree
    provides optimal O(log n) complexity for both operations by organizing
    the data in a tree structure where each node represents the aggregate
    of a contiguous range, enabling efficient recursive updates and queries."

15. INTERVIEW TIPS:
    - Emphasize the complexity trade-offs early
    - Draw the segment tree structure for clarity
    - Show how updates propagate up the tree
    - Explain how queries combine partial results
    - Mention BIT as an advanced alternative
    - Discuss when to use simpler approaches
"""
