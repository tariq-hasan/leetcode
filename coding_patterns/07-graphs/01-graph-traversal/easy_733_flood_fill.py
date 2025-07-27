"""
LeetCode 733: Flood Fill

Problem: Given a 2D grid, a starting pixel (sr, sc), and a new color, 
perform a flood fill operation starting from the given pixel.

Time Complexity: O(N) where N is the number of pixels in the image
Space Complexity: O(N) in worst case for recursion stack
"""

class Solution:
    def floodFill(self, image, sr, sc, color):
        """
        DFS Recursive Solution - Most intuitive and clean
        """
        if not image or sr < 0 or sr >= len(image) or sc < 0 or sc >= len(image[0]):
            return image
        
        original_color = image[sr][sc]
        
        # Edge case: if new color is same as original, no work needed
        if original_color == color:
            return image
        
        def dfs(r, c):
            # Base cases
            if (r < 0 or r >= len(image) or 
                c < 0 or c >= len(image[0]) or 
                image[r][c] != original_color):
                return
            
            # Fill current pixel
            image[r][c] = color
            
            # Recursively fill 4-directionally connected pixels
            dfs(r + 1, c)  # down
            dfs(r - 1, c)  # up
            dfs(r, c + 1)  # right
            dfs(r, c - 1)  # left
        
        dfs(sr, sc)
        return image

    def floodFillIterative(self, image, sr, sc, color):
        """
        BFS Iterative Solution - Better for deep recursion scenarios
        """
        if not image or sr < 0 or sr >= len(image) or sc < 0 or sc >= len(image[0]):
            return image
        
        original_color = image[sr][sc]
        
        if original_color == color:
            return image
        
        from collections import deque
        
        queue = deque([(sr, sc)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            r, c = queue.popleft()
            
            # Skip if out of bounds or different color
            if (r < 0 or r >= len(image) or 
                c < 0 or c >= len(image[0]) or 
                image[r][c] != original_color):
                continue
            
            # Fill current pixel
            image[r][c] = color
            
            # Add neighbors to queue
            for dr, dc in directions:
                queue.append((r + dr, c + dc))
        
        return image

    def floodFillOptimized(self, image, sr, sc, color):
        """
        Optimized DFS with bounds checking upfront
        """
        if (not image or not image[0] or 
            sr < 0 or sr >= len(image) or 
            sc < 0 or sc >= len(image[0])):
            return image
        
        original_color = image[sr][sc]
        
        if original_color == color:
            return image
        
        rows, cols = len(image), len(image[0])
        
        def dfs(r, c):
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                image[r][c] != original_color):
                return
            
            image[r][c] = color
            
            # Use list comprehension for cleaner code
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc)
        
        dfs(sr, sc)
        return image


# Test cases for interview
def test_flood_fill():
    solution = Solution()
    
    # Test case 1: Basic flood fill
    image1 = [[1,1,1],[1,1,0],[1,0,1]]
    result1 = solution.floodFill(image1, 1, 1, 2)
    print("Test 1:", result1)  # Expected: [[2,2,2],[2,2,0],[2,0,1]]
    
    # Test case 2: Single pixel
    image2 = [[0,0,0],[0,1,1]]
    result2 = solution.floodFill(image2, 1, 1, 1)
    print("Test 2:", result2)  # Expected: [[0,0,0],[0,1,1]] (no change)
    
    # Test case 3: Edge pixel
    image3 = [[1,1,1],[1,1,0],[1,0,1]]
    result3 = solution.floodFill(image3, 0, 0, 2)
    print("Test 3:", result3)  # Expected: [[2,2,2],[2,2,0],[2,0,1]]

if __name__ == "__main__":
    test_flood_fill()


"""
Key Interview Points to Discuss:

1. APPROACH EXPLANATION:
   - Classic graph traversal problem using DFS or BFS
   - Need to change all connected pixels of same color to new color
   - 4-directional connectivity (up, down, left, right)

2. EDGE CASES TO MENTION:
   - Empty image or invalid coordinates
   - New color same as original color (optimization)
   - Single pixel image
   - Starting pixel at boundary

3. TIME/SPACE COMPLEXITY:
   - Time: O(N) where N is number of pixels
   - Space: O(N) worst case for recursion stack (entire image is same color)

4. FOLLOW-UP QUESTIONS TO EXPECT:
   - "What if the image is very large?" -> Use iterative BFS to avoid stack overflow
   - "Can you optimize space?" -> Iterative solution uses O(W*H) queue space but avoids recursion
   - "What about 8-directional connectivity?" -> Add diagonal directions
   - "How to handle different data types?" -> Template/generic solution

5. CODE STYLE POINTS:
   - Clean variable names (sr, sc for start row/column)
   - Proper bounds checking
   - Early termination for optimization
   - Clear separation of concerns

6. ALTERNATIVE APPROACHES:
   - Union-Find (overkill for this problem)
   - Two-pass algorithm with marking (unnecessarily complex)
"""
