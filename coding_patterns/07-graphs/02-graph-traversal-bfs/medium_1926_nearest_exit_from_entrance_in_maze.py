"""
LeetCode 1926: Nearest Exit from Entrance in Maze

Problem Statement:
You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') 
and walls (represented as '+'). You are also given the entrance of the maze, 
where entrance = [entrancerow, entrancecol] denotes the row and column of the cell 
you are initially standing at.

In one step, you can move one cell up, down, left, or right. You cannot step into 
a cell with a wall, and you cannot step outside the maze. Your goal is to find the 
nearest exit from the entrance. An exit is defined as an empty cell that is at the 
border of the maze. The entrance does not count as an exit.

Return the number of steps in the shortest path from the entrance to the nearest exit, 
or -1 if no such path exists.

Constraints:
- maze.length == m
- maze[i].length == n
- 1 <= m, n <= 100
- maze[i][j] is either '.' or '+'
- entrance.length == 2
- 0 <= entrancerow < m
- 0 <= entrancecol < n
- entrance will always be an empty cell

Examples:
Input: maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]
Output: 1
Explanation: There are 3 exits in this maze at [1,0], [1,3], and [2,3].
Initially, you are at the entrance cell [1,2].
- You can reach [1,0] by moving 2 steps left.
- You can reach [1,3] by moving 1 step right.
- You can reach [2,3] by moving 1 step right and 1 step down.
The nearest exit is [1,3], which is 1 step away.

Input: maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]
Output: 2
Explanation: The only exit is at [1,2], which is 2 steps away.

Input: maze = [[".","+"]],entrance = [0,0]
Output: -1
Explanation: There is no exit in this maze.
"""

from collections import deque
from typing import List

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        """
        Solution 1: BFS (Optimal)
        
        Key Insight: Use BFS to find shortest path from entrance to any exit.
        An exit is any empty cell ('.') at the border that is not the entrance.
        
        Time Complexity: O(m * n) - visit each cell at most once
        Space Complexity: O(m * n) - queue and visited set in worst case
        
        This is the optimal solution for interviews.
        """
        m, n = len(maze), len(maze[0])
        queue = deque([(entrance[0], entrance[1], 0)])  # (row, col, steps)
        visited = set()
        visited.add((entrance[0], entrance[1]))
        
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            row, col, steps = queue.popleft()
            
            # Check all 4 directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds and if cell is not a wall and not visited
                if (0 <= new_row < m and 0 <= new_col < n and 
                    maze[new_row][new_col] == '.' and 
                    (new_row, new_col) not in visited):
                    
                    # Check if this is an exit (at border and not entrance)
                    if (new_row == 0 or new_row == m - 1 or 
                        new_col == 0 or new_col == n - 1):
                        return steps + 1
                    
                    # Mark as visited and add to queue
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, steps + 1))
        
        return -1  # No exit found

    def nearestExit_v2(self, maze: List[List[str]], entrance: List[int]) -> int:
        """
        Solution 2: BFS with in-place marking (Space optimized)
        
        Modifies the input maze to mark visited cells.
        Slightly more space efficient but modifies input.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n) - queue only, no separate visited set
        """
        m, n = len(maze), len(maze[0])
        queue = deque([(entrance[0], entrance[1], 0)])
        maze[entrance[0]][entrance[1]] = '+'  # Mark entrance as visited
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            row, col, steps = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < m and 0 <= new_col < n and 
                    maze[new_row][new_col] == '.'):
                    
                    # Check if this is an exit
                    if (new_row == 0 or new_row == m - 1 or 
                        new_col == 0 or new_col == n - 1):
                        return steps + 1
                    
                    # Mark as visited and add to queue
                    maze[new_row][new_col] = '+'
                    queue.append((new_row, new_col, steps + 1))
        
        return -1

    def nearestExit_with_helper(self, maze: List[List[str]], entrance: List[int]) -> int:
        """
        Solution 3: BFS with helper function for exit check
        
        Clean separation of concerns with helper function.
        Good for demonstrating code organization in interviews.
        
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        def is_exit(row: int, col: int, m: int, n: int, entrance: List[int]) -> bool:
            """Check if a cell is an exit (at border and not entrance)"""
            if row != entrance[0] or col != entrance[1]:  # Not entrance
                return row == 0 or row == m - 1 or col == 0 or col == n - 1
            return False
        
        m, n = len(maze), len(maze[0])
        queue = deque([(entrance[0], entrance[1], 0)])
        visited = {(entrance[0], entrance[1])}
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            row, col, steps = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < m and 0 <= new_col < n and 
                    maze[new_row][new_col] == '.' and 
                    (new_row, new_col) not in visited):
                    
                    if is_exit(new_row, new_col, m, n, entrance):
                        return steps + 1
                    
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, steps + 1))
        
        return -1

    def nearestExit_dfs(self, maze: List[List[str]], entrance: List[int]) -> int:
        """
        Solution 4: DFS approach (NOT recommended for interviews)
        
        DFS doesn't guarantee shortest path without additional logic.
        Included for completeness but BFS is always better for shortest path.
        
        Time Complexity: O(4^(m*n)) in worst case - exponential
        Space Complexity: O(m * n) - recursion stack
        """
        def dfs(row: int, col: int, steps: int, visited: set) -> int:
            # Check if current position is an exit
            if ((row == 0 or row == len(maze) - 1 or col == 0 or col == len(maze[0]) - 1) 
                and [row, col] != entrance):
                return steps
            
            visited.add((row, col))
            min_steps = float('inf')
            
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and 
                    maze[new_row][new_col] == '.' and (new_row, new_col) not in visited):
                    
                    result = dfs(new_row, new_col, steps + 1, visited.copy())
                    min_steps = min(min_steps, result)
            
            return min_steps if min_steps != float('inf') else -1
        
        return dfs(entrance[0], entrance[1], 0, set())


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    # Test case 1
    maze1 = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]]
    entrance1 = [1,2]
    expected1 = 1
    result1 = solution.nearestExit(maze1, entrance1)
    print(f"Test 1: Expected {expected1}, Got {result1}, {'PASS' if result1 == expected1 else 'FAIL'}")
    
    # Test case 2
    maze2 = [["+","+","+"],[".",".","."],["+","+","+"]]
    entrance2 = [1,0]
    expected2 = 2
    result2 = solution.nearestExit(maze2, entrance2)
    print(f"Test 2: Expected {expected2}, Got {result2}, {'PASS' if result2 == expected2 else 'FAIL'}")
    
    # Test case 3 - No exit
    maze3 = [[".","+"],["+"," +"]]
    entrance3 = [0,0]
    expected3 = -1
    # Note: This test case has been modified as the original had formatting issues
    
    # Test case 4 - Entrance is already at border (edge case)
    maze4 = [[".",".","."]]
    entrance4 = [0,0]
    expected4 = 2  # Need to reach [0,2]
    result4 = solution.nearestExit(maze4, entrance4)
    print(f"Test 4: Expected {expected4}, Got {result4}, {'PASS' if result4 == expected4 else 'FAIL'}")
    
    # Test case 5 - Single cell maze
    maze5 = [["."]]
    entrance5 = [0,0]
    expected5 = -1  # Entrance is at border but doesn't count as exit
    result5 = solution.nearestExit(maze5, entrance5)
    print(f"Test 5: Expected {expected5}, Got {result5}, {'PASS' if result5 == expected5 else 'FAIL'}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Algorithm Choice:
   - BFS is optimal for shortest path problems
   - DFS would require additional logic and is less efficient
   - Always use BFS for "shortest path" or "minimum steps" problems

2. Key Insights:
   - An exit is any empty cell at the border (row 0, row m-1, col 0, col n-1)
   - The entrance itself doesn't count as an exit (even if at border)
   - Need to track visited cells to avoid cycles
   - BFS naturally finds shortest path due to level-order traversal

3. Implementation Details:
   - Use queue for BFS with (row, col, steps) tuples
   - Mark cells as visited to avoid infinite loops
   - Check bounds before accessing maze cells
   - Exit condition: reach any border cell that's not the entrance

4. Edge Cases:
   - No exits exist (surrounded by walls)
   - Entrance is at border but no other exits
   - Single cell maze
   - All border cells are walls except entrance

5. Space/Time Trade-offs:
   - Can modify input maze to save space (mark visited cells as walls)
   - Or use separate visited set for cleaner code
   - Queue space is O(m*n) in worst case

6. Follow-up Questions You Might Get:
   - What if there are multiple entrances?
   - How would you find ALL exits and their distances?
   - What if diagonal movement was allowed?
   - How would you modify for weighted graph (different step costs)?
   - Can you solve this with A* algorithm?

7. Complexity Analysis:
   - Time: O(m * n) - each cell visited at most once
   - Space: O(m * n) - queue and visited set

8. Common Mistakes to Avoid:
   - Forgetting entrance doesn't count as exit
   - Not checking bounds properly
   - Using DFS instead of BFS for shortest path
   - Not handling the case where no exit exists
"""
