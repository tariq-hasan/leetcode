"""
LeetCode 1306: Jump Game III

Problem:
Given an array of non-negative integers arr, you are initially positioned at start index.
When at index i, you can jump to i + arr[i] or i - arr[i].
Check if you can reach any index with value 0.

Key Insight: This is graph traversal (BFS/DFS) where each index is a node,
and edges exist from i to i+arr[i] and i-arr[i] if they're in bounds.

Constraints:
- 1 <= arr.length <= 5 * 10^4
- 0 <= arr[i] < arr.length
- 0 <= start < arr.length
"""

# Solution 1: BFS (Most Intuitive) - BEST FOR INTERVIEWS
# Time: O(n), Space: O(n)
from collections import deque

class Solution:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        BFS to explore all reachable indices.
        Clean, easy to explain, and naturally avoids revisiting.
        """
        n = len(arr)
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            idx = queue.popleft()
            
            # Check if we reached a zero
            if arr[idx] == 0:
                return True
            
            # Try both jumps: forward and backward
            for next_idx in [idx + arr[idx], idx - arr[idx]]:
                # Check if in bounds and not visited
                if 0 <= next_idx < n and next_idx not in visited:
                    visited.add(next_idx)
                    queue.append(next_idx)
        
        return False


# Solution 2: DFS Recursive (Clean & Elegant)
# Time: O(n), Space: O(n)
class Solution2:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        Recursive DFS - very clean code.
        Mark visited by setting values to -1 (in-place).
        """
        n = len(arr)
        
        def dfs(idx):
            # Base cases
            if idx < 0 or idx >= n or arr[idx] < 0:
                return False
            
            if arr[idx] == 0:
                return True
            
            # Mark as visited (negative means visited)
            jump = arr[idx]
            arr[idx] = -1
            
            # Try both directions
            result = dfs(idx + jump) or dfs(idx - jump)
            
            # Optional: restore value (not necessary for this problem)
            # arr[idx] = jump
            
            return result
        
        return dfs(start)


# Solution 3: DFS with Visited Set (More Explicit)
# Time: O(n), Space: O(n)
class Solution3:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        DFS with explicit visited set.
        Doesn't modify input array.
        """
        visited = set()
        
        def dfs(idx):
            # Out of bounds or already visited
            if idx < 0 or idx >= len(arr) or idx in visited:
                return False
            
            # Found zero
            if arr[idx] == 0:
                return True
            
            visited.add(idx)
            
            # Explore both jumps
            return dfs(idx + arr[idx]) or dfs(idx - arr[idx])
        
        return dfs(start)


# Solution 4: DFS Iterative (Using Stack)
# Time: O(n), Space: O(n)
class Solution4:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        Iterative DFS using stack.
        Good alternative to avoid recursion depth issues.
        """
        n = len(arr)
        visited = set()
        stack = [start]
        
        while stack:
            idx = stack.pop()
            
            # Check if already visited or out of bounds
            if idx < 0 or idx >= n or idx in visited:
                continue
            
            # Found zero
            if arr[idx] == 0:
                return True
            
            visited.add(idx)
            
            # Add both possible jumps to stack
            stack.append(idx + arr[idx])
            stack.append(idx - arr[idx])
        
        return False


# Solution 5: BFS with In-place Marking (Space Optimized)
# Time: O(n), Space: O(n) for queue, but no separate visited set
class Solution5:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        BFS with in-place marking to save space.
        Mark visited by negating values.
        """
        n = len(arr)
        queue = deque([start])
        
        while queue:
            idx = queue.popleft()
            
            # Check bounds
            if idx < 0 or idx >= n or arr[idx] < 0:
                continue
            
            # Found zero
            if arr[idx] == 0:
                return True
            
            # Mark as visited and get jump distance
            jump = arr[idx]
            arr[idx] = -arr[idx] - 1  # Negate (handle 0 specially)
            
            # Add both directions
            queue.append(idx + jump)
            queue.append(idx - jump)
        
        return False


# Solution 6: Union-Find (Overkill but Creative)
# Time: O(n * α(n)), Space: O(n)
class Solution6:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        Union-Find approach - connects reachable indices.
        Interesting but overkill for this problem.
        """
        n = len(arr)
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Union all reachable pairs
        visited = [False] * n
        queue = deque([start])
        visited[start] = True
        
        while queue:
            idx = queue.popleft()
            
            for next_idx in [idx + arr[idx], idx - arr[idx]]:
                if 0 <= next_idx < n:
                    union(idx, next_idx)
                    if not visited[next_idx]:
                        visited[next_idx] = True
                        queue.append(next_idx)
        
        # Check if any zero is reachable from start
        start_root = find(start)
        for i in range(n):
            if arr[i] == 0 and find(i) == start_root:
                return True
        
        return False


# Solution 7: BFS with Early Termination (Optimized)
# Time: O(n), Space: O(n)
class Solution7:
    def canReach(self, arr: list[int], start: int) -> bool:
        """
        BFS with optimization: check for zero before adding to queue.
        """
        n = len(arr)
        
        # Quick check: is start already zero?
        if arr[start] == 0:
            return True
        
        visited = {start}
        queue = deque([start])
        
        while queue:
            idx = queue.popleft()
            
            # Try both jumps
            for next_idx in [idx + arr[idx], idx - arr[idx]]:
                if 0 <= next_idx < n and next_idx not in visited:
                    # Early termination: found zero
                    if arr[next_idx] == 0:
                        return True
                    
                    visited.add(next_idx)
                    queue.append(next_idx)
        
        return False


# Test cases
def test():
    sol = Solution()
    sol2 = Solution2()
    sol3 = Solution3()
    
    # Test case 1: Can reach zero
    arr = [4,2,3,0,3,1,2]
    start = 5
    print(f"Test 1 (BFS): {sol.canReach(arr.copy(), start)}")  # True
    print(f"Test 1 (DFS): {sol2.canReach(arr.copy(), start)}")  # True
    print(f"Path: 5 -> 4 -> 1 -> 3 (value=0) ✓")
    
    # Test case 2: Cannot reach zero
    arr = [4,2,3,0,3,1,2]
    start = 0
    print(f"\nTest 2 (BFS): {sol.canReach(arr.copy(), start)}")  # False
    print(f"Test 2 (DFS): {sol2.canReach(arr.copy(), start)}")  # False
    
    # Test case 3: Start at zero
    arr = [3,0,2,1,2]
    start = 2
    print(f"\nTest 3 (BFS): {sol.canReach(arr.copy(), start)}")  # False
    print(f"Test 3 (DFS): {sol2.canReach(arr.copy(), start)}")  # False
    
    # Test case 4: Single element zero
    arr = [0]
    start = 0
    print(f"\nTest 4 (BFS): {sol.canReach(arr.copy(), start)}")  # True
    
    # Test case 5: Can reach with backward jump
    arr = [3,0,1]
    start = 2
    print(f"\nTest 5 (BFS): {sol.canReach(arr.copy(), start)}")  # True
    print(f"Path: 2 -> 1 (value=0) ✓")
    
    # Test case 6: Complex path
    arr = [0,3,0,1,3,0,2]
    start = 3
    print(f"\nTest 6 (BFS): {sol.canReach(arr.copy(), start)}")  # True
    
    # Visualize Test 1
    print("\n" + "="*50)
    print("Visualization of Test 1:")
    print("arr = [4,2,3,0,3,1,2], start = 5")
    print("\nIndices: 0  1  2  3  4  5  6")
    print("Values:  4  2  3  0  3  1  2")
    print("         ^           ^     ^")
    print("         |           |     start")
    print("         |           zero")
    print("\nPath: 5 -> 5+1=6 (dead end)")
    print("      5 -> 5-1=4 -> 4+3=7 (out of bounds)")
    print("      5 -> 5-1=4 -> 4-3=1 -> 1+2=3 (FOUND ZERO!) ✓")

if __name__ == "__main__":
    test()
