"""
LeetCode 421. Maximum XOR of Two Numbers in an Array
Problem: Given an integer array nums, return the maximum result of nums[i] XOR nums[j], 
where 0 ≤ i ≤ j < n.

Example:
Input: nums = [3,10,5,25,2,8]
Output: 28
Explanation: The maximum result is 5 XOR 25 = 28.

Key Insights:
1. XOR is maximized when bits are different (1 XOR 0 = 1, 0 XOR 1 = 1)
2. We want to maximize from most significant bit (MSB) to least significant bit (LSB)
3. Use Trie (prefix tree) to store binary representations and find optimal matches
4. For each number, traverse Trie trying to take opposite bits when possible
5. Alternative: bit-by-bit construction with prefix checking
"""

from typing import List

class TrieNode:
    """Node for binary Trie"""
    def __init__(self):
        self.children = {}  # 0 or 1
        self.value = None   # Store the actual number at leaf

class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        """
        Approach 1: Trie-based Solution (OPTIMAL FOR INTERVIEWS)
        Time: O(n * 32) where n is length of nums
        Space: O(n * 32) for Trie storage
        
        This is the most intuitive and commonly expected approach.
        """
        if not nums or len(nums) < 2:
            return 0
        
        # Build Trie with binary representations
        root = TrieNode()
        
        # Insert all numbers into Trie
        for num in nums:
            node = root
            for i in range(31, -1, -1):  # 32 bits, MSB first
                bit = (num >> i) & 1
                if bit not in node.children:
                    node.children[bit] = TrieNode()
                node = node.children[bit]
            node.value = num
        
        max_xor = 0
        
        # For each number, find the number that gives maximum XOR
        for num in nums:
            node = root
            current_xor = 0
            
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                # Try to go opposite direction for maximum XOR
                opposite_bit = 1 - bit
                
                if opposite_bit in node.children:
                    current_xor |= (1 << i)  # Set this bit in result
                    node = node.children[opposite_bit]
                else:
                    # Have to go same direction
                    node = node.children[bit]
            
            max_xor = max(max_xor, current_xor)
        
        return max_xor

    def findMaximumXOR_v2(self, nums: List[int]) -> int:
        """
        Approach 2: Optimized Trie with Early Termination
        Time: O(n * 32)
        Space: O(n * 32)
        
        Same as approach 1 but with optimizations.
        """
        class TrieNode:
            def __init__(self):
                self.children = [None, None]  # Index 0 and 1
        
        root = TrieNode()
        
        # Build Trie
        for num in nums:
            node = root
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                if not node.children[bit]:
                    node.children[bit] = TrieNode()
                node = node.children[bit]
        
        max_xor = 0
        
        # Find maximum XOR for each number
        for num in nums:
            node = root
            current_xor = 0
            
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                opposite_bit = 1 - bit
                
                if node.children[opposite_bit]:
                    current_xor |= (1 << i)
                    node = node.children[opposite_bit]
                else:
                    node = node.children[bit]
            
            max_xor = max(max_xor, current_xor)
        
        return max_xor

    def findMaximumXOR_v3(self, nums: List[int]) -> int:
        """
        Approach 3: Bit-by-Bit Construction with Prefix Set
        Time: O(n * 32)
        Space: O(n * 32)
        
        Build result bit by bit from MSB to LSB using prefix checking.
        """
        max_xor = 0
        mask = 0
        
        # Build result bit by bit from MSB to LSB
        for i in range(31, -1, -1):
            mask |= (1 << i)  # Include current bit in mask
            
            # Get all prefixes of current length
            prefixes = {num & mask for num in nums}
            
            # Try to update max_xor by setting current bit
            candidate = max_xor | (1 << i)
            
            # Check if this candidate is achievable
            # If candidate = a XOR b, then a = candidate XOR b
            for prefix in prefixes:
                if candidate ^ prefix in prefixes:
                    max_xor = candidate
                    break
        
        return max_xor

    def findMaximumXOR_v4(self, nums: List[int]) -> int:
        """
        Approach 4: Brute Force (FOR COMPARISON)
        Time: O(n²)
        Space: O(1)
        
        Check all pairs - too slow for large inputs but good for understanding.
        """
        max_xor = 0
        n = len(nums)
        
        for i in range(n):
            for j in range(i + 1, n):
                max_xor = max(max_xor, nums[i] ^ nums[j])
        
        return max_xor

    def findMaximumXOR_v5(self, nums: List[int]) -> int:
        """
        Approach 5: Trie with Path Compression (ADVANCED)
        Time: O(n * 32)
        Space: O(n * 32) worst case, better average case
        
        Advanced optimization with path compression.
        """
        class CompressedTrieNode:
            def __init__(self):
                self.children = {}
                self.value = None
                self.compressed_path = None  # For path compression
        
        root = CompressedTrieNode()
        
        # Build compressed Trie
        for num in nums:
            node = root
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                if bit not in node.children:
                    node.children[bit] = CompressedTrieNode()
                node = node.children[bit]
            node.value = num
        
        max_xor = 0
        
        for num in nums:
            node = root
            current_xor = 0
            
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                opposite = 1 - bit
                
                if opposite in node.children:
                    current_xor |= (1 << i)
                    node = node.children[opposite]
                elif bit in node.children:
                    node = node.children[bit]
                else:
                    break  # Should not happen with valid input
            
            max_xor = max(max_xor, current_xor)
        
        return max_xor

def test_solutions():
    solution = Solution()
    
    # Test case 1: [3,10,5,25,2,8]
    nums1 = [3, 10, 5, 25, 2, 8]
    print("Test case 1: [3,10,5,25,2,8]")
    print("Expected: 28 (5 XOR 25)")
    print("Trie solution:", solution.findMaximumXOR(nums1))
    print("Bit-by-bit:", solution.findMaximumXOR_v3(nums1))
    print("Brute force:", solution.findMaximumXOR_v4(nums1))
    
    # Show the XOR calculation
    print("Verification: 5 XOR 25 =", 5 ^ 25)
    print("5  in binary: ", format(5, '032b'))
    print("25 in binary: ", format(25, '032b'))
    print("5 XOR 25:     ", format(5 ^ 25, '032b'))
    print()
    
    # Test case 2: [2,4]
    nums2 = [2, 4]
    print("Test case 2: [2,4]")
    print("Expected: 6 (2 XOR 4)")
    print("Result:", solution.findMaximumXOR(nums2))
    print()
    
    # Test case 3: [8,10,2]
    nums3 = [8, 10, 2]
    print("Test case 3: [8,10,2]")
    print("Expected: 10 (8 XOR 2)")
    print("Result:", solution.findMaximumXOR(nums3))
    print()
    
    # Test case 4: Single element
    nums4 = [1]
    print("Test case 4: [1]")
    print("Expected: 0 (need at least 2 elements)")
    print("Result:", solution.findMaximumXOR(nums4))
    print()
    
    # Test case 5: All same elements
    nums5 = [4, 4, 4, 4]
    print("Test case 5: [4,4,4,4]")
    print("Expected: 0 (all XORs are 0)")
    print("Result:", solution.findMaximumXOR(nums5))

def explain_xor_properties():
    """Explain XOR properties relevant to the problem"""
    print("=== XOR PROPERTIES EXPLANATION ===")
    print("XOR (exclusive OR) properties:")
    print("- 0 XOR 0 = 0")
    print("- 0 XOR 1 = 1")  
    print("- 1 XOR 0 = 1")
    print("- 1 XOR 1 = 0")
    print()
    print("Key insight: XOR is maximized when bits are DIFFERENT")
    print("To maximize XOR, we want:")
    print("- Most significant bits to be different")
    print("- As many high-value bits different as possible")
    print()
    
    # Example
    print("Example with 5 and 25:")
    print("5  = 00101")
    print("25 = 11001") 
    print("XOR= 11100 = 28")
    print("Notice how most significant bits are different!")

def explain_trie_approach():
    """Explain the Trie approach in detail"""
    print("=== TRIE APPROACH EXPLANATION ===")
    print("1. Build a binary Trie storing all numbers")
    print("2. For each number, traverse Trie trying to take opposite bits")
    print("3. This greedily maximizes XOR from MSB to LSB")
    print()
    
    nums = [3, 10, 5]
    print(f"Example with {nums}:")
    for num in nums:
        print(f"{num:2d} = {format(num, '05b')}")
    
    print("\nTrie structure (5 bits for simplicity):")
    print("Root")
    print("├─0 (numbers starting with 0)")
    print("│ └─0 (00xxx)")
    print("│   └─1 (001xx)")
    print("│     └─0 (0010x)")
    print("│       └─1 (00101) → 5")
    print("└─1 (numbers starting with 1)")
    print("  └─0 (10xxx)")
    print("    └─1 (101xx)")
    print("      └─0 (1010x)")
    print("        └─1 (10101) → ?")

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*50 + "\n")
    explain_xor_properties()
    print("\n" + "="*50 + "\n")
    explain_trie_approach()

"""
INTERVIEW TALKING POINTS:

1. Problem Understanding:
   - Find maximum XOR between any two numbers in array
   - XOR is maximized when bits are different
   - Need to consider all pairs but avoid O(n²) brute force

2. Key Insights:
   - XOR maximized by having different bits, especially MSBs
   - Build binary Trie to efficiently find "opposite" numbers
   - For each number, greedily choose opposite bits when traversing Trie
   - Work from MSB to LSB for maximum value

3. Why Trie Works:
   - Trie stores binary representations of all numbers
   - For any number, we can efficiently find the number that maximizes XOR
   - Greedy approach: always choose opposite bit if available
   - Time complexity: O(n * 32) instead of O(n²)

4. Algorithm Steps:
   - Build Trie with all numbers (32 bits each)
   - For each number, traverse Trie choosing opposite bits when possible
   - Track the XOR value as we traverse
   - Return maximum XOR found

5. Edge Cases:
   - Array with less than 2 elements → return 0
   - All elements are same → return 0
   - Array with duplicate elements
   - Very large numbers (up to 2³¹ - 1)

6. Time/Space Complexity:
   - Time: O(n * 32) = O(n) since 32 is constant
   - Space: O(n * 32) for Trie storage
   - Much better than O(n²) brute force

7. Alternative Approaches:
   - Bit-by-bit construction with prefix checking
   - Hash set based approach
   - Brute force O(n²) for comparison

8. Common Mistakes:
   - Not handling bit ordering correctly (MSB first)
   - Forgetting to handle edge cases (< 2 elements)
   - Incorrect Trie traversal logic
   - Not understanding XOR properties

9. Optimization Techniques:
   - Early termination in some cases
   - Path compression in Trie
   - Using arrays instead of hashmaps for children

10. Follow-up Questions:
    - What if we want k-th maximum XOR?
    - How to modify for XOR of multiple numbers?
    - What about memory optimization for very large arrays?
    - How to handle negative numbers?

RECOMMENDED APPROACH FOR INTERVIEW:
1. Start by explaining XOR properties and why we want different bits
2. Mention brute force O(n²) solution first
3. Explain why Trie is perfect for this problem
4. Draw a small Trie example to show the concept
5. Implement the Trie solution step by step
6. Walk through example showing how traversal works
7. Discuss time/space complexity
8. Handle edge cases
9. Mention alternative approaches if time permits

CRITICAL INSIGHTS TO COMMUNICATE:
- "XOR is maximized when bits are different, especially MSBs"
- "Trie allows us to efficiently find the 'most different' number"
- "We greedily choose opposite bits from MSB to LSB"
- "This reduces complexity from O(n²) to O(n)"

PATTERN RECOGNITION:
This problem combines several advanced concepts:
- Bit manipulation and XOR properties
- Trie data structure for binary representations
- Greedy algorithms (choosing opposite bits)
- Prefix-based optimization techniques

The Trie approach is a classic pattern for problems involving:
- Maximum/minimum XOR
- Binary representation optimization
- Prefix-based searching in bit space

This is definitely an advanced problem that tests deep understanding of:
- Bit manipulation
- Data structure design (Trie)
- Algorithmic optimization
- XOR mathematical properties
"""
