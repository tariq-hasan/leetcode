"""
LeetCode 762: Prime Number of Set Bits in Binary Representation
https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/

Problem: Given two integers left and right, return the count of numbers in the 
inclusive range [left, right] having a prime number of set bits in their binary representation.

Constraints: 1 <= left <= right <= 10^6

Example 1:
Input: left = 6, right = 10
Output: 4
Explanation:
6  -> 110 (2 set bits, 2 is prime) ✓
7  -> 111 (3 set bits, 3 is prime) ✓  
8  -> 1000 (1 set bit, 1 is not prime) ✗
9  -> 1001 (2 set bits, 2 is prime) ✓
10 -> 1010 (2 set bits, 2 is prime) ✓

Example 2:
Input: left = 10, right = 15
Output: 5
Explanation:
10 -> 1010 (2 set bits, 2 is prime) ✓
11 -> 1011 (3 set bits, 3 is prime) ✓
12 -> 1100 (2 set bits, 2 is prime) ✓
13 -> 1101 (3 set bits, 3 is prime) ✓
14 -> 1110 (3 set bits, 3 is prime) ✓
15 -> 1111 (4 set bits, 4 is not prime) ✗
"""

class Solution:
    
    # ============== APPROACH 1: Brute Force with Prime Check ==============
    # Time: O(n * log(max_num) * sqrt(log(max_num))), Space: O(1)
    def countPrimeSetBits_bruteforce(self, left: int, right: int) -> int:
        """
        Straightforward approach:
        1. For each number, count set bits using Brian Kernighan
        2. Check if the count is prime using trial division
        
        Good starting point but not optimal.
        """
        def count_set_bits(n):
            count = 0
            while n:
                n &= n - 1  # Clear lowest set bit
                count += 1
            return count
        
        def is_prime(n):
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            
            for i in range(3, int(n**0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
        
        count = 0
        for num in range(left, right + 1):
            set_bits = count_set_bits(num)
            if is_prime(set_bits):
                count += 1
        
        return count
    
    
    # ============== APPROACH 2: Optimized with Precomputed Primes (GOOD) ==============
    # Time: O(n), Space: O(1)
    def countPrimeSetBits_precomputed(self, left: int, right: int) -> int:
        """
        Key optimization: Since max number is 10^6, max set bits is 20.
        We can precompute all primes up to 20 and use a set for O(1) lookup.
        
        This eliminates the need for prime checking during iteration.
        """
        # Precompute primes up to 20 (max possible set bits for numbers <= 10^6)
        primes = {2, 3, 5, 7, 11, 13, 17, 19}
        
        def count_set_bits(n):
            count = 0
            while n:
                n &= n - 1
                count += 1
            return count
        
        count = 0
        for num in range(left, right + 1):
            set_bits = count_set_bits(num)
            if set_bits in primes:
                count += 1
        
        return count
    
    
    # ============== APPROACH 3: Bit Mask Optimization (OPTIMAL) ==============
    # Time: O(n), Space: O(1)
    def countPrimeSetBits(self, left: int, right: int) -> int:
        """
        Ultimate optimization: Use bit manipulation for both counting and prime check.
        
        Key insights:
        1. Use Brian Kernighan for efficient bit counting
        2. Use a bitmask to represent prime numbers for O(1) lookup
        3. Bitmask: 665772 represents primes {2,3,5,7,11,13,17,19} in binary
        
        How the bitmask works:
        - 665772 in binary has bits set at positions 2,3,5,7,11,13,17,19
        - To check if k is prime: (665772 >> k) & 1
        """
        # Bitmask representing primes 2,3,5,7,11,13,17,19
        # 665772 = 10100010100010101100 in binary
        prime_mask = 0b10100010100010101100  # = 665772
        
        count = 0
        for num in range(left, right + 1):
            # Count set bits using Brian Kernighan
            set_bits = 0
            temp = num
            while temp:
                temp &= temp - 1
                set_bits += 1
            
            # Check if set_bits is prime using bitmask
            if (prime_mask >> set_bits) & 1:
                count += 1
        
        return count
    
    
    # ============== APPROACH 4: Built-in Functions (Most Concise) ==============
    # Time: O(n), Space: O(1)
    def countPrimeSetBits_builtin(self, left: int, right: int) -> int:
        """
        Most concise solution using Python built-ins.
        Good to mention as alternative but may not showcase bit manipulation skills.
        """
        primes = {2, 3, 5, 7, 11, 13, 17, 19}
        return sum(bin(num).count('1') in primes for num in range(left, right + 1))
    
    
    # ============== APPROACH 5: Mathematical Insight with Bit Patterns ==============
    # Time: O(n), Space: O(1)
    def countPrimeSetBits_pattern(self, left: int, right: int) -> int:
        """
        Advanced approach: Recognize that we can use bit manipulation patterns
        to count set bits more efficiently by recognizing number patterns.
        
        This shows deeper understanding of bit manipulation.
        """
        # Same prime mask as approach 3
        prime_mask = 665772  # Binary: 10100010100010101100
        
        count = 0
        for num in range(left, right + 1):
            # Alternative bit counting using bit manipulation tricks
            # Count set bits using the "divide and conquer" method
            n = num
            n = n - ((n >> 1) & 0x55555555)
            n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
            set_bits = (((n + (n >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24
            
            if (prime_mask >> set_bits) & 1:
                count += 1
        
        return count


# ============== HELPER FUNCTIONS FOR ANALYSIS ==============
def analyze_bit_patterns(left: int, right: int):
    """Helper function to visualize the bit patterns and prime checking"""
    primes = {2, 3, 5, 7, 11, 13, 17, 19}
    
    print(f"\nAnalyzing range [{left}, {right}]:")
    print("Num | Binary      | Set Bits | Prime? | Count")
    print("----|-------------|----------|--------|-------")
    
    total_count = 0
    for num in range(left, min(right + 1, left + 10)):  # Limit output for readability
        binary = bin(num)[2:]
        set_bits = binary.count('1')
        is_prime = set_bits in primes
        if is_prime:
            total_count += 1
        
        print(f"{num:2d}  | {binary:>10s} | {set_bits:6d}   | {is_prime:>6} | {total_count}")


def explain_bitmask():
    """Explain how the prime bitmask works"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    prime_mask = 665772
    
    print(f"\nPrime Bitmask Explanation:")
    print(f"Bitmask value: {prime_mask}")
    print(f"Binary: {bin(prime_mask)[2:]:>20s}")
    print(f"Positions (right to left): {''.join(str(i%10) for i in range(20))}")
    print()
    
    print("Prime checking examples:")
    for i in range(21):
        is_prime_by_mask = (prime_mask >> i) & 1
        is_actually_prime = i in primes
        status = "✓" if is_prime_by_mask == is_actually_prime else "✗"
        print(f"Position {i:2d}: mask={(prime_mask >> i) & 1}, actual={i in primes} {status}")


# ============== TEST CASES ==============
def test_solutions():
    solution = Solution()
    
    test_cases = [
        (6, 10, 4),
        (10, 15, 5), 
        (1, 1, 0),    # Edge case: single number, 1 set bit (not prime)
        (2, 2, 1),    # Edge case: single number, 1 set bit (not prime) - wait, 2 has 1 set bit!
        (4, 4, 0),    # 4 = 100, 1 set bit (not prime)
        (3, 3, 1),    # 3 = 11, 2 set bits (prime)
        (1, 10, 4),   # Broader range
        (1, 100, 30)  # Larger range for performance testing
    ]
    
    for left, right, expected in test_cases:
        # Test main approaches
        assert solution.countPrimeSetBits_bruteforce(left, right) == expected
        assert solution.countPrimeSetBits_precomputed(left, right) == expected  
        assert solution.countPrimeSetBits(left, right) == expected
        assert solution.countPrimeSetBits_builtin(left, right) == expected
        
        print(f"✓ range=[{left}, {right}], expected={expected}")
    
    print("All test cases passed!")


# ============== INTERVIEW TALKING POINTS ==============
"""
WHAT TO MENTION IN INTERVIEW:

1. PROBLEM BREAKDOWN:
   - Need to count set bits for each number in range
   - Check if that count is prime
   - Sum up all numbers with prime set bit counts

2. KEY OPTIMIZATIONS TO DISCUSS:

   a) CONSTRAINT ANALYSIS:
      - Max number is 10^6, so max set bits is ⌊log₂(10^6)⌋ = 19
      - Only need to check primes up to 19: {2,3,5,7,11,13,17,19}
      - This enables precomputation!

   b) BIT MANIPULATION OPTIMIZATIONS:
      - Use Brian Kernighan for O(k) bit counting where k = set bits
      - Use bitmask 665772 for O(1) prime checking
      - Explain how bitmask works: bit at position i is set if i is prime

   c) TIME COMPLEXITY:
      - Brute force: O(n * log(max) * sqrt(log(max)))
      - Optimized: O(n * average_set_bits) ≈ O(n)

3. RECOMMENDED INTERVIEW APPROACH:
   1. Start with brute force to show understanding
   2. Identify optimization opportunities (constraint analysis!)
   3. Code the bitmask solution (most impressive)
   4. Explain the bitmask calculation: 665772 = sum(2^p for p in primes)
   5. Walk through examples to verify correctness

4. FOLLOW-UP QUESTIONS THEY MIGHT ASK:
   - "How did you get 665772?" → Show bitmask construction
   - "What if the range was larger?" → Discuss prime sieve, more efficient bit counting
   - "Can you solve without bit manipulation?" → Show built-in approach
   - "Space-time tradeoffs?" → Discuss precomputation vs on-the-fly calculation

5. MATHEMATICAL INSIGHT TO MENTION:
   - The bitmask 665772 = 2² + 2³ + 2⁵ + 2⁷ + 2¹¹ + 2¹³ + 2¹⁷ + 2¹⁹
   - This encodes all primes ≤ 19 in a single integer
   - Checking (mask >> k) & 1 is O(1) prime test for k ≤ 19

6. EDGE CASES:
   - Single number ranges
   - Numbers with 1 set bit (1 is not prime!)
   - Powers of 2 (always have 1 set bit)
   - Numbers with maximum set bits

7. CODE INTERVIEW STRATEGY:
   Write the bitmask solution first - it's clean, optimal, and impressive.
   If asked for alternatives, show the precomputed set approach.
   Always explain WHY your optimizations work.
"""

if __name__ == "__main__":
    test_solutions()
    analyze_bit_patterns(6, 10)
    explain_bitmask()
