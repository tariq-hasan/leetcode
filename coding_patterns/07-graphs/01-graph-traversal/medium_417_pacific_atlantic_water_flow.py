"""
LeetCode 417: Pacific Atlantic Water Flow

Problem: Given an m x n rectangular island that borders both the Pacific Ocean 
and Atlantic Ocean. Water can only flow in four directions and only from a cell 
to another one with height equal or lower. Find all cells where water can flow 
to both the Pacific and Atlantic oceans.

Key Insight: Instead of checking each cell individually (expensive), start from 
ocean borders and work backwards using reverse flow (water flows upward/equal).

Pacific Ocean touches: top edge and left edge
Atlantic Ocean touches: bottom edge and right edge

Time Complexity: O(M*N) where M and N are grid dimensions
Space Complexity: O(M*N) for visited sets and recursion stack
"""

class Solution:
    def pacificAtlantic(self, heights):
        """
        DFS Solution - Start from ocean borders, flow backwards
        This is the optimal approach for interviews
        """
        if not heights or not heights[0]:
            return []
        
        rows, cols = len(heights), len(heights[0])
        
        # Sets to track which cells can reach each ocean
        pacific_reachable = set()
        atlantic_reachable = set()
        
        def dfs(r, c, reachable, prev_height):
            # Base cases: out of bounds, already visited, or can't flow here
            if ((r, c) in reachable or r < 0 or r >= rows or 
                c < 0 or c >= cols or heights[r][c] < prev_height):
                return
            
            reachable.add((r, c))
            
            # Explore all 4 directions (water flows backwards/upward)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc, reachable, heights[r][c])
        
        # Start DFS from Pacific Ocean borders (top and left edges)
        for c in range(cols):
            dfs(0, c, pacific_reachable, heights[0][c])           # top edge
            dfs(rows-1, c, atlantic_reachable, heights[rows-1][c]) # bottom edge
        
        for r in range(rows):
            dfs(r, 0, pacific_reachable, heights[r][0])           # left edge
            dfs(r, cols-1, atlantic_reachable, heights[r][cols-1]) # right edge
        
        # Find intersection - cells that can reach both oceans
        result = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pacific_reachable and (r, c) in atlantic_reachable:
                    result.append([r, c])
        
        return result

    def pacificAtlanticBFS(self, heights):
        """
        BFS Solution - Better for very large grids
        """
        if not heights or not heights[0]:
            return []
        
        from collections import deque
        
        rows, cols = len(heights), len(heights[0])
        
        pacific_queue = deque()
        atlantic_queue = deque()
        pacific_reachable = set()
        atlantic_reachable = set()
        
        # Initialize queues with border cells
        for c in range(cols):
            pacific_queue.append((0, c))
            pacific_reachable.add((0, c))
            atlantic_queue.append((rows-1, c))
            atlantic_reachable.add((rows-1, c))
        
        for r in range(rows):
            pacific_queue.append((r, 0))
            pacific_reachable.add((r, 0))
            atlantic_queue.append((r, cols-1))
            atlantic_reachable.add((r, cols-1))
        
        def bfs(queue, reachable):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            while queue:
                r, c = queue.popleft()
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        (nr, nc) not in reachable and 
                        heights[nr][nc] >= heights[r][c]):  # reverse flow
                        reachable.add((nr, nc))
                        queue.append((nr, nc))
        
        bfs(pacific_queue, pacific_reachable)
        bfs(atlantic_queue, atlantic_reachable)
        
        # Find intersection
        result = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pacific_reachable and (r, c) in atlantic_reachable:
                    result.append([r, c])
        
        return result

    def pacificAtlanticOptimized(self, heights):
        """
        Optimized solution with combined traversal and early termination
        """
        if not heights or not heights[0]:
            return []
        
        rows, cols = len(heights), len(heights[0])
        
        # Use matrices instead of sets for potentially better cache performance
        pacific = [[False] * cols for _ in range(rows)]
        atlantic = [[False] * cols for _ in range(rows)]
        
        def dfs(r, c, ocean, prev_height):
            if (r < 0 or r >= rows or c < 0 or c >= cols or 
                ocean[r][c] or heights[r][c] < prev_height):
                return
            
            ocean[r][c] = True
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(r + dr, c + dc, ocean, heights[r][c])
        
        # Start from borders
        for i in range(rows):
            dfs(i, 0, pacific, heights[i][0])          # left edge -> pacific
            dfs(i, cols-1, atlantic, heights[i][cols-1]) # right edge -> atlantic
        
        for j in range(cols):
            dfs(0, j, pacific, heights[0][j])          # top edge -> pacific
            dfs(rows-1, j, atlantic, heights[rows-1][j]) # bottom edge -> atlantic
        
        # Collect results
        result = []
        for r in range(rows):
            for c in range(cols):
                if pacific[r][c] and atlantic[r][c]:
                    result.append([r, c])
        
        return result

    def pacificAtlanticMemoized(self, heights):
        """
        Alternative approach with memoization (less efficient but shows technique)
        """
        if not heights or not heights[0]:
            return []
        
        rows, cols = len(heights), len(heights[0])
        
        # Memoization for each ocean
        pacific_memo = {}
        atlantic_memo = {}
        
        def can_reach_pacific(r, c, visited):
            if (r, c) in visited:
                return False
            if (r, c) in pacific_memo:
                return pacific_memo[(r, c)]
            
            # Base case: reached Pacific Ocean border
            if r == 0 or c == 0:
                pacific_memo[(r, c)] = True
                return True
            
            visited.add((r, c))
            
            # Try all 4 directions (normal flow - downward/equal)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    heights[nr][nc] <= heights[r][c] and 
                    can_reach_pacific(nr, nc, visited)):
                    pacific_memo[(r, c)] = True
                    visited.remove((r, c))
                    return True
            
            visited.remove((r, c))
            pacific_memo[(r, c)] = False
            return False
        
        def can_reach_atlantic(r, c, visited):
            if (r, c) in visited:
                return False
            if (r, c) in atlantic_memo:
                return atlantic_memo[(r, c)]
            
            # Base case: reached Atlantic Ocean border
            if r == rows-1 or c == cols-1:
                atlantic_memo[(r, c)] = True
                return True
            
            visited.add((r, c))
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    heights[nr][nc] <= heights[r][c] and 
                    can_reach_atlantic(nr, nc, visited)):
                    atlantic_memo[(r, c)] = True
                    visited.remove((r, c))
                    return True
            
            visited.remove((r, c))
            atlantic_memo[(r, c)] = False
            return False
        
        result = []
        for r in range(rows):
            for c in range(cols):
                if (can_reach_pacific(r, c, set()) and 
                    can_reach_atlantic(r, c, set())):
                    result.append([r, c])
        
        return result


# Test cases for interview
def test_pacific_atlantic():
    solution = Solution()
    
    # Test case 1: Standard case
    heights1 = [
        [1,2,2,3,5],
        [3,2,3,4,4],
        [2,4,5,3,1],
        [6,7,1,4,5],
        [5,1,1,2,4]
    ]
    result1 = solution.pacificAtlantic(heights1)
    print(f"Test 1: {sorted(result1)}")
    # Expected: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    
    # Test case 2: Simple case
    heights2 = [[2,1],[1,2]]
    result2 = solution.pacificAtlantic(heights2)
    print(f"Test 2: {sorted(result2)}")
    # Expected: [[0,0],[0,1],[1,0],[1,1]]
    
    # Test case 3: Single cell
    heights3 = [[1]]
    result3 = solution.pacificAtlantic(heights3)
    print(f"Test 3: {result3}")
    # Expected: [[0,0]]
    
    # Test case 4: No valid cells (theoretical)
    heights4 = [
        [1,2,3],
        [8,9,4],
        [7,6,5]
    ]
    result4 = solution.pacificAtlantic(heights4)
    print(f"Test 4: {sorted(result4)}")

if __name__ == "__main__":
    test_pacific_atlantic()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Water flows from higher/equal to lower heights
   - Pacific Ocean: touches top and left edges
   - Atlantic Ocean: touches bottom and right edges
   - Find cells where water can reach BOTH oceans

2. KEY INSIGHT - REVERSE FLOW:
   - Instead of checking each cell individually (O(M*N) DFS calls)
   - Start from ocean borders and flow backwards (upward/equal heights)
   - Much more efficient: only 2 DFS traversals total

3. ALGORITHM STEPS:
   - Create two sets: pacific_reachable, atlantic_reachable
   - DFS from Pacific borders (top + left edges) flowing upward
   - DFS from Atlantic borders (bottom + right edges) flowing upward
   - Find intersection of both sets

4. WHY REVERSE FLOW WORKS:
   - If water can flow from A to B, then we can reach A from B
   - Starting from borders eliminates need to check border conditions
   - Single traversal marks all reachable cells for each ocean

5. EDGE CASES TO MENTION:
   - Single cell (always valid - touches both oceans)
   - All same height (all cells valid)
   - Monotonic increasing/decreasing
   - Empty grid

6. TIME/SPACE COMPLEXITY:
   - Time: O(M*N) - each cell visited at most twice
   - Space: O(M*N) for visited sets + recursion stack

7. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Why not check each cell individually?" -> Explain efficiency difference
   - "What if grid is very large?" -> BFS approach
   - "Can you optimize space?" -> Use boolean matrices instead of sets
   - "What about diagonal flow?" -> Add diagonal directions
   - "Multiple oceans?" -> Extend to k oceans with k traversals

8. COMPARISON WITH SIMILAR PROBLEMS:
   - Number of Islands: Count components vs. reachability
   - Surrounded Regions: Border connectivity but different goal
   - Flood Fill: Single traversal vs. multiple ocean traversals

9. ALTERNATIVE APPROACHES:
   - Naive: O(M*N) DFS calls from each cell (too slow)
   - Memoized DFS: Better but still suboptimal
   - Union-Find: Possible but more complex

10. REAL-WORLD APPLICATIONS:
    - Watershed analysis in geography
    - Network reachability problems
    - Game development (terrain water simulation)
    - Circuit design (signal flow analysis)

11. IMPLEMENTATION TIPS:
    - Use sets for O(1) lookup vs. lists
    - Consider matrix vs. set trade-offs
    - Handle border initialization carefully
    - Remember reverse flow condition (>= instead of <=)
"""
