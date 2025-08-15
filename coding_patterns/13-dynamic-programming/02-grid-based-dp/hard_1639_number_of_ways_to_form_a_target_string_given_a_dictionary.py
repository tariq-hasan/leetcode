"""
LeetCode 1639: Number of Ways to Form a Target String Given a Dictionary

Problem Statement:
You are given a list of strings of the same length words and a string target.

Your task is to form target using the given words under the following rules:
- target should be formed from left to right.
- To form the ith character (0-indexed) of target, you can choose the kth character 
  of the jth string in words if target[i] = words[j][k].
- Once you use the kth character of the jth string of words, you can no longer use 
  the xth character of any string in words where x <= k. That is, all characters to 
  the left of or at index k become unusable for every string.
- Repeat the process until you form the string target.

Notice that you can use multiple characters from the same string in words provided 
the conditions above are met.

Return the number of ways to form target from words. Since the answer may be large, 
return it modulo 10^9 + 7.

Example 1:
Input: words = ["acca","bbbb","caca"], target = "aba"
Output: 6
Explanation: There are 6 ways to form target.
"aba" -> index 0 ("acca"), index 1 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("acca"), index 2 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("caca"), index 1 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("caca"), index 1 ("bbbb"), index 3 ("acca")
"aba" -> index 0 ("caca"), index 2 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("caca"), index 2 ("bbbb"), index 3 ("acca")

Example 2:
Input: words = ["abba","baab"], target = "bab"
Output: 4
Explanation: There are 4 ways to form target.
"bab" -> index 0 ("baab"), index 1 ("abba"), index 2 ("abba")
"bab" -> index 0 ("baab"), index 1 ("abba"), index 3 ("baab")
"bab" -> index 0 ("baab"), index 2 ("baab"), index 3 ("baab")
"bab" -> index 1 ("abba"), index 2 ("abba"), index 3 ("baab")
"""

from collections import defaultdict

def numWaysToFormTarget(words, target):
    """
    Optimal Solution: Dynamic Programming with Character Frequency Optimization
    
    Key Insights:
    1. We can only move left-to-right through both words and target
    2. Once we use position k, we can't use positions <= k anymore
    3. Multiple words can contribute the same character at the same position
    4. This is a classic DP problem with two dimensions: target position and word position
    
    State Definition:
    dp[i][j] = number of ways to form target[0:i] using words[*][0:j]
    
    Transitions:
    - Don't use position j: dp[i][j] += dp[i][j-1]
    - Use position j (if target[i-1] matches): dp[i][j] += dp[i-1][j-1] * count[j][target[i-1]]
    
    Optimization: Precompute character frequencies at each position
    
    Time Complexity: O(m * n + len(target) * m) where m = word length, n = number of words
    Space Complexity: O(len(target) * m)
    """
    
    MOD = 10**9 + 7
    m = len(words[0])  # Length of each word
    n = len(target)
    
    if n > m:  # Impossible to form target if it's longer than word length
        return 0
    
    # Step 1: Precompute character frequencies at each position
    # freq[pos][char] = number of words that have 'char' at position 'pos'
    freq = [defaultdict(int) for _ in range(m)]
    
    for word in words:
        for pos, char in enumerate(word):
            freq[pos][char] += 1
    
    # Step 2: Dynamic Programming
    # dp[i][j] = ways to form target[0:i] using positions [0:j] from words
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: empty target can be formed in 1 way (by not using any characters)
    for j in range(m + 1):
        dp[0][j] = 1
    
    # Fill the DP table
    for i in range(1, n + 1):  # For each character in target
        for j in range(1, m + 1):  # For each position in words
            # Option 1: Don't use position j-1
            dp[i][j] = dp[i][j-1]
            
            # Option 2: Use position j-1 (if character matches)
            target_char = target[i-1]
            if target_char in freq[j-1]:
                ways_using_pos = (dp[i-1][j-1] * freq[j-1][target_char]) % MOD
                dp[i][j] = (dp[i][j] + ways_using_pos) % MOD
    
    return dp[n][m]


def numWaysToFormTarget_space_optimized(words, target):
    """
    Space-optimized version using only O(m) space
    
    Since dp[i] only depends on dp[i-1], we can use 1D arrays
    """
    
    MOD = 10**9 + 7
    m = len(words[0])
    n = len(target)
    
    if n > m:
        return 0
    
    # Precompute frequencies
    freq = [defaultdict(int) for _ in range(m)]
    for word in words:
        for pos, char in enumerate(word):
            freq[pos][char] += 1
    
    # Use 1D DP arrays
    prev_dp = [1] * (m + 1)  # dp[i-1][j]
    curr_dp = [0] * (m + 1)  # dp[i][j]
    
    for i in range(1, n + 1):
        curr_dp[0] = 0  # Can't form non-empty target with 0 positions
        
        for j in range(1, m + 1):
            # Don't use position j-1
            curr_dp[j] = curr_dp[j-1]
            
            # Use position j-1 if possible
            target_char = target[i-1]
            if target_char in freq[j-1]:
                ways_using_pos = (prev_dp[j-1] * freq[j-1][target_char]) % MOD
                curr_dp[j] = (curr_dp[j] + ways_using_pos) % MOD
        
        # Swap arrays for next iteration
        prev_dp, curr_dp = curr_dp, prev_dp
        curr_dp = [0] * (m + 1)  # Reset current array
    
    return prev_dp[m]


def numWaysToFormTarget_memoization(words, target):
    """
    Top-down approach with memoization
    
    Sometimes easier to understand the recursion logic
    """
    
    MOD = 10**9 + 7
    m = len(words[0])
    n = len(target)
    
    if n > m:
        return 0
    
    # Precompute frequencies
    freq = [defaultdict(int) for _ in range(m)]
    for word in words:
        for pos, char in enumerate(word):
            freq[pos][char] += 1
    
    memo = {}
    
    def dp(target_idx, word_pos):
        """
        Returns number of ways to form target[target_idx:] 
        using word positions [word_pos:]
        """
        # Base cases
        if target_idx == n:  # Successfully formed entire target
            return 1
        
        if word_pos == m:  # Ran out of positions but target not complete
            return 0
        
        if n - target_idx > m - word_pos:  # Not enough positions left
            return 0
        
        if (target_idx, word_pos) in memo:
            return memo[(target_idx, word_pos)]
        
        result = 0
        
        # Option 1: Skip current word position
        result = dp(target_idx, word_pos + 1)
        
        # Option 2: Use current word position (if character matches)
        target_char = target[target_idx]
        if target_char in freq[word_pos]:
            ways_using_pos = (dp(target_idx + 1, word_pos + 1) * freq[word_pos][target_char]) % MOD
            result = (result + ways_using_pos) % MOD
        
        memo[(target_idx, word_pos)] = result
        return result
    
    return dp(0, 0)


def numWaysToFormTarget_brute_force(words, target):
    """
    Brute force solution for small inputs (exponential time)
    
    Useful for understanding the problem and verifying correctness
    """
    
    MOD = 10**9 + 7
    m = len(words[0])
    n = len(target)
    
    if n > m:
        return 0
    
    def backtrack(target_idx, word_pos):
        # Successfully formed target
        if target_idx == n:
            return 1
        
        # Ran out of word positions
        if word_pos == m:
            return 0
        
        # Not enough positions remaining
        if n - target_idx > m - word_pos:
            return 0
        
        total_ways = 0
        
        # Try all ways to continue
        for next_pos in range(word_pos, m - (n - target_idx) + 1):
            # Count how many words have the required character at next_pos
            count = 0
            target_char = target[target_idx]
            
            for word in words:
                if word[next_pos] == target_char:
                    count += 1
            
            if count > 0:
                ways = backtrack(target_idx + 1, next_pos + 1)
                total_ways = (total_ways + count * ways) % MOD
        
        return total_ways
    
    return backtrack(0, 0)


def demonstrate_algorithm():
    """
    Step-by-step demonstration of the DP algorithm
    """
    words = ["acca", "bbbb", "caca"]
    target = "aba"
    
    print("Demonstrating DP Algorithm:")
    print("=" * 50)
    print(f"Words: {words}")
    print(f"Target: '{target}'")
    print()
    
    MOD = 10**9 + 7
    m = len(words[0])
    n = len(target)
    
    # Step 1: Show frequency computation
    print("Step 1: Character frequencies at each position")
    freq = [defaultdict(int) for _ in range(m)]
    for word in words:
        for pos, char in enumerate(word):
            freq[pos][char] += 1
    
    for pos in range(m):
        print(f"Position {pos}: {dict(freq[pos])}")
    print()
    
    # Step 2: Show DP table construction
    print("Step 2: DP table construction")
    print("dp[i][j] = ways to form target[0:i] using word positions [0:j]")
    print()
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case
    for j in range(m + 1):
        dp[0][j] = 1
    
    print("After base case (dp[0][j] = 1 for all j):")
    print_dp_table(dp, target, m)
    print()
    
    # Fill DP table step by step
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i][j-1]
            
            target_char = target[i-1]
            if target_char in freq[j-1]:
                ways_using_pos = (dp[i-1][j-1] * freq[j-1][target_char]) % MOD
                dp[i][j] = (dp[i][j] + ways_using_pos) % MOD
        
        print(f"After processing target[{i-1}] = '{target[i-1]}':")
        print_dp_table(dp, target, m)
        print()
    
    print(f"Final answer: {dp[n][m]}")


def print_dp_table(dp, target, m):
    """Helper function to print DP table nicely"""
    n = len(target)
    
    # Header
    print("    j:", end="")
    for j in range(m + 1):
        print(f"{j:4d}", end="")
    print()
    
    # Rows
    for i in range(n + 1):
        if i == 0:
            print("  ''  :", end="")
        else:
            print(f" '{target[i-1]}' :", end="")
        
        for j in range(m + 1):
            print(f"{dp[i][j]:4d}", end="")
        print()


# Test cases
def test_solution():
    """Test all solutions with provided examples and edge cases"""
    
    test_cases = [
        (["acca","bbbb","caca"], "aba", 6),
        (["abba","baab"], "bab", 4),
        (["abcd"], "abcd", 1),
        (["abcd"], "dcba", 0),  # Impossible
        (["aa","bb"], "ab", 0),  # No valid way
        (["abc"], "def", 0),  # No matching characters
        (["a"], "a", 1),  # Single character
        (["a","b","c"], "abc", 1),  # Each char from different position
        (["abcdef"], "ace", 1),  # Skip some positions
    ]
    
    solutions = [
        ("DP Bottom-Up", numWaysToFormTarget),
        ("DP Space-Optimized", numWaysToFormTarget_space_optimized),
        ("DP Memoization", numWaysToFormTarget_memoization),
    ]
    
    for sol_name, solution_func in solutions:
        print(f"\nTesting {sol_name}:")
        print("=" * 50)
        
        for i, (words, target, expected) in enumerate(test_cases, 1):
            try:
                result = solution_func(words.copy(), target)
                status = "✓ PASS" if result == expected else "✗ FAIL"
                
                print(f"Test Case {i}: {status}")
                print(f"  Words: {words}")
                print(f"  Target: '{target}'")
                print(f"  Expected: {expected}")
                print(f"  Got:      {result}")
            except Exception as e:
                print(f"Test Case {i}: ✗ ERROR - {str(e)}")
        print()


# Run tests and demonstration
if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70 + "\n")
    demonstrate_algorithm()


"""
INTERVIEW DISCUSSION POINTS:

1. PROBLEM CLASSIFICATION:
   - Dynamic Programming (2D state space)
   - String matching with constraints
   - Combinatorial counting problem
   - Similar to "Distinct Subsequences" but with positional constraints

2. KEY INSIGHTS:
   - Can only move left-to-right (monotonic constraint)
   - Multiple strings can contribute same character at same position
   - Need to count frequency of each character at each position
   - Classic DP with choice: use current position or skip it

3. STATE DEFINITION:
   - dp[i][j] = ways to form target[0:i] using word positions [0:j]
   - Two dimensions needed: progress in target, progress in word positions
   - Base case: empty string can be formed in 1 way

4. TRANSITION ANALYSIS:
   - Always have choice to skip current position: dp[i][j] += dp[i][j-1]
   - If character matches, can use position: dp[i][j] += dp[i-1][j-1] * frequency
   - Frequency optimization crucial for performance

5. COMPLEXITY ANALYSIS:
   - Time: O(num_words * word_length + target_length * word_length)
   - Space: O(target_length * word_length) or O(word_length) with optimization
   - Frequency precomputation: O(num_words * word_length)

6. OPTIMIZATION TECHNIQUES:
   - Space optimization: Use 1D arrays since dp[i] only depends on dp[i-1]
   - Early termination: If remaining target longer than remaining positions
   - Frequency precomputation: Avoid counting same characters repeatedly

7. EDGE CASES:
   - Target longer than word length (impossible)
   - No matching characters at any position
   - Single character words/target
   - Empty target (should return 1)
   - All characters same vs all different

8. ALTERNATIVE APPROACHES:
   - Top-down memoization (sometimes easier to understand)
   - Brute force with backtracking (exponential, only for small inputs)
   - Could use different state representations

9. FOLLOW-UP QUESTIONS:
   - "What if we could use characters out of order?" (Different problem)
   - "What if words had different lengths?" (Need to handle variable lengths)
   - "Memory optimization for very long words?" (Consider rolling arrays)
   - "What if we wanted actual combinations, not just count?" (Need to track paths)

10. COMMON MISTAKES:
    - Forgetting the modulo operation
    - Wrong indexing (off-by-one errors)
    - Not handling the monotonic constraint properly
    - Inefficient character counting (should precompute frequencies)
    - Incorrect base cases

11. PROBLEM VARIANTS:
    - LeetCode 115: Distinct Subsequences (similar DP pattern)
    - Edit distance problems (similar 2D DP)
    - Longest Common Subsequence (foundation for this type of problem)
"""
