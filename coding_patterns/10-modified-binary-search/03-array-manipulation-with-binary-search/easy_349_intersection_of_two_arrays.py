"""
LeetCode 349: Intersection of Two Arrays

Problem: Given two integer arrays nums1 and nums2, return an array of their intersection.
Each element in the result must be unique and you may return the result in any order.

Multiple approaches with different time/space trade-offs
"""

def intersection_set_builtin(nums1, nums2):
    """
    Approach 1: Built-in Set Operations (Most Pythonic)
    
    Time Complexity: O(m + n)
    Space Complexity: O(m + n) for the sets
    
    Best for: Clean, readable code in interviews
    """
    return list(set(nums1) & set(nums2))


def intersection_set_manual(nums1, nums2):
    """
    Approach 2: Manual Set Implementation
    
    Time Complexity: O(m + n)
    Space Complexity: O(m) for the set, O(k) for result where k = intersection size
    
    Best for: Showing understanding of hash table operations
    """
    # Convert smaller array to set for better space efficiency
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    seen = set(nums1)
    result = []
    
    for num in nums2:
        if num in seen:
            result.append(num)
            seen.remove(num)  # Remove to ensure uniqueness
    
    return result


def intersection_two_pointers(nums1, nums2):
    """
    Approach 3: Two Pointers (After Sorting)
    
    Time Complexity: O(m log m + n log n) due to sorting
    Space Complexity: O(1) if not counting output array, O(log m + log n) for sorting
    
    Best for: When asked to minimize space or if arrays come pre-sorted
    """
    nums1.sort()
    nums2.sort()
    
    i, j = 0, 0
    result = []
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            i += 1
        elif nums1[i] > nums2[j]:
            j += 1
        else:  # nums1[i] == nums2[j]
            # Add to result if not already added (handle duplicates)
            if not result or result[-1] != nums1[i]:
                result.append(nums1[i])
            i += 1
            j += 1
    
    return result


def intersection_binary_search(nums1, nums2):
    """
    Approach 4: Binary Search
    
    Time Complexity: O(m log n) or O(n log m) depending on which array we search
    Space Complexity: O(m) for the set of nums1, O(k) for result
    
    Best for: When one array is much larger than the other
    """
    # Use smaller array for the set, search in the larger sorted array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    nums2.sort()  # Sort the array we'll binary search in
    seen = set()
    result = []
    
    def binary_search(arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return True
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False
    
    for num in nums1:
        if num not in seen and binary_search(nums2, num):
            result.append(num)
            seen.add(num)  # Ensure uniqueness
    
    return result


def intersection_frequency_map(nums1, nums2):
    """
    Approach 5: Frequency Map (Good for follow-up questions)
    
    Time Complexity: O(m + n)
    Space Complexity: O(m) for the frequency map
    
    Best for: When you need to extend to intersection with frequencies
    """
    from collections import Counter
    
    freq1 = Counter(nums1)
    result = []
    
    for num in nums2:
        if num in freq1 and freq1[num] > 0:
            result.append(num)
            freq1[num] = 0  # Mark as used to ensure uniqueness
    
    return result


# Test cases
def test_solutions():
    test_cases = [
        {
            "nums1": [1, 2, 2, 1],
            "nums2": [2, 2],
            "expected": [2]
        },
        {
            "nums1": [4, 9, 5],
            "nums2": [9, 4, 9, 8, 4],
            "expected": [9, 4]  # or [4, 9]
        },
        {
            "nums1": [1, 2, 3],
            "nums2": [4, 5, 6],
            "expected": []
        },
        {
            "nums1": [1],
            "nums2": [1],
            "expected": [1]
        },
        {
            "nums1": [1, 2, 3, 4, 5],
            "nums2": [1, 3, 5, 7, 9],
            "expected": [1, 3, 5]  # order may vary
        }
    ]
    
    solutions = [
        ("Set Built-in", intersection_set_builtin),
        ("Set Manual", intersection_set_manual),
        ("Two Pointers", intersection_two_pointers),
        ("Binary Search", intersection_binary_search),
        ("Frequency Map", intersection_frequency_map)
    ]
    
    for i, test in enumerate(test_cases):
        print(f"Test Case {i + 1}: nums1={test['nums1']}, nums2={test['nums2']}")
        print(f"Expected: {test['expected']}")
        
        for name, solution in solutions:
            # Create copies since some solutions modify input
            nums1_copy = test['nums1'][:]
            nums2_copy = test['nums2'][:]
            
            result = solution(nums1_copy, nums2_copy)
            
            # Check if result matches expected (order doesn't matter)
            is_correct = set(result) == set(test['expected'])
            print(f"{name:15}: {result} {'✓' if is_correct else '✗'}")
        
        print("-" * 50)


# Space-optimized version for follow-up questions
def intersection_space_optimized(nums1, nums2):
    """
    Follow-up: What if elements of nums2 are stored on disk, 
    and the memory is limited such that you cannot load all elements into memory?
    
    Approach: Process nums2 in chunks
    """
    def process_chunk(chunk, nums1_set):
        """Process a chunk of nums2"""
        chunk_result = []
        for num in chunk:
            if num in nums1_set:
                chunk_result.append(num)
                nums1_set.discard(num)  # Remove to avoid duplicates
        return chunk_result
    
    nums1_set = set(nums1)
    result = []
    
    # Simulate processing nums2 in chunks
    chunk_size = max(1, len(nums2) // 3)  # Process in 3 chunks for demo
    
    for i in range(0, len(nums2), chunk_size):
        chunk = nums2[i:i + chunk_size]
        chunk_result = process_chunk(chunk, nums1_set)
        result.extend(chunk_result)
        
        # Early termination if nums1_set is empty
        if not nums1_set:
            break
    
    return result


if __name__ == "__main__":
    test_solutions()
    
    # Demonstrate space-optimized approach
    print("\nSpace-Optimized Approach Demo:")
    result = intersection_space_optimized([1, 2, 2, 1], [2, 2, 3, 4, 2])
    print(f"Result: {result}")


"""
Interview Discussion Points:

1. APPROACH SELECTION:
   - Set operations: Best for general case, clean code
   - Two pointers: Good when space is limited or arrays are sorted
   - Binary search: When one array is much larger than the other
   - Frequency map: When you need to extend to duplicates later

2. TIME/SPACE TRADE-OFFS:
   - Hash set: O(m+n) time, O(min(m,n)) space
   - Two pointers: O(m log m + n log n) time, O(1) space
   - Binary search: O(m log n) time, O(m) space

3. FOLLOW-UP QUESTIONS:
   - What if the result needs to include duplicates? → Use Counter
   - What if arrays are already sorted? → Use two pointers
   - What if one array is much larger? → Use binary search
   - What if nums2 is stored on disk? → Process in chunks

4. EDGE CASES:
   - Empty arrays
   - No intersection
   - One element arrays
   - All elements are duplicates

5. OPTIMIZATION CONSIDERATIONS:
   - Always process smaller array first when using hash sets
   - Use early termination when possible
   - Consider input characteristics (sorted, size difference, etc.)

Recommended approach for interviews:
1. Start with set intersection (clean and efficient)
2. Discuss trade-offs
3. Code alternative if asked for space optimization
"""
