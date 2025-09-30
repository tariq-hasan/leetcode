"""
LeetCode 787: Cheapest Flights Within K Stops
Medium

There are n cities connected by some number of flights. You are given an array 
flights where flights[i] = [from_i, to_i, price_i] indicates that there is a 
flight from city from_i to city to_i with cost price_i.

You are also given three integers src, dst, and k, return the cheapest price 
from src to dst with at most k stops. If there is no such route, return -1.

Example 1:
Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 
       src = 0, dst = 3, k = 1
Output: 700
Explanation: The optimal path is 0->1->3 with price 700.

Example 2:
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], 
       src = 0, dst = 2, k = 1
Output: 200

Example 3:
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], 
       src = 0, dst = 2, k = 0
Output: 500
"""

from typing import List
import heapq
from collections import defaultdict, deque


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 1: Modified Dijkstra's Algorithm
        Time: O(E * K * log(E * K)), Space: O(E * K)
        
        ⭐ RECOMMENDED FOR INTERVIEWS ⭐
        
        Key Insight: This is NOT standard Dijkstra's!
        - Standard Dijkstra's: once a node is visited, never revisit
        - This problem: MUST revisit nodes with different stop counts
        - State: (cost, node, stops_used) - node can appear multiple times
        
        CRITICAL: We can't mark node as "visited" permanently because we might
        reach it later with more stops remaining, allowing cheaper final path.
        """
        # Build adjacency list
        graph = defaultdict(list)
        for u, v, price in flights:
            graph[u].append((v, price))
        
        # Min-heap: (cost, node, stops_used)
        heap = [(0, src, 0)]
        
        # Track minimum cost to reach each (node, stops) state
        # Key insight: we need to track BOTH node and stops used
        visited = {}
        
        while heap:
            cost, node, stops = heapq.heappop(heap)
            
            # Found destination
            if node == dst:
                return cost
            
            # Exceeded stop limit
            if stops > k:
                continue
            
            # Skip if we've seen this (node, stops) state with lower cost
            if (node, stops) in visited and visited[(node, stops)] <= cost:
                continue
            
            visited[(node, stops)] = cost
            
            # Explore neighbors
            for neighbor, price in graph[node]:
                new_cost = cost + price
                new_stops = stops + 1
                
                # Only add if within stop limit
                if new_stops <= k + 1:  # +1 because we count edges, not nodes
                    heapq.heappush(heap, (new_cost, neighbor, new_stops))
        
        return -1


class Solution2:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 2: Bellman-Ford with K+1 Iterations
        Time: O(K * E), Space: O(N)
        
        ⭐ MOST ELEGANT SOLUTION ⭐
        
        Perfect for this problem! Natural fit because:
        - Bellman-Ford relaxes edges iteratively
        - K+1 iterations = at most K stops
        - Simpler to implement correctly than Dijkstra's
        """
        # Initialize distances to infinity
        dist = [float('inf')] * n
        dist[src] = 0
        
        # Relax edges K+1 times (K stops = K+1 edges)
        for _ in range(k + 1):
            # Important: use a copy to avoid using updated values in same iteration
            temp = dist[:]
            
            for u, v, price in flights:
                if dist[u] != float('inf'):
                    temp[v] = min(temp[v], dist[u] + price)
            
            dist = temp
        
        return dist[dst] if dist[dst] != float('inf') else -1


class Solution3:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 3: BFS with Level-Order Traversal
        Time: O(N * K), Space: O(N)
        
        Intuitive approach: each BFS level = one stop
        Good for explaining the problem conceptually
        """
        graph = defaultdict(list)
        for u, v, price in flights:
            graph[u].append((v, price))
        
        # Track minimum cost to reach each node
        min_cost = [float('inf')] * n
        min_cost[src] = 0
        
        # BFS queue: (node, cost)
        queue = deque([(src, 0)])
        stops = 0
        
        while queue and stops <= k:
            size = len(queue)
            
            # Process all nodes at current level (same number of stops)
            for _ in range(size):
                node, cost = queue.popleft()
                
                for neighbor, price in graph[node]:
                    new_cost = cost + price
                    
                    # Only proceed if this path is cheaper
                    if new_cost < min_cost[neighbor]:
                        min_cost[neighbor] = new_cost
                        queue.append((neighbor, new_cost))
            
            stops += 1
        
        return min_cost[dst] if min_cost[dst] != float('inf') else -1


class Solution4:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 4: DFS with Memoization
        Time: O(N * K * E), Space: O(N * K)
        
        More intuitive but potentially slower
        Good for showing different thinking approach
        """
        graph = defaultdict(list)
        for u, v, price in flights:
            graph[u].append((v, price))
        
        # Memoization: (node, stops_remaining) -> min_cost
        memo = {}
        
        def dfs(node, stops_remaining):
            # Base cases
            if node == dst:
                return 0
            
            if stops_remaining < 0:
                return float('inf')
            
            if (node, stops_remaining) in memo:
                return memo[(node, stops_remaining)]
            
            # Try all neighbors
            min_price = float('inf')
            for neighbor, price in graph[node]:
                cost = price + dfs(neighbor, stops_remaining - 1)
                min_price = min(min_price, cost)
            
            memo[(node, stops_remaining)] = min_price
            return min_price
        
        result = dfs(src, k + 1)  # k stops = k+1 edges
        return result if result != float('inf') else -1


class Solution5:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 5: Dynamic Programming
        Time: O(K * E), Space: O(N * K)
        
        Bottom-up DP approach
        dp[i][j] = min cost to reach city j using at most i stops
        """
        # dp[stops][city] = minimum cost
        dp = [[float('inf')] * n for _ in range(k + 2)]
        
        # Base case: 0 cost to reach src with any number of stops
        for i in range(k + 2):
            dp[i][src] = 0
        
        # Build up solution
        for stops in range(1, k + 2):
            for u, v, price in flights:
                dp[stops][v] = min(dp[stops][v], dp[stops - 1][u] + price)
        
        # Find minimum across all stop counts
        result = min(dp[i][dst] for i in range(k + 2))
        return result if result != float('inf') else -1


class Solution6:
    def findCheapestPrice(self, n: int, flights: List[List[int]], 
                          src: int, dst: int, k: int) -> int:
        """
        Approach 6: Space-Optimized Bellman-Ford
        Time: O(K * E), Space: O(N)
        
        Most efficient in practice - clean and fast
        """
        prices = [float('inf')] * n
        prices[src] = 0
        
        for _ in range(k + 1):
            temp_prices = prices[:]
            
            for u, v, price in flights:
                if prices[u] < float('inf'):
                    temp_prices[v] = min(temp_prices[v], prices[u] + price)
            
            prices = temp_prices
        
        return -1 if prices[dst] == float('inf') else prices[dst]


# Test cases
def test_solutions():
    solutions = [
        ("Modified Dijkstra's", Solution()),
        ("Bellman-Ford (K+1 iterations)", Solution2()),
        ("BFS Level-Order", Solution3()),
        ("DFS with Memoization", Solution4()),
        ("Dynamic Programming", Solution5()),
        ("Space-Optimized Bellman-Ford", Solution6())
    ]
    
    test_cases = [
        (4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1, 700),
        (3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1, 200),
        (3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 0, 500),
        (3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 2, 200),
        (5, [[0,1,5],[1,2,5],[0,3,2],[3,1,2],[1,4,1],[4,2,1]], 0, 2, 2, 7),
        (4, [[0,1,1],[0,2,5],[1,2,1],[2,3,1]], 0, 3, 1, 6),
        (2, [[0,1,100]], 0, 1, 0, 100),
        (2, [[0,1,100]], 0, 1, 1, 100),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        all_passed = True
        for n, flights, src, dst, k, expected in test_cases:
            result = solution.findCheapestPrice(n, flights, src, dst, k)
            passed = result == expected
            status = "✓" if passed else "✗"
            if not passed:
                all_passed = False
            print(f"  {status} n={n}, edges={len(flights)}, k={k} -> {result} (expected: {expected})")
        print(f"  {'All tests passed!' if all_passed else 'Some tests failed!'}\n")


if __name__ == "__main__":
    test_solutions()


"""
═══════════════════════════════════════════════════════════════════════════
COMPREHENSIVE INTERVIEW GUIDE
═══════════════════════════════════════════════════════════════════════════

PART 1: CRITICAL PROBLEM RECOGNITION (First 60 seconds)
═══════════════════════════════════════════════════════════════════════════

⚠️ THIS IS THE TRAP: It looks like standard Dijkstra's, but IT'S NOT! ⚠️

What to say immediately:

"This looks like a shortest path problem, but there's a critical constraint: 
at most K stops. This changes everything!

In standard Dijkstra's, once we visit a node, we never revisit it because 
we've found the shortest path. But here, we might need to reach a node 
multiple times with different numbers of stops used, because having more 
stops remaining might lead to a cheaper final path.

I see three main approaches:
1. Bellman-Ford with K+1 iterations - O(K*E) ⭐ MOST ELEGANT
2. Modified Dijkstra's tracking (node, stops) states - O(E*K*log(E*K))
3. BFS with level-order traversal - O(N*K)

I'll implement Bellman-Ford as it's the cleanest solution for this constraint."

═══════════════════════════════════════════════════════════════════════════
PART 2: WHY STANDARD DIJKSTRA'S FAILS
═══════════════════════════════════════════════════════════════════════════

CRITICAL to explain this:

"Standard Dijkstra's fails because:

Example: 
  A --$10--> B --$1--> C
  A -------$15-------> C

With k=1 (one stop allowed):
- Dijkstra's would first find A->C for $15 (direct, 0 stops)
- It would mark C as 'visited' with cost $15
- Later it would find A->B->C for $11 (but 1 stop)
- But C is already 'visited', so it ignores this cheaper path!

The issue: Dijkstra's optimizes on cost only, but we have a SECOND dimension
(number of stops) that affects reachability.

Solution: Track states as (node, stops_used) pairs, not just nodes."

═══════════════════════════════════════════════════════════════════════════
PART 3: WHY BELLMAN-FORD IS PERFECT HERE
═══════════════════════════════════════════════════════════════════════════

"Bellman-Ford is ideal because:

1. It iterates exactly K+1 times (K stops = K+1 edges)
2. Each iteration considers paths with one more edge
3. It naturally respects the stop constraint
4. Simpler implementation with fewer edge cases
5. O(K*E) time is excellent for typical inputs

The algorithm:
- Iteration 0: Only src is reachable (cost 0)
- Iteration 1: All nodes 1 edge from src
- Iteration 2: All nodes 2 edges from src
- ...
- Iteration K+1: All nodes K+1 edges from src (K stops)

Perfect match for the problem!"

═══════════════════════════════════════════════════════════════════════════
PART 4: IMPLEMENTATION STRATEGY - BELLMAN-FORD (Recommended)
═══════════════════════════════════════════════════════════════════════════

Step 1 (2 min): Setup
"Initialize all distances to infinity, except src = 0"

Step 2 (3 min): Critical insight
"Use a COPY of dist array for each iteration. Why? If we update in-place,
we might use newly updated values in the same iteration, which represents
paths with MORE than one additional edge. The copy ensures each iteration
represents exactly one more edge."

Step 3 (8 min): Main loop
```python
for _ in range(k + 1):  # K stops = K+1 edges
    temp = dist[:]  # CRITICAL: use copy!
    
    for u, v, price in flights:
        if dist[u] != float('inf'):
            temp[v] = min(temp[v], dist[u] + price)
    
    dist = temp
```

Step 4 (2 min): Return result
"Check if dst is reachable (not infinity), return cost or -1"

═══════════════════════════════════════════════════════════════════════════
PART 5: IMPLEMENTATION STRATEGY - DIJKSTRA'S (Alternative)
═══════════════════════════════════════════════════════════════════════════

If you prefer Dijkstra's:

Key modifications:
1. State is (cost, node, stops_used) - three dimensions!
2. Track visited as {(node, stops): min_cost}
3. Can visit same node multiple times with different stop counts
4. Don't mark node as permanently visited

```python
heap = [(0, src, 0)]  # (cost, node, stops)
visited = {}  # {(node, stops): cost}

while heap:
    cost, node, stops = heapq.heappop(heap)
    
    if node == dst:
        return cost  # First time reaching dst is optimal
    
    if stops > k:
        continue
    
    # Check if this (node, stops) state already seen with better cost
    if (node, stops) in visited and visited[(node, stops)] <= cost:
        continue
    
    visited[(node, stops)] = cost
    
    for neighbor, price in graph[node]:
        if stops < k + 1:  # Can still add stops
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))
```

⚠️ Common mistake: Checking `if node in visited` without considering stops!

═══════════════════════════════════════════════════════════════════════════
PART 6: COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

Bellman-Ford Approach:
Time: O(K * E)
- K+1 iterations
- Each iteration: O(E) to process all edges
- Total: O((K+1) * E) = O(K * E)

Space: O(N)
- Two arrays of size N (dist and temp)
- Total: O(N)

Modified Dijkstra's:
Time: O(E * K * log(E * K))
- Up to E*K states in heap
- Each heap operation: O(log(E*K))

Space: O(E * K)
- Heap and visited dictionary can store E*K states

"For typical interview constraints (K << N, E << N^2), Bellman-Ford is 
simpler and more efficient!"

═══════════════════════════════════════════════════════════════════════════
PART 7: EDGE CASES & TESTING
═══════════════════════════════════════════════════════════════════════════

Must discuss:

✓ k = 0 (no stops, only direct flights)
✓ k >= n-1 (no constraint, reduce to standard shortest path)
✓ src = dst (return 0)
✓ No path exists (return -1)
✓ Multiple paths with same cost but different stops
✓ Negative cycles (problem states prices are positive, so not an issue)
✓ Self-loops (generally not in input, but handle gracefully)

Example trace for [[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1:

Iteration 0: dist = [0, inf, inf]
Iteration 1: 
  - Edge 0->1: dist[1] = min(inf, 0+100) = 100
  - Edge 0->2: dist[2] = min(inf, 0+500) = 500
  Result: [0, 100, 500]

Iteration 2:
  - Edge 0->1: dist[1] = min(100, 0+100) = 100
  - Edge 1->2: dist[2] = min(500, 100+100) = 200 ✓
  - Edge 0->2: dist[2] = min(200, 0+500) = 200
  Result: [0, 100, 200]

Answer: 200

═══════════════════════════════════════════════════════════════════════════
PART 8: COMMON MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════

❌ Using standard Dijkstra's without state modification
❌ Not using a copy in Bellman-Ford (updating in-place)
❌ Off-by-one error: k stops = k+1 edges!
❌ In Dijkstra's: marking node as visited without considering stops
❌ Not checking if source cost is infinity before relaxing
❌ Confusing stops with edges (1 stop = 2 nodes = 1 edge)
❌ Early termination in Dijkstra's without proper state checking
❌ Not handling unreachable destination

═══════════════════════════════════════════════════════════════════════════
PART 9: WHY THIS PROBLEM IS TRICKY
═══════════════════════════════════════════════════════════════════════════

This problem is deceptively hard because:

1. **Looks like standard shortest path** - but has critical twist
2. **Dijkstra's seems natural** - but fails without modification
3. **The constraint is subtle** - "at most k stops" affects algorithm choice
4. **State space increases** - from N nodes to N*K states
5. **Multiple correct approaches** - need to choose and justify

"This is a great interview problem because it tests whether you truly 
understand shortest path algorithms, not just memorize them. Recognizing 
that standard Dijkstra's fails shows algorithmic maturity."

═══════════════════════════════════════════════════════════════════════════
PART 10: COMPARISON OF APPROACHES
═══════════════════════════════════════════════════════════════════════════

Approach           Time         Space    Implementation    Interview Rating
--------------------------------------------------------------------------
Bellman-Ford      O(K*E)       O(N)     Easy             ⭐⭐⭐⭐⭐ BEST
Modified Dijkstra O(EK*log EK) O(EK)    Medium           ⭐⭐⭐⭐ GOOD
BFS Level-Order   O(N*K)       O(N)     Easy             ⭐⭐⭐ OK
DFS + Memo        O(N*K*E)     O(N*K)   Medium           ⭐⭐ ACCEPTABLE
Dynamic Programming O(K*E)     O(N*K)   Medium           ⭐⭐⭐ GOOD

Recommendation: 
- Primary choice: Bellman-Ford (Solution 2 or 6)
- Backup: Modified Dijkstra's if you're more comfortable with it
- Mention: BFS approach shows good problem-solving thinking

═══════════════════════════════════════════════════════════════════════════
PART 11: FOLLOW-UP QUESTIONS & ANSWERS
═══════════════════════════════════════════════════════════════════════════

Q: "What if we want EXACTLY k stops, not at most k?"
A: "Change the iteration count to exactly k+1 in Bellman-Ford. In Dijkstra's,
   only add to result when stops == k."

Q: "What if there are negative edge weights?"
A: "Bellman-Ford handles negative weights naturally! But we'd need to detect
   negative cycles. Standard Dijkstra's would fail completely."

Q: "How would you find the actual path, not just the cost?"
A: "Add parent tracking. In Bellman-Ford, store parent[v] = u when updating.
   In Dijkstra's, store parent as part of state: (node, stops) -> parent."

Q: "What if we want top K cheapest paths?"
A: "Modify to not mark states as visited immediately. Keep finding paths
   until we've found K distinct paths to destination. Use priority queue
   to get them in order."

Q: "Can you optimize space further?"
A: "Bellman-Ford already uses O(N) which is optimal - we need at least that
   to store distances. Dijkstra's could use less space with careful pruning."

Q: "What if graph is very dense?"
A: "Bellman-Ford becomes O(K*N^2) which might be slow. Consider A* search
   with heuristic, or bidirectional search from both src and dst."

Q: "How would you handle multiple destinations?"
A: "Run algorithm once without early termination. Check costs to all 
   destination nodes at the end. Bellman-Ford naturally handles this."

═══════════════════════════════════════════════════════════════════════════
PART 12: KEY TALKING POINTS DURING INTERVIEW
═══════════════════════════════════════════════════════════════════════════

Opening (show recognition):
"I immediately notice this isn't standard shortest path because of the stop
constraint. Standard Dijkstra's would fail here."

Middle (show understanding):
"Using Bellman-Ford's k+1 iterations naturally enforces the constraint - 
each iteration adds one more edge, which is exactly what we need."

"The key insight is using a copy of the distance array - this ensures each
iteration represents exactly one additional edge, not multiple."

Critical detail:
"Note that k stops means k+1 edges! This is a common off-by-one error point."

Complexity:
"Time is O(K*E) which is excellent for typical cases where K is small. Much
better than the O(N^3) of Floyd-Warshall or the O(EK*log(EK)) of modified
Dijkstra's."

═══════════════════════════════════════════════════════════════════════════
PART 13: CONCRETE EXAMPLE WALKTHROUGH
═══════════════════════════════════════════════════════════════════════════

Let's trace: n=4, edges=[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src=0, dst=3, k=1

Initial: dist = [0, ∞, ∞, ∞]

Iteration 1 (paths with 1 edge):
  0->1: dist[1] = min(∞, 0+100) = 100
  Result: [0, 100, ∞, ∞]

Iteration 2 (paths with 2 edges = 1 stop):
  0->1: dist[1] = min(100, 0+100) = 100
  1->2: dist[2] = min(∞, 100+100) = 200
  1->3: dist[3] = min(∞, 100+600) = 700
  Result: [0, 100, 200, 700]

Answer: 700 ✓

Note: Path 0->1->2->3 would cost 500 but requires 2 stops, exceeding k=1!

═══════════════════════════════════════════════════════════════════════════
PART 14: TIME MANAGEMENT (45-minute interview)
═══════════════════════════════════════════════════════════════════════════

0-3 min:   Understand problem, identify it's constrained shortest path
3-6 min:   Explain why standard Dijkstra's fails, discuss approaches
6-10 min:  Decide on Bellman-Ford, explain why it's perfect
10-28 min: Code Bellman-Ford solution (clean implementation)
28-35 min: Trace through example, verify correctness
35-40 min: Test edge cases (k=0, no path, src=dst)
40-43 min: Complexity analysis
43-45 min: Discuss alternatives (Dijkstra's) and follow-ups

═══════════════════════════════════════════════════════════════════════════
FINAL RECOMMENDATION
═══════════════════════════════════════════════════════════════════════════

IMPLEMENT: Solution 2 or 6 (Bellman-Ford)

WHY:
✓ Simplest correct solution
✓ Best time complexity for typical inputs
✓ Naturally respects stop constraint
✓ Easier to implement correctly under pressure
✓ Shows deep understanding of when to use which algorithm

MENTION: "I could also use modified Dijkstra's tracking (node, stops) states,
but Bellman-Ford is more elegant for this specific constraint."

DEMONSTRATE:
✓ Recognition that standard algorithms need adaptation
✓ Understanding of why Bellman-Ford fits perfectly
✓ Attention to detail (copy array, k+1 iterations)
✓ Clean, bug-free implementation
✓ Thorough testing and edge case handling

This problem separates candidates who memorize from those who understand!
"""
