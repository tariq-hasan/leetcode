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
