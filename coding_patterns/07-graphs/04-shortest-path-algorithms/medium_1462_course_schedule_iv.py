"""
LeetCode 1462: Course Schedule IV

Problem:
There are n courses labeled from 0 to n-1. Some courses have prerequisites.
Given:
- n: number of courses
- prerequisites: array where prerequisites[i] = [ai, bi] means you must take ai before bi
- queries: array where queries[j] = [uj, vj] asking if uj is a prerequisite of vj

Return a boolean array where answer[j] is true if uj is a prerequisite of vj.

Constraints:
- 2 <= n <= 100
- 0 <= prerequisites.length <= (n * (n - 1) / 2)
- 0 <= queries.length <= 10^4
"""

# Solution 1: Floyd-Warshall (Transitive Closure) - BEST FOR INTERVIEWS
# Time: O(n^3 + q), Space: O(n^2)
class Solution:
    def checkIfPrerequisite(self, n: int, prerequisites: list[list[int]], 
                           queries: list[list[int]]) -> list[bool]:
        """
        Floyd-Warshall to compute transitive closure of prerequisite graph.
        This finds ALL prerequisite relationships efficiently.
        """
        # Build reachability matrix
        # reachable[i][j] = True means i is a prerequisite of j
        reachable = [[False] * n for _ in range(n)]
        
        # Mark direct prerequisites
        for pre, course in prerequisites:
            reachable[pre][course] = True
        
        # Floyd-Warshall: if i->k and k->j, then i->j
        # k is the intermediate course
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # If i can reach k AND k can reach j, then i can reach j
                    if reachable[i][k] and reachable[k][j]:
                        reachable[i][j] = True
        
        # Answer queries using precomputed reachability
        return [reachable[u][v] for u, v in queries]


# Solution 2: DFS with Memoization
# Time: O(n^2 + q) worst case, Space: O(n^2)
from collections import defaultdict

class Solution2:
    def checkIfPrerequisite(self, n: int, prerequisites: list[list[int]], 
                           queries: list[list[int]]) -> list[bool]:
        """
        DFS from each course to find all prerequisites.
        Efficient when prerequisites are sparse.
        """
        # Build adjacency list (prerequisite -> courses that need it)
        graph = defaultdict(list)
        for pre, course in prerequisites:
            graph[pre].append(course)
        
        # For each course, store all its prerequisites
        all_prereqs = [set() for _ in range(n)]
        
        def dfs(course):
            """Find all prerequisites for a course (memoized)."""
            if all_prereqs[course]:  # Already computed
                return all_prereqs[course]
            
            # Get prerequisites from all direct prerequisites
            for prereq_course in graph:
                if course in graph[prereq_course]:
                    # prereq_course is a direct prerequisite
                    all_prereqs[course].add(prereq_course)
                    # Add all of prereq_course's prerequisites transitively
                    all_prereqs[course].update(dfs(prereq_course))
            
            return all_prereqs[course]
        
        # Compute prerequisites for all courses
        for i in range(n):
            dfs(i)
        
        # Answer queries
        return [u in all_prereqs[v] for u, v in queries]


# Solution 3: Topological Sort with BFS (Optimized)
# Time: O(n * (n + E) + q), Space: O(n^2)
from collections import deque

class Solution3:
    def checkIfPrerequisite(self, n: int, prerequisites: list[list[int]], 
                           queries: list[list[int]]) -> list[bool]:
        """
        Process courses in topological order, propagating prerequisites.
        This is efficient and intuitive for DAG problems.
        """
        # Build graph and in-degree
        graph = defaultdict(list)
        in_degree = [0] * n
        
        for pre, course in prerequisites:
            graph[pre].append(course)
            in_degree[course] += 1
        
        # Track all prerequisites for each course
        prereqs = [set() for _ in range(n)]
        
        # Add direct prerequisites
        for pre, course in prerequisites:
            prereqs[course].add(pre)
        
        # Topological sort with BFS (Kahn's algorithm)
        queue = deque([i for i in range(n) if in_degree[i] == 0])
        
        while queue:
            course = queue.popleft()
            
            # Process all courses that depend on this course
            for next_course in graph[course]:
                # Propagate: next_course inherits all prerequisites of course
                prereqs[next_course].add(course)
                prereqs[next_course].update(prereqs[course])
                
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        # Answer queries
        return [u in prereqs[v] for u, v in queries]


# Solution 4: DFS Query-by-Query (Simple but Less Efficient)
# Time: O(q * (n + E)), Space: O(n)
class Solution4:
    def checkIfPrerequisite(self, n: int, prerequisites: list[list[int]], 
                           queries: list[list[int]]) -> list[bool]:
        """
        For each query, run DFS to check if path exists.
        Good when q is small, but inefficient for many queries.
        """
        # Build adjacency list
        graph = defaultdict(list)
        for pre, course in prerequisites:
            graph[pre].append(course)
        
        def can_reach(start, target):
            """Check if we can reach target from start."""
            if start == target:
                return True
            
            visited = set()
            stack = [start]
            
            while stack:
                node = stack.pop()
                if node == target:
                    return True
                
                if node in visited:
                    continue
                visited.add(node)
                
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            
            return False
        
        return [can_reach(u, v) for u, v in queries]


# Test cases
def test():
    sol = Solution()
    
    # Test case 1
    n = 2
    prerequisites = [[1,0]]
    queries = [[0,1],[1,0]]
    result = sol.checkIfPrerequisite(n, prerequisites, queries)
    print(f"Test 1: {result}")  # Expected: [False, True]
    
    # Test case 2
    n = 3
    prerequisites = [[1,2],[1,0],[2,0]]
    queries = [[1,0],[1,2]]
    result = sol.checkIfPrerequisite(n, prerequisites, queries)
    print(f"Test 2: {result}")  # Expected: [True, True]
    
    # Test case 3: Transitive case
    n = 5
    prerequisites = [[0,1],[1,2],[2,3],[3,4]]
    queries = [[0,4],[4,0],[1,3],[3,0]]
    result = sol.checkIfPrerequisite(n, prerequisites, queries)
    print(f"Test 3: {result}")  # Expected: [True, False, True, False]
    
    # Test case 4: Complex graph
    n = 4
    prerequisites = [[2,3],[2,1],[0,3],[0,1]]
    queries = [[0,1],[0,3],[2,3],[3,0],[2,0],[0,2]]
    result = sol.checkIfPrerequisite(n, prerequisites, queries)
    print(f"Test 4: {result}")  # Expected: [True, True, True, False, False, False]

if __name__ == "__main__":
    test()
