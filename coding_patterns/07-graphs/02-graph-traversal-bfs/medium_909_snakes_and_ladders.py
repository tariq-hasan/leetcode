"""
LeetCode 909: Snakes and Ladders
Problem: Find minimum number of moves to reach the last square on a board.
Board is numbered 1 to n² in Boustrophedon style (alternating left-to-right and right-to-left).
Snakes and ladders are represented by board[r][c] != -1.

Time Complexity: O(n²) where board is n×n
Space Complexity: O(n²) for visited set and queue
"""

from collections import deque
from typing import List

class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        """
        Solution 1: Standard BFS with coordinate conversion
        Key insight: Convert between square numbers and (row, col) coordinates
        """
        n = len(board)
        target = n * n
        
        def get_coordinates(square):
            """Convert square number (1-indexed) to (row, col) coordinates"""
            # Adjust to 0-indexed
            square -= 1
            row = n - 1 - square // n  # Bottom to top
            col = square % n
            
            # Handle Boustrophedon (snake-like) numbering
            # Odd rows (from bottom) go right-to-left
            if (n - 1 - row) % 2 == 1:
                col = n - 1 - col
            
            return row, col
        
        queue = deque([1])  # Start at square 1
        visited = {1}
        moves = 0
        
        while queue:
            # Process all squares at current move level
            for _ in range(len(queue)):
                square = queue.popleft()
                
                if square == target:
                    return moves
                
                # Try all possible dice rolls (1-6)
                for dice in range(1, 7):
                    next_square = square + dice
                    
                    if next_square > target:
                        break  # Can't go beyond the board
                    
                    row, col = get_coordinates(next_square)
                    
                    # Check for snake or ladder
                    if board[row][col] != -1:
                        next_square = board[row][col]
                    
                    if next_square not in visited:
                        visited.add(next_square)
                        queue.append(next_square)
            
            moves += 1
        
        return -1

    def snakesAndLadders_optimized(self, board: List[List[int]]) -> int:
        """
        Solution 2: BFS with moves tracking in queue
        Alternative approach storing moves with each state
        """
        n = len(board)
        target = n * n
        
        def square_to_position(square):
            """Convert 1-indexed square to (row, col)"""
            square -= 1  # Convert to 0-indexed
            row = n - 1 - square // n
            col = square % n if (square // n) % 2 == 0 else n - 1 - square % n
            return row, col
        
        queue = deque([(1, 0)])  # (square, moves)
        visited = {1}
        
        while queue:
            square, moves = queue.popleft()
            
            if square == target:
                return moves
            
            # Try dice rolls 1-6
            for dice in range(1, 7):
                next_square = square + dice
                
                if next_square > target:
                    continue
                
                row, col = square_to_position(next_square)
                
                # Handle snake/ladder
                if board[row][col] != -1:
                    next_square = board[row][col]
                
                if next_square not in visited:
                    visited.add(next_square)
                    queue.append((next_square, moves + 1))
        
        return -1

    def snakesAndLadders_with_early_termination(self, board: List[List[int]]) -> int:
        """
        Solution 3: BFS with early termination optimization
        Check for immediate win condition during dice roll exploration
        """
        n = len(board)
        target = n * n
        
        def get_position(num):
            """Convert square number to board position"""
            num -= 1
            row = n - 1 - num // n
            col = num % n
            if (n - 1 - row) % 2 == 1:
                col = n - 1 - col
            return row, col
        
        queue = deque([1])
        visited = {1}
        moves = 0
        
        while queue:
            for _ in range(len(queue)):
                curr = queue.popleft()
                
                # Early termination check
                if curr == target:
                    return moves
                
                for dice in range(1, 7):
                    next_pos = curr + dice
                    
                    if next_pos > target:
                        break
                    
                    # Immediate win check
                    if next_pos == target:
                        return moves + 1
                    
                    row, col = get_position(next_pos)
                    
                    if board[row][col] != -1:
                        next_pos = board[row][col]
                        # Check if snake/ladder leads to win
                        if next_pos == target:
                            return moves + 1
                    
                    if next_pos not in visited:
                        visited.add(next_pos)
                        queue.append(next_pos)
            
            moves += 1
        
        return -1

# Utility function to demonstrate coordinate conversion
def demonstrate_coordinate_conversion():
    """Helper function to understand the coordinate system"""
    n = 6  # 6x6 board
    print("Square -> (row, col) mapping for 6x6 board:")
    
    for square in range(1, n*n + 1):
        square_0_indexed = square - 1
        row = n - 1 - square_0_indexed // n
        col = square_0_indexed % n
        
        # Handle Boustrophedon
        if (n - 1 - row) % 2 == 1:
            col = n - 1 - col
        
        print(f"Square {square:2d} -> ({row}, {col})")
        if square % 6 == 0:
            print()

# Test cases for interview demonstration
def test_solutions():
    sol = Solution()
    
    # Test case 1: Example from problem
    board1 = [
        [-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1],
        [-1,35,-1,-1,13,-1],
        [-1,-1,-1,-1,-1,-1],
        [-1,15,-1,-1,-1,-1]
    ]
    print(f"Test 1: {sol.snakesAndLadders(board1)}")  # Expected: 4
    
    # Test case 2: No snakes or ladders
    board2 = [[-1,-1],[-1,3]]
    print(f"Test 2: {sol.snakesAndLadders(board2)}")  # Expected: 1
    
    # Test case 3: Single cell
    board3 = [[-1]]
    print(f"Test 3: {sol.snakesAndLadders(board3)}")  # Expected: 0
    
    # Test case 4: Immediate ladder to end
    board4 = [[-1,4,-1],[6,2,-1],[-1,3,-1]]
    print(f"Test 4: {sol.snakesAndLadders(board4)}")

if __name__ == "__main__":
    print("Coordinate conversion demo:")
    demonstrate_coordinate_conversion()
    print("\nTest results:")
    test_solutions()

"""
Interview Discussion Points:

1. **Key Challenge - Coordinate Conversion**:
   - Board is numbered in Boustrophedon (snake-like) pattern
   - Square 1 is bottom-left, square n² is top-right
   - Even rows: left-to-right, Odd rows: right-to-left
   - Formula: row = n-1-square//n, col handling depends on row parity

2. **Algorithm Choice**:
   - BFS guarantees minimum moves (shortest path in unweighted graph)
   - Each square is a node, dice rolls create edges
   - Snakes/ladders are teleportation edges

3. **Implementation Details**:
   - Use visited set to avoid cycles
   - Process level-by-level to track moves
   - Handle dice rolls 1-6 from each position
   - Early termination when reaching target

4. **Edge Cases**:
   - Single cell board (n=1) → return 0
   - Landing exactly on target square
   - Snake/ladder leading directly to target
   - Unreachable target (should not happen with valid input)

5. **Time/Space Complexity**:
   - Time: O(n²) - each square visited at most once
   - Space: O(n²) - visited set and queue storage

6. **Coordinate Conversion Deep Dive**:
   - This is the trickiest part of the problem
   - Practice converting between square numbers and (row,col)
   - Understand Boustrophedon numbering pattern

7. **Common Mistakes**:
   - Incorrect coordinate conversion (most common error)
   - Not handling snakes/ladders properly
   - Off-by-one errors in square numbering
   - Forgetting to check dice roll bounds

8. **Follow-up Optimizations**:
   - Bidirectional BFS (complex due to reverse movement rules)
   - Early termination checks
   - Efficient data structures

9. **Testing Strategy**:
   - Test coordinate conversion separately
   - Verify with small boards first
   - Check edge cases like n=1, immediate win conditions

Key Coordinate Conversion Visual:
For 6x6 board (squares numbered 1-36):

Row 0: 31 32 33 34 35 36
Row 1: 30 29 28 27 26 25  ← Right-to-left
Row 2: 19 20 21 22 23 24
Row 3: 18 17 16 15 14 13  ← Right-to-left  
Row 4:  7  8  9 10 11 12
Row 5:  6  5  4  3  2  1  ← Right-to-left (start here)

Conversion formula:
- square -= 1 (convert to 0-indexed)
- row = n - 1 - square // n (bottom-up)
- col = square % n
- if (n - 1 - row) % 2 == 1: col = n - 1 - col (reverse odd rows)
"""
