def maxSubArray(nums):
    """
    KADANE'S ALGORITHM - Most Important Solution for Interviews
    
    Find the maximum sum of any contiguous subarray.
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Key insight: At each position, we decide whether to:
    1. Start a new subarray from current element
    2. Extend the existing subarray by including current element
    """
    max_sum = nums[0]  # Global maximum
    current_sum = nums[0]  # Current subarray sum
    
    for i in range(1, len(nums)):
        # Key decision: extend current subarray or start new one
        current_sum = max(nums[i], current_sum + nums[i])
        
        # Update global maximum
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def maxSubArrayWithIndices(nums):
    """
    Kadane's Algorithm with tracking start/end indices
    Useful for follow-up questions about returning the actual subarray
    """
    max_sum = nums[0]
    current_sum = nums[0]
    
    start = 0  # Start of max subarray
    end = 0    # End of max subarray
    temp_start = 0  # Temporary start for current subarray
    
    for i in range(1, len(nums)):
        if current_sum < 0:
            # Start new subarray
            current_sum = nums[i]
            temp_start = i
        else:
            # Extend current subarray
            current_sum += nums[i]
        
        # Update maximum and indices
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end


def maxSubArrayDP(nums):
    """
    Dynamic Programming Approach - Alternative perspective
    
    dp[i] = maximum sum of subarray ending at index i
    Time: O(n), Space: O(n) - can be optimized to O(1)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    max_sum = nums[0]
    
    for i in range(1, n):
        # Either start new subarray or extend previous
        dp[i] = max(nums[i], dp[i-1] + nums[i])
        max_sum = max(max_sum, dp[i])
    
    return max_sum


def maxSubArrayDivideConquer(nums):
    """
    Divide and Conquer Approach - Less efficient but good to know
    Time: O(n log n), Space: O(log n)
    
    The maximum subarray is either:
    1. Entirely in left half
    2. Entirely in right half  
    3. Crosses the middle (spans both halves)
    """
    def maxSubarrayHelper(left, right):
        if left == right:
            return nums[left]
        
        mid = (left + right) // 2
        
        # Maximum subarray in left half
        left_max = maxSubarrayHelper(left, mid)
        
        # Maximum subarray in right half
        right_max = maxSubarrayHelper(mid + 1, right)
        
        # Maximum subarray crossing the middle
        # Find max sum from mid going left
        left_sum = float('-inf')
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += nums[i]
            left_sum = max(left_sum, current_sum)
        
        # Find max sum from mid+1 going right
        right_sum = float('-inf')
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += nums[i]
            right_sum = max(right_sum, current_sum)
        
        cross_max = left_sum + right_sum
        
        return max(left_max, right_max, cross_max)
    
    return maxSubarrayHelper(0, len(nums) - 1)


def maxSubArrayBruteForce(nums):
    """
    Brute Force - Check all possible subarrays
    Time: O(n²), Space: O(1)
    Only for understanding - too slow for large inputs
    """
    n = len(nums)
    max_sum = float('-inf')
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += nums[j]
            max_sum = max(max_sum, current_sum)
    
    return max_sum


# ALGORITHM ANALYSIS AND INTERVIEW TIPS:
"""
KADANE'S ALGORITHM - THE GOLD STANDARD:

Key Insight: At each position, we make a local decision that leads to global optimum:
- If current_sum < 0: start fresh (negative prefix hurts us)
- If current_sum >= 0: extend the subarray (positive prefix helps us)

WHY IT WORKS:
- A negative prefix can never help maximize the sum
- We greedily choose the better option at each step
- This greedy choice leads to the optimal solution

INTERVIEW TALKING POINTS:

1. APPROACH COMPARISON:
   - Brute Force: O(n²) - check all subarrays
   - Kadane's: O(n) - optimal single pass
   - Divide & Conquer: O(n log n) - good for learning recursion
   - DP: O(n) - same as Kadane's but with extra space

2. FOLLOW-UP QUESTIONS:
   - "Return the actual subarray": Use the index-tracking version
   - "What if all numbers are negative?": Return the maximum single element
   - "2D version (maximum rectangle)": Extends to harder problems
   - "Circular array": Needs special handling for wrap-around

3. EDGE CASES:
   - Single element array
   - All negative numbers
   - All positive numbers
   - Empty array (clarify requirements)

4. VARIATIONS:
   - Maximum product subarray (different algorithm needed)
   - At most K elements (sliding window + Kadane's)
   - At least K elements (modified Kadane's)

5. OPTIMIZATION NOTES:
   - Space: O(1) is optimal
   - Time: O(n) is optimal - must see each element once
   - Can be extended to streams with slight modifications
"""
