"""
LeetCode 31. Next Permutation

Problem: Find the next lexicographically greater permutation of numbers.
If such arrangement is not possible, arrange it as the lowest possible order (sorted in ascending order).

Time Complexity: O(n)
Space Complexity: O(1)

Algorithm:
1. Find the largest index i such that nums[i] < nums[i + 1]
   If no such index exists, the permutation is the last permutation
2. Find the largest index j greater than i such that nums[i] < nums[j]
3. Swap nums[i] and nums[j]
4. Reverse the suffix starting at nums[i + 1]
"""

def nextPermutation(nums):
    """
    Do not return anything, modify nums in-place instead.
    """
    # Step 1: Find the pivot point
    # Look for the rightmost character that is smaller than its next character
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    
    # If no such character is found, we have the largest permutation
    # Just reverse the entire array to get the smallest permutation
    if i == -1:
        nums.reverse()
        return
    
    # Step 2: Find the smallest character on right side of above character 
    # that is greater than above character
    j = len(nums) - 1
    while nums[j] <= nums[i]:
        j -= 1
    
    # Step 3: Swap the found characters
    nums[i], nums[j] = nums[j], nums[i]
    
    # Step 4: Reverse the substring after position i
    nums[i + 1:] = reversed(nums[i + 1:])

# Alternative implementation with explicit reverse function
def nextPermutation_v2(nums):
    """
    More explicit version showing each step clearly
    """
    n = len(nums)
    
    # Step 1: Find pivot
    pivot = -1
    for i in range(n - 2, -1, -1):
        if nums[i] < nums[i + 1]:
            pivot = i
            break
    
    # If no pivot found, reverse entire array
    if pivot == -1:
        reverse(nums, 0, n - 1)
        return
    
    # Step 2: Find successor
    successor = -1
    for i in range(n - 1, pivot, -1):
        if nums[i] > nums[pivot]:
            successor = i
            break
    
    # Step 3: Swap pivot and successor
    nums[pivot], nums[successor] = nums[successor], nums[pivot]
    
    # Step 4: Reverse suffix
    reverse(nums, pivot + 1, n - 1)

def reverse(nums, start, end):
    """Helper function to reverse array from start to end"""
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1

# Test cases
def test_next_permutation():
    # Test case 1: [1,2,3] -> [1,3,2]
    nums1 = [1, 2, 3]
    nextPermutation(nums1)
    print(f"[1,2,3] -> {nums1}")  # Expected: [1,3,2]
    
    # Test case 2: [3,2,1] -> [1,2,3]
    nums2 = [3, 2, 1]
    nextPermutation(nums2)
    print(f"[3,2,1] -> {nums2}")  # Expected: [1,2,3]
    
    # Test case 3: [1,1,5] -> [1,5,1]
    nums3 = [1, 1, 5]
    nextPermutation(nums3)
    print(f"[1,1,5] -> {nums3}")  # Expected: [1,5,1]
    
    # Test case 4: [1] -> [1]
    nums4 = [1]
    nextPermutation(nums4)
    print(f"[1] -> {nums4}")  # Expected: [1]
    
    # Test case 5: [1,3,2] -> [2,1,3]
    nums5 = [1, 3, 2]
    nextPermutation(nums5)
    print(f"[1,3,2] -> {nums5}")  # Expected: [2,1,3]

if __name__ == "__main__":
    test_next_permutation()

"""
Key Interview Points to Mention:

1. Algorithm Intuition:
   - We need to find the "rightmost" position where we can make a small increase
   - This happens when we find a character smaller than its next character
   - We then find the smallest possible character to swap with it
   - Finally, we make the suffix as small as possible by reversing it

2. Edge Cases:
   - Array is already the largest permutation (descending order)
   - Single element array
   - Array with duplicates

3. Why this works:
   - By finding the rightmost pivot, we ensure minimal change
   - By swapping with the smallest valid successor, we get the next larger permutation
   - By reversing the suffix, we get the lexicographically smallest arrangement

4. Time/Space Complexity:
   - Time: O(n) - we scan the array at most 3 times
   - Space: O(1) - only using constant extra space

5. Alternative approaches and why they're worse:
   - Generate all permutations: O(n!) time
   - Use built-in next_permutation: Not available in all languages, less educational
"""
