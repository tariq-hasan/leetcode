def nextGreatestLetter(letters, target):
    """
    SOLUTION 1: Binary Search - "Find First Greater" Pattern
    
    This is the MOST IMPORTANT solution for big tech interviews.
    It uses the "find first occurrence" binary search template.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(letters)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if letters[mid] <= target:
            # Current letter is too small, search right half
            left = mid + 1
        else:
            # Current letter might be the answer, keep it in search space
            right = mid
    
    # Handle wrap-around: if left == len(letters), return first letter
    return letters[left % len(letters)]


def nextGreatestLetterAlternative(letters, target):
    """
    SOLUTION 2: Binary Search - Traditional Template
    
    Alternative approach using the standard binary search template.
    Good to know but Solution 1 is cleaner for this problem.
    """
    left, right = 0, len(letters) - 1
    result = letters[0]  # Default wrap-around answer
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if letters[mid] > target:
            result = letters[mid]  # Potential answer
            right = mid - 1  # Look for smaller valid answer
        else:
            left = mid + 1  # Need something larger
    
    return result


def nextGreatestLetterLinear(letters, target):
    """
    SOLUTION 3: Linear Search - Simple but not optimal
    
    Mention this as the brute force approach, then optimize to binary search.
    Time: O(n), Space: O(1)
    """
    for letter in letters:
        if letter > target:
            return letter
    
    # Wrap around to first letter
    return letters[0]


def nextGreatestLetterBuiltIn(letters, target):
    """
    SOLUTION 4: Using Built-in bisect (Python specific)
    
    Good to mention you know about it, but implement binary search manually.
    """
    import bisect
    
    # Find insertion point for target
    idx = bisect.bisect_right(letters, target)
    
    # Handle wrap-around
    return letters[idx % len(letters)]


# ALGORITHM ANALYSIS FOR INTERVIEWS:
"""
PROBLEM PATTERN: "Find First Greater Element" with Wrap-Around

This problem combines two important concepts:
1. Binary search for "find first occurrence" pattern
2. Circular array handling (wrap-around)

KEY INSIGHTS:

1. PROBLEM TRANSFORMATION:
   - We're looking for the first letter that is > target
   - If no such letter exists, wrap around to letters[0]

2. WHY SOLUTION 1 IS OPTIMAL:
   - Uses the "left < right" template which is perfect for "find first" problems
   - Handles wrap-around elegantly with modulo operator
   - No need to track separate result variable

3. BINARY SEARCH TEMPLATE CHOICE:
   Template: left < right, right = len(letters)
   - When letters[mid] <= target: left = mid + 1 (exclude mid)
   - When letters[mid] > target: right = mid (keep mid as potential answer)

4. WRAP-AROUND HANDLING:
   - If left == len(letters), no letter > target exists
   - Return letters[left % len(letters)] = letters[0]

INTERVIEW TALKING POINTS:

1. APPROACH EVOLUTION:
   "I'll start with the brute force O(n) linear scan, then optimize to O(log n) binary search."

2. PATTERN RECOGNITION:
   "This is a 'find first greater' problem, which is a common binary search variant."

3. EDGE CASES:
   - Target smaller than all letters → return first letter
   - Target larger than all letters → wrap around to first letter
   - Target equals some letters → find first letter that's strictly greater
   - All letters are the same → wrap around

4. WHY BINARY SEARCH:
   "The array is sorted, so we can eliminate half the search space at each step."

5. COMPLEXITY ANALYSIS:
   - Time: O(log n) - binary search
   - Space: O(1) - only using a few variables

COMMON VARIATIONS TO EXPECT:

1. "What if we wanted the smallest letter >= target?" 
   → Change condition from letters[mid] <= target to letters[mid] < target

2. "What if there was no wrap-around?"
   → Return -1 or some sentinel value when left == len(letters)

3. "What about finding the largest letter < target?"
   → Similar approach but search for "last smaller" instead

4. "How would you handle duplicates?"
   → Current solution already handles duplicates correctly

IMPLEMENTATION STRATEGY:
1. Start with the main binary search solution (Solution 1)
2. Walk through the example step by step
3. Explain the wrap-around logic
4. Discuss time/space complexity
5. Mention edge cases and how they're handled

The key is to demonstrate mastery of the "find first occurrence" binary search pattern,
which appears in many other problems!
"""
