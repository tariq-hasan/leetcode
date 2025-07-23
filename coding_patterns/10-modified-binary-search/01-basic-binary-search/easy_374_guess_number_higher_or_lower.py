# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

def guessNumber(n: int) -> int:
    """
    Find the picked number using binary search.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    The guess API returns:
    - -1: your guess is too high
    -  1: your guess is too low  
    -  0: correct guess
    """
    left, right = 1, n
    
    while left <= right:
        # Avoid potential integer overflow
        mid = left + (right - left) // 2
        
        result = guess(mid)
        
        if result == 0:
            return mid  # Found the number!
        elif result == -1:
            # Guess is too high, search lower half
            right = mid - 1
        else:  # result == 1
            # Guess is too low, search upper half
            left = mid + 1
    
    # Should never reach here given problem constraints
    return -1


# Alternative implementation using left < right pattern
def guessNumberAlternative(n: int) -> int:
    """
    Alternative implementation using left < right pattern.
    Some prefer this to avoid the <= comparison.
    """
    left, right = 1, n + 1  # Note: right = n + 1
    
    while left < right:
        mid = left + (right - left) // 2
        result = guess(mid)
        
        if result == 0:
            return mid
        elif result == -1:
            # Too high, search left half
            right = mid
        else:
            # Too low, search right half  
            left = mid + 1
    
    return left


# Recursive solution (less preferred due to space complexity)
def guessNumberRecursive(n: int) -> int:
    """
    Recursive binary search solution.
    Time: O(log n), Space: O(log n) due to call stack
    """
    def binary_search(left, right):
        if left > right:
            return -1
        
        mid = left + (right - left) // 2
        result = guess(mid)
        
        if result == 0:
            return mid
        elif result == -1:
            return binary_search(left, mid - 1)
        else:
            return binary_search(mid + 1, right)
    
    return binary_search(1, n)


# KEY INTERVIEW POINTS:
"""
1. RECOGNIZE THE PATTERN: This is classic binary search with API interaction

2. API UNDERSTANDING:
   - guess(num) == -1: your guess is too high
   - guess(num) == 1: your guess is too low
   - guess(num) == 0: correct answer

3. WHY BINARY SEARCH: Reduces O(n) linear search to O(log n)

4. INTEGER OVERFLOW: Use left + (right - left) // 2

5. EDGE CASES: n=1, picked number at boundaries

6. FOLLOW-UP: What if the API had a cost per call? (Same approach, minimize calls)
"""
