"""
LeetCode 529: Minesweeper

Problem Statement:
You are given an m x n char matrix board representing the game board where:
- 'M' represents an unrevealed mine
- 'E' represents an unrevealed empty square
- 'B' represents a revealed blank square that has no adjacent mines
- digit ('1' to '8') represents how many mines are adjacent to this revealed square
- 'X' represents a revealed mine

Given a board and a click position [click_r, click_c], return the board after revealing this position according to the following rules:
1. If a mine 'M' is revealed, then the game is over. You should change it to 'X'.
2. If an empty square 'E' with no adjacent mines is revealed, then change it to 'B' and all of its adjacent unrevealed squares should be revealed recursively.
3. If an empty square 'E' with at least one adjacent mine is revealed, then change it to a digit ('1' to '8') representing the number of adjacent mines.
4. Return the board when no more squares will be revealed.
"""

from typing import List

class Solution:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        """
        DFS Solution - Most intuitive and commonly expected in interviews
        Time Complexity: O(m * n) in worst case
        Space Complexity: O(m * n) for recursion stack
        """
        if not board or not board[0]:
            return board
        
        m, n = len(board), len(board[0])
        r, c = click[0], click[1]
        
        # Directions for 8 adjacent cells (including diagonals)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        def dfs(r, c):
            # Base case: out of bounds or already revealed
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != 'E':
                return
            
            # Count adjacent mines
            mine_count = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 'M':
                    mine_count += 1
            
            if mine_count > 0:
                # Has adjacent mines - mark with count
                board[r][c] = str(mine_count)
            else:
                # No adjacent mines - mark as blank and continue DFS
                board[r][c] = 'B'
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    dfs(nr, nc)
        
        # Handle the clicked cell
        if board[r][c] == 'M':
            # Hit a mine - game over
            board[r][c] = 'X'
        elif board[r][c] == 'E':
            # Empty cell - start DFS
            dfs(r, c)
        
        return board

class SolutionBFS:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        """
        BFS Solution - Alternative approach using queue
        Time Complexity: O(m * n)
        Space Complexity: O(m * n) for queue
        """
        if not board or not board[0]:
            return board
        
        from collections import deque
        
        m, n = len(board), len(board[0])
        r, c = click[0], click[1]
        
        # If clicked on mine, game over
        if board[r][c] == 'M':
            board[r][c] = 'X'
            return board
        
        # BFS for empty cells
        queue = deque([(r, c)])
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        while queue:
            curr_r, curr_c = queue.popleft()
            
            # Skip if already processed or not empty
            if board[curr_r][curr_c] != 'E':
                continue
            
            # Count adjacent mines
            mine_count = 0
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 'M':
                    mine_count += 1
            
            if mine_count > 0:
                # Has adjacent mines
                board[curr_r][curr_c] = str(mine_count)
            else:
                # No adjacent mines - reveal and add neighbors to queue
                board[curr_r][curr_c] = 'B'
                for dr, dc in directions:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 'E':
                        queue.append((nr, nc))
        
        return board

# Test cases
def test_solution():
    sol = Solution()
    
    # Test case 1: Click on empty cell with adjacent mines
    board1 = [['E', 'E', 'E', 'E', 'E'],
              ['E', 'E', 'M', 'E', 'E'],
              ['E', 'E', 'E', 'E', 'E'],
              ['E', 'E', 'E', 'E', 'E']]
    click1 = [3, 0]
    result1 = sol.updateBoard(board1, click1)
    print("Test 1:")
    for row in result1:
        print(row)
    print()
    
    # Test case 2: Click on mine
    board2 = [['B', '1', 'E', '1', 'B'],
              ['B', '1', 'M', '1', 'B'],
              ['B', '1', '1', '1', 'B'],
              ['B', 'B', 'B', 'B', 'B']]
    click2 = [1, 2]
    result2 = sol.updateBoard(board2, click2)
    print("Test 2:")
    for row in result2:
        print(row)

if __name__ == "__main__":
    test_solution()

class SolutionIterativeDFS:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        """
        Iterative DFS Solution - Avoids recursion stack overflow for large boards
        Time Complexity: O(m * n)
        Space Complexity: O(m * n) for explicit stack
        """
        if not board or not board[0]:
            return board
        
        m, n = len(board), len(board[0])
        r, c = click[0], click[1]
        
        # If clicked on mine, game over
        if board[r][c] == 'M':
            board[r][c] = 'X'
            return board
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        stack = [(r, c)]
        
        while stack:
            curr_r, curr_c = stack.pop()
            
            # Skip if out of bounds or not empty
            if (curr_r < 0 or curr_r >= m or curr_c < 0 or curr_c >= n or 
                board[curr_r][curr_c] != 'E'):
                continue
            
            # Count adjacent mines
            mine_count = 0
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 'M':
                    mine_count += 1
            
            if mine_count > 0:
                # Has adjacent mines
                board[curr_r][curr_c] = str(mine_count)
            else:
                # No adjacent mines - reveal and add neighbors to stack
                board[curr_r][curr_c] = 'B'
                for dr, dc in directions:
                    nr, nc = curr_r + dr, curr_c + dc
                    stack.append((nr, nc))
        
        return board

# Java Implementation (commonly asked in interviews)
java_solution = '''
class Solution {
    private int[][] directions = {{-1,-1}, {-1,0}, {-1,1}, {0,-1}, {0,1}, {1,-1}, {1,0}, {1,1}};
    
    public char[][] updateBoard(char[][] board, int[] click) {
        int m = board.length, n = board[0].length;
        int r = click[0], c = click[1];
        
        if (board[r][c] == 'M') {
            board[r][c] = 'X';
            return board;
        }
        
        dfs(board, r, c, m, n);
        return board;
    }
    
    private void dfs(char[][] board, int r, int c, int m, int n) {
        if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] != 'E') {
            return;
        }
        
        int mineCount = 0;
        for (int[] dir : directions) {
            int nr = r + dir[0], nc = c + dir[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && board[nr][nc] == 'M') {
                mineCount++;
            }
        }
        
        if (mineCount > 0) {
            board[r][c] = (char) ('0' + mineCount);
        } else {
            board[r][c] = 'B';
            for (int[] dir : directions) {
                int nr = r + dir[0], nc = c + dir[1];
                dfs(board, nr, nc, m, n);
            }
        }
    }
}
'''

"""
Key Interview Points to Discuss:

1. **Algorithm Choice**: DFS is more intuitive and commonly expected. BFS works too but uses more memory.

2. **Edge Cases to Consider**:
   - Clicking on already revealed cells (should do nothing)
   - Clicking on mines vs empty cells
   - Board boundaries
   - Empty board
   - Single cell board

3. **Optimization Opportunities**:
   - Early termination when clicking revealed cells
   - Avoid revisiting cells in BFS by marking them
   - Use iterative DFS for very large boards to avoid stack overflow

4. **Time/Space Complexity**:
   - Time: O(m * n) in worst case when revealing entire board
   - Space: O(m * n) for recursion stack (DFS) or queue (BFS)

5. **Follow-up Questions**:
   - How would you handle a very large board? (Use iterative DFS)
   - How would you implement undo functionality? (Keep history of changes)
   - How would you optimize for sparse mine distribution? (Same approach works well)
   - What if we need to support multiple clicks? (Apply same logic repeatedly)

6. **Common Mistakes to Avoid**:
   - Forgetting to check bounds when counting adjacent mines
   - Not handling the mine click case properly
   - Infinite recursion due to incorrect base cases
   - Off-by-one errors in direction arrays

The DFS solution is typically preferred in interviews due to its clean recursive structure
and intuitive logic flow that mirrors the game mechanics. Be prepared to code it in both
Python and Java, and discuss the iterative version as an optimization.
"""
