"""
LeetCode 1514: Path with Maximum Probability
Medium

You are given an undirected weighted graph of n nodes (0-indexed), represented 
by an edge list where edges[i] = [a, b] is an undirected edge connecting the 
nodes a and b with a probability of success of traversing that edge 
succProb[i].

Given two nodes start and end, find the path with the maximum probability of 
success to go from start to end and return its success probability.

If there is no path from start to end, return 0. Your answer will be accepted 
if it differs from the correct answer by at most 1e-5.

Example 1:
Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], 
       start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end, one having probability 
0.2 and the other 0.5 * 0.5 = 0.25.

Example 2:
Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], 
       start = 0, end = 2
Output: 0.30000

Example 3:
Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
"""

from typing import List
import heapq
from collections import defaultdict, deque


class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start: int, end: int) -> float:
        """
        Approach 1: Modified Dijkstra's Algorithm (Max-Heap)
        Time: O(E log V), Space: O(V + E)
        
        ⭐ RECOMMENDED FOR INTERVIEWS ⭐
        
        Key Insight: This is Dijkstra's algorithm with modifications:
        1. Instead of minimizing distance, we MAXIMIZE probability
        2. Instead of addition, we use MULTIPLICATION (probabilities multiply)
        3. Use negative probabilities in heap to simulate max-heap
        4. Stop early when we reach the end node
        """
        # Build adjacency list for undirected graph
        graph = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            prob = succProb[i]
            graph[a].append((b, prob))
            graph[b].append((a, prob))
        
        # Max-heap using negative probabilities (Python has min-heap only)
        # Format: (-probability, node)
        heap = [(-1.0, start)]  # Start with probability 1.0
        
        # Track maximum probability to reach each node
        max_prob = {}
        
        while heap:
            neg_prob, node = heapq.heappop(heap)
            prob = -neg_prob
            
            # Early termination: found the end node
            if node == end:
                return prob
            
            # Skip if we've already processed this node with better probability
            if node in max_prob:
                continue
            
            max_prob[node] = prob
            
            # Explore neighbors
            for neighbor, edge_prob in graph[node]:
                if neighbor not in max_prob:
                    new_prob = prob * edge_prob
                    heapq.heappush(heap, (-new_prob, neighbor))
        
        # If end node not reachable
        return 0.0


class Solution2:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start: int, end: int) -> float:
        """
        Approach 2: Modified Bellman-Ford Algorithm
        Time: O(V * E), Space: O(V + E)
        
        Relaxation approach - good for understanding, less efficient
        """
        # Initialize probabilities
        prob = [0.0] * n
        prob[start] = 1.0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            updated = False
            for i, (a, b) in enumerate(edges):
                edge_prob = succProb[i]
                
                # Try to improve probability to b through a
                if prob[a] * edge_prob > prob[b]:
                    prob[b] = prob[a] * edge_prob
                    updated = True
                
                # Try to improve probability to a through b (undirected)
                if prob[b] * edge_prob > prob[a]:
                    prob[a] = prob[b] * edge_prob
                    updated = True
            
            # Early termination if no updates
            if not updated:
                break
        
        return prob[end]


class Solution3:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start: int, end: int) -> float:
        """
        Approach 3: SPFA (Shortest Path Faster Algorithm) - Modified for Max
        Time: O(V * E) worst case, O(E) average, Space: O(V + E)
        
        Optimized relaxation using queue - often faster in practice
        """
        graph = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            prob = succProb[i]
            graph[a].append((b, prob))
            graph[b].append((a, prob))
        
        # Initialize probabilities
        max_prob = [0.0] * n
        max_prob[start] = 1.0
        
        # Queue for nodes to process
        queue = deque([start])
        in_queue = [False] * n
        in_queue[start] = True
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, edge_prob in graph[node]:
                new_prob = max_prob[node] * edge_prob
                
                # If we found a better probability to neighbor
                if new_prob > max_prob[neighbor]:
                    max_prob[neighbor] = new_prob
                    
                    # Add to queue if not already there
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
        
        return max_prob[end]


class Solution4:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start: int, end: int) -> float:
        """
        Approach 4: Dijkstra's with Visited Array (Alternative Implementation)
        Time: O(E log V), Space: O(V + E)
        
        Uses boolean visited array instead of checking dictionary
        """
        graph = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            prob = succProb[i]
            graph[a].append((b, prob))
            graph[b].append((a, prob))
        
        # Max-heap: (-probability, node)
        heap = [(-1.0, start)]
        
        # Track best probability to each node
        best_prob = [0.0] * n
        best_prob[start] = 1.0
        
        visited = [False] * n
        
        while heap:
            neg_prob, node = heapq.heappop(heap)
            prob = -neg_prob
            
            if visited[node]:
                continue
            
            visited[node] = True
            
            # Early exit when reaching end
            if node == end:
                return prob
            
            for neighbor, edge_prob in graph[node]:
                if not visited[neighbor]:
                    new_prob = prob * edge_prob
                    if new_prob > best_prob[neighbor]:
                        best_prob[neighbor] = new_prob
                        heapq.heappush(heap, (-new_prob, neighbor))
        
        return 0.0


class Solution5:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start: int, end: int) -> float:
        """
        Approach 5: DFS with Memoization
        Time: Exponential worst case, Space: O(V + E)
        
        NOT RECOMMENDED - included for educational purposes
        Can work but inefficient for large graphs
        """
        graph = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            prob = succProb[i]
            graph[a].append((b, prob))
            graph[b].append((a, prob))
        
        # Memoization: max probability from node to end
        memo = {}
        
        def dfs(node, visited):
            if node == end:
                return 1.0
            
            if node in memo:
                return memo[node]
            
            max_prob = 0.0
            visited.add(node)
            
            for neighbor, edge_prob in graph[node]:
                if neighbor not in visited:
                    prob = edge_prob * dfs(neighbor, visited)
                    max_prob = max(max_prob, prob)
            
            visited.remove(node)
            memo[node] = max_prob
            return max_prob
        
        return dfs(start, set())


# Test cases
def test_solutions():
    solutions = [
        ("Dijkstra's with Max-Heap (Optimal)", Solution()),
        ("Bellman-Ford", Solution2()),
        ("SPFA", Solution3()),
        ("Dijkstra's with Visited Array", Solution4()),
        ("DFS with Memoization", Solution5())
    ]
    
    test_cases = [
        (3, [[0,1],[1,2],[0,2]], [0.5,0.5,0.2], 0, 2, 0.25),
        (3, [[0,1],[1,2],[0,2]], [0.5,0.5,0.3], 0, 2, 0.3),
        (3, [[0,1]], [0.5], 0, 2, 0.0),
        (5, [[0,1],[1,2],[0,2],[2,3],[3,4]], [0.5,0.5,0.2,0.5,0.5], 0, 4, 0.125),
        (3, [[0,1],[1,2],[0,2]], [0.9,0.9,0.8], 0, 2, 0.81),
        (1, [], [0.5], 0, 0, 1.0),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        all_passed = True
        for n, edges, succProb, start, end, expected in test_cases:
            result = solution.maxProbability(n, edges, succProb, start, end)
            # Use approximate comparison for floating point
            passed = abs(result - expected) < 1e-5
            status = "✓" if passed else "✗"
            if not passed:
                all_passed = False
            print(f"  {status} n={n}, edges={len(edges)}, start={start}, end={end} -> {result:.5f} (expected: {expected:.5f})")
        print(f"  {'All tests passed!' if all_passed else 'Some tests failed!'}\n")


if __name__ == "__main__":
    test_solutions()


"""
═══════════════════════════════════════════════════════════════════════════
COMPREHENSIVE INTERVIEW GUIDE
═══════════════════════════════════════════════════════════════════════════

PART 1: INSTANT RECOGNITION (First 30 seconds)
═══════════════════════════════════════════════════════════════════════════

"This is a modified shortest path problem - instead of finding the shortest 
distance, we're finding the path with MAXIMUM probability. It's essentially 
Dijkstra's algorithm with two key modifications:

1. We MAXIMIZE instead of minimize
2. We MULTIPLY probabilities instead of adding distances

Since probabilities are always positive (0 to 1), Dijkstra's guarantees still 
hold - once we process a node, we've found its maximum probability path."

═══════════════════════════════════════════════════════════════════════════
PART 2: KEY INSIGHTS TO VERBALIZE
═══════════════════════════════════════════════════════════════════════════

Critical points to mention:

1. **Why it's similar to Dijkstra's:**
   "Probabilities multiply along a path: P(A→B→C) = P(A→B) × P(B→C)
   This is analogous to distances adding in regular shortest path"

2. **Why we maximize:**
   "Higher probability = better path. We want the path with highest 
   probability of success"

3. **The heap trick:**
   "Python only has min-heap, so I use negative probabilities to simulate 
   a max-heap: heap stores (-probability, node)"

4. **Early termination:**
   "Once we pop the end node from the heap, we've found the optimal path 
   and can return immediately"

5. **Graph is undirected:**
   "Each edge goes both ways, so I add it to adjacency list for both nodes"

═══════════════════════════════════════════════════════════════════════════
PART 3: IMPLEMENTATION STRATEGY (Recommended: Solution 1)
═══════════════════════════════════════════════════════════════════════════

Step 1 (3 min): Build adjacency list
- "Building undirected graph - each edge connects both nodes"
- Use defaultdict(list) for clean code

Step 2 (2 min): Initialize heap and tracking
- "Start with probability 1.0 at source node"
- "Use dictionary to track visited nodes and their max probabilities"

Step 3 (10 min): Main Dijkstra's loop
- "Pop node with highest probability (most negative in min-heap)"
- "Early return when we reach end node - optimization!"
- "For each neighbor, calculate new probability via this path"
- "Only process if we haven't visited this node yet"

Step 4 (2 min): Return result
- "Return 0.0 if end node never reached (not in graph)"

═══════════════════════════════════════════════════════════════════════════
PART 4: COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

Time Complexity: O(E log V)
- Build graph: O(E)
- Each edge processed once: O(E)
- Each heap operation: O(log V)
- Total: O(E log V)

Space Complexity: O(V + E)
- Adjacency list: O(E)
- Heap: O(V) worst case
- Visited dictionary: O(V)
- Total: O(V + E)

"This is optimal for single-source paths with non-negative weights/probabilities"

═══════════════════════════════════════════════════════════════════════════
PART 5: EDGE CASES & TESTING
═══════════════════════════════════════════════════════════════════════════

Must discuss:
✓ start == end → return 1.0
✓ No path exists → return 0.0
✓ Direct edge vs. multi-hop path → pick higher probability
✓ Graph with single node → handle gracefully
✓ All probabilities are 1.0 → any path works
✓ Very small probabilities → numerical stability (generally OK with doubles)

Example walkthrough:
"For Example 1: edges [[0,1],[1,2],[0,2]], probs [0.5,0.5,0.2]
- Direct path 0→2: probability 0.2
- Path 0→1→2: probability 0.5 × 0.5 = 0.25
- Maximum is 0.25, so that's our answer"

═══════════════════════════════════════════════════════════════════════════
PART 6: COMMON MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════

❌ Using min instead of max (minimizing probability is wrong!)
❌ Adding probabilities instead of multiplying
❌ Using regular min-heap without negation
❌ Forgetting to handle undirected edges (must add both directions)
❌ Not checking if node already visited before processing
❌ Continuing after finding end node (waste of computation)
❌ Using BFS (doesn't work - need priority by probability)

═══════════════════════════════════════════════════════════════════════════
PART 7: COMPARISON WITH STANDARD DIJKSTRA'S
═══════════════════════════════════════════════════════════════════════════

Standard Dijkstra's          | This Problem
----------------------------|-----------------------------
Minimize distance           | Maximize probability
Add distances               | Multiply probabilities
Start with dist[s] = 0      | Start with prob[s] = 1.0
dist[s] + w < dist[v]       | prob[u] × p > prob[v]
Use min-heap directly       | Use negative values in heap
Initial: 0 (identity +)     | Initial: 1.0 (identity ×)

"The core algorithm structure is identical - only the operations change!"

═══════════════════════════════════════════════════════════════════════════
PART 8: FOLLOW-UP QUESTIONS & ANSWERS
═══════════════════════════════════════════════════════════════════════════

Q: "What if probabilities could be 0?"
A: "Still works - zero probability means that path is impossible, which 
   Dijkstra's handles naturally. We'd just never use those edges."

Q: "What if we need to find top K paths?"
A: "Modify to not mark nodes as visited immediately - continue finding 
   alternative paths. Use Yen's algorithm or modified Dijkstra's with 
   K-best tracking."

Q: "How would you handle very long paths where probabilities become tiny?"
A: "Could use log-probabilities: log(P1 × P2) = log(P1) + log(P2)
   This converts multiplication to addition and prevents underflow.
   Then maximize sum of logs instead of product of probabilities."

Q: "What if graph is directed?"
A: "Actually simpler - only add edges in one direction when building 
   adjacency list. The algorithm stays the same."

Q: "Can you prove this modification of Dijkstra's is correct?"
A: "Yes! The key property is monotonicity: 
   - Probabilities are in (0,1], multiplying them never increases value
   - Once we process a node with probability P, any future path to it will 
     have probability ≤ P (because we already picked the max)
   - This preserves Dijkstra's greedy choice correctness"

═══════════════════════════════════════════════════════════════════════════
PART 9: ALTERNATIVE APPROACHES (What to mention)
═══════════════════════════════════════════════════════════════════════════

"I could also solve this with:

1. Bellman-Ford variant: O(V×E) - less efficient but simpler logic
2. SPFA: O(E) average - queue-based relaxation, often fast in practice
3. DFS with memoization: Exponential worst case - not recommended

But Dijkstra's is optimal here: O(E log V) and most expected in interviews."

═══════════════════════════════════════════════════════════════════════════
PART 10: IMPLEMENTATION TIPS
═══════════════════════════════════════════════════════════════════════════

Clean code practices:

1. Use defaultdict(list) for graph - cleaner than checking key existence
2. Store (-prob, node) in heap - negative for max-heap behavior
3. Use dictionary for visited tracking - clean and Pythonic
4. Early return when end node found - important optimization
5. Return 0.0 explicitly if no path - clear intent

Naming conventions:
- Use 'prob' not 'weight' or 'dist' - makes code self-documenting
- Use 'max_prob' to emphasize we're maximizing
- Clear variable names: 'edge_prob', 'new_prob', 'neg_prob'

═══════════════════════════════════════════════════════════════════════════
PART 11: TIME MANAGEMENT (45-minute interview)
═══════════════════════════════════════════════════════════════════════════

0-3 min:   Understand problem, identify it's modified Dijkstra's
3-7 min:   Explain approach, draw example, discuss modifications
7-25 min:  Code Solution 1 (Dijkstra's with max-heap)
25-30 min: Trace through example, verify correctness
30-35 min: Test edge cases
35-40 min: Complexity analysis
40-45 min: Discuss alternatives, answer follow-ups

═══════════════════════════════════════════════════════════════════════════
FINAL RECOMMENDATION
═══════════════════════════════════════════════════════════════════════════

ALWAYS implement Solution 1 (Modified Dijkstra's with Max-Heap).

This shows:
✓ Strong grasp of classical algorithms
✓ Ability to adapt algorithms to new problems
✓ Understanding of why the modification works
✓ Optimal time complexity
✓ Clean, production-ready code

The fact that it's "just Dijkstra's with modifications" is actually a 
strength - it shows pattern recognition and algorithmic maturity.
"""
