"""
LeetCode 477: Total Hamming Distance
https://leetcode.com/problems/total-hamming-distance/

Problem: The Hamming distance between two integers is the number of positions 
at which the corresponding bits are different. Given an integer array nums, 
return the sum of Hamming distances between all the pairs of integers in nums.

Constraints: 1 <= nums.length <= 10^4, 0 <= nums[i] <= 10^9

Example 1:
Input: nums = [4,14,2]
Output: 6
Explanation: 
4  = 0100
14 = 1110  
2  = 0010

Hamming distances:
- hamming(4, 14) = 2 (positions 1 and 3 differ)
- hamming(4, 2) = 2 (positions 1 and 2 differ)  
- hamming(14, 2) = 2 (positions 0 and 2 differ)
Total = 2 + 2 + 2 = 6

Example 2:
Input: nums = [4,14,4]
Output: 4
Explanation:
- hamming(4, 14) = 2
- hamming(4, 4) = 0  
- hamming(14, 4) = 2
Total = 2 + 0 + 2 = 4
"""

from typing import List

class Solution:
    
    # ============== APPROACH 1: Brute Force (TLE - Time Limit Exceeded) ==============
    # Time: O(n² × log(max_val)), Space: O(1)
    def totalHammingDistance_bruteforce(self, nums: List[int]) -> int:
        """
        Brute force: Calculate Hamming distance for every pair.
        
        This will TLE for large inputs but good to show understanding.
        Useful for deriving the optimal solution.
        """
        def hamming_distance(x, y):
            xor = x ^ y
            distance = 0
            while xor:
                distance += xor & 1
                xor >>= 1
            return distance
        
        total = 0
        n = len(nums)
        
        for i in range(n):
            for j in range(i + 1, n):
                total += hamming_distance(nums[i], nums[j])
        
        return total
    
    
    # ============== APPROACH 2: Optimized Brute Force with Brian Kernighan ==============
    # Time: O(n² × k) where k = average set bits, Space: O(1)
    def totalHammingDistance_optimized_brute(self, nums: List[int]) -> int:
        """
        Slightly optimized brute force using Brian Kernighan's algorithm
        for counting differing bits. Still O(n²) but with better constants.
        """
        def hamming_distance(x, y):
            xor = x ^ y
            distance = 0
            while xor:
                xor &= xor - 1  # Brian Kernighan: remove lowest set bit
                distance += 1
            return distance
        
        total = 0
        n = len(nums)
        
        for i in range(n):
            for j in range(i + 1, n):
                total += hamming_distance(nums[i], nums[j])
        
        return total
    
    
    # ============== APPROACH 3: Bit Position Analysis (OPTIMAL) ==============
    # Time: O(n × 32) = O(n), Space: O(1)
    def totalHammingDistance(self, nums: List[int]) -> int:
        """
        KEY INSIGHT: Instead of comparing pairs, analyze each bit position.
        
        For each bit position i:
        - Count how many numbers have bit i = 0 (zeros)
        - Count how many numbers have bit i = 1 (ones)
        - Contribution to total = zeros × ones
        
        Why this works:
        - Every pair with different bits at position i contributes 1 to total
        - If we have 'zeros' numbers with bit=0 and 'ones' numbers with bit=1
        - Then there are exactly zeros × ones pairs that differ at this position
        
        Example: nums = [4, 14, 2] = [100, 1110, 10]
        Position 0: [0,0,0] → 3 zeros, 0 ones → contribution = 3×0 = 0
        Position 1: [0,1,1] → 1 zero,  2 ones → contribution = 1×2 = 2  
        Position 2: [1,1,0] → 1 zero,  2 ones → contribution = 1×2 = 2
        Position 3: [0,1,0] → 2 zeros, 1 one  → contribution = 2×1 = 2
        Total = 0 + 2 + 2 + 2 = 6 ✓
        """
        total = 0
        n = len(nums)
        
        # Check each bit position (0 to 31 for 32-bit integers)
        for bit_pos in range(32):
            zeros = ones = 0
            
            # Count 0s and 1s at current bit position
            for num in nums:
                if (num >> bit_pos) & 1:
                    ones += 1
                else:
                    zeros += 1
            
            # Add contribution of this bit position
            total += zeros * ones
        
        return total
    
    
    # ============== APPROACH 4: Bit Manipulation with Bit Counting ==============
    # Time: O(n × 32) = O(n), Space: O(1) 
    def totalHammingDistance_bit_count(self, nums: List[int]) -> int:
        """
        Alternative implementation using bit counting.
        Same logic but different style - good to show versatility.
        """
        total = 0
        n = len(nums)
        
        for bit_pos in range(32):
            ones = sum((num >> bit_pos) & 1 for num in nums)
            zeros = n - ones
            total += zeros * ones
        
        return total
    
    
    # ============== APPROACH 5: Mathematical Formula Explanation ==============
    # Time: O(n × log(max_val)), Space: O(1)
    def totalHammingDistance_mathematical(self, nums: List[int]) -> int:
        """
        Mathematical approach with clear step-by-step explanation.
        Good for interview discussion about the underlying math.
        """
        if not nums:
            return 0
        
        total = 0
        n = len(nums)
        max_val = max(nums)
        
        # Only check bit positions that matter (up to highest bit in max_val)
        bit_pos = 0
        while (1 << bit_pos) <= max_val:
            ones = 0
            
            # Count 1s at current bit position
            for num in nums:
                if num & (1 << bit_pos):
                    ones += 1
            
            zeros = n - ones
            
            # Mathematical insight: C(zeros,1) × C(ones,1) = zeros × ones
            # This counts all pairs that differ at this bit position
            total += zeros * ones
            
            bit_pos += 1
        
        return total


# ============== VISUALIZATION AND ANALYSIS HELPERS ==============
def visualize_hamming_calculation(nums: List[int]):
    """Helper to visualize the bit-by-bit calculation"""
    print(f"\nVisualizing Hamming Distance Calculation for {nums}:")
    n = len(nums)
    
    # Show binary representations
    max_val = max(nums) if nums else 0
    max_bits = max_val.bit_length()
    
    print(f"\nBinary representations (showing {max_bits} bits):")
    for i, num in enumerate(nums):
        binary = format(num, f'0{max_bits}b')
        print(f"nums[{i}] = {num:2d} = {binary}")
    
    # Analyze each bit position
    print(f"\nBit position analysis:")
    print("Pos | Bits  | Zeros | Ones | Contribution")
    print("----|-------|-------|------|-------------")
    
    total = 0
    for bit_pos in range(max_bits):
        bits = []
        ones = zeros = 0
        
        for num in nums:
            bit = (num >> bit_pos) & 1
            bits.append(str(bit))
            if bit:
                ones += 1
            else:
                zeros += 1
        
        contribution = zeros * ones
        total += contribution
        
        bits_str = ''.join(reversed(bits))  # Show from left to right
        print(f"{bit_pos:2d}  | {bits_str:5s} | {zeros:4d}  | {ones:3d}  | {contribution:5d}")
    
    print(f"\nTotal Hamming Distance: {total}")


def explain_mathematical_insight():
    """Explain the key mathematical insight behind the optimal solution"""
    print("\n" + "="*60)
    print("MATHEMATICAL INSIGHT EXPLANATION")
    print("="*60)
    
    print("""
    WHY zeros × ones WORKS:
    
    Consider bit position i with:
    - 'zeros' numbers having bit i = 0
    - 'ones' numbers having bit i = 1
    
    Question: How many pairs differ at bit position i?
    Answer: Every number with bit=0 paired with every number with bit=1
    
    This gives us: zeros × ones pairs
    
    EXAMPLE: nums = [4, 14, 2] at bit position 1
    - Numbers with bit 1 = 0: [4, 2] → zeros = 2  
    - Numbers with bit 1 = 1: [14] → ones = 1
    - Pairs that differ: (4,14), (2,14) → count = 2 × 1 = 2 ✓
    
    COMBINATORIAL INTERPRETATION:
    - Choose 1 number from zeros: C(zeros, 1) = zeros
    - Choose 1 number from ones: C(ones, 1) = ones  
    - Total combinations: zeros × ones
    
    This is why we sum zeros × ones across all bit positions!
    """)


# ============== TEST CASES ==============
def test_solutions():
    solution = Solution()
    
    test_cases = [
        ([4, 14, 2], 6),
        ([4, 14, 4], 4),
        ([1], 0),              # Edge case: single element
        ([0, 0, 0], 0),        # Edge case: all zeros
        ([1, 3, 5], 4),        # Small case: [001, 011, 101]
        ([0, 1], 1),           # Minimal case: 1 bit differs
        ([7, 7, 7], 0),        # All same numbers
        ([1, 2, 4, 8], 12),    # Powers of 2
        ([15, 15, 15, 15], 0)  # All same, larger numbers
    ]
    
    for nums, expected in test_cases:
        # Test optimal approaches (brute force would be too slow for large cases)
        assert solution.totalHammingDistance(nums) == expected
        assert solution.totalHammingDistance_bit_count(nums) == expected
        assert solution.totalHammingDistance_mathematical(nums) == expected
        
        # Test brute force on small cases only
        if len(nums) <= 10:
            assert solution.totalHammingDistance_bruteforce(nums) == expected
            assert solution.totalHammingDistance_optimized_brute(nums) == expected
        
        print(f"✓ nums={nums}, expected={expected}")
    
    print("All test cases passed!")


# ============== COMPLEXITY ANALYSIS ==============
def complexity_analysis():
    """Explain complexity analysis for interview"""
    print("\n" + "="*50)
    print("COMPLEXITY ANALYSIS")
    print("="*50)
    
    print("""
    BRUTE FORCE APPROACH:
    - Time: O(n² × log(max_val))
      - n² pairs to check
      - log(max_val) bits to compare per pair
    - Space: O(1)
    - Result: TLE (Time Limit Exceeded) for large inputs
    
    OPTIMAL BIT POSITION APPROACH:
    - Time: O(n × 32) = O(n)
      - 32 bit positions to check (constant)
      - n numbers to examine per bit position
    - Space: O(1)
    - Result: Efficient and scalable!
    
    WHY IT'S BETTER:
    - Reduces n² pair comparisons to n×32 bit checks
    - For n=10⁴: brute force ~10⁸ ops vs optimal ~3×10⁵ ops
    - Massive improvement: 333x faster!
    """)


# ============== INTERVIEW TALKING POINTS ==============
"""
WHAT TO MENTION IN INTERVIEW:

1. PROBLEM ANALYSIS:
   - Hamming distance = count of differing bit positions
   - Brute force: check all O(n²) pairs → too slow
   - Need to find a pattern or mathematical insight

2. KEY INSIGHT DERIVATION:
   "Instead of comparing pairs, let's think about individual bit positions.
   For each bit position, how many pairs will contribute to the total?"
   
   - Draw out examples on whiteboard
   - Show how zeros × ones counts differing pairs at each position
   - This transforms O(n²) problem into O(n) problem!

3. STEP-BY-STEP SOLUTION:
   a) For each bit position (0 to 31)
   b) Count numbers with bit=0 and bit=1
   c) Add zeros × ones to total
   d) Sum across all positions

4. MATHEMATICAL JUSTIFICATION:
   - Every pair that differs at bit position i contributes 1
   - Numbers with bit=0 paired with numbers with bit=1 = zeros × ones
   - This counts exactly the pairs we want, no double counting

5. COMPLEXITY IMPROVEMENT:
   - From O(n² × log(max)) to O(n × 32) = O(n)
   - Space remains O(1)
   - Handles constraint n ≤ 10⁴ efficiently

6. IMPLEMENTATION DETAILS:
   - Use bit shifting: (num >> bit_pos) & 1
   - Check 32 bit positions (enough for 32-bit integers)
   - Handle edge cases: empty array, single element

7. FOLLOW-UP QUESTIONS THEY MIGHT ASK:
   - "What if numbers were 64-bit?" → Change loop to 64 iterations
   - "Can you optimize further?" → Early termination when max_val reached
   - "What's the intuition?" → Draw bit-by-bit analysis
   - "Space-time tradeoffs?" → Could precompute but O(1) space is optimal

8. RECOMMENDED INTERVIEW STRATEGY:
   1. Start with brute force (shows understanding)
   2. Identify inefficiency: "We're doing redundant work"
   3. Derive insight: "Let's analyze bit positions instead"
   4. Code optimal solution with clear variable names
   5. Walk through example to verify correctness
   6. Analyze complexity improvement

9. CODE INTERVIEW TIPS:
   - Write clean, readable code with good variable names
   - Add comments explaining the key insight
   - Test with provided examples
   - Mention edge cases and how you handle them

This problem perfectly demonstrates the transformation from brute force to 
optimal solution using mathematical insight - exactly what big tech interviews love!
"""

if __name__ == "__main__":
    test_solutions()
    visualize_hamming_calculation([4, 14, 2])
    explain_mathematical_insight()
    complexity_analysis()
