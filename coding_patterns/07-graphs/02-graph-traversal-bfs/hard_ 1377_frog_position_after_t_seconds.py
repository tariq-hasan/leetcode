"""
LeetCode 1377: Frog Position After T Seconds

Problem Statement:
Given an undirected tree consisting of n vertices numbered from 1 to n. 
A frog starts jumping from vertex 1. In one second, the frog jumps from its 
current vertex to another unvisited vertex if they are directly connected. 
The frog cannot jump back to a visited vertex. In case the frog can jump to 
several vertices, it jumps randomly to one of them with the same probability. 
If the frog cannot jump to any unvisited vertex, it stays at the current vertex forever.

Return the probability that after t seconds the frog is on the vertex target.

Constraints:
- 1 <= n <= 100
- edges.length == n - 1
- edges[i].length == 2
- 1 <= ai, bi <= n
- 1 <= t <= 50
- 1 <= target <= n

Key Rules:
1. Frog starts at vertex 1
2. Can only jump to unvisited vertices
3. If multiple choices, equal probability for each
4. If no unvisited neighbors, stays forever at current vertex
5. Cannot revisit vertices

Examples:
Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 2, target = 4
Output: 0.16666666666666666
Explanation: The frog starts at vertex 1, jumping with 1/3 probability to vertex 2 
after second 1 and then jumping with 1/2 probability to vertex 4 after second 2.
Thus the probability = 1/3 * 1/2 = 1/6 ≈ 0.16667

Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 1, target = 7
Output: 0.3333333333333333
Explanation: After 1 second, frog has 1/3 probability to be at vertex 7.
"""

from collections import defaultdict, deque
from typing import List

class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        """
        Solution 1: BFS (Level-by-Level) - Optimal for Interview
        
        Key Insight: Use BFS to simulate frog's movement level by level.
        At each second, calculate probability of reaching each vertex.
        
        Time Complexity: O(min(t, n) * n) = O(t * n) 
        Space Complexity: O(n)
        
        This is the most intuitive and recommended approach for interviews.
        """
        # Build adjacency list representation of tree
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        # BFS queue: (vertex, probability)
        queue = deque([(1, 1.0)])
        visited = [False] * (n + 1)
        visited[1] = True
        
        # Process each second (level in BFS)
        while queue and t >= 0:
            # Process all vertices at current time step
            for _ in range(len(queue)):
                vertex, prob = queue.popleft()
                
                # Count unvisited neighbors
                # For vertex 1, all neighbors are unvisited initially
                # For other vertices, subtract 1 to exclude parent (already visited)
                unvisited_count = len(graph[vertex]) - (0 if vertex == 1 else 1)
                
                # Check if we've reached the target
                if vertex == target:
                    # Two cases where frog stays at target:
                    # 1. No more unvisited neighbors (leaf node or all explored)
                    # 2. Exactly at time t (no more time to move)
                    if unvisited_count == 0 or t == 0:
                        return prob
                    else:
                        # Frog will be forced to move away from target
                        return 0.0
                
                # Add unvisited neighbors to queue with updated probability
                for neighbor in graph[vertex]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        # Probability splits equally among all unvisited neighbors
                        queue.append((neighbor, prob / unvisited_count))
            
            # Move to next second
            t -= 1
        
        # Target not reachable within time limit
        return 0.0

    def frogPosition_dfs(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        """
        Solution 2: DFS (Recursive) - Alternative Approach
        
        Uses DFS to explore all possible paths from start to target.
        More complex to understand but demonstrates recursion skills.
        
        Time Complexity: O(n)
        Space Complexity: O(n) - recursion stack
        """
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def dfs(vertex: int, parent: int, time_left: int) -> float:
            # Get unvisited children (exclude parent)
            children = [child for child in graph[vertex] if child != parent]
            
            # Base case: reached target
            if vertex == target:
                # Can stay at target if no children or no time left
                if len(children) == 0 or time_left == 0:
                    return 1.0
                else:
                    return 0.0  # Must move away from target
            
            # Base case: no time left and not at target
            if time_left == 0:
                return 0.0
            
            # Base case: no children to explore
            if len(children) == 0:
                return 0.0
            
            # Recursively explore children
            total_prob = 0.0
            for child in children:
                # Each child has equal probability of being chosen
                child_prob = dfs(child, vertex, time_left - 1)
                total_prob += child_prob / len(children)
            
            return total_prob
        
        return dfs(1, -1, t)

    def frogPosition_optimized_bfs(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        """
        Solution 3: Optimized BFS - Early Termination
        
        Same as BFS but with optimizations:
        - Early termination when target found
        - Direct path calculation for simple cases
        
        Time Complexity: O(min(t, n) * n)
        Space Complexity: O(n)
        """
        if n == 1:
            return 1.0 if target == 1 else 0.0
        
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        # Special case: target is directly connected to start
        if target in graph[1] and t == 1:
            return 1.0 / len(graph[1])
        
        queue = deque([(1, 1.0)])
        visited = {1}
        
        current_time = 0
        while queue and current_time < t:
            next_queue = deque()
            
            while queue:
                vertex, prob = queue.popleft()
                unvisited_neighbors = [v for v in graph[vertex] if v not in visited]
                
                if vertex == target:
                    if len(unvisited_neighbors) == 0 or current_time == t - 1:
                        return prob
                    else:
                        return 0.0
                
                for neighbor in unvisited_neighbors:
                    visited.add(neighbor)
                    next_queue.append((neighbor, prob / len(unvisited_neighbors)))
            
            queue = next_queue
            current_time += 1
        
        # Check if target is in final queue
        for vertex, prob in queue:
            if vertex == target:
                return prob
        
        return 0.0


# Test cases for verification
def test_solutions():
    solution = Solution()
    
    # Test case 1
    n1, edges1, t1, target1 = 7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 2, 4
    expected1 = 1/6  # 0.16666666666666666
    result1 = solution.frogPosition(n1, edges1, t1, target1)
    print(f"Test 1: Expected {expected1:.6f}, Got {result1:.6f}, {'PASS' if abs(result1 - expected1) < 1e-5 else 'FAIL'}")
    
    # Test case 2
    n2, edges2, t2, target2 = 7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 1, 7
    expected2 = 1/3  # 0.3333333333333333
    result2 = solution.frogPosition(n2, edges2, t2, target2)
    print(f"Test 2: Expected {expected2:.6f}, Got {result2:.6f}, {'PASS' if abs(result2 - expected2) < 1e-5 else 'FAIL'}")
    
    # Test case 3 - Single node
    n3, edges3, t3, target3 = 1, [], 1, 1
    expected3 = 1.0
    result3 = solution.frogPosition(n3, edges3, t3, target3)
    print(f"Test 3: Expected {expected3:.6f}, Got {result3:.6f}, {'PASS' if abs(result3 - expected3) < 1e-5 else 'FAIL'}")
    
    # Test case 4 - Target unreachable in time
    n4, edges4, t4, target4 = 3, [[1,2],[2,3]], 1, 3
    expected4 = 0.0
    result4 = solution.frogPosition(n4, edges4, t4, target4)
    print(f"Test 4: Expected {expected4:.6f}, Got {result4:.6f}, {'PASS' if abs(result4 - expected4) < 1e-5 else 'FAIL'}")
    
    # Test case 5 - Frog must move away from target
    n5, edges5, t5, target5 = 3, [[1,2],[2,3]], 2, 2
    expected5 = 0.0  # Frog reaches 2 at t=1 but must move to 3 at t=2
    result5 = solution.frogPosition(n5, edges5, t5, target5)
    print(f"Test 5: Expected {expected5:.6f}, Got {result5:.6f}, {'PASS' if abs(result5 - expected5) < 1e-5 else 'FAIL'}")
    
    # Test DFS solution
    print("\nTesting DFS solution:")
    result_dfs = solution.frogPosition_dfs(n1, edges1, t1, target1)
    print(f"DFS Test 1: Expected {expected1:.6f}, Got {result_dfs:.6f}, {'PASS' if abs(result_dfs - expected1) < 1e-5 else 'FAIL'}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW DISCUSSION POINTS:

1. Problem Understanding:
   - Tree structure (n-1 edges, no cycles)
   - Frog starts at vertex 1
   - Cannot revisit vertices
   - Equal probability when multiple choices
   - Stays forever when no unvisited neighbors

2. Key Insights:
   - BFS naturally models time progression (level = second)
   - Probability calculation: current_prob / number_of_choices
   - Two stopping conditions: no unvisited neighbors OR time runs out
   - Critical case: frog reaches target but still has time and neighbors

3. Algorithm Choice:
   - BFS is optimal for this time-based simulation
   - DFS can work but is more complex to reason about
   - Level-by-level processing matches the problem's time constraint

4. Edge Cases:
   - Single node tree (n=1)
   - Target is starting vertex (vertex 1)
   - Target unreachable within time limit
   - Frog reaches target but must move away (has unvisited neighbors and time left)
   - Leaf node targets (frog stays forever once reached)

5. Probability Calculation:
   - Start with probability 1.0 at vertex 1
   - At each step, divide probability by number of unvisited neighbors
   - Accumulate probabilities for paths leading to target

6. Implementation Details:
   - Use adjacency list for tree representation
   - Track visited vertices to avoid cycles
   - Handle parent-child relationship (subtract 1 from neighbor count for non-root)
   - Queue stores (vertex, probability) pairs

7. Complexity Analysis:
   - Time: O(t * n) - process at most min(t, n) levels, each level processes O(n) vertices
   - Space: O(n) - adjacency list, queue, and visited array

8. Follow-up Questions:
   - What if frog could revisit vertices?
   - What if different edges had different probabilities?
   - How to handle multiple frogs?
   - What if we wanted all probabilities after t seconds?

9. Common Mistakes:
   - Forgetting that frog must move if it has unvisited neighbors and time
   - Not handling the parent-child relationship correctly
   - Miscalculating probability distribution
   - Not considering the "stays forever" rule
"""
