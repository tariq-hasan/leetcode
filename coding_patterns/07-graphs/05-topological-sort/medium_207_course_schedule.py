"""
LeetCode 207: Course Schedule

Problem:
There are n courses labeled from 0 to n-1. Some courses have prerequisites.
Given:
- numCourses: total number of courses
- prerequisites: array where prerequisites[i] = [ai, bi] means you must take bi before ai

Return true if you can finish all courses, false otherwise.

Key Insight: This is asking "Is the directed graph a DAG?" (Does it have a cycle?)

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
"""

# Solution 1: DFS Cycle Detection (MOST COMMON IN INTERVIEWS)
# Time: O(V + E), Space: O(V + E)
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """
        DFS with three states to detect cycles.
        This is the cleanest and most intuitive approach.
        """
        # Build adjacency list
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        
        # States: 0 = unvisited, 1 = visiting (in current path), 2 = visited
        state = [0] * numCourses
        
        def has_cycle(course):
            """Returns True if cycle detected starting from course."""
            if state[course] == 1:  # Found a back edge (cycle)
                return True
            if state[course] == 2:  # Already fully explored
                return False
            
            # Mark as visiting (in current DFS path)
            state[course] = 1
            
            # Check all prerequisites
            for prereq in graph[course]:
                if has_cycle(prereq):
                    return True
            
            # Mark as visited (fully explored)
            state[course] = 2
            return False
        
        # Check each course for cycles
        for course in range(numCourses):
            if state[course] == 0:  # Not yet visited
                if has_cycle(course):
                    return False
        
        return True


# Solution 2: BFS Topological Sort (Kahn's Algorithm) - ALSO VERY POPULAR
# Time: O(V + E), Space: O(V + E)
from collections import deque

class Solution2:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """
        Kahn's algorithm: Remove nodes with no incoming edges iteratively.
        If we can process all nodes, there's no cycle.
        """
        # Build adjacency list and in-degree array
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course)  # prereq -> course
            in_degree[course] += 1
        
        # Start with courses that have no prerequisites
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        processed = 0
        
        while queue:
            prereq = queue.popleft()
            processed += 1
            
            # Remove this course and update in-degrees
            for course in graph[prereq]:
                in_degree[course] -= 1
                if in_degree[course] == 0:
                    queue.append(course)
        
        # If we processed all courses, no cycle exists
        return processed == numCourses


# Solution 3: DFS with Visited Set (Alternative DFS approach)
# Time: O(V + E), Space: O(V + E)
class Solution3:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """
        DFS tracking current path with a set.
        Slightly different implementation style.
        """
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        
        visited = set()  # Globally visited
        
        def dfs(course, path):
            """
            Returns False if cycle detected.
            path: set of courses in current DFS path
            """
            if course in path:  # Cycle detected
                return False
            if course in visited:  # Already checked, no cycle
                return True
            
            visited.add(course)
            path.add(course)
            
            for prereq in graph[course]:
                if not dfs(prereq, path):
                    return False
            
            path.remove(course)  # Backtrack
            return True
        
        for course in range(numCourses):
            if course not in visited:
                if not dfs(course, set()):
                    return False
        
        return True


# Solution 4: DFS with Recursion Stack (More Explicit)
# Time: O(V + E), Space: O(V + E)
class Solution4:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """
        DFS with explicit recursion stack tracking.
        Very clear what's happening at each step.
        """
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        
        WHITE, GRAY, BLACK = 0, 1, 2  # unvisited, visiting, visited
        color = [WHITE] * numCourses
        
        def dfs(node):
            """Returns True if NO cycle found."""
            if color[node] == GRAY:  # Back edge = cycle
                return False
            if color[node] == BLACK:  # Already processed
                return True
            
            color[node] = GRAY  # Mark as visiting
            
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            
            color[node] = BLACK  # Mark as visited
            return True
        
        for course in range(numCourses):
            if color[course] == WHITE:
                if not dfs(course):
                    return False
        
        return True


# Solution 5: Union Find (Less Common, but Good to Know)
# Time: O(E * α(V)), Space: O(V)
class Solution5:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """
        Union-Find to detect cycles.
        Works but requires reversing edges and checking connectivity.
        Less intuitive than DFS/BFS for this problem.
        """
        parent = list(range(numCourses))
        rank = [0] * numCourses
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False  # Already in same set = cycle
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Build reverse graph (for topological order)
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        
        # Process in topological order
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        
        while queue:
            prereq = queue.popleft()
            for course in graph[prereq]:
                if not union(prereq, course):
                    return False
                in_degree[course] -= 1
                if in_degree[course] == 0:
                    queue.append(course)
        
        return True


# Test cases
def test():
    sol = Solution()
    sol2 = Solution2()
    
    # Test case 1: Possible
    numCourses = 2
    prerequisites = [[1,0]]
    print(f"Test 1 (DFS): {sol.canFinish(numCourses, prerequisites)}")  # True
    print(f"Test 1 (BFS): {sol2.canFinish(numCourses, prerequisites)}")  # True
    
    # Test case 2: Cycle exists
    numCourses = 2
    prerequisites = [[1,0],[0,1]]
    print(f"Test 2 (DFS): {sol.canFinish(numCourses, prerequisites)}")  # False
    print(f"Test 2 (BFS): {sol2.canFinish(numCourses, prerequisites)}")  # False
    
    # Test case 3: Complex valid case
    numCourses = 4
    prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    print(f"Test 3 (DFS): {sol.canFinish(numCourses, prerequisites)}")  # True
    print(f"Test 3 (BFS): {sol2.canFinish(numCourses, prerequisites)}")  # True
    
    # Test case 4: Complex cycle
    numCourses = 3
    prerequisites = [[0,1],[1,2],[2,0]]
    print(f"Test 4 (DFS): {sol.canFinish(numCourses, prerequisites)}")  # False
    print(f"Test 4 (BFS): {sol2.canFinish(numCourses, prerequisites)}")  # False
    
    # Test case 5: No prerequisites
    numCourses = 5
    prerequisites = []
    print(f"Test 5 (DFS): {sol.canFinish(numCourses, prerequisites)}")  # True
    print(f"Test 5 (BFS): {sol2.canFinish(numCourses, prerequisites)}")  # True

if __name__ == "__main__":
    test()
