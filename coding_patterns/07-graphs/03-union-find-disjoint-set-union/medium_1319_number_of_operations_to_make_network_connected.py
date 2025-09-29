"""
LeetCode 1319: Number of Operations to Make Network Connected
Medium

There are n computers numbered from 0 to n-1 connected by ethernet cables 
connections forming a network where connections[i] = [a, b] represents a 
connection between computers a and b.

Any computer can reach any other computer directly or indirectly through 
the network.

Given an initial computer network connections, you can extract certain 
cables between two directly connected computers and place them between any 
pair of disconnected computers to make them directly connected.

Return the minimum number of times you need to do this in order to make all 
the computers connected. If it's not possible, return -1.

Example 1:
Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
Explanation: Remove cable between 0 and 1, use it to connect 2 and 3.

Example 2:
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2

Example 3:
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
Explanation: There are not enough cables.
"""

from typing import List
from collections import deque, defaultdict


class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Approach 1: Union-Find (Disjoint Set Union)
        Time: O(n + m * α(n)) ≈ O(n + m), Space: O(n)
        where m = len(connections), α is inverse Ackermann function
        
        Key Insight:
        - To connect k disconnected components, we need k-1 cables
        - Extra cables = total cables - cables needed for current structure
        - If extra_cables >= k-1, we can connect all components
        """
        # Early termination: need at least n-1 cables to connect n computers
        if len(connections) < n - 1:
            return -1
        
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False  # Already connected (redundant cable)
            
            # Union by rank
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1
            return True
        
        # Count redundant cables while building the union-find structure
        redundant_cables = 0
        for a, b in connections:
            if not union(a, b):
                redundant_cables += 1
        
        # Count number of connected components
        components = len(set(find(i) for i in range(n)))
        
        # Need (components - 1) cables to connect all components
        cables_needed = components - 1
        
        return cables_needed if redundant_cables >= cables_needed else -1


class Solution2:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Approach 2: DFS/BFS to find connected components
        Time: O(n + m), Space: O(n + m)
        
        Simpler to understand but slightly more space due to adjacency list
        """
        # Early termination
        if len(connections) < n - 1:
            return -1
        
        # Build adjacency list
        graph = defaultdict(list)
        for a, b in connections:
            graph[a].append(b)
            graph[b].append(a)
        
        visited = [False] * n
        
        def dfs(node):
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
        
        # Count connected components
        components = 0
        for i in range(n):
            if not visited[i]:
                dfs(i)
                components += 1
        
        # To connect k components, we need k-1 operations
        return components - 1


class Solution3:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Approach 3: BFS variant (iterative)
        Time: O(n + m), Space: O(n + m)
        
        Same logic as DFS but using BFS for traversal
        """
        if len(connections) < n - 1:
            return -1
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for a, b in connections:
            graph[a].append(b)
            graph[b].append(a)
        
        visited = [False] * n
        components = 0
        
        for start in range(n):
            if visited[start]:
                continue
            
            # BFS from unvisited node
            queue = deque([start])
            visited[start] = True
            components += 1
            
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
        
        return components - 1


class Solution4:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Approach 4: Union-Find with Cleaner Implementation
        Time: O(n + m * α(n)), Space: O(n)
        
        More compact version - good for quick implementation in interviews
        """
        if len(connections) < n - 1:
            return -1
        
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        # Build union-find structure
        for a, b in connections:
            parent[find(a)] = find(b)
        
        # Count unique roots (components)
        return sum(parent[i] == i for i in range(n)) - 1


# Test cases
def test_solutions():
    solutions = [
        ("Union-Find with Redundant Cable Tracking", Solution()),
        ("DFS Approach", Solution2()),
        ("BFS Approach", Solution3()),
        ("Compact Union-Find", Solution4())
    ]
    
    test_cases = [
        (4, [[0,1],[0,2],[1,2]], 1),
        (6, [[0,1],[0,2],[0,3],[1,2],[1,3]], 2),
        (6, [[0,1],[0,2],[0,3],[1,2]], -1),
        (5, [[0,1],[0,2],[3,4],[2,3]], 0),
        (1, [], 0),
        (2, [], -1),
        (100, [[0,1],[1,2]], -1),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        for n, connections, expected in test_cases:
            result = solution.makeConnected(n, connections)
            status = "✓" if result == expected else "✗"
            print(f"  {status} n={n}, connections={len(connections)} edges -> {result} (expected: {expected})")
        print()


if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW GUIDE AND TALKING POINTS:

1. **Problem Analysis** (First 2-3 minutes):
   - Key insight: To connect k disconnected groups, need k-1 connections
   - Minimum cables needed to connect n computers: n-1
   - If we have fewer than n-1 cables, impossible to connect all
   - Extra cables can be repurposed to connect disconnected components

2. **Approach Selection** (What to say):
   "I see two main approaches here:
   
   a) Union-Find: Track connected components efficiently, O(n + m*α(n)) ≈ O(n + m)
      - Best for this type of connectivity problem
      - Clean implementation
      
   b) DFS/BFS: Count connected components by traversal, O(n + m)
      - More intuitive for some
      - Easier to explain
   
   I'll implement Union-Find as it's optimal for disjoint set problems."

3. **Implementation Strategy** (Recommended order):
   Step 1: Early termination check (if connections < n-1, return -1)
   Step 2: Implement Union-Find with path compression
   Step 3: Count connected components
   Step 4: Return components - 1

4. **For Time-Constrained Interviews**:
   - Start with Solution 4 (compact Union-Find) - fastest to code
   - Explain the logic clearly as you write
   - Mention optimizations (path compression, union by rank) even if not implementing all

5. **Edge Cases to Discuss**:
   - n = 1 (already connected)
   - Empty connections list
   - Exactly n-1 connections (tree structure)
   - All computers already connected
   - Disconnected graph with insufficient cables

6. **Follow-up Questions You Might Get**:
   Q: "What if we want to minimize the number of cable movements?"
   A: Same answer - we still need components-1 operations minimum
   
   Q: "Can you optimize further?"
   A: Union-Find with path compression is already near-optimal O(α(n)) per operation
   
   Q: "What if connections can have weights/costs?"
   A: Then we'd need MST algorithms (Kruskal's/Prim's)

7. **Time Complexity Explanation**:
   - Union-Find: O(m * α(n)) for unions + O(n) for counting = O(n + m)
   - DFS/BFS: O(n + m) for traversal
   - α(n) is inverse Ackermann function, practically constant (≤ 4 for all practical n)

8. **Why This Problem is Great for Interviews**:
   - Tests graph connectivity understanding
   - Multiple valid approaches (can adapt based on what you remember)
   - Clear optimization path from brute force to optimal
   - Good for discussing trade-offs

9. **Red Flags to Avoid**:
   ✗ Trying to simulate actual cable movements
   ✗ Overthinking the problem (it's simpler than it looks)
   ✗ Not checking the early termination condition
   ✗ Forgetting that we need exactly components-1 operations

10. **Green Flags to Show**:
    ✓ Recognize it's a connected components problem immediately
    ✓ Explain the mathematical insight (k components → k-1 operations)
    ✓ Implement Union-Find correctly with path compression
    ✓ Consider edge cases upfront
"""
