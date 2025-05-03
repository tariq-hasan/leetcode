from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Recursive DFS Solution for Number of Islands

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(M*N) for the recursion stack in worst case
        """
        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(r: int, c: int) -> None:
            # Base case: out of bounds or not land
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
                return

            # Mark as visited
            grid[r][c] = '0'

            # Explore four adjacent cells
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left

        # Scan the grid to find islands
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1  # Found a new island
                    dfs(r, c)     # Mark all connected land cells

        return islands


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Iterative DFS Solution for Number of Islands

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(M*N) for the stack in worst case
        """
        rows, cols = len(grid), len(grid[0])
        islands = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1  # Found a new island

                    # Start DFS from this land cell
                    stack = [(r, c)]
                    grid[r][c] = '0'  # Mark as visited immediately

                    while stack:
                        cur_r, cur_c = stack.pop()

                        # Check all adjacent cells
                        for dr, dc in directions:
                            nr, nc = cur_r + dr, cur_c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                                stack.append((nr, nc))
                                grid[nr][nc] = '0'  # Mark as visited when adding to stack

        return islands


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Iterative BFS Solution for Number of Islands

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(min(M,N)) - at most size of the largest island in queue
        """
        rows, cols = len(grid), len(grid[0])
        islands = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1  # Found a new island

                    # Start BFS from this land cell
                    queue = deque([(r, c)])
                    grid[r][c] = '0'  # Mark as visited immediately

                    while queue:
                        cur_r, cur_c = queue.popleft()

                        # Check all adjacent cells
                        for dr, dc in directions:
                            nr, nc = cur_r + dr, cur_c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                                queue.append((nr, nc))
                                grid[nr][nc] = '0'  # Mark as visited when adding to queue

        return islands
