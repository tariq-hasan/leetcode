def search(nums, target):
    """
    STANDARD BINARY SEARCH - Most Important Template
    
    Search for target in sorted array. Return index if found, -1 otherwise.
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    This is the fundamental binary search template you must know.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        # Avoid integer overflow (important in other languages)
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            # Target is in right half
            left = mid + 1
        else:
            # Target is in left half
            right = mid - 1
    
    # Target not found
    return -1


def searchAlternativeTemplate(nums, target):
    """
    ALTERNATIVE TEMPLATE: left < right
    
    Some prefer this template to avoid the <= comparison.
    Both templates are valid - choose one and be consistent.
    """
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    # Check if we found the target
    if left < len(nums) and nums[left] == target:
        return left
    
    return -1


def searchRecursive(nums, target):
    """
    RECURSIVE BINARY SEARCH
    
    Same time complexity but O(log n) space due to call stack.
    Less preferred in interviews due to space usage.
    """
    def binarySearchHelper(left, right):
        if left > right:
            return -1
        
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return binarySearchHelper(mid + 1, right)
        else:
            return binarySearchHelper(left, mid - 1)
    
    return binarySearchHelper(0, len(nums) - 1)


# BINARY SEARCH FUNDAMENTALS:
"""
THE GOLDEN RULE OF BINARY SEARCH:

The search space must be SORTED and we must be able to eliminate 
half of the remaining elements at each step.

KEY COMPONENTS:

1. INITIALIZATION:
   - left = 0, right = len(nums) - 1 (inclusive bounds)
   - OR left = 0, right = len(nums) (exclusive right bound)

2. LOOP CONDITION:
   - while left <= right (for inclusive bounds)
   - OR while left < right (for exclusive right bound)

3. MID CALCULATION:
   - mid = left + (right - left) // 2
   - Avoids overflow: DON'T use (left + right) // 2

4. COMPARISON & UPDATE:
   - If nums[mid] == target: return mid
   - If nums[mid] < target: left = mid + 1 (search right)
   - If nums[mid] > target: right = mid - 1 (search left)

COMMON MISTAKES TO AVOID:

1. INTEGER OVERFLOW:
   ❌ mid = (left + right) // 2
   ✅ mid = left + (right - left) // 2

2. INFINITE LOOPS:
   ❌ Incorrect boundary updates
   ✅ Always make progress: left = mid + 1 or right = mid - 1

3. OFF-BY-ONE ERRORS:
   ❌ Mixing inclusive/exclusive bound conventions
   ✅ Be consistent with your chosen template

4. WRONG RETURN VALUE:
   ❌ Returning mid when target not found
   ✅ Return -1 when loop ends without finding target

TEMPLATE CHOICE:

Template 1 (left <= right): More intuitive, widely used
Template 2 (left < right): Avoids some edge cases, preferred by some

Choose ONE template and stick with it consistently!

TIME COMPLEXITY ANALYSIS:

- Best case: O(1) - target is at middle
- Average case: O(log n) - need log₂(n) comparisons
- Worst case: O(log n) - target at boundary or not found

Why O(log n)?
Each iteration eliminates half the search space:
n → n/2 → n/4 → n/8 → ... → 1
This takes log₂(n) steps.

SPACE COMPLEXITY:
- Iterative: O(1) - only using a few variables
- Recursive: O(log n) - due to call stack depth

INTERVIEW STRATEGY:
1. Always start with the standard iterative template
2. Walk through a concrete example
3. Discuss time/space complexity
4. Mention the overflow-safe mid calculation
5. Be ready for variations (find first/last occurrence, rotated arrays, etc.)
"""
