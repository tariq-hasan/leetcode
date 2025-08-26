"""
LeetCode 69. Sqrt(x)
Problem: Given a non-negative integer x, return the square root of x rounded down to the nearest integer.
The returned integer should be non-negative as well.
You must not use any built-in exponent function or operator.

Examples:
- Input: x = 4, Output: 2
- Input: x = 8, Output: 2 (since sqrt(8) = 2.82..., rounded down to 2)
"""

# SOLUTION 1: Binary Search (PREFERRED for interviews)
# Time: O(log n), Space: O(1)
def mySqrt(x):
    """
    Binary search approach - most elegant and efficient
    This is what interviewers typically expect
    """
    if x < 2:
        return x
    
    left, right = 1, x // 2
    
    while left <= right:
        mid = (left + right) // 2
        square = mid * mid
        
        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1
    
    # When loop ends, right is the largest integer whose square <= x
    return right


# SOLUTION 2: Newton's Method (Advanced optimization)
# Time: O(log n), Space: O(1)
def mySqrt_newton(x):
    """
    Newton's method for finding square roots
    Faster convergence than binary search
    """
    if x < 2:
        return x
    
    # Initial guess
    guess = x
    
    while guess * guess > x:
        # Newton's formula: next_guess = (guess + x/guess) / 2
        guess = (guess + x // guess) // 2
    
    return guess


# SOLUTION 3: Linear Search (Brute Force - for completeness)
# Time: O(sqrt(n)), Space: O(1)
def mySqrt_linear(x):
    """
    Linear search - simple but inefficient
    Only mention this to show you know it's suboptimal
    """
    if x < 2:
        return x
    
    i = 1
    while i * i <= x:
        i += 1
    
    return i - 1


# SOLUTION 4: Bit Manipulation (Show advanced knowledge)
# Time: O(log n), Space: O(1)
def mySqrt_bits(x):
    """
    Bit manipulation approach
    Good to mention for showing bit manipulation skills
    """
    if x < 2:
        return x
    
    # Find the position of the most significant bit
    # This gives us an upper bound for our answer
    left = 1
    right = 1
    while right * right <= x:
        right <<= 1
    
    # Now do binary search between left and right
    left = right >> 1
    
    while left <= right:
        mid = (left + right) >> 1
        square = mid * mid
        
        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right


# Test cases
def test_solutions():
    test_cases = [0, 1, 4, 8, 16, 24, 2147395599]  # Include edge cases
    
    print("Testing all solutions:")
    for x in test_cases:
        result1 = mySqrt(x)
        result2 = mySqrt_newton(x)
        result3 = mySqrt_linear(x)
        result4 = mySqrt_bits(x)
        
        print(f"x = {x}")
        print(f"  Binary Search: {result1}")
        print(f"  Newton's:      {result2}")
        print(f"  Linear:        {result3}")
        print(f"  Bit Manip:     {result4}")
        print(f"  Built-in:      {int(x**0.5)}")
        print()

if __name__ == "__main__":
    test_solutions()


"""
INTERVIEW TALKING POINTS:

1. START WITH BINARY SEARCH:
   - "I'll use binary search since we're looking for a target value in a sorted range"
   - "The search space is from 1 to x/2 (since sqrt(x) <= x/2 for x >= 4)"
   - Time: O(log n), Space: O(1)

2. EDGE CASES TO MENTION:
   - x = 0 → return 0
   - x = 1 → return 1
   - Large numbers (mention integer overflow if using mid*mid)

3. OPTIMIZATION (if time permits):
   - "We could also use Newton's method for faster convergence"
   - "For very performance-critical applications, bit manipulation could be faster"

4. ALTERNATIVE APPROACHES:
   - Linear search: O(sqrt(n)) - mention it's too slow
   - Built-in functions: Not allowed per problem constraints

5. FOLLOW-UP QUESTIONS YOU MIGHT GET:
   - "What about floating point precision?" → Discuss how we handle rounding down
   - "How would you handle negative inputs?" → Problem states non-negative
   - "Can you optimize further?" → Mention Newton's method or bit tricks

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem (non-negative integers, round down, no built-ins)
2. Discuss approach (binary search)
3. Code the binary search solution
4. Test with examples
5. Discuss time/space complexity
6. Mention alternative approaches if asked
"""
