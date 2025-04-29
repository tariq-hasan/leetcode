from collections import deque
from typing import List


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Recursive DFS Solution for Walls and Gates

        Time Complexity: O(m*n) where m is number of rows and n is number of columns
        Space Complexity: O(m*n) for the recursion stack in worst case
        """
        rows, cols = len(rooms), len(rooms[0])

        def dfs(r: int, c: int, distance: int) -> None:
            # If out of bounds, wall, gate, or already found shorter path
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                rooms[r][c] == -1 or rooms[r][c] == 0 or rooms[r][c] <= distance):
                return

            # Update distance
            rooms[r][c] = distance

            # Explore four directions
            dfs(r + 1, c, distance + 1)  # Down
            dfs(r - 1, c, distance + 1)  # Up
            dfs(r, c + 1, distance + 1)  # Right
            dfs(r, c - 1, distance + 1)  # Left

        # Start DFS from each gate
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:  # Found a gate
                    dfs(r + 1, c, 1)  # Start one step away from the gate
                    dfs(r - 1, c, 1)
                    dfs(r, c + 1, 1)
                    dfs(r, c - 1, 1)
