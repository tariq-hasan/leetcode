"""
LeetCode 137: Single Number II
Problem: Given an integer array where every element appears exactly three times 
except for one, which appears exactly once. Find the single element.

Must solve in O(n) time and O(1) extra space.

Key Insight: Use bit manipulation to count occurrences of each bit position.
For each bit position, if count % 3 != 0, that bit belongs to the single number.
"""

from typing import List
from collections import Counter

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Solution 1: Bit Counting (Most Intuitive)
        Count frequency of each bit position across all numbers.
        If a bit appears in positions that aren't multiples of 3, 
        it must belong to the single number.
        
        Time: O(32n) = O(n), Space: O(1)
        """
        result = 0
        
        # Check each bit position (32 bits for integer)
        for i in range(32):
            bit_count = 0
            
            # Count how many numbers have bit i set
            for num in nums:
                if num & (1 << i):
                    bit_count += 1
            
            # If count is not divisible by 3, single number has this bit set
            if bit_count % 3 != 0:
                result |= (1 << i)
        
        # Handle negative numbers (Python's int can be arbitrarily large)
        # Convert to 32-bit signed integer
        if result >= 2**31:
            result -= 2**32
            
        return result

    def singleNumber_optimized_counting(self, nums: List[int]) -> int:
        """
        Solution 2: Optimized Bit Counting
        Same logic but with cleaner bit manipulation
        """
        result = 0
        
        for i in range(32):
            bit_sum = sum((num >> i) & 1 for num in nums)
            
            if bit_sum % 3 != 0:
                result |= (1 << i)
        
        # Convert to signed 32-bit integer
        return result if result < 2**31 else result - 2**32

    def singleNumber_digital_circuit(self, nums: List[int]) -> int:
        """
        Solution 3: Digital Circuit Approach (Advanced)
        Simulate a digital circuit that counts mod 3 using two bits.
        This is the most space-efficient and elegant solution.
        
        Uses two variables (ones, twos) to represent states:
        - ones: bits that appeared 1 time mod 3
        - twos: bits that appeared 2 times mod 3
        - when a bit appears 3 times, both ones and twos become 0
        """
        ones = twos = 0
        
        for num in nums:
            # Update twos: bits that were in ones and also in current num
            twos |= ones & num
            
            # Update ones: XOR with current number
            ones ^= num
            
            # Remove bits that appeared 3 times (present in both ones and twos)
            common_bits = ones & twos
            ones &= ~common_bits
            twos &= ~common_bits
        
        return ones

    def singleNumber_three_state_fsm(self, nums: List[int]) -> int:
        """
        Solution 4: Three-State Finite State Machine
        Another way to think about the digital circuit approach.
        Each bit can be in 3 states: seen 0, 1, or 2 times (mod 3).
        """
        seen_once = seen_twice = 0
        
        for num in nums:
            # What bits appear for the first time
            seen_once = (seen_once ^ num) & ~seen_twice
            
            # What bits appear for the second time  
            seen_twice = (seen_twice ^ num) & ~seen_once
        
        return seen_once

    def singleNumber_general_solution(self, nums: List[int]) -> int:
        """
        Solution 5: Generalized Solution for k=3, p=1
        Can be adapted for "every element appears k times except one appears p times"
        Here k=3, p=1
        """
        # For k=3, we need ceil(log2(3)) = 2 bits to represent states
        x1 = x2 = 0
        mask = 0
        
        for num in nums:
            # State transition for 3-state counter
            x2 ^= x1 & num
            x1 ^= num
            
            # When count reaches 3 (11 in binary), reset to 0
            mask = ~(x1 & x2)
            x1 &= mask
            x2 &= mask
        
        return x1  # x1 contains bits that appeared 1 time (mod 3)

    def singleNumber_hashmap_for_reference(self, nums: List[int]) -> int:
        """
        Solution 6: Hash Map Solution (Not O(1) space, but clear logic)
        This violates space constraint but good for understanding the problem
        """
        count = Counter(nums)
        
        for num, freq in count.items():
            if freq == 1:
                return num
        
        return -1  # Should never reach here with valid input

    def singleNumber_sum_based(self, nums: List[int]) -> int:
        """
        Solution 7: Mathematical Approach (Not always feasible)
        3 * (sum of unique numbers) - sum of all numbers = 2 * single number
        
        Note: This can cause integer overflow and requires extra space for set
        """
        unique_nums = set(nums)
        return (3 * sum(unique_nums) - sum(nums)) // 2

# Helper function to test and demonstrate solutions
def test_solutions():
    sol = Solution()
    
    test_cases = [
        [2, 2, 3, 2],           # Expected: 3
        [0, 1, 0, 1, 0, 1, 99], # Expected: 99
        [1],                    # Expected: 1
        [-2, -2, 1, 1, 4, 1, 4, 4, -4, -2], # Expected: -4
    ]
    
    methods = [
        ("Bit Counting", sol.singleNumber),
        ("Optimized Counting", sol.singleNumber_optimized_counting),
        ("Digital Circuit", sol.singleNumber_digital_circuit),
        ("FSM", sol.singleNumber_three_state_fsm),
        ("General Solution", sol.singleNumber_general_solution),
        ("HashMap", sol.singleNumber_hashmap_for_reference),
        ("Sum Based", sol.singleNumber_sum_based),
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case}")
        for method_name, method in methods:
            try:
                result = method(test_case.copy())
                print(f"  {method_name:20}: {result}")
            except Exception as e:
                print(f"  {method_name:20}: Error - {e}")

# Visualization of the digital circuit approach
def visualize_digital_circuit():
    """
    Demonstrate how the digital circuit approach works step by step
    """
    print("Digital Circuit Approach Visualization:")
    print("For input [2, 2, 3, 2]:")
    print("Binary: [10, 10, 11, 10]")
    print()
    
    nums = [2, 2, 3, 2]  # Binary: [10, 10, 11, 10]
    ones = twos = 0
    
    print("Step | num | ones | twos | common | ones_final | twos_final")
    print("-" * 65)
    
    for i, num in enumerate(nums):
        print(f"{i:4} | {num:3} | {ones:4} | {twos:4} | ", end="")
        
        # Calculate updates
        new_twos = twos | (ones & num)
        new_ones = ones ^ num
        common_bits = new_ones & new_twos
        final_ones = new_ones & ~common_bits
        final_twos = new_twos & ~common_bits
        
        print(f"{common_bits:6} | {final_ones:10} | {final_twos:10}")
        
        ones, twos = final_ones, final_twos
    
    print(f"\nFinal result: ones = {ones} (which is our answer)")

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*50)
    visualize_digital_circuit()

"""
Interview Discussion Points:

1. **Problem Understanding**:
   - Every number appears exactly 3 times except one appears once
   - Must solve in O(n) time and O(1) space
   - Cannot use sorting or hash maps due to space constraint

2. **Key Insight - Bit Manipulation**:
   - Think about each bit position independently
   - If a bit appears in positions divisible by 3, it cancels out
   - Remaining bits belong to the single number

3. **Solution Evolution**:
   - Start with bit counting (easiest to understand)
   - Progress to digital circuit (most elegant)
   - Show understanding of state machines

4. **Digital Circuit Explanation**:
   - ones: tracks bits seen 1 time (mod 3)
   - twos: tracks bits seen 2 times (mod 3)  
   - When bit seen 3 times, reset both to 0
   - Final answer is in 'ones'

5. **Edge Cases**:
   - Single element array
   - Negative numbers
   - Large numbers
   - Arrays with minimum valid size

6. **Follow-up Questions**:
   - "What if every element appears k times except one appears p times?"
   - "How would you handle floating point numbers?"
   - "Can you solve it with different space/time trade-offs?"

7. **Common Mistakes**:
   - Forgetting to handle negative numbers properly
   - Not understanding the state transitions in digital circuit
   - Trying to use XOR directly (works for pairs, not triplets)

8. **Implementation Tips**:
   - Start with bit counting approach in interview
   - Explain the logic clearly before coding
   - Mention the digital circuit approach as optimization
   - Test with small examples to verify logic
"""
