from collections import deque
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Recursive DFS Solution for Surrounded Regions

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(M*N) for the recursion stack in worst case
        """
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int) -> None:
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
                return

            # Mark as safe ('T' for temporary)
            board[r][c] = 'T'

            # Check all four directions
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left

        # Step 1: Mark unsurrounded regions (connected to border)
        # Process borders only
        for r in range(rows):
            dfs(r, 0)          # First column
            dfs(r, cols - 1)   # Last column

        for c in range(cols):
            dfs(0, c)          # First row
            dfs(rows - 1, c)   # Last row

        # Step 2: Flip all cells - 'O' to 'X', 'T' back to 'O'
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'      # Surrounded, flip
                elif board[r][c] == 'T':
                    board[r][c] = 'O'      # Unsurrounded, restore
