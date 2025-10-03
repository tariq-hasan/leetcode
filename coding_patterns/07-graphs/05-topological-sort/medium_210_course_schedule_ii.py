"""
LeetCode 210: Course Schedule II

Problem:
There are n courses labeled from 0 to n-1. Some courses have prerequisites.
Given:
- numCourses: total number of courses
- prerequisites: array where prerequisites[i] = [ai, bi] means you must take bi before ai

Return the ordering of courses you should take to finish all courses.
If there are multiple valid orderings, return any of them.
If it's impossible to finish all courses, return an empty array.

Key Insight: This is topological sort of a DAG. If cycle exists, return [].

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
"""

# Solution 1: BFS Topological Sort (Kahn's Algorithm) - BEST FOR THIS PROBLEM
# Time: O(V + E), Space: O(V + E)
from collections import deque, defaultdict

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        Kahn's algorithm - Most intuitive for returning topological order.
        Process nodes with no incoming edges, naturally gives us the order.
        """
        # Build adjacency list and in-degree array
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course)  # prereq must come before course
            in_degree[course] += 1
        
        # Start with courses that have no prerequisites
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        order = []
        
        while queue:
            course = queue.popleft()
            order.append(course)
            
            # Remove this course and update in-degrees
            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        # If we processed all courses, return order; otherwise cycle exists
        return order if len(order) == numCourses else []


# Solution 2: DFS Topological Sort (Postorder) - ALSO EXCELLENT
# Time: O(V + E), Space: O(V + E)
class Solution2:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        DFS with reverse postorder gives topological sort.
        Add to result when finishing a node (postorder), then reverse.
        """
        # Build adjacency list
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        
        # States: 0 = unvisited, 1 = visiting, 2 = visited
        state = [0] * numCourses
        order = []
        
        def dfs(course):
            """Returns False if cycle detected."""
            if state[course] == 1:  # Cycle detected
                return False
            if state[course] == 2:  # Already processed
                return True
            
            state[course] = 1  # Mark as visiting
            
            # Visit all prerequisites first
            for prereq in graph[course]:
                if not dfs(prereq):
                    return False
            
            state[course] = 2  # Mark as visited
            order.append(course)  # Add in postorder
            return True
        
        # Try to visit all courses
        for course in range(numCourses):
            if state[course] == 0:
                if not dfs(course):
                    return []
        
        # Order is already in correct topological order (no need to reverse!)
        # because we built graph as course -> prereq
        return order


# Solution 3: DFS with Traditional Graph Direction
# Time: O(V + E), Space: O(V + E)
class Solution3:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        DFS with graph in prereq -> course direction.
        Results in reverse postorder (need to reverse at end).
        """
        # Build adjacency list (prereq -> course)
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * numCourses
        order = []
        
        def dfs(node):
            """Returns False if cycle detected."""
            if color[node] == GRAY:
                return False
            if color[node] == BLACK:
                return True
            
            color[node] = GRAY
            
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            
            color[node] = BLACK
            order.append(node)  # Postorder
            return True
        
        for course in range(numCourses):
            if color[course] == WHITE:
                if not dfs(course):
                    return []
        
        # Reverse postorder gives topological order
        return order[::-1]


# Solution 4: BFS with Explicit Level Processing
# Time: O(V + E), Space: O(V + E)
class Solution4:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        Kahn's algorithm with level-by-level processing.
        More verbose but very clear what's happening.
        """
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        
        # Initialize with all courses having no prerequisites
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
        
        order = []
        
        while queue:
            # Process one level at a time (not necessary but shows structure)
            level_size = len(queue)
            
            for _ in range(level_size):
                course = queue.popleft()
                order.append(course)
                
                # Reduce in-degree of dependent courses
                for dependent in graph[course]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        return order if len(order) == numCourses else []


# Solution 5: DFS Iterative (No Recursion)
# Time: O(V + E), Space: O(V + E)
class Solution5:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        Iterative DFS to avoid recursion stack overflow.
        Good for very deep graphs.
        """
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * numCourses
        order = []
        
        for start in range(numCourses):
            if color[start] != WHITE:
                continue
            
            stack = [start]
            
            while stack:
                node = stack[-1]
                
                if color[node] == BLACK:
                    stack.pop()
                    continue
                
                if color[node] == GRAY:
                    # Finished processing all children
                    color[node] = BLACK
                    order.append(node)
                    stack.pop()
                    continue
                
                # First time seeing this node
                color[node] = GRAY
                
                # Check for cycles and add children
                has_cycle = False
                for neighbor in graph[node]:
                    if color[neighbor] == GRAY:
                        return []  # Cycle detected
                    if color[neighbor] == WHITE:
                        stack.append(neighbor)
        
        return order[::-1]


# Test cases
def test():
    sol = Solution()
    sol2 = Solution2()
    
    # Test case 1: Simple linear dependency
    numCourses = 2
    prerequisites = [[1,0]]
    result1 = sol.findOrder(numCourses, prerequisites)
    result2 = sol2.findOrder(numCourses, prerequisites)
    print(f"Test 1 (BFS): {result1}")  # [0, 1]
    print(f"Test 1 (DFS): {result2}")  # [0, 1]
    
    # Test case 2: Cycle exists
    numCourses = 2
    prerequisites = [[1,0],[0,1]]
    result1 = sol.findOrder(numCourses, prerequisites)
    result2 = sol2.findOrder(numCourses, prerequisites)
    print(f"Test 2 (BFS): {result1}")  # []
    print(f"Test 2 (DFS): {result2}")  # []
    
    # Test case 3: Complex valid case
    numCourses = 4
    prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    result1 = sol.findOrder(numCourses, prerequisites)
    result2 = sol2.findOrder(numCourses, prerequisites)
    print(f"Test 3 (BFS): {result1}")  # [0,1,2,3] or [0,2,1,3]
    print(f"Test 3 (DFS): {result2}")  # Valid ordering
    
    # Test case 4: No prerequisites
    numCourses = 3
    prerequisites = []
    result1 = sol.findOrder(numCourses, prerequisites)
    result2 = sol2.findOrder(numCourses, prerequisites)
    print(f"Test 4 (BFS): {result1}")  # [0,1,2] or any permutation
    print(f"Test 4 (DFS): {result2}")  # Valid ordering
    
    # Test case 5: Multiple dependencies
    numCourses = 6
    prerequisites = [[1,0],[2,0],[3,1],[3,2],[4,3],[5,3]]
    result1 = sol.findOrder(numCourses, prerequisites)
    result2 = sol2.findOrder(numCourses, prerequisites)
    print(f"Test 5 (BFS): {result1}")  # Valid ordering
    print(f"Test 5 (DFS): {result2}")  # Valid ordering
    
    # Verify result is valid
    def is_valid_order(order, numCourses, prerequisites):
        if len(order) != numCourses:
            return False
        position = {course: i for i, course in enumerate(order)}
        for course, prereq in prerequisites:
            if position[prereq] >= position[course]:
                return False
        return True
    
    print(f"\nTest 5 BFS valid: {is_valid_order(result1, numCourses, prerequisites)}")
    print(f"Test 5 DFS valid: {is_valid_order(result2, numCourses, prerequisites)}")

if __name__ == "__main__":
    test()
