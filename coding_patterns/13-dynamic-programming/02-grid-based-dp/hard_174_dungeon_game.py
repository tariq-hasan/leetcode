"""
LeetCode 174: Dungeon Game (Hard)

A knight wants to rescue a princess trapped in the bottom-right corner of a dungeon.
The dungeon consists of m x n rooms laid out in a 2D grid. The knight starts in the 
top-left corner and can only move right or down.

Each room contains either:
- A positive integer (health potion that increases knight's health)
- A negative integer (demon that decreases knight's health)
- Zero (empty room)

The knight's health must never drop to 0 or below during the journey.
Return the minimum initial health needed to rescue the princess.

Example:
dungeon = [[-3,5],
           [1,-4]]

Knight starts at (-3) with health H
- At (0,0): H - 3 ≥ 1, so H ≥ 4
- Path 1: (-3) → (5) → (-4): 4-3=1, 1+5=6, 6-4=2 ✓
- Path 2: (-3) → (1) → (-4): 4-3=1, 1+1=2, 2-4=-2 ✗ (dies)

Answer: 5 (take path (-3)→(1)→(-4): 5-3=2, 2+1=3, 3-4=-1, need at least 5)
Wait, that's wrong. Let me recalculate...

Actually, answer is 7:
- Path (-3)→(5)→(-4): 7-3=4, 4+5=9, 9-4=5 ✓
- We need to ensure health ≥ 1 after each step
"""

# Solution 1: Bottom-Up DP (RECOMMENDED for interviews)
def calculateMinimumHP_optimal(dungeon):
    """
    Time: O(m*n), Space: O(m*n)
    
    Key insight: Work backwards from princess to knight!
    dp[i][j] = minimum health needed when entering cell (i,j)
    
    Why backwards? We need to know future requirements to make current decisions.
    """
    if not dungeon or not dungeon[0]:
        return 1
    
    m, n = len(dungeon), len(dungeon[0])
    # dp[i][j] = min health needed when entering (i,j)
    dp = [[0] * n for _ in range(m)]
    
    # Base case: princess cell (bottom-right)
    # After taking damage/heal, we need at least 1 health
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
    
    # Fill last row (can only come from left)
    for j in range(n-2, -1, -1):
        dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])
    
    # Fill last column (can only come from above)
    for i in range(m-2, -1, -1):
        dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])
    
    # Fill the rest of the table
    for i in range(m-2, -1, -1):
        for j in range(n-2, -1, -1):
            # We can go right or down, choose the path requiring less initial health
            min_health_needed = min(dp[i][j+1], dp[i+1][j])
            dp[i][j] = max(1, min_health_needed - dungeon[i][j])
    
    return dp[0][0]


# Solution 2: Space Optimized (1D DP)
def calculateMinimumHP_space_optimized(dungeon):
    """
    Time: O(m*n), Space: O(n)
    
    Since we only need the next row/column, we can optimize space.
    """
    if not dungeon or not dungeon[0]:
        return 1
    
    m, n = len(dungeon), len(dungeon[0])
    # dp represents the next row initially
    dp = [0] * n
    
    # Initialize last row
    dp[n-1] = max(1, 1 - dungeon[m-1][n-1])
    for j in range(n-2, -1, -1):
        dp[j] = max(1, dp[j+1] - dungeon[m-1][j])
    
    # Process remaining rows from bottom to top
    for i in range(m-2, -1, -1):
        # Process rightmost column first (can only come from below)
        dp[n-1] = max(1, dp[n-1] - dungeon[i][n-1])
        
        # Process remaining columns from right to left
        for j in range(n-2, -1, -1):
            min_health_needed = min(dp[j+1], dp[j])  # right, down
            dp[j] = max(1, min_health_needed - dungeon[i][j])
    
    return dp[0]


# Solution 3: Top-Down DP with Memoization (for understanding)
def calculateMinimumHP_memo(dungeon):
    """
    Time: O(m*n), Space: O(m*n)
    
    Recursive approach with memoization. Good for explaining the logic.
    """
    if not dungeon or not dungeon[0]:
        return 1
    
    m, n = len(dungeon), len(dungeon[0])
    memo = {}
    
    def min_health_needed(i, j):
        """Returns minimum health needed when entering cell (i,j)"""
        # Base case: reached princess
        if i == m-1 and j == n-1:
            return max(1, 1 - dungeon[i][j])
        
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Out of bounds
        if i >= m or j >= n:
            return float('inf')
        
        # Try both directions and take the minimum requirement
        right = min_health_needed(i, j+1)
        down = min_health_needed(i+1, j)
        
        min_health_from_here = min(right, down)
        result = max(1, min_health_from_here - dungeon[i][j])
        
        memo[(i, j)] = result
        return result
    
    return min_health_needed(0, 0)


# Solution 4: Brute Force with Backtracking (for understanding only)
def calculateMinimumHP_brute(dungeon):
    """
    Time: O(2^(m+n)), Space: O(m+n)
    
    Try all possible paths and track minimum health needed.
    Too slow for large inputs but good for verification.
    """
    if not dungeon or not dungeon[0]:
        return 1
    
    m, n = len(dungeon), len(dungeon[0])
    min_initial_health = [float('inf')]
    
    def dfs(i, j, current_health, min_health_seen):
        # Update minimum health we've needed so far
        min_health_seen = min(min_health_seen, current_health)
        
        # If health drops to 0 or below, this path is invalid
        if current_health < 1:
            return
        
        # Reached princess
        if i == m-1 and j == n-1:
            # Calculate what initial health was needed
            # If min_health_seen was the lowest point, we needed at least (1 - min_health_seen + 1)
            needed_initial = 1 if min_health_seen >= 1 else (1 - min_health_seen + 1)
            min_initial_health[0] = min(min_initial_health[0], needed_initial)
            return
        
        # Try going right
        if j + 1 < n:
            new_health = current_health + dungeon[i][j+1]
            dfs(i, j+1, new_health, min(min_health_seen, new_health))
        
        # Try going down
        if i + 1 < m:
            new_health = current_health + dungeon[i+1][j]
            dfs(i+1, j, new_health, min(min_health_seen, new_health))
    
    # Try different initial health values
    for initial_health in range(1, 1000):  # Reasonable upper bound
        current_health = initial_health + dungeon[0][0]
        if current_health >= 1:
            dfs(0, 0, current_health, current_health)
            if min_initial_health[0] != float('inf'):
                return min_initial_health[0]
    
    return 1


def visualize_solution(dungeon):
    """
    Helper to visualize the DP table construction
    """
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    
    print("Dungeon:")
    for row in dungeon:
        print([f"{x:3d}" for x in row])
    
    # Build DP table step by step
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
    
    print(f"\nStep 1 - Princess cell: dp[{m-1}][{n-1}] = max(1, 1 - {dungeon[m-1][n-1]}) = {dp[m-1][n-1]}")
    
    # Last row
    for j in range(n-2, -1, -1):
        dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])
        print(f"Last row: dp[{m-1}][{j}] = max(1, {dp[m-1][j+1]} - {dungeon[m-1][j]}) = {dp[m-1][j]}")
    
    # Last column
    for i in range(m-2, -1, -1):
        dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])
        print(f"Last col: dp[{i}][{n-1}] = max(1, {dp[i+1][n-1]} - {dungeon[i][n-1]}) = {dp[i][n-1]}")
    
    # Rest of the table
    for i in range(m-2, -1, -1):
        for j in range(n-2, -1, -1):
            min_health = min(dp[i][j+1], dp[i+1][j])
            dp[i][j] = max(1, min_health - dungeon[i][j])
            print(f"dp[{i}][{j}] = max(1, min({dp[i][j+1]}, {dp[i+1][j]}) - {dungeon[i][j]}) = {dp[i][j]}")
    
    print("\nFinal DP table:")
    for i, row in enumerate(dp):
        print(f"Row {i}: {[f'{x:3d}' for x in row]}")
    
    return dp[0][0]


def test_solutions():
    """Test all solutions with various test cases"""
    test_cases = [
        # Test case 1: Given example
        [[-3, 5], [1, -4]],  # Expected: 7
        
        # Test case 2: All negative
        [[-1, -2], [-3, -4]],  # Expected: 5
        
        # Test case 3: All positive
        [[1, 2], [3, 4]],  # Expected: 1
        
        # Test case 4: Single cell negative
        [[-5]],  # Expected: 6
        
        # Test case 5: Single cell positive
        [[5]],  # Expected: 1
        
        # Test case 6: Complex case
        [[1, -3, 3], [0, -2, 0], [-3, -3, -3]]  # Expected: 3
    ]
    
    solutions = [
        ("Optimal DP", calculateMinimumHP_optimal),
        ("Space Optimized", calculateMinimumHP_space_optimized),
        ("Memoization", calculateMinimumHP_memo),
        # ("Brute Force", calculateMinimumHP_brute)  # Too slow for larger cases
    ]
    
    for i, dungeon in enumerate(test_cases):
        print(f"\nTest case {i + 1}: {dungeon}")
        for name, func in solutions:
            result = func(dungeon)
            print(f"{name}: {result}")


if __name__ == "__main__":
    test_solutions()
    
    # Uncomment to see detailed visualization
    # print("\n" + "="*60)
    # print("DETAILED SOLUTION WALKTHROUGH")
    # print("="*60)
    # result = visualize_solution([[-3, 5], [1, -4]])
    # print(f"\nFinal answer: {result}")


"""
INTERVIEW STRATEGY FOR HARD DP PROBLEMS:

1. Problem Understanding (3-5 minutes):
   - "Knight moves right/down from top-left to bottom-right"
   - "Health must stay ≥ 1 at all times during journey"
   - "Want minimum initial health to guarantee success"
   
2. Key Insight Discussion (5-7 minutes):
   - "This is different from typical path problems"
   - "Can't use forward DP because future requirements affect current decisions"
   - "Need to work backwards from the destination!"
   
3. Backwards DP Explanation:
   - "dp[i][j] = minimum health needed when ENTERING cell (i,j)"
   - "At princess: need max(1, 1 - dungeon_value) health after taking damage"
   - "At any cell: need max(1, min_future_requirement - current_gain) health"

4. Implementation (10-12 minutes):
   - Start with base case (princess cell)
   - Handle boundaries (last row, last column)
   - Fill the table backwards
   
5. Complexity Analysis:
   - Time: O(m*n) - visit each cell once
   - Space: O(m*n) for 2D DP, can optimize to O(n)

6. Edge Cases:
   - Single cell (positive/negative)
   - All positive values (answer = 1)
   - All negative values
   
KEY INSIGHTS TO EMPHASIZE:
- "Forward DP doesn't work - we need to know future requirements"
- "Health requirement propagates backwards through the dungeon"
- "Always need at least 1 health after each room"

COMMON MISTAKES:
- Trying forward DP (explain why it fails)
- Forgetting the "at least 1 health" constraint
- Off-by-one errors in the recurrence relation
"""
