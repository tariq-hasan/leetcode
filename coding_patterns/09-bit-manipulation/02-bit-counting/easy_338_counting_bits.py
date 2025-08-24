"""
LeetCode 338: Counting Bits
https://leetcode.com/problems/counting-bits/

Problem: Given an integer n, return an array ans of length n + 1 such that 
for each i (0 <= i <= n), ans[i] is the number of 1's in the binary 
representation of i.

Example 1:
Input: n = 2
Output: [0,1,1]
Explanation:
0 --> 0 (0 ones)
1 --> 1 (1 one)  
2 --> 10 (1 one)

Example 2:
Input: n = 5
Output: [0,1,1,2,1,2]
Explanation:
0 --> 0 (0 ones)
1 --> 1 (1 one)
2 --> 10 (1 one)
3 --> 11 (2 ones)
4 --> 100 (1 one)
5 --> 101 (2 ones)

Follow up: Can you do it in O(n) time and O(1) extra space (excluding the output array)?
"""

from typing import List

class Solution:
    
    # ============== APPROACH 1: Brute Force (Not Optimal) ==============
    # Time: O(n log n), Space: O(1) extra space
    def countBits_bruteforce(self, n: int) -> List[int]:
        """
        For each number, count bits using Brian Kernighan's algorithm.
        Simple but not optimal - good starting point to show understanding.
        """
        def count_ones(num):
            count = 0
            while num:
                num &= num - 1  # Clear lowest set bit
                count += 1
            return count
        
        return [count_ones(i) for i in range(n + 1)]
    
    
    # ============== APPROACH 2: DP with Bit Shift Pattern (OPTIMAL) ==============
    # Time: O(n), Space: O(1) extra space
    def countBits(self, n: int) -> List[int]:
        """
        Dynamic Programming using bit manipulation pattern.
        
        KEY INSIGHT: For any number i, the bit count is:
        dp[i] = dp[i >> 1] + (i & 1)
        
        Explanation:
        - i >> 1 is i divided by 2 (removes the last bit)
        - i & 1 tells us if the last bit is 1 or 0
        - So we take the bit count of i//2 and add 1 if last bit is set
        
        Example: i = 5 (101)
        - i >> 1 = 2 (10), dp[2] = 1
        - i & 1 = 1 (last bit is 1)
        - dp[5] = dp[2] + 1 = 1 + 1 = 2 ✓
        """
        if n == 0:
            return [0]
        
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        
        return dp
    
    
    # ============== APPROACH 3: DP with Power of 2 Pattern ==============
    # Time: O(n), Space: O(1) extra space
    def countBits_power_of_2(self, n: int) -> List[int]:
        """
        DP using powers of 2 pattern.
        
        KEY INSIGHT: Every power of 2 starts a new pattern.
        For numbers between 2^k and 2^(k+1)-1:
        dp[i] = 1 + dp[i - 2^k]
        
        Example pattern:
        0: 0 ones
        1: 1 one  (1 + dp[0])
        2: 1 one  (1 + dp[0])  
        3: 2 ones (1 + dp[1])
        4: 1 one  (1 + dp[0])
        5: 2 ones (1 + dp[1])
        6: 2 ones (1 + dp[2])
        7: 3 ones (1 + dp[3])
        """
        dp = [0] * (n + 1)
        power_of_2 = 1
        
        for i in range(1, n + 1):
            # When we reach the next power of 2, update it
            if i == power_of_2 * 2:
                power_of_2 = i
            
            dp[i] = 1 + dp[i - power_of_2]
        
        return dp
    
    
    # ============== APPROACH 4: DP with i & (i-1) Pattern ==============
    # Time: O(n), Space: O(1) extra space
    def countBits_kernighan_dp(self, n: int) -> List[int]:
        """
        DP using Brian Kernighan's insight: i & (i-1) removes the lowest set bit.
        
        KEY INSIGHT: dp[i] = dp[i & (i-1)] + 1
        - i & (i-1) gives us i with the lowest set bit removed
        - We add 1 for the bit we just removed
        
        Example: i = 6 (110)
        - i & (i-1) = 6 & 5 = 110 & 101 = 100 = 4
        - dp[6] = dp[4] + 1 = 1 + 1 = 2 ✓
        """
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        
        return dp


# ============== TEST CASES ==============
def test_solutions():
    solution = Solution()
    
    test_cases = [
        (2, [0, 1, 1]),
        (5, [0, 1, 1, 2, 1, 2]),
        (0, [0]),
        (1, [0, 1]),
        (8, [0, 1, 1, 2, 1, 2, 2, 3, 1])  # Powers of 2 pattern visible
    ]
    
    for n, expected in test_cases:
        # Test all approaches
        assert solution.countBits_bruteforce(n) == expected
        assert solution.countBits(n) == expected
        assert solution.countBits_power_of_2(n) == expected
        assert solution.countBits_kernighan_dp(n) == expected
        
        print(f"✓ n={n}, result={expected}")
        # Show binary representations for better understanding
        if n <= 8:
            print(f"  Binary pattern: {[f'{i}:{bin(i)[2:]}({expected[i]})' for i in range(n+1)]}")
    
    print("All test cases passed!")


# ============== PATTERN VISUALIZATION ==============
def visualize_pattern(n: int = 15):
    """Helper function to visualize the bit counting pattern"""
    solution = Solution()
    result = solution.countBits(n)
    
    print(f"\nBit Counting Pattern for n={n}:")
    print("Num | Binary   | Count | Explanation")
    print("----|----------|-------|-------------")
    
    for i in range(n + 1):
        binary = bin(i)[2:].zfill(4)
        count = result[i]
        
        if i == 0:
            explanation = "Base case"
        else:
            parent = i >> 1
            last_bit = i & 1
            explanation = f"dp[{parent}] + {last_bit}"
        
        print(f"{i:2d}  | {binary} | {count:2d}    | {explanation}")


# ============== INTERVIEW TALKING POINTS ==============
"""
WHAT TO MENTION IN INTERVIEW:

1. PROBLEM ANALYSIS:
   - This is asking for bit counts for ALL numbers 0 to n
   - Brute force would be O(n log n) - can we do better?
   - Key insight: We can reuse previous computations (DP!)

2. OPTIMAL APPROACH EXPLANATION:
   Start with: dp[i] = dp[i >> 1] + (i & 1)
   
   WHY THIS WORKS:
   - i >> 1 is i with the last bit removed
   - We already computed bit count for i >> 1
   - i & 1 tells us if we need to add 1 for the last bit
   - This gives us O(n) time, O(1) extra space!

3. ALTERNATIVE PATTERNS TO MENTION:
   - Powers of 2 pattern: Shows pattern recognition skills
   - Kernighan pattern: Shows deep bit manipulation understanding
   - All achieve O(n) time complexity

4. EDGE CASES:
   - n = 0: Return [0]
   - n = 1: Return [0, 1]
   - Powers of 2: Always have exactly 1 bit set

5. FOLLOW-UP QUESTIONS THEY MIGHT ASK:
   - "Can you solve it without DP?" → Show brute force approach
   - "Explain why your DP relation works" → Draw out examples
   - "What if n is very large?" → Discuss space optimizations
   - "Can you do it iteratively vs recursively?" → Show iterative DP

6. RECOMMENDED INTERVIEW STRATEGY:
   1. Start with brute force to show you understand the problem
   2. Explain why O(n log n) isn't optimal for this problem
   3. Derive the DP relationship: dp[i] = dp[i >> 1] + (i & 1)
   4. Code the optimal solution
   5. Walk through an example to verify correctness
   6. Mention other DP patterns if time permits

7. COMPLEXITY ANALYSIS:
   Time: O(n) - single pass through all numbers
   Space: O(1) extra space (output array doesn't count)
   This meets the follow-up requirement perfectly!
"""

if __name__ == "__main__":
    test_solutions()
    visualize_pattern(15)
