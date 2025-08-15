# LeetCode 1547: Minimum Cost to Cut a Stick
#
# Problem: Given a wooden stick of length n units. The stick is labelled from 0 to n and has n+1 marks 
# at 0, 1, 2, ..., n. You are given an integer array cuts where cuts[i] denotes a position you should 
# perform a cut at. You should perform the cuts in any order you like.
#
# The cost of a cut depends on the length of the stick segment being cut. For example, if the stick is 
# of length 10 and you cut it at position 5, the cost is 10. If you then cut the left piece at position 
# 2, the cost is 5. Return the minimum total cost of the cuts.

# Solution 1: Top-down DP with Memoization - Most Common Interview Solution
def minCost(n, cuts):
    """
    Time: O(m^3), Space: O(m^2) where m = len(cuts)
    
    Key insight: The cost of cutting between positions i and j is (j - i).
    We need to find the optimal order to make all cuts.
    """
    # Add boundary points and sort
    cuts_with_bounds = [0] + sorted(cuts) + [n]
    memo = {}
    
    def dp(left, right):
        """
        Find minimum cost to make all cuts between positions left and right.
        left and right are indices in cuts_with_bounds array.
        """
        # Base case: no cuts possible between adjacent positions
        if right - left <= 1:
            return 0
        
        if (left, right) in memo:
            return memo[(left, right)]
        
        # Cost of current segment
        current_length = cuts_with_bounds[right] - cuts_with_bounds[left]
        min_cost = float('inf')
        
        # Try each possible cut position between left and right
        for mid in range(left + 1, right):
            # Cost = current segment length + cost of left part + cost of right part
            cost = current_length + dp(left, mid) + dp(mid, right)
            min_cost = min(min_cost, cost)
        
        memo[(left, right)] = min_cost
        return min_cost
    
    return dp(0, len(cuts_with_bounds) - 1)

# Solution 2: Bottom-up DP - Alternative Approach
def minCostBottomUp(n, cuts):
    """
    Time: O(m^3), Space: O(m^2)
    
    Bottom-up dynamic programming approach.
    """
    cuts_with_bounds = [0] + sorted(cuts) + [n]
    m = len(cuts_with_bounds)
    
    # dp[i][j] = minimum cost to cut between positions i and j
    dp = [[0] * m for _ in range(m)]
    
    # Fill dp table for increasing lengths
    for length in range(3, m + 1):  # Need at least length 3 to have cuts between
        for left in range(m - length + 1):
            right = left + length - 1
            current_length = cuts_with_bounds[right] - cuts_with_bounds[left]
            
            dp[left][right] = float('inf')
            # Try each cut position between left and right
            for mid in range(left + 1, right):
                cost = current_length + dp[left][mid] + dp[mid][right]
                dp[left][right] = min(dp[left][right], cost)
    
    return dp[0][m - 1]

# Solution 3: Optimized with Range Caching
def minCostOptimized(n, cuts):
    """
    Time: O(m^3), Space: O(m^2)
    
    Same complexity but with cleaner implementation and better cache efficiency.
    """
    cuts_sorted = sorted(cuts)
    
    # Use a more cache-friendly approach
    from functools import lru_cache
    
    @lru_cache(None)
    def dp(left_pos, right_pos, cut_start, cut_end):
        """
        Find min cost to cut between left_pos and right_pos,
        considering only cuts from cut_start to cut_end-1 in cuts_sorted.
        """
        # No cuts in this range
        if cut_start >= cut_end:
            return 0
        
        # Current segment length
        current_length = right_pos - left_pos
        min_cost = float('inf')
        
        # Try each cut in the valid range
        for i in range(cut_start, cut_end):
            cut_pos = cuts_sorted[i]
            if left_pos < cut_pos < right_pos:
                # Cost of making this cut + recursively solve left and right parts
                left_cost = dp(left_pos, cut_pos, cut_start, i)
                right_cost = dp(cut_pos, right_pos, i + 1, cut_end)
                total_cost = current_length + left_cost + right_cost
                min_cost = min(min_cost, total_cost)
        
        return min_cost if min_cost != float('inf') else 0
    
    return dp(0, n, 0, len(cuts_sorted))

# Solution 4: Matrix Chain Multiplication Style
def minCostMCM(n, cuts):
    """
    Time: O(m^3), Space: O(m^2)
    
    Classic Matrix Chain Multiplication style implementation.
    This shows the connection to other interval DP problems.
    """
    # Add boundaries and sort
    positions = [0] + sorted(cuts) + [n]
    m = len(positions)
    
    # dp[i][j] represents minimum cost to make all cuts between positions[i] and positions[j]
    dp = [[0] * m for _ in range(m)]
    
    # For each possible interval length
    for gap in range(2, m):  # gap is the distance between i and j
        for i in range(m - gap):
            j = i + gap
            dp[i][j] = float('inf')
            
            # Try each possible last cut position
            for k in range(i + 1, j):
                # Cost = length of current segment + cost of left part + cost of right part
                cost = (positions[j] - positions[i]) + dp[i][k] + dp[k][j]
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][m - 1]

# Solution 5: Recursive with Detailed Explanation
def minCostExplained(n, cuts):
    """
    Time: O(m^3), Space: O(m^2)
    
    Most detailed version with extensive comments for interview explanation.
    """
    # Step 1: Add boundary points (0 and n) and sort all positions
    all_positions = [0] + sorted(cuts) + [n]
    cache = {}
    
    def solve(left_idx, right_idx):
        """
        Solve the subproblem: minimum cost to make all cuts between 
        all_positions[left_idx] and all_positions[right_idx].
        
        Args:
            left_idx: index of left boundary in all_positions
            right_idx: index of right boundary in all_positions
        
        Returns:
            Minimum cost to make all cuts in this interval
        """
        # Base case: no cuts possible (adjacent positions)
        if right_idx - left_idx <= 1:
            return 0
        
        # Check cache
        if (left_idx, right_idx) in cache:
            return cache[(left_idx, right_idx)]
        
        # Current segment spans from all_positions[left_idx] to all_positions[right_idx]
        segment_length = all_positions[right_idx] - all_positions[left_idx]
        
        min_total_cost = float('inf')
        
        # Try making each possible cut as the "last" cut in this segment
        for cut_idx in range(left_idx + 1, right_idx):
            # If we make the cut at all_positions[cut_idx] last:
            # 1. Cost of this cut = segment_length (length before any cuts)
            # 2. Plus cost of optimally cutting left part [left_idx, cut_idx]
            # 3. Plus cost of optimally cutting right part [cut_idx, right_idx]
            
            left_cost = solve(left_idx, cut_idx)
            right_cost = solve(cut_idx, right_idx)
            total_cost = segment_length + left_cost + right_cost
            
            min_total_cost = min(min_total_cost, total_cost)
        
        cache[(left_idx, right_idx)] = min_total_cost
        return min_total_cost
    
    return solve(0, len(all_positions) - 1)

# Test cases and examples
def test_solutions():
    test_cases = [
        (7, [1, 3, 4, 5]),      # Expected: 16
        (9, [5, 6, 1, 4, 2]),   # Expected: 22
        (10, [1, 2, 5]),        # Expected: 16
        (20, [10]),             # Expected: 20
    ]
    
    for n, cuts in test_cases:
        result1 = minCost(n, cuts)
        result2 = minCostBottomUp(n, cuts)
        result3 = minCostMCM(n, cuts)
        result4 = minCostExplained(n, cuts)
        
        print(f"n={n}, cuts={cuts}")
        print(f"  Top-down: {result1}")
        print(f"  Bottom-up: {result2}")
        print(f"  MCM Style: {result3}")
        print(f"  Explained: {result4}")
        print(f"  All match: {result1 == result2 == result3 == result4}")
        print()

# Detailed walkthrough example
def explain_example():
    """
    Example: n=7, cuts=[1,3,4,5]
    
    Stick: 0----1----2----3----4----5----6----7
    Cuts needed at positions: 1, 3, 4, 5
    
    Different cutting orders give different costs:
    
    Order 1: Cut at 1, then 3, then 4, then 5
    - Cut at 1: cost = 7 (full stick length), pieces: [0,1], [1,7]
    - Cut at 3: cost = 6 (length of [1,7]), pieces: [0,1], [1,3], [3,7] 
    - Cut at 4: cost = 4 (length of [3,7]), pieces: [0,1], [1,3], [3,4], [4,7]
    - Cut at 5: cost = 3 (length of [4,7]), pieces: [0,1], [1,3], [3,4], [4,5], [5,7]
    Total: 7 + 6 + 4 + 3 = 20
    
    Order 2: Cut at 4, then 1, then 3, then 5  
    - Cut at 4: cost = 7, pieces: [0,4], [4,7]
    - Cut at 1: cost = 4 (length of [0,4]), pieces: [0,1], [1,4], [4,7]
    - Cut at 3: cost = 3 (length of [1,4]), pieces: [0,1], [1,3], [3,4], [4,7]
    - Cut at 5: cost = 3 (length of [4,7]), pieces: [0,1], [1,3], [3,4], [4,5], [5,7]
    Total: 7 + 4 + 3 + 3 = 17
    
    The DP finds the optimal order with cost 16.
    """
    print("Example walkthrough:")
    print("n=7, cuts=[1,3,4,5]")
    print("Different orders of cuts give different total costs")
    print("DP finds the optimal order by trying all possibilities")
    print("Key insight: cost of a cut = length of segment being cut")

# Interview strategy and common patterns
def interview_strategy():
    """
    Interview Approach for Interval DP Problems:
    
    1. **Problem Recognition** (1-2 mins):
       - Keywords: "optimal order", "interval", "cuts", "minimum cost"
       - Pattern: Cost depends on current state, decisions affect future costs
       - This is classic Interval DP (like Matrix Chain Multiplication)
    
    2. **State Definition** (2-3 mins):
       - What represents a subproblem? → Interval [i, j]
       - What do we need to track? → Minimum cost to make all cuts in interval
       - Boundaries: Add 0 and n to cuts array
    
    3. **Recurrence Relation** (3-4 mins):
       - Try each cut as the "last" cut in current interval
       - Cost = current_length + cost(left_part) + cost(right_part)
       - Base case: no cuts possible between adjacent positions
    
    4. **Implementation Choice** (1-2 mins):
       - Top-down (memoization) is usually more intuitive
       - Bottom-up if you want to show mastery of both approaches
    
    5. **Complexity Analysis** (1-2 mins):
       - Time: O(m³) where m = number of cuts
       - Space: O(m²) for memoization/DP table
    
    6. **Testing and Edge Cases** (2-3 mins):
       - Single cut, no cuts, cuts at boundaries
       - Verify with small example
    
    Key Interview Points:
    - This is similar to Matrix Chain Multiplication
    - The "trick" is thinking about which cut to make LAST
    - Adding boundaries (0, n) simplifies the implementation
    - Always sort the cuts array first
    
    Common Mistakes:
    - Not adding boundary points
    - Forgetting to sort cuts
    - Wrong recurrence (trying first cut instead of last cut)
    - Off-by-one errors in indices
    """
    pass

# Pattern recognition for similar problems
def similar_problems():
    """
    This problem follows the classic "Interval DP" pattern. Similar problems:
    
    1. Matrix Chain Multiplication (exact same pattern)
    2. Burst Balloons (LC 312) - very similar structure
    3. Palindrome Partitioning II (LC 132) - related concept
    4. Stone Game problems - interval game theory
    5. Optimal Binary Search Tree - classic interval DP
    
    General Interval DP template:
    ```
    for length in range(2, n+1):
        for left in range(n-length+1):
            right = left + length - 1
            for mid in range(left, right):
                # try splitting at mid
                dp[left][right] = min(dp[left][right], 
                                    cost + dp[left][mid] + dp[mid+1][right])
    ```
    """
    pass

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60)
    explain_example()
    print("\n" + "="*60)
    print("Interview tip: Start with Solution 1 (top-down memoization)")
    print("Emphasize the connection to Matrix Chain Multiplication!")
    print("Key insight: think about which cut to make LAST, not FIRST")
