"""
LeetCode 947: Most Stones Removed with Same Row or Column

Problem: On a 2D plane, we place n stones at some integer coordinate points. Each 
coordinate point may have at most one stone.

A stone can be removed if it shares a row or column with another stone that has not been removed.

Given an array stones where stones[i] = [xi, yi] represents the location of the ith stone, 
return the maximum number of stones that can be removed.

Example 1:
Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
Output: 5
Explanation: One way to remove 5 stones is as follows:
1. Remove stone [2,2] because it shares a column with [2,1].
2. Remove stone [2,1] because it shares a row with [1,2].
3. Remove stone [1,2] because it shares a column with [0,1].
4. Remove stone [0,1] because it shares a row with [0,0].
5. Remove stone [1,0] because it shares a column with [0,0].
We cannot remove [0,0] because it does not share a row/column with another stone still on the plane.

Example 2:
Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
Output: 3
"""

# SOLUTION 1: Union-Find - Coordinate Based (Most Intuitive)
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.components = 0
    
    def find(self, x):
        """Find with path compression"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.components += 1
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            
            self.components -= 1
    
    def get_components(self):
        return self.components

def removeStones(stones):
    """
    Key insight: Stones in the same row or column are connected.
    We can remove all stones in a connected component except one.
    Answer = total_stones - number_of_connected_components
    
    Time: O(n²) - checking all pairs of stones
    Space: O(n) - for Union-Find structure
    """
    uf = UnionFind()
    
    # Union stones that share row or column
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            x1, y1 = stones[i]
            x2, y2 = stones[j]
            
            # If stones share row or column, union them
            if x1 == x2 or y1 == y2:
                uf.union(i, j)  # Union by stone indices
    
    # Each stone creates a component initially
    for i in range(len(stones)):
        uf.find(i)  # Ensure all stones are initialized
    
    return len(stones) - uf.get_components()


# SOLUTION 2: Union-Find - Row/Column Based (Most Elegant)
def removeStonesOptimal(stones):
    """
    More elegant approach: Union rows and columns directly.
    Use negative column indices to distinguish from row indices.
    
    Time: O(n * α(n)) ≈ O(n) - much better than O(n²)
    Space: O(n)
    """
    uf = UnionFind()
    
    for x, y in stones:
        # Union row x with column y
        # Use ~y (bitwise NOT) to distinguish columns from rows
        # This ensures no collision between row and column indices
        uf.union(x, ~y)
    
    return len(stones) - uf.get_components()


# SOLUTION 3: DFS Connected Components
def removeStonesDFS(stones):
    """
    Build graph and use DFS to count connected components.
    
    Time: O(n²) - for building adjacency list and DFS
    Space: O(n²) - for adjacency list in worst case
    """
    n = len(stones)
    graph = [[] for _ in range(n)]
    
    # Build adjacency list
    for i in range(n):
        for j in range(i + 1, n):
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                graph[i].append(j)
                graph[j].append(i)
    
    visited = [False] * n
    components = 0
    
    def dfs(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)
    
    # Count connected components
    for i in range(n):
        if not visited[i]:
            dfs(i)
            components += 1
    
    return n - components


# SOLUTION 4: Union-Find with HashMap (Alternative implementation)
def removeStonesHashMap(stones):
    """
    Union-Find using row and column mapping with offset.
    
    Time: O(n * α(n))
    Space: O(n)
    """
    parent = {}
    
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            parent[root_x] = root_y
    
    for x, y in stones:
        # Union row x with column (y + 10001) to avoid collision
        # Since coordinates are at most 10^4, adding 10001 ensures separation
        union(x, y + 10001)
    
    # Count unique components that have stones
    return len(stones) - len({find(x) for x, y in stones})


# SOLUTION 5: BFS Connected Components
def removeStonesBFS(stones):
    """
    BFS approach to count connected components.
    
    Time: O(n²)
    Space: O(n²)
    """
    from collections import deque
    
    n = len(stones)
    graph = [[] for _ in range(n)]
    
    # Build adjacency list
    for i in range(n):
        for j in range(i + 1, n):
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                graph[i].append(j)
                graph[j].append(i)
    
    visited = [False] * n
    components = 0
    
    for i in range(n):
        if not visited[i]:
            # BFS to mark all nodes in this component
            queue = deque([i])
            visited[i] = True
            
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            components += 1
    
    return n - components


# Test cases
def test_solutions():
    test_cases = [
        ([[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]], 5),
        ([[0,0],[0,2],[1,1],[2,0],[2,2]], 3),
        ([[0,0]], 0),
        ([[0,1],[1,0]], 0),  # Two separate stones
        ([[0,0],[0,1],[1,0]], 2),  # All connected
    ]
    
    solutions = [
        ("Union-Find (Coordinate)", removeStones),
        ("Union-Find (Optimal)", removeStonesOptimal),
        ("DFS", removeStonesDFS),
        ("Union-Find (HashMap)", removeStonesHashMap),
        ("BFS", removeStonesBFS)
    ]
    
    for i, (stones, expected) in enumerate(test_cases):
        print(f"Test Case {i+1}: {stones}")
        print(f"Expected: {expected}")
        
        for name, solution in solutions:
            result = solution(stones)
            status = "✓" if result == expected else "✗"
            print(f"{name}: {result} {status}")
        print("-" * 60)

# Visualization helper
def visualize_example():
    """
    Visualize the first example to understand the problem better.
    """
    stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
    print("Stones visualization:")
    print("  0 1 2")
    for row in range(3):
        line = f"{row} "
        for col in range(3):
            if [row, col] in stones:
                line += "● "
            else:
                line += ". "
        print(line)
    
    print("\nConnected components:")
    print("All stones are connected through shared rows/columns")
    print("Component 1: All 6 stones form one connected component")
    print("Can remove 5 stones, must leave 1 in each component")
    print("Answer: 6 - 1 = 5")

if __name__ == "__main__":
    visualize_example()
    print("\n" + "="*60 + "\n")
    test_solutions()


"""
ALGORITHM EXPLANATION:

KEY INSIGHT: 
- Stones that share a row OR column are "connected"
- In each connected component, we can remove all stones except one
- Answer = Total stones - Number of connected components

WHY THIS WORKS:
- If stones share row/column, one can be removed using the other
- This creates a connected component of removable stones
- We must leave exactly one stone per component (can't remove the last one)

SOLUTION COMPARISON:

1. Union-Find (Coordinate): O(n²) time, intuitive but not optimal
2. Union-Find (Row/Column): O(n) time, most elegant and optimal
3. DFS/BFS: O(n²) time, clear but less efficient

INTERVIEW STRATEGY:
1. Recognize this as connected components problem
2. Explain the key insight about removability
3. Start with coordinate-based Union-Find for clarity
4. Optimize to row/column Union-Find if time permits
5. Discuss why answer = stones - components

EDGE CASES:
- Single stone: Cannot be removed (0 removals)
- All stones isolated: Each is its own component (0 removals)
- All stones connected: One big component (n-1 removals)

FOLLOW-UP QUESTIONS:
- "How to find actual sequence of removals?" → DFS/BFS from leaves
- "What if we can remove stones sharing diagonals too?" → Modify connection logic
- "Memory optimization for large grids?" → Coordinate compression
"""
