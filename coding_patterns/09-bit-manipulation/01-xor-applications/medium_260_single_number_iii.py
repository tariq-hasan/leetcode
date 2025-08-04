"""
LeetCode 260: Single Number III
Problem: Given an integer array where every element appears exactly twice 
except for two elements which appear exactly once. Find the two single elements.

Must solve in O(n) time and O(1) extra space.

Key Insight: Use XOR to find XOR of the two unique numbers, then use a 
distinguishing bit to separate them into two groups.
"""

from typing import List
from collections import Counter

class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        """
        Solution 1: Two-Pass XOR with Bit Separation (Standard)
        
        Step 1: XOR all numbers to get xor_result = a ^ b (where a, b are the two unique numbers)
        Step 2: Find any bit position where a and b differ
        Step 3: Use this bit to separate numbers into two groups and XOR each group
        
        Time: O(n), Space: O(1)
        """
        # Step 1: XOR all numbers to get a ^ b
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Step 2: Find the rightmost set bit (where a and b differ)
        # This bit is 1 in exactly one of the two unique numbers
        rightmost_set_bit = xor_all & (-xor_all)
        
        # Step 3: Separate numbers into two groups based on this bit
        group1_xor = group2_xor = 0
        
        for num in nums:
            if num & rightmost_set_bit:
                group1_xor ^= num  # Numbers with this bit set
            else:
                group2_xor ^= num  # Numbers without this bit set
        
        return [group1_xor, group2_xor]

    def singleNumber_optimized(self, nums: List[int]) -> List[int]:
        """
        Solution 2: Single-Pass Optimized Version
        Same logic but optimized for fewer variables and cleaner code
        """
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Find rightmost set bit using bit manipulation trick
        diff_bit = xor_all & (-xor_all)
        
        # Separate into two groups and find the unique numbers
        result = [0, 0]
        for num in nums:
            if num & diff_bit:
                result[0] ^= num
            else:
                result[1] ^= num
        
        return result

    def singleNumber_with_any_bit(self, nums: List[int]) -> List[int]:
        """
        Solution 3: Using Any Distinguishing Bit (Not Just Rightmost)
        Shows understanding that any bit where the two numbers differ works
        """
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Find any set bit (here we use leftmost for variety)
        distinguishing_bit = 1
        while not (xor_all & distinguishing_bit):
            distinguishing_bit <<= 1
        
        a = b = 0
        for num in nums:
            if num & distinguishing_bit:
                a ^= num
            else:
                b ^= num
        
        return [a, b]

    def singleNumber_with_explanation(self, nums: List[int]) -> List[int]:
        """
        Solution 4: Step-by-Step with Detailed Comments
        Best for explaining during interview
        """
        # Phase 1: Find XOR of the two unique numbers
        combined_xor = 0
        for num in nums:
            combined_xor ^= num
        # Now combined_xor = a ^ b where a and b are our target numbers
        
        # Phase 2: Find a bit position where a and b differ
        # We know combined_xor has at least one bit set (since a != b)
        # Find the rightmost set bit using the formula: x & (-x)
        separating_bit = combined_xor & (-combined_xor)
        
        # Phase 3: Use this bit to partition numbers into two groups
        # Group 1: numbers with separating_bit set
        # Group 2: numbers with separating_bit not set
        # Since pairs are identical, they'll go to the same group
        # The two unique numbers will go to different groups
        
        first_unique = second_unique = 0
        
        for num in nums:
            if num & separating_bit:
                first_unique ^= num   # XOR all numbers in group 1
            else:
                second_unique ^= num  # XOR all numbers in group 2
        
        return [first_unique, second_unique]

    def singleNumber_bit_by_bit(self, nums: List[int]) -> List[int]:
        """
        Solution 5: Alternative Approach - Check Each Bit Position
        Less efficient but shows different thinking approach
        """
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Find first bit position where the two numbers differ
        bit_pos = 0
        while not (xor_all & (1 << bit_pos)):
            bit_pos += 1
        
        mask = 1 << bit_pos
        
        group1 = group2 = 0
        for num in nums:
            if num & mask:
                group1 ^= num
            else:
                group2 ^= num
        
        return [group1, group2]

    def singleNumber_hashmap_reference(self, nums: List[int]) -> List[int]:
        """
        Solution 6: Hash Map Solution (Violates Space Constraint)
        Good for verifying correctness and explaining the problem
        """
        count = Counter(nums)
        result = []
        
        for num, freq in count.items():
            if freq == 1:
                result.append(num)
                if len(result) == 2:
                    break
        
        return result

# Helper functions for understanding and testing
def explain_rightmost_set_bit():
    """
    Explain the bit manipulation trick: x & (-x) gives rightmost set bit
    """
    print("Understanding x & (-x) for finding rightmost set bit:")
    print("Example: x = 12 (binary: 1100)")
    
    x = 12  # Binary: 1100
    print(f"x = {x} = {bin(x)}")
    print(f"-x = {-x} = {bin(-x & 0xFFFFFFFF)}")  # Show two's complement
    print(f"x & (-x) = {x & (-x)} = {bin(x & (-x))}")
    print("This isolates the rightmost set bit (position 2)")
    print()

def visualize_algorithm():
    """
    Step-by-step visualization of the algorithm
    """
    print("Algorithm Visualization with [1,2,1,3,2,5]:")
    nums = [1, 2, 1, 3, 2, 5]
    print(f"Input: {nums}")
    print("Expected output: Two unique numbers are 3 and 5")
    print()
    
    # Step 1: XOR all numbers
    xor_all = 0
    print("Step 1: XOR all numbers")
    for i, num in enumerate(nums):
        xor_all ^= num
        print(f"  After {num}: xor_all = {xor_all} ({bin(xor_all)})")
    
    print(f"Final XOR result: {xor_all} = {bin(xor_all)} = 3^5 = 6")
    print()
    
    # Step 2: Find distinguishing bit
    rightmost_bit = xor_all & (-xor_all)
    print(f"Step 2: Find rightmost set bit")
    print(f"  {xor_all} & (-{xor_all}) = {rightmost_bit} = {bin(rightmost_bit)}")
    print()
    
    # Step 3: Separate into groups
    print("Step 3: Separate numbers by bit 1 (position 1):")
    group1, group2 = [], []
    group1_xor = group2_xor = 0
    
    for num in nums:
        if num & rightmost_bit:
            group1.append(num)
            group1_xor ^= num
            print(f"  {num} ({bin(num)}) has bit 1 set → Group 1")
        else:
            group2.append(num)
            group2_xor ^= num
            print(f"  {num} ({bin(num)}) has bit 1 clear → Group 2")
    
    print(f"\nGroup 1: {group1}, XOR result: {group1_xor}")
    print(f"Group 2: {group2}, XOR result: {group2_xor}")
    print(f"Final answer: [{group1_xor}, {group2_xor}]")

def test_solutions():
    """Test all solutions with various test cases"""
    sol = Solution()
    
    test_cases = [
        [1, 2, 1, 3, 2, 5],      # Expected: [3, 5] or [5, 3]
        [1, 2],                  # Expected: [1, 2] or [2, 1]  
        [-1, 0, -1, 2],          # Expected: [0, 2] or [2, 0]
        [1, 1, 0, -2147483648],  # Expected: [0, -2147483648]
    ]
    
    methods = [
        ("Standard Two-Pass", sol.singleNumber),
        ("Optimized", sol.singleNumber_optimized),
        ("Any Bit", sol.singleNumber_with_any_bit),
        ("With Explanation", sol.singleNumber_with_explanation),
        ("Bit by Bit", sol.singleNumber_bit_by_bit),
        ("HashMap Reference", sol.singleNumber_hashmap_reference),
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case}")
        for method_name, method in methods:
            result = method(test_case.copy())
            print(f"  {method_name:20}: {sorted(result)}")

if __name__ == "__main__":
    explain_rightmost_set_bit()
    print("="*50)
    visualize_algorithm()
    print("="*50)
    test_solutions()

"""
Interview Discussion Points:

1. **Problem Analysis**:
   - Two numbers appear once, all others appear twice
   - XOR of all numbers gives us a^b (where a,b are unique numbers)
   - Need to separate a and b using their differences

2. **Key Insight - Bit Separation**:
   - a^b will have set bits where a and b differ
   - Use any such bit to partition numbers into two groups
   - Each unique number will be in a different group
   - Pairs will be in the same group (identical numbers)

3. **Rightmost Set Bit Trick**:
   - x & (-x) isolates the rightmost set bit
   - Works due to two's complement representation
   - Any set bit can be used, rightmost is just convenient

4. **Algorithm Steps**:
   1. XOR all numbers → get a^b
   2. Find any bit where a and b differ
   3. Partition numbers using this bit
   4. XOR each partition to get the unique numbers

5. **Why This Works**:
   - XOR eliminates pairs (x^x = 0)
   - Partitioning ensures each unique number is in different group
   - XOR within each group eliminates remaining pairs

6. **Edge Cases**:
   - Minimum array size (2 elements)
   - Negative numbers
   - Large numbers
   - Array with mixed positive/negative

7. **Common Mistakes**:
   - Not understanding why partitioning works
   - Trying to find both numbers in single pass without partitioning
   - Confusion about which bit to use for separation
   - Not handling negative numbers properly

8. **Follow-up Questions**:
   - "What if three numbers appear once and others twice?"
   - "Can you find them in specific order?"
   - "What's the time complexity breakdown?"

9. **Optimization Notes**:
   - Single pass possible (shown in optimized version)
   - Space complexity is truly O(1)
   - Time complexity is optimal O(n)

10. **Interview Strategy**:
    - Start by explaining the XOR insight
    - Draw examples with binary representations
    - Explain partitioning logic clearly
    - Code the standard solution first
    - Mention optimizations if time allows
"""
