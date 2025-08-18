"""
LeetCode 1444: Number of Ways of Cutting a Pizza

Problem: Given a rectangular pizza represented as a rows x cols matrix containing 
'A' (apple) and '.' (empty), and k people. Each person must get at least one apple.
You can only cut horizontally or vertically. Return number of ways to cut the pizza.

Key Insights:
1. Each cut must leave at least one apple in each resulting piece
2. Use prefix sums to quickly count apples in any rectangle
3. DP state: (top, left, cuts_left) = ways to distribute pizza[top:][left:] with cuts_left
4. Try all possible horizontal and vertical cuts for each state

State: dp[r][c][k] = number of ways to cut pizza[r:][c:] into k pieces
Transition: Try all valid horizontal/vertical cuts that leave apples in both pieces

Time Complexity: O(rows * cols * k * (rows + cols))
Space Complexity: O(rows * cols * k)
"""

class Solution:
    def ways(self, pizza: list[str], k: int) -> int:
        """
        Main solution using 3D DP with prefix sums optimization.
        
        Uses bottom-right to top-left prefix sums for efficient apple counting.
        """
        if not pizza or not pizza[0]:
            return 0
        
        rows, cols = len(pizza), len(pizza[0])
        MOD = 10**9 + 7
        
        # Build prefix sum array for counting apples
        # prefix[i][j] = number of apples in rectangle from (i,j) to (rows-1,cols-1)
        prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                prefix[r][c] = (
                    prefix[r + 1][c] + 
                    prefix[r][c + 1] - 
                    prefix[r + 1][c + 1] + 
                    (1 if pizza[r][c] == 'A' else 0)
                )
        
        # Memoization cache
        memo = {}
        
        def dp(top: int, left: int, cuts_left: int) -> int:
            """
            Returns number of ways to cut pizza[top:][left:] into cuts_left pieces
            
            Args:
                top: top row of current pizza piece
                left: left column of current pizza piece  
                cuts_left: number of pieces we need to create
            """
            # Base case: no more cuts needed
            if cuts_left == 1:
                # Check if remaining piece has at least one apple
                return 1 if prefix[top][left] > 0 else 0
            
            # Base case: no apples left or impossible cuts
            if prefix[top][left] == 0 or cuts_left <= 0:
                return 0
            
            # Memoization check
            if (top, left, cuts_left) in memo:
                return memo[(top, left, cuts_left)]
            
            result = 0
            
            # Try all horizontal cuts
            # Cut after row r (give away top portion, keep bottom)
            for r in range(top, rows - 1):
                # Top piece: from (top, left) to (r, cols-1)
                top_apples = prefix[top][left] - prefix[r + 1][left]
                
                if top_apples > 0:  # Top piece has apples
                    # Recursively solve for bottom piece
                    result = (result + dp(r + 1, left, cuts_left - 1)) % MOD
            
            # Try all vertical cuts  
            # Cut after column c (give away left portion, keep right)
            for c in range(left, cols - 1):
                # Left piece: from (top, left) to (rows-1, c)
                left_apples = prefix[top][left] - prefix[top][c + 1]
                
                if left_apples > 0:  # Left piece has apples
                    # Recursively solve for right piece
                    result = (result + dp(top, c + 1, cuts_left - 1)) % MOD
            
            memo[(top, left, cuts_left)] = result
            return result
        
        return dp(0, 0, k)


class SolutionBottomUp:
    def ways(self, pizza: list[str], k: int) -> int:
        """
        Bottom-up DP solution for better understanding of state transitions.
        """
        if not pizza or not pizza[0]:
            return 0
        
        rows, cols = len(pizza), len(pizza[0])
        MOD = 10**9 + 7
        
        # Build prefix sum array
        prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                prefix[r][c] = (
                    prefix[r + 1][c] + 
                    prefix[r][c + 1] - 
                    prefix[r + 1][c + 1] + 
                    (1 if pizza[r][c] == 'A' else 0)
                )
        
        # dp[r][c][p] = ways to cut pizza[r:][c:] into p pieces
        dp = [[[0] * (k + 1) for _ in range(cols)] for _ in range(rows)]
        
        # Base case: 1 piece (no cuts)
        for r in range(rows):
            for c in range(cols):
                dp[r][c][1] = 1 if prefix[r][c] > 0 else 0
        
        # Fill DP table
        for pieces in range(2, k + 1):
            for r in range(rows):
                for c in range(cols):
                    # Try horizontal cuts
                    for cut_r in range(r, rows - 1):
                        top_apples = prefix[r][c] - prefix[cut_r + 1][c]
                        if top_apples > 0:
                            dp[r][c][pieces] = (dp[r][c][pieces] + 
                                              dp[cut_r + 1][c][pieces - 1]) % MOD
                    
                    # Try vertical cuts
                    for cut_c in range(c, cols - 1):
                        left_apples = prefix[r][c] - prefix[r][cut_c + 1]
                        if left_apples > 0:
                            dp[r][c][pieces] = (dp[r][c][pieces] + 
                                              dp[r][cut_c + 1][pieces - 1]) % MOD
        
        return dp[0][0][k]


class SolutionOptimized:
    def ways(self, pizza: list[str], k: int) -> int:
        """
        Optimized solution with better constant factors and cleaner code.
        """
        rows, cols = len(pizza), len(pizza[0])
        MOD = 10**9 + 7
        
        # Prefix sum for apple count
        apples = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                apples[r][c] = (apples[r + 1][c] + apples[r][c + 1] - 
                               apples[r + 1][c + 1] + (pizza[r][c] == 'A'))
        
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dfs(r: int, c: int, k: int) -> int:
            """Count ways to cut pizza[r:][c:] into k pieces"""
            # Base cases
            if k == 1:
                return 1 if apples[r][c] > 0 else 0
            if apples[r][c] == 0:
                return 0
            
            ways = 0
            
            # Horizontal cuts
            for nr in range(r + 1, rows):
                if apples[r][c] - apples[nr][c] > 0:  # Top piece has apples
                    ways = (ways + dfs(nr, c, k - 1)) % MOD
            
            # Vertical cuts  
            for nc in range(c + 1, cols):
                if apples[r][c] - apples[r][nc] > 0:  # Left piece has apples
                    ways = (ways + dfs(r, nc, k - 1)) % MOD
            
            return ways
        
        return dfs(0, 0, k)


def test_solutions():
    """Comprehensive test cases"""
    
    # Test case 1
    pizza1 = ["A..", "AAA", "..."]
    k1 = 3
    # Expected: 3
    # Can cut: vertical after col 0, then horizontal after row 0
    #         or horizontal after row 0, then vertical cuts
    
    # Test case 2  
    pizza2 = ["A..", "AA.", "..."]
    k2 = 3
    # Expected: 1
    
    # Test case 3
    pizza3 = ["A..", "A..", "..."]  
    k3 = 1
    # Expected: 1
    
    # Test case 4 - Edge case
    pizza4 = ["...", "...", "..."]
    k4 = 1
    # Expected: 0 (no apples)
    
    solutions = [
        ("Top-down DP", Solution()),
        ("Bottom-up DP", SolutionBottomUp()),
        ("Optimized", SolutionOptimized())
    ]
    
    test_cases = [
        ("Test 1", pizza1, k1, 3),
        ("Test 2", pizza2, k2, 1),
        ("Test 3", pizza3, k3, 1),
        ("Test 4", pizza4, k4, 0)
    ]
    
    for name, pizza, k, expected in test_cases:
        print(f"\n{name} - Pizza: {pizza}, k={k} (Expected: {expected}):")
        for sol_name, solution in solutions:
            try:
                result = solution.ways(pizza, k)
                status = "✓" if result == expected else "✗"
                print(f"  {sol_name}: {result} {status}")
            except Exception as e:
                print(f"  {sol_name}: ERROR - {e}")


def visualize_approach():
    """Visual explanation of the approach"""
    print("\nPROBLEM VISUALIZATION:")
    pizza = ["A..", "AAA", "..."]
    print("Pizza:")
    for i, row in enumerate(pizza):
        print(f"Row {i}: {row}")
    
    print(f"\nPrefix sum array (apples[r][c] = apples in rectangle from (r,c) to bottom-right):")
    print("  Col: 0 1 2 3")
    
    # Manually compute for visualization
    apples = [[0] * 4 for _ in range(4)]
    rows, cols = 3, 3
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            apples[r][c] = (apples[r + 1][c] + apples[r][c + 1] - 
                           apples[r + 1][c + 1] + (pizza[r][c] == 'A'))
    
    for r in range(4):
        print(f"Row {r}: {apples[r]}")
    
    print("\nExample cuts for k=3:")
    print("1. Vertical cut after col 0: ['A'] + ['..', 'AA', '..']")
    print("   Then horizontal cut on right piece after row 0")
    print("2. Horizontal cut after row 0: ['A..'] + ['AAA', '...']")
    print("   Then vertical cuts on bottom piece")


def explain_key_insights():
    """Key algorithmic insights"""
    print("\nKEY INSIGHTS:")
    
    print("\n1. Prefix Sum Optimization:")
    print("   - prefix[r][c] = total apples from (r,c) to bottom-right")
    print("   - Apple count in rectangle = prefix math in O(1)")
    print("   - Essential for efficiency in this problem")
    
    print("\n2. State Design:")  
    print("   - dp(r, c, k) = ways to cut pizza[r:][c:] into k pieces")
    print("   - Natural recursive structure matches problem")
    print("   - Each cut reduces k by 1")
    
    print("\n3. Cut Validation:")
    print("   - Every piece must have ≥1 apple")
    print("   - Use prefix sums to check in O(1)")
    print("   - Invalid cuts return 0 ways")
    
    print("\n4. Direction Independence:")
    print("   - Can cut horizontally or vertically")
    print("   - Try all possible positions for each direction")
    print("   - Sum up all valid possibilities")


def complexity_analysis():
    """Detailed complexity breakdown"""
    print("\nCOMPLEXITY ANALYSIS:")
    
    print("\nTime Complexity: O(rows * cols * k * (rows + cols))")
    print("- States: O(rows * cols * k)")
    print("- Per state: try O(rows + cols) cuts")
    print("- Each cut check: O(1) with prefix sums")
    
    print("\nSpace Complexity: O(rows * cols * k)")  
    print("- DP memoization table")
    print("- Prefix sum array: O(rows * cols)")
    print("- Total dominated by DP table")
    
    print("\nWithout prefix sums:")
    print("- Each apple count would be O(rows * cols)")
    print("- Total time: O(rows^2 * cols^2 * k * (rows + cols))")
    print("- Prefix sums provide crucial optimization!")


# Interview discussion points
"""
INTERVIEW DISCUSSION POINTS:

1. Problem Understanding:
   - Must cut pizza into exactly k pieces
   - Each piece must contain ≥1 apple
   - Can only cut horizontally or vertically
   - Count total number of valid cutting sequences

2. Key Insights:
   - Use prefix sums for O(1) apple counting in rectangles
   - DP state: (top_row, left_col, pieces_remaining)
   - Try all possible cuts from current state

3. Critical Optimizations:
   - Prefix sums: Without this, TLE guaranteed
   - Memoization: Avoid recomputing same subproblems
   - Early termination: If no apples, return 0

4. Edge Cases:
   - k = 1 (no cuts needed)
   - No apples in pizza
   - k > number of apples
   - Single row/column pizza

5. State Transition Logic:
   - For each cut position, validate both pieces have apples
   - Recurse on the remaining piece (keep one, give away other)
   - Sum all valid transitions

6. Alternative Approaches:
   - Could model as interval DP
   - Could use BFS with state compression
   - Current DP approach is most natural

7. Follow-up Questions:
   - What if we want to maximize apples per person?
   - What if pizza is circular?
   - What about 3D pizza (cube cutting)?

8. Common Mistakes:
   - Forgetting MOD operation
   - Not validating apple counts
   - Inefficient apple counting without prefix sums
   - Wrong base cases in recursion

Recommended Interview Approach:
1. Start with brute force explanation
2. Identify overlapping subproblems → DP
3. Discuss prefix sum optimization
4. Code the memoized solution
5. Walk through test case
6. Discuss complexity and optimizations
"""

if __name__ == "__main__":
    test_solutions()
    visualize_approach()
    explain_key_insights()
    complexity_analysis()
