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
