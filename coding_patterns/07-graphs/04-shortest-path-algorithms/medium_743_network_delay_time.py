"""
LeetCode 743: Network Delay Time
Medium

You are given a network of n nodes, labeled from 1 to n. You are also given 
times, a list of travel times as directed edges times[i] = (ui, vi, wi), where 
ui is the source node, vi is the target node, and wi is the time it takes for 
a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes 
for all the n nodes to receive the signal. If it is impossible for all nodes 
to receive the signal, return -1.

Example 1:
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

Example 2:
Input: times = [[1,2,1]], n = 2, k = 1
Output: 1

Example 3:
Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
"""

from typing import List
import heapq
from collections import defaultdict, deque


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach 1: Dijkstra's Algorithm with Min-Heap
        Time: O(E log V), Space: O(V + E)
        
        RECOMMENDED FOR INTERVIEWS - This is the standard and optimal solution
        
        Why Dijkstra's?
        - Single-source shortest path problem
        - Non-negative edge weights
        - Need to find max of all shortest paths
        """
        # Build adjacency list: graph[u] = [(v, weight), ...]
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        
        # Min-heap: (time, node)
        # Priority queue to always process the node with minimum time first
        heap = [(0, k)]
        
        # Track minimum time to reach each node
        dist = {}
        
        while heap:
            time, node = heapq.heappop(heap)
            
            # If we've already processed this node, skip
            if node in dist:
                continue
            
            # Record the time to reach this node
            dist[node] = time
            
            # Explore neighbors
            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(heap, (time + weight, neighbor))
        
        # Check if all nodes are reachable
        if len(dist) != n:
            return -1
        
        # Return the maximum time (last node to receive signal)
        return max(dist.values())


class Solution2:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach 2: Bellman-Ford Algorithm
        Time: O(V * E), Space: O(V)
        
        Less efficient but handles negative weights (not needed here)
        Good to mention if asked about alternatives
        """
        # Initialize distances to infinity
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            for u, v, w in times:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        
        # Find maximum distance (excluding index 0)
        max_time = max(dist[1:])
        
        return max_time if max_time != float('inf') else -1


class Solution3:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach 3: SPFA (Shortest Path Faster Algorithm)
        Time: O(V * E) worst case, O(E) average, Space: O(V + E)
        
        Optimized Bellman-Ford using a queue
        Often faster in practice than standard Bellman-Ford
        """
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        
        # Initialize distances
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        
        # Queue for BFS-like relaxation
        queue = deque([k])
        in_queue = [False] * (n + 1)
        in_queue[k] = True
        
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
        
        max_time = max(dist[1:])
        return max_time if max_time != float('inf') else -1


class Solution4:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach 4: DFS with Memoization (Not Optimal)
        Time: O(V^V) in worst case, Space: O(V + E)
        
        NOT RECOMMENDED - included for completeness
        Shows understanding but not efficient for this problem
        """
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        
        # Store minimum time to reach each node
        min_time = {}
        
        def dfs(node, time):
            # If we've reached this node with a better time before, skip
            if node in min_time and min_time[node] <= time:
                return
            
            min_time[node] = time
            
            for neighbor, weight in graph[node]:
                dfs(neighbor, time + weight)
        
        dfs(k, 0)
        
        if len(min_time) != n:
            return -1
        
        return max(min_time.values())


class Solution5:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach 5: Floyd-Warshall (Overkill for this problem)
        Time: O(V^3), Space: O(V^2)
        
        Finds all-pairs shortest paths - more than we need
        Good to mention if asked "what if we need delays from all sources?"
        """
        # Initialize distance matrix
        INF = float('inf')
        dist = [[INF] * (n + 1) for _ in range(n + 1)]
        
        # Distance from node to itself is 0
        for i in range(n + 1):
            dist[i][i] = 0
        
        # Fill in given edges
        for u, v, w in times:
            dist[u][v] = w
        
        # Floyd-Warshall algorithm
        for mid in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    dist[i][j] = min(dist[i][j], dist[i][mid] + dist[mid][j])
        
        # Find max distance from source k
        max_time = max(dist[k][1:])
        
        return max_time if max_time != INF else -1


# Test cases
def test_solutions():
    solutions = [
        ("Dijkstra's Algorithm (Optimal)", Solution()),
        ("Bellman-Ford", Solution2()),
        ("SPFA", Solution3()),
        ("DFS with Memoization", Solution4()),
        ("Floyd-Warshall", Solution5())
    ]
    
    test_cases = [
        ([[2,1,1],[2,3,1],[3,4,1]], 4, 2, 2),
        ([[1,2,1]], 2, 1, 1),
        ([[1,2,1]], 2, 2, -1),
        ([[1,2,1],[2,3,2],[1,3,4]], 3, 1, 3),
        ([[1,2,1],[2,1,3]], 2, 1, 1),
        ([[1,2,1],[2,3,2],[1,3,1]], 3, 2, -1),
        ([[1,2,1]], 3, 1, -1),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        all_passed = True
        for times, n, k, expected in test_cases:
            result = solution.networkDelayTime(times, n, k)
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
            print(f"  {status} times={times}, n={n}, k={k} -> {result} (expected: {expected})")
        print(f"  {'All tests passed!' if all_passed else 'Some tests failed!'}\n")


if __name__ == "__main__":
    test_solutions()


"""
COMPREHENSIVE INTERVIEW GUIDE:

═══════════════════════════════════════════════════════════════════════════
PART 1: PROBLEM RECOGNITION (First 1-2 minutes)
═══════════════════════════════════════════════════════════════════════════

What to say immediately:
"This is a classic single-source shortest path problem. We need to find the 
shortest path from node k to all other nodes, then return the maximum of 
these shortest paths (since all nodes must receive the signal).

Key observations:
1. Directed weighted graph with non-negative weights
2. Single source (node k)
3. Need shortest paths to ALL nodes
4. Answer is max(shortest_paths) - the last node to receive signal

This is a textbook case for Dijkstra's algorithm."

═══════════════════════════════════════════════════════════════════════════
PART 2: ALGORITHM SELECTION
═══════════════════════════════════════════════════════════════════════════

BEST CHOICE: Dijkstra's Algorithm (Solution 1)
✓ Time: O(E log V) - optimal for this problem
✓ Space: O(V + E)
✓ Perfect for non-negative weights
✓ Most commonly expected in interviews

ALTERNATIVES (Good to mention):
- Bellman-Ford: O(V*E) - handles negative weights, slower
- SPFA: O(E) average - optimization of Bellman-Ford
- Floyd-Warshall: O(V³) - overkill, finds ALL-pairs shortest paths

═══════════════════════════════════════════════════════════════════════════
PART 3: IMPLEMENTATION STRATEGY (15-20 minutes)
═══════════════════════════════════════════════════════════════════════════

Step-by-step approach:

1. Build adjacency list (2 min)
   "I'll create a graph representation for efficient neighbor lookup"

2. Initialize min-heap and distance tracking (2 min)
   "Using a priority queue to always process the closest unvisited node"

3. Implement Dijkstra's main loop (8 min)
   "Process nodes by minimum distance, relaxing edges to neighbors"

4. Check reachability and return result (3 min)
   "If all n nodes reached, return max distance; otherwise -1"

═══════════════════════════════════════════════════════════════════════════
PART 4: KEY INSIGHTS TO VERBALIZE
═══════════════════════════════════════════════════════════════════════════

While coding, explain:

1. "I'm using a min-heap to ensure I always process the node with the 
   smallest current distance first - this is the greedy choice that makes 
   Dijkstra's work."

2. "Once a node is visited (added to dist dict), we've found its shortest 
   path and never need to update it again - this is the key optimization."

3. "The answer is the MAX of all shortest paths because we need to wait for 
   the LAST node to receive the signal."

4. "If we can't reach all n nodes, we return -1."

═══════════════════════════════════════════════════════════════════════════
PART 5: COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

Time Complexity: O(E log V)
- Each edge is processed once: O(E)
- Each heap operation (push/pop) is O(log V)
- Total: O(E log V)

Space Complexity: O(V + E)
- Adjacency list: O(E)
- Distance dictionary: O(V)
- Heap: O(V) in worst case
- Total: O(V + E)

═══════════════════════════════════════════════════════════════════════════
PART 6: EDGE CASES
═══════════════════════════════════════════════════════════════════════════

Must discuss:
✓ n = 1 (single node) - should return 0
✓ Disconnected graph - return -1
✓ Starting node k has no outgoing edges but n > 1 - return -1
✓ Self-loops (shouldn't affect answer)
✓ Multiple edges between same nodes - Dijkstra's handles naturally
✓ All nodes directly connected to k - return max(direct weights)

═══════════════════════════════════════════════════════════════════════════
PART 7: COMMON MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════

❌ Using BFS without considering weights (wrong for weighted graphs)
❌ Forgetting to check if all nodes are reachable
❌ Using wrong data structure (list instead of heap) → O(V²) complexity
❌ Not handling 1-indexed nodes properly
❌ Updating already-visited nodes (breaks Dijkstra's guarantee)
❌ Using DFS for shortest path (doesn't work reliably)

═══════════════════════════════════════════════════════════════════════════
PART 8: FOLLOW-UP QUESTIONS & ANSWERS
═══════════════════════════════════════════════════════════════════════════

Q: "What if edges have negative weights?"
A: "Dijkstra's doesn't work with negative weights. I'd use Bellman-Ford 
   O(VE) or if there are negative cycles, need to detect them first."

Q: "What if we need delay time from ALL nodes to all other nodes?"
A: "Then Floyd-Warshall would be appropriate - O(V³) but finds all-pairs 
   shortest paths. Or run Dijkstra's V times - O(VE log V)."

Q: "Can you optimize further?"
A: "With a Fibonacci heap, we could achieve O(E + V log V), but it's 
   complex to implement and not worth it for interviews. The current 
   solution is optimal for practical purposes."

Q: "How would you handle very large graphs?"
A: "For massive graphs, consider:
   - Bidirectional Dijkstra (meet in the middle)
   - A* search with heuristics
   - Graph preprocessing/compression
   - Distributed computing for parallel processing"

Q: "What if we want the actual paths, not just times?"
A: "Add a 'parent' dictionary during Dijkstra's to track predecessors,
   then reconstruct paths by backtracking from each node to source."

═══════════════════════════════════════════════════════════════════════════
PART 9: TALKING POINTS DURING CODING
═══════════════════════════════════════════════════════════════════════════

As you code, say things like:

"I'm using a dictionary for the adjacency list because it handles sparse
graphs efficiently..."

"The heap stores (time, node) tuples, with time first so Python's heapq
sorts by time automatically..."

"I check 'if node in dist' to skip already-processed nodes - once we've
found the shortest path to a node, it won't improve..."

"At the end, I check if len(dist) == n to ensure all nodes are reachable..."

═══════════════════════════════════════════════════════════════════════════
PART 10: TIME MANAGEMENT (45-minute interview)
═══════════════════════════════════════════════════════════════════════════

0-5 min:   Problem understanding, clarifying questions, identify it's Dijkstra's
5-10 min:  Explain approach, draw example on whiteboard/screen
10-30 min: Code implementation (Dijkstra's with heap)
30-35 min: Walk through example, trace execution
35-40 min: Discuss edge cases, test with examples
40-45 min: Complexity analysis, discuss optimizations/alternatives

═══════════════════════════════════════════════════════════════════════════
FINAL RECOMMENDATION
═══════════════════════════════════════════════════════════════════════════

ALWAYS implement Solution 1 (Dijkstra's with heap) in an interview.
It's the expected solution, optimal, and demonstrates solid graph knowledge.

Be prepared to discuss alternatives, but don't implement them unless
specifically asked.
"""
