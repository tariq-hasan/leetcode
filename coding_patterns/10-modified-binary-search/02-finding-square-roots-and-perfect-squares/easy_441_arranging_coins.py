"""
LeetCode 441. Arranging Coins
Problem: You have n coins and you want to build a staircase with these coins.
The staircase consists of k rows where the ith row has exactly i coins.
The last row of the staircase may be incomplete.
Given the integer n, return the number of complete rows of the staircase you will have.

Examples:
- Input: n = 5, Output: 2 (1 + 2 = 3 coins used, row 3 would need 3 more coins)
- Input: n = 8, Output: 3 (1 + 2 + 3 = 6 coins used, row 4 would need 4 more coins)

Key insight: We need to find largest k such that k*(k+1)/2 <= n
This is the sum formula: 1 + 2 + 3 + ... + k = k*(k+1)/2
"""

# SOLUTION 1: Binary Search (PREFERRED for interviews)
# Time: O(log n), Space: O(1)
def arrangeCoins(n):
    """
    Binary search approach - most efficient and expected solution
    Search for the largest k where k*(k+1)/2 <= n
    """
    left, right = 0, n
    
    while left <= right:
        mid = (left + right) // 2
        # Calculate sum of 1+2+...+mid using arithmetic series formula
        coins_used = mid * (mid + 1) // 2
        
        if coins_used <= n:
            left = mid + 1
        else:
            right = mid - 1
    
    # When loop ends, right is the largest k where k*(k+1)/2 <= n
    return right


# SOLUTION 2: Mathematical Formula (Most Optimal)
# Time: O(1), Space: O(1)
def arrangeCoins_math(n):
    """
    Direct mathematical solution using quadratic formula
    From k*(k+1)/2 <= n, we get k² + k - 2n <= 0
    Using quadratic formula: k = (-1 + sqrt(1 + 8n)) / 2
    """
    import math
    # Solve k*(k+1)/2 = n for k using quadratic formula
    # k² + k - 2n = 0
    # k = (-1 + sqrt(1 + 8n)) / 2
    return int((-1 + math.sqrt(1 + 8 * n)) / 2)


# SOLUTION 3: Linear Search/Simulation (Brute Force)
# Time: O(sqrt(n)), Space: O(1)
def arrangeCoins_linear(n):
    """
    Simple iterative approach - easy to understand but less efficient
    Keep adding rows until we don't have enough coins
    """
    row = 1
    while n >= row:
        n -= row
        row += 1
    return row - 1


# SOLUTION 4: Optimized Linear with Direct Calculation
# Time: O(sqrt(n)), Space: O(1)
def arrangeCoins_optimized_linear(n):
    """
    Calculate sum directly instead of subtracting row by row
    Still O(sqrt(n)) but with better constants
    """
    k = 1
    while k * (k + 1) // 2 <= n:
        k += 1
    return k - 1


# SOLUTION 5: Binary Search with Different Bounds
# Time: O(log n), Space: O(1)
def arrangeCoins_binary_optimized(n):
    """
    Binary search with optimized upper bound
    Since k*(k+1)/2 ~ k²/2, we have k ~ sqrt(2n)
    So we can set right = sqrt(2n) instead of n
    """
    import math
    left, right = 0, int(math.sqrt(2 * n)) + 1
    
    while left <= right:
        mid = (left + right) // 2
        coins_used = mid * (mid + 1) // 2
        
        if coins_used <= n:
            left = mid + 1
        else:
            right = mid - 1
    
    return right


# SOLUTION 6: Newton's Method (Advanced)
# Time: O(log log n), Space: O(1)
def arrangeCoins_newton(n):
    """
    Newton's method to solve k*(k+1)/2 = n
    f(k) = k*(k+1)/2 - n = k²/2 + k/2 - n
    f'(k) = k + 1/2
    Newton's iteration: k_next = k - f(k)/f'(k)
    """
    if n == 0:
        return 0
    
    # Initial guess
    k = n
    while True:
        # f(k) = k*(k+1)/2 - n
        f_k = k * (k + 1) // 2 - n
        
        # If we're close enough, return floor(k)
        if abs(f_k) <= 1:
            # Check if current k works
            if k * (k + 1) // 2 <= n:
                return k
            else:
                return k - 1
        
        # f'(k) = k + 0.5
        f_prime_k = k + 0.5
        
        # Newton's update: k_next = k - f(k)/f'(k)
        k_next = k - f_k / f_prime_k
        k = int(k_next)


# Test cases
def test_solutions():
    test_cases = [0, 1, 3, 5, 8, 10, 15, 1804289383]  # Include edge cases
    
    print("Testing all solutions:")
    for n in test_cases:
        result1 = arrangeCoins(n)
        result2 = arrangeCoins_math(n)
        result3 = arrangeCoins_linear(n)
        result4 = arrangeCoins_optimized_linear(n)
        result5 = arrangeCoins_binary_optimized(n)
        result6 = arrangeCoins_newton(n)
        
        print(f"n = {n}")
        print(f"  Binary Search:       {result1}")
        print(f"  Mathematical:        {result2}")
        print(f"  Linear:              {result3}")
        print(f"  Optimized Linear:    {result4}")
        print(f"  Binary Optimized:    {result5}")
        print(f"  Newton's Method:     {result6}")
        
        # Verify correctness
        k = result1
        coins_used = k * (k + 1) // 2
        coins_next = (k + 1) * (k + 2) // 2
        print(f"  Verification: k={k}, used={coins_used}, next_row_needs={coins_next}")
        print(f"  Valid: {coins_used <= n < coins_next}")
        print()

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   - "We need to find the largest k such that 1+2+3+...+k <= n"
   - "This is equivalent to finding largest k where k*(k+1)/2 <= n"
   - "It's essentially finding the 'inverse' of the triangular number formula"

2. START WITH BINARY SEARCH (PREFERRED):
   - "Since we're looking for a boundary value in a sorted space, binary search is optimal"
   - "Search space is [0, n] looking for largest valid k"
   - "Key insight: if k works, try larger; if k doesn't work, try smaller"
   - Time: O(log n), Space: O(1)

3. MATHEMATICAL SOLUTION (MOST OPTIMAL):
   - "We can solve this directly using quadratic formula"
   - "From k*(k+1)/2 <= n, we get k² + k - 2n <= 0"
   - "Quadratic formula gives k = (-1 + sqrt(1 + 8n)) / 2"
   - Time: O(1), Space: O(1)

4. EDGE CASES:
   - n = 0 → return 0
   - n = 1 → return 1 (first row complete)
   - Large n → mention potential overflow in k*(k+1)

5. ALTERNATIVE APPROACHES:
   - Linear simulation: O(sqrt(n)) - mention as straightforward but slower
   - Newton's method: O(log log n) - advanced optimization

6. OPTIMIZATION DISCUSSIONS:
   - "Can optimize binary search bounds since k ≈ sqrt(2n)"
   - "Mathematical solution is O(1) but binary search is more intuitive"
   - "For very large numbers, be careful about integer overflow"

7. FOLLOW-UP QUESTIONS:
   - "What if we want incomplete rows too?" → Just return total rows attempted
   - "How to handle overflow?" → Use long long or check bounds
   - "Can you solve without sqrt?" → Binary search approach

RECOMMENDED INTERVIEW FLOW:
1. Understand problem: "Find largest k where sum 1+2+...+k <= n"
2. Explain binary search approach first (most interviewers expect this)
3. Code binary search solution cleanly
4. Test with examples: n=5 (answer=2), n=8 (answer=3)
5. Discuss complexity: O(log n) time, O(1) space
6. If time permits, mention mathematical O(1) solution
7. Briefly mention linear approach as alternative

KEY INSIGHT TO COMMUNICATE:
"This problem is about finding the largest triangular number <= n, which is equivalent to finding the inverse of the triangular number formula k*(k+1)/2."

COMMON MISTAKES TO AVOID:
- Off-by-one errors in binary search bounds
- Integer overflow with k*(k+1)
- Confusing "complete rows" vs "total coins used"
- Not handling edge case n=0
"""
