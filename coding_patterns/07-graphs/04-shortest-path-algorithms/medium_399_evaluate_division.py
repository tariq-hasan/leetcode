"""
LeetCode 399: Evaluate Division
Medium

You are given an array of variable pairs equations and an array of real 
numbers values, where equations[i] = [Ai, Bi] and values[i] represent the 
equation Ai / Bi = values[i]. Each Ai or Bi is a string that represents a 
single variable.

You are also given some queries, where queries[j] = [Cj, Dj] represents the 
jth query where you must find the answer for Cj / Dj = ?.

Return the answers to all queries. If a single answer cannot be determined, 
return -1.0.

Note: The input is always valid. You may assume that evaluating the queries 
will not result in division by zero and that there is no contradiction.

Example 1:
Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], 
       queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
Explanation: 
Given: a/b=2.0, b/c=3.0
queries: a/c=?, b/a=?, a/e=?, a/a=?, x/x=?
return: [6.0, 0.5, -1.0, 1.0, -1.0]

Example 2:
Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], 
       queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
Output: [3.75000,0.40000,5.00000,0.20000]
"""

from typing import List
from collections import defaultdict, deque


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], 
                     queries: List[List[str]]) -> List[float]:
        """
        Approach 1: DFS on Weighted Directed Graph
        Time: O((E + Q) * (V + E)), Space: O(V + E)
        
        ⭐ RECOMMENDED FOR INTERVIEWS ⭐
        
        Key Insight: Model as a weighted directed graph
        - Each variable is a node
        - If a/b = k, then:
          - Edge a → b with weight k
          - Edge b → a with weight 1/k
        - Query x/y = finding path from x to y and multiplying edge weights
        
        This is elegant and intuitive!
        """
        # Build weighted directed graph
        graph = defaultdict(dict)
        
        for (dividend, divisor), value in zip(equations, values):
            graph[dividend][divisor] = value
            graph[divisor][dividend] = 1.0 / value
        
        def dfs(start, end, visited):
            """Find path from start to end, return product of edge weights"""
            # Base cases
            if start not in graph or end not in graph:
                return -1.0
            
            if start == end:
                return 1.0
            
            visited.add(start)
            
            # Try all neighbors
            for neighbor, weight in graph[start].items():
                if neighbor not in visited:
                    result = dfs(neighbor, end, visited)
                    if result != -1.0:
                        return weight * result
            
            return -1.0
        
        # Process each query
        results = []
        for dividend, divisor in queries:
            results.append(dfs(dividend, divisor, set()))
        
        return results


class Solution2:
    def calcEquation(self, equations: List[List[str]], values: List[float], 
                     queries: List[List[str]]) -> List[float]:
        """
        Approach 2: Union-Find (Disjoint Set Union)
        Time: O((E + Q) * α(V)), Space: O(V)
        
        ⭐ MOST EFFICIENT ⭐
        
        Key Insight: Use weighted union-find
        - Track weight[x] = value of x relative to its parent
        - Path compression updates weights correctly
        - Query: if x and y in same component, return weight[x] / weight[y]
        
        More complex but optimal for many queries!
        """
        parent = {}
        weight = {}  # weight[x] = value of x relative to parent[x]
        
        def find(x):
            """Find root with path compression, update weights"""
            if x not in parent:
                parent[x] = x
                weight[x] = 1.0
                return x
            
            if parent[x] != x:
                root = find(parent[x])
                # Update weight: x's value relative to root
                weight[x] *= weight[parent[x]]
                parent[x] = root
            
            return parent[x]
        
        def union(x, y, value):
            """Union: x / y = value"""
            root_x = find(x)
            root_y = find(y)
            
            if root_x != root_y:
                # Connect root_x to root_y
                # weight[root_x] should represent root_x / root_y
                parent[root_x] = root_y
                # x / y = value
                # x / root_x * root_x / root_y * root_y / y = value
                # (1/weight[x]) * (root_x/root_y) * weight[y] = value
                # root_x / root_y = value * weight[x] / weight[y]
                weight[root_x] = value * weight[y] / weight[x]
        
        # Build union-find structure
        for (dividend, divisor), value in zip(equations, values):
            union(dividend, divisor, value)
        
        # Process queries
        results = []
        for dividend, divisor in queries:
            if dividend not in parent or divisor not in parent:
                results.append(-1.0)
            elif find(dividend) != find(divisor):
                results.append(-1.0)
            else:
                # Both in same component
                results.append(weight[dividend] / weight[divisor])
        
        return results


class Solution3:
    def calcEquation(self, equations: List[List[str]], values: List[float], 
                     queries: List[List[str]]) -> List[float]:
        """
        Approach 3: BFS on Weighted Graph
        Time: O((E + Q) * (V + E)), Space: O(V + E)
        
        Alternative to DFS - same idea, iterative approach
        Good if you prefer BFS over DFS
        """
        # Build graph
        graph = defaultdict(dict)
        
        for (dividend, divisor), value in zip(equations, values):
            graph[dividend][divisor] = value
            graph[divisor][dividend] = 1.0 / value
        
        def bfs(start, end):
            """Find path from start to end using BFS"""
            if start not in graph or end not in graph:
                return -1.0
            
            if start == end:
                return 1.0
            
            queue = deque([(start, 1.0)])  # (node, accumulated_product)
            visited = {start}
            
            while queue:
                node, product = queue.popleft()
                
                for neighbor, weight in graph[node].items():
                    if neighbor == end:
                        return product * weight
                    
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, product * weight))
            
            return -1.0
        
        return [bfs(dividend, divisor) for dividend, divisor in queries]


class Solution4:
    def calcEquation(self, equations: List[List[str]], values: List[float], 
                     queries: List[List[str]]) -> List[float]:
        """
        Approach 4: Floyd-Warshall (All-Pairs Shortest Path)
        Time: O(V³ + Q), Space: O(V²)
        
        Precompute all pairs of divisions
        Excellent when number of queries >> number of variables
        """
        # Collect all variables
        variables = set()
        for eq in equations:
            variables.update(eq)
        
        var_list = list(variables)
        var_to_idx = {var: i for i, var in enumerate(var_list)}
        n = len(var_list)
        
        # Initialize distance matrix
        dist = [[0.0] * n for _ in range(n)]
        
        # Set diagonal to 1 (x/x = 1)
        for i in range(n):
            dist[i][i] = 1.0
        
        # Fill in given equations
        for (dividend, divisor), value in zip(equations, values):
            i, j = var_to_idx[dividend], var_to_idx[divisor]
            dist[i][j] = value
            dist[j][i] = 1.0 / value
        
        # Floyd-Warshall: compute all pairs
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != 0 and dist[k][j] != 0:
                        if dist[i][j] == 0:
                            dist[i][j] = dist[i][k] * dist[k][j]
        
        # Process queries
        results = []
        for dividend, divisor in queries:
            if dividend not in var_to_idx or divisor not in var_to_idx:
                results.append(-1.0)
            else:
                i, j = var_to_idx[dividend], var_to_idx[divisor]
                results.append(dist[i][j] if dist[i][j] != 0 else -1.0)
        
        return results


class Solution5:
    def calcEquation(self, equations: List[List[str]], values: List[float], 
                     queries: List[List[str]]) -> List[float]:
        """
        Approach 5: DFS with Path Recording (Educational)
        Time: O(Q * V!), Space: O(V + E)
        
        Finds all paths from start to end - educational but inefficient
        Shows the problem structure clearly
        """
        graph = defaultdict(dict)
        
        for (dividend, divisor), value in zip(equations, values):
            graph[dividend][divisor] = value
            graph[divisor][dividend] = 1.0 / value
        
        def find_all_paths(start, end, visited, current_product):
            """DFS to find path and accumulate product"""
            if start not in graph or end not in graph:
                return -1.0
            
            if start == end:
                return current_product
            
            visited.add(start)
            
            for neighbor, weight in graph[start].items():
                if neighbor not in visited:
                    result = find_all_paths(neighbor, end, visited, 
                                           current_product * weight)
                    if result != -1.0:
                        return result
            
            visited.remove(start)  # Backtrack
            return -1.0
        
        results = []
        for dividend, divisor in queries:
            if dividend == divisor:
                if dividend in graph:
                    results.append(1.0)
                else:
                    results.append(-1.0)
            else:
                results.append(find_all_paths(dividend, divisor, set(), 1.0))
        
        return results


# Test cases
def test_solutions():
    solutions = [
        ("DFS on Weighted Graph (Best)", Solution()),
        ("Union-Find (Most Efficient)", Solution2()),
        ("BFS on Weighted Graph", Solution3()),
        ("Floyd-Warshall (All-Pairs)", Solution4()),
        ("DFS with Backtracking", Solution5())
    ]
    
    test_cases = [
        (
            [["a","b"],["b","c"]], 
            [2.0, 3.0],
            [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]],
            [6.0, 0.5, -1.0, 1.0, -1.0]
        ),
        (
            [["a","b"],["b","c"],["bc","cd"]], 
            [1.5, 2.5, 5.0],
            [["a","c"],["c","b"],["bc","cd"],["cd","bc"]],
            [3.75, 0.4, 5.0, 0.2]
        ),
        (
            [["a","b"]], 
            [0.5],
            [["a","b"],["b","a"],["a","c"],["x","y"]],
            [0.5, 2.0, -1.0, -1.0]
        ),
        (
            [["x1","x2"],["x2","x3"],["x3","x4"],["x4","x5"]], 
            [3.0, 4.0, 5.0, 6.0],
            [["x1","x5"],["x5","x2"],["x2","x4"],["x2","x2"],["x2","x9"]],
            [360.0, 1.0/72.0, 20.0, 1.0, -1.0]
        ),
    ]
    
    for name, solution in solutions:
        print(f"Testing {name}:")
        all_passed = True
        for equations, values, queries, expected in test_cases:
            result = solution.calcEquation(equations, values, queries)
            
            # Check if results match (with floating point tolerance)
            passed = len(result) == len(expected) and all(
                abs(r - e) < 1e-5 if e != -1.0 else r == -1.0
                for r, e in zip(result, expected)
            )
            
            status = "✓" if passed else "✗"
            if not passed:
                all_passed = False
            print(f"  {status} {len(equations)} equations, {len(queries)} queries")
        
        print(f"  {'All tests passed!' if all_passed else 'Some tests failed!'}\n")


if __name__ == "__main__":
    test_solutions()


"""
═══════════════════════════════════════════════════════════════════════════
COMPREHENSIVE INTERVIEW GUIDE
═══════════════════════════════════════════════════════════════════════════

PART 1: CRITICAL PROBLEM RECOGNITION (First 60 seconds)
═══════════════════════════════════════════════════════════════════════════

⭐ THIS IS A GRAPH PROBLEM IN DISGUISE! ⭐

What to say immediately:

"This is a graph problem! The key insight is modeling divisions as a weighted 
directed graph:

- Each variable is a NODE
- If a/b = k, create TWO EDGES:
  * Edge a → b with weight k
  * Edge b → a with weight 1/k
  
Then, finding x/y means finding a path from x to y and MULTIPLYING the edge 
weights along the path!

For example:
- Given: a/b = 2.0, b/c = 3.0
- Query a/c: Path a → b → c, product = 2.0 × 3.0 = 6.0

I see three main approaches:
1. DFS/BFS on graph - O((E+Q)*(V+E)) ⭐ MOST INTUITIVE
2. Union-Find - O((E+Q)*α(V)) ⭐ MOST EFFICIENT  
3. Floyd-Warshall - O(V³ + Q) - Good for many queries

I'll implement DFS as it's the most intuitive and clean."

═══════════════════════════════════════════════════════════════════════════
PART 2: THE BEAUTIFUL GRAPH TRANSFORMATION
═══════════════════════════════════════════════════════════════════════════

Visual explanation:

Given: a/b = 2, b/c = 3

Graph representation:
    a ----2.0---→ b ----3.0---→ c
      ←--0.5----    ←--0.33---

Query a/c:
- Path: a → b → c
- Product: 2.0 × 3.0 = 6.0 ✓

Query c/a:
- Path: c → b → a
- Product: 0.33 × 0.5 = 0.166... = 1/6 ✓

Query b/a:
- Path: b → a
- Product: 0.5 ✓

"This transformation is elegant because:
1. Divisions become path-finding
2. Transitivity is automatic (a/b × b/c = a/c)
3. Inverses are natural (reverse edge with reciprocal weight)
4. Each query is independent - just find one path"

═══════════════════════════════════════════════════════════════════════════
PART 3: IMPLEMENTATION STRATEGY - DFS (Recommended)
═══════════════════════════════════════════════════════════════════════════

Step 1 (3 min): Build the graph
"Use defaultdict of dicts for weighted adjacency list. For each equation 
a/b=k, add both directions with reciprocal weights."

```python
graph = defaultdict(dict)
for (dividend, divisor), value in zip(equations, values):
    graph[dividend][divisor] = value
    graph[divisor][dividend] = 1.0 / value
```

Step 2 (8 min): DFS to find path
```python
def dfs(start, end, visited):
    # Base cases
    if start not in graph or end not in graph:
        return -1.0
    
    if start == end:
        return 1.0  # x/x = 1
    
    visited.add(start)
    
    # Try each neighbor
    for neighbor, weight in graph[start].items():
        if neighbor not in visited:
            result = dfs(neighbor, end, visited)
            if result != -1.0:
                return weight * result  # Multiply along path
    
    return -1.0
```

Step 3 (3 min): Process queries
"For each query, run DFS with fresh visited set."

Step 4 (1 min): Return results
"Collect all query results in list and return."

═══════════════════════════════════════════════════════════════════════════
PART 4: UNION-FIND APPROACH (Advanced Alternative)
═══════════════════════════════════════════════════════════════════════════

"Union-Find is more complex but more efficient for many queries!

Key insight: Track relative weights
- parent[x] = parent of x in tree
- weight[x] = value of x relative to parent[x]

Example: a/b = 2, b/c = 3
- After union: parent[a]=b, weight[a]=2 (a is 2× its parent b)
- After union: parent[b]=c, weight[b]=3 (b is 3× its parent c)
- Query a/c: Find makes a's parent c, weight[a]=6 (path compression!)

The magic is in path compression - it automatically computes transitive 
relationships!"

Time complexity:
- Build: O(E × α(V))
- Query: O(Q × α(V))
- Total: O((E+Q) × α(V)) where α is inverse Ackermann (practically constant)

"This is optimal when Q >> V, but harder to implement correctly in interviews."

═══════════════════════════════════════════════════════════════════════════
PART 5: COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

DFS/BFS Approach (Solution 1 & 3):
Time: O((E + Q) × (V + E))
- Build graph: O(E)
- Each query: O(V + E) worst case (DFS/BFS through graph)
- Q queries: O(Q × (V + E))
- Total: O(E + Q × (V + E))

Space: O(V + E)
- Graph adjacency list: O(E)
- Visited set: O(V)
- Recursion stack: O(V)

Union-Find Approach (Solution 2):
Time: O((E + Q) × α(V)) ≈ O(E + Q)
- Build: O(E × α(V))
- Each query: O(α(V)) ≈ O(1)
- Total: O((E + Q) × α(V))

Space: O(V)
- Parent and weight arrays: O(V)

Floyd-Warshall Approach (Solution 4):
Time: O(V³ + Q)
- Precompute all pairs: O(V³)
- Each query: O(1)
- Total: O(V³ + Q)

Space: O(V²)
- Distance matrix: O(V²)

"For interviews, DFS is best balance of simplicity and efficiency!"

═══════════════════════════════════════════════════════════════════════════
PART 6: EDGE CASES & TESTING
═══════════════════════════════════════════════════════════════════════════

Must discuss:

✓ Query for x/x where x exists → return 1.0
✓ Query for x/x where x doesn't exist → return -1.0
✓ Query for variables not in equations → return -1.0
✓ Query for x/y in different connected components → return -1.0
✓ Chain of divisions: a/b, b/c, c/d → can compute a/d
✓ Reciprocal queries: if a/b=2, then b/a=0.5
✓ Single variable: [["a","a"]] with value [1.0] → valid

Example trace:
equations = [["a","b"],["b","c"]], values = [2.0, 3.0]
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]

Graph:
  a ←0.5→ b ←0.33→ c
    →2.0→   →3.0→

Query "a","c": DFS path a→b→c, product 2.0×3.0 = 6.0 ✓
Query "b","a": DFS path b→a, product 0.5 ✓
Query "a","e": e not in graph → -1.0 ✓
Query "a","a": same node → 1.0 ✓
Query "x","x": x not in graph → -1.0 ✓

═══════════════════════════════════════════════════════════════════════════
PART 7: COMMON MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════

❌ Only adding one direction (forgetting reciprocal edge)
❌ Using addition instead of multiplication for weights
❌ Not handling x/x case (should return 1.0 if x exists)
❌ Not checking if variables exist in graph before querying
❌ Reusing visited set across queries (must reset per query!)
❌ Forgetting to multiply weights along path (just returning weight)
❌ Not handling disconnected components

✅ CORRECT pattern:
```python
# Build bidirectional edges with reciprocals
graph[a][b] = value
graph[b][a] = 1.0 / value

# Fresh visited set per query
for dividend, divisor in queries:
    result = dfs(dividend, divisor, set())  # NEW set()
    results.append(result)

# Multiply along path
for neighbor, weight in graph[node].items():
    result = dfs(neighbor, end, visited)
    if result != -1.0:
        return weight * result  # MULTIPLY!
```

═══════════════════════════════════════════════════════════════════════════
PART 8: WHY THIS PROBLEM IS BRILLIANT
═══════════════════════════════════════════════════════════════════════════

This problem is perfect for interviews because:

1. **Not obviously a graph problem** - tests abstraction skills
2. **Multiple valid approaches** - can discuss tradeoffs
3. **Combines multiple concepts** - graphs, DFS, weighted edges
4. **Clean implementation** - ~30 lines for DFS solution
5. **Natural follow-ups** - many interesting extensions
6. **Real-world relevance** - currency exchange, unit conversions

"The key skill tested: Can you transform a non-obvious problem into a 
well-known algorithmic pattern (graph traversal)?"

═══════════════════════════════════════════════════════════════════════════
PART 9: COMPARISON OF ALL APPROACHES
═══════════════════════════════════════════════════════════════════════════

Approach          Time           Space   Implementation   Interview Rating
-------------------------------------------------------------------------
DFS              O(Q*(V+E))     O(V+E)  Easy            ⭐⭐⭐⭐⭐ BEST
BFS              O(Q*(V+E))     O(V+E)  Easy            ⭐⭐⭐⭐⭐ BEST
Union-Find       O((E+Q)*α(V))  O(V)    Hard            ⭐⭐⭐⭐ ADVANCED
Floyd-Warshall   O(V³+Q)        O(V²)   Medium          ⭐⭐⭐ OVERKILL
DFS+Backtrack    O(Q*V!)        O(V+E)  Medium          ⭐⭐ TOO SLOW

Recommendation:
- Primary: DFS (Solution 1) - intuitive, clean, correct
- Mention: Union-Find for optimization with many queries
- Mention: Floyd-Warshall if Q >> V³

═══════════════════════════════════════════════════════════════════════════
PART 10: FOLLOW-UP QUESTIONS & ANSWERS
═══════════════════════════════════════════════════════════════════════════

Q1: "What if there are contradictory equations?"
A: "We'd need to detect cycles with inconsistent products. During graph 
   construction, if we find an alternate path between two nodes, verify 
   the products match. If not, return error."

```python
def has_contradiction(graph):
    for start in graph:
        visited = {start: 1.0}
        queue = [(start, 1.0)]
        
        while queue:
            node, product = queue.pop()
            for neighbor, weight in graph[node].items():
                new_product = product * weight
                if neighbor in visited:
                    if abs(visited[neighbor] - new_product) > 1e-5:
                        return True  # Contradiction!
                else:
                    visited[neighbor] = new_product
                    queue.append((neighbor, new_product))
    return False
```

Q2: "What if we have millions of queries?"
A: "Use Floyd-Warshall to precompute all pairs: O(V³) preprocessing, then 
   O(1) per query. Only worth it if Q >> V³. Or use Union-Find for 
   O((E+Q)*α(V)) total time."

Q3: "How would you handle updates (adding new equations)?"
A: "For DFS/BFS: just add edges to graph - O(1) per update.
   For Union-Find: union the new pair - O(α(V)) per update.
   For Floyd-Warshall: rerun algorithm or update incrementally - expensive."

Q4: "What about finding ALL paths between two variables?"
A: "Modify DFS to not mark as visited until backtrack. Store all valid 
   paths. But note: in a valid equation system, all paths should give 
   same answer!"

Q5: "How to handle very large or very small numbers (numerical stability)?"
A: "Use logarithms: log(a/b) = log(a) - log(b). Store log values as weights,
   then multiply becomes add. More numerically stable for extreme values."

```python
# Log-based approach
graph[a][b] = math.log(value)
graph[b][a] = -math.log(value)

# In DFS, add instead of multiply
result = weight + dfs(neighbor, end, visited)

# Final answer: exponentiate
return math.exp(result)
```

Q6: "What if equations involve more than two variables (e.g., a/b/c)?"
A: "Break down into pairs: a/b/c = (a/b) / c. Create intermediate results
   and add to graph. Or extend graph to hyperedges (more complex)."

═══════════════════════════════════════════════════════════════════════════
PART 11: KEY TALKING POINTS DURING INTERVIEW
═══════════════════════════════════════════════════════════════════════════

Opening (show insight):
"I immediately recognize this as a graph problem. Divisions form relationships
that can be represented as weighted directed edges."

Middle (show understanding):
"The key insight is that finding x/y is equivalent to finding a path from x
to y and multiplying the edge weights. This leverages transitivity of 
division: (a/b) × (b/c) = a/c."

Implementation:
"I'm using DFS because it's clean and intuitive. For each query, I do a 
graph traversal from the dividend to divisor, accumulating the product of 
weights along the path."

Edge cases:
"Important cases: variables not in graph return -1, same variable returns 1,
and disconnected components return -1."

Optimization:
"If we had many more queries than variables, I'd use Floyd-Warshall to 
precompute all pairs, or Union-Find for better amortized complexity."
"""
