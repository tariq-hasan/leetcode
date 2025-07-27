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
















"""
LeetCode 130: Surrounded Regions

Problem: Given a 2D board containing 'X' and 'O', capture all regions 
surrounded by 'X'. A region is captured by flipping all 'O's into 'X's 
in that surrounded region.

Key Insight: Instead of finding surrounded regions, find UN-surrounded regions
(those connected to the border) and mark them as safe.

Time Complexity: O(M*N) where M and N are board dimensions
Space Complexity: O(M*N) for recursion stack in worst case
"""

class Solution:
    def solve(self, board):
        """
        DFS Solution - Mark border-connected 'O's as safe, then flip the rest
        This is the most intuitive approach for interviews
        """
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])
        
        def dfs(r, c):
            # Base cases: out of bounds or not an 'O'
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                board[r][c] != 'O'):
                return
            
            # Mark as safe (temporarily use '#')
            board[r][c] = '#'
            
            # Explore all 4 directions
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        # Step 1: Mark all border-connected 'O's as safe
        # Check first and last rows
        for c in range(cols):
            if board[0][c] == 'O':
                dfs(0, c)
            if board[rows-1][c] == 'O':
                dfs(rows-1, c)
        
        # Check first and last columns
        for r in range(rows):
            if board[r][0] == 'O':
                dfs(r, 0)
            if board[r][cols-1] == 'O':
                dfs(r, cols-1)
        
        # Step 2: Process the entire board
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'  # Surrounded, capture it
                elif board[r][c] == '#':
                    board[r][c] = 'O'  # Safe, restore it

    def solveIterative(self, board):
        """
        BFS Iterative Solution - Better for very large boards
        """
        if not board or not board[0]:
            return
        
        from collections import deque
        
        rows, cols = len(board), len(board[0])
        queue = deque()
        
        # Add all border 'O's to queue
        for r in range(rows):
            for c in range(cols):
                if ((r == 0 or r == rows-1 or c == 0 or c == cols-1) and 
                    board[r][c] == 'O'):
                    queue.append((r, c))
                    board[r][c] = '#'  # Mark as safe immediately
        
        # BFS to mark all connected 'O's as safe
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    board[nr][nc] == 'O'):
                    board[nr][nc] = '#'
                    queue.append((nr, nc))
        
        # Final pass: capture surrounded regions and restore safe ones
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == '#':
                    board[r][c] = 'O'

    def solveUnionFind(self, board):
        """
        Union-Find Solution - Advanced approach, good for follow-up discussion
        """
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])
        
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n
            
            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]
            
            def union(self, x, y):
                px, py = self.find(x), self.find(y)
                if px == py:
                    return
                if self.rank[px] < self.rank[py]:
                    px, py = py, px
                self.parent[py] = px
                if self.rank[px] == self.rank[py]:
                    self.rank[px] += 1
            
            def connected(self, x, y):
                return self.find(x) == self.find(y)
        
        # Create dummy node for border-connected regions
        dummy = rows * cols
        uf = UnionFind(rows * cols + 1)
        
        def get_index(r, c):
            return r * cols + c
        
        # Union all 'O's with their neighbors and border 'O's with dummy
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    # If on border, union with dummy
                    if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                        uf.union(get_index(r, c), dummy)
                    
                    # Union with adjacent 'O's
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < rows and 0 <= nc < cols and 
                            board[nr][nc] == 'O'):
                            uf.union(get_index(r, c), get_index(nr, nc))
        
        # Capture all 'O's not connected to border
        for r in range(rows):
            for c in range(cols):
                if (board[r][c] == 'O' and 
                    not uf.connected(get_index(r, c), dummy)):
                    board[r][c] = 'X'

    def solveOptimized(self, board):
        """
        Space-optimized DFS with iterative stack to avoid recursion limits
        """
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])
        stack = []
        
        # Add all border 'O's to stack
        for r in range(rows):
            for c in range(cols):
                if ((r == 0 or r == rows-1 or c == 0 or c == cols-1) and 
                    board[r][c] == 'O'):
                    stack.append((r, c))
        
        # Iterative DFS to mark safe regions
        while stack:
            r, c = stack.pop()
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                board[r][c] != 'O'):
                continue
            
            board[r][c] = '#'  # Mark as safe
            
            # Add neighbors to stack
            stack.extend([(r+1, c), (r-1, c), (r, c+1), (r, c-1)])
        
        # Final processing
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == '#':
                    board[r][c] = 'O'


# Test cases for interview
def test_surrounded_regions():
    def print_board(board, title):
        print(f"\n{title}:")
        for row in board:
            print(''.join(row))
    
    solution = Solution()
    
    # Test case 1: Standard case
    board1 = [
        ['X','X','X','X'],
        ['X','O','O','X'],
        ['X','X','O','X'],
        ['X','O','X','X']
    ]
    print_board(board1, "Test 1 - Before")
    solution.solve([row[:] for row in board1])  # Create copy
    board1_copy = [row[:] for row in board1]
    solution.solve(board1_copy)
    print_board(board1_copy, "Test 1 - After")
    
    # Test case 2: Border connected
    board2 = [
        ['O','X','X','O'],
        ['X','O','O','X'],
        ['X','X','O','X'],
        ['X','O','X','X']
    ]
    print_board(board2, "Test 2 - Before")
    board2_copy = [row[:] for row in board2]
    solution.solve(board2_copy)
    print_board(board2_copy, "Test 2 - After")
    
    # Test case 3: All X's
    board3 = [['X','X'],['X','X']]
    print_board(board3, "Test 3 - Before")
    board3_copy = [row[:] for row in board3]
    solution.solve(board3_copy)
    print_board(board3_copy, "Test 3 - After")

if __name__ == "__main__":
    test_surrounded_regions()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Don't directly find surrounded regions (complex)
   - Instead, find UN-surrounded regions (border-connected)
   - Use "reverse thinking" - mark safe regions first

2. ALGORITHM STEPS:
   - Mark border-connected 'O's as safe (use temporary marker '#')
   - Capture remaining 'O's (turn to 'X')
   - Restore safe 'O's (turn '#' back to 'O')

3. WHY THIS APPROACH WORKS:
   - Any 'O' connected to border cannot be surrounded
   - Only isolated 'O' regions can be captured
   - Simpler than checking if each region is fully enclosed

4. EDGE CASES TO MENTION:
   - Empty board
   - All X's or all O's
   - Single row/column
   - Border entirely O's

5. TIME/SPACE COMPLEXITY:
   - Time: O(M*N) - visit each cell at most twice
   - Space: O(M*N) worst case for recursion/queue

6. FOLLOW-UP QUESTIONS:
   - "What if board is huge?" -> Use iterative BFS/DFS
   - "Memory constraints?" -> In-place with temporary markers
   - "Multiple queries?" -> Union-Find for preprocessing
   - "8-directional?" -> Add diagonal directions

7. COMPARISON WITH FLOOD FILL:
   - Similar DFS/BFS traversal
   - Different goal: mark safe vs. change color
   - Multi-pass algorithm vs. single pass

8. ALTERNATIVE APPROACHES:
   - Union-Find: More complex but handles dynamic queries
   - Two-pass marking: Similar idea, different implementation
   - Topological approach: Overkill for this problem
"""
