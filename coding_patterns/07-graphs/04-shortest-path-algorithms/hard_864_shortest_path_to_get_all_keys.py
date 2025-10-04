"""
LeetCode 864: Shortest Path to Get All Keys

Problem:
Given a 2D grid where:
- '@' is the starting position
- '#' is a wall
- '.' is an empty space
- Lowercase letters 'a'-'f' are keys
- Uppercase letters 'A'-'F' are locks (need corresponding key)

Find the shortest path that collects all keys. Return -1 if impossible.

Key Insight: BFS with state = (row, col, keys_collected)
State space: O(m * n * 2^k) where k = number of keys (max 6)

Constraints:
- m, n <= 30
- 1 <= number of keys <= 6
"""

# Solution 1: BFS with Bitmask State - OPTIMAL & BEST FOR INTERVIEWS
# Time: O(m * n * 2^k), Space: O(m * n * 2^k)
from collections import deque

class Solution:
    def shortestPathAllKeys(self, grid: list[str]) -> int:
        """
        BFS with state tracking using bitmask for collected keys.
        State = (row, col, keys_bitmask)
        
        Why bitmask? Efficiently represent which keys we have.
        If 3 keys (a,b,c): 
          - 0b000 = no keys
          - 0b101 = have keys a and c
          - 0b111 = have all keys (target state)
        """
        m, n = len(grid), len(grid[0])
        
        # Find starting position and count total keys
        start_r = start_c = 0
        total_keys = 0
        
        for r in range(m):
            for c in range(n):
                if grid[r][c] == '@':
                    start_r, start_c = r, c
                elif grid[r][c].islower():
                    total_keys += 1
        
        # Target: all keys collected (all bits set)
        all_keys = (1 << total_keys) - 1
        
        # BFS: state = (row, col, keys_bitmask, steps)
        queue = deque([(start_r, start_c, 0, 0)])
        
        # Visited: (row, col, keys) - we might visit same cell with different keys
        visited = set()
        visited.add((start_r, start_c, 0))
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            r, c, keys, steps = queue.popleft()
            
            # Check if we collected all keys
            if keys == all_keys:
                return steps
            
            # Try all 4 directions
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check bounds
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                
                cell = grid[nr][nc]
                
                # Hit a wall
                if cell == '#':
                    continue
                
                new_keys = keys
                
                # Found a key
                if cell.islower():
                    # Add this key to our collection
                    key_bit = ord(cell) - ord('a')
                    new_keys = keys | (1 << key_bit)
                
                # Found a lock
                if cell.isupper():
                    # Check if we have the key
                    key_bit = ord(cell.lower()) - ord('a')
                    if not (keys & (1 << key_bit)):
                        continue  # Don't have the key, can't pass
                
                # Check if this state was visited
                state = (nr, nc, new_keys)
                if state in visited:
                    continue
                
                visited.add(state)
                queue.append((nr, nc, new_keys, steps + 1))
        
        return -1  # Couldn't collect all keys


# Solution 2: BFS with Cleaner Helper Functions
# Time: O(m * n * 2^k), Space: O(m * n * 2^k)
class Solution2:
    def shortestPathAllKeys(self, grid: list[str]) -> int:
        """
        Same algorithm but with helper functions for clarity.
        Good for interviews to show code organization.
        """
        m, n = len(grid), len(grid[0])
        
        def find_start_and_keys():
            """Returns (start_pos, total_keys)."""
            start = None
            keys = 0
            for r in range(m):
                for c in range(n):
                    if grid[r][c] == '@':
                        start = (r, c)
                    elif 'a' <= grid[r][c] <= 'f':
                        keys += 1
            return start, keys
        
        def can_pass(cell, keys_mask):
            """Check if we can pass through this cell."""
            if cell == '#':
                return False
            if cell.isupper():
                # It's a lock, check if we have the key
                key_index = ord(cell) - ord('A')
                return (keys_mask >> key_index) & 1
            return True
        
        def get_new_keys(cell, current_keys):
            """Update keys if we found a new one."""
            if 'a' <= cell <= 'f':
                key_index = ord(cell) - ord('a')
                return current_keys | (1 << key_index)
            return current_keys
        
        start_pos, total_keys = find_start_and_keys()
        target = (1 << total_keys) - 1
        
        queue = deque([(start_pos[0], start_pos[1], 0, 0)])
        visited = {(start_pos[0], start_pos[1], 0)}
        
        while queue:
            r, c, keys, dist = queue.popleft()
            
            if keys == target:
                return dist
            
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < m and 0 <= nc < n:
                    cell = grid[nr][nc]
                    
                    if can_pass(cell, keys):
                        new_keys = get_new_keys(cell, keys)
                        state = (nr, nc, new_keys)
                        
                        if state not in visited:
                            visited.add(state)
                            queue.append((nr, nc, new_keys, dist + 1))
        
        return -1


# Solution 3: A* Search (Advanced Optimization)
# Time: O(m * n * 2^k * log(m*n*2^k)), Space: O(m * n * 2^k)
import heapq

class Solution3:
    def shortestPathAllKeys(self, grid: list[str]) -> int:
        """
        A* search with heuristic = minimum distance to uncollected keys.
        Faster in practice but same worst-case complexity.
        """
        m, n = len(grid), len(grid[0])
        
        # Find start and all key positions
        start = None
        key_positions = {}
        total_keys = 0
        
        for r in range(m):
            for c in range(n):
                if grid[r][c] == '@':
                    start = (r, c)
                elif grid[r][c].islower():
                    key_index = ord(grid[r][c]) - ord('a')
                    key_positions[key_index] = (r, c)
                    total_keys += 1
        
        target = (1 << total_keys) - 1
        
        def heuristic(r, c, keys):
            """Estimate remaining distance: min distance to any uncollected key."""
            if keys == target:
                return 0
            
            min_dist = float('inf')
            for key_idx in range(total_keys):
                if not (keys & (1 << key_idx)):
                    kr, kc = key_positions[key_idx]
                    dist = abs(r - kr) + abs(c - kc)
                    min_dist = min(min_dist, dist)
            
            return min_dist
        
        # Priority queue: (f_score, g_score, r, c, keys)
        # f_score = g_score + heuristic
        heap = [(heuristic(*start, 0), 0, start[0], start[1], 0)]
        visited = {(start[0], start[1], 0): 0}
        
        while heap:
            f, g, r, c, keys = heapq.heappop(heap)
            
            if keys == target:
                return g
            
            # Skip if we've found a better path to this state
            if visited.get((r, c, keys), float('inf')) < g:
                continue
            
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                
                cell = grid[nr][nc]
                
                if cell == '#':
                    continue
                
                if cell.isupper():
                    key_bit = ord(cell) - ord('A')
                    if not (keys & (1 << key_bit)):
                        continue
                
                new_keys = keys
                if cell.islower():
                    key_bit = ord(cell) - ord('a')
                    new_keys = keys | (1 << key_bit)
                
                new_g = g + 1
                state = (nr, nc, new_keys)
                
                if new_g < visited.get(state, float('inf')):
                    visited[state] = new_g
                    new_f = new_g + heuristic(nr, nc, new_keys)
                    heapq.heappush(heap, (new_f, new_g, nr, nc, new_keys))
        
        return -1


# Solution 4: BFS with Optimized Memory (Bidirectional)
# Time: O(m * n * 2^k), Space: O(m * n * 2^k)
class Solution4:
    def shortestPathAllKeys(self, grid: list[str]) -> int:
        """
        Standard BFS but with key insight explanations.
        This is what you'd code in an interview with clear comments.
        """
        m, n = len(grid), len(grid[0])
        start_r = start_c = total_keys = 0
        
        # Find starting position and count keys
        for r in range(m):
            for c in range(n):
                if grid[r][c] == '@':
                    start_r, start_c = r, c
                elif 'a' <= grid[r][c] <= 'f':
                    total_keys += 1
        
        # All keys collected = 2^total_keys - 1
        # Example: 3 keys -> 0b111 = 7
        all_keys = (1 << total_keys) - 1
        
        # BFS initialization
        queue = deque([(start_r, start_c, 0, 0)])  # (row, col, keys_mask, steps)
        visited = set([(start_r, start_c, 0)])
        
        while queue:
            r, c, keys, steps = queue.popleft()
            
            # Goal check: collected all keys
            if keys == all_keys:
                return steps
            
            # Explore 4 directions
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc, nkeys = r + dr, c + dc, keys
                
                # Boundary check
                if nr < 0 or nr >= m or nc < 0 or nc >= n:
                    continue
                
                cell = grid[nr][nc]
                
                # Wall check
                if cell == '#':
                    continue
                
                # Lock check - need corresponding key
                if 'A' <= cell <= 'F':
                    key_needed = ord(cell) - ord('A')
                    if not (keys & (1 << key_needed)):
                        continue  # Don't have the key
                
                # Key collection
                if 'a' <= cell <= 'f':
                    key_index = ord(cell) - ord('a')
                    nkeys |= (1 << key_index)  # Add key to collection
                
                # State deduplication
                if (nr, nc, nkeys) not in visited:
                    visited.add((nr, nc, nkeys))
                    queue.append((nr, nc, nkeys, steps + 1))
        
        return -1


# Test cases
def test():
    sol = Solution()
    sol2 = Solution2()
    
    # Test case 1: Simple path
    grid1 = ["@.a..", "###.#", "b.A.B"]
    print(f"Test 1: {sol.shortestPathAllKeys(grid1)}")  # 8
    print(f"Test 1 (Sol2): {sol2.shortestPathAllKeys(grid1)}")
    
    # Test case 2: Complex maze
    grid2 = ["@..aA", "..B#.", "....b"]
    print(f"\nTest 2: {sol.shortestPathAllKeys(grid2)}")  # 6
    
    # Test case 3: Impossible
    grid3 = ["@...a", ".###A", "b.BCc"]
    print(f"\nTest 3: {sol.shortestPathAllKeys(grid3)}")  # -1
    
    # Test case 4: Single key
    grid4 = ["@Aa"]
    print(f"\nTest 4: {sol.shortestPathAllKeys(grid4)}")  # -1
    
    # Test case 5: Start with all access
    grid5 = ["@.a"]
    print(f"\nTest 5: {sol.shortestPathAllKeys(grid5)}")  # 2
    
    # Visualize Test 1
    print("\n" + "="*60)
    print("Visualization of Test 1:")
    print("@.a..")
    print("###.#")
    print("b.A.B")
    print("\nPath: @ -> a (2 steps) -> b (go down, left, down) = 8 steps")
    print("Need key 'a' to open lock 'A'")
    print("Need key 'b' to open lock 'B'")
    
    # Explain bitmask
    print("\n" + "="*60)
    print("Bitmask Explanation (2 keys: a, b):")
    print("0b00 = no keys")
    print("0b01 = have key 'a'")
    print("0b10 = have key 'b'")
    print("0b11 = have both keys (target!)")
    print("\nState example: (row=1, col=2, keys=0b01)")
    print("Means: at position (1,2) with only key 'a' collected")

if __name__ == "__main__":
    test()
