"""
LeetCode 51: N-Queens
Hard Difficulty

Problem:
The n-queens puzzle is the problem of placing n chess queens on an n×n chessboard 
such that no two queens attack each other. Given an integer n, return all distinct 
solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, 
where 'Q' and '.' both indicate a queen and an empty space, respectively.

Example:
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]

Time Complexity: O(N!) - exponential
Space Complexity: O(N) for recursion stack and board state
"""

from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Main approach: Backtracking with conflict detection
        
        Key insight: Queens attack horizontally, vertically, and diagonally.
        - Row conflicts: handled by placing one queen per row
        - Column conflicts: track occupied columns
        - Diagonal conflicts: track occupied diagonals
        """
        result = []
        board = ['.' * n for _ in range(n)]
        
        # Track conflicts efficiently
        cols = set()           # occupied columns
        diag1 = set()          # occupied diagonals (row - col)
        diag2 = set()          # occupied anti-diagonals (row + col)
        
        def backtrack(row):
            # Base case: placed all queens
            if row == n:
                result.append(board[:])  # Make a copy
                return
            
            # Try placing queen in each column of current row
            for col in range(n):
                # Check if position is under attack
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                # Place queen
                board[row] = board[row][:col] + 'Q' + board[row][col+1:]
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                # Recurse to next row
                backtrack(row + 1)
                
                # Backtrack: remove queen
                board[row] = board[row][:col] + '.' + board[row][col+1:]
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
        
        backtrack(0)
        return result


class OptimizedSolution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Optimized version using position array instead of string manipulation
        This is more efficient for large n
        """
        result = []
        positions = [-1] * n  # positions[i] = column of queen in row i
        
        cols = set()
        diag1 = set()
        diag2 = set()
        
        def backtrack(row):
            if row == n:
                # Convert positions to board representation
                board = []
                for i in range(n):
                    line = ['.'] * n
                    line[positions[i]] = 'Q'
                    board.append(''.join(line))
                result.append(board)
                return
            
            for col in range(n):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                # Place queen
                positions[row] = col
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                backtrack(row + 1)
                
                # Backtrack
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
        
        backtrack(0)
        return result


class BitManipulationSolution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Ultra-optimized version using bit manipulation
        Most efficient for competitive programming but harder to understand
        """
        result = []
        positions = [-1] * n
        
        def backtrack(row, cols, diag1, diag2):
            if row == n:
                board = []
                for i in range(n):
                    line = ['.'] * n
                    line[positions[i]] = 'Q'
                    board.append(''.join(line))
                result.append(board)
                return
            
            # Available positions are where all three bitmasks are 0
            available = ~(cols | diag1 | diag2) & ((1 << n) - 1)
            
            while available:
                # Get rightmost available position
                pos = available & -available
                available ^= pos  # Remove this position
                
                col = pos.bit_length() - 1
                positions[row] = col
                
                backtrack(row + 1,
                         cols | pos,
                         (diag1 | pos) << 1,
                         (diag2 | pos) >> 1)
        
        backtrack(0, 0, 0, 0)
        return result


class SolutionWithValidation:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Version with explicit validation function - good for explaining logic
        """
        result = []
        board = [['.' for _ in range(n)] for _ in range(n)]
        
        def is_safe(row, col):
            """Check if placing queen at (row, col) is safe"""
            # Check column
            for i in range(row):
                if board[i][col] == 'Q':
                    return False
            
            # Check diagonal (top-left to bottom-right)
            i, j = row - 1, col - 1
            while i >= 0 and j >= 0:
                if board[i][j] == 'Q':
                    return False
                i -= 1
                j -= 1
            
            # Check anti-diagonal (top-right to bottom-left)
            i, j = row - 1, col + 1
            while i >= 0 and j < n:
                if board[i][j] == 'Q':
                    return False
                i -= 1
                j += 1
            
            return True
        
        def backtrack(row):
            if row == n:
                result.append([''.join(row) for row in board])
                return
            
            for col in range(n):
                if is_safe(row, col):
                    board[row][col] = 'Q'
                    backtrack(row + 1)
                    board[row][col] = '.'  # Backtrack
        
        backtrack(0)
        return result


# Related problem: N-Queens II (count solutions only)
class NQueensII:
    def totalNQueens(self, n: int) -> int:
        """
        Optimized version that only counts solutions without storing them
        """
        def backtrack(row, cols, diag1, diag2):
            if row == n:
                return 1
            
            count = 0
            available = ~(cols | diag1 | diag2) & ((1 << n) - 1)
            
            while available:
                pos = available & -available
                available ^= pos
                
                count += backtrack(row + 1,
                                 cols | pos,
                                 (diag1 | pos) << 1,
                                 (diag2 | pos) >> 1)
            return count
        
        return backtrack(0, 0, 0, 0)


def test_solutions():
    """Test all solutions with sample inputs"""
    test_cases = [1, 4, 8]
    
    for n in test_cases:
        sol = Solution()
        result = sol.solveNQueens(n)
        print(f"N-Queens for n={n}: {len(result)} solutions")
        
        if n == 4:
            print("Sample solutions:")
            for i, solution in enumerate(result):
                print(f"Solution {i + 1}:")
                for row in solution:
                    print(row)
                print()


# Performance comparison function
def compare_performance():
    """Compare different implementations (for interview discussion)"""
    import time
    
    n = 8  # Standard chess board
    solutions = [
        ("Basic with validation", SolutionWithValidation()),
        ("Optimized with sets", Solution()),
        ("Position array", OptimizedSolution()),
        ("Bit manipulation", BitManipulationSolution())
    ]
    
    print(f"Performance comparison for N-Queens with n={n}:")
    print("-" * 50)
    
    for name, sol in solutions:
        start = time.time()
        result = sol.solveNQueens(n)
        end = time.time()
        print(f"{name:25}: {len(result)} solutions in {end-start:.4f}s")


"""
Interview Strategy and Key Points:

1. **Start with the conceptual explanation**:
   - "We need to place N queens on an N×N board such that none attack each other"
   - "Queens attack horizontally, vertically, and diagonally"
   - "This is a classic backtracking problem"

2. **Explain the approach step by step**:
   - Place queens row by row (eliminates row conflicts)
   - For each row, try each column
   - Check if the position is safe (no column/diagonal conflicts)
   - Recursively solve for next row
   - Backtrack if no solution found

3. **Discuss optimization techniques**:
   - Use sets to track occupied columns and diagonals
   - Diagonal formulas: row-col for main diagonal, row+col for anti-diagonal
   - Bit manipulation for ultimate optimization

4. **Complexity Analysis**:
   - Time: O(N!) - we have N choices for first row, N-2 for second, etc.
   - Space: O(N) for recursion stack and tracking sets

5. **Common follow-ups**:
   - "How would you count solutions only?" → N-Queens II
   - "Can you optimize further?" → Bit manipulation approach
   - "What about larger boards?" → Discuss memory and time trade-offs

6. **Edge cases to mention**:
   - n=1: trivial case, one solution
   - n=2,3: no solutions exist
   - n=4: two solutions (good for testing)

7. **Variants you should know**:
   - N-Queens II (count only)
   - Different board representations
   - Symmetric solution pruning
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60 + "\n")
    compare_performance()
