from typing import List


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        
        Time Complexity: O(9^(n*n)) where n=9, but practically much better due to pruning
        Space Complexity: O(n*n) for recursion stack in worst case
        """
        def is_valid(board, row, col, num):
            """Check if placing num at (row, col) is valid"""
            # Check row
            for j in range(9):
                if board[row][j] == num:
                    return False
            
            # Check column
            for i in range(9):
                if board[i][col] == num:
                    return False
            
            # Check 3x3 box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] == num:
                        return False
            
            return True
        
        def backtrack():
            """Recursive backtracking function"""
            for i in range(9):
                for j in range(9):
                    if board[i][j] == '.':
                        # Try digits 1-9
                        for num in '123456789':
                            if is_valid(board, i, j, num):
                                board[i][j] = num
                                
                                # Recursively solve rest of the board
                                if backtrack():
                                    return True
                                
                                # Backtrack if solution not found
                                board[i][j] = '.'
                        
                        # If no digit works, return False
                        return False
            
            # All cells filled successfully
            return True
        
        backtrack()


# Alternative optimized solution with precomputed constraints
class OptimizedSolution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Optimized version using sets to track used numbers
        
        Time Complexity: O(9^k) where k is number of empty cells
        Space Complexity: O(1) additional space for constraint sets
        """
        # Precompute constraints
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empty_cells = []
        
        # Initialize constraints and find empty cells
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    empty_cells.append((i, j))
                else:
                    num = board[i][j]
                    rows[i].add(num)
                    cols[j].add(num)
                    boxes[3 * (i // 3) + j // 3].add(num)
        
        def backtrack(idx):
            if idx == len(empty_cells):
                return True
            
            row, col = empty_cells[idx]
            box_idx = 3 * (row // 3) + col // 3
            
            for num in '123456789':
                if (num not in rows[row] and 
                    num not in cols[col] and 
                    num not in boxes[box_idx]):
                    
                    # Place number
                    board[row][col] = num
                    rows[row].add(num)
                    cols[col].add(num)
                    boxes[box_idx].add(num)
                    
                    # Recurse
                    if backtrack(idx + 1):
                        return True
                    
                    # Backtrack
                    board[row][col] = '.'
                    rows[row].remove(num)
                    cols[col].remove(num)
                    boxes[box_idx].remove(num)
            
            return False
        
        backtrack(0)


# Most optimized solution with constraint propagation
class MostOptimizedSolution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Most optimized version with MRV (Most Restrictive Variable) heuristic
        """
        def get_candidates(board, row, col):
            """Get possible candidates for a cell"""
            if board[row][col] != '.':
                return set()
            
            used = set()
            
            # Check row
            for j in range(9):
                if board[row][j] != '.':
                    used.add(board[row][j])
            
            # Check column
            for i in range(9):
                if board[i][col] != '.':
                    used.add(board[i][col])
            
            # Check box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] != '.':
                        used.add(board[i][j])
            
            return set('123456789') - used
        
        def find_best_cell(board):
            """Find empty cell with minimum candidates (MRV heuristic)"""
            min_candidates = 10
            best_cell = None
            best_candidates = None
            
            for i in range(9):
                for j in range(9):
                    if board[i][j] == '.':
                        candidates = get_candidates(board, i, j)
                        if len(candidates) < min_candidates:
                            min_candidates = len(candidates)
                            best_cell = (i, j)
                            best_candidates = candidates
                            
                            # Early termination if no candidates
                            if min_candidates == 0:
                                return best_cell, best_candidates
            
            return best_cell, best_candidates
        
        def solve():
            cell, candidates = find_best_cell(board)
            
            # No empty cells left - solved!
            if cell is None:
                return True
            
            # No candidates available - invalid state
            if len(candidates) == 0:
                return False
            
            row, col = cell
            
            for num in candidates:
                board[row][col] = num
                
                if solve():
                    return True
                
                board[row][col] = '.'
            
            return False
        
        solve()


# Test cases and usage example
def test_sudoku_solver():
    # Test case from LeetCode
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    
    def print_board(board):
        for i, row in enumerate(board):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            for j, cell in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(cell, end=" ")
            print()
    
    print("Original board:")
    print_board(board)
    
    # Solve using the basic solution
    solution = Solution()
    solution.solveSudoku(board)
    
    print("\nSolved board:")
    print_board(board)

# Expected output for the test case:
# [["5","3","4","6","7","8","9","1","2"],
#  ["6","7","2","1","9","5","3","4","8"],
#  ["1","9","8","3","4","2","5","6","7"],
#  ["8","5","9","7","6","1","4","2","3"],
#  ["4","2","6","8","5","3","7","9","1"],
#  ["7","1","3","9","2","4","8","5","6"],
#  ["9","6","1","5","3","7","2","8","4"],
#  ["2","8","7","4","1","9","6","3","5"],
#  ["3","4","5","2","8","6","1","7","9"]]


"""
KEY INTERVIEW POINTS:

1. ALGORITHM EXPLANATION:
   - Backtracking: Try each possibility, backtrack if invalid
   - For each empty cell, try digits 1-9
   - Check if placement is valid (row, column, 3x3 box)
   - Recursively solve remaining cells
   - Backtrack if no solution found

2. TIME COMPLEXITY:
   - Worst case: O(9^(n²)) where n=9
   - Practically much better due to constraint propagation
   - With optimizations: closer to O(9^k) where k = empty cells

3. SPACE COMPLEXITY:
   - O(n²) for recursion stack in worst case
   - O(1) additional space for basic solution

4. OPTIMIZATIONS TO DISCUSS:
   - Precompute constraints using sets (faster lookups)
   - MRV heuristic: choose cell with fewest candidates first
   - Constraint propagation: eliminate impossible values early
   - Early termination when no candidates available

5. EDGE CASES:
   - Invalid board (no solution exists)
   - Already solved board
   - Multiple solutions (problem guarantees unique solution)

6. FOLLOW-UP QUESTIONS:
   - How to check if sudoku is solvable?
   - How to generate valid sudoku puzzles?
   - Parallel solving approaches?
   - Memory-optimized versions?
"""
