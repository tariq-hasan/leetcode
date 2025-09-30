"""
LeetCode 1631: Path With Minimum Effort
Medium

You are a hiker preparing for an upcoming hike. You are given heights, a 2D 
array of size rows x columns, where heights[i][j] represents the height of 
cell (i, j).

You are situated in the top-left cell, (0, 0), and you hope to travel to the 
bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, 
down, left, or right, and you wish to find a route that requires the minimum 
effort.

A route's effort is the maximum absolute difference in heights between two 
consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the 
bottom-right cell.

Example 1:
Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
Explanation: The route [1,3,5,3,5] has a maximum absolute difference of 2.

Example 2:
Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
Explanation: The route [1,2,3,4,5] has a maximum absolute difference of 1.

Example 3:
Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
"""

from typing import List
import heapq
from collections import deque


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Approach 1: Dijkstra's Algorithm (Modified for Max on Path)
        Time: O(rows * cols * log(rows * cols)), Space: O(rows * cols)
        
        ⭐ RECOMMENDED FOR INTERVIEWS ⭐
        
        Key Insight: This is Dijkstra's with a twist:
        - Instead of summing edge weights, track MAX edge weight seen so far
        - Effort of path = max(abs differences) along the path
        - We minimize this maximum effort across all paths
        """
        rows, cols = len(heights), len(heights[0])
        
        # Directions: up, down, left, right
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Min-heap: (effort, row, col)
        heap = [(0, 0, 0)]  # Start at (0,0) with 0 effort
        
        # Track minimum effort to reach each cell
        min_effort = {}
        
        while heap:
            effort, r, c = heapq.heappop(heap)
            
            # Reached destination
            if r == rows - 1 and c == cols - 1:
                return effort
            
            # Skip if already processed with better effort
            if (r, c) in min_effort:
                continue
            
            min_effort[(r, c)] = effort
            
            # Explore all 4 neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in min_effort:
                    # Effort to this neighbor is max of:
                    # 1. Current path's effort
                    # 2. Difference between current and neighbor cell
                    new_effort = max(effort, abs(heights[r][c] - heights[nr][nc]))
                    heapq.heappush(heap, (new_effort, nr, nc))
        
        return 0  # Should never reach here if input is valid


class Solution2:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Approach 2: Binary Search + BFS/DFS
        Time: O(rows * cols * log(max_height)), Space: O(rows * cols)
        
        Elegant approach combining binary search with graph traversal
        Good alternative to show algorithmic creativity
        """
        rows, cols = len(heights), len(heights[0])
        
        def canReach(max_effort):
            """Check if we can reach destination with given max effort"""
            visited = [[False] * cols for _ in range(rows)]
            queue = deque([(0, 0)])
            visited[0][0] = True
            
            while queue:
                r, c = queue.popleft()
                
                if r == rows - 1 and c == cols - 1:
                    return True
                
                for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        not visited[nr][nc] and
                        abs(heights[r][c] - heights[nr][nc]) <= max_effort):
                        visited[nr][nc] = True
                        queue.append((nr, nc))
            
            return False
        
        # Binary search on the answer
        left, right = 0, max(max(row) for row in heights)
        result = right
        
        while left <= right:
            mid = (left + right) // 2
            
            if canReach(mid):
                result = mid
                right = mid - 1  # Try to find smaller effort
            else:
                left = mid + 1
        
        return result


class Solution3:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Approach 3: Union-Find with Edge Sorting
        Time: O(rows * cols * log(rows * cols)), Space: O(rows * cols)
        
        Creative approach using MST-like thinking
        Sort edges by weight, use Union-Find to connect cells
        """
        rows, cols = len(heights), len(heights[0])
        
        if rows == 1 and cols == 1:
            return 0
        
        # Create all edges with their efforts
        edges = []
        for r in range(rows):
            for c in range(cols):
                cell_id = r * cols + c
                
                # Right neighbor
                if c + 1 < cols:
                    effort = abs(heights[r][c] - heights[r][c + 1])
                    edges.append((effort, cell_id, cell_id + 1))
                
                # Down neighbor
                if r + 1 < rows:
                    effort = abs(heights[r][c] - heights[r + 1][c])
                    edges.append((effort, cell_id, cell_id + cols))
        
        # Sort edges by effort
        edges.sort()
        
        # Union-Find
        parent = list(range(rows * cols))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        start, end = 0, rows * cols - 1
        
        # Process edges in increasing order of effort
        for effort, u, v in edges:
            union(u, v)
            
            # Check if start and end are connected
            if find(start) == find(end):
                return effort
        
        return 0


class Solution4:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Approach 4: Modified Dijkstra's with 2D Array
        Time: O(rows * cols * log(rows * cols)), Space: O(rows * cols)
        
        Alternative implementation using 2D array instead of dictionary
        Sometimes preferred for matrix problems
        """
        rows, cols = len(heights), len(heights[0])
        
        # Initialize effort array with infinity
        effort = [[float('inf')] * cols for _ in range(rows)]
        effort[0][0] = 0
        
        # Min-heap: (effort, row, col)
        heap = [(0, 0, 0)]
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while heap:
            curr_effort, r, c = heapq.heappop(heap)
            
            # Early termination
            if r == rows - 1 and c == cols - 1:
                return curr_effort
            
            # Skip if we've found a better path to this cell
            if curr_effort > effort[r][c]:
                continue
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_effort = max(curr_effort, abs(heights[r][c] - heights[nr][nc]))
                    
                    if new_effort < effort[nr][nc]:
                        effort[nr][nc] = new_effort
                        heapq.heappush(heap, (new_effort, nr, nc))
        
        return effort[rows - 1][cols - 1]


class Solution5:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Approach 5: Binary Search + DFS (Recursive)
        Time: O(rows * cols * log(max_height)), Space: O(rows * cols)
        
        DFS variant of binary search approach
        """
        rows, cols = len(heights), len(heights[0])
        
        def dfs(r, c, max_effort, visited):
            if r == rows - 1 and c == cols - 1:
                return True
            
            visited[r][c] = True
            
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    not visited[nr][nc] and
                    abs(heights[r][c] - heights[nr][nc]) <= max_effort):
                    if dfs(nr, nc, max_effort, visited):
                        return True
            
            return False
        
        # Binary search on effort
        left, right = 0, 10**6
        result = right
        
        while left <= right:
            mid = (left + right) // 2
            visited = [[False] * cols for _ in range(rows)]
            
            if dfs(0, 0, mid, visited):
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        
        return result


# Test cases
def test_solutions():
    solutions = [
        ("Dijkstra's Algorithm (Optimal)", Solution()),
        ("Binary Search + BFS", Solution2()),
        ("Union-Find with Edge Sorting", Solution3()),
        ("Dijkstra's with 2D Array", Solution4()),
        ("Binary Search + DFS", Solution5())
    ]
    
    test_cases = [
        ([[1,2,2],[3,8,2],[5,3,5]], 2),
        ([[1,2,3],[3,8,4],[5,3,5]], 1),
        ([[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]], 0),
        ([[1,10,6,7,9,10,4,9]], 9),
        ([[1]], 0),
        ([[1,2],[2,3]], 1),
        ([[3]], 0),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        all_passed = True
        for heights, expected in test_cases:
            result = solution.minimumEffortPath(heights)
            passed = result == expected
            status = "✓" if passed else "✗"
            if not passed:
                all_passed = False
            rows, cols = len(heights), len(heights[0])
            print(f"  {status} {rows}x{cols} grid -> {result} (expected: {expected})")
        print(f"  {'All tests passed!' if all_passed else 'Some tests failed!'}\n")


if __name__ == "__main__":
    test_solutions()


"""
═══════════════════════════════════════════════════════════════════════════
COMPREHENSIVE INTERVIEW GUIDE
═══════════════════════════════════════════════════════════════════════════

PART 1: PROBLEM RECOGNITION (First 60 seconds)
═══════════════════════════════════════════════════════════════════════════

What to say immediately:

"This is a modified shortest path problem on a 2D grid. The key twist is that 
'effort' is defined as the MAXIMUM absolute difference along a path, not the 
sum. This changes how we think about the problem.

I see three viable approaches:
1. Dijkstra's algorithm (modified) - O((RC) log(RC)) ⭐ OPTIMAL
2. Binary search + BFS/DFS - O(RC log(max_height)) - ELEGANT
3. Union-Find with sorted edges - O((RC) log(RC)) - CREATIVE

I'll implement Dijkstra's as it's most straightforward and optimal."

═══════════════════════════════════════════════════════════════════════════
PART 2: THE CRITICAL INSIGHT
═══════════════════════════════════════════════════════════════════════════

**The Twist from Standard Dijkstra's:**

Standard shortest path:
- Path cost = SUM of edge weights
- dist[v] = dist[u] + weight(u, v)

This problem:
- Path effort = MAX of edge weights
- effort[v] = max(effort[u], weight(u, v))

"Instead of accumulating costs, we're tracking the maximum 'jump' seen so 
far. The effort to reach a cell is the maximum of:
1. The effort to reach the previous cell
2. The difference between the two cells

This still works with Dijkstra's because we're maintaining a minimum value 
that has a monotonic property."

═══════════════════════════════════════════════════════════════════════════
PART 3: WHY DIJKSTRA'S WORKS HERE
═══════════════════════════════════════════════════════════════════════════

Critical to explain:

"Dijkstra's works because of this property: if we reach a cell with effort E,
any future path through that cell will have effort ≥ E. The max operation 
preserves the monotonicity we need:

- If effort[u] = 5 and edge weight is 3, new effort = max(5,3) = 5
- If effort[u] = 5 and edge weight is 7, new effort = max(5,7) = 7

Once we process a cell with minimum effort, we've found the optimal path to 
it - just like in standard Dijkstra's!"

═══════════════════════════════════════════════════════════════════════════
PART 4: IMPLEMENTATION STRATEGY (Solution 1 - Recommended)
═══════════════════════════════════════════════════════════════════════════

Step 1 (2 min): Setup
- "Define directions for 4-directional movement"
- "Initialize heap with (0, 0, 0) - start position with 0 effort"
- "Use dictionary to track visited cells and their minimum effort"

Step 2 (3 min): Main loop structure
- "Pop cell with minimum effort from heap"
- "Check if we reached destination - early return!"
- "Skip if already processed this cell"

Step 3 (8 min): Process neighbors
- "For each of 4 directions, calculate new cell position"
- "Check bounds and if not visited"
- "Calculate new effort: max(current_effort, abs(height_diff))"
- "Push to heap if not visited"

Step 4 (2 min): Return
- "When we pop destination from heap, return its effort"

═══════════════════════════════════════════════════════════════════════════
PART 5: SOLUTION 2 - BINARY SEARCH APPROACH
═══════════════════════════════════════════════════════════════════════════

"An elegant alternative approach:

Observation: If we can reach the destination with effort E, we can also 
reach it with any effort ≥ E (monotonic property).

Algorithm:
1. Binary search on the answer (effort from 0 to max_height)
2. For each candidate effort, use BFS/DFS to check if reachable
3. Only traverse edges where abs(height_diff) ≤ candidate_effort

Time: O(RC × log(max_height)) where max_height ≤ 10^6

This is actually slower than Dijkstra's in worst case, but shows good 
problem-solving creativity. Mention it if time allows!"

═══════════════════════════════════════════════════════════════════════════
PART 6: COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

**Dijkstra's Approach (Solution 1):**

Time: O(R × C × log(R × C))
- Each cell can be added to heap once: O(RC)
- Each heap operation: O(log(RC))
- Total: O(RC log(RC))

Space: O(R × C)
- Heap: O(RC) worst case
- Visited dictionary: O(RC)
- Total: O(RC)

"This is optimal for this problem - we can't do better than visiting all 
cells at least once."

**Binary Search Approach (Solution 2):**

Time: O(R × C × log(max_height))
- Binary search iterations: O(log(max_height)) ≈ O(20)
- Each BFS: O(RC)
- Total: O(RC × log(max_height))

Space: O(R × C) for visited array

"Asymptotically different! Could be faster if max_height is small."

═══════════════════════════════════════════════════════════════════════════
PART 7: EDGE CASES & TESTING
═══════════════════════════════════════════════════════════════════════════

Must discuss:

✓ 1x1 grid → return 0 (already at destination)
✓ Single row/column → maximum difference along that path
✓ All same heights → return 0 (no effort needed)
✓ Path requires backtracking → Dijkstra's handles naturally
✓ Large height differences → algorithm scales well
✓ Multiple paths with same effort → any one is correct

Example walkthrough for [[1,2,2],[3,8,2],[5,3,5]]:

"Let me trace through this:
- Start at (0,0) with height 1
- Path 1→3→5→3→5: efforts are |1-3|=2, |3-5|=2, |5-3|=2, |3-5|=2
  Maximum effort: 2
- Path 1→2→2→8→2→3→5: has effort 6 (the jump 2→8)
- Optimal is effort 2"

═══════════════════════════════════════════════════════════════════════════
PART 8: COMMON MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════

❌ Using standard BFS (ignores effort, finds any path not optimal path)
❌ Summing efforts instead of taking maximum
❌ Not using priority queue (degrades to exponential time)
❌ Processing cells multiple times (should skip if visited)
❌ Not checking bounds properly
❌ Forgetting early termination when reaching destination
❌ Wrong effort calculation: using current height instead of difference

═══════════════════════════════════════════════════════════════════════════
PART 9: FOLLOW-UP QUESTIONS & ANSWERS
═══════════════════════════════════════════════════════════════════════════

Q: "What if we can move diagonally too?"
A: "Just add 4 more directions: (1,1), (1,-1), (-1,1), (-1,-1). The 
   algorithm stays the same. Time complexity unchanged."

Q: "What if effort is defined as SUM of differences instead of MAX?"
A: "Then it's standard Dijkstra's! Replace max() with + in the effort 
   calculation. Same algorithm structure, different operation."

Q: "Can you optimize space?"
A: "Hard to optimize significantly - need to track visited cells. Could use 
   bit manipulation if grid is small, but not worth the complexity."

Q: "What if we want to find the actual path, not just the effort?"
A: "Add a parent/predecessor tracking. When updating effort[v], also store 
   parent[v] = u. Backtrack from destination to reconstruct path."

Q: "How would you handle very large grids?"
A: "Consider:
   - A* with heuristic (Manhattan distance to goal)
   - Bidirectional search (meet in middle)
   - Memory-mapped storage for very large grids
   - Parallel processing of independent regions"

Q: "What if there are obstacles (cells you can't enter)?"
A: "Simply skip those cells when processing neighbors. Check if cell is 
   obstacle before adding to heap."

═══════════════════════════════════════════════════════════════════════════
PART 10: COMPARISON OF ALL APPROACHES
═══════════════════════════════════════════════════════════════════════════

Approach              Time              Space    Interview Rating
------------------------------------------------------------------
Dijkstra's           O(RC log RC)      O(RC)    ⭐⭐⭐⭐⭐ BEST
Binary Search+BFS    O(RC log H)       O(RC)    ⭐⭐⭐⭐ ELEGANT
Union-Find           O(RC log RC)      O(RC)    ⭐⭐⭐ CREATIVE
Binary Search+DFS    O(RC log H)       O(RC)    ⭐⭐⭐ ALTERNATIVE

Where: R=rows, C=cols, H=max_height

Recommendation: Always start with Dijkstra's. Mention binary search if time.

═══════════════════════════════════════════════════════════════════════════
PART 11: KEY TALKING POINTS WHILE CODING
═══════════════════════════════════════════════════════════════════════════

"I'm using a min-heap to always process the cell with minimum effort first..."

"The key line is: new_effort = max(current_effort, height_difference) - 
this captures that effort is the maximum jump, not the sum..."

"I'm checking if the cell is in min_effort dictionary to avoid reprocessing - 
once we've found the optimal effort to a cell, it won't improve..."

"Early termination when we pop the destination cell - at that moment we've 
found the optimal effort..."

"Using a dictionary for visited tracking is cleaner than a 2D boolean array 
in Python, though both work..."

═══════════════════════════════════════════════════════════════════════════
PART 12: TIME MANAGEMENT (45-minute interview)
═══════════════════════════════════════════════════════════════════════════

0-3 min:   Understand problem, identify it's modified Dijkstra's
3-8 min:   Explain approach, discuss max vs sum insight
8-28 min:  Code Solution 1 (Dijkstra's)
28-33 min: Trace through example
33-38 min: Test edge cases (1x1 grid, all same heights)
38-42 min: Complexity analysis
42-45 min: Discuss binary search alternative, answer follow-ups

═══════════════════════════════════════════════════════════════════════════
PART 13: WHAT MAKES THIS PROBLEM SPECIAL
═══════════════════════════════════════════════════════════════════════════

This problem tests:

✓ Recognition that it's a graph problem (2D grid = graph)
✓ Understanding Dijkstra's algorithm deeply (not just memorization)
✓ Ability to adapt algorithms (max instead of sum)
✓ Graph traversal on implicit graphs (grid as graph)
✓ Multiple valid approaches (Dijkstra's vs binary search)

"This is a great interview problem because there's no trick - it's pure 
algorithmic thinking and adaptation."

═══════════════════════════════════════════════════════════════════════════
FINAL RECOMMENDATION
═══════════════════════════════════════════════════════════════════════════

IMPLEMENT: Solution 1 (Dijkstra's with max operation)

MENTION: "I could also solve this with binary search on the answer combined 
with BFS, which would be O(RC × log(max_height)). That's elegant but 
potentially slower."

DEMONSTRATE: 
- Strong grasp of Dijkstra's algorithm
- Ability to modify algorithms for new problems
- Understanding of the max vs sum distinction
- Clean, bug-free implementation

The fact that it's "Dijkstra's with one operation changed" shows algorithmic 
maturity - you understand the fundamental principles, not just recipes.
"""
