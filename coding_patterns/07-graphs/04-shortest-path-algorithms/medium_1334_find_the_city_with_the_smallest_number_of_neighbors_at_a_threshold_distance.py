"""
LeetCode 1334: Find the City With the Smallest Number of Neighbors at a Threshold Distance

Problem:
There are n cities numbered from 0 to n-1. Given edges where edges[i] = [from_i, to_i, weight_i]
represents a bidirectional weighted edge. Find the city with the smallest number of cities that 
are reachable through some path and whose distance is at most distanceThreshold. If there are 
multiple such cities, return the city with the greatest number.

Constraints:
- 2 <= n <= 100
- 1 <= edges.length <= n * (n - 1) / 2
- 0 <= distanceThreshold <= 10^4
"""

# Solution 1: Floyd-Warshall Algorithm (Most Common in Interviews)
# Time: O(n^3), Space: O(n^2)
class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        """
        Floyd-Warshall approach - finds shortest paths between all pairs of cities.
        This is the most intuitive solution for this problem.
        """
        # Initialize distance matrix with infinity
        INF = float('inf')
        dist = [[INF] * n for _ in range(n)]
        
        # Distance from city to itself is 0
        for i in range(n):
            dist[i][i] = 0
        
        # Fill in direct edges
        for u, v, w in edges:
            dist[u][v] = w
            dist[v][u] = w
        
        # Floyd-Warshall: try each intermediate city k
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        # Count reachable cities for each city
        min_count = n
        result = 0
        
        for i in range(n):
            count = 0
            for j in range(n):
                if i != j and dist[i][j] <= distanceThreshold:
                    count += 1
            
            # Update result if we found fewer reachable cities
            # Or same count but larger city number
            if count <= min_count:
                min_count = count
                result = i
        
        return result


# Solution 2: Dijkstra's Algorithm from Each City
# Time: O(n^2 * log(n) + n*m) where m = edges, Space: O(n + m)
import heapq
from collections import defaultdict

class Solution2:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        """
        Run Dijkstra from each city to find shortest paths.
        More efficient when graph is sparse (fewer edges).
        """
        # Build adjacency list
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        
        def dijkstra(start):
            """Returns count of reachable cities from start within threshold."""
            dist = [float('inf')] * n
            dist[start] = 0
            heap = [(0, start)]  # (distance, city)
            
            while heap:
                d, u = heapq.heappop(heap)
                
                if d > dist[u]:
                    continue
                
                for v, w in graph[u]:
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        heapq.heappush(heap, (dist[v], v))
            
            # Count cities within threshold (excluding start city)
            return sum(1 for i in range(n) if i != start and dist[i] <= distanceThreshold)
        
        min_count = n
        result = 0
        
        for city in range(n):
            count = dijkstra(city)
            if count <= min_count:
                min_count = count
                result = city
        
        return result


# Solution 3: Optimized Floyd-Warshall with Early Exit
# Time: O(n^3), Space: O(n^2)
class Solution3:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        """
        Floyd-Warshall with optimizations:
        - Use distanceThreshold + 1 as infinity for better cache performance
        - Count during distance calculation
        """
        INF = distanceThreshold + 1
        dist = [[INF] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
        
        for u, v, w in edges:
            dist[u][v] = w
            dist[v][u] = w
        
        # Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        # Find result
        result = 0
        min_reachable = n
        
        for i in range(n):
            reachable = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if reachable <= min_reachable:
                min_reachable = reachable
                result = i
        
        return result


# Test cases
def test():
    sol = Solution()
    
    # Test case 1
    n = 4
    edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]
    distanceThreshold = 4
    print(f"Test 1: {sol.findTheCity(n, edges, distanceThreshold)}")  # Expected: 3
    
    # Test case 2
    n = 5
    edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]]
    distanceThreshold = 2
    print(f"Test 2: {sol.findTheCity(n, edges, distanceThreshold)}")  # Expected: 0
    
    # Test case 3
    n = 6
    edges = [[0,1,10],[0,2,1],[2,3,1],[1,3,1],[1,4,1],[4,5,10]]
    distanceThreshold = 20
    print(f"Test 3: {sol.findTheCity(n, edges, distanceThreshold)}")  # Expected: 5

if __name__ == "__main__":
    test()
