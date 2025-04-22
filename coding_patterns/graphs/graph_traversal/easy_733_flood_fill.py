from collections import deque
from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        """
        DFS (Depth-First Search) - Recursive

        Time Complexity: O(N), where N is the number of pixels in the image.
        We might process every pixel once.

        Space Complexity: O(N) in worst case for the recursion stack.
        In a fully connected image with the same original color, the recursion
        stack could grow to include all pixels.
        """
        rows, cols = len(image), len(image[0])
        original_color = image[sr][sc]

        # Early return if the starting pixel is already the target color
        if original_color == color:
            return image

        def dfs(r, c):
            # Check boundaries and if current pixel has the original color
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                image[r][c] != original_color):
                return

            # Change color of the current pixel
            image[r][c] = color

            # Explore the four adjacent pixels
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left

        dfs(sr, sc)
        return image


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        """
        DFS - Iterative (Using Stack)

        Time Complexity: O(N), where N is the number of pixels in the image.
        We process each pixel at most once.

        Space Complexity: O(N) for the stack in worst case.
        The stack might need to store many pixel coordinates in a large connected area.
        """
        rows, cols = len(image), len(image[0])
        original_color = image[sr][sc]

        # Early return if starting pixel is already the target color
        if original_color == color:
            return image

        stack = [(sr, sc)]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        while stack:
            r, c = stack.pop()

            # Only process uncolored pixels with the original color
            if image[r][c] == original_color:
                image[r][c] = color

                # Add valid neighbors to stack
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        image[nr][nc] == original_color):
                        stack.append((nr, nc))

        return image


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        """
        BFS (Breadth-First Search)

        Time Complexity: O(N), where N is the number of pixels in the image.
        We process each pixel at most once.

        Space Complexity: O(N) for the queue in worst case.
        The queue size depends on the breadth of the connected area with the original color.
        """
        rows, cols = len(image), len(image[0])
        original_color = image[sr][sc]

        # Early return if starting pixel is already the target color
        if original_color == color:
            return image

        queue = deque([(sr, sc)])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        while queue:
            r, c = queue.popleft()

            # Only process uncolored pixels with the original color
            if image[r][c] == original_color:
                image[r][c] = color

                # Add valid neighbors to queue
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        image[nr][nc] == original_color):
                        queue.append((nr, nc))

        return image
