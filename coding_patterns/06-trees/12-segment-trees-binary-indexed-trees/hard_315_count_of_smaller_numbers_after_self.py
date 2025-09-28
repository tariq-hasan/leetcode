from typing import List

class BinaryIndexedTree:
    """
    Binary Indexed Tree (Fenwick Tree) for efficient range sum queries
    Used to count elements in coordinate-compressed space
    """
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)
    
    def update(self, idx, delta=1):
        """Add delta to position idx (1-indexed)"""
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        """Get prefix sum up to idx (1-indexed)"""
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)
        return result
    
    def range_query(self, left, right):
        """Get sum in range [left, right] (1-indexed)"""
        return self.query(right) - self.query(left - 1)

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        """
        Optimal Solution - Merge Sort with Index Tracking
        
        Key insight: Use merge sort to count inversions. During merge,
        count how many elements from right array are smaller than left array elements.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        n = len(nums)
        if n == 0:
            return []
        
        # Create array of (value, original_index) pairs
        indexed_nums = [(nums[i], i) for i in range(n)]
        result = [0] * n
        
        def merge_sort(arr, temp_arr, left, right):
            """Merge sort with inversion counting"""
            if left >= right:
                return
            
            mid = (left + right) // 2
            merge_sort(arr, temp_arr, left, mid)
            merge_sort(arr, temp_arr, mid + 1, right)
            merge(arr, temp_arr, left, mid, right)
        
        def merge(arr, temp_arr, left, mid, right):
            """Merge two sorted subarrays and count inversions"""
            i, j, k = left, mid + 1, left
            
            while i <= mid and j <= right:
                if arr[i][0] <= arr[j][0]:
                    # Element from left array
                    temp_arr[k] = arr[i]
                    # Count smaller elements from right array processed so far
                    result[arr[i][1]] += (j - mid - 1)
                    i += 1
                else:
                    # Element from right array is smaller
                    temp_arr[k] = arr[j]
                    j += 1
                k += 1
            
            # Copy remaining elements from left array
            while i <= mid:
                temp_arr[k] = arr[i]
                result[arr[i][1]] += (j - mid - 1)
                i += 1
                k += 1
            
            # Copy remaining elements from right array
            while j <= right:
                temp_arr[k] = arr[j]
                j += 1
                k += 1
            
            # Copy merged result back
            for i in range(left, right + 1):
                arr[i] = temp_arr[i]
        
        temp_array = [None] * n
        merge_sort(indexed_nums, temp_array, 0, n - 1)
        return result

    def countSmallerBIT(self, nums: List[int]) -> List[int]:
        """
        Binary Indexed Tree Solution with Coordinate Compression
        
        Key insight: Compress coordinates, process from right to left,
        use BIT to count smaller elements efficiently.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        if not nums:
            return []
        
        n = len(nums)
        
        # Coordinate compression
        sorted_nums = sorted(set(nums))
        coord_map = {num: i + 1 for i, num in enumerate(sorted_nums)}
        
        bit = BinaryIndexedTree(len(sorted_nums))
        result = []
        
        # Process from right to left
        for i in range(n - 1, -1, -1):
            # Find coordinate of current number
            coord = coord_map[nums[i]]
            
            # Count smaller numbers (prefix sum up to coord-1)
            count = bit.query(coord - 1)
            result.append(count)
            
            # Add current number to BIT
            bit.update(coord)
        
        return result[::-1]  # Reverse to get correct order

    def countSmallerSegmentTree(self, nums: List[int]) -> List[int]:
        """
        Segment Tree Solution with Coordinate Compression
        
        Alternative approach using segment tree for range queries
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        if not nums:
            return []
        
        # Coordinate compression
        sorted_nums = sorted(set(nums))
        coord_map = {num: i for i, num in enumerate(sorted_nums)}
        
        class SegmentTree:
            def __init__(self, size):
                self.size = size
                self.tree = [0] * (4 * size)
            
            def update(self, node, start, end, idx):
                if start == end:
                    self.tree[node] += 1
                else:
                    mid = (start + end) // 2
                    if idx <= mid:
                        self.update(2 * node, start, mid, idx)
                    else:
                        self.update(2 * node + 1, mid + 1, end, idx)
                    self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
            
            def query(self, node, start, end, l, r):
                if r < start or end < l:
                    return 0
                if l <= start and end <= r:
                    return self.tree[node]
                mid = (start + end) // 2
                return (self.query(2 * node, start, mid, l, r) +
                        self.query(2 * node + 1, mid + 1, end, l, r))
            
            def update_point(self, idx):
                self.update(1, 0, self.size - 1, idx)
            
            def range_sum(self, l, r):
                if l > r:
                    return 0
                return self.query(1, 0, self.size - 1, l, r)
        
        st = SegmentTree(len(sorted_nums))
        result = []
        
        # Process from right to left
        for i in range(len(nums) - 1, -1, -1):
            coord = coord_map[nums[i]]
            
            # Count smaller elements (range [0, coord-1])
            count = st.range_sum(0, coord - 1)
            result.append(count)
            
            # Add current element
            st.update_point(coord)
        
        return result[::-1]

    def countSmallerBruteForce(self, nums: List[int]) -> List[int]:
        """
        Brute Force Solution (For Comparison)
        
        Simple nested loop approach
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        n = len(nums)
        result = []
        
        for i in range(n):
            count = 0
            for j in range(i + 1, n):
                if nums[j] < nums[i]:
                    count += 1
            result.append(count)
        
        return result

    def countSmallerSortedList(self, nums: List[int]) -> List[int]:
        """
        Sorted List Solution using Binary Search
        
        Maintain sorted list, use binary search for insertion and counting
        Time Complexity: O(n^2) worst case due to list insertions
        Space Complexity: O(n)
        """
        import bisect
        
        result = []
        sorted_list = []
        
        # Process from right to left
        for i in range(len(nums) - 1, -1, -1):
            # Find insertion position
            pos = bisect.bisect_left(sorted_list, nums[i])
            result.append(pos)
            
            # Insert current number
            sorted_list.insert(pos, nums[i])
        
        return result[::-1]

    def countSmallerDivideConquer(self, nums: List[int]) -> List[int]:
        """
        Pure Divide and Conquer Solution
        
        Alternative implementation focusing on divide-and-conquer approach
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        if not nums:
            return []
        
        n = len(nums)
        result = [0] * n
        indices = list(range(n))
        
        def merge_sort_count(left, right):
            if left >= right:
                return
            
            mid = (left + right) // 2
            merge_sort_count(left, mid)
            merge_sort_count(mid + 1, right)
            
            # Merge and count
            temp_indices = []
            i, j = left, mid + 1
            
            while i <= mid and j <= right:
                if nums[indices[i]] <= nums[indices[j]]:
                    # Count smaller elements from right part
                    result[indices[i]] += (j - mid - 1)
                    temp_indices.append(indices[i])
                    i += 1
                else:
                    temp_indices.append(indices[j])
                    j += 1
            
            # Add remaining elements from left part
            while i <= mid:
                result[indices[i]] += (j - mid - 1)
                temp_indices.append(indices[i])
                i += 1
            
            # Add remaining elements from right part
            while j <= right:
                temp_indices.append(indices[j])
                j += 1
            
            # Copy back
            for k, idx in enumerate(temp_indices):
                indices[left + k] = idx
        
        merge_sort_count(0, n - 1)
        return result

# Test cases and utility functions
def test_basic_functionality():
    """Test basic counting functionality"""
    solution = Solution()
    
    test_cases = [
        {
            "nums": [5, 2, 6, 1],
            "expected": [2, 1, 1, 0],
            "description": "Standard case with mixed order"
        },
        {
            "nums": [-1],
            "expected": [0],
            "description": "Single element"
        },
        {
            "nums": [-1, -1],
            "expected": [0, 0],
            "description": "Duplicate elements"
        },
        {
            "nums": [1, 2, 3, 4, 5],
            "expected": [0, 0, 0, 0, 0],
            "description": "Already sorted ascending"
        },
        {
            "nums": [5, 4, 3, 2, 1],
            "expected": [4, 3, 2, 1, 0],
            "description": "Reverse sorted"
        }
    ]
    
    print("Testing Basic Functionality:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases):
        nums = test_case["nums"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        result_merge = solution.countSmaller(nums)
        result_bit = solution.countSmallerBIT(nums)
        
        print(f"Test {i+1}: {description}")
        print(f"  Input: {nums}")
        print(f"  Merge Sort: {result_merge}")
        print(f"  BIT: {result_bit}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if result_merge == expected and result_bit == expected else '✗'}")
        print()

def compare_different_approaches():
    """Compare performance of different solution approaches"""
    solution = Solution()
    
    test_nums = [5, 2, 6, 1, 8, 3, 7]
    
    approaches = [
        ("Merge Sort", solution.countSmaller),
        ("Binary Indexed Tree", solution.countSmallerBIT),
        ("Segment Tree", solution.countSmallerSegmentTree),
        ("Brute Force", solution.countSmallerBruteForce),
        ("Divide & Conquer", solution.countSmallerDivideConquer),
    ]
    
    print("Comparing Different Approaches:")
    print("=" * 50)
    print(f"Input: {test_nums}")
    print()
    
    results = []
    for name, method in approaches:
        result = method(test_nums)
        results.append(result)
        print(f"{name}: {result}")
    
    # Verify all approaches give same result
    all_same = all(r == results[0] for r in results)
    print(f"\nAll approaches consistent: {'✓' if all_same else '✗'}")

def demonstrate_merge_sort_process():
    """Visualize merge sort counting process"""
    print("\nMerge Sort Process Visualization:")
    print("=" * 50)
    
    nums = [5, 2, 6, 1]
    print(f"Array: {nums}")
    print("Process: Count inversions during merge sort")
    print()
    
    print("Step-by-step merge sort with counting:")
    print("1. Divide: [5,2] | [6,1]")
    print("2. Divide further: [5] [2] | [6] [1]")
    print("3. Merge [5] and [2]: 2 < 5, so 5 has 1 smaller element after it")
    print("4. Merge [6] and [1]: 1 < 6, so 6 has 1 smaller element after it")
    print("5. Merge [2,5] and [1,6]: count cross-inversions")
    print("   - 2 > 1: count increases for 2 and 5")
    print("   - 5 > 1: count increases for 5")
    print("   - Final result: [2, 1, 1, 0]")

def demonstrate_bit_process():
    """Show BIT coordinate compression and processing"""
    print("\nBIT Process Visualization:")
    print("=" * 50)
    
    nums = [5, 2, 6, 1]
    print(f"Array: {nums}")
    print()
    
    # Coordinate compression
    sorted_nums = sorted(set(nums))
    coord_map = {num: i + 1 for i, num in enumerate(sorted_nums)}
    
    print("Coordinate compression:")
    print(f"Unique sorted: {sorted_nums}")
    print(f"Coordinate map: {coord_map}")
    print()
    
    print("Process from right to left:")
    bit = BinaryIndexedTree(len(sorted_nums))
    
    for i in range(len(nums) - 1, -1, -1):
        coord = coord_map[nums[i]]
        count = bit.query(coord - 1)
        print(f"Index {i}, value {nums[i]}, coord {coord}: count = {count}")
        bit.update(coord)
        print(f"  BIT after update: {bit.tree[1:len(sorted_nums)+1]}")

def analyze_complexity():
    """Analyze time and space complexity of different approaches"""
    print("\nComplexity Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Merge Sort", "O(n log n)", "O(n)", "Optimal, most intuitive"),
        ("Binary Indexed Tree", "O(n log n)", "O(n)", "Efficient, requires coordinate compression"),
        ("Segment Tree", "O(n log n)", "O(n)", "Alternative to BIT, more memory"),
        ("Brute Force", "O(n²)", "O(1)", "Simple but inefficient"),
        ("Divide & Conquer", "O(n log n)", "O(n)", "Pure D&C approach"),
    ]
    
    print(f"{'Approach':<20} {'Time':<12} {'Space':<8} {'Notes'}")
    print("-" * 65)
    
    for approach, time, space, notes in approaches:
        print(f"{approach:<20} {time:<12} {space:<8} {notes}")
    
    print("\nRecommendation:")
    print("- Merge Sort: Best for interviews (intuitive inversion counting)")
    print("- BIT: Good for follow-up optimization discussions")
    print("- Segment Tree: Alternative data structure approach")

def test_edge_cases():
    """Test edge cases and corner scenarios"""
    solution = Solution()
    
    print("\nTesting Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        {
            "name": "Empty array",
            "nums": [],
            "expected": []
        },
        {
            "name": "Single element",
            "nums": [1],
            "expected": [0]
        },
        {
            "name": "All same elements",
            "nums": [3, 3, 3, 3],
            "expected": [0, 0, 0, 0]
        },
        {
            "name": "Negative numbers",
            "nums": [-1, -5, 3, -2],
            "expected": [1, 0, 2, 0]
        },
        {
            "name": "Large numbers",
            "nums": [100, 50, 200, 25],
            "expected": [2, 1, 1, 0]
        }
    ]
    
    for case in edge_cases:
        result = solution.countSmaller(case["nums"])
        expected = case["expected"]
        
        print(f"{case['name']}:")
        print(f"  Input: {case['nums']}")
        print(f"  Result: {result}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if result == expected else '✗'}")
        print()

def demonstrate_real_world_applications():
    """Show real-world applications of this problem"""
    print("Real-world Applications:")
    print("=" * 50)
    
    applications = [
        {
            "domain": "Financial Trading",
            "use_case": "Order book analysis",
            "example": "Count trades at lower prices after each trade"
        },
        {
            "domain": "E-commerce",
            "use_case": "Price comparison tracking",
            "example": "Track how many cheaper products appear after each listing"
        },
        {
            "domain": "Gaming/Sports",
            "use_case": "Ranking system analysis",
            "example": "Count players with lower scores appearing later"
        },
        {
            "domain": "Data Analytics",
            "use_case": "Time series trend analysis",
            "example": "Count future data points below current threshold"
        },
        {
            "domain": "Algorithm Competitions",
            "use_case": "Inversion counting problems",
            "example": "Measure disorder in sequences"
        }
    ]
    
    for app in applications:
        print(f"{app['domain']}:")
        print(f"  Use case: {app['use_case']}")
        print(f"  Example: {app['example']}")
        print()

def performance_simulation():
    """Simulate performance on different input patterns"""
    solution = Solution()
    
    print("Performance Simulation on Different Patterns:")
    print("=" * 50)
    
    patterns = [
        ("Random", [3, 1, 4, 1, 5, 9, 2, 6]),
        ("Sorted", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("Reverse", [8, 7, 6, 5, 4, 3, 2, 1]),
        ("Duplicates", [3, 3, 1, 1, 5, 5, 2, 2])
    ]
    
    for pattern_name, nums in patterns:
        result = solution.countSmaller(nums)
        inversion_count = sum(result)
        
        print(f"{pattern_name} pattern: {nums}")
        print(f"  Result: {result}")
        print(f"  Total inversions: {inversion_count}")
        print()

if __name__ == "__main__":
    test_basic_functionality()
    compare_different_approaches()
    demonstrate_merge_sort_process()
    demonstrate_bit_process()
    analyze_complexity()
    test_edge_cases()
    demonstrate_real_world_applications()
    performance_simulation()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - For each element, count how many smaller elements appear after it
   - This is essentially counting inversions for each position
   - Need efficient algorithm for large arrays
   - Output array has same length as input

2. KEY INSIGHTS:

   INSIGHT 1: Inversion Counting Problem
   - Each element needs to count inversions with elements to its right
   - Classic problem with multiple optimal solutions
   - Requires O(n log n) for efficiency

   INSIGHT 2: Multiple Optimal Approaches
   - Merge sort with inversion counting
   - Coordinate compression + BIT/Segment Tree
   - All achieve O(n log n) time complexity

3. OPTIMAL APPROACHES:

   APPROACH 1 - Merge Sort (RECOMMENDED):
   - Most intuitive for inversion counting
   - Natural divide-and-conquer structure
   - Count cross-inversions during merge step

   APPROACH 2 - BIT with Coordinate Compression:
   - Process from right to left
   - Use BIT to count elements smaller than current
   - Requires coordinate compression for large ranges

   APPROACH 3 - Segment Tree:
   - Alternative to BIT with similar performance
   - More memory but easier to understand for some

4. WHY MERGE SORT IS PREFERRED:
   - Direct application of inversion counting
   - No coordinate compression needed
   - Natural recursive structure
   - Easier to explain and implement correctly

5. ALGORITHM WALKTHROUGH (Merge Sort):
   - Track original indices during sorting
   - During merge, count how many elements from right array are smaller
   - These counts contribute to left array elements' results
   - Maintain result array indexed by original positions

6. COMPLEXITY ANALYSIS:
   - Time: O(n log n) for optimal approaches
   - Space: O(n) for auxiliary arrays and recursion
   - Much better than O(n²) brute force

7. COORDINATE COMPRESSION (BIT/Segment Tree):
   - Map values to smaller coordinate space
   - Process from right to left
   - Query smaller coordinates, then insert current coordinate
   - Requires sorting unique values first

8. EDGE CASES:
   - Empty array → empty result
   - Single element → [0]
   - All same elements → all zeros
   - Already sorted → all zeros
   - Reverse sorted → maximum inversions

9. INTERVIEW PRESENTATION:
   - Start with: "This is an inversion counting problem"
   - Present merge sort approach as primary
   - Walk through merge process with example
   - Mention BIT approach as optimization
   - Discuss complexity improvements over brute force

10. FOLLOW-UP QUESTIONS:
    - "Count larger numbers after self?" → Similar with slight modification
    - "Range of values is huge?" → Coordinate compression is essential
    - "Memory optimization?" → In-place merge sort variants
    - "Parallel processing?" → Parallel merge sort approaches

11. WHY THIS PROBLEM IS CHALLENGING:
    - Requires understanding of inversion counting
    - Multiple optimal approaches with trade-offs
    - Coordinate compression adds complexity
    - Tests advanced data structure knowledge

12. COMMON MISTAKES:
    - Using O(n²) brute force without optimization
    - Incorrect inversion counting during merge
    - Not handling original indices properly
    - Coordinate compression off-by-one errors

13. IMPLEMENTATION DETAILS:
    - Track original indices with (value, index) pairs
    - Count inversions during merge step carefully
    - For BIT: process right to left, query then update
    - Handle empty arrays and single elements

14. OPTIMIZATION OPPORTUNITIES:
    - In-place merge sort to reduce space
    - Iterative merge sort to avoid recursion overhead
    - Parallel merge sort for very large arrays
    - Early termination optimizations

15. KEY INSIGHT TO ARTICULATE:
    "This problem is fundamentally about counting inversions efficiently. 
    The merge sort approach is most intuitive because it naturally counts 
    cross-inversions during the merge step. By tracking original indices, 
    we can attribute these inversion counts to the correct positions in 
    the result array, achieving optimal O(n log n) complexity."

16. INTERVIEW TIPS:
    - Lead with merge sort approach (most intuitive)
    - Draw example showing merge process
    - Explain how original indices are maintained
    - Show inversion counting during merge step
    - Mention BIT approach as advanced alternative
    - Discuss coordinate compression if values are large
"""
