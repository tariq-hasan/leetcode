"""
LeetCode 1915. Number of Wonderful Substrings
Problem: A wonderful string is a string where at most one letter appears an odd number of times.
Given a string word consisting only of the first ten lowercase English letters ('a' to 'j'), 
return the number of wonderful non-empty substrings in word. If the same substring appears 
multiple times, count each occurrence separately.

Example:
Input: word = "aba"
Output: 4
Explanation: The four wonderful substrings are "a", "b", "a", and "aba".

Key Insights:
1. A wonderful string has at most one character with odd frequency
2. Use bit manipulation: each bit represents whether a character has odd count
3. Two substrings have same parity if their XOR is 0 or has exactly one bit set
4. Use prefix XOR with frequency counting to avoid O(n²) brute force
5. Only 10 possible characters, so bitmask fits in 10 bits (0 to 1023)
"""

from typing import Dict
from collections import defaultdict

class Solution:
    def wonderfulSubstrings(self, word: str) -> int:
        """
        Approach 1: Bit Manipulation with Prefix XOR (OPTIMAL SOLUTION)
        Time: O(n) where n is length of word
        Space: O(1) since we have at most 2^10 = 1024 possible states
        
        This is the optimal solution that most interviewers expect.
        """
        # freq[mask] = number of prefixes with this bitmask
        freq = defaultdict(int)
        freq[0] = 1  # Empty prefix has bitmask 0
        
        current_mask = 0
        result = 0
        
        for char in word:
            # Update current bitmask by flipping bit for this character
            bit_position = ord(char) - ord('a')
            current_mask ^= (1 << bit_position)
            
            # Case 1: Substring with all even frequencies
            # Look for previous prefix with same mask
            result += freq[current_mask]
            
            # Case 2: Substring with exactly one odd frequency
            # Look for previous prefixes that differ by exactly one bit
            for i in range(10):
                target_mask = current_mask ^ (1 << i)
                result += freq[target_mask]
            
            # Update frequency of current mask
            freq[current_mask] += 1
        
        return result

    def wonderfulSubstrings_v2(self, word: str) -> int:
        """
        Approach 2: Bit Manipulation with Array (Space Optimized)
        Time: O(n)
        Space: O(2^10) = O(1024) = O(1)
        
        Use array instead of hashmap since we know exact range of masks.
        """
        # Since we have 10 characters, we have 2^10 = 1024 possible masks
        freq = [0] * 1024
        freq[0] = 1  # Empty prefix
        
        current_mask = 0
        result = 0
        
        for char in word:
            # Flip bit for current character
            current_mask ^= (1 << (ord(char) - ord('a')))
            
            # Count substrings with all even frequencies
            result += freq[current_mask]
            
            # Count substrings with exactly one odd frequency
            for i in range(10):
                result += freq[current_mask ^ (1 << i)]
            
            freq[current_mask] += 1
        
        return result

    def wonderfulSubstrings_v3(self, word: str) -> int:
        """
        Approach 3: Brute Force with Optimization (FOR UNDERSTANDING)
        Time: O(n²)
        Space: O(1)
        
        Check all substrings but use running count to avoid O(n³).
        This helps understand the problem but is not optimal.
        """
        def is_wonderful(s):
            """Check if string has at most one character with odd frequency"""
            count = [0] * 10
            for char in s:
                count[ord(char) - ord('a')] += 1
            
            odd_count = sum(1 for c in count if c % 2 == 1)
            return odd_count <= 1
        
        result = 0
        n = len(word)
        
        for i in range(n):
            char_count = [0] * 10
            for j in range(i, n):
                # Update count for current character
                char_count[ord(word[j]) - ord('a')] += 1
                
                # Check if current substring is wonderful
                odd_count = sum(1 for c in char_count if c % 2 == 1)
                if odd_count <= 1:
                    result += 1
        
        return result

    def wonderfulSubstrings_v4(self, word: str) -> int:
        """
        Approach 4: Detailed Explanation Version
        Time: O(n)
        Space: O(1)
        
        Same as approach 1 but with detailed comments for learning.
        """
        # Each bit in mask represents whether character has odd frequency
        # mask = 0 means all characters have even frequency
        # mask with exactly one bit set means one character has odd frequency
        
        mask_frequency = {}
        mask_frequency[0] = 1  # Empty prefix contributes one way
        
        current_mask = 0
        wonderful_count = 0
        
        for i, char in enumerate(word):
            char_index = ord(char) - ord('a')
            
            # XOR flips the bit: 0->1 (even to odd), 1->0 (odd to even)
            current_mask ^= (1 << char_index)
            
            # Scenario 1: All characters in substring have even frequency
            # This happens when current_mask equals some previous mask
            if current_mask in mask_frequency:
                wonderful_count += mask_frequency[current_mask]
            
            # Scenario 2: Exactly one character has odd frequency
            # This happens when current_mask differs from previous mask by exactly one bit
            for bit in range(10):
                # Create mask that differs by one bit
                target_mask = current_mask ^ (1 << bit)
                if target_mask in mask_frequency:
                    wonderful_count += mask_frequency[target_mask]
            
            # Update frequency count for current mask
            mask_frequency[current_mask] = mask_frequency.get(current_mask, 0) + 1
        
        return wonderful_count

    def wonderfulSubstrings_debug(self, word: str) -> int:
        """
        Approach 5: Debug Version (Shows all wonderful substrings)
        Time: O(n²)
        Space: O(n²)
        
        For understanding - shows which substrings are wonderful.
        """
        def get_mask(s):
            """Get bitmask for string"""
            mask = 0
            for char in s:
                mask ^= (1 << (ord(char) - ord('a')))
            return mask
        
        def is_wonderful_mask(mask):
            """Check if mask represents wonderful string"""
            # Count number of set bits (odd frequencies)
            count = 0
            while mask:
                count += mask & 1
                mask >>= 1
            return count <= 1
        
        result = 0
        wonderful_substrings = []
        n = len(word)
        
        for i in range(n):
            for j in range(i + 1, n + 1):
                substring = word[i:j]
                mask = get_mask(substring)
                if is_wonderful_mask(mask):
                    result += 1
                    wonderful_substrings.append(substring)
        
        print(f"Wonderful substrings: {wonderful_substrings}")
        return result

# Test the solutions
def test_solutions():
    solution = Solution()
    
    # Test case 1: "aba"
    word1 = "aba"
    print(f"Test case 1: word = '{word1}'")
    print("Expected: 4")
    print("Optimal solution:", solution.wonderfulSubstrings(word1))
    print("Array version:", solution.wonderfulSubstrings_v2(word1))
    print("Debug version:", solution.wonderfulSubstrings_debug(word1))
    print()
    
    # Test case 2: "aabb"
    word2 = "aabb"
    print(f"Test case 2: word = '{word2}'")
    print("Expected: 9")
    print("Result:", solution.wonderfulSubstrings(word2))
    print()
    
    # Test case 3: "he"
    word3 = "he"
    print(f"Test case 3: word = '{word3}'")
    print("Expected: 2")
    print("Result:", solution.wonderfulSubstrings(word3))
    print()
    
    # Test case 4: Single character
    word4 = "a"
    print(f"Test case 4: word = '{word4}'")
    print("Expected: 1")
    print("Result:", solution.wonderfulSubstrings(word4))
    print()
    
    # Test case 5: All same characters
    word5 = "aaaa"
    print(f"Test case 5: word = '{word5}'")
    print("Expected: 10 (all substrings are wonderful)")
    print("Result:", solution.wonderfulSubstrings(word5))

def explain_bit_manipulation():
    """Explain the bit manipulation concept"""
    print("=== BIT MANIPULATION EXPLANATION ===")
    print("Each bit position represents a character (a=0, b=1, c=2, ...)")
    print("Bit value: 0 = even frequency, 1 = odd frequency")
    print()
    
    examples = [
        ("", 0, "All even frequencies"),
        ("a", 1, "Only 'a' has odd frequency"), 
        ("ab", 3, "'a' and 'b' have odd frequencies - NOT wonderful"),
        ("aa", 0, "'a' has even frequency"),
        ("aba", 1, "Only 'b' has odd frequency"),
    ]
    
    for string, expected_mask, explanation in examples:
        mask = 0
        for char in string:
            mask ^= (1 << (ord(char) - ord('a')))
        
        bit_count = bin(mask).count('1')
        is_wonderful = bit_count <= 1
        
        print(f"String: '{string}' -> Mask: {mask:04b} ({mask}) -> {explanation}")
        print(f"  Wonderful: {is_wonderful} (has {bit_count} odd frequencies)")
        print()

if __name__ == "__main__":
    test_solutions()
    print()
    explain_bit_manipulation()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - A wonderful string has AT MOST one character with odd frequency
   - Need to count all wonderful substrings (including single characters)
   - Only characters 'a' to 'j' (10 characters total)
   - Same substring at different positions counts separately

2. Key Insights:
   - Brute force O(n³) is too slow - need to optimize
   - Use bit manipulation: each bit represents odd/even frequency
   - XOR operation naturally tracks parity (even/odd)
   - Prefix technique: if two prefixes have "compatible" masks, substring between them is wonderful

3. Bit Manipulation Magic:
   - Mask = 0: all characters have even frequency (wonderful)
   - Mask with 1 bit set: one character has odd frequency (wonderful)  
   - Mask with 2+ bits set: multiple odd frequencies (not wonderful)
   - XOR flips bits: even->odd, odd->even

4. Core Algorithm:
   - Track running XOR mask as we process each character
   - For each position, count previous prefixes that would create wonderful substring
   - Two cases: same mask (all even) or differ by one bit (one odd)

5. Why This Works:
   - XOR(prefix_i, prefix_j) gives frequency parity of substring[i+1:j+1]
   - If XOR has 0 or 1 bits set, substring is wonderful
   - Use hashmap to count occurrences of each mask

6. Edge Cases:
   - Single characters (always wonderful)
   - Empty string (mask = 0)
   - All same characters
   - Maximum length strings

7. Time/Space Complexity:
   - Time: O(n) - single pass with constant work per character
   - Space: O(1) - at most 2^10 = 1024 possible masks

8. Common Mistakes:
   - Forgetting empty prefix (mask_frequency[0] = 1)
   - Not checking all 10 possible single-bit differences
   - Confusing XOR operation (it tracks parity, not count)
   - Off-by-one errors in bit manipulation

9. Alternative Approaches:
   - Brute force O(n²) with running count
   - Different data structures (array vs hashmap)
   - Bit manipulation optimizations

10. Follow-up Questions:
    - What if we had more characters? (larger bitmask)
    - What if we wanted exactly k odd frequencies?
    - How to modify for longest wonderful substring?
    - Memory optimization for very long strings?

RECOMMENDED APPROACH FOR INTERVIEW:
1. Start by understanding what makes a string "wonderful"
2. Explain why brute force is too slow
3. Introduce bit manipulation concept with examples
4. Show how XOR tracks frequency parity
5. Explain prefix technique and why it works
6. Implement the optimal O(n) solution
7. Walk through example showing mask evolution
8. Handle edge cases and discuss complexity

CRITICAL INSIGHTS TO COMMUNICATE:
- "XOR naturally tracks whether we've seen a character an odd or even number of times"
- "A wonderful substring exists between two prefixes if their masks are the same or differ by exactly one bit"
- "We can use a hashmap to count how many times we've seen each mask pattern"

This is an advanced problem that combines multiple concepts:
- Bit manipulation for state representation
- Prefix techniques for optimization  
- XOR properties for parity tracking
- Combinatorial counting

The key is explaining each concept clearly and showing how they work together.
"""
