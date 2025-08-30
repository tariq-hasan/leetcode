"""
LeetCode 778. Swim in Rising Water
Problem: On an N x N grid, each square grid[i][j] represents the elevation at that point (i,j).

Now rain starts to fall. At time t, the depth of the water everywhere is t. You can swim from a square 
to another 4-directionally adjacent square if and only if the elevation of both squares is at most t.

You can swim infinite distance in zero time. Of course, you must stay within the boundaries of the grid 
during your swim.

You start at the top left square (0, 0). What is the minimum time until you can reach the bottom right square (N-1, N-1)?

Examples:
- Input: grid = [[0,2],[1,3]], Output: 3
  At t=3, water level is 3, so we can swim through all cells (max elevation = 3)

Key insight: Find minimum time t such that there exists a path from (0,0) to (n-1,n-1) 
where all cells in path have elevation ≤ t.
"""

# SOLUTION 1: Binary Search + DFS/BFS (PREFERRED for interviews)
# Time: O(n²·log(max_elevation)), Space: O(n²)
def swimInWater(grid):
    """
    Binary search on answer + DFS to check reachability
    Most intuitive approach that interviewers expect
    """
    n = len(grid)
    
    def canReach(time_limit):
        """Check if we can reach (n-1,n-1) with water level = time_limit"""
        if grid[0][0] > time_limit:
            return False
        
        visited = [[False] * n for _ in range(n)]
        
        def dfs(i, j):
            if i == n-1 and j == n-1:
                return True
            
            visited[i][j] = True
            
            # Try all 4 directions
            for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
                ni, nj = i + di, j + dj
                
                if (0 <= ni < n and 0 <= nj < n and 
                    not visited[ni][nj] and 
                    grid[ni][nj] <= time_limit):
                    
                    if dfs(ni, nj):
                        return True
            
            return False
        
        return dfs(0, 0)
    
    # Binary search on the answer
    left = max(grid[0][0], grid[n-1][n-1])  # Minimum possible time
    right = max(max(row) for row in grid)   # Maximum possible time
    
    while left < right:
        mid = (left + right) // 2
        
        if canReach(mid):
            right = mid
        else:
            left = mid + 1
    
    return left


# SOLUTION 2: Dijkstra's Algorithm (Most Optimal)
# Time: O(n²·log(n²)), Space: O(n²)
def swimInWater_dijkstra(grid):
    """
    Dijkstra's algorithm - find path with minimum maximum elevation
    This is actually finding the path that minimizes the maximum edge weight
    """
    import heapq
    
    n = len(grid)
    
    # Priority queue: (max_elevation_so_far, row, col)
    pq = [(grid[0][0], 0, 0)]
    visited = [[False] * n for _ in range(n)]
    
    while pq:
        curr_max, i, j = heapq.heappop(pq)
        
        if visited[i][j]:
            continue
        
        visited[i][j] = True
        
        # Reached destination
        if i == n-1 and j == n-1:
            return curr_max
        
        # Explore all 4 directions
        for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
            ni, nj = i + di, j + dj
            
            if (0 <= ni < n and 0 <= nj < n and not visited[ni][nj]):
                # The "cost" is the maximum elevation seen so far
                new_max = max(curr_max, grid[ni][nj])
                heapq.heappush(pq, (new_max, ni, nj))
    
    return -1  # Should never reach here


# SOLUTION 3: Union-Find with Sorted Edges (Advanced)
# Time: O(n²·log(n²)), Space: O(n²)
def swimInWater_unionfind(grid):
    """
    Union-Find approach: Process cells in elevation order
    Connect cells when water level allows, stop when start and end are connected
    """
    n = len(grid)
    
    class UnionFind:
        def __init__(self, size):
            self.parent = list(range(size))
            self.rank = [0] * size
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            
            return True
        
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    def get_index(i, j):
        return i * n + j
    
    # Create list of all cells sorted by elevation
    cells = []
    for i in range(n):
        for j in range(n):
            cells.append((grid[i][j], i, j))
    
    cells.sort()  # Sort by elevation
    
    uf = UnionFind(n * n)
    start, end = get_index(0, 0), get_index(n-1, n-1)
    
    for elevation, i, j in cells:
        # Connect to adjacent cells with elevation <= current
        for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
            ni, nj = i + di, j + dj
            
            if (0 <= ni < n and 0 <= nj < n and 
                grid[ni][nj] <= elevation):
                uf.union(get_index(i, j), get_index(ni, nj))
        
        # Check if start and end are connected
        if uf.connected(start, end):
            return elevation
    
    return grid[n-1][n-1]  # Should never reach here


# SOLUTION 4: Modified Dijkstra (Priority Queue on Time)
# Time: O(n²·log(n²)), Space: O(n²)
def swimInWater_dijkstra_time(grid):
    """
    Alternative Dijkstra formulation: minimize the time needed
    Priority queue based on earliest possible arrival time
    """
    import heapq
    
    n = len(grid)
    
    # dist[i][j] = minimum time to reach cell (i,j)
    dist = [[float('inf')] * n for _ in range(n)]
    dist[0][0] = grid[0][0]
    
    # Priority queue: (time, row, col)
    pq = [(grid[0][0], 0, 0)]
    
    while pq:
        curr_time, i, j = heapq.heappop(pq)
        
        # If we found a better path already, skip
        if curr_time > dist[i][j]:
            continue
        
        # Reached destination
        if i == n-1 and j == n-1:
            return curr_time
        
        # Explore neighbors
        for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
            ni, nj = i + di, j + dj
            
            if 0 <= ni < n and 0 <= nj < n:
                # Time needed = max(current_time, elevation_of_next_cell)
                new_time = max(curr_time, grid[ni][nj])
                
                if new_time < dist[ni][nj]:
                    dist[ni][nj] = new_time
                    heapq.heappush(pq, (new_time, ni, nj))
    
    return dist[n-1][n-1]


# SOLUTION 5: Binary Search + BFS (Alternative to DFS)
# Time: O(n²·log(max_elevation)), Space: O(n²)
def swimInWater_bfs(grid):
    """
    Binary search + BFS instead of DFS
    Good alternative if worried about recursion stack
    """
    from collections import deque
    
    n = len(grid)
    
    def canReach(time_limit):
        if grid[0][0] > time_limit:
            return False
        
        visited = [[False] * n for _ in range(n)]
        queue = deque([(0, 0)])
        visited[0][0] = True
        
        while queue:
            i, j = queue.popleft()
            
            if i == n-1 and j == n-1:
                return True
            
            for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
                ni, nj = i + di, j + dj
                
                if (0 <= ni < n and 0 <= nj < n and 
                    not visited[ni][nj] and 
                    grid[ni][nj] <= time_limit):
                    
                    visited[ni][nj] = True
                    queue.append((ni, nj))
        
        return False
    
    left = max(grid[0][0], grid[n-1][n-1])
    right = max(max(row) for row in grid)
    
    while left < right:
        mid = (left + right) // 2
        
        if canReach(mid):
            right = mid
        else:
            left = mid + 1
    
    return left


# Test cases
def test_solutions():
    # Test case 1
    grid1 = [
        [0, 2],
        [1, 3]
    ]
    
    # Test case 2
    grid2 = [
        [0, 1, 2, 3, 4],
        [24, 23, 22, 21, 5],
        [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20],
        [10, 9, 8, 7, 6]
    ]
    
    # Test case 3
    grid3 = [
        [3, 2],
        [0, 1]
    ]
    
    test_cases = [grid1, grid2, grid3]
    expected = [3, 16, 3]
    
    print("Testing all solutions:")
    for i, grid in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("Grid:")
        for row in grid:
            print(row)
        
        result1 = swimInWater(grid)
        result2 = swimInWater_dijkstra(grid)
        result3 = swimInWater_unionfind(grid)
        result4 = swimInWater_dijkstra_time(grid)
        result5 = swimInWater_bfs(grid)
        
        print(f"Binary Search + DFS:     {result1}")
        print(f"Dijkstra (max elevation): {result2}")
        print(f"Union-Find:              {result3}")
        print(f"Dijkstra (time):         {result4}")
        print(f"Binary Search + BFS:     {result5}")
        print(f"Expected:                {expected[i]}")
        print(f"All correct: {all(r == expected[i] for r in [result1, result2, result3, result4, result5])}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - "Find minimum time t such that there's a path from (0,0) to (n-1,n-1)"
   - "At time t, can only move through cells with elevation ≤ t"
   - "This is finding the path that minimizes the maximum elevation"
   - "Classic minimax path problem"

2. APPROACH ANALYSIS:
   - Binary Search + DFS: "Search on answer, verify with path-finding"
   - Dijkstra: "Modified shortest path - minimize maximum instead of sum"
   - Union-Find: "Process cells by elevation, connect when possible"

3. START WITH BINARY SEARCH + DFS (MOST INTUITIVE):
   - "Binary search on the answer (time/water level)"
   - "For each candidate time, check if path exists using DFS/BFS"
   - "Search space: [max(start,end), max_elevation_in_grid]"
   - Time: O(n²·log(max_elevation)), Space: O(n²)

4. DIJKSTRA'S ALGORITHM (MOST OPTIMAL):
   - "This is shortest path where edge weight = elevation"
   - "But we want to minimize maximum elevation, not sum"
   - "Use priority queue with (max_elevation_so_far, row, col)"
   - Time: O(n²·log(n²)), Space: O(n²)

5. KEY INSIGHTS:
   - "This is NOT standard shortest path - we minimize the maximum, not the sum"
   - "Binary search works because: if time t works, then t+1 also works (monotonic)"
   - "Dijkstra variation: track maximum elevation instead of total distance"

6. IMPLEMENTATION DETAILS:
   - Binary search bounds: [max(grid[0][0], grid[n-1][n-1]), max(all elevations)]
   - DFS/BFS: only move to cells with elevation ≤ current_time_limit
   - Dijkstra: priority queue on maximum elevation seen so far

7. COMPLEXITY COMPARISON:
   - Binary Search + DFS: O(n²·log(max_elevation))
   - Dijkstra: O(n²·log(n²)) - generally better for large elevation ranges
   - Union-Find: O(n²·log(n²)) - elegant but more complex

8. FOLLOW-UP QUESTIONS:
   - "Why not regular BFS?" → Doesn't handle varying elevations optimally
   - "Which approach is better?" → Dijkstra for most cases, binary search more intuitive
   - "What if elevations are very large?" → Dijkstra becomes clearly better
   - "How to handle floating point elevations?" → Same approaches work

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem: "Find minimum time for path from top-left to bottom-right"
2. Recognize: "This is minimax path problem - minimize the maximum elevation"
3. Start with binary search approach: "Search on answer, verify with DFS"
4. Code binary search + DFS solution
5. Test with example: show how binary search narrows down answer
6. Discuss complexity and mention Dijkstra as optimization
7. Code Dijkstra if time permits

KEY INSIGHT TO COMMUNICATE:
"This is a minimax path problem where we want to minimize the maximum elevation along the path, not the sum of elevations. Binary search on the answer is intuitive, but Dijkstra's algorithm adapted for minimax is more elegant."

INTERVIEW STRATEGY:
- **Start with Binary Search**: More intuitive to explain and understand
- **Upgrade to Dijkstra**: Shows advanced algorithm knowledge
- **Explain the connection**: Both solve the same minimax path problem

COMMON MISTAKES TO AVOID:
- Using regular shortest path (summing elevations instead of taking maximum)
- Wrong binary search bounds
- Forgetting that we need path from (0,0) to (n-1,n-1)
- Not handling the constraint that starting cell must be reachable at time t

ADVANCED OPTIMIZATIONS:
- "Can terminate Dijkstra early when we reach destination"
- "Union-Find approach processes cells in elevation order"
- "A* algorithm could work with appropriate heuristic"
"""
