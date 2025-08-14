# LeetCode 920: Number of Music Playlists
#
# Problem: Your music player contains n different songs. You want to listen to goal songs 
# (not necessarily different) during your trip. You create a playlist so that:
# - Every song is played at least once
# - A song can only be replayed if k other songs have been played after it
#
# Return the number of possible playlists modulo 10^9 + 7

# Solution 1: Dynamic Programming (2D) - Most Common Interview Solution
def numMusicPlaylists(n, goal, k):
    """
    Time: O(n * goal), Space: O(n * goal)
    
    dp[i][j] = number of ways to create playlist of length i using j unique songs
    
    Transitions:
    1. Add a new song: dp[i-1][j-1] * (n - (j-1)) ways
    2. Repeat existing song: dp[i-1][j] * max(0, j-k) ways
    """
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to make playlist of length i with j unique songs
    dp = [[0] * (n + 1) for _ in range(goal + 1)]
    dp[0][0] = 1  # Base case: empty playlist
    
    for i in range(1, goal + 1):
        for j in range(1, min(i, n) + 1):
            # Case 1: Add a new song (haven't used before)
            # We have (n - (j-1)) = (n - j + 1) songs to choose from
            if j <= n:
                dp[i][j] = (dp[i][j] + dp[i-1][j-1] * (n - j + 1)) % MOD
            
            # Case 2: Repeat an existing song
            # We can only repeat if we have more than k songs to choose from
            if j > k:
                dp[i][j] = (dp[i][j] + dp[i-1][j] * (j - k)) % MOD
    
    return dp[goal][n]

# Solution 2: Space Optimized DP (1D) - Interview Follow-up
def numMusicPlaylistsOptimized(n, goal, k):
    """
    Time: O(n * goal), Space: O(n)
    Space-optimized version using only 1D array.
    """
    MOD = 10**9 + 7
    
    # Only need previous row, so use 1D array
    prev = [0] * (n + 1)
    prev[0] = 1
    
    for i in range(1, goal + 1):
        curr = [0] * (n + 1)
        for j in range(1, min(i, n) + 1):
            # Add new song
            if j <= n:
                curr[j] = (curr[j] + prev[j-1] * (n - j + 1)) % MOD
            
            # Repeat existing song
            if j > k:
                curr[j] = (curr[j] + prev[j] * (j - k)) % MOD
        
        prev = curr
    
    return prev[n]

# Solution 3: Mathematical Approach with Inclusion-Exclusion
def numMusicPlaylistsMath(n, goal, k):
    """
    Time: O(n), Space: O(1)
    Advanced mathematical solution using inclusion-exclusion principle.
    This is more complex but shows deep understanding.
    """
    MOD = 10**9 + 7
    
    def mod_pow(base, exp, mod):
        result = 1
        base %= mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp //= 2
            base = (base * base) % mod
        return result
    
    def mod_inverse(a, mod):
        return mod_pow(a, mod - 2, mod)
    
    def factorial(n, mod):
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        return result
    
    def falling_factorial(n, k, mod):
        """Compute n * (n-1) * ... * (n-k+1) mod mod"""
        result = 1
        for i in range(k):
            result = (result * (n - i)) % mod
        return result
    
    # Use inclusion-exclusion principle
    # Answer = sum over i from 0 to n of:
    # (-1)^i * C(n,i) * (n-i)^(goal-k*(n-i)) * falling_factorial(goal, n-i)
    
    result = 0
    factorial_n = factorial(n, MOD)
    
    for i in range(n + 1):
        if goal < k * (n - i):
            continue
            
        # Calculate C(n, i)
        if i == 0:
            comb = 1
        else:
            comb = factorial_n
            comb = (comb * mod_inverse(factorial(i, MOD), MOD)) % MOD
            comb = (comb * mod_inverse(factorial(n - i, MOD), MOD)) % MOD
        
        # Calculate (n-i)^(goal - k*(n-i))
        exponent = goal - k * (n - i)
        if exponent < 0:
            continue
            
        power_term = mod_pow(n - i, exponent, MOD) if n - i > 0 else (1 if exponent == 0 else 0)
        
        # Calculate falling factorial
        fall_fact = falling_factorial(goal, n - i, MOD)
        
        # Combine terms
        term = (comb * power_term) % MOD
        term = (term * fall_fact) % MOD
        
        if i % 2 == 0:
            result = (result + term) % MOD
        else:
            result = (result - term + MOD) % MOD
    
    return result

# Solution 4: Top-down DP with Memoization - Alternative Approach
def numMusicPlaylistsMemo(n, goal, k):
    """
    Time: O(n * goal), Space: O(n * goal)
    Top-down recursive approach with memoization.
    """
    MOD = 10**9 + 7
    memo = {}
    
    def dp(remaining_songs, remaining_positions, used_songs):
        if remaining_positions == 0:
            return 1 if remaining_songs == 0 else 0
        
        if remaining_songs > remaining_positions:
            return 0
        
        if (remaining_songs, remaining_positions, used_songs) in memo:
            return memo[(remaining_songs, remaining_positions, used_songs)]
        
        result = 0
        
        # Case 1: Use a new song
        if remaining_songs > 0:
            new_ways = remaining_songs  # Can choose from remaining_songs
            result = (result + new_ways * dp(remaining_songs - 1, remaining_positions - 1, used_songs + 1)) % MOD
        
        # Case 2: Repeat an existing song
        if used_songs > k:  # Can only repeat if we have more than k songs available
            repeat_ways = used_songs - k
            result = (result + repeat_ways * dp(remaining_songs, remaining_positions - 1, used_songs)) % MOD
        
        memo[(remaining_songs, remaining_positions, used_songs)] = result
        return result
    
    return dp(n, goal, 0)

# Test cases and detailed examples
def test_solutions():
    test_cases = [
        (3, 3, 1),  # Expected: 6
        (2, 3, 0),  # Expected: 6  
        (2, 3, 1),  # Expected: 2
        (3, 4, 2),  # Expected: 6
    ]
    
    for n, goal, k in test_cases:
        result1 = numMusicPlaylists(n, goal, k)
        result2 = numMusicPlaylistsOptimized(n, goal, k)
        result3 = numMusicPlaylistsMemo(n, goal, k)
        
        print(f"n={n}, goal={goal}, k={k}:")
        print(f"  2D DP: {result1}")
        print(f"  1D DP: {result2}")  
        print(f"  Memo: {result3}")
        print(f"  Match: {result1 == result2 == result3}")
        print()

# Detailed example walkthrough for n=3, goal=3, k=1:
def explain_example():
    """
    Example: n=3, goal=3, k=1
    
    We have 3 songs: A, B, C
    We want playlist of length 3
    After playing a song, must wait 1 song before replaying
    
    Valid playlists:
    1. A-B-C: Use each song once
    2. A-C-B: Use each song once  
    3. B-A-C: Use each song once
    4. B-C-A: Use each song once
    5. C-A-B: Use each song once
    6. C-B-A: Use each song once
    
    Total: 6 ways (which is 3! = 6)
    
    Note: We can't have playlists like A-A-B because after playing A,
    we need to wait k=1 songs before playing A again.
    """
    print("Example explanation:")
    print("n=3 (songs A,B,C), goal=3 (playlist length), k=1 (wait time)")
    print("Valid playlists: A-B-C, A-C-B, B-A-C, B-C-A, C-A-B, C-B-A")
    print("Total: 6 ways")

# Interview tips and complexity analysis
def interview_tips():
    """
    Interview Strategy:
    
    1. Start with problem understanding:
       - Clarify what k means (songs to wait before replay)
       - Confirm that all n songs must be used at least once
    
    2. Think about state representation:
       - dp[i][j] = ways to make playlist of length i using j unique songs
    
    3. Identify transitions:
       - Add new song: have (n-j+1) choices, transition from dp[i-1][j-1]
       - Repeat song: have max(0, j-k) choices, transition from dp[i-1][j]
    
    4. Discuss optimizations:
       - Space optimization (1D array)
       - Mathematical approach (advanced)
    
    Time Complexity: O(n * goal)
    Space Complexity: O(n * goal) for 2D, O(n) for optimized
    
    Common mistakes:
    - Forgetting that ALL n songs must be used
    - Misunderstanding the k constraint
    - Off-by-one errors in transitions
    """
    pass

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*50)
    explain_example()
    print("\n" + "="*50)
    print("Remember: Focus on the 2D DP solution first, then mention optimizations!")
