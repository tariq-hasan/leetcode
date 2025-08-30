"""
LeetCode 1263. Minimum Moves to Move a Box to Their Target Location
Problem: A storekeeper is a game in which the player pushes boxes around in a warehouse trying to get them to target locations.

The game is represented by an m x n grid where each element is a wall, floor, or box:
- '#' represents a wall
- '.' represents the floor
- 'B' represents the box
- 'S' represents the storekeeper (player)
- 'T' represents the target location

The player can push the box if:
1. The player is adjacent to the box
2. There's a free space on the opposite side of the box (to push it into)

Return the minimum number of pushes required to move the box to the target location. 
If it is impossible, return -1.

Key insights:
1. This is BFS on states: (box_position, player_position)
2. To push box from A to B, player must be at opposite side of A from B
3. Player must be able to reach the required position (separate BFS problem)
4. State space is much larger than typical grid problems
"""

# SOLUTION 1: BFS on States (PREFERRED for interviews)
# Time: O(m²*n²), Space: O(m²*n²)
def minPushBox(grid):
    """
    BFS on (box_position, player_position) states
    For each box position, try all valid pushes
    """
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    
    # Find initial positions
    box_pos = player_pos = target_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'B':
                box_pos = (i, j)
            elif grid[i][j] == 'S':
                player_pos = (i, j)
            elif grid[i][j] == 'T':
                target_pos = (i, j)
    
    def is_valid(x, y):
        """Check if position is valid (within bounds and not a wall)"""
        return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'
    
    def can_player_reach(player_start, player_target, box_position):
        """
        Check if player can reach target position without moving the box
        Uses BFS to find path for player
        """
        if player_start == player_target:
            return True
        
        if not is_valid(*player_target) or player_target == box_position:
            return False
        
        visited = set()
        queue = deque([player_start])
        visited.add(player_start)
        
        while queue:
            px, py = queue.popleft()
            
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = px + dx, py + dy
                
                if ((nx, ny) not in visited and 
                    is_valid(nx, ny) and 
                    (nx, ny) != box_position):
                    
                    if (nx, ny) == player_target:
                        return True
                    
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return False
    
    # BFS on states: (box_x, box_y, player_x, player_y)
    queue = deque([(box_pos[0], box_pos[1], player_pos[0], player_pos[1], 0)])
    visited = set()
    visited.add((box_pos[0], box_pos[1], player_pos[0], player_pos[1]))
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        bx, by, px, py, pushes = queue.popleft()
        
        # Check if box reached target
        if (bx, by) == target_pos:
            return pushes
        
        # Try pushing box in all 4 directions
        for dx, dy in directions:
            # New box position after push
            new_bx, new_by = bx + dx, by + dy
            
            # Position player needs to be to make this push
            required_px, required_py = bx - dx, by - dy
            
            # Check if new box position is valid
            if not is_valid(new_bx, new_by):
                continue
            
            # Check if required player position is valid
            if not is_valid(required_px, required_py):
                continue
            
            # Check if player can reach the required position
            if not can_player_reach((px, py), (required_px, required_py), (bx, by)):
                continue
            
            # New state after push
            new_state = (new_bx, new_by, bx, by)  # Player moves to old box position
            
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_bx, new_by, bx, by, pushes + 1))
    
    return -1


# SOLUTION 2: A* Algorithm (Advanced optimization)
# Time: O(m²*n²), Space: O(m²*n²) 
def minPushBox_astar(grid):
    """
    A* algorithm with Manhattan distance heuristic
    More efficient than pure BFS for large grids
    """
    import heapq
    
    m, n = len(grid), len(grid[0])
    
    # Find positions
    box_pos = player_pos = target_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'B':
                box_pos = (i, j)
            elif grid[i][j] == 'S':
                player_pos = (i, j)
            elif grid[i][j] == 'T':
                target_pos = (i, j)
    
    def is_valid(x, y):
        return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'
    
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def can_player_reach(start, target, box_pos):
        if start == target:
            return True
        if not is_valid(*target) or target == box_pos:
            return False
        
        visited = set([start])
        queue = deque([start])
        
        while queue:
            px, py = queue.popleft()
            
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = px + dx, py + dy
                
                if ((nx, ny) not in visited and 
                    is_valid(nx, ny) and (nx, ny) != box_pos):
                    
                    if (nx, ny) == target:
                        return True
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return False
    
    # A* with priority queue: (f_score, pushes, box_x, box_y, player_x, player_y)
    pq = [(manhattan_distance(box_pos, target_pos), 0, box_pos[0], box_pos[1], player_pos[0], player_pos[1])]
    visited = set()
    visited.add((box_pos[0], box_pos[1], player_pos[0], player_pos[1]))
    
    while pq:
        f_score, pushes, bx, by, px, py = heapq.heappop(pq)
        
        if (bx, by) == target_pos:
            return pushes
        
        # Try all push directions
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_bx, new_by = bx + dx, by + dy
            required_px, required_py = bx - dx, by - dy
            
            if (is_valid(new_bx, new_by) and 
                is_valid(required_px, required_py) and
                can_player_reach((px, py), (required_px, required_py), (bx, by))):
                
                new_state = (new_bx, new_by, bx, by)
                
                if new_state not in visited:
                    visited.add(new_state)
                    h_score = manhattan_distance((new_bx, new_by), target_pos)
                    f_score = pushes + 1 + h_score
                    heapq.heappush(pq, (f_score, pushes + 1, new_bx, new_by, bx, by))
    
    return -1


# SOLUTION 3: BFS with Optimized State Representation
# Time: O(m²*n²), Space: O(m²*n²)
def minPushBox_optimized(grid):
    """
    BFS with optimized state representation and early termination
    Use tuple packing for cleaner state management
    """
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    
    # Parse grid
    positions = {}
    for i in range(m):
        for j in range(n):
            if grid[i][j] in 'BST':
                positions[grid[i][j]] = (i, j)
    
    box_pos, player_pos, target = positions['B'], positions['S'], positions['T']
    
    def is_valid(pos):
        x, y = pos
        return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'
    
    def get_neighbors(pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)] if is_valid((x+dx, y+dy))]
    
    def player_can_reach(start, end, box):
        """BFS to check if player can reach destination without disturbing box"""
        if start == end:
            return True
        if not is_valid(end) or end == box:
            return False
        
        visited = {start}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            
            for neighbor in get_neighbors(current):
                if neighbor == end:
                    return True
                if neighbor not in visited and neighbor != box:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
    
    # BFS on game states
    initial_state = (*box_pos, *player_pos)
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        state, pushes = queue.popleft()
        bx, by, px, py = state
        
        if (bx, by) == target:
            return pushes
        
        # Try pushing box in each direction
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_box = (bx + dx, by + dy)
            required_player = (bx - dx, by - dy)
            
            if (is_valid(new_box) and 
                is_valid(required_player) and
                player_can_reach((px, py), required_player, (bx, by))):
                
                new_state = (*new_box, bx, by)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, pushes + 1))
    
    return -1


# SOLUTION 4: DFS with Memoization (Alternative approach)
# Time: O(m²*n²), Space: O(m²*n²)
def minPushBox_dfs_memo(grid):
    """
    DFS with memoization - recursive approach
    Sometimes easier to think about recursively
    """
    m, n = len(grid), len(grid[0])
    
    # Find positions
    box_pos = player_pos = target_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'B':
                box_pos = (i, j)
            elif grid[i][j] == 'S':
                player_pos = (i, j)
            elif grid[i][j] == 'T':
                target_pos = (i, j)
    
    def is_valid(x, y):
        return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'
    
    def can_reach(start, end, blocked):
        """Check if player can reach end from start, avoiding blocked position"""
        if start == end:
            return True
        if not is_valid(*end) or end == blocked:
            return False
        
        visited = set([start])
        stack = [start]
        
        while stack:
            px, py = stack.pop()
            
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = px + dx, py + dy
                
                if ((nx, ny) not in visited and 
                    is_valid(nx, ny) and (nx, ny) != blocked):
                    
                    if (nx, ny) == end:
                        return True
                    visited.add((nx, ny))
                    stack.append((nx, ny))
        
        return False
    
    # Memoization for DFS
    memo = {}
    
    def dfs(box_x, box_y, player_x, player_y):
        # Base case: box at target
        if (box_x, box_y) == target_pos:
            return 0
        
        state = (box_x, box_y, player_x, player_y)
        if state in memo:
            return memo[state]
        
        min_pushes = float('inf')
        
        # Try pushing box in all directions
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_bx, new_by = box_x + dx, box_y + dy
            required_px, required_py = box_x - dx, box_y - dy
            
            if (is_valid(new_bx, new_by) and 
                is_valid(required_px, required_py) and
                can_reach((player_x, player_y), (required_px, required_py), (box_x, box_y))):
                
                # Recursive call with new state
                result = dfs(new_bx, new_by, box_x, box_y)
                if result != -1:
                    min_pushes = min(min_pushes, result + 1)
        
        result = min_pushes if min_pushes != float('inf') else -1
        memo[state] = result
        return result
    
    return dfs(box_pos[0], box_pos[1], player_pos[0], player_pos[1])


# SOLUTION 5: BFS with State Compression (Memory optimization)
# Time: O(m²*n²), Space: O(m²*n²)
def minPushBox_compressed(grid):
    """
    BFS with state compression using single integer instead of tuple
    Good for discussing space optimization
    """
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    
    # Find positions
    box_pos = player_pos = target_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'B':
                box_pos = (i, j)
            elif grid[i][j] == 'S':
                player_pos = (i, j)
            elif grid[i][j] == 'T':
                target_pos = (i, j)
    
    def is_valid(x, y):
        return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'
    
    def encode_state(bx, by, px, py):
        """Compress state into single integer"""
        return bx * n * m * n + by * m * n + px * n + py
    
    def decode_state(state):
        """Decompress state back to coordinates"""
        py = state % n
        px = (state // n) % m
        by = (state // (n * m)) % n
        bx = state // (n * m * n)
        return bx, by, px, py
    
    def can_player_reach(start, end, box):
        if start == end:
            return True
        if not is_valid(*end) or end == box:
            return False
        
        visited = set([start])
        queue = deque([start])
        
        while queue:
            px, py = queue.popleft()
            
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = px + dx, py + dy
                
                if ((nx, ny) not in visited and 
                    is_valid(nx, ny) and (nx, ny) != box):
                    
                    if (nx, ny) == end:
                        return True
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return False
    
    initial_state = encode_state(box_pos[0], box_pos[1], player_pos[0], player_pos[1])
    queue = deque([(initial_state, 0)])
    visited = set([initial_state])
    
    while queue:
        state, pushes = queue.popleft()
        bx, by, px, py = decode_state(state)
        
        if (bx, by) == target_pos:
            return pushes
        
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_bx, new_by = bx + dx, by + dy
            required_px, required_py = bx - dx, by - dy
            
            if (is_valid(new_bx, new_by) and 
                is_valid(required_px, required_py) and
                can_player_reach((px, py), (required_px, required_py), (bx, by))):
                
                new_state = encode_state(new_bx, new_by, bx, by)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, pushes + 1))
    
    return -1


# Test cases
def test_solutions():
    # Test case 1: Simple case
    grid1 = [
        ["#","#","#","#","#","#"],
        ["#","T","#","#","#","#"],
        ["#",".",".","B",".","#"],
        ["#",".","#","#",".","#"],
        ["#",".",".",".","S","#"],
        ["#","#","#","#","#","#"]
    ]
    
    # Test case 2: More complex
    grid2 = [
        ["#","#","#","#","#","#"],
        ["#","T","#","#","#","#"],
        ["#",".",".","B",".","#"],
        ["#","#","#","#",".","#"],
        ["#",".",".",".","S","#"],
        ["#","#","#","#","#","#"]
    ]
    
    # Test case 3: Impossible
    grid3 = [
        ["#","#","#","#","#","#","#"],
        ["#","S","#",".","B","T","#"],
        ["#","#","#","#","#","#","#"]
    ]
    
    test_cases = [grid1, grid2, grid3]
    expected = [3, -1, -1]  # Approximate expected results
    
    print("Testing all solutions:")
    for i, grid in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("Grid:")
        for row in grid:
            print(''.join(row))
        
        result1 = minPushBox(grid)
        result2 = minPushBox_astar(grid)
        result3 = minPushBox_compressed(grid)
        result4 = minPushBox_dfs_memo(grid)
        
        print(f"BFS on States:           {result1}")
        print(f"A* Algorithm:            {result2}")
        print(f"BFS (compressed):        {result3}")
        print(f"DFS with Memoization:    {result4}")
        print(f"Expected (approx):       {expected[i]}")

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING (CRITICAL):
   - "This is a classic Sokoban/box-pushing puzzle"
   - "State = (box_position, player_position) - both matter!"
   - "To push box from A to B, player must be at opposite side of A"
   - "Player movement is constrained by walls and current box position"

2. START WITH BFS ON STATES (PREFERRED):
   - "BFS on game states, not just positions"
   - "State: (box_row, box_col, player_row, player_col)"
   - "For each state, try all 4 possible box pushes"
   - "Check if player can reach required position for each push"
   - Time: O(m²*n²), Space: O(m²*n²)

3. KEY INSIGHTS:
   - "This is NOT a simple pathfinding problem - it's state space search"
   - "Need separate BFS for player reachability checks"
   - "State space is much larger: O(m²*n²) instead of O(m*n)"
   - "Each push requires validating player can get into position"

4. IMPLEMENTATION COMPLEXITIES:
   - "Two-level BFS: outer for game states, inner for player movement"
   - "Must track both box and player positions in state"
   - "Validate: new box position valid, required player position valid, player can reach it"

5. ADVANCED OPTIMIZATIONS:
   - A*: "Use Manhattan distance heuristic to target for faster convergence"
   - State compression: "Encode state as single integer for memory efficiency"
   - Bidirectional BFS: "Search from both start and target states"

6. EDGE CASES:
   - Box already at target → return 0
   - Player cannot reach required positions → return -1
   - Box gets stuck in corner → return -1
   - Invalid initial setup → return -1

7. COMPLEXITY ANALYSIS:
   - "State space: O(m²*n²) - all combinations of box and player positions"
   - "Each state explores O(1) transitions"
   - "Player reachability check: O(m*n) per state"
   - "Overall: O(m³*n³) worst case, but often much better"

8. FOLLOW-UP QUESTIONS:
   - "How to optimize for large grids?" → A* with better heuristics
   - "Multiple boxes?" → State becomes (box1_pos, box2_pos, ..., player_pos)
   - "Find actual sequence of moves?" → Store parent pointers and reconstruct

RECOMMENDED INTERVIEW FLOW:
1. Understand problem: "Sokoban puzzle - push box to target with movement constraints"
2. Identify state space: "Not just box position - need (box_pos, player_pos)"
3. Explain BFS approach: "Search game states, validate player movement for each push"
4. Code BFS solution with player reachability helper
5. Test with example: trace through state transitions
6. Discuss complexity: O(m²*n²) states, O(m*n) per reachability check
7. Mention A* optimization if time permits

KEY INSIGHT TO COMMUNICATE:
"This is state space search where the state includes both box and player positions. The key challenge is that each box push requires validating the player can reach the required pushing position."

COMMON MISTAKES TO AVOID:
- Treating this as simple pathfinding (ignoring player position)
- Not validating player reachability for each push
- Incorrect state representation
- Missing the constraint that player must be on opposite side to push
- Not handling walls and boundaries correctly

CRITICAL SUCCESS FACTORS:
- Recognize this as state space search, not pathfinding
- Implement clean player reachability check
- Proper state management with both positions
- Clear explanation of why both positions matter

This is a challenging problem that tests graph algorithms, state space search, and implementation skills - perfect for demonstrating advanced problem-solving abilities!
"""