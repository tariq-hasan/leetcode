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


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Iterative DFS Solution for Walls and Gates

        Time Complexity: O(m*n) where m is number of rows and n is number of columns
        Space Complexity: O(m*n) for the stack in worst case
        """
        rows, cols = len(rooms), len(rooms[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        # First, collect all gate positions
        gates = []
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    gates.append((r, c))

        # For each gate, perform DFS
        for gate_r, gate_c in gates:
            stack = [(gate_r, gate_c, 0)]  # (row, col, distance)

            # Use a visited set to avoid revisiting cells in this DFS
            visited = set([(gate_r, gate_c)])

            while stack:
                r, c, distance = stack.pop()

                # Update distance (not needed for gate itself)
                if distance > 0:
                    rooms[r][c] = min(rooms[r][c], distance)

                # Check all four directions
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        (nr, nc) not in visited and
                        rooms[nr][nc] != -1 and rooms[nr][nc] != 0):
                        # Only visit if it's an empty room and not visited yet
                        if distance + 1 < rooms[nr][nc]:
                            stack.append((nr, nc, distance + 1))
                            visited.add((nr, nc))


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Iterative BFS Solution for Walls and Gates

        Time Complexity: O(m*n) where m is number of rows and n is number of columns
        Space Complexity: O(m*n) for the queue in worst case
        """
        rows, cols = len(rooms), len(rooms[0])
        INF = 2147483647  # Value representing empty room

        queue = deque()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        # Add all gates to the queue with distance 0
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:  # Found a gate
                    queue.append((r, c, 0))  # (row, col, distance)

        # BFS
        while queue:
            r, c, distance = queue.popleft()

            # Check all four directions
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Only process if it's an unexplored empty room
                if (0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF):
                    rooms[nr][nc] = distance + 1
                    queue.append((nr, nc, distance + 1))
