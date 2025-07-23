# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

def firstBadVersion(n: int) -> int:
    """
    Find the first bad version using binary search.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Key insight: All versions after the first bad version are also bad.
    This creates a sorted pattern: [good, good, ..., good, bad, bad, ..., bad]
    We need to find the first occurrence of 'bad'.
    """
    left, right = 1, n
    
    while left < right:
        # Use left + (right - left) // 2 to avoid integer overflow
        mid = left + (right - left) // 2
        
        if isBadVersion(mid):
            # mid is bad, so first bad version is at mid or before
            # Don't exclude mid as it could be the answer
            right = mid
        else:
            # mid is good, so first bad version is after mid
            left = mid + 1
    
    # When left == right, we found the first bad version
    return left


# Alternative implementation with left <= right pattern
def firstBadVersionAlternative(n: int) -> int:
    """
    Alternative binary search implementation.
    Same time/space complexity but slightly different structure.
    """
    left, right = 1, n
    result = n
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if isBadVersion(mid):
            result = mid  # Store potential answer
            right = mid - 1  # Look for earlier bad version
        else:
            left = mid + 1  # Look for bad version in right half
    
    return result


# COMMON MISTAKES TO AVOID:
"""
1. INTEGER OVERFLOW:
   ❌ mid = (left + right) // 2  # Can overflow in other languages
   ✅ mid = left + (right - left) // 2

2. INFINITE LOOP:
   ❌ right = mid + 1 when isBadVersion(mid) is True
   ✅ right = mid (don't exclude the potential answer)

3. WRONG RETURN VALUE:
   ❌ return mid (might return when left != right)
   ✅ return left (when left == right, we found the answer)

4. OFF-BY-ONE ERRORS:
   ❌ while left <= right with right = mid
   ✅ while left < right with right = mid
"""

# INTERVIEW TALKING POINTS:
"""
1. PROBLEM PATTERN: This is a "find first occurrence" binary search problem

2. KEY INSIGHT: The versions form a sorted pattern where all good versions 
   come before all bad versions

3. WHY BINARY SEARCH: Linear search would be O(n), binary search is O(log n)

4. TEMPLATE: This uses the "left < right" template which is safer for 
   "find first" problems as it avoids infinite loops

5. ALTERNATIVE APPROACHES: 
   - Linear search: O(n) time
   - Binary search: O(log n) time ← Optimal solution
"""
