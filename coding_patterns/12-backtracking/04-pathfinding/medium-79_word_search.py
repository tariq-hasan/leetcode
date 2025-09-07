"""
LeetCode 79: Word Search
Medium Difficulty

Problem:
Given an m x n grid of characters board and a string word, return true if word 
exists in the grid. The word can be constructed from letters of sequentially 
adjacent cells, where adjacent cells are horizontally or vertically neighboring. 
The same letter cell may not be used more than once.

Example:
board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true

Time Complexity: O(N * 4^L) where N is number of cells, L is length of word
Space Complexity: O(L) for recursion stack
"""

class Solution:
    def exist(self, board, word):
        """
        Main approach: DFS + Backtracking
        
        For each cell in the board, try to start the word search from that cell.
        Use DFS to explore all possible paths while marking visited cells.
        Backtrack by unmarking cells when returning from recursion.
        """
        if not board or not board[0] or not word:
            return False
        
        rows, cols = len(board), len(board[0])
        
        def dfs(row, col, index):
            # Base case: found the complete word
            if index == len(word):
                return True
            
            # Boundary checks and character match
            if (row < 0 or row >= rows or 
                col < 0 or col >= cols or 
                board[row][col] != word[index] or 
                board[row][col] == '#'):  # '#' means visited
                return False
            
            # Mark current cell as visited
            temp = board[row][col]
            board[row][col] = '#'
            
            # Explore all 4 directions
            found = (dfs(row + 1, col, index + 1) or    # down
                    dfs(row - 1, col, index + 1) or     # up
                    dfs(row, col + 1, index + 1) or     # right
                    dfs(row, col - 1, index + 1))       # left
            
            # Backtrack: restore the original character
            board[row][col] = temp
            
            return found
        
        # Try starting from each cell
        for i in range(rows):
            for j in range(cols):
                if dfs(i, j, 0):
                    return True
        
        return False


# Alternative Solution: Using visited set instead of modifying board
class SolutionWithVisitedSet:
    def exist(self, board, word):
        """
        Alternative approach using visited set to track visited cells
        This doesn't modify the original board
        """
        if not board or not board[0] or not word:
            return False
        
        rows, cols = len(board), len(board[0])
        
        def dfs(row, col, index, visited):
            if index == len(word):
                return True
            
            if (row < 0 or row >= rows or 
                col < 0 or col >= cols or 
                (row, col) in visited or 
                board[row][col] != word[index]):
                return False
            
            visited.add((row, col))
            
            # Explore 4 directions
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                if dfs(row + dr, col + dc, index + 1, visited):
                    visited.remove((row, col))  # Backtrack
                    return True
            
            visited.remove((row, col))  # Backtrack
            return False
        
        for i in range(rows):
            for j in range(cols):
                if dfs(i, j, 0, set()):
                    return True
        
        return False


# Optimized Solution with early termination
class OptimizedSolution:
    def exist(self, board, word):
        """
        Optimized version with early termination checks
        """
        if not board or not board[0] or not word:
            return False
        
        rows, cols = len(board), len(board[0])
        
        # Early termination: check if all characters in word exist in board
        from collections import Counter
        board_count = Counter()
        for row in board:
            for char in row:
                board_count[char] += 1
        
        word_count = Counter(word)
        for char, count in word_count.items():
            if board_count[char] < count:
                return False
        
        # Optimization: start from the less frequent character end
        if word_count[word[0]] > word_count[word[-1]]:
            word = word[::-1]
        
        def dfs(row, col, index):
            if index == len(word):
                return True
            
            if (row < 0 or row >= rows or 
                col < 0 or col >= cols or 
                board[row][col] != word[index]):
                return False
            
            temp = board[row][col]
            board[row][col] = '#'
            
            found = (dfs(row + 1, col, index + 1) or
                    dfs(row - 1, col, index + 1) or
                    dfs(row, col + 1, index + 1) or
                    dfs(row, col - 1, index + 1))
            
            board[row][col] = temp
            return found
        
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == word[0] and dfs(i, j, 0):
                    return True
        
        return False


# Test cases
def test_solutions():
    # Test case 1
    board1 = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    word1 = "ABCCED"
    
    # Test case 2
    board2 = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    word2 = "SEE"
    
    # Test case 3
    board3 = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    word3 = "ABCB"
    
    sol = Solution()
    print(f"Test 1: {sol.exist(board1, word1)}")  # True
    print(f"Test 2: {sol.exist(board2, word2)}")  # True  
    print(f"Test 3: {sol.exist(board3, word3)}")  # False


# Interview talking points:
"""
Key Points to Mention in Interview:

1. **Algorithm Choice**: 
   - DFS + Backtracking is the optimal approach
   - Need to explore all possible paths from each starting position

2. **Time Complexity**: 
   - O(N * 4^L) where N = number of cells, L = word length
   - In worst case, explore 4 directions for each character in word

3. **Space Complexity**: 
   - O(L) for recursion stack depth
   - If using visited set: O(L) additional space

4. **Key Optimizations**:
   - Mark cells as visited during DFS to avoid cycles
   - Backtrack properly to allow other paths to use the cell
   - Early termination if character counts don't match
   - Start from less frequent character end

5. **Edge Cases**:
   - Empty board or word
   - Single character word/board
   - Word longer than total cells
   - All same characters

6. **Alternative Approaches**:
   - Trie-based solution for multiple words (Word Search II)
   - BFS (less efficient due to path tracking complexity)
"""

if __name__ == "__main__":
    test_solutions()
