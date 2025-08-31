"""
LeetCode 547: Number of Provinces

Problem: There are n cities. Some of them are connected, while some are not. 
If city a is connected directly with city b, and city b is connected directly 
with city c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other 
cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the 
ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.

Example 1:
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2

Example 2:
Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
"""

# SOLUTION 1: DFS Approach - Most Intuitive
def findCircleNum(isConnected):
    """
    Use DFS to find connected components (provinces).
    
    Time: O(n²) - we might visit each cell in the matrix
    Space: O(n) - for the visited array and recursion stack
    """
    n = len(isConnected)
    visited = [False] * n
    provinces = 0
    
    def dfs(city):
        """Mark all cities connected to the current city as visited"""
        visited[city] = True
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)
    
    # Start DFS from each unvisited city
    for city in range(n):
        if not visited[city]:
            dfs(city)  # Explore the entire province
            provinces += 1
    
    return provinces


# SOLUTION 2: BFS Approach - Alternative traversal
from collections import deque

def findCircleNumBFS(isConnected):
    """
    Use BFS to find connected components.
    
    Time: O(n²) - we might visit each cell in the matrix
    Space: O(n) - for the visited array and queue
    """
    n = len(isConnected)
    visited = [False] * n
    provinces = 0
    
    def bfs(start_city):
        """Use BFS to mark all cities in the same province"""
        queue = deque([start_city])
        visited[start_city] = True
        
        while queue:
            city = queue.popleft()
            for neighbor in range(n):
                if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
    
    # Start BFS from each unvisited city
    for city in range(n):
        if not visited[city]:
            bfs(city)
            provinces += 1
    
    return provinces


# SOLUTION 3: Union-Find (Disjoint Set Union) - Most Elegant
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # Each city is its own parent initially
        self.rank = [0] * n           # Rank for union by rank optimization
        self.components = n           # Initially n separate components
    
    def find(self, x):
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x != root_y:
            # Union by rank: attach smaller tree under larger tree
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

def findCircleNumUnionFind(isConnected):
    """
    Use Union-Find to count connected components.
    
    Time: O(n² * α(n)) where α is inverse Ackermann (practically O(n²))
    Space: O(n) - for the Union-Find data structure
    """
    n = len(isConnected)
    uf = UnionFind(n)
    
    # Union all directly connected cities
    for i in range(n):
        for j in range(i + 1, n):  # Only check upper triangle (symmetric matrix)
            if isConnected[i][j] == 1:
                uf.union(i, j)
    
    return uf.get_components()


# SOLUTION 4: Iterative DFS with Stack - Avoid recursion limits
def findCircleNumIterative(isConnected):
    """
    Iterative DFS using explicit stack to avoid recursion depth issues.
    
    Time: O(n²)
    Space: O(n)
    """
    n = len(isConnected)
    visited = [False] * n
    provinces = 0
    
    for city in range(n):
        if not visited[city]:
            # Use stack for iterative DFS
            stack = [city]
            
            while stack:
                current_city = stack.pop()
                if not visited[current_city]:
                    visited[current_city] = True
                    
                    # Add all unvisited neighbors to stack
                    for neighbor in range(n):
                        if (isConnected[current_city][neighbor] == 1 and 
                            not visited[neighbor]):
                            stack.append(neighbor)
            
            provinces += 1
    
    return provinces


# Test cases
def test_solutions():
    test_cases = [
        ([[1,1,0],[1,1,0],[0,0,1]], 2),
        ([[1,0,0],[0,1,0],[0,0,1]], 3),
        ([[1,0,0,1],[0,1,1,0],[0,1,1,1],[1,0,1,1]], 1),
        ([[1]], 1),
        ([[1,1],[1,1]], 1)
    ]
    
    solutions = [
        ("DFS Recursive", findCircleNum),
        ("BFS", findCircleNumBFS), 
        ("Union-Find", findCircleNumUnionFind),
        ("DFS Iterative", findCircleNumIterative)
    ]
    
    for i, (isConnected, expected) in enumerate(test_cases):
        print(f"Test Case {i+1}: {isConnected}")
        print(f"Expected: {expected}")
        
        for name, solution in solutions:
            result = solution(isConnected)
            print(f"{name}: {result} {'✓' if result == expected else '✗'}")
        print("-" * 60)

# Run tests
if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. PROBLEM UNDERSTANDING:
   - This is a classic "connected components" problem
   - The matrix represents an undirected graph (symmetric)
   - Each province is a connected component in the graph

2. APPROACH COMPARISON:
   
   DFS/BFS Approach:
   - Most intuitive and commonly expected
   - Time: O(n²), Space: O(n)
   - Easy to implement and explain
   
   Union-Find Approach:
   - More advanced, shows strong DS&A knowledge
   - Efficient for dynamic connectivity queries
   - Time: O(n² * α(n)) ≈ O(n²), Space: O(n)
   - Great for follow-up questions about dynamic connections

3. KEY INSIGHTS:
   - Matrix is symmetric (isConnected[i][j] == isConnected[j][i])
   - Can optimize by only checking upper triangle in Union-Find
   - Each unvisited city starts a new DFS/BFS = new province

4. EDGE CASES:
   - Single city: [[1]] → 1 province
   - No connections: [[1,0],[0,1]] → 2 provinces  
   - All connected: [[1,1],[1,1]] → 1 province

5. FOLLOW-UP QUESTIONS:
   - "What if connections could be added/removed dynamically?" → Union-Find shines
   - "Find the largest province size?" → Track component sizes
   - "List all cities in each province?" → Modify to collect cities
   - "What if the graph was represented as adjacency list?" → Adapt accordingly

6. INTERVIEW TIPS:
   - Start with DFS solution (most expected)
   - Mention other approaches to show breadth of knowledge
   - Walk through example step by step
   - Discuss time/space tradeoffs
   - Be ready to implement any of the three approaches
"""
