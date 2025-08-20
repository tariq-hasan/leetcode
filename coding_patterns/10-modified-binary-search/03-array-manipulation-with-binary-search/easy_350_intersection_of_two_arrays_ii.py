"""
LeetCode 350: Intersection of Two Arrays II

Problem: Given two integer arrays nums1 and nums2, return an array of their intersection.
Each element in the result should appear as many times as it shows in both arrays.
The result can be in any order.

Key Difference from 349: We need to include duplicates based on frequency in both arrays.
"""

def intersect_frequency_map(nums1, nums2):
    """
    Approach 1: Frequency Map/Counter (Most Common Interview Solution)
    
    Time Complexity: O(m + n)
    Space Complexity: O(min(m, n)) for the frequency map
    
    Strategy: Count frequencies in one array, then decrement while iterating the other
    """
    from collections import Counter
    
    # Optimization: Use smaller array for the frequency map
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    # Count frequencies in nums1
    freq = Counter(nums1)
    result = []
    
    # Iterate through nums2 and collect intersection
    for num in nums2:
        if freq[num] > 0:
            result.append(num)
            freq[num] -= 1  # Decrement frequency
    
    return result


def intersect_manual_dict(nums1, nums2):
    """
    Approach 2: Manual Dictionary Implementation
    
    Time Complexity: O(m + n)
    Space Complexity: O(min(m, n))
    
    Best for: Showing understanding without using Counter
    """
    # Use smaller array for frequency counting (space optimization)
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    # Manual frequency counting
    freq = {}
    for num in nums1:
        freq[num] = freq.get(num, 0) + 1
    
    result = []
    for num in nums2:
        if freq.get(num, 0) > 0:
            result.append(num)
            freq[num] -= 1
    
    return result


def intersect_two_pointers(nums1, nums2):
    """
    Approach 3: Two Pointers (After Sorting)
    
    Time Complexity: O(m log m + n log n) due to sorting
    Space Complexity: O(1) if not counting output, O(log m + log n) for sorting
    
    Best for: When asked to minimize space or arrays come pre-sorted
    """
    nums1.sort()
    nums2.sort()
    
    i = j = 0
    result = []
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            i += 1
        elif nums1[i] > nums2[j]:
            j += 1
        else:  # nums1[i] == nums2[j]
            result.append(nums1[i])
            i += 1
            j += 1
    
    return result


def intersect_space_optimized(nums1, nums2):
    """
    Approach 4: Space-Optimized for Large Arrays
    
    Time Complexity: O(m + n)
    Space Complexity: O(1) extra space if we can modify input arrays
    
    Best for: When space is extremely limited
    Note: This modifies the input arrays
    """
    # Sort both arrays in-place
    nums1.sort()
    nums2.sort()
    
    # Use the two-pointer approach
    return intersect_two_pointers(nums1, nums2)


def intersect_follow_up_streaming(nums1, nums2_stream):
    """
    Follow-up: What if nums2 is a stream (elements come one by one)?
    
    Approach: Build frequency map from nums1, process stream elements
    """
    from collections import Counter
    
    freq = Counter(nums1)
    result = []
    
    # Simulate streaming processing
    for num in nums2_stream:
        if freq[num] > 0:
            result.append(num)
            freq[num] -= 1
    
    return result


def intersect_follow_up_disk_chunks(nums1, nums2, chunk_size=1000):
    """
    Follow-up: What if nums2 is stored on disk and memory is limited?
    
    Approach: Process nums2 in chunks while maintaining frequency map from nums1
    """
    from collections import Counter
    
    freq1 = Counter(nums1)
    result = []
    
    # Process nums2 in chunks
    for i in range(0, len(nums2), chunk_size):
        chunk = nums2[i:i + chunk_size]
        
        for num in chunk:
            if freq1[num] > 0:
                result.append(num)
                freq1[num] -= 1
        
        # Early termination optimization
        if not any(freq1.values()):
            break
    
    return result


def intersect_follow_up_sorted_memory_limited(nums1, nums2):
    """
    Follow-up: Arrays are sorted, but memory is limited
    
    Approach: External merge-like algorithm processing chunks
    """
    def merge_intersect_chunk(chunk1, chunk2):
        """Helper to find intersection of two sorted chunks"""
        i = j = 0
        result = []
        
        while i < len(chunk1) and j < len(chunk2):
            if chunk1[i] < chunk2[j]:
                i += 1
            elif chunk1[i] > chunk2[j]:
                j += 1
            else:
                result.append(chunk1[i])
                i += 1
                j += 1
        
        return result
    
    # For demo, process in chunks (in real scenario, read from disk)
    chunk_size = max(1, min(len(nums1), len(nums2)) // 3)
    result = []
    
    # This is a simplified version - real implementation would be more complex
    for i in range(0, len(nums1), chunk_size):
        chunk1 = nums1[i:i + chunk_size]
        for j in range(0, len(nums2), chunk_size):
            chunk2 = nums2[j:j + chunk_size]
            chunk_result = merge_intersect_chunk(chunk1, chunk2)
            result.extend(chunk_result)
    
    return result


# Test cases
def test_solutions():
    test_cases = [
        {
            "nums1": [1, 2, 2, 1],
            "nums2": [2, 2],
            "expected": [2, 2]
        },
        {
            "nums1": [4, 9, 5],
            "nums2": [9, 4, 9, 8, 4],
            "expected": [4, 9]  # or [9, 4] - order doesn't matter
        },
        {
            "nums1": [1, 2, 2, 1],
            "nums2": [2],
            "expected": [2]
        },
        {
            "nums1": [3, 1, 2],
            "nums2": [1, 1],
            "expected": [1]
        },
        {
            "nums1": [1, 1, 1, 1],
            "nums2": [1, 1],
            "expected": [1, 1]
        },
        {
            "nums1": [],
            "nums2": [1, 2],
            "expected": []
        }
    ]
    
    solutions = [
        ("Frequency Map", intersect_frequency_map),
        ("Manual Dict", intersect_manual_dict),
        ("Two Pointers", intersect_two_pointers),
    ]
    
    for i, test in enumerate(test_cases):
        print(f"Test Case {i + 1}: nums1={test['nums1']}, nums2={test['nums2']}")
        print(f"Expected: {test['expected']}")
        
        for name, solution in solutions:
            # Create copies since some solutions modify input
            nums1_copy = test['nums1'][:]
            nums2_copy = test['nums2'][:]
            
            result = solution(nums1_copy, nums2_copy)
            
            # Check if result matches expected (frequency matters, order doesn't)
            from collections import Counter
            is_correct = Counter(result) == Counter(test['expected'])
            print(f"{name:15}: {result} {'✓' if is_correct else '✗'}")
        
        print("-" * 60)


def demonstrate_follow_ups():
    """Demonstrate follow-up scenarios"""
    print("Follow-up Demonstrations:")
    print("=" * 50)
    
    # Follow-up 1: Streaming
    print("1. Streaming nums2:")
    nums1 = [1, 2, 2, 1]
    nums2_stream = [2, 2, 3, 1]  # Stream of elements
    result = intersect_follow_up_streaming(nums1, nums2_stream)
    print(f"   nums1: {nums1}, stream: {nums2_stream}")
    print(f"   Result: {result}")
    print()
    
    # Follow-up 2: Disk storage with chunks
    print("2. nums2 stored on disk (chunked processing):")
    nums1 = [1, 2, 2, 1, 3, 3]
    nums2 = [2, 2, 1, 3, 4, 5, 6, 3]
    result = intersect_follow_up_disk_chunks(nums1, nums2, chunk_size=3)
    print(f"   nums1: {nums1}")
    print(f"   nums2 (on disk): {nums2}")
    print(f"   Result: {result}")
    print()
    
    # Follow-up 3: Both arrays sorted but memory limited
    print("3. Sorted arrays with memory constraints:")
    nums1 = [1, 2, 2, 3, 4, 4]
    nums2 = [2, 2, 3, 4, 4, 5]
    result = intersect_follow_up_sorted_memory_limited(nums1, nums2)
    print(f"   Sorted nums1: {nums1}")
    print(f"   Sorted nums2: {nums2}")
    print(f"   Result: {result}")


if __name__ == "__main__":
    test_solutions()
    print("\n")
    demonstrate_follow_ups()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Key difference from problem 349: Include duplicates based on frequency
   - Result frequency = min(freq_in_nums1, freq_in_nums2) for each element

2. APPROACH SELECTION:
   
   Primary Approaches (choose based on constraints):
   
   a) Frequency Map - O(m+n) time, O(min(m,n)) space
      - Best general solution
      - Easy to understand and implement
      - Optimal time complexity
   
   b) Two Pointers - O(m log m + n log n) time, O(1) space
      - When space is limited
      - When arrays are already sorted
      - When you can't use extra data structures

3. OPTIMIZATION TECHNIQUES:
   - Always use smaller array for frequency map (space optimization)
   - Early termination when frequency map becomes empty
   - Consider input characteristics (sorted, size difference, etc.)

4. FOLLOW-UP QUESTIONS (Very Important for Big Tech):
   
   a) "What if nums1's size is small compared to nums2's size?"
      → Use frequency map on nums1, iterate through nums2
   
   b) "What if elements of nums2 are stored on disk?"
      → Process nums2 in chunks, maintain frequency map of nums1 in memory
   
   c) "What if both arrays are so large that you cannot load all elements into memory?"
      → External sorting + merge-like approach with chunked processing
   
   d) "What if nums2 is a stream of elements?"
      → Build frequency map from nums1, process stream elements one by one

5. EDGE CASES:
   - Empty arrays
   - No intersection
   - One array is subset of another
   - Arrays with different sizes
   - All elements are the same

6. CODE QUALITY POINTS:
   - Handle edge cases gracefully
   - Use descriptive variable names
   - Add comments for complex logic
   - Consider space optimizations (use smaller array for map)

7. TIME/SPACE TRADE-OFF DISCUSSION:
   - Hash map approach: Better time, more space
   - Two pointer approach: Better space, more time (due to sorting)
   - Discuss when each approach is preferred

RECOMMENDED INTERVIEW FLOW:
1. Clarify requirements (duplicates, order, constraints)
2. Start with frequency map approach (most intuitive)
3. Code it cleanly with optimizations
4. Discuss time/space complexity
5. Present two-pointer alternative if space is constrained
6. Be ready to handle follow-up scenarios
7. Test with edge cases

This problem is excellent for demonstrating:
- Understanding of hash maps vs arrays
- Space-time trade-offs
- Real-world system constraints (streaming, disk storage)
- Code optimization skills
"""
