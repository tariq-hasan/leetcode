"""
LeetCode 300: Longest Increasing Subsequence

Problem: Given an integer array nums, return the length of the longest strictly increasing subsequence.

This is a classic problem with multiple solutions of different time complexities.
Essential for understanding DP optimization techniques.
"""

def lengthOfLIS_dp_basic(nums):
    """
    Approach 1: Basic Dynamic Programming
    
    Time Complexity: O(n²)
    Space Complexity: O(n)
    
    Strategy: dp[i] = length of LIS ending at index i
    For each position, check all previous positions with smaller values
    
    Best for: Understanding the DP concept, easy to explain
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n  # Each element forms a subsequence of length 1
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def lengthOfLIS_binary_search(nums):
    """
    Approach 2: Binary Search + Greedy (Patience Sorting)
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Strategy: Maintain array 'tails' where tails[i] is the smallest tail 
    of all increasing subsequences of length i+1
    
    Best for: Optimal solution, shows advanced algorithmic thinking
    """
    if not nums:
        return 0
    
    # tails[i] = smallest ending element of all subsequences of length i+1
    tails = []
    
    for num in nums:
        # Binary search for the position to insert/replace
        left, right = 0, len(tails)
        
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        # If num is larger than all elements in tails, append it
        if left == len(tails):
            tails.append(num)
        else:
            # Replace the first element that is >= num
            tails[left] = num
    
    return len(tails)


def lengthOfLIS_binary_search_builtin(nums):
    """
    Approach 3: Binary Search with Built-in bisect
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Same strategy as above but using Python's bisect module
    More concise but shows less implementation detail
    """
    if not nums:
        return 0
    
    import bisect
    tails = []
    
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)


def lengthOfLIS_with_sequence(nums):
    """
    Approach 4: Binary Search + Reconstruct Actual Sequence
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Extension: Returns both length and one possible LIS
    Great for follow-up questions about the actual subsequence
    """
    if not nums:
        return 0, []
    
    n = len(nums)
    tails = []
    # Store the index in original array for each position in tails
    tail_indices = []
    # Store the previous index for reconstruction
    prev_indices = [-1] * n
    # Store which tail position each element belongs to
    positions = [0] * n
    
    for i, num in enumerate(nums):
        # Binary search for insertion position
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        # Update tails and tracking arrays
        if left == len(tails):
            tails.append(num)
            tail_indices.append(i)
        else:
            tails[left] = num
            tail_indices[left] = i
        
        positions[i] = left
        if left > 0:
            prev_indices[i] = tail_indices[left - 1]
    
    # Reconstruct the sequence
    length = len(tails)
    sequence = []
    current = tail_indices[length - 1]
    
    while current != -1:
        sequence.append(nums[current])
        current = prev_indices[current]
    
    sequence.reverse()
    return length, sequence


def lengthOfLIS_segment_tree(nums):
    """
    Approach 5: Coordinate Compression + Segment Tree
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Advanced approach using coordinate compression and segment tree
    Good for showing knowledge of advanced data structures
    """
    if not nums:
        return 0
    
    # Coordinate compression
    sorted_unique = sorted(set(nums))
    coord_map = {v: i for i, v in enumerate(sorted_unique)}
    
    # Segment tree for range maximum query
    class SegmentTree:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (4 * n)
        
        def update(self, node, start, end, idx, val):
            if start == end:
                self.tree[node] = max(self.tree[node], val)
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    self.update(2 * node, start, mid, idx, val)
                else:
                    self.update(2 * node + 1, mid + 1, end, idx, val)
                self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])
        
        def query(self, node, start, end, l, r):
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return max(self.query(2 * node, start, mid, l, r),
                      self.query(2 * node + 1, mid + 1, end, l, r))
    
    n = len(sorted_unique)
    seg_tree = SegmentTree(n)
    max_length = 0
    
    for num in nums:
        coord = coord_map[num]
        # Query for LIS length ending with values < num
        current_length = seg_tree.query(1, 0, n - 1, 0, coord - 1) + 1
        # Update segment tree
        seg_tree.update(1, 0, n - 1, coord, current_length)
        max_length = max(max_length, current_length)
    
    return max_length


# Test cases
def test_solutions():
    test_cases = [
        {
            "nums": [10, 9, 2, 5, 3, 7, 101, 18],
            "expected": 4  # [2, 3, 7, 18] or [2, 3, 7, 101]
        },
        {
            "nums": [0, 1, 0, 3, 2, 3],
            "expected": 4  # [0, 1, 2, 3]
        },
        {
            "nums": [7, 7, 7, 7, 7, 7, 7],
            "expected": 1  # [7]
        },
        {
            "nums": [1, 3, 6, 7, 9, 4, 10, 5, 6],
            "expected": 6  # [1, 3, 4, 5, 6, 10] (one possibility)
        },
        {
            "nums": [],
            "expected": 0
        },
        {
            "nums": [1],
            "expected": 1
        },
        {
            "nums": [4, 3, 2, 1],
            "expected": 1  # Any single element
        }
    ]
    
    solutions = [
        ("Basic DP", lengthOfLIS_dp_basic),
        ("Binary Search", lengthOfLIS_binary_search),
        ("Binary Search (Built-in)", lengthOfLIS_binary_search_builtin),
        ("Segment Tree", lengthOfLIS_segment_tree),
    ]
    
    for i, test in enumerate(test_cases):
        print(f"Test Case {i + 1}: {test['nums']}")
        print(f"Expected Length: {test['expected']}")
        
        for name, solution in solutions:
            result = solution(test['nums'][:])  # Pass copy to avoid modification
            is_correct = result == test['expected']
            print(f"{name:20}: {result} {'✓' if is_correct else '✗'}")
        
        # Test sequence reconstruction
        if test['nums']:
            length, sequence = lengthOfLIS_with_sequence(test['nums'][:])
            is_increasing = all(sequence[i] < sequence[i+1] for i in range(len(sequence)-1))
            print(f"{'With Sequence':20}: Length {length}, Sequence {sequence}")
            print(f"{'':20}  Valid: {'✓' if length == test['expected'] and is_increasing else '✗'}")
        
        print("-" * 70)


def demonstrate_algorithms():
    """Demonstrate how different algorithms work step by step"""
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print("Algorithm Demonstrations:")
    print("=" * 50)
    print(f"Input: {nums}")
    print()
    
    # Basic DP demonstration
    print("1. Basic DP Step-by-Step:")
    n = len(nums)
    dp = [1] * n
    print(f"   Initial dp: {dp}")
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                old_val = dp[i]
                dp[i] = max(dp[i], dp[j] + 1)
                if dp[i] != old_val:
                    print(f"   dp[{i}] updated: {old_val} -> {dp[i]} (nums[{j}]={nums[j]} < nums[{i}]={nums[i]})")
    
    print(f"   Final dp: {dp}")
    print(f"   Result: {max(dp)}")
    print()
    
    # Binary search demonstration
    print("2. Binary Search Step-by-Step:")
    tails = []
    print("   Processing each element:")
    
    for i, num in enumerate(nums):
        import bisect
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            tails.append(num)
            print(f"   nums[{i}]={num}: Append to tails -> {tails}")
        else:
            old_val = tails[pos]
            tails[pos] = num
            print(f"   nums[{i}]={num}: Replace tails[{pos}]={old_val} -> {tails}")
    
    print(f"   Final tails: {tails}")
    print(f"   Result: {len(tails)}")


if __name__ == "__main__":
    test_solutions()
    print("\n")
    demonstrate_algorithms()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Subsequence vs Subarray: Elements don't need to be contiguous
   - Strictly increasing: nums[i] < nums[j] for i < j in subsequence
   - Return LENGTH, not the actual subsequence (unless asked)

2. APPROACH PROGRESSION (Show algorithmic maturity):
   
   Step 1: Basic DP - O(n²) 
   - Easy to understand and explain
   - Good starting point to show DP thinking
   - dp[i] = length of LIS ending at index i
   
   Step 2: Optimized DP with Binary Search - O(n log n)
   - Show optimization skills
   - More complex but optimal
   - Key insight: maintain "tails" array

3. KEY INSIGHTS FOR BINARY SEARCH APPROACH:
   - tails[i] = smallest ending element of all LIS of length i+1
   - For each new element, find its position using binary search
   - Either extend the LIS or improve an existing length

4. COMMON INTERVIEW FLOW:
   a) Start with basic DP (shows you understand the problem)
   b) Code it cleanly
   c) Analyze time/space complexity
   d) Ask "Can we optimize this?"
   e) Present binary search solution
   f) Handle follow-up questions

5. FOLLOW-UP QUESTIONS:
   - "Can you return the actual LIS?" → Use reconstruction technique
   - "What if we want all possible LIS?" → More complex DP with backtracking
   - "What about longest non-decreasing subsequence?" → Change < to <=
   - "Memory optimization?" → Can optimize basic DP to O(1) space in some cases

6. EDGE CASES:
   - Empty array → return 0
   - Single element → return 1
   - All elements equal → return 1
   - Strictly decreasing → return 1
   - Already sorted → return n

7. VARIANTS TO MENTION:
   - Longest Decreasing Subsequence
   - Longest Bitonic Subsequence
   - Russian Doll Envelopes (2D version)

8. IMPLEMENTATION TIPS:
   - Handle empty arrays first
   - Use clear variable names (dp, tails, etc.)
   - Binary search can be tricky - practice the bounds
   - Consider using bisect module for cleaner code

9. COMPLEXITY ANALYSIS:
   - Basic DP: O(n²) time, O(n) space
   - Binary Search: O(n log n) time, O(n) space
   - Space can't be optimized below O(n) if we need the length

10. REAL-WORLD APPLICATIONS:
    - Patience sorting algorithm
    - Version control systems
    - Stock price analysis
    - Sequence alignment in bioinformatics

RECOMMENDED INTERVIEW APPROACH:
1. Clarify problem (subsequence vs subarray)
2. Start with basic DP solution
3. Walk through example step by step
4. Code the basic solution
5. Discuss optimization opportunity
6. Present binary search approach
7. Handle follow-ups about actual sequence
8. Test with edge cases

This problem is perfect for demonstrating:
- DP thinking and optimization
- Binary search skills
- Algorithm analysis
- Problem-solving progression from brute force to optimal
"""
