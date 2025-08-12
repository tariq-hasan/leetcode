"""
LeetCode 763: Partition Labels

Problem Statement:
You are given a string s. We want to partition this string into as many parts as possible 
so that each letter appears in at most one part.

Note that the partition is done so that after concatenating all the parts in order, 
the resultant string should be the original string.

Return a list of integers representing the size of these parts.

Example 1:
Input: s = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.

Example 2:
Input: s = "eccbbbbdec"
Output: [10]
"""

def partitionLabels(s):
    """
    Approach: Greedy Algorithm with Two Passes
    
    Key Insight: For each character, we need to know its last occurrence position.
    Then, we extend the current partition until we've seen all characters completely.
    
    Algorithm:
    1. First pass: Record the last occurrence of each character
    2. Second pass: Use greedy approach to determine partition boundaries
       - Keep track of the farthest position we need to reach
       - When current index equals the farthest position, we can make a partition
    
    Time Complexity: O(n) - two passes through the string
    Space Complexity: O(1) - at most 26 characters in the hash map
    """
    
    # Step 1: Record the last occurrence of each character
    last_occurrence = {}
    for i, char in enumerate(s):
        last_occurrence[char] = i
    
    # Step 2: Greedily determine partition boundaries
    result = []
    start = 0  # Start of current partition
    end = 0    # End boundary of current partition
    
    for i, char in enumerate(s):
        # Extend the end boundary if this character's last occurrence is farther
        end = max(end, last_occurrence[char])
        
        # If we've reached the end boundary, we can partition here
        if i == end:
            result.append(end - start + 1)
            start = i + 1  # Start of next partition
    
    return result


def partitionLabels_alternative(s):
    """
    Alternative implementation with more explicit tracking
    """
    # Find last occurrence of each character
    last = {char: i for i, char in enumerate(s)}
    
    partitions = []
    partition_start = 0
    partition_end = 0
    
    for i, char in enumerate(s):
        # Extend current partition to include this character's last occurrence
        partition_end = max(partition_end, last[char])
        
        # If we've processed all characters in the current partition
        if i == partition_end:
            partitions.append(partition_end - partition_start + 1)
            partition_start = i + 1
    
    return partitions


# Test cases
def test_solution():
    """Test the solution with provided examples and edge cases"""
    
    test_cases = [
        ("ababcbacadefegdehijhklij", [9, 7, 8]),
        ("eccbbbbdec", [10]),
        ("a", [1]),
        ("abc", [1, 1, 1]),
        ("aaaa", [4]),
        ("abcabc", [6])
    ]
    
    print("Testing partitionLabels function:")
    print("=" * 50)
    
    for i, (input_str, expected) in enumerate(test_cases, 1):
        result = partitionLabels(input_str)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        print(f"Test Case {i}: {status}")
        print(f"  Input: '{input_str}'")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        print()

# Run tests
if __name__ == "__main__":
    test_solution()


"""
INTERVIEW DISCUSSION POINTS:

1. TIME & SPACE COMPLEXITY:
   - Time: O(n) where n is length of string
   - Space: O(1) since we have at most 26 lowercase letters

2. KEY INSIGHTS:
   - We need to know the last occurrence of each character
   - Use greedy approach: extend current partition until all seen characters are complete
   - A partition is complete when current index equals the farthest last occurrence

3. EDGE CASES TO CONSIDER:
   - Single character string
   - All characters are the same
   - All characters are different
   - Empty string (though constraints say 1 <= s.length <= 500)

4. ALTERNATIVE APPROACHES:
   - Could use a more complex approach with intervals, but this greedy solution is optimal
   - The two-pass approach is necessary because we need to know last occurrences upfront

5. FOLLOW-UP QUESTIONS YOU MIGHT GET:
   - What if we wanted to minimize the number of partitions instead?
   - What if characters could repeat in different partitions?
   - How would this change with different character sets?
"""
