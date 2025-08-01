"""
LeetCode 841: Keys and Rooms

Problem Statement:
There are n rooms labeled from 0 to n - 1 and all the rooms are locked except for room 0. 
Your goal is to visit all the rooms. However, you cannot enter a locked room without having its key.

When you visit a room, you may find a set of distinct keys in it. Each key has a number on it, 
denoting which room it unlocks, and you can take all of them with you to unlock the other rooms.

Given an array rooms where rooms[i] is the set of keys that you can obtain if you visited room i, 
return true if you can visit all the rooms, or false otherwise.

Example 1:
Input: rooms = [[1],[2],[3],[]]
Output: true
Explanation: We start in room 0 and pick up key 1.
We then go to room 1 and pick up key 2.
We then go to room 2 and pick up key 3.
We then go to room 3.
Since we were able to go to every room, we return true.

Example 2:
Input: rooms = [[1,3],[3,0,1],[2],[0]]
Output: false
Explanation: We can not enter room number 2 since the only key that unlocks it is in that room.

Constraints:
- n == rooms.length
- 2 <= n <= 1000
- 0 <= rooms[i].length <= 1000
- 0 <= rooms[i][j] < n
- All the values of rooms[i] are unique.
"""

from typing import List
from collections import deque

class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        DFS Solution - Most intuitive and commonly expected in interviews
        Time Complexity: O(n + k) where n is number of rooms, k is total number of keys
        Space Complexity: O(n) for visited set and recursion stack
        """
        n = len(rooms)
        visited = set()
        
        def dfs(room):
            if room in visited:
                return
            
            visited.add(room)
            # Collect keys from current room and visit those rooms
            for key in rooms[room]:
                dfs(key)
        
        # Start from room 0 (always unlocked)
        dfs(0)
        
        # Check if we visited all rooms
        return len(visited) == n

class SolutionOptimalArray:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        Optimized DFS using boolean array - Better performance than set approach
        Time Complexity: O(n + k) - same as set version
        Space Complexity: O(n) - same space but more cache-friendly
        
        Advantages:
        1. Faster O(1) access vs O(1) average for set
        2. Better cache locality - contiguous memory
        3. Lower memory overhead per element
        4. More predictable performance
        """
        visited = [False] * len(rooms)
        
        def dfs(room):
            if visited[room]:
                return
            
            visited[room] = True
            for key in rooms[room]:
                if not visited[key]:  # Small optimization: check before recursing
                    dfs(key)
        
        dfs(0)
        return all(visited)  # More Pythonic than len(visited) == n equivalent

class SolutionBFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        BFS Solution - Alternative approach using queue
        Time Complexity: O(n + k) where n is number of rooms, k is total number of keys
        Space Complexity: O(n) for visited set and queue
        """
        n = len(rooms)
        visited = set()
        queue = deque([0])  # Start from room 0
        
        while queue:
            room = queue.popleft()
            
            if room in visited:
                continue
                
            visited.add(room)
            
            # Add all rooms we can access with keys from current room
            for key in rooms[room]:
                if key not in visited:
                    queue.append(key)
        
        return len(visited) == n

class SolutionIterativeDFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        Iterative DFS Solution - Avoids recursion stack
        Time Complexity: O(n + k)
        Space Complexity: O(n) for visited set and stack
        """
        n = len(rooms)
        visited = set()
        stack = [0]  # Start from room 0
        
        while stack:
            room = stack.pop()
            
            if room in visited:
                continue
                
            visited.add(room)
            
            # Add all accessible rooms to stack
            for key in rooms[room]:
                if key not in visited:
                    stack.append(key)
        
        return len(visited) == n

class SolutionOptimized:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        Early termination optimization - stops as soon as all rooms are visited
        Time Complexity: O(n + k) but potentially faster in practice
        Space Complexity: O(n)
        """
        n = len(rooms)
        visited = set()
        stack = [0]
        
        while stack and len(visited) < n:  # Early termination
            room = stack.pop()
            
            if room in visited:
                continue
                
            visited.add(room)
            
            # Add unvisited rooms to stack
            for key in rooms[room]:
                if key not in visited:
                    stack.append(key)
        
        return len(visited) == n

# Alternative approach using Union-Find (overkill but shows advanced knowledge)
class SolutionUnionFind:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        Union-Find approach - demonstrates knowledge of different data structures
        Not the most efficient for this problem but shows algorithmic breadth
        """
        n = len(rooms)
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Union all reachable rooms starting from room 0
        visited = set()
        stack = [0]
        
        while stack:
            room = stack.pop()
            if room in visited:
                continue
            visited.add(room)
            
            for key in rooms[room]:
                union(0, key)  # Connect to component containing room 0
                if key not in visited:
                    stack.append(key)
        
        # Check if all rooms are in the same component as room 0
        root = find(0)
        return all(find(i) == root for i in range(n))

# Test cases
def test_solutions():
    solutions = [Solution(), SolutionBFS(), SolutionIterativeDFS(), SolutionOptimized()]
    
    test_cases = [
        ([[1],[2],[3],[]], True),  # Can visit all rooms
        ([[1,3],[3,0,1],[2],[0]], False),  # Cannot reach room 2
        ([[1],[0,2,3],[1],[1]], True),  # Complex connectivity
        ([[]], True),  # Single room
        ([[1,2],[3],[3],[]], True),  # Multiple paths
    ]
    
    for i, (rooms, expected) in enumerate(test_cases):
        print(f"Test case {i + 1}: rooms = {rooms}")
        for j, sol in enumerate(solutions):
            result = sol.canVisitAllRooms(rooms)
            status = "✓" if result == expected else "✗"
            sol_names = ["DFS", "BFS", "Iterative DFS", "Optimized"]
            print(f"  {sol_names[j]}: {result} {status}")
        print()

if __name__ == "__main__":
    test_solutions()

# Java Implementation (commonly requested in big tech interviews)
java_solution = '''
// DFS Recursive Solution - Most Common Interview Answer
class Solution {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        Set<Integer> visited = new HashSet<>();
        dfs(rooms, 0, visited);
        return visited.size() == rooms.size();
    }
    
    private void dfs(List<List<Integer>> rooms, int room, Set<Integer> visited) {
        if (visited.contains(room)) return;
        
        visited.add(room);
        for (int key : rooms.get(room)) {
            dfs(rooms, key, visited);
        }
    }
}

// BFS Solution
class SolutionBFS {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        Set<Integer> visited = new HashSet<>();
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(0);
        
        while (!queue.isEmpty()) {
            int room = queue.poll();
            if (visited.contains(room)) continue;
            
            visited.add(room);
            for (int key : rooms.get(room)) {
                if (!visited.contains(key)) {
                    queue.offer(key);
                }
            }
        }
        
        return visited.size() == rooms.size();
    }
}

// Iterative DFS Solution
class SolutionIterative {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> stack = new Stack<>();
        stack.push(0);
        
        while (!stack.isEmpty()) {
            int room = stack.pop();
            if (visited.contains(room)) continue;
            
            visited.add(room);
            for (int key : rooms.get(room)) {
                if (!visited.contains(key)) {
                    stack.push(key);
                }
            }
        }
        
        return visited.size() == rooms.size();
    }
}
'''

# C++ Implementation for completeness
cpp_solution = '''
// DFS Recursive Solution
class Solution {
public:
    bool canVisitAllRooms(vector<vector<int>>& rooms) {
        unordered_set<int> visited;
        dfs(rooms, 0, visited);
        return visited.size() == rooms.size();
    }
    
private:
    void dfs(vector<vector<int>>& rooms, int room, unordered_set<int>& visited) {
        if (visited.count(room)) return;
        
        visited.insert(room);
        for (int key : rooms[room]) {
            dfs(rooms, key, visited);
        }
    }
};

// BFS Solution
class SolutionBFS {
public:
    bool canVisitAllRooms(vector<vector<int>>& rooms) {
        unordered_set<int> visited;
        queue<int> q;
        q.push(0);
        
        while (!q.empty()) {
            int room = q.front();
            q.pop();
            
            if (visited.count(room)) continue;
            
            visited.insert(room);
            for (int key : rooms[room]) {
                if (!visited.count(key)) {
                    q.push(key);
                }
            }
        }
        
        return visited.size() == rooms.size();
    }
};
'''

"""
Key Interview Points:

1. **Problem Recognition**: This is a graph traversal problem where:
   - Rooms are nodes
   - Keys represent edges (directed graph)
   - Goal: check if all nodes are reachable from node 0

2. **Algorithm Choice**: 
   - DFS is most intuitive and natural for this problem
   - BFS works equally well and might be preferred for shortest path variants
   - Both have same time/space complexity

3. **Implementation Details**:
   - Always start from room 0 (given as unlocked)
   - Use visited set to avoid cycles and redundant visits
   - Return len(visited) == n to check if all rooms were visited

4. **Edge Cases**:
   - Single room (trivially true)
   - No keys in any room
   - Self-referencing keys (room contains key to itself)
   - Disconnected components

5. **Optimization Opportunities**:
   - Early termination when all rooms visited
   - Avoid adding already visited rooms to queue/stack

6. **Time/Space Complexity**:
   - Time: O(n + k) where n = rooms, k = total keys
   - Space: O(n) for visited set + O(n) for recursion/stack

7. **Follow-up Questions**:
   - What if we need to find the minimum number of keys to collect?
   - How would you modify for weighted edges?
   - Can you solve without extra space for visited set? (modify input array)

8. **Common Mistakes**:
   - Forgetting to start from room 0
   - Not handling cycles properly
   - Incorrect termination condition

The DFS recursive solution is typically what interviewers expect first,
followed by discussion of BFS alternative and potential optimizations.
"""
