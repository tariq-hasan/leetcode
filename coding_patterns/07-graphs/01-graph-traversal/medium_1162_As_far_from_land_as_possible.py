"""
LeetCode 1162: As Far from Land as Possible

Problem Statement:
Given an n x n grid containing only values 0 and 1, where:
- 0 represents water
- 1 represents land
Find a water cell such that its distance to the nearest land cell is maximized, 
and return the distance.

The distance used is Manhattan distance: |x1 - x2| + |y1 - y2|

Constraints:
- n == grid.length
- n == grid[i].length
- 1 <= n <= 100
- grid[i][j] is 0 or 1

Examples:
Input: grid = [[1,0,1],[0,0,0],[1,0,1]]
Output: 2
Explanation: The cell (1,1) is as far as possible from all the land with distance 2.

Input: grid = [[1,0,0],[0,0,0],[0,0,0]]
Output: 4
Explanation: The cell (2,2) is as far as possible from all the land with distance 4.
"""

from collections import deque
from typing import List

class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        """
        Solution 1: Multi-source BFS (Optimal)
        
        Key Insight: Instead of finding distance from each water cell to nearest land,
        we can start BFS from ALL land cells simultaneously and expand outward.
        
        Time Complexity: O(n²)
        Space Complexity: O(n²)
        
        This is the most efficient and elegant solution for interviews.
        """
        n = len(grid)
        queue = deque()
        
        # Add all land cells to queue as starting points
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    queue.append((i, j, 0))  # (row, col, distance)
        
        # Edge cases
        if len(queue) == 0 or len(queue) == n * n:
            return -1  # All water or all land
        
        # BFS directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        max_distance = 0
        
        while queue:
            row, col, distance = queue.popleft()
            
            # Explore all 4 directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds and if it's water (unvisited)
                if (0 <= new_row < n and 0 <= new_col < n and 
                    grid[new_row][new_col] == 0):
                    
                    # Mark as visited and update distance
                    grid[new_row][new_col] = distance + 1
                    queue.append((new_row, new_col, distance + 1))
                    max_distance = max(max_distance, distance + 1)
        
        return max_distance

    def maxDistance_v2(self, grid: List[List[int]]) -> int:
        """
        Solution 2: BFS with separate visited array (Alternative approach)
        
        This version doesn't modify the input grid, which might be preferred
        in some interview contexts.
        
        Time Complexity: O(n²)
        Space Complexity: O(n²)
        """
        n = len(grid)
        queue = deque()
        visited = [[False] * n for _ in range(n)]
        
        # Add all land cells to queue
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    queue.append((i, j, 0))
                    visited[i][j] = True
        
        # Edge cases
        if len(queue) == 0 or len(queue) == n * n:
            return -1
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        max_distance = 0
        
        while queue:
            row, col, distance = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < n and 
                    not visited[new_row][new_col] and grid[new_row][new_col] == 0):
                    
                    visited[new_row][new_col] = True
                    queue.append((new_row, new_col, distance + 1))
                    max_distance = max(max_distance, distance + 1)
        
        return max_distance

    def maxDistance_bruteforce(self, grid: List[List[int]]) -> int:
        """
        Solution 3: Brute Force (For comparison - NOT recommended for interviews)
        
        For each water cell, find minimum distance to any land cell.
        
        Time Complexity: O(n⁴)
        Space Complexity: O(1)
        
        This is too slow but good to understand the problem.
        """
        n = len(grid)
        max_dist = -1
        
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 0:  # Water cell
                    min_dist = float('inf')
                    
                    # Find distance to nearest land
                    for x in range(n):
                        for y in range(n):
                            if grid[x][y] == 1:  # Land cell
                                dist = abs(i - x) + abs(j - y)
                                min_dist = min(min_dist, dist)
                    
                    if min_dist != float('inf'):
                        max_dist = max(max_dist, min_dist)
        
        return max_dist


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    # Test case 1
    grid1 = [[1,0,1],[0,0,0],[1,0,1]]
    expected1 = 2
    result1 = solution.maxDistance(grid1)
    print(f"Test 1: Expected {expected1}, Got {result1}, {'PASS' if result1 == expected1 else 'FAIL'}")
    
    # Test case 2
    grid2 = [[1,0,0],[0,0,0],[0,0,0]]
    expected2 = 4
    result2 = solution.maxDistance(grid2)
    print(f"Test 2: Expected {expected2}, Got {result2}, {'PASS' if result2 == expected2 else 'FAIL'}")
    
    # Test case 3 - All land
    grid3 = [[1,1,1],[1,1,1],[1,1,1]]
    expected3 = -1
    result3 = solution.maxDistance(grid3)
    print(f"Test 3: Expected {expected3}, Got {result3}, {'PASS' if result3 == expected3 else 'FAIL'}")
    
    # Test case 4 - All water
    grid4 = [[0,0,0],[0,0,0],[0,0,0]]
    expected4 = -1
    result4 = solution.maxDistance(grid4)
    print(f"Test 4: Expected {expected4}, Got {result4}, {'PASS' if result4 == expected4 else 'FAIL'}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Algorithm Choice:
   - Multi-source BFS is the optimal approach
   - Think of it as "expanding water level from all shores simultaneously"
   - More intuitive than single-source BFS from each water cell

2. Key Insights:
   - Manhattan distance is used (not Euclidean)
   - BFS naturally gives shortest path/distance
   - Multi-source BFS eliminates need for multiple single-source BFS calls

3. Edge Cases:
   - All cells are land: return -1
   - All cells are water: return -1
   - Single land cell: maximum distance is to corner

4. Optimization Considerations:
   - Could modify input grid to save space (mark visited cells)
   - Or use separate visited array if input shouldn't be modified

5. Follow-up Questions You Might Get:
   - What if we used Euclidean distance instead?
   - How would you handle a larger grid that doesn't fit in memory?
   - Can you solve this with dynamic programming? (Yes, but BFS is better)
   - What if there are obstacles (other values besides 0 and 1)?

6. Complexity Analysis:
   - Time: O(n²) - visit each cell at most once
   - Space: O(n²) - queue can contain all cells in worst case
"""
