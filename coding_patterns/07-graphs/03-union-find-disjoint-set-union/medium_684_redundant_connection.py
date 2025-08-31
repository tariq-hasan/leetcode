"""
LeetCode 684: Redundant Connection

Problem: In this problem, a tree is an undirected graph that is connected and has no cycles.
You are given a graph that started as a tree with n nodes labeled from 1 to n, with one 
additional edge added. The added edge has two vertices chosen from 1 to n, and was not an 
edge that already existed. The graph is represented as an array edges of length n where 
edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. 
If there are multiple answers, return the answer that occurs last in the input.

Example 1:
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
Explanation: The given undirected graph will be like this:
  1
 / \
2---3

Example 2:
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
"""

# SOLUTION 1: Union-Find (Optimal and Most Expected)
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Union by rank. Returns True if union was successful,
        False if x and y were already in the same component (cycle detected).
        """
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x == root_y:
            return False  # Already connected - this edge creates a cycle
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True

def findRedundantConnection(edges):
    """
    Use Union-Find to detect the first edge that creates a cycle.
    
    Time: O(n * α(n)) where α is inverse Ackermann (practically O(n))
    Space: O(n) - for the Union-Find data structure
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # +1 because nodes are 1-indexed
    
    for edge in edges:
        u, v = edge
        if not uf.union(u, v):
            # This edge connects two nodes that are already connected
            # = creates a cycle, so this is the redundant edge
            return edge
    
    # Should never reach here given valid input
    return []


# SOLUTION 2: DFS Cycle Detection
def findRedundantConnectionDFS(edges):
    """
    Build graph incrementally and use DFS to detect cycles.
    
    Time: O(n²) - DFS for each edge can take O(n) time
    Space: O(n) - for the graph and recursion stack
    """
    graph = {}
    
    def has_cycle(source, target, visited):
        """Check if adding edge source->target creates a cycle"""
        if source == target:
            return True
        
        visited.add(source)
        
        for neighbor in graph.get(source, []):
            if neighbor not in visited:
                if has_cycle(neighbor, target, visited):
                    return True
        
        return False
    
    for u, v in edges:
        # Check if adding this edge creates a cycle
        if u in graph and v in graph and has_cycle(u, v, set()):
            return [u, v]
        
        # Add edge to graph
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        
        graph[u].append(v)
        graph[v].append(u)
    
    return []


# SOLUTION 3: Simple Union-Find without rank optimization
def findRedundantConnectionSimple(edges):
    """
    Simplified Union-Find without rank optimization.
    Good for interviews where you need to code quickly.
    
    Time: O(n²) in worst case without rank optimization
    Space: O(n)
    """
    parent = {}
    
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False  # Already connected
        parent[root_x] = root_y
        return True
    
    for edge in edges:
        u, v = edge
        if not union(u, v):
            return edge
    
    return []


# SOLUTION 4: DFS with Adjacency List (Alternative DFS implementation)
def findRedundantConnectionDFS2(edges):
    """
    Another DFS approach using adjacency list representation.
    
    Time: O(n²)
    Space: O(n)
    """
    graph = [[] for _ in range(len(edges) + 1)]
    
    def dfs(source, target, parent):
        """DFS to check if path exists from source to target"""
        if source == target:
            return True
        
        for neighbor in graph[source]:
            if neighbor != parent and dfs(neighbor, target, source):
                return True
        
        return False
    
    for u, v in edges:
        # If path already exists between u and v, this edge is redundant
        if graph[u] and graph[v] and dfs(u, v, -1):
            return [u, v]
        
        # Add edge to graph
        graph[u].append(v)
        graph[v].append(u)
    
    return []


# Test cases
def test_solutions():
    test_cases = [
        ([[1,2],[1,3],[2,3]], [2,3]),
        ([[1,2],[2,3],[3,4],[1,4],[1,5]], [1,4]),
        ([[1,2],[2,3],[3,1]], [3,1]),
        ([[2,3],[5,2],[1,5],[4,3],[1,4]], [1,4]),
        ([[1,2]], [])  # Edge case: no cycle possible
    ]
    
    solutions = [
        ("Union-Find Optimized", findRedundantConnection),
        ("DFS Cycle Detection", findRedundantConnectionDFS),
        ("Union-Find Simple", findRedundantConnectionSimple),
        ("DFS Adjacency List", findRedundantConnectionDFS2)
    ]
    
    for i, (edges, expected) in enumerate(test_cases):
        print(f"Test Case {i+1}: {edges}")
        print(f"Expected: {expected}")
        
        for name, solution in solutions:
            try:
                result = solution(edges)
                print(f"{name}: {result}")
            except:
                print(f"{name}: Error (likely due to no cycle case)")
        print("-" * 60)

# Run tests
if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. PROBLEM ANALYSIS:
   - We have a tree + 1 extra edge
   - Need to find which edge creates the cycle
   - Return the last edge that appears in input that creates a cycle

2. WHY UNION-FIND IS OPTIMAL:
   - Perfect for detecting cycles in undirected graphs
   - Process edges in order, first edge that connects already-connected 
     components is the answer
   - Time: O(n * α(n)) ≈ O(n) with path compression and union by rank
   - Space: O(n)

3. ALGORITHM WALKTHROUGH (Union-Find):
   - Initialize each node as its own parent
   - For each edge [u,v]:
     * If find(u) == find(v): they're already connected → cycle found
     * Otherwise: union(u,v) to connect them
   - First edge that fails to union is the redundant connection

4. ALTERNATIVE APPROACHES:
   - DFS: Build graph incrementally, check for cycles before adding each edge
   - BFS: Similar to DFS but uses queue instead of recursion
   - Both have O(n²) time complexity in worst case

5. KEY INSIGHTS:
   - Process edges in the order given (important for "last occurring" requirement)
   - Union-Find naturally finds the first edge that creates a cycle
   - The graph is guaranteed to have exactly one cycle

6. EDGE CASES:
   - Minimum case: 3 nodes, 3 edges
   - Self-loops: won't occur based on problem constraints
   - Multiple cycles: won't occur (only 1 extra edge added to tree)

7. FOLLOW-UP VARIATIONS:
   - "Find all possible edges to remove?" → Need to identify the cycle
   - "What if we want the first occurring redundant edge?" → Same solution
   - "Directed graph version?" → Different problem (Leetcode 685)

8. INTERVIEW TIPS:
   - Start by explaining that this is cycle detection
   - Mention Union-Find is optimal for this type of problem
   - Code the Union-Find solution cleanly
   - Be ready to explain path compression and union by rank
   - Walk through example step by step showing parent array changes
"""
