# LeetCode 403: Frog Jump
# 
# Problem: A frog is crossing a river. The river is divided into units, and in each unit 
# there may or may not exist a stone. The frog can jump on a stone, but not in the water.
# Given a list of stones positions (in units) in sorted ascending order, determine if 
# the frog can cross the river by landing on the last stone.

class Solution:
    def canCross(self, stones) -> bool:
        """
        Solution 1: DFS with Memoization (Top-Down DP)
        Time: O(n^2), Space: O(n^2)
        Most intuitive approach for interviews
        """
        if not stones or stones[0] != 0:
            return False
        
        # Convert to set for O(1) lookup
        stone_set = set(stones)
        target = stones[-1]
        
        # Memoization: (current_stone, last_jump_size) -> can_reach_end
        memo = {}
        
        def dfs(stone, last_jump):
            # Base case: reached the target
            if stone == target:
                return True
            
            # Check memoization
            if (stone, last_jump) in memo:
                return memo[(stone, last_jump)]
            
            # Try all possible next jumps: k-1, k, k+1
            for next_jump in [last_jump - 1, last_jump, last_jump + 1]:
                if next_jump > 0:  # Jump size must be positive
                    next_stone = stone + next_jump
                    if next_stone in stone_set and dfs(next_stone, next_jump):
                        memo[(stone, last_jump)] = True
                        return True
            
            memo[(stone, last_jump)] = False
            return False
        
        # Start from stone 0 with initial jump of 1
        return dfs(0, 1)

class SolutionDP:
    def canCross(self, stones) -> bool:
        """
        Solution 2: Bottom-Up DP with Dictionary
        Time: O(n^2), Space: O(n^2)
        Clean implementation for interviews
        """
        if not stones or stones[0] != 0:
            return False
        
        n = len(stones)
        if n == 1:
            return True
        
        # Edge case: second stone must be at position 1
        if stones[1] != 1:
            return False
        
        # dp[i] = set of possible jump sizes to reach stone i
        dp = [set() for _ in range(n)]
        dp[0].add(1)  # Can reach first stone with jump size 1
        
        # Create position to index mapping
        stone_to_idx = {stone: i for i, stone in enumerate(stones)}
        
        for i in range(n):
            for jump_size in dp[i]:
                # Try jumps of size: jump_size-1, jump_size, jump_size+1
                for next_jump in [jump_size - 1, jump_size, jump_size + 1]:
                    if next_jump > 0:
                        next_pos = stones[i] + next_jump
                        if next_pos in stone_to_idx:
                            next_idx = stone_to_idx[next_pos]
                            dp[next_idx].add(next_jump)
        
        return len(dp[n - 1]) > 0

class SolutionOptimized:
    def canCross(self, stones) -> bool:
        """
        Solution 3: Optimized DP with HashMap
        Time: O(n^2), Space: O(n^2)
        Best for production - handles edge cases well
        """
        if not stones:
            return False
        
        n = len(stones)
        if n == 1:
            return stones[0] == 0
        
        # Early validation
        if stones[0] != 0 or stones[1] != 1:
            return False
        
        # stone_pos -> set of possible jump sizes to reach this stone
        dp = {stone: set() for stone in stones}
        dp[0].add(1)
        
        for stone in stones:
            for jump in dp[stone]:
                # Try all three possible next jumps
                for next_jump in [jump - 1, jump, jump + 1]:
                    if next_jump > 0:
                        next_stone = stone + next_jump
                        if next_stone in dp:
                            dp[next_stone].add(next_jump)
        
        return bool(dp[stones[-1]])

class SolutionBFS:
    def canCross(self, stones) -> bool:
        """
        Solution 4: BFS Approach
        Time: O(n^2), Space: O(n^2)
        Alternative approach - good to mention in interviews
        """
        if not stones or stones[0] != 0:
            return False
        
        stone_set = set(stones)
        target = stones[-1]
        
        # BFS: (current_stone, last_jump_size)
        from collections import deque
        queue = deque([(0, 1)])  # Start at stone 0 with jump size 1
        visited = set([(0, 1)])
        
        while queue:
            stone, last_jump = queue.popleft()
            
            # Try next jumps: k-1, k, k+1
            for next_jump in [last_jump - 1, last_jump, last_jump + 1]:
                if next_jump > 0:
                    next_stone = stone + next_jump
                    
                    if next_stone == target:
                        return True
                    
                    if next_stone in stone_set and (next_stone, next_jump) not in visited:
                        visited.add((next_stone, next_jump))
                        queue.append((next_stone, next_jump))
        
        return False

# Test cases and analysis
def test_solutions():
    solutions = [Solution(), SolutionDP(), SolutionOptimized(), SolutionBFS()]
    
    test_cases = [
        ([0,1,3,5,6,8,12,17], True),   # Example 1: Can reach end
        ([0,1,2,3,4,8,9,11], False),  # Example 2: Cannot reach end
        ([0], True),                  # Single stone
        ([0,1], True),                # Two stones
        ([0,2], False),               # Invalid: second stone not at position 1
        ([0,1,3,6,10,15,21], True),   # Arithmetic progression
        ([0,1,3,4,5,7,9,10,12], True) # Complex valid case
    ]
    
    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i} ({sol.__class__.__name__}) Results:")
        for stones, expected in test_cases:
            try:
                result = sol.canCross(stones)
                status = "✓" if result == expected else "✗"
                print(f"  {status} canCross({stones}) = {result}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        print()

def analyze_complexity():
    print("Complexity Analysis:")
    print("Time Complexity: O(n^2) for all solutions")
    print("- Each stone can be reached with at most n different jump sizes")
    print("- We process each (stone, jump_size) pair at most once")
    print()
    print("Space Complexity: O(n^2)")
    print("- Memoization/DP table stores (stone, jump_size) pairs")
    print("- In worst case, each stone can have O(n) different jump sizes")

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*50)
    analyze_complexity()

# Interview Strategy Guide:
"""
1. Start by understanding the problem:
   - Frog starts at stone 0
   - First jump must be size 1 (to stone at position 1)
   - From jump size k, next jump can be k-1, k, or k+1
   - Goal: reach the last stone

2. Key insights to mention:
   - This is a graph traversal problem disguised as DP
   - State: (current_stone, last_jump_size)
   - Transition: try jumps of size k-1, k, k+1

3. Edge cases to handle:
   - Empty stones array
   - Single stone (trivial case)
   - Second stone not at position 1 (impossible)
   - Stones[0] != 0 (invalid start)

4. Optimization techniques:
   - Use set for O(1) stone lookup
   - Memoization to avoid recalculating states
   - Early termination when target is reached

5. Follow-up questions to expect:
   - What if frog could jump backwards?
   - What's the minimum number of jumps needed?
   - How to find the actual path taken?
"""
