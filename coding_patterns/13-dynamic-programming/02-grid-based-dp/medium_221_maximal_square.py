"""
LeetCode 221: Maximal Square
Given an m x n binary matrix filled with 0's and 1's, find the largest square 
containing only 1's and return its area.

Example 1:
Input: matrix = [["1","0","1","0","0"],
                 ["1","0","1","1","1"],
                 ["1","1","1","1","1"],
                 ["1","0","0","1","0"]]
Output: 4 (2x2 square)

Example 2:
Input: matrix = [["0","1"],["1","0"]]
Output: 1

Example 3:
Input: matrix = [["0"]]
Output: 0
"""

# Solution 1: 2D DP (Most Intuitive) - RECOMMENDED for interviews
def maximalSquare_2d(matrix):
    """
    Time: O(m*n), Space: O(m*n)
    
    Key insight: dp[i][j] = side length of largest square with bottom-right corner at (i,j)
    Formula: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
    """
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    # dp[i][j] = side length of max square ending at (i,j)
    dp = [[0] * n for _ in range(m)]
    max_side = 0
    
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    # First row or column can only form 1x1 squares
                    dp[i][j] = 1
                else:
                    # Core DP recurrence relation
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                
                max_side = max(max_side, dp[i][j])
    
    return max_side * max_side


# Solution 2: Space Optimized 1D DP
def maximalSquare_1d(matrix):
    """
    Time: O(m*n), Space: O(n)
    
    Since we only need previous row and current row, we can optimize space.
    """
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    dp = [0] * n  # Previous row
    max_side = 0
    prev = 0  # dp[i-1][j-1] for current iteration
    
    for i in range(m):
        for j in range(n):
            temp = dp[j]  # Store dp[i-1][j] before overwriting
            
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[j] = 1
                else:
                    # dp[j] = dp[i-1][j] (before update)
                    # dp[j-1] = dp[i][j-1] (already updated)
                    # prev = dp[i-1][j-1]
                    dp[j] = min(dp[j], dp[j-1], prev) + 1
                
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            
            prev = temp  # Update prev for next iteration
    
    return max_side * max_side


# Solution 3: Brute Force (for understanding)
def maximalSquare_brute(matrix):
    """
    Time: O(m*n*min(m,n)^2), Space: O(1)
    
    For each cell, try all possible square sizes.
    Good for explaining the problem but too slow for large inputs.
    """
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    max_side = 0
    
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                # Try squares of increasing size starting from (i,j)
                max_possible = min(m - i, n - j)
                
                for size in range(1, max_possible + 1):
                    # Check if we can form a square of this size
                    valid = True
                    for r in range(i, i + size):
                        for c in range(j, j + size):
                            if matrix[r][c] == '0':
                                valid = False
                                break
                        if not valid:
                            break
                    
                    if valid:
                        max_side = max(max_side, size)
                    else:
                        break  # No point checking larger squares
    
    return max_side * max_side


# Solution 4: Most Space Optimized (In-place if input can be modified)
def maximalSquare_inplace(matrix):
    """
    Time: O(m*n), Space: O(1)
    
    Modify the input matrix to store DP values.
    Only use if explicitly allowed to modify input.
    """
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    max_side = 0
    
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = min(int(matrix[i-1][j]), 
                                     int(matrix[i][j-1]), 
                                     int(matrix[i-1][j-1])) + 1
                
                max_side = max(max_side, int(matrix[i][j]))
    
    return max_side * max_side


def test_solutions():
    """Test all solutions with various test cases"""
    test_cases = [
        # Test case 1: Standard example
        [["1","0","1","0","0"],
         ["1","0","1","1","1"],
         ["1","1","1","1","1"],
         ["1","0","0","1","0"]],  # Expected: 4
        
        # Test case 2: Small matrix
        [["0","1"],["1","0"]],  # Expected: 1
        
        # Test case 3: Single cell
        [["0"]],  # Expected: 0
        [["1"]],  # Expected: 1
        
        # Test case 4: All ones
        [["1","1","1"],
         ["1","1","1"],
         ["1","1","1"]],  # Expected: 9
        
        # Test case 5: All zeros
        [["0","0","0"],
         ["0","0","0"]],  # Expected: 0
    ]
    
    solutions = [
        ("2D DP", maximalSquare_2d),
        ("1D DP", maximalSquare_1d),
        ("Brute Force", maximalSquare_brute),
        ("In-place", maximalSquare_inplace)
    ]
    
    for i, matrix in enumerate(test_cases):
        print(f"\nTest case {i + 1}:")
        for row in matrix:
            print(''.join(row))
        
        for name, func in solutions:
            # Create a copy for in-place solution
            matrix_copy = [row[:] for row in matrix]
            result = func(matrix_copy)
            print(f"{name}: {result}")


# Visual explanation helper
def visualize_dp_process(matrix):
    """
    Helper function to visualize how DP table is built
    Useful for explaining during interview
    """
    if not matrix or not matrix[0]:
        return
    
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    
    print("Original matrix:")
    for row in matrix:
        print(''.join(row))
    
    print("\nDP table construction:")
    
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        
        # Print current state
        print(f"After row {i}:")
        for row in dp:
            print(' '.join(str(x) for x in row))
        print()


if __name__ == "__main__":
    test_solutions()
    
    # Uncomment to see DP visualization
    # print("\n" + "="*50)
    # print("DP PROCESS VISUALIZATION")
    # print("="*50)
    # visualize_dp_process([["1","0","1","0","0"],
    #                      ["1","0","1","1","1"],
    #                      ["1","1","1","1","1"],
    #                      ["1","0","0","1","0"]])


"""
INTERVIEW STRATEGY:

1. Problem Understanding (2-3 minutes):
   - "I need to find the largest square of 1's"
   - "I should return the area, not the side length"
   - Ask about edge cases: empty matrix, all 0's, etc.

2. Approach Discussion (3-4 minutes):
   - Start with brute force: "For each cell, try all square sizes"
   - "That's O(mn*min(m,n)^2) - can we do better?"
   - "Dynamic Programming: dp[i][j] = largest square ending at (i,j)"
   - Key insight: "To form a k×k square, I need three (k-1)×(k-1) squares around me"

3. Implementation (8-10 minutes):
   - Code the 2D DP solution first
   - Explain the recurrence: min(top, left, diagonal) + 1
   - Handle base cases carefully

4. Optimization Discussion (2-3 minutes):
   - "Can optimize space from O(mn) to O(n)"
   - "Could modify input in-place for O(1) space if allowed"

5. Testing (2-3 minutes):
   - Walk through example manually
   - Consider edge cases

KEY INSIGHTS TO MENTION:
- "The bottleneck for square formation is the smallest adjacent square"
- "We build larger squares from smaller ones"
- "Each cell stores the side length, not area"

COMPLEXITY:
- Time: O(m*n) - visit each cell once
- Space: O(m*n) for 2D DP, O(n) for optimized, O(1) for in-place
"""
