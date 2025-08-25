"""
LeetCode 1201: Ugly Number III
https://leetcode.com/problems/ugly-number-iii/

Problem: An ugly number is a positive integer that is divisible by a, b, or c.
Given four integers n, a, b, and c, return the nth ugly number.

Constraints: 
- 1 <= n, a, b, c <= 10^9
- 1 <= a * b * c <= 10^18
- It's guaranteed that the result will be in range [1, 2 * 10^9]

Example 1:
Input: n = 3, a = 2, b = 3, c = 5
Output: 4
Explanation: The ugly numbers are 2, 3, 4, 5, 6, 8, 9, 10... The 3rd is 4.

Example 2:
Input: n = 4, a = 2, b = 3, c = 4
Output: 6
Explanation: The ugly numbers are 2, 3, 4, 6, 8, 9, 10, 12... The 4th is 6.

Example 3:
Input: n = 1000000000, a = 2, b = 217983653, c = 336916467
Output: 1999999984
"""

import math
from typing import List

class Solution:
    
    # ============== APPROACH 1: Brute Force (TLE - For Understanding) ==============
    # Time: O(result), Space: O(1)
    def nthUglyNumber_bruteforce(self, n: int, a: int, b: int, c: int) -> int:
        """
        Brute force: Check every number starting from 1.
        This will TLE but helps understand the problem.
        Only use for small test cases.
        """
        count = 0
        num = 0
        
        while count < n:
            num += 1
            if num % a == 0 or num % b == 0 or num % c == 0:
                count += 1
        
        return num
    
    
    # ============== HELPER FUNCTIONS FOR OPTIMAL SOLUTION ==============
    
    def gcd(self, x: int, y: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm"""
        while y:
            x, y = y, x % y
        return x
    
    def lcm(self, x: int, y: int) -> int:
        """Calculate Least Common Multiple using GCD"""
        return x * y // self.gcd(x, y)
    
    def count_ugly_numbers_up_to_x(self, x: int, a: int, b: int, c: int) -> int:
        """
        Count how many ugly numbers are <= x using Inclusion-Exclusion Principle
        
        INCLUSION-EXCLUSION PRINCIPLE:
        |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|
        
        Where:
        - |A| = numbers divisible by a = x // a
        - |A ∩ B| = numbers divisible by both a and b = x // lcm(a,b)
        - etc.
        
        This counts exactly the ugly numbers <= x without double counting.
        """
        # Individual counts (inclusion)
        count_a = x // a
        count_b = x // b  
        count_c = x // c
        
        # Pairwise overlaps (exclusion)
        count_ab = x // self.lcm(a, b)
        count_ac = x // self.lcm(a, c)
        count_bc = x // self.lcm(b, c)
        
        # Triple overlap (inclusion)
        count_abc = x // self.lcm(self.lcm(a, b), c)
        
        return count_a + count_b + count_c - count_ab - count_ac - count_bc + count_abc
    
    
    # ============== APPROACH 2: Binary Search + Inclusion-Exclusion (OPTIMAL) ==============
    # Time: O(log(2×10^9) × log(max(a,b,c))) = O(log n), Space: O(1)
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        """
        OPTIMAL SOLUTION: Binary Search on the answer + Inclusion-Exclusion
        
        KEY INSIGHTS:
        1. If we can count ugly numbers <= x, we can binary search for the answer
        2. Use inclusion-exclusion principle to count without double counting
        3. Search space: [1, 2×10^9] (guaranteed by problem constraints)
        
        ALGORITHM:
        1. Binary search on possible answers
        2. For each candidate x, count ugly numbers <= x
        3. If count >= n, x could be our answer (search left)
        4. If count < n, we need a larger number (search right)
        5. Return the smallest x where count >= n
        """
        left, right = 1, 2 * 10**9
        
        while left < right:
            mid = (left + right) // 2
            
            # Count ugly numbers <= mid
            count = self.count_ugly_numbers_up_to_x(mid, a, b, c)
            
            if count < n:
                # Need more ugly numbers, search right half
                left = mid + 1
            else:
                # We have enough ugly numbers, this could be our answer
                # But we want the smallest such number, so search left half
                right = mid
        
        return left
    
    
    # ============== APPROACH 3: Optimized with Early LCM Calculation ==============
    # Time: O(log n), Space: O(1)
    def nthUglyNumber_optimized(self, n: int, a: int, b: int, c: int) -> int:
        """
        Same algorithm but precompute LCMs for better performance.
        Shows optimization mindset for interviews.
        """
        # Precompute all LCMs to avoid redundant calculations
        lcm_ab = self.lcm(a, b)
        lcm_ac = self.lcm(a, c)  
        lcm_bc = self.lcm(b, c)
        lcm_abc = self.lcm(lcm_ab, c)
        
        def count_ugly_up_to_x(x):
            return (x // a + x // b + x // c 
                   - x // lcm_ab - x // lcm_ac - x // lcm_bc 
                   + x // lcm_abc)
        
        left, right = 1, 2 * 10**9
        
        while left < right:
            mid = (left + right) // 2
            
            if count_ugly_up_to_x(mid) < n:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    
    # ============== APPROACH 4: Mathematical Analysis (Advanced) ==============
    # Time: O(log n), Space: O(1)
    def nthUglyNumber_mathematical(self, n: int, a: int, b: int, c: int) -> int:
        """
        Advanced approach with detailed mathematical analysis.
        Good for showing deep understanding in interviews.
        """
        # Calculate all LCMs with mathematical insight
        def gcd_extended(x, y):
            """Extended Euclidean algorithm for educational purposes"""
            return math.gcd(x, y)  # Using built-in for reliability
        
        def lcm_safe(x, y):
            """LCM with overflow protection"""
            g = gcd_extended(x, y)
            return (x // g) * y  # Prevent intermediate overflow
        
        # Precompute LCMs
        lcm_ab = lcm_safe(a, b)
        lcm_ac = lcm_safe(a, c)
        lcm_bc = lcm_safe(b, c)
        lcm_abc = lcm_safe(lcm_ab, c)
        
        def count_uglies(x):
            """
            Apply inclusion-exclusion principle with detailed explanation
            """
            # Single sets: multiples of individual numbers
            single = x // a + x // b + x // c
            
            # Pairwise intersections: multiples of LCMs
            pairwise = x // lcm_ab + x // lcm_ac + x // lcm_bc
            
            # Triple intersection: multiples of LCM of all three
            triple = x // lcm_abc
            
            # Inclusion-exclusion: include singles, exclude pairwise, include triple
            return single - pairwise + triple
        
        # Binary search with bounds analysis
        # Lower bound: min(a,b,c) (first ugly number)
        # Upper bound: 2×10^9 (guaranteed by problem)
        left = min(a, b, c)
        right = 2 * 10**9
        
        while left < right:
            mid = left + (right - left) // 2  # Avoid overflow
            
            count = count_uglies(mid)
            
            if count < n:
                left = mid + 1
            else:
                right = mid
        
        return left


# ============== VISUALIZATION AND ANALYSIS HELPERS ==============
def visualize_ugly_numbers(n: int, a: int, b: int, c: int, limit: int = 50):
    """Visualize the first few ugly numbers to understand the pattern"""
    solution = Solution()
    
    print(f"\nUgly numbers for a={a}, b={b}, c={c}:")
    print("Num | Divisible by | Ugly?")
    print("----|--------------|------")
    
    ugly_numbers = []
    for num in range(1, limit + 1):
        is_ugly = (num % a == 0) or (num % b == 0) or (num % c == 0)
        
        divisors = []
        if num % a == 0: divisors.append(f"a({a})")
        if num % b == 0: divisors.append(f"b({b})")  
        if num % c == 0: divisors.append(f"c({c})")
        
        divisor_str = ", ".join(divisors) if divisors else "none"
        
        if is_ugly:
            ugly_numbers.append(num)
        
        print(f"{num:2d}  | {divisor_str:<12} | {'YES' if is_ugly else 'NO'}")
        
        if len(ugly_numbers) >= n:
            break
    
    print(f"\nFirst {min(n, len(ugly_numbers))} ugly numbers: {ugly_numbers[:n]}")
    if n <= len(ugly_numbers):
        print(f"The {n}th ugly number is: {ugly_numbers[n-1]}")


def explain_inclusion_exclusion():
    """Explain the inclusion-exclusion principle with examples"""
    print("\n" + "="*60)
    print("INCLUSION-EXCLUSION PRINCIPLE EXPLAINED")
    print("="*60)
    
    print("""
    PROBLEM: Count numbers ≤ x that are divisible by a, b, or c
    
    NAIVE APPROACH (WRONG):
    count = (x//a) + (x//b) + (x//c)  ❌ Double/triple counting!
    
    CORRECT APPROACH (Inclusion-Exclusion):
    Step 1: Include all individual counts
    Step 2: Exclude pairwise overlaps (avoid double counting)  
    Step 3: Include triple overlap (we excluded it twice in step 2)
    
    FORMULA:
    |A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
    
    WHERE:
    - |A| = x // a        (numbers divisible by a)
    - |A∩B| = x // lcm(a,b)  (numbers divisible by both a and b)
    - etc.
    
    EXAMPLE: x = 12, a = 2, b = 3, c = 4
    - Divisible by 2: [2,4,6,8,10,12] → count = 6
    - Divisible by 3: [3,6,9,12] → count = 4  
    - Divisible by 4: [4,8,12] → count = 3
    - Divisible by lcm(2,3)=6: [6,12] → count = 2
    - Divisible by lcm(2,4)=4: [4,8,12] → count = 3
    - Divisible by lcm(3,4)=12: [12] → count = 1
    - Divisible by lcm(2,3,4)=12: [12] → count = 1
    
    Result = 6 + 4 + 3 - 2 - 3 - 1 + 1 = 8
    
    Verification: {2,3,4,6,8,9,10,12} = 8 numbers ✓
    """)


def analyze_binary_search_bounds():
    """Explain why binary search bounds work"""
    print("\n" + "="*50)  
    print("BINARY SEARCH BOUNDS ANALYSIS")
    print("="*50)
    
    print("""
    SEARCH SPACE: [1, 2×10^9]
    
    LOWER BOUND JUSTIFICATION:
    - The smallest ugly number is min(a, b, c)
    - But we can start from 1 for simplicity (still correct)
    
    UPPER BOUND JUSTIFICATION:  
    - Problem guarantees result ≤ 2×10^9
    - In worst case: a = b = c = 10^9, n = 10^9
    - Then nth ugly number = n × min(a,b,c) = 10^9 × 10^9 = 10^18
    - But problem says result ≤ 2×10^9, so we can use that bound
    
    WHY BINARY SEARCH WORKS:
    - If count(x) < n, then answer > x (monotonic property)
    - If count(x) ≥ n, then answer ≤ x  
    - We want the smallest x where count(x) ≥ n
    - This is exactly what binary search finds!
    
    COMPLEXITY: O(log(2×10^9)) = O(30) = O(1) practically
    """)


# ============== TEST CASES ==============
def test_solutions():
    solution = Solution()
    
    test_cases = [
        (3, 2, 3, 5, 4),
        (4, 2, 3, 4, 6),
        (1000000000, 2, 217983653, 336916467, 1999999984),
        (1, 2, 3, 5, 2),      # Edge case: first ugly number
        (10, 2, 3, 5, 12),    # Verify with small example
        (5, 3, 5, 7, 9),      # Different numbers
        (1, 1, 1, 1, 1),      # Edge case: all same
        (100, 5, 7, 11, 260)  # Medium test case
    ]
    
    for n, a, b, c, expected in test_cases:
        # Test optimal solutions
        assert solution.nthUglyNumber(n, a, b, c) == expected
        assert solution.nthUglyNumber_optimized(n, a, b, c) == expected  
        assert solution.nthUglyNumber_mathematical(n, a, b, c) == expected
        
        # Test brute force only on very small cases
        if n <= 1000 and max(a, b, c) <= 100:
            assert solution.nthUglyNumber_bruteforce(n, a, b, c) == expected
        
        print(f"✓ n={n}, a={a}, b={b}, c={c}, expected={expected}")
    
    print("All test cases passed!")


# ============== INTERVIEW TALKING POINTS ==============
"""
WHAT TO MENTION IN INTERVIEW:

1. PROBLEM ANALYSIS:
   - Brute force: Check every number → O(result) → TLE for large inputs
   - Need smarter approach: What if we binary search on the answer?
   - Key insight: If we can count ugly numbers ≤ x, we can find the nth one

2. COUNTING STRATEGY (Inclusion-Exclusion):
   - Can't just add x//a + x//b + x//c (double counting!)
   - Use inclusion-exclusion principle to count exactly
   - Need LCM calculations to find intersections
   - This is a classic number theory application

3. BINARY SEARCH INSIGHT:
   - Search space: [1, 2×10^9] (given by problem constraints)
   - Monotonic property: If count(x) ≥ n, then count(x+1) ≥ n
   - Want smallest x where count(x) ≥ n
   - Binary search finds this efficiently in O(log n) time

4. MATHEMATICAL COMPONENTS:
   - GCD calculation (Euclidean algorithm)
   - LCM calculation using GCD
   - Inclusion-exclusion principle
   - Overflow considerations for large numbers

5. IMPLEMENTATION DETAILS:
   - Precompute LCMs for efficiency
   - Handle integer overflow in LCM calculations
   - Use proper binary search template (avoid infinite loops)

6. COMPLEXITY ANALYSIS:
   - Time: O(log(2×10^9)) per binary search iteration
   - Each iteration does O(1) work (constant time counting)
   - Total: O(log n) where n is the upper bound
   - Space: O(1) - only storing a few variables

7. FOLLOW-UP QUESTIONS THEY MIGHT ASK:
   - "What if we had k numbers instead of 3?" → Generalize inclusion-exclusion
   - "How do you handle overflow?" → Use (x//gcd) * y for LCM
   - "Can you solve without binary search?" → Discuss mathematical approaches
   - "What's the bottleneck?" → LCM calculations and binary search bounds

8. RECOMMENDED INTERVIEW STRATEGY:
   1. Start with brute force to show understanding
   2. Identify why it's too slow (large constraints)
   3. Propose binary search: "What if we search for the answer?"
   4. Explain counting strategy (inclusion-exclusion)
   5. Code the solution with clear helper functions
   6. Walk through an example to verify correctness
   7. Analyze time complexity and discuss optimizations

9. COMMON MISTAKES TO AVOID:
   - Forgetting inclusion-exclusion (just adding counts)
   - Integer overflow in LCM calculations
   - Wrong binary search bounds or infinite loops
   - Not handling edge cases (n=1, a=b=c, etc.)

10. WHY THIS PROBLEM IS GREAT FOR INTERVIEWS:
    - Combines multiple advanced concepts (binary search + number theory)
    - Has clear brute force → optimal solution progression  
    - Tests mathematical reasoning and implementation skills
    - Scalable to different variations and follow-ups
    - Demonstrates problem-solving methodology

This problem showcases the beautiful intersection of algorithms and mathematics
that big tech companies love to see!
"""

if __name__ == "__main__":
    test_solutions()
    visualize_ugly_numbers(10, 2, 3, 5, 30)
    explain_inclusion_exclusion() 
    analyze_binary_search_bounds()
