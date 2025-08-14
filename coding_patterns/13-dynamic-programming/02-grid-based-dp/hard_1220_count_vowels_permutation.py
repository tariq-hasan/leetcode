# LeetCode 1220: Count Vowels Permutation
# 
# Problem: Given an integer n, return the number of strings of length n that consist only of vowels
# (a, e, i, o, u) and are lexicographically sorted.
#
# Rules:
# - 'a' may only be followed by 'e'
# - 'e' may only be followed by 'a' or 'i'  
# - 'i' may not be followed by another 'i' or 'u'
# - 'o' may only be followed by 'i' or 'u'
# - 'u' may only be followed by 'a'

# Solution 1: Dynamic Programming (Bottom-up) - Most Common Interview Solution
def countVowelPermutation(n):
    """
    Time: O(n), Space: O(1)
    This is the optimal solution most interviewers expect.
    """
    MOD = 10**9 + 7
    
    # dp[i] represents count of strings ending with vowel i
    # 0=a, 1=e, 2=i, 3=o, 4=u
    prev = [1, 1, 1, 1, 1]  # Base case: n=1
    
    for length in range(2, n + 1):
        curr = [0] * 5
        
        # Each vowel can be formed from specific previous vowels
        curr[0] = (prev[1] + prev[2] + prev[4]) % MOD  # 'a' from e,i,u
        curr[1] = (prev[0] + prev[2]) % MOD            # 'e' from a,i  
        curr[2] = (prev[1] + prev[3]) % MOD            # 'i' from e,o
        curr[3] = prev[2] % MOD                        # 'o' from i
        curr[4] = (prev[2] + prev[3]) % MOD            # 'u' from i,o
        
        prev = curr
    
    return sum(prev) % MOD

# Solution 2: Matrix Exponentiation - Advanced Optimization
def countVowelPermutationMatrix(n):
    """
    Time: O(log n), Space: O(1)
    Advanced solution using matrix exponentiation for very large n.
    """
    MOD = 10**9 + 7
    
    # Transition matrix based on the rules
    # Each row i represents transitions TO vowel i
    transition = [
        [0, 1, 1, 0, 1],  # to 'a': from e,i,u
        [1, 0, 1, 0, 0],  # to 'e': from a,i
        [0, 1, 0, 1, 0],  # to 'i': from e,o  
        [0, 0, 1, 0, 0],  # to 'o': from i
        [0, 0, 1, 1, 0]   # to 'u': from i,o
    ]
    
    def matrix_multiply(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        result = [[0] * cols_B for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % MOD
        return result
    
    def matrix_power(matrix, power):
        size = len(matrix)
        result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        base = [row[:] for row in matrix]
        
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        
        return result
    
    if n == 1:
        return 5
    
    # Calculate transition^(n-1)
    result_matrix = matrix_power(transition, n - 1)
    
    # Sum all possibilities (each vowel can be starting vowel)
    total = 0
    for i in range(5):
        for j in range(5):
            total = (total + result_matrix[i][j]) % MOD
    
    return total

# Solution 3: Memoization (Top-down DP) - Alternative Approach
def countVowelPermutationMemo(n):
    """
    Time: O(n), Space: O(n)
    Top-down approach with memoization.
    """
    MOD = 10**9 + 7
    memo = {}
    
    # Mapping: 0=a, 1=e, 2=i, 3=o, 4=u
    # Rules encoded as what can follow each vowel
    next_vowels = {
        0: [1],           # 'a' -> 'e'
        1: [0, 2],        # 'e' -> 'a', 'i'
        2: [0, 1, 3, 4],  # 'i' -> 'a', 'e', 'o', 'u'
        3: [2, 4],        # 'o' -> 'i', 'u'
        4: [0]            # 'u' -> 'a'
    }
    
    def dfs(pos, last_vowel):
        if pos == n:
            return 1
        
        if (pos, last_vowel) in memo:
            return memo[(pos, last_vowel)]
        
        result = 0
        for next_vowel in next_vowels[last_vowel]:
            result = (result + dfs(pos + 1, next_vowel)) % MOD
        
        memo[(pos, last_vowel)] = result
        return result
    
    # Try starting with each vowel
    total = 0
    for start_vowel in range(5):
        total = (total + dfs(1, start_vowel)) % MOD
    
    return total

# Test cases and examples
def test_solutions():
    test_cases = [1, 2, 5, 144]
    
    for n in test_cases:
        result1 = countVowelPermutation(n)
        result2 = countVowelPermutationMatrix(n)
        result3 = countVowelPermutationMemo(n)
        
        print(f"n={n}:")
        print(f"  DP Solution: {result1}")
        print(f"  Matrix Solution: {result2}")
        print(f"  Memo Solution: {result3}")
        print(f"  All match: {result1 == result2 == result3}")
        print()

# Example walkthrough for n=2:
# Length 1: a, e, i, o, u (5 strings)
# Length 2: 
# - Starting with 'a': ae (1)
# - Starting with 'e': ea, ei (2) 
# - Starting with 'i': ia, ie, io, iu (4)
# - Starting with 'o': oi, ou (2)
# - Starting with 'u': ua (1)
# Total: 10

if __name__ == "__main__":
    test_solutions()

# Interview Tips:
# 1. Start with the DP solution - it's the most expected
# 2. Clearly explain the state transitions based on the rules
# 3. Mention the matrix solution as an optimization for large n
# 4. Time complexity: O(n) for DP, O(log n) for matrix
# 5. Space complexity: O(1) for DP, O(1) for matrix, O(n) for memo
