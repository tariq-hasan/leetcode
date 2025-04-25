from collections import deque
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Recursive DFS Solution for Surrounded Regions

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(M*N) for the recursion stack in worst case
        """
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


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Iterative DFS Solution for Surrounded Regions

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(M*N) for the stack in worst case
        """
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])
        stack = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        # Add border 'O's to stack and mark immediately
        for r in range(rows):
            if board[r][0] == 'O':
                stack.append((r, 0))
                board[r][0] = 'T'
            if board[r][cols-1] == 'O':
                stack.append((r, cols-1))
                board[r][cols-1] = 'T'

        for c in range(cols):
            if board[0][c] == 'O':
                stack.append((0, c))
                board[0][c] = 'T'
            if board[rows-1][c] == 'O':
                stack.append((rows-1, c))
                board[rows-1][c] = 'T'

        # Process stack - mark all connected 'O's
        while stack:
            r, c = stack.pop()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O':
                    board[nr][nc] = 'T'    # Mark as safe
                    stack.append((nr, nc))

        # Flip remaining 'O's to 'X' and restore 'T's to 'O'
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'      # Surrounded, flip
                elif board[r][c] == 'T':
                    board[r][c] = 'O'      # Unsurrounded, restore


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Iterative BFS Solution for Surrounded Regions

        Time Complexity: O(M*N) where M is number of rows and N is number of columns
        Space Complexity: O(min(M, N)) - at most the border cells in queue
        """
        rows, cols = len(board), len(board[0])
        queue = deque()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        # Add border 'O's to queue and mark immediately
        for r in range(rows):
            if board[r][0] == 'O':
                queue.append((r, 0))
                board[r][0] = 'T'
            if board[r][cols-1] == 'O':
                queue.append((r, cols-1))
                board[r][cols-1] = 'T'

        for c in range(cols):
            if board[0][c] == 'O':
                queue.append((0, c))
                board[0][c] = 'T'
            if board[rows-1][c] == 'O':
                queue.append((rows-1, c))
                board[rows-1][c] = 'T'

        # Process queue - mark all connected 'O's
        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O':
                    board[nr][nc] = 'T'    # Mark as safe
                    queue.append((nr, nc))

        # Flip remaining 'O's to 'X' and restore 'T's to 'O'
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'      # Surrounded, flip
                elif board[r][c] == 'T':
                    board[r][c] = 'O'      # Unsurrounded, restore
