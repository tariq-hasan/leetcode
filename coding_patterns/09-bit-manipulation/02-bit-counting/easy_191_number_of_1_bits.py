"""
LeetCode 191: Number of 1 Bits
https://leetcode.com/problems/number-of-1-bits/

Problem: Write a function that takes the binary representation of a positive integer 
and returns the number of set bits it has (also known as the Hamming weight).

Example 1:
Input: n = 11 (binary: 1011)
Output: 3
Explanation: The input binary string 1011 has a total of three set bits.

Example 2:
Input: n = 128 (binary: 10000000)
Output: 1
"""

class Solution:
    
    # ============== APPROACH 1: Built-in Function (Simplest) ==============
    # Time: O(1), Space: O(1)
    def hammingWeight_builtin(self, n: int) -> int:
        """
        Using Python's built-in bin() and count() methods.
        Most concise but may not be preferred in interviews.
        """
        return bin(n).count('1')
    
    
    # ============== APPROACH 2: Right Shift & Check LSB ==============
    # Time: O(log n), Space: O(1)
    def hammingWeight_shift(self, n: int) -> int:
        """
        Check each bit by examining the least significant bit (LSB)
        and right-shifting the number.
        
        This is the most intuitive approach for beginners.
        """
        count = 0
        while n:
            count += n & 1  # Check if LSB is 1
            n >>= 1         # Right shift by 1 bit
        return count
    
    
    # ============== APPROACH 3: Brian Kernighan's Algorithm (OPTIMAL) ==============
    # Time: O(k) where k = number of set bits, Space: O(1)
    def hammingWeight(self, n: int) -> int:
        """
        Brian Kernighan's algorithm - most efficient!
        
        Key insight: n & (n-1) clears the lowest set bit.
        We only iterate for the number of set bits, not all bits.
        
        Example: n = 12 (1100)
        - n = 1100, n-1 = 1011, n & (n-1) = 1000 (cleared rightmost 1)
        - n = 1000, n-1 = 0111, n & (n-1) = 0000 (cleared rightmost 1)
        - Done! Count = 2
        """
        count = 0
        while n:
            n &= n - 1  # Clear the lowest set bit
            count += 1
        return count
    
    
    # ============== APPROACH 4: Bit Manipulation with Lookup ==============
    # Time: O(1), Space: O(1)
    def hammingWeight_lookup(self, n: int) -> int:
        """
        Process 4 bits at a time using a lookup table.
        More complex but demonstrates advanced bit manipulation.
        """
        # Lookup table for 4-bit combinations (0-15)
        lookup = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
        
        count = 0
        while n:
            count += lookup[n & 0xF]  # Process last 4 bits
            n >>= 4                   # Shift right by 4 bits
        return count


# ============== TEST CASES ==============
def test_solutions():
    solution = Solution()
    
    test_cases = [
        (11, 3),      # 1011 -> 3 ones
        (128, 1),     # 10000000 -> 1 one  
        (4294967293, 31),  # 11111111111111111111111111111101 -> 31 ones
        (0, 0),       # Edge case: 0
        (1, 1),       # Edge case: 1
        (2147483647, 31)  # 01111111111111111111111111111111 -> 31 ones
    ]
    
    for n, expected in test_cases:
        # Test all approaches
        assert solution.hammingWeight_builtin(n) == expected
        assert solution.hammingWeight_shift(n) == expected  
        assert solution.hammingWeight(n) == expected
        assert solution.hammingWeight_lookup(n) == expected
        print(f"✓ n={n}, expected={expected}, binary={bin(n)}")
    
    print("All test cases passed!")


# ============== INTERVIEW TALKING POINTS ==============
"""
WHAT TO MENTION IN INTERVIEW:

1. APPROACH COMPARISON:
   - Built-in: Simplest but may not showcase bit manipulation skills
   - Right shift: Most intuitive, good for explanation
   - Brian Kernighan: Most optimal, shows advanced knowledge
   - Lookup: Demonstrates understanding of space-time tradeoffs

2. TIME COMPLEXITY ANALYSIS:
   - Shift approach: O(log n) - checks all bits
   - Brian Kernighan: O(k) where k = number of set bits - BETTER!
   - Why? Because we only iterate for set bits, not all bits

3. EDGE CASES TO DISCUSS:
   - n = 0 (no set bits)
   - n = 1 (single set bit)
   - Large numbers with many set bits
   - Powers of 2 (single set bit)

4. FOLLOW-UP QUESTIONS THEY MIGHT ASK:
   - "Can you solve it without using built-in functions?" → Use Brian Kernighan
   - "Can you optimize further?" → Discuss lookup table or SIMD instructions
   - "What if we had multiple numbers?" → Batch processing considerations

5. RECOMMENDED ANSWER:
   Start with Brian Kernighan algorithm (most optimal), then mention alternatives
   if asked. This shows you know the best solution first.
"""

if __name__ == "__main__":
    test_solutions()
