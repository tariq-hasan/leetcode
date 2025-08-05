"""
LeetCode 931: Minimum Falling Path Sum

Problem Statement:
Given an n x n array of integers matrix, return the minimum sum of any falling path 
through matrix.

A falling path starts at any element in the first row and chooses the element in 
the next row that is either directly below or diagonally left/right. 
Specifically, the next element from position (row, col) will be one of:
- (row + 1, col - 1)
- (row + 1, col)  
- (row + 1, col + 1)

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 100
- -100 <= matrix[i][j] <= 100

Examples:
Input: matrix = [[2,1,3],[6,5,4],[7,8,9]]
Output: 13
Explanation: There are two falling paths with a minimum sum as shown:
Path 1: [1,5,7] with sum = 13
Path 2: [1,4,8] with sum = 13

Input: matrix = [[-19,57],[-40,-5]]
Output: -59
Explanation: The falling path with a minimum sum is [-19,-40] with sum = -59.

Input: matrix = [[-48]]
Output: -48
"""

from typing import List

class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        """
        Solution 1: 2D Dynamic Programming (Most Intuitive)
        
        Key Insight: dp[i][j] represents minimum falling path sum to reach cell (i,j)
        from any starting position in the first row.
        
        Recurrence relation: 
        dp[i][j] = matrix[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])
        
        Time Complexity: O(n^2)
        Space Complexity: O(n^2)
        
        This is the most straightforward approach for interviews.
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        
        # Create DP table
        dp = [[0] * n for _ in range(n)]
        
        # Initialize first row (base case)
        for j in range(n):
            dp[0][j] = matrix[0][j]
        
        # Fill the DP table row by row
        for i in range(1, n):
            for j in range(n):
                # Start with the element directly above
                min_prev = dp[i-1][j]
                
                # Check diagonal left (if exists)
                if j > 0:
                    min_prev = min(min_prev, dp[i-1][j-1])
                
                # Check diagonal right (if exists)
                if j < n-1:
                    min_prev = min(min_prev, dp[i-1][j+1])
                
                dp[i][j] = matrix[i][j] + min_prev
        
        # Return minimum value from last row
        return min(dp[n-1])

    def minFallingPathSum_optimized(self, matrix: List[List[int]]) -> int:
        """
        Solution 2: Space-Optimized DP (1D Array)
        
        Key Insight: We only need the previous row to calculate current row.
        Use a 1D array and update it row by row.
        
        Time Complexity: O(n^2)
        Space Complexity: O(n)
        
        Great optimization to show after the 2D approach.
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        
        # Initialize with first row
        prev_row = matrix[0][:]
        
        # Process each subsequent row
        for i in range(1, n):
            curr_row = [0] * n
            
            for j in range(n):
                # Find minimum from valid positions in previous row
                candidates = [prev_row[j]]  # directly above
                
                if j > 0:  # diagonal left
                    candidates.append(prev_row[j-1])
                
                if j < n-1:  # diagonal right
                    candidates.append(prev_row[j+1])
                
                curr_row[j] = matrix[i][j] + min(candidates)
            
            prev_row = curr_row
        
        return min(prev_row)

    def minFallingPathSum_in_place(self, matrix: List[List[int]]) -> int:
        """
        Solution 3: In-Place DP (Modify Input Matrix)
        
        Key Insight: Use the input matrix itself as DP table.
        Process row by row, updating each cell with minimum falling path sum.
        
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        
        Most space-efficient but modifies input (ask interviewer first).
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        
        # Process from second row onwards
        for i in range(1, n):
            for j in range(n):
                # Find minimum from valid positions in previous row
                candidates = [matrix[i-1][j]]  # directly above
                
                if j > 0:  # diagonal left
                    candidates.append(matrix[i-1][j-1])
                
                if j < n-1:  # diagonal right
                    candidates.append(matrix[i-1][j+1])
                
                matrix[i][j] += min(candidates)
        
        return min(matrix[n-1])

    def minFallingPathSum_recursive_memo(self, matrix: List[List[int]]) -> int:
        """
        Solution 4: Recursive with Memoization (Top-Down DP)
        
        Good to show understanding of recursion and memoization.
        Demonstrates the recursive structure of the problem.
        
        Time Complexity: O(n^2)
        Space Complexity: O(n^2)
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        memo = {}
        
        def dfs(row: int, col: int) -> int:
            # Base case: reached bottom
            if row == n:
                return 0
            
            # Out of bounds
            if col < 0 or col >= n:
                return float('inf')
            
            if (row, col) in memo:
                return memo[(row, col)]
            
            # Try all three possible moves: down-left, down, down-right
            min_path = min(
                dfs(row + 1, col - 1),  # down-left
                dfs(row + 1, col),      # down
                dfs(row + 1, col + 1)   # down-right
            )
            
            memo[(row, col)] = matrix[row][col] + min_path
            return memo[(row, col)]
        
        # Try starting from each position in first row
        return min(dfs(0, j) for j in range(n))

    def minFallingPathSum_cleaner(self, matrix: List[List[int]]) -> int:
        """
        Solution 5: Cleaner Implementation using List Slicing
        
        More Pythonic approach using slicing for boundary handling.
        
        Time Complexity: O(n^2)
        Space Complexity: O(n)
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        dp = matrix[0][:]  # Initialize with first row
        
        for i in range(1, n):
            new_dp = [0] * n
            
            for j in range(n):
                # Get valid range from previous row
                left = max(0, j - 1)
                right = min(n, j + 2)  # j + 2 because slice is exclusive
                
                # Find minimum in the valid range
                new_dp[j] = matrix[i][j] + min(dp[left:right])
            
            dp = new_dp
        
        return min(dp)

    def minFallingPathSum_brute_force(self, matrix: List[List[int]]) -> int:
        """
        Solution 6: Brute Force Recursion (For Understanding Only)
        
        Exponential time complexity - NOT for interviews!
        Included only to show the recursive structure of the problem.
        
        Time Complexity: O(3^n)
        Space Complexity: O(n) - recursion stack
        """
        if not matrix or not matrix[0]:
            return 0
        
        n = len(matrix)
        
        def dfs(row: int, col: int) -> int:
            # Base case: reached bottom
            if row == n:
                return 0
            
            # Out of bounds
            if col < 0 or col >= n:
                return float('inf')
            
            # Try all three possible moves
            return matrix[row][col] + min(
                dfs(row + 1, col - 1),  # down-left
                dfs(row + 1, col),      # down
                dfs(row + 1, col + 1)   # down-right
            )
        
        # Try starting from each position in first row
        return min(dfs(0, j) for j in range(n))


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    test_cases = [
        # Test case 1: Basic example
        ([[2,1,3],[6,5,4],[7,8,9]], 13),
        
        # Test case 2: Negative numbers
        ([[-19,57],[-40,-5]], -59),
        
        # Test case 3: Single element
        ([[-48]], -48),
        
        # Test case 4: Single row
        ([[1,2,3]], 1),  # minimum of first row
        
        # Test case 5: Single column
        ([[1],[2],[3]], 6),
        
        # Test case 6: All negative
        ([[-1,-2,-3],[-4,-5,-6],[-7,-8,-9]], -12),  # -3 + -6 + -3 = -12
        
        # Test case 7: Mixed values
        ([[1,2,3],[4,5,6],[7,8,9]], 12),  # 1 + 4 + 7 = 12
        
        # Test case 8: Larger matrix
        ([[17,82,3,-15],[-50,-90,70,80],[25,19,-2,100],[-70,89,60,-100]], -139)
    ]
    
    methods = [
        ("2D DP", solution.minFallingPathSum),
        ("Optimized DP", solution.minFallingPathSum_optimized),
        ("Memoized", solution.minFallingPathSum_recursive_memo),
        ("Cleaner", solution.minFallingPathSum_cleaner)
    ]
    
    for i, (matrix, expected) in enumerate(test_cases, 1):
        print(f"\nTest case {i}: Matrix = {matrix}, Expected = {expected}")
        for method_name, method in methods:
            # Create a copy for methods that might modify input
            matrix_copy = [row[:] for row in matrix]
            result = method(matrix_copy)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {method_name}: {result} ({status})")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Problem Recognition:
   - Extension of path optimization problems with more movement options
   - Similar to Minimum Path Sum but allows diagonal movement
   - Can start from ANY position in first row (not fixed start point)
   - Classic Dynamic Programming with path optimization

2. Key Differences from Previous Problems:
   - Unique Paths: Count paths, only right/down movement
   - Minimum Path Sum: Minimize cost, only right/down movement
   - Minimum Falling Path Sum: Minimize cost, diagonal movement allowed, flexible start

3. Movement Rules:
   - From position (i,j), can move to:
     * (i+1, j-1) - diagonal left
     * (i+1, j) - directly down
     * (i+1, j+1) - diagonal right
   - Must stay within matrix bounds

4. DP Approach Evolution:
   
   a) State Definition:
      - dp[i][j] = minimum falling path sum to reach cell (i,j)
      - Base case: dp[0][j] = matrix[0][j] for all j
   
   b) Recurrence Relation:
      - dp[i][j] = matrix[i][j] + min(valid_previous_positions)
      - Valid previous: (i-1,j-1), (i-1,j), (i-1,j+1) if in bounds
   
   c) Final Answer:
      - min(dp[n-1][j]) for all j in last row
      - Can end at any position in last row

5. Boundary Handling:
   - Left edge (j=0): can't come from diagonal left
   - Right edge (j=n-1): can't come from diagonal right
   - Middle cells: all three directions available

6. Space Optimization Insight:
   - Only need previous row to compute current row
   - Can use 1D array instead of 2D matrix
   - Further optimize by modifying input in-place

7. Edge Cases:
   - Single element matrix: return that element
   - Single row: return minimum element in that row
   - Single column: return sum of all elements
   - All negative numbers: find path with least negative sum
   - Large positive/negative values: ensure no overflow

8. Follow-up Questions You Might Get:
   - "What if you can start from any position in the matrix?" → Different problem
   - "What if you want the actual path?" → Store parent pointers or backtrack
   - "What if matrix is too large for memory?" → Use rolling array
   - "What about maximum falling path sum?" → Change min to max
   - "What if some cells are blocked?" → Combine with obstacle logic

9. Interview Strategy:
   - Start by comparing to Minimum Path Sum
   - Highlight key differences: diagonal movement, flexible start/end
   - Implement 2D DP first (most intuitive)
   - Show space optimization if time permits
   - Walk through boundary handling carefully

10. Time/Space Analysis:
    - Time: O(n²) - process each cell once
    - Space: O(n²) for 2D DP, O(n) for optimized, O(1) for in-place
    - Cannot do better than O(n²) time since we need to consider all cells

11. Common Mistakes to Avoid:
    - Forgetting boundary checks for diagonal movements
    - Not considering all starting positions in first row
    - Incorrect handling of edge cases (single row/column)
    - Off-by-one errors in boundary calculations
    - Not taking minimum from last row for final answer

12. Related Problems:
    - LeetCode 64: Minimum Path Sum (predecessor)
    - LeetCode 1289: Minimum Falling Path Sum II (with constraint)
    - Triangle problem variations
    - General path optimization in grids

13. Optimization Techniques:
    - Space optimization: O(n) instead of O(n²)
    - In-place modification: O(1) extra space
    - Early termination: if negative cycles detected
    - Memoization: top-down approach with caching
"""
