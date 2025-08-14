# LeetCode 1575: Count All Possible Routes
#
# Problem: You are given an array of distinct positive integers locations where locations[i] 
# represents the position of city i. You are also given start, finish, and fuel representing 
# the starting city, ending city, and initial fuel.
#
# At each step, if you are at city i, you can pick any city j != i and move to city j. 
# Moving from city i to city j reduces fuel by |locations[i] - locations[j]|.
#
# Return the count of all possible routes from start to finish with exactly fuel amount.

# Solution 1: Top-down DP with Memoization - Most Common Interview Solution
def countRoutes(locations, start, finish, fuel):
    """
    Time: O(n^2 * fuel), Space: O(n * fuel)
    
    This is the most intuitive approach for interviews.
    State: (current_city, remaining_fuel)
    """
    MOD = 10**9 + 7
    n = len(locations)
    memo = {}
    
    def dfs(city, remaining_fuel):
        # Base case: if no fuel left, check if we're at finish
        if remaining_fuel < 0:
            return 0
        
        if (city, remaining_fuel) in memo:
            return memo[(city, remaining_fuel)]
        
        # If we're at finish, count this as 1 route
        # But we can still continue if we have fuel
        result = 1 if city == finish else 0
        
        # Try going to all other cities
        for next_city in range(n):
            if next_city != city:
                fuel_cost = abs(locations[city] - locations[next_city])
                if remaining_fuel >= fuel_cost:
                    result = (result + dfs(next_city, remaining_fuel - fuel_cost)) % MOD
        
        memo[(city, remaining_fuel)] = result
        return result
    
    return dfs(start, fuel)

# Solution 2: Bottom-up DP - Alternative Approach
def countRoutesDP(locations, start, finish, fuel):
    """
    Time: O(n^2 * fuel), Space: O(n * fuel)
    
    Bottom-up dynamic programming approach.
    dp[f][i] = number of routes ending at city i with exactly f fuel used
    """
    MOD = 10**9 + 7
    n = len(locations)
    
    # dp[fuel_used][city] = number of ways
    dp = [[0] * n for _ in range(fuel + 1)]
    
    # Base case: we start at 'start' city with 0 fuel used
    dp[0][start] = 1
    
    result = 0
    
    # For each amount of fuel used
    for f in range(fuel + 1):
        # If we're at finish city, add to result
        result = (result + dp[f][finish]) % MOD
        
        # Try all possible moves
        for city in range(n):
            if dp[f][city] == 0:
                continue
                
            for next_city in range(n):
                if city != next_city:
                    fuel_needed = abs(locations[city] - locations[next_city])
                    if f + fuel_needed <= fuel:
                        dp[f + fuel_needed][next_city] = (dp[f + fuel_needed][next_city] + dp[f][city]) % MOD
    
    return result

# Solution 3: Space Optimized Bottom-up DP
def countRoutesOptimized(locations, start, finish, fuel):
    """
    Time: O(n^2 * fuel), Space: O(n)
    
    Space-optimized version using rolling arrays.
    """
    MOD = 10**9 + 7
    n = len(locations)
    
    # Only keep current and next fuel level
    prev = [0] * n
    prev[start] = 1
    
    result = 0
    if start == finish:
        result = 1
    
    # For each fuel level
    for f in range(1, fuel + 1):
        curr = [0] * n
        
        # For each city at previous fuel level
        for city in range(n):
            if prev[city] == 0:
                continue
                
            # Try moving to all other cities
            for next_city in range(n):
                if city != next_city:
                    fuel_needed = abs(locations[city] - locations[next_city])
                    if fuel_needed == f:  # We need exactly f fuel to make this move
                        curr[next_city] = (curr[next_city] + prev[city]) % MOD
        
        # Add routes that end at finish with this fuel level
        result = (result + curr[finish]) % MOD
        prev = curr
    
    return result

# Solution 4: Advanced Memoization with Pruning
def countRoutesAdvanced(locations, start, finish, fuel):
    """
    Time: O(n^2 * fuel), Space: O(n * fuel)
    
    Enhanced version with pruning optimizations for better performance.
    """
    MOD = 10**9 + 7
    n = len(locations)
    memo = {}
    
    # Precompute minimum fuel needed to reach finish from each city
    min_fuel_to_finish = [0] * n
    for i in range(n):
        min_fuel_to_finish[i] = abs(locations[i] - locations[finish])
    
    def dfs(city, remaining_fuel):
        # Pruning: if we can't reach finish even with optimal path
        if remaining_fuel < min_fuel_to_finish[city]:
            return 0
        
        if (city, remaining_fuel) in memo:
            return memo[(city, remaining_fuel)]
        
        # Count current position if it's the finish
        result = 1 if city == finish else 0
        
        # Try all possible next cities
        for next_city in range(n):
            if next_city != city:
                fuel_cost = abs(locations[city] - locations[next_city])
                if remaining_fuel >= fuel_cost:
                    result = (result + dfs(next_city, remaining_fuel - fuel_cost)) % MOD
        
        memo[(city, remaining_fuel)] = result
        return result
    
    return dfs(start, fuel)

# Solution 5: BFS Approach - Alternative Thinking
def countRoutesBFS(locations, start, finish, fuel):
    """
    Time: O(n^2 * fuel), Space: O(n * fuel)
    
    BFS approach using queue - good for showing different thinking patterns.
    """
    from collections import defaultdict, deque
    
    MOD = 10**9 + 7
    n = len(locations)
    
    # count[city][fuel] = number of ways to reach city with fuel remaining
    count = defaultdict(lambda: defaultdict(int))
    count[start][fuel] = 1
    
    result = 0
    
    # Process all states level by level
    queue = deque([(start, fuel)])
    visited = set()
    
    while queue:
        city, remaining_fuel = queue.popleft()
        
        if (city, remaining_fuel) in visited:
            continue
        visited.add((city, remaining_fuel))
        
        # If we're at finish, add to result
        if city == finish:
            result = (result + count[city][remaining_fuel]) % MOD
        
        # Try all next cities
        for next_city in range(n):
            if next_city != city:
                fuel_needed = abs(locations[city] - locations[next_city])
                if remaining_fuel >= fuel_needed:
                    new_fuel = remaining_fuel - fuel_needed
                    count[next_city][new_fuel] = (count[next_city][new_fuel] + count[city][remaining_fuel]) % MOD
                    
                    if (next_city, new_fuel) not in visited:
                        queue.append((next_city, new_fuel))
    
    return result

# Test cases and examples
def test_solutions():
    test_cases = [
        ([2,3,6,8,4], 1, 3, 5),    # Expected: 4
        ([4,3,1], 1, 0, 6),        # Expected: 5
        ([5,2,1], 0, 2, 3),        # Expected: 0
        ([1,2,3], 0, 2, 40),       # Expected: large number
    ]
    
    for locations, start, finish, fuel in test_cases:
        result1 = countRoutes(locations, start, finish, fuel)
        result2 = countRoutesDP(locations, start, finish, fuel)
        result3 = countRoutesAdvanced(locations, start, finish, fuel)
        
        print(f"locations={locations}, start={start}, finish={finish}, fuel={fuel}")
        print(f"  Memoization: {result1}")
        print(f"  Bottom-up DP: {result2}")
        print(f"  Advanced Memo: {result3}")
        print(f"  All match: {result1 == result2 == result3}")
        print()

# Detailed walkthrough for understanding
def explain_example():
    """
    Example: locations=[2,3,6,8,4], start=1, finish=3, fuel=5
    
    Cities: 0(pos=2), 1(pos=3), 2(pos=6), 3(pos=8), 4(pos=4)
    Start at city 1 (position 3), want to reach city 3 (position 8), with 5 fuel
    
    Possible routes:
    1. 1→3 directly: cost = |3-8| = 5, fuel left = 0 ✓
    2. 1→0→3: cost = |3-2| + |2-8| = 1 + 6 = 7 > 5 ✗
    3. 1→4→3: cost = |3-4| + |4-8| = 1 + 4 = 5, fuel left = 0 ✓
    4. 1→2→3: cost = |3-6| + |6-8| = 3 + 2 = 5, fuel left = 0 ✓
    5. 1→0→4→3: cost = 1 + |2-4| + 4 = 1 + 2 + 4 = 7 > 5 ✗
    6. Can we do 1→4→0→... No, after 1→4 we have 4 fuel, 4→0 costs 2, leaves 2 fuel
       Then 0→3 costs 6, but we only have 2 fuel ✗
    7. But wait, we can end at intermediate positions if they equal finish!
    
    Actually, let's trace more carefully with memoization...
    """
    print("Example walkthrough:")
    print("locations=[2,3,6,8,4], start=1, finish=3, fuel=5")
    print("Need to find all routes from city 1 to city 3 with exactly 5 fuel")
    print("This requires careful enumeration with memoization")

# Interview strategy and tips
def interview_strategy():
    """
    Interview Approach:
    
    1. **Problem Understanding** (2-3 mins):
       - Clarify that we can visit finish multiple times
       - Understand that we need EXACTLY the fuel amount
       - Confirm we can revisit cities
    
    2. **Approach Discussion** (3-4 mins):
       - Identify this as a DP problem
       - State space: (current_city, remaining_fuel)
       - Recursive relation: try all possible next moves
    
    3. **Implementation** (8-10 mins):
       - Start with top-down memoization (most intuitive)
       - Handle base cases carefully
       - Remember to mod the result
    
    4. **Optimization Discussion** (2-3 mins):
       - Space optimization possibilities
       - Pruning techniques
       - Bottom-up alternative
    
    5. **Testing** (2-3 mins):
       - Walk through small example
       - Discuss edge cases
    
    Key Points to Mention:
    - Time: O(n² × fuel) - for each state, try n-1 transitions
    - Space: O(n × fuel) - memoization table size
    - The problem allows visiting finish city multiple times
    - Need to handle the case where start == finish
    
    Common Mistakes:
    - Forgetting that we can pass through finish multiple times
    - Not handling the case where remaining_fuel < 0
    - Forgetting to apply MOD operation
    - Confusion about "exactly fuel" vs "at most fuel"
    """
    pass

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60)
    explain_example()
    print("\n" + "="*60)
    print("Interview tip: Start with Solution 1 (top-down memoization) - it's the most intuitive!")
    print("Then discuss optimizations and alternative approaches.")
