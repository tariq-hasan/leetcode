"""
LeetCode 1027: Longest Arithmetic Subsequence

Problem: Given an array nums of integers, return the length of the longest arithmetic subsequence in nums.

An arithmetic subsequence is a sequence where the difference between consecutive elements is constant.

Example 1:
Input: nums = [3,6,9,12]
Output: 4
Explanation: The whole array is an arithmetic sequence with steps of length = 3.

Example 2:
Input: nums = [9,4,7,2,10]
Output: 3
Explanation: The longest arithmetic subsequence is [4,7,10].

Example 3:
Input: nums = [20,1,15,3,10,5,8]
Output: 4
Explanation: The longest arithmetic subsequence is [20,15,10,5].

Key Insight: Use DP with HashMap to track (difference, length) for each position
Time: O(n²), Space: O(n²)
"""

def longestArithSeqLength(nums):
    """
    Main solution using dynamic programming with hash maps.
    
    For each position i, maintain a dictionary where:
    - Key: common difference d
    - Value: length of arithmetic sequence ending at i with difference d
    
    Args:
        nums: List[int] - input array
    
    Returns:
        int - length of longest arithmetic subsequence
    """
    if len(nums) <= 2:
        return len(nums)
    
    n = len(nums)
    # dp[i] = dictionary mapping difference -> length of sequence ending at i
    dp = [dict() for _ in range(n)]
    max_length = 2  # minimum length is 2 for arithmetic sequence
    
    for i in range(n):
        for j in range(i):
            # Calculate difference between nums[i] and nums[j]
            diff = nums[i] - nums[j]
            
            # If there was already a sequence ending at j with this difference,
            # extend it. Otherwise, start a new sequence of length 2.
            if diff in dp[j]:
                dp[i][diff] = dp[j][diff] + 1
            else:
                dp[i][diff] = 2
            
            # Update global maximum
            max_length = max(max_length, dp[i][diff])
    
    return max_length


def longestArithSeqLength_optimized(nums):
    """
    Space-optimized version using 2D array instead of list of dicts.
    This can be more efficient for certain input ranges.
    
    Time: O(n²), Space: O(n * range) where range is max(nums) - min(nums)
    """
    if len(nums) <= 2:
        return len(nums)
    
    n = len(nums)
    min_val, max_val = min(nums), max(nums)
    diff_range = max_val - min_val
    
    # If all elements are the same, return n
    if diff_range == 0:
        return n
    
    # dp[i][d + diff_range] = length of arithmetic sequence ending at i with difference d
    # We offset by diff_range to handle negative differences
    dp = [[0] * (2 * diff_range + 1) for _ in range(n)]
    max_length = 2
    
    for i in range(n):
        for j in range(i):
            diff = nums[i] - nums[j]
            diff_idx = diff + diff_range  # offset for array indexing
            
            if dp[j][diff_idx] == 0:
                dp[i][diff_idx] = 2
            else:
                dp[i][diff_idx] = dp[j][diff_idx] + 1
            
            max_length = max(max_length, dp[i][diff_idx])
    
    return max_length


def longestArithSeqLength_with_reconstruction(nums):
    """
    Enhanced version that can also reconstruct the actual longest sequence.
    Useful for follow-up questions.
    """
    if len(nums) <= 2:
        return len(nums), nums if len(nums) <= 2 else []
    
    n = len(nums)
    dp = [dict() for _ in range(n)]
    parent = [dict() for _ in range(n)]  # for reconstruction
    
    max_length = 2
    best_end_idx = 1
    best_diff = nums[1] - nums[0]
    
    for i in range(n):
        for j in range(i):
            diff = nums[i] - nums[j]
            
            if diff in dp[j]:
                dp[i][diff] = dp[j][diff] + 1
                parent[i][diff] = j
            else:
                dp[i][diff] = 2
                parent[i][diff] = j
            
            if dp[i][diff] > max_length:
                max_length = dp[i][diff]
                best_end_idx = i
                best_diff = diff
    
    # Reconstruct the sequence
    sequence = []
    curr_idx = best_end_idx
    curr_diff = best_diff
    
    while curr_idx != -1 and curr_diff in parent[curr_idx]:
        sequence.append(nums[curr_idx])
        next_idx = parent[curr_idx][curr_diff]
        if next_idx == curr_idx:  # base case
            break
        curr_idx = next_idx
    
    if curr_idx != -1:
        sequence.append(nums[curr_idx])
    
    sequence.reverse()
    return max_length, sequence


def longestArithSeqLength_brute_force(nums):
    """
    Brute force solution for comparison and understanding.
    Time: O(n³), Space: O(1)
    Not recommended for interview, but good for initial thinking.
    """
    if len(nums) <= 2:
        return len(nums)
    
    n = len(nums)
    max_length = 2
    
    # Try every pair as the first two elements
    for i in range(n):
        for j in range(i + 1, n):
            diff = nums[j] - nums[i]
            length = 2
            last_val = nums[j]
            
            # Extend the sequence
            for k in range(j + 1, n):
                if nums[k] - last_val == diff:
                    length += 1
                    last_val = nums[k]
            
            max_length = max(max_length, length)
    
    return max_length


# Test cases and analysis
def test_solution():
    """Test the solution with example cases."""
    
    test_cases = [
        ([3, 6, 9, 12], 4),
        ([9, 4, 7, 2, 10], 3),
        ([20, 1, 15, 3, 10, 5, 8], 4),
        ([1, 2, 3, 4], 4),
        ([1, 1, 1, 1], 4),
        ([1, 7, 9, 2, 5, 8], 3),
        ([24, 13, 1, 100, 0, 94, 3, 0, 3], 2),
        ([1, 2], 2),
        ([1], 1),
        ([], 0)
    ]
    
    print("Testing DP solution:")
    for nums, expected in test_cases:
        result = longestArithSeqLength(nums)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {nums}, Expected: {expected}, Got: {result}")
    
    print("\nTesting with sequence reconstruction:")
    test_reconstruction = [
        [20, 1, 15, 3, 10, 5, 8],
        [9, 4, 7, 2, 10],
        [3, 6, 9, 12]
    ]
    
    for nums in test_reconstruction:
        if nums:  # avoid empty arrays
            length, sequence = longestArithSeqLength_with_reconstruction(nums)
            print(f"Input: {nums}")
            print(f"Longest arithmetic subsequence: {sequence} (length: {length})")
            print()


def trace_example(nums):
    """Trace through the algorithm step by step for understanding."""
    print(f"Tracing algorithm for {nums}:")
    
    if len(nums) <= 2:
        print(f"Base case: length = {len(nums)}")
        return
    
    n = len(nums)
    dp = [dict() for _ in range(n)]
    max_length = 2
    
    print(f"Initial setup: n = {n}, max_length = {max_length}")
    print()
    
    for i in range(n):
        print(f"Processing nums[{i}] = {nums[i]}:")
        for j in range(i):
            diff = nums[i] - nums[j]
            
            if diff in dp[j]:
                dp[i][diff] = dp[j][diff] + 1
                print(f"  Extending sequence from j={j}: diff={diff}, "
                      f"new_length={dp[i][diff]}")
            else:
                dp[i][diff] = 2
                print(f"  Starting new sequence from j={j}: diff={diff}, "
                      f"length=2")
            
            if dp[i][diff] > max_length:
                max_length = dp[i][diff]
                print(f"  ** New maximum length: {max_length}")
        
        if dp[i]:
            print(f"  dp[{i}] = {dp[i]}")
        print()
    
    print(f"Final result: {max_length}")


def analyze_complexity():
    """Analyze time and space complexity of different approaches."""
    
    analysis = """
    COMPLEXITY ANALYSIS:
    
    1. DP with HashMap (Main Solution):
       - Time: O(n²) - two nested loops
       - Space: O(n²) - worst case, each dp[i] can have O(n) different differences
       - Best for interview: Clean, efficient, handles all cases
    
    2. DP with 2D Array:
       - Time: O(n²) 
       - Space: O(n * range) where range = max(nums) - min(nums)
       - Good when range is small, but can be worse if range is large
    
    3. Brute Force:
       - Time: O(n³) - three nested loops
       - Space: O(1) - only using constants
       - Not recommended, but good for initial understanding
    
    TRADE-OFFS:
    - HashMap approach is most flexible and generally best
    - 2D array can be faster for small ranges due to better cache locality
    - Consider input constraints when choosing approach
    """
    
    print(analysis)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*50)
    trace_example([20, 1, 15, 3, 10, 5, 8])
    print("\n" + "="*50)
    analyze_complexity()
