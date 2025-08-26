"""
LeetCode 367. Valid Perfect Square
Problem: Given a positive integer num, return true if num is a perfect square or false otherwise.
A perfect square is an integer that is the square of an integer.
You must not use any built-in library function, such as sqrt.

Examples:
- Input: num = 16, Output: true (4 * 4 = 16)
- Input: num = 14, Output: false
"""

# SOLUTION 1: Binary Search (PREFERRED for interviews)
# Time: O(log n), Space: O(1)
def isPerfectSquare(num):
    """
    Binary search approach - most common interview solution
    Search for a number whose square equals num
    """
    if num < 1:
        return False
    
    left, right = 1, num
    
    while left <= right:
        mid = (left + right) // 2
        square = mid * mid
        
        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# SOLUTION 2: Optimized Binary Search
# Time: O(log n), Space: O(1)
def isPerfectSquare_optimized(num):
    """
    Binary search with optimized upper bound
    For num >= 4, sqrt(num) <= num/2, so we can reduce search space
    """
    if num < 1:
        return False
    if num == 1:
        return True
    
    left, right = 1, num // 2
    
    while left <= right:
        mid = (left + right) // 2
        square = mid * mid
        
        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# SOLUTION 3: Newton's Method
# Time: O(log n), Space: O(1)
def isPerfectSquare_newton(num):
    """
    Newton's method for finding square roots
    Faster convergence than binary search
    """
    if num < 1:
        return False
    
    x = num
    while x * x > num:
        x = (x + num // x) // 2
    
    return x * x == num


# SOLUTION 4: Mathematical Property (1 + 3 + 5 + ... = n²)
# Time: O(sqrt(n)), Space: O(1)
def isPerfectSquare_math(num):
    """
    Mathematical approach using the fact that:
    1² = 1
    2² = 1 + 3 = 4
    3² = 1 + 3 + 5 = 9
    4² = 1 + 3 + 5 + 7 = 16
    Perfect squares are sums of consecutive odd numbers
    """
    if num < 1:
        return False
    
    odd = 1
    while num > 0:
        num -= odd
        odd += 2
    
    return num == 0


# SOLUTION 5: Linear Search (Brute Force - mention as suboptimal)
# Time: O(sqrt(n)), Space: O(1)
def isPerfectSquare_linear(num):
    """
    Linear search - simple but inefficient
    Only mention to show you understand it's suboptimal
    """
    if num < 1:
        return False
    
    i = 1
    while i * i <= num:
        if i * i == num:
            return True
        i += 1
    
    return False


# SOLUTION 6: Bit Manipulation with Binary Search
# Time: O(log n), Space: O(1)
def isPerfectSquare_bits(num):
    """
    Binary search using bit operations
    Shows bit manipulation skills
    """
    if num < 1:
        return False
    
    left = 0
    right = 1
    
    # Find upper bound using bit shifting
    while right * right < num:
        left = right
        right <<= 1
    
    # Binary search between left and right
    while left <= right:
        mid = (left + right) >> 1
        square = mid * mid
        
        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# Test cases
def test_solutions():
    test_cases = [1, 4, 14, 16, 25, 808201, 2147395600]  # Include edge cases
    
    print("Testing all solutions:")
    for num in test_cases:
        result1 = isPerfectSquare(num)
        result2 = isPerfectSquare_optimized(num)
        result3 = isPerfectSquare_newton(num)
        result4 = isPerfectSquare_math(num)
        result5 = isPerfectSquare_linear(num)
        result6 = isPerfectSquare_bits(num)
        
        # Verify with built-in (for testing only)
        import math
        sqrt_val = int(math.sqrt(num))
        expected = sqrt_val * sqrt_val == num
        
        print(f"num = {num}")
        print(f"  Binary Search:     {result1}")
        print(f"  Optimized Binary:  {result2}")
        print(f"  Newton's:          {result3}")
        print(f"  Mathematical:      {result4}")
        print(f"  Linear:            {result5}")
        print(f"  Bit Manipulation:  {result6}")
        print(f"  Expected:          {expected}")
        print(f"  All match: {all([result1, result2, result3, result4, result5, result6]) == expected}")
        print()

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. START WITH BINARY SEARCH:
   - "I need to find if there exists an integer x such that x² = num"
   - "Since we're searching in a sorted space (1 to num), binary search is optimal"
   - "We can optimize by setting right = num//2 since sqrt(num) <= num/2 for num >= 4"
   - Time: O(log n), Space: O(1)

2. EDGE CASES TO MENTION:
   - num = 1 → return True (1² = 1)
   - Very large numbers → mention potential integer overflow with mid*mid

3. KEY DIFFERENCES FROM SQRT(X):
   - Here we need EXACT match (perfect square)
   - In Sqrt(x), we needed floor of square root
   - Return type is boolean, not integer

4. ALTERNATIVE APPROACHES (if time permits):
   - Newton's Method: "Faster convergence, good for very large numbers"
   - Mathematical Property: "Perfect squares = sum of consecutive odd numbers"
   - Linear Search: "O(sqrt(n)), too slow for large inputs"

5. OPTIMIZATION DISCUSSION:
   - "We can reduce search space from [1, num] to [1, num//2]"
   - "For num >= 4, sqrt(num) <= num/2"
   - "Be careful with integer overflow when computing mid*mid"

6. FOLLOW-UP QUESTIONS:
   - "What if num is very large?" → Discuss Newton's method or handling overflow
   - "Can you solve without multiplication?" → Show the mathematical approach
   - "How would you handle negative numbers?" → Problem states positive integers only

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem (positive integers, no built-in sqrt, exact match needed)
2. Explain binary search approach
3. Code the optimized binary search solution
4. Test with examples (1, 4, 14, 16)
5. Discuss time/space complexity
6. Mention alternative approaches if asked

COMMON MISTAKES TO AVOID:
- Don't confuse with Sqrt(x) problem - this needs exact match
- Handle num = 1 correctly
- Watch out for integer overflow with large numbers
- Remember to return boolean, not integer
"""
