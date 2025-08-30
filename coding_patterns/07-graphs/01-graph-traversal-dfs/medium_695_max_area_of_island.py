from typing import List
from collections import deque

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        Problem: Find the maximum area of an island in a 2D binary grid.
        An island is a group of connected 1s (horizontally or vertically).
        
        APPROACH 1: DFS (MOST COMMON INTERVIEW SOLUTION)
        Time: O(m * n) - visit each cell at most once
        Space: O(m * n) - recursion stack in worst case (entire grid is one island)
        
        This is the most intuitive and expected approach.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        max_area = 0
        
        def dfs(row, col):
            """
            DFS to calculate area of island starting from (row, col)
            Returns the total area of the connected island
            """
            # Base cases: out of bounds or water/already visited
            if (row < 0 or row >= rows or col < 0 or col >= cols or 
                grid[row][col] != 1):
                return 0
            
            # Mark current cell as visited by setting to 0
            grid[row][col] = 0
            
            # Count current cell + area from all 4 neighbors
            area = 1
            area += dfs(row + 1, col)  # Down
            area += dfs(row - 1, col)  # Up
            area += dfs(row, col + 1)  # Right
            area += dfs(row, col - 1)  # Left
            
            return area
        
        # Check each cell as potential island start
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    current_area = dfs(i, j)
                    max_area = max(max_area, current_area)
        
        return max_area
    
    def maxAreaOfIsland_preserve_input(self, grid: List[List[int]]) -> int:
        """
        APPROACH 2: DFS WITHOUT MODIFYING INPUT
        Time: O(m * n)
        Space: O(m * n) - visited set + recursion stack
        
        Better practice to not modify input grid.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        max_area = 0
        
        def dfs(row, col):
            """DFS with explicit visited tracking"""
            if (row < 0 or row >= rows or col < 0 or col >= cols or 
                grid[row][col] != 1 or (row, col) in visited):
                return 0
            
            visited.add((row, col))
            
            # Count current cell + neighbors
            area = 1
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in directions:
                area += dfs(row + dr, col + dc)
            
            return area
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1 and (i, j) not in visited:
                    current_area = dfs(i, j)
                    max_area = max(max_area, current_area)
        
        return max_area
    
    def maxAreaOfIsland_bfs(self, grid: List[List[int]]) -> int:
        """
        APPROACH 3: BFS (ITERATIVE ALTERNATIVE)
        Time: O(m * n)
        Space: O(min(m, n)) - queue size in worst case
        
        Good alternative to show you know both DFS and BFS.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        max_area = 0
        
        def bfs(start_row, start_col):
            """BFS to calculate island area"""
            if (start_row, start_col) in visited or grid[start_row][start_col] != 1:
                return 0
            
            queue = deque([(start_row, start_col)])
            visited.add((start_row, start_col))
            area = 0
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            
            while queue:
                row, col = queue.popleft()
                area += 1
                
                # Add all valid neighbors to queue
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    
                    if (0 <= new_row < rows and 0 <= new_col < cols and 
                        grid[new_row][new_col] == 1 and 
                        (new_row, new_col) not in visited):
                        
                        visited.add((new_row, new_col))
                        queue.append((new_row, new_col))
            
            return area
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1 and (i, j) not in visited:
                    current_area = bfs(i, j)
                    max_area = max(max_area, current_area)
        
        return max_area
    
    def maxAreaOfIsland_union_find(self, grid: List[List[int]]) -> int:
        """
        APPROACH 4: UNION-FIND (ADVANCED APPROACH)
        Time: O(m * n * α(m * n)) where α is inverse Ackermann function
        Space: O(m * n)
        
        Overkill for this problem but good to mention for follow-ups.
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        
        class UnionFind:
            def __init__(self):
                self.parent = {}
                self.size = {}
            
            def make_set(self, x):
                if x not in self.parent:
                    self.parent[x] = x
                    self.size[x] = 1
            
            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])  # Path compression
                return self.parent[x]
            
            def union(self, x, y):
                root_x, root_y = self.find(x), self.find(y)
                if root_x != root_y:
                    # Union by size
                    if self.size[root_x] < self.size[root_y]:
                        root_x, root_y = root_y, root_x
                    self.parent[root_y] = root_x
                    self.size[root_x] += self.size[root_y]
        
        uf = UnionFind()
        
        # Create sets for all land cells
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    uf.make_set((i, j))
        
        # Union adjacent land cells
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    for dr, dc in directions:
                        ni, nj = i + dr, j + dc
                        if (0 <= ni < rows and 0 <= nj < cols and 
                            grid[ni][nj] == 1):
                            uf.union((i, j), (ni, nj))
        
        # Find maximum component size
        max_area = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    root = uf.find((i, j))
                    max_area = max(max_area, uf.size[root])
        
        return max_area

# INTERVIEW DEMONSTRATION CLASS
class InterviewSolution:
    """
    Clean, interview-ready solution with clear explanation
    """
    
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        MAIN INTERVIEW SOLUTION: DFS approach
        Find the largest connected component of 1s in the grid
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        max_area = 0
        
        def calculate_island_area(row, col):
            """
            DFS to calculate area of island starting from (row, col)
            Modifies grid by marking visited cells as 0
            """
            # Base case: invalid position or water/already visited
            if (row < 0 or row >= rows or 
                col < 0 or col >= cols or 
                grid[row][col] != 1):
                return 0
            
            # Mark as visited to avoid revisiting
            grid[row][col] = 0
            
            # Count current cell + recursively count neighbors
            current_area = 1
            current_area += calculate_island_area(row + 1, col)  # Down
            current_area += calculate_island_area(row - 1, col)  # Up  
            current_area += calculate_island_area(row, col + 1)  # Right
            current_area += calculate_island_area(row, col - 1)  # Left
            
            return current_area
        
        # Try each cell as potential island starting point
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:  # Found unvisited land
                    island_area = calculate_island_area(i, j)
                    max_area = max(max_area, island_area)
        
        return max_area
    
    def maxAreaOfIsland_clean(self, grid: List[List[int]]) -> int:
        """
        ALTERNATIVE: Clean version without modifying input
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()
        
        def dfs(row, col):
            """DFS with visited set instead of modifying grid"""
            if (row < 0 or row >= rows or col < 0 or col >= cols or 
                grid[row][col] != 1 or (row, col) in visited):
                return 0
            
            visited.add((row, col))
            
            area = 1
            # Use direction array for cleaner code
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                area += dfs(row + dr, col + dc)
            
            return area
        
        max_area = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1 and (i, j) not in visited:
                    max_area = max(max_area, dfs(i, j))
        
        return max_area

# COMPREHENSIVE TESTING
def test_solutions():
    """Test all solution approaches"""
    # Note: Some solutions modify input, so we need fresh copies
    def get_test_cases():
        return [
            # (input_grid, expected_output)
            ([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]], 4),
            ([[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]], 6),
            ([[0,0,0,0,0,0,0,0]], 0),
            ([[1]], 1),
            ([[1,1,1],[1,0,1],[1,1,1]], 8),
            ([[0]], 0),
        ]
    
    solutions = [
        ("DFS (modifies input)", Solution().maxAreaOfIsland),
        ("DFS (preserves input)", Solution().maxAreaOfIsland_preserve_input),
        ("BFS", Solution().maxAreaOfIsland_bfs),
        ("Union-Find", Solution().maxAreaOfIsland_union_find),
        ("Interview DFS", InterviewSolution().maxAreaOfIsland),
        ("Interview Clean", InterviewSolution().maxAreaOfIsland_clean),
    ]
    
    for name, solution_func in solutions:
        print(f"Testing {name}...")
        test_cases = get_test_cases()
        
        for i, (grid, expected) in enumerate(test_cases):
            # Make deep copy since some solutions modify input
            grid_copy = [row[:] for row in grid]
            
            try:
                result = solution_func(grid_copy)
                if result == expected:
                    print(f"  Test {i+1}: PASSED ✓")
                else:
                    print(f"  Test {i+1}: FAILED - Expected {expected}, got {result}")
            except Exception as e:
                print(f"  Test {i+1}: ERROR - {e}")
        print()

# INTERVIEW STRATEGY GUIDE
interview_strategy = """
INTERVIEW WALKTHROUGH (6-8 minutes total):

1. PROBLEM UNDERSTANDING (1 minute):
   "I need to find the largest connected component of 1s in a 2D grid."
   "Connected means horizontally or vertically adjacent (not diagonally)."
   "This is a classic graph traversal problem - I can use DFS or BFS."

2. APPROACH EXPLANATION (1 minute):
   "I'll iterate through each cell in the grid."
   "When I find a 1, I'll use DFS to explore the entire island and count its area."
   "I'll keep track of the maximum area found."
   "To avoid double-counting, I'll mark visited cells (either modify grid or use visited set)."

3. IMPLEMENTATION CHOICE (30 seconds):
   "I'll start with DFS since it's more intuitive for this problem."
   "I can modify the grid in-place by changing 1s to 0s as I visit them."
   "This saves space compared to using a separate visited set."

4. CODE IMPLEMENTATION (3-4 minutes):
   - Show the main function that iterates through grid
   - Implement DFS helper function with clear base cases
   - Demonstrate marking cells as visited
   - Show how to count area (1 + sum of neighbor areas)
   - Handle boundary checking properly

5. COMPLEXITY ANALYSIS (30 seconds):
   "Time: O(m*n) - each cell visited at most once"
   "Space: O(m*n) - recursion stack in worst case (if entire grid is one island)"

6. ALTERNATIVE APPROACHES (1 minute):
   "Could also use BFS with a queue - same time complexity"
   "Could use Union-Find for more complex scenarios with dynamic updates"
   "Could use visited set instead of modifying input - trade space for cleaner code"

KEY TALKING POINTS:
✓ "This is a connected components problem - perfect for DFS/BFS"
✓ "I'll mark visited cells to avoid double-counting"
✓ "DFS naturally calculates area by summing 1 + neighbor areas"
✓ "Each cell is visited at most once, so it's O(m*n) time"

COMMON MISTAKES TO AVOID:
✗ Not handling boundary conditions properly
✗ Forgetting to mark cells as visited (infinite recursion)
✗ Not resetting/handling visited state between different islands
✗ Counting the same cell multiple times
✗ Stack overflow on large connected components (prefer iterative BFS if concerned)

FOLLOW-UP QUESTIONS TO EXPECT:
- "What if islands could be connected diagonally?" → Add diagonal directions
- "What if you couldn't modify the input?" → Use visited set
- "What if the grid was too large for recursion?" → Use iterative BFS
- "What if you needed to handle dynamic updates?" → Union-Find approach
"""

# ALGORITHM VARIATIONS
algorithm_variations = """
DIFFERENT IMPLEMENTATION STYLES:

1. DFS WITH GRID MODIFICATION (Most Common):
   - Pros: O(1) extra space, simple implementation
   - Cons: Modifies input (not always acceptable)
   - Best for: When input modification is allowed

2. DFS WITH VISITED SET:
   - Pros: Preserves input, clear separation of concerns
   - Cons: O(m*n) extra space for visited set
   - Best for: When input must be preserved

3. BFS WITH QUEUE:
   - Pros: No recursion stack overflow risk, iterative
   - Cons: Slightly more complex, requires queue
   - Best for: Very large grids or when avoiding recursion

4. UNION-FIND:
   - Pros: Good for dynamic scenarios, path compression
   - Cons: Overkill for this problem, more complex
   - Best for: When you have updates/queries over time

SPACE-TIME TRADE-OFFS:
- Modify input: O(1) extra space, O(m*n) time
- Visited set: O(m*n) extra space, O(m*n) time  
- BFS queue: O(min(m,n)) extra space, O(m*n) time
- Union-Find: O(m*n) extra space, O(m*n*α(m*n)) time

WHEN TO USE EACH:
- Interview default: DFS with grid modification
- Production code: DFS with visited set (preserve input)
- Large grids: BFS to avoid stack overflow
- Dynamic updates: Union-Find for efficiency
"""

# EDGE CASES AND TESTING
edge_cases_guide = """
IMPORTANT EDGE CASES:

1. EMPTY/NULL GRID:
   - [] or [[]] → return 0
   - Handle gracefully in input validation

2. ALL WATER:
   - [[0,0,0],[0,0,0]] → return 0
   - No islands found, should return 0

3. ALL LAND:
   - [[1,1,1],[1,1,1]] → return total cells (6)
   - Single connected component covering entire grid

4. SINGLE CELL:
   - [[1]] → return 1
   - [[0]] → return 0
   - Minimal valid inputs

5. COMPLEX SHAPES:
   - L-shaped, T-shaped, spiral islands
   - Test that algorithm follows connections correctly

6. MULTIPLE ISLANDS:
   - Various sizes, ensure we find the maximum
   - Test that islands are properly separated

7. BOUNDARY ISLANDS:
   - Islands touching edges/corners of grid
   - Ensure boundary checking works correctly

TESTING STRATEGY:
- Start with simple cases (single cell, all water, all land)
- Test multiple islands of different sizes
- Verify complex shapes are handled correctly
- Check boundary conditions and edge touching
- Test large grids for performance
- Verify no modification of areas that should stay unchanged

DEBUGGING TECHNIQUES:
- Print grid state before and after each DFS call
- Add debug prints in DFS to trace path
- Visualize which cells are being visited
- Check that visited marking works correctly
- Verify boundary conditions with print statements
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*70)
    print(interview_strategy)
    print("\n" + "="*70)
    print(algorithm_variations)
    print("\n" + "="*70)
    print(edge_cases_guide)
