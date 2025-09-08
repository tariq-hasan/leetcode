"""
LeetCode 52: N-Queens II
Hard Difficulty

Problem:
The n-queens puzzle is the problem of placing n chess queens on an n×n chessboard 
such that no two queens attack each other. Given an integer n, return the number 
of distinct solutions to the n-queens puzzle.

Example:
Input: n = 4
Output: 2
Explanation: There are two distinct solutions to the 4-queens puzzle.

Input: n = 1
Output: 1

Time Complexity: O(N!) - exponential but optimized
Space Complexity: O(N) for recursion stack only
"""

class Solution:
    def totalNQueens(self, n: int) -> int:
        """
        Optimized backtracking approach - only count solutions, don't store them
        
        Key optimizations:
        1. No board representation needed
        2. Use sets for O(1) conflict detection
        3. Only increment counter, no string building
        """
        def backtrack(row, cols, diag1, diag2):
            # Base case: successfully placed all queens
            if row == n:
                return 1
            
            count = 0
            # Try placing queen in each column of current row
            for col in range(n):
                # Check if position is under attack
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                # Place queen and recurse
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                count += backtrack(row + 1, cols, diag1, diag2)
                
                # Backtrack
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
            
            return count
        
        return backtrack(0, set(), set(), set())


class BitManipulationSolution:
    def totalNQueens(self, n: int) -> int:
        """
        Ultra-optimized bit manipulation solution
        
        This is the fastest possible approach for N-Queens counting.
        Each bit position represents a column/diagonal state.
        
        Time: O(N!) but with minimal constants
        Space: O(N) recursion only
        """
        def backtrack(row, cols, diag1, diag2):
            if row == n:
                return 1
            
            count = 0
            # Get available positions: where all three bitmasks have 0
            # Mask with (1 << n) - 1 to keep only valid positions
            available = ~(cols | diag1 | diag2) & ((1 << n) - 1)
            
            # Process each available position
            while available:
                # Get the rightmost available position
                position = available & -available
                # Remove this position from available
                available ^= position
                
                # Recurse with updated bitmasks
                count += backtrack(row + 1,
                                 cols | position,        # Mark column as occupied
                                 (diag1 | position) << 1,  # Shift main diagonal
                                 (diag2 | position) >> 1)  # Shift anti-diagonal
            
            return count
        
        return backtrack(0, 0, 0, 0)


class MemoizedSolution:
    def totalNQueens(self, n: int) -> int:
        """
        Memoized version - useful for multiple queries
        
        Note: Memoization doesn't help much for single queries since
        each state is typically visited only once, but demonstrates
        the technique for interview discussion.
        """
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def backtrack(row, cols_mask, diag1_mask, diag2_mask):
            if row == n:
                return 1
            
            count = 0
            available = ~(cols_mask | diag1_mask | diag2_mask) & ((1 << n) - 1)
            
            while available:
                pos = available & -available
                available ^= pos
                
                count += backtrack(row + 1,
                                 cols_mask | pos,
                                 (diag1_mask | pos) << 1,
                                 (diag2_mask | pos) >> 1)
            
            return count
        
        return backtrack(0, 0, 0, 0)


class SymmetryOptimizedSolution:
    def totalNQueens(self, n: int) -> int:
        """
        Advanced optimization using symmetry
        
        For boards with odd n, we can reduce computation by considering
        symmetry and only computing half the solutions.
        """
        def backtrack_half(row, cols, diag1, diag2, max_col):
            if row == n:
                return 1
            
            count = 0
            end_col = min(max_col + 1, n) if row == 0 else n
            
            for col in range(end_col):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                count += backtrack_half(row + 1, cols, diag1, diag2, n - 1)
                
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
            
            return count
        
        if n == 1:
            return 1
        
        # For even n or when symmetry doesn't apply simply
        if n % 2 == 0:
            return 2 * backtrack_half(0, set(), set(), set(), n // 2 - 1)
        else:
            # For odd n, handle middle column separately
            middle = n // 2
            count = 2 * backtrack_half(0, set(), set(), set(), middle - 1)
            
            # Add solutions with queen in middle column of first row
            cols, diag1, diag2 = {middle}, {-middle}, {middle}
            count += backtrack_half(1, cols, diag1, diag2, n - 1)
            
            return count


class ComparisonClass:
    """Class to demonstrate different approaches for interview discussion"""
    
    def naive_with_board_generation(self, n: int) -> int:
        """
        Naive approach: generate all solutions then count
        This is what you'd get from modifying N-Queens I
        """
        def backtrack(row, cols, diag1, diag2, path):
            if row == n:
                return [path[:]]  # Return solution
            
            solutions = []
            for col in range(n):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                path.append(col)
                
                solutions.extend(backtrack(row + 1, cols, diag1, diag2, path))
                
                path.pop()
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
            
            return solutions
        
        solutions = backtrack(0, set(), set(), set(), [])
        return len(solutions)
    
    def optimized_counting_only(self, n: int) -> int:
        """The optimal approach - count without storing"""
        def backtrack(row, cols, diag1, diag2):
            if row == n:
                return 1
            
            count = 0
            for col in range(n):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue
                
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                count += backtrack(row + 1, cols, diag1, diag2)
                
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
            
            return count
        
        return backtrack(0, set(), set(), set())


def test_solutions():
    """Test all solutions with known results"""
    # Known results for N-Queens
    expected = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724}
    
    solutions = [
        ("Basic backtracking", Solution()),
        ("Bit manipulation", BitManipulationSolution()),
        ("Memoized", MemoizedSolution()),
        ("Symmetry optimized", SymmetryOptimizedSolution())
    ]
    
    print("N-Queens II Test Results:")
    print("-" * 40)
    
    for n in range(1, 11):
        print(f"n={n:2d}: expected={expected[n]:3d}", end=" | ")
        
        for name, sol in solutions:
            try:
                result = sol.totalNQueens(n)
                status = "✓" if result == expected[n] else "✗"
                print(f"{name[:10]}:{result:3d}{status}", end=" ")
            except Exception as e:
                print(f"{name[:10]}:ERR", end=" ")
        print()


def benchmark_performance():
    """Benchmark different solutions for interview discussion"""
    import time
    
    test_n = 10  # Reasonable size for comparison
    iterations = 5
    
    solutions = [
        ("Set-based backtracking", Solution()),
        ("Bit manipulation", BitManipulationSolution()),
        ("Memoized version", MemoizedSolution())
    ]
    
    print(f"\nPerformance Benchmark (n={test_n}, {iterations} iterations):")
    print("-" * 60)
    
    for name, sol in solutions:
        times = []
        for _ in range(iterations):
            start = time.time()
            result = sol.totalNQueens(test_n)
            end = time.time()
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        print(f"{name:25}: {result:4d} solutions in {avg_time:.6f}s avg")


"""
Interview Strategy and Key Points:

1. **Immediate Recognition**:
   "This is N-Queens I but we only need the count, not the actual solutions.
   This means we can optimize by removing all board representation overhead."

2. **Key Optimization Insight**:
   "Since we're only counting, we don't need to store any board state or 
   construct solution strings. We just increment a counter and recurse."

3. **Approach Progression** (show evolution of thinking):
   - Naive: Generate all solutions from N-Queens I, then count
   - Better: Count during backtracking without storing solutions
   - Optimal: Bit manipulation for maximum speed

4. **Complexity Analysis**:
   - Time: O(N!) - same as N-Queens I, but lower constants
   - Space: O(N) - only recursion stack, no solution storage

5. **Bit Manipulation Explanation** (if asked):
   "We use three bitmasks to track conflicts:
   - cols: occupied columns
   - diag1: main diagonals (shift left each row)
   - diag2: anti-diagonals (shift right each row)
   
   Available positions = ~(cols | diag1 | diag2) & valid_mask"

6. **Common Follow-ups**:
   - "Can you optimize further?" → Symmetry optimization
   - "What about memoization?" → Explain why it doesn't help much
   - "Space optimization?" → Show bit manipulation approach
   - "Multiple queries?" → Discuss precomputation strategies

7. **Edge Cases**:
   - n=1: 1 solution
   - n=2,3: 0 solutions (impossible)
   - n=4: 2 solutions (classic test case)

8. **Key Interview Points**:
   - Recognize this as an optimization problem of N-Queens I
   - Show you understand when to avoid unnecessary work
   - Demonstrate progression from naive to optimal
   - Handle bit manipulation questions confidently
"""

if __name__ == "__main__":
    test_solutions()
    benchmark_performance()
    
    print("\nQuick verification for common test cases:")
    sol = BitManipulationSolution()  # Use fastest for demo
    for n in [1, 4, 8]:
        result = sol.totalNQueens(n)
        print(f"N-Queens II for n={n}: {result} solutions")
