"""
LeetCode 526. Beautiful Arrangement

Problem: Given an integer n, return the number of beautiful arrangements you can construct.
A beautiful arrangement is a permutation of integers from 1 to n where:
- perm[i] is divisible by i, OR
- i is divisible by perm[i]
where i is 1-indexed.

Key Insights:
1. This is a backtracking/constraint satisfaction problem
2. Early pruning is crucial for performance
3. We can optimize by trying positions with fewer valid choices first

Time Complexity: O(k) where k is the number of valid arrangements (much less than n!)
Space Complexity: O(n) for recursion depth + used array
"""

# Approach 1: Basic Backtracking (Standard Solution)
def countArrangement_v1(n):
    """
    Standard backtracking approach - build arrangement position by position
    """
    used = [False] * (n + 1)  # 1-indexed, so size n+1
    
    def backtrack(pos):
        # Base case: filled all positions
        if pos > n:
            return 1
        
        count = 0
        # Try each unused number at current position
        for num in range(1, n + 1):
            if not used[num] and is_beautiful(pos, num):
                # Choose
                used[num] = True
                
                # Explore
                count += backtrack(pos + 1)
                
                # Unchoose
                used[num] = False
        
        return count
    
    def is_beautiful(pos, num):
        """Check if placing num at position pos is valid"""
        return pos % num == 0 or num % pos == 0
    
    return backtrack(1)

# Approach 2: Optimized Backtracking (Recommended for Interview)
def countArrangement_v2(n):
    """
    Optimized version: precompute valid numbers for each position
    This reduces the search space significantly
    """
    # Precompute valid numbers for each position
    valid = [[] for _ in range(n + 1)]
    for pos in range(1, n + 1):
        for num in range(1, n + 1):
            if pos % num == 0 or num % pos == 0:
                valid[pos].append(num)
    
    used = [False] * (n + 1)
    
    def backtrack(pos):
        if pos > n:
            return 1
        
        count = 0
        # Only try numbers that are valid for this position
        for num in valid[pos]:
            if not used[num]:
                used[num] = True
                count += backtrack(pos + 1)
                used[num] = False
        
        return count
    
    return backtrack(1)

# Approach 3: Bottom-up with Memoization
def countArrangement_v3(n):
    """
    Using memoization with bitmask to represent used numbers
    More advanced but shows optimization thinking
    """
    # Precompute valid positions for each number
    valid = [[] for _ in range(n + 1)]
    for num in range(1, n + 1):
        for pos in range(1, n + 1):
            if pos % num == 0 or num % pos == 0:
                valid[num].append(pos)
    
    memo = {}
    
    def dp(mask, pos):
        """
        mask: bitmask representing which numbers are used
        pos: current position to fill
        """
        if pos > n:
            return 1
        
        if mask in memo:
            return memo[mask]
        
        count = 0
        # Try each unused number
        for num in range(1, n + 1):
            if not (mask & (1 << num)) and pos in valid[num]:
                count += dp(mask | (1 << num), pos + 1)
        
        memo[mask] = count
        return count
    
    return dp(0, 1)

# Approach 4: Most Optimized - Fill by Constraint Difficulty
def countArrangement_v4(n):
    """
    Advanced optimization: fill positions with fewer valid options first
    This maximizes pruning effectiveness
    """
    # Precompute valid numbers for each position
    valid = [[] for _ in range(n + 1)]
    for pos in range(1, n + 1):
        for num in range(1, n + 1):
            if pos % num == 0 or num % pos == 0:
                valid[pos].append(num)
    
    # Sort positions by number of valid choices (ascending)
    positions = list(range(1, n + 1))
    positions.sort(key=lambda pos: len(valid[pos]))
    
    used = [False] * (n + 1)
    
    def backtrack(idx):
        if idx == n:
            return 1
        
        pos = positions[idx]
        count = 0
        
        for num in valid[pos]:
            if not used[num]:
                used[num] = True
                count += backtrack(idx + 1)
                used[num] = False
        
        return count
    
    return backtrack(0)

# Approach 5: Backwards Filling (Alternative Perspective)
def countArrangement_v5(n):
    """
    Fill from position n to 1 - sometimes more efficient
    """
    used = [False] * (n + 1)
    
    def backtrack(pos):
        if pos == 0:
            return 1
        
        count = 0
        for num in range(1, n + 1):
            if not used[num] and (pos % num == 0 or num % pos == 0):
                used[num] = True
                count += backtrack(pos - 1)
                used[num] = False
        
        return count
    
    return backtrack(n)

def test_beautiful_arrangement():
    """Test all approaches with various inputs"""
    test_cases = [1, 2, 3, 4, 5, 6]
    
    for n in test_cases:
        print(f"\n=== Testing n = {n} ===")
        
        results = []
        approaches = [
            ("Basic Backtracking", countArrangement_v1),
            ("Optimized Precompute", countArrangement_v2),
            ("Memoization + Bitmask", countArrangement_v3),
            ("Constraint-based Order", countArrangement_v4),
            ("Backwards Filling", countArrangement_v5)
        ]
        
        for name, func in approaches:
            result = func(n)
            results.append(result)
            print(f"{name}: {result}")
        
        # Verify all approaches give same result
        assert all(r == results[0] for r in results), f"Results don't match for n={n}"
        
        # Show the actual arrangements for small n
        if n <= 4:
            arrangements = find_all_arrangements(n)
            print(f"Actual arrangements: {arrangements}")

def find_all_arrangements(n):
    """Helper function to show actual arrangements for small n"""
    def is_beautiful(arrangement):
        for i in range(1, len(arrangement)):
            if not (i % arrangement[i-1] == 0 or arrangement[i-1] % i == 0):
                return False
        return True
    
    from itertools import permutations
    arrangements = []
    for perm in permutations(range(1, n + 1)):
        if is_beautiful([0] + list(perm)):  # Add dummy 0 for 1-indexing
            arrangements.append(list(perm))
    
    return arrangements

def analyze_constraints(n):
    """Analyze the constraint graph for interview discussion"""
    print(f"\n=== Constraint Analysis for n = {n} ===")
    
    # Show valid numbers for each position
    for pos in range(1, n + 1):
        valid_nums = []
        for num in range(1, n + 1):
            if pos % num == 0 or num % pos == 0:
                valid_nums.append(num)
        print(f"Position {pos}: can use {valid_nums} ({len(valid_nums)} choices)")
    
    # Show valid positions for each number
    print()
    for num in range(1, n + 1):
        valid_positions = []
        for pos in range(1, n + 1):
            if pos % num == 0 or num % pos == 0:
                valid_positions.append(pos)
        print(f"Number {num}: can go in positions {valid_positions} ({len(valid_positions)} choices)")

def demonstrate_backtracking(n):
    """Show step-by-step backtracking for interview explanation"""
    if n > 4:
        print(f"Demonstration skipped for n={n} (too large)")
        return
    
    print(f"\n=== Step-by-step Backtracking for n = {n} ===")
    
    used = [False] * (n + 1)
    solutions = []
    
    def backtrack(pos, current_arrangement, depth=0):
        indent = "  " * depth
        print(f"{indent}Filling position {pos}, current: {current_arrangement[1:]}")
        
        if pos > n:
            print(f"{indent}✓ Found valid arrangement: {current_arrangement[1:]}")
            solutions.append(current_arrangement[1:])
            return 1
        
        count = 0
        for num in range(1, n + 1):
            if not used[num]:
                is_valid = pos % num == 0 or num % pos == 0
                print(f"{indent}Trying num {num} at pos {pos}: {'✓' if is_valid else '✗'}")
                
                if is_valid:
                    used[num] = True
                    current_arrangement[pos] = num
                    
                    count += backtrack(pos + 1, current_arrangement[:], depth + 1)
                    
                    used[num] = False
                    current_arrangement[pos] = 0
        
        print(f"{indent}Position {pos} returned {count} arrangements")
        return count
    
    total = backtrack(1, [0] * (n + 1))
    print(f"\nTotal arrangements found: {total}")
    return solutions

if __name__ == "__main__":
    print("=== Beautiful Arrangement Solutions ===")
    test_beautiful_arrangement()
    
    # Detailed analysis for interview
    analyze_constraints(4)
    
    # Step-by-step demonstration
    demonstrate_backtracking(3)

"""
Key Interview Discussion Points:

1. **Problem Understanding**:
   - Beautiful arrangement: perm[i] % i == 0 OR i % perm[i] == 0
   - We need to COUNT arrangements, not generate them
   - 1-indexed positions (important detail!)

2. **Algorithm Choice - Why Backtracking?**:
   - Constraint satisfaction problem with early pruning opportunities
   - Much more efficient than generating all n! permutations
   - Can eliminate invalid paths early

3. **Optimization Strategies** (mention these for extra credit):
   - **Precomputation**: Calculate valid numbers for each position upfront
   - **Constraint ordering**: Fill most constrained positions first
   - **Memoization**: Cache results for repeated subproblems
   - **Direction choice**: Sometimes backwards (n→1) is more efficient

4. **Why Precomputation Helps**:
   - Reduces inner loop from O(n) to O(valid_count)
   - For position 1: only number 1 is valid
   - For position 2: numbers 1, 2 are valid
   - Significant pruning as n grows

5. **Complexity Analysis**:
   - Time: O(k) where k = number of valid arrangements (≪ n!)
   - Space: O(n) for recursion stack + used array
   - Much better than naive O(n!) approach

6. **Edge Cases & Considerations**:
   - n = 1: Always 1 arrangement
   - Small values of n have surprisingly many arrangements
   - As n grows, constraints become tighter

7. **Follow-up Questions**:
   - What if we wanted to generate all arrangements? (similar code, store results)
   - Can we optimize further with dynamic programming? (bitmask DP shown)
   - What's the pattern in the number of arrangements as n increases?

8. **Implementation Tips**:
   - Use 1-indexed arrays or adjust indices carefully
   - Precompute valid choices for better performance
   - Consider constraint ordering for maximum pruning

9. **Alternative Approaches to Mention**:
   - Bitmask DP for advanced optimization
   - Constraint satisfaction with graph coloring perspective
   - Mathematical analysis of the divisibility constraints
"""
