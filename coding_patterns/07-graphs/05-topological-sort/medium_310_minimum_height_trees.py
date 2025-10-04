"""
LeetCode 310: Minimum Height Trees

Problem:
A tree is an undirected graph where any two vertices are connected by exactly one path.
Given n nodes labeled 0 to n-1 and edges, find all root nodes that minimize the tree height.

Key Insight: The roots of minimum height trees are the "center(s)" of the graph.
A tree has at most 2 centers (if path has even nodes, both middle nodes are centers).

Constraints:
- 1 <= n <= 2 * 10^4
- edges.length == n - 1
"""

# Solution 1: Topological Sort (Peeling Leaves) - OPTIMAL & BEST FOR INTERVIEWS
# Time: O(n), Space: O(n)
from collections import deque, defaultdict

class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Key insight: Remove leaves layer by layer until 1 or 2 nodes remain.
        These are the center(s) of the tree - the MHT roots.
        
        Why this works: Centers are equidistant from all leaves.
        """
        # Edge case: single node or two nodes
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        # Find all leaf nodes (degree = 1)
        leaves = deque([i for i in range(n) if len(graph[i]) == 1])
        
        # Peel off leaves layer by layer
        remaining = n
        while remaining > 2:
            leaves_count = len(leaves)
            remaining -= leaves_count
            
            # Process current layer of leaves
            for _ in range(leaves_count):
                leaf = leaves.popleft()
                
                # Remove leaf from its neighbor
                neighbor = graph[leaf][0]  # Leaf has only one neighbor
                graph[neighbor].remove(leaf)
                
                # If neighbor becomes a leaf, add to queue
                if len(graph[neighbor]) == 1:
                    leaves.append(neighbor)
        
        # Remaining nodes are the centers
        return list(leaves)


# Solution 2: Topological Sort with Degree Array (More Efficient)
# Time: O(n), Space: O(n)
class Solution2:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Same algorithm but using degree array instead of modifying graph.
        Slightly more efficient in practice.
        """
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list and degree array
        graph = defaultdict(set)  # Using set for O(1) removal
        degree = [0] * n
        
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
            degree[u] += 1
            degree[v] += 1
        
        # Initialize with all leaves
        leaves = deque([i for i in range(n) if degree[i] == 1])
        
        remaining = n
        while remaining > 2:
            leaves_count = len(leaves)
            remaining -= leaves_count
            
            for _ in range(leaves_count):
                leaf = leaves.popleft()
                
                # Reduce degree of neighbors
                for neighbor in graph[leaf]:
                    degree[neighbor] -= 1
                    if degree[neighbor] == 1:
                        leaves.append(neighbor)
        
        return list(leaves)


# Solution 3: Two BFS (Find Longest Path, Then Find Center)
# Time: O(n), Space: O(n)
class Solution3:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Alternative approach:
        1. Find one end of the longest path (BFS from any node)
        2. Find the other end of longest path (BFS from first end)
        3. Return middle node(s) of this path
        
        Less intuitive but shows deep understanding of tree properties.
        """
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def bfs_farthest(start):
            """Returns (farthest_node, parent_map)."""
            visited = {start}
            queue = deque([start])
            parent = {start: -1}
            farthest = start
            
            while queue:
                node = queue.popleft()
                farthest = node
                
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parent[neighbor] = node
                        queue.append(neighbor)
            
            return farthest, parent
        
        # Find one end of longest path
        end1, _ = bfs_farthest(0)
        
        # Find other end of longest path
        end2, parent = bfs_farthest(end1)
        
        # Reconstruct path from end1 to end2
        path = []
        current = end2
        while current != -1:
            path.append(current)
            current = parent[current]
        
        # Return middle node(s)
        path_len = len(path)
        if path_len % 2 == 1:
            return [path[path_len // 2]]
        else:
            mid = path_len // 2
            return [path[mid - 1], path[mid]]


# Solution 4: Brute Force (For Understanding Only)
# Time: O(n^2), Space: O(n)
class Solution4:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Brute force: Try each node as root, compute height.
        This is TOO SLOW but good for understanding the problem.
        DO NOT code this in interview unless asked.
        """
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def get_height(root):
            """Get height of tree rooted at root using BFS."""
            visited = {root}
            queue = deque([root])
            height = -1
            
            while queue:
                height += 1
                for _ in range(len(queue)):
                    node = queue.popleft()
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
            
            return height
        
        # Try each node as root
        min_height = float('inf')
        result = []
        
        for root in range(n):
            height = get_height(root)
            if height < min_height:
                min_height = height
                result = [root]
            elif height == min_height:
                result.append(root)
        
        return result


# Solution 5: Optimized Topological Sort (One Pass)
# Time: O(n), Space: O(n)
class Solution5:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Most optimized version with early termination.
        """
        if n <= 2:
            return list(range(n))
        
        graph = [set() for _ in range(n)]
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        
        # Current layer of leaves
        leaves = [i for i in range(n) if len(graph[i]) == 1]
        
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            new_leaves = []
            
            for leaf in leaves:
                # Get the only neighbor
                neighbor = graph[leaf].pop()
                graph[neighbor].remove(leaf)
                
                if len(graph[neighbor]) == 1:
                    new_leaves.append(neighbor)
            
            leaves = new_leaves
        
        return leaves


# Test cases
def test():
    sol = Solution()
    sol2 = Solution2()
    sol3 = Solution3()
    
    # Test case 1: Linear tree
    n = 4
    edges = [[1,0],[1,2],[1,3]]
    print(f"Test 1 (Sol1): {sol.findMinHeightTrees(n, edges)}")  # [1]
    print(f"Test 1 (Sol2): {sol2.findMinHeightTrees(n, edges)}")  # [1]
    print(f"Test 1 (Sol3): {sol3.findMinHeightTrees(n, edges)}")  # [1]
    
    # Test case 2: Two centers
    n = 6
    edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
    print(f"Test 2 (Sol1): {sorted(sol.findMinHeightTrees(n, edges))}")  # [3, 4]
    print(f"Test 2 (Sol2): {sorted(sol2.findMinHeightTrees(n, edges))}")  # [3, 4]
    print(f"Test 2 (Sol3): {sorted(sol3.findMinHeightTrees(n, edges))}")  # [3, 4]
    
    # Test case 3: Single node
    n = 1
    edges = []
    print(f"Test 3 (Sol1): {sol.findMinHeightTrees(n, edges)}")  # [0]
    
    # Test case 4: Two nodes
    n = 2
    edges = [[0,1]]
    print(f"Test 4 (Sol1): {sorted(sol.findMinHeightTrees(n, edges))}")  # [0, 1]
    
    # Test case 5: Chain
    n = 6
    edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]
    print(f"Test 5 (Sol1): {sorted(sol.findMinHeightTrees(n, edges))}")  # [2, 3]
    print(f"Test 5 (Sol2): {sorted(sol2.findMinHeightTrees(n, edges))}")  # [2, 3]
    print(f"Test 5 (Sol3): {sorted(sol3.findMinHeightTrees(n, edges))}")  # [2, 3]
    
    # Visualize test case 2:
    print("\nVisualization of Test 2:")
    print("    0")
    print("    |")
    print("1---3---4---5")
    print("    |")
    print("    2")
    print("Centers: 3 and 4 (both give height 2)")

if __name__ == "__main__":
    test()
