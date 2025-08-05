"""
LeetCode 120: Triangle
Given a triangle array, return the minimum path sum from top to bottom.

For each step, you may move to an adjacent number of the row below.
More formally, if you are on index i on the current row, you may move to 
either index i or index i + 1 on the next row.

Example:
Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
Output: 11
Explanation: The triangle looks like:
   2
  3 4
 6 5 7
4 1 8 3
The minimum path sum from top to bottom is 2 + 3 + 5 + 1 = 11.
"""

# Solution 1: Bottom-Up DP (Space Optimized) - RECOMMENDED for interviews
def minimumTotal_optimal(triangle):
    """
    Time: O(n^2) where n is number of rows
    Space: O(n) - only using the last row
    
    Key insight: Start from bottom and work upwards.
    Each position stores the minimum path sum from that position to bottom.
    """
    if not triangle:
        return 0
    
    # Use the last row as our DP array
    dp = triangle[-1][:]
    
    # Work backwards from second-to-last row
    for row in range(len(triangle) - 2, -1, -1):
        for col in range(len(triangle[row])):
            # Current position + min of two possible next positions
            dp[col] = triangle[row][col] + min(dp[col], dp[col + 1])
    
    return dp[0]


# Solution 2: Top-Down DP with Memoization
def minimumTotal_memo(triangle):
    """
    Time: O(n^2), Space: O(n^2)
    Good for explaining the recursive thinking process
    """
    memo = {}
    
    def dfs(row, col):
        # Base case: reached bottom
        if row == len(triangle) - 1:
            return triangle[row][col]
        
        if (row, col) in memo:
            return memo[(row, col)]
        
        # Try both possible moves: (row+1, col) and (row+1, col+1)
        left = dfs(row + 1, col)
        right = dfs(row + 1, col + 1)
        
        memo[(row, col)] = triangle[row][col] + min(left, right)
        return memo[(row, col)]
    
    return dfs(0, 0)


# Solution 3: Bottom-Up DP (2D Array) - Good for understanding
def minimumTotal_2d(triangle):
    """
    Time: O(n^2), Space: O(n^2)
    More intuitive but uses extra space
    """
    n = len(triangle)
    # dp[i][j] = minimum path sum from (i,j) to bottom
    dp = [[0] * len(triangle[i]) for i in range(n)]
    
    # Initialize last row
    dp[-1] = triangle[-1][:]
    
    # Fill from bottom to top
    for row in range(n - 2, -1, -1):
        for col in range(len(triangle[row])):
            dp[row][col] = triangle[row][col] + min(dp[row + 1][col], 
                                                   dp[row + 1][col + 1])
    
    return dp[0][0]


# Solution 4: In-place modification (if allowed)
def minimumTotal_inplace(triangle):
    """
    Time: O(n^2), Space: O(1)
    Modifies input array - only use if explicitly allowed
    """
    for row in range(len(triangle) - 2, -1, -1):
        for col in range(len(triangle[row])):
            triangle[row][col] += min(triangle[row + 1][col], 
                                    triangle[row + 1][col + 1])
    
    return triangle[0][0]


# Test cases
def test_solutions():
    test_cases = [
        [[2],[3,4],[6,5,7],[4,1,8,3]],  # Expected: 11
        [[-10]],                         # Expected: -10
        [[1],[2,3]],                     # Expected: 3
        [[1],[2,3],[4,5,6]]             # Expected: 7
    ]
    
    solutions = [
        ("Optimal (Bottom-Up)", minimumTotal_optimal),
        ("Memoization", minimumTotal_memo),
        ("2D DP", minimumTotal_2d),
        ("In-place", minimumTotal_inplace)
    ]
    
    for i, triangle in enumerate(test_cases):
        print(f"\nTest case {i + 1}: {triangle}")
        for name, func in solutions:
            # Make a copy for in-place solution
            triangle_copy = [row[:] for row in triangle]
            result = func(triangle_copy)
            print(f"{name}: {result}")


if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TIPS:

1. Start with the recursive approach to show your thinking:
   - "For each position, I can go to position i or i+1 in next row"
   - "I want minimum of both paths plus current value"

2. Mention the optimization:
   - "Bottom-up is more efficient than top-down"
   - "We can optimize space by reusing the last row"

3. Complexity Analysis:
   - Time: O(n²) where n is number of rows
   - Space: O(n) for optimal solution, O(n²) for memoization

4. Edge cases to consider:
   - Single element triangle
   - Negative numbers
   - Empty triangle (though constraints usually prevent this)

5. Follow-up questions you might get:
   - "Can you do it in O(1) space?" → In-place modification
   - "What if we need the actual path?" → Store parent pointers
   - "What about going from bottom to top?" → Same logic, reverse direction
"""
