from typing import List
from collections import deque

class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """
        Problem: Given m x n binary matrix, find distance of nearest 0 for each cell.
        
        APPROACH 1: MULTI-SOURCE BFS (OPTIMAL - Most Expected Solution)
        Time: O(m * n) - visit each cell once
        Space: O(m * n) - queue can hold up to m*n elements
        
        Key insight: Start BFS from ALL 0s simultaneously (multi-source BFS).
        This finds shortest path from any 0 to each 1 in single pass.
        """
        if not mat or not mat[0]:
            return mat
        
        m, n = len(mat), len(mat[0])
        # Initialize result matrix
        result = [[float('inf')] * n for _ in range(m)]
        queue = deque()
        
        # Step 1: Find all 0s and add to queue, set their distance to 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    result[i][j] = 0
                    queue.append((i, j))
        
        # Step 2: BFS from all 0s simultaneously
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            row, col = queue.popleft()
            
            # Check all 4 neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds
                if 0 <= new_row < m and 0 <= new_col < n:
                    # If we found a shorter path to this cell
                    if result[new_row][new_col] > result[row][col] + 1:
                        result[new_row][new_col] = result[row][col] + 1
                        queue.append((new_row, new_col))
        
        return result
    
    def updateMatrix_brute_force(self, mat: List[List[int]]) -> List[List[int]]:
        """
        APPROACH 2: BRUTE FORCE (Start with this to show understanding)
        Time: O(m * n * m * n) = O(m^2 * n^2) - BFS from each 1 to find nearest 0
        Space: O(m * n) for BFS queue
        
        For each 1, run BFS to find nearest 0. Not optimal but correct.
        """
        if not mat or not mat[0]:
            return mat
        
        m, n = len(mat), len(mat[0])
        result = [[0] * n for _ in range(m)]
        
        def bfs_from_cell(start_row, start_col):
            """BFS from given cell to find nearest 0"""
            if mat[start_row][start_col] == 0:
                return 0
            
            queue = deque([(start_row, start_col, 0)])
            visited = set()
            visited.add((start_row, start_col))
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            while queue:
                row, col, dist = queue.popleft()
                
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    
                    if (0 <= new_row < m and 0 <= new_col < n and 
                        (new_row, new_col) not in visited):
                        
                        if mat[new_row][new_col] == 0:
                            return dist + 1
                        
                        visited.add((new_row, new_col))
                        queue.append((new_row, new_col, dist + 1))
            
            return float('inf')  # Should never reach here
        
        # Run BFS from each cell
        for i in range(m):
            for j in range(n):
                result[i][j] = bfs_from_cell(i, j)
        
        return result
    
    def updateMatrix_dp(self, mat: List[List[int]]) -> List[List[int]]:
        """
        APPROACH 3: DYNAMIC PROGRAMMING (Alternative Approach)
        Time: O(m * n) - two passes through matrix
        Space: O(1) if modifying in place, O(m * n) for result
        
        Two-pass approach: top-left to bottom-right, then bottom-right to top-left.
        Good to mention as alternative, but BFS is more intuitive for this problem.
        """
        if not mat or not mat[0]:
            return mat
        
        m, n = len(mat), len(mat[0])
        result = [[float('inf')] * n for _ in range(m)]
        
        # Initialize 0s
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    result[i][j] = 0
        
        # First pass: top-left to bottom-right
        for i in range(m):
            for j in range(n):
                if result[i][j] != 0:
                    if i > 0:
                        result[i][j] = min(result[i][j], result[i-1][j] + 1)
                    if j > 0:
                        result[i][j] = min(result[i][j], result[i][j-1] + 1)
        
        # Second pass: bottom-right to top-left
        for i in range(m-1, -1, -1):
            for j in range(n-1, -1, -1):
                if result[i][j] != 0:
                    if i < m-1:
                        result[i][j] = min(result[i][j], result[i+1][j] + 1)
                    if j < n-1:
                        result[i][j] = min(result[i][j], result[i][j+1] + 1)
        
        return result

# INTERVIEW DEMONSTRATION CLASS
class InterviewSolution:
    """
    Clean, interview-ready solution with clear explanation
    """
    
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """
        MAIN INTERVIEW SOLUTION: Multi-source BFS
        Find shortest distance from each cell to nearest 0
        """
        if not mat or not mat[0]:
            return []
        
        rows, cols = len(mat), len(mat[0])
        
        # Initialize distances and queue for BFS
        distances = [[float('inf')] * cols for _ in range(rows)]
        queue = deque()
        
        # Step 1: Find all 0s - these are our starting points
        for i in range(rows):
            for j in range(cols):
                if mat[i][j] == 0:
                    distances[i][j] = 0
                    queue.append((i, j))
        
        # Step 2: Multi-source BFS
        # Start from all 0s simultaneously and propagate distances
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            current_row, current_col = queue.popleft()
            current_distance = distances[current_row][current_col]
            
            # Explore all 4 neighbors
            for row_delta, col_delta in directions:
                neighbor_row = current_row + row_delta
                neighbor_col = current_col + col_delta
                
                # Check if neighbor is within bounds
                if (0 <= neighbor_row < rows and 0 <= neighbor_col < cols):
                    new_distance = current_distance + 1
                    
                    # If we found a shorter path to this neighbor
                    if new_distance < distances[neighbor_row][neighbor_col]:
                        distances[neighbor_row][neighbor_col] = new_distance
                        queue.append((neighbor_row, neighbor_col))
        
        return distances
    
    def updateMatrix_step_by_step(self, mat: List[List[int]]) -> List[List[int]]:
        """
        DETAILED VERSION: Same algorithm with more explicit steps for explanation
        """
        # Input validation
        if not mat or not mat[0]:
            return []
        
        rows, cols = len(mat), len(mat[0])
        
        # Step 1: Initialize result matrix with infinity (except 0s)
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                if mat[i][j] == 0:
                    row.append(0)  # Distance from 0 to itself is 0
                else:
                    row.append(float('inf'))  # Unknown distance initially
            result.append(row)
        
        # Step 2: Prepare BFS - add all 0s to queue
        bfs_queue = deque()
        for i in range(rows):
            for j in range(cols):
                if mat[i][j] == 0:
                    bfs_queue.append((i, j))
        
        # Step 3: BFS to find shortest distances
        neighbor_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while bfs_queue:
            curr_i, curr_j = bfs_queue.popleft()
            
            # Check all 4 neighbors
            for di, dj in neighbor_directions:
                next_i, next_j = curr_i + di, curr_j + dj
                
                # Ensure neighbor is within matrix bounds
                if 0 <= next_i < rows and 0 <= next_j < cols:
                    # Calculate potential new distance
                    new_dist = result[curr_i][curr_j] + 1
                    
                    # Update if we found shorter path
                    if new_dist < result[next_i][next_j]:
                        result[next_i][next_j] = new_dist
                        bfs_queue.append((next_i, next_j))
        
        return result

# COMPREHENSIVE TESTING
def test_solutions():
    """Test all solution approaches"""
    solutions = [
        Solution().updateMatrix,
        Solution().updateMatrix_brute_force,
        Solution().updateMatrix_dp,
        InterviewSolution().updateMatrix,
        InterviewSolution().updateMatrix_step_by_step
    ]
    
    test_cases = [
        # (input_matrix, expected_output)
        ([[0,0,0],[0,1,0],[0,0,0]], [[0,0,0],[0,1,0],[0,0,0]]),
        ([[0,0,0],[0,1,0],[1,1,1]], [[0,0,0],[0,1,0],[1,2,1]]),
        ([[0]], [[0]]),
        ([[1]], [[1]]),  # This should be inf, but problem guarantees at least one 0
        ([[1,1,1],[1,1,1],[1,1,0]], [[4,3,2],[3,2,1],[2,1,0]]),
        ([[0,1,0,1,1],[1,1,0,0,1],[0,0,0,1,0],[1,0,1,1,1],[1,0,0,0,1]], 
         [[0,1,0,1,2],[1,1,0,0,1],[0,0,0,1,0],[1,0,1,1,1],[1,0,0,0,1]]),
    ]
    
    # Note: Test case with [[1]] is invalid according to problem constraints
    # Problem guarantees at least one 0, so removing it
    test_cases = test_cases[:-3] + test_cases[-2:]  # Skip the [[1]] case
    
    for i, solution_func in enumerate(solutions):
        print(f"Testing Solution {i+1}...")
        for j, (input_mat, expected) in enumerate(test_cases):
            try:
                # Make deep copy since some solutions might modify input
                input_copy = [row[:] for row in input_mat]
                result = solution_func(input_copy)
                
                if result != expected:
                    print(f"  FAILED Test Case {j+1}")
                    print(f"    Input: {input_mat}")
                    print(f"    Expected: {expected}")
                    print(f"    Got: {result}")
                else:
                    print(f"  Test Case {j+1}: PASSED ✓")
            except Exception as e:
                print(f"  ERROR in Test Case {j+1}: {e}")
        print()

# INTERVIEW STRATEGY GUIDE
interview_strategy = """
INTERVIEW WALKTHROUGH (7-9 minutes total):

1. PROBLEM UNDERSTANDING (1 minute):
   "I need to find the distance from each cell to the nearest 0."
   "Distance is Manhattan distance (horizontal + vertical steps)."
   "This sounds like a shortest path problem - BFS is perfect for this."

2. INITIAL APPROACH - BRUTE FORCE (1 minute):
   "My first thought: for each 1, run BFS to find nearest 0."
   "This works but is O(mn * mn) = O(m²n²) - too slow for large matrices."
   "Let me think of a better approach..."

3. KEY INSIGHT - MULTI-SOURCE BFS (1 minute):
   "Instead of BFS from each 1, what if I start BFS from ALL 0s simultaneously?"
   "This is called multi-source BFS - like spreading water from all 0s at once."
   "The first time BFS reaches a cell, that's the shortest distance to any 0."

4. IMPLEMENTATION (3-4 minutes):
   - Initialize result matrix with infinity (except 0s)
   - Add all 0s to BFS queue initially
   - Standard BFS with 4-directional movement
   - Update distances only when we find shorter path
   - Key: process all 0s simultaneously, not one by one

5. COMPLEXITY ANALYSIS (1 minute):
   "Time: O(mn) - each cell visited at most once"
   "Space: O(mn) - queue can hold up to mn cells, result matrix"
   "Much better than O(m²n²) brute force!"

6. ALTERNATIVE APPROACHES (1 minute):
   "Could also solve with DP - two passes through matrix"
   "But BFS is more intuitive for shortest path problems"

KEY TALKING POINTS:
✓ "Multi-source BFS is the key insight - start from all 0s simultaneously"
✓ "Each cell is visited at most once, so it's O(mn) time"
✓ "First time BFS reaches a cell gives shortest distance"
✓ "Standard BFS template with 4-directional movement"

COMMON MISTAKES TO AVOID:
✗ Running separate BFS from each 1 (inefficient O(m²n²))
✗ Not initializing result matrix properly (forgetting infinity values)
✗ Processing 0s one by one instead of simultaneously
✗ Not checking bounds properly in BFS
✗ Modifying input matrix instead of using separate result matrix
"""

# ALGORITHM EXPLANATION
algorithm_deep_dive = """
WHY MULTI-SOURCE BFS WORKS:

1. INTUITION:
   - Imagine all 0s as water sources
   - Water spreads simultaneously from all sources
   - First time water reaches a cell = shortest distance to any water source
   - This is exactly what multi-source BFS does

2. CORRECTNESS:
   - BFS guarantees shortest path in unweighted graphs
   - Each cell is a node, adjacent cells are connected edges
   - Starting from all 0s simultaneously doesn't break BFS properties
   - When BFS first reaches a cell, it's via shortest path from some 0

3. EFFICIENCY:
   - Instead of mn separate BFS calls (one from each 1)
   - We do single BFS starting from all 0s
   - Each cell processed exactly once
   - Total time: O(mn) instead of O(m²n²)

4. IMPLEMENTATION DETAILS:
   - Use deque for O(1) queue operations
   - Check bounds before accessing neighbors
   - Only add to queue if we found shorter distance
   - Initialize distances correctly (0 for zeros, infinity for ones)

COMPARISON WITH OTHER APPROACHES:

1. BRUTE FORCE BFS:
   - Time: O(m²n²), Space: O(mn)
   - Easy to understand but too slow
   - Good for explaining initial thinking

2. DYNAMIC PROGRAMMING:
   - Time: O(mn), Space: O(mn) 
   - Two passes: top-left to bottom-right, then reverse
   - Less intuitive but also O(mn) optimal
   - Good alternative to mention

3. MULTI-SOURCE BFS:
   - Time: O(mn), Space: O(mn)
   - Most intuitive for shortest path problems
   - Single pass with optimal complexity
   - Standard solution expected in interviews
"""

# EDGE CASES AND TESTING
edge_cases_guide = """
IMPORTANT EDGE CASES:

1. SINGLE CELL MATRICES:
   - [[0]] → [[0]] (distance from 0 to itself is 0)
   - [[1]] → Invalid per problem constraints (must have at least one 0)

2. ALL ZEROS:
   - [[0,0],[0,0]] → [[0,0],[0,0]]
   - Every cell already at distance 0

3. SINGLE ROW/COLUMN:
   - [[0,1,1,1,0]] → [[0,1,2,1,0]]
   - BFS still works in 1D case

4. CORNERS AND EDGES:
   - 0s at corners/edges should propagate correctly
   - Check boundary conditions in BFS

5. LARGE DISTANCES:
   - Matrix where some 1s are far from any 0
   - Ensure algorithm handles distances > matrix dimensions

6. CHECKERBOARD PATTERN:
   - [[0,1,0],[1,0,1],[0,1,0]]
   - Tests that algorithm finds truly shortest paths

TESTING STRATEGY:
- Verify result matrix dimensions match input
- Check that all 0s have distance 0 in result
- Verify distances are Manhattan distances
- Test with small examples you can verify by hand
- Ensure no modification of input matrix
- Check boundary handling (corners, edges)

DEBUGGING TIPS:
- Print intermediate states of BFS queue and distances
- Verify initialization step (all 0s added to queue)
- Check that BFS processes cells in correct order
- Ensure proper bounds checking in neighbor exploration
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*70)
    print(interview_strategy)
    print("\n" + "="*70)
    print(algorithm_deep_dive)
    print("\n" + "="*70)
    print(edge_cases_guide)
