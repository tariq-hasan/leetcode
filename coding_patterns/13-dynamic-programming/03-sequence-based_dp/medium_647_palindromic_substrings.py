"""
LeetCode 647: Palindromic Substrings

Problem: Given a string s, return the number of palindromic substrings in it.
A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

Example 1:
Input: s = "abc"
Output: 3
Explanation: Three palindromic strings: "a", "b", "c".

Example 2:
Input: s = "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

KEY INSIGHT: Multiple approaches with different trade-offs
1. Expand Around Centers - O(n²) time, O(1) space - RECOMMENDED for interviews
2. Dynamic Programming - O(n²) time, O(n²) space
3. Manacher's Algorithm - O(n) time, O(n) space - advanced

Time: O(n²) for basic approaches, O(n) for Manacher's
Space: O(1) to O(n²) depending on approach
"""

def countSubstrings(s):
    """
    RECOMMENDED SOLUTION: Expand Around Centers approach.
    
    Key insight: Every palindrome has a center. For string of length n:
    - n possible centers for odd-length palindromes (single character)
    - n-1 possible centers for even-length palindromes (between characters)
    - Total: 2n-1 possible centers
    
    For each center, expand outward while characters match.
    
    Time: O(n²) - n centers, each can expand up to n/2
    Space: O(1) - only using constant extra space
    
    Args:
        s: str - input string
    
    Returns:
        int - count of palindromic substrings
    """
    if not s:
        return 0
    
    count = 0
    n = len(s)
    
    def expand_around_center(left, right):
        """Helper to count palindromes with given center"""
        palindrome_count = 0
        
        # Expand while characters match and indices are valid
        while left >= 0 and right < n and s[left] == s[right]:
            palindrome_count += 1
            left -= 1
            right += 1
        
        return palindrome_count
    
    # Check all possible centers
    for i in range(n):
        # Odd length palindromes (center at i)
        count += expand_around_center(i, i)
        
        # Even length palindromes (center between i and i+1)
        count += expand_around_center(i, i + 1)
    
    return count


def countSubstrings_dp(s):
    """
    Dynamic Programming approach.
    
    dp[i][j] = True if substring s[i:j+1] is palindrome
    
    Recurrence:
    - dp[i][j] = True if s[i] == s[j] AND (j-i <= 2 OR dp[i+1][j-1])
    
    Advantage: Can easily be extended to return actual palindromes
    Disadvantage: O(n²) space complexity
    
    Time: O(n²), Space: O(n²)
    """
    if not s:
        return 0
    
    n = len(s)
    # dp[i][j] = True if s[i:j+1] is palindrome
    dp = [[False] * n for _ in range(n)]
    count = 0
    
    # Fill DP table
    # Process by substring length
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                # Characters match
                if length <= 2:
                    # Single char or two matching chars
                    dp[i][j] = True
                else:
                    # Check inner substring
                    dp[i][j] = dp[i + 1][j - 1]
            else:
                # Characters don't match
                dp[i][j] = False
            
            if dp[i][j]:
                count += 1
    
    return count


def countSubstrings_brute_force(s):
    """
    Brute force approach - check every possible substring.
    
    Good for initial understanding and small test cases.
    NOT recommended for interview unless as starting point.
    
    Time: O(n³), Space: O(1)
    """
    if not s:
        return 0
    
    def is_palindrome(substr):
        return substr == substr[::-1]
    
    count = 0
    n = len(s)
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i, n):
            if is_palindrome(s[i:j+1]):
                count += 1
    
    return count


def countSubstrings_manacher(s):
    """
    Manacher's Algorithm - O(n) solution for advanced discussion.
    
    This is optimal but quite complex. Mention only if specifically asked
    about O(n) solution or if you have extra time.
    
    The algorithm uses previously computed information to avoid redundant work.
    """
    if not s:
        return 0
    
    # Transform string to handle even-length palindromes
    # "abc" -> "#a#b#c#"
    transformed = '#'.join('^{}$'.format(s))
    n = len(transformed)
    
    # Array to store radius of palindrome at each center
    P = [0] * n
    center = right = 0  # rightmost palindrome's center and right boundary
    
    for i in range(1, n - 1):
        # Mirror of i with respect to center
        mirror = 2 * center - i
        
        # If i is within right boundary, use previously computed info
        if i < right:
            P[i] = min(right - i, P[mirror])
        
        # Try to expand palindrome centered at i
        try:
            while transformed[i + P[i] + 1] == transformed[i - P[i] - 1]:
                P[i] += 1
        except IndexError:
            pass
        
        # If palindrome centered at i extends past right, update center and right
        if i + P[i] > right:
            center, right = i, i + P[i]
    
    # Count palindromes
    # Each P[i] represents radius, so number of palindromes = (P[i] + 1) // 2
    return sum((p + 1) // 2 for p in P)


def countSubstrings_with_list(s):
    """
    Enhanced version that returns both count and list of palindromic substrings.
    
    Useful for follow-up questions asking for the actual palindromes.
    Based on expand around centers approach.
    """
    if not s:
        return 0, []
    
    palindromes = []
    n = len(s)
    
    def expand_and_collect(left, right):
        """Expand and collect all palindromes with given center"""
        collected = []
        
        while left >= 0 and right < n and s[left] == s[right]:
            collected.append(s[left:right+1])
            left -= 1
            right += 1
        
        return collected
    
    # Check all possible centers
    for i in range(n):
        # Odd length palindromes
        palindromes.extend(expand_and_collect(i, i))
        
        # Even length palindromes  
        palindromes.extend(expand_and_collect(i, i + 1))
    
    return len(palindromes), palindromes


def countSubstrings_iterative_optimized(s):
    """
    Slightly optimized version of expand around centers.
    
    Combines odd and even length palindrome checking in single loop.
    Good for showing optimization thinking.
    """
    if not s:
        return 0
    
    count = 0
    n = len(s)
    
    for center in range(2 * n - 1):  # 2n-1 possible centers
        # Convert center index to left and right pointers
        left = center // 2
        right = left + center % 2
        
        # Expand around center
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    return count


# Test cases and comprehensive analysis
def test_solution():
    """Test all solutions with comprehensive examples."""
    
    test_cases = [
        ("abc", 3),          # basic case
        ("aaa", 6),          # repeated characters
        ("", 0),             # empty string
        ("a", 1),            # single character
        ("aa", 3),           # two same chars
        ("ab", 2),           # two different chars
        ("racecar", 10),     # classic palindrome
        ("abccba", 9),       # even-length palindrome
        ("abcdef", 6),       # no multi-char palindromes
        ("aaaa", 10),        # all same characters
        ("abacabad", 12)     # mixed case
    ]
    
    solutions = [
        ("Expand Around Centers (Recommended)", countSubstrings),
        ("Dynamic Programming", countSubstrings_dp),
        ("Brute Force", countSubstrings_brute_force),
        ("Iterative Optimized", countSubstrings_iterative_optimized),
        ("Manacher's Algorithm", countSubstrings_manacher)
    ]
    
    print("Testing all solutions:")
    for name, func in solutions:
        print(f"\n{name}:")
        for s, expected in test_cases:
            try:
                result = func(s)
                status = "✓" if result == expected else "✗"
                print(f"  {status} '{s}' → Expected: {expected}, Got: {result}")
            except Exception as e:
                print(f"  ✗ '{s}' → Error: {e}")
    
    print("\n" + "="*70)
    print("Testing palindrome collection:")
    collection_cases = ["abc", "aaa", "racecar", "abccba"]
    
    for s in collection_cases:
        count, palindromes = countSubstrings_with_list(s)
        print(f"'{s}' → Count: {count}")
        print(f"  Palindromes: {palindromes}")


def trace_example(s):
    """Step-by-step trace of expand around centers algorithm."""
    print(f"Tracing expand around centers for s = '{s}'")
    
    n = len(s)
    total_count = 0
    
    print(f"String length: {n}")
    print(f"Possible centers: {2*n-1} (odd: {n}, even: {n-1})")
    print()
    
    def expand_and_trace(left, right, center_type, center_pos):
        count = 0
        expansions = []
        
        original_left, original_right = left, right
        
        while left >= 0 and right < n and s[left] == s[right]:
            palindrome = s[left:right+1]
            expansions.append(f"s[{left}:{right+1}] = '{palindrome}'")
            count += 1
            left -= 1
            right += 1
        
        if expansions:
            print(f"{center_type} center at {center_pos}: found {count} palindrome(s)")
            for expansion in expansions:
                print(f"  {expansion}")
        else:
            print(f"{center_type} center at {center_pos}: no palindromes")
        
        return count
    
    # Check all centers
    for i in range(n):
        # Odd length palindromes
        count = expand_and_trace(i, i, "Odd", f"position {i} ('{s[i]}')")
        total_count += count
        
        # Even length palindromes
        if i < n - 1:
            count = expand_and_trace(i, i + 1, "Even", f"between {i} and {i+1}")
            total_count += count
        
        print()
    
    print(f"Total palindromic substrings: {total_count}")


def analyze_approaches():
    """Comprehensive analysis of different solution approaches."""
    
    analysis = """
    APPROACH COMPARISON FOR PALINDROMIC SUBSTRINGS:

    1. Expand Around Centers (RECOMMENDED FOR INTERVIEWS):
       ✓ Optimal O(n²) time with O(1) space
       ✓ Intuitive and easy to explain
       ✓ No complex data structures needed
       ✓ Easy to trace and debug
       ✓ Can be easily modified to collect actual palindromes
       ⚠ Still O(n²) in worst case

    2. Dynamic Programming:
       ✓ Clear recurrence relation
       ✓ Easy to extend for related problems
       ✓ Can store results for reuse
       ✗ O(n²) space complexity
       ⚠ More complex implementation

    3. Brute Force:
       ✓ Most straightforward approach
       ✓ Good for initial understanding
       ✗ O(n³) time complexity - too slow
       ✗ Not acceptable for interviews

    4. Manacher's Algorithm:
       ✓ Optimal O(n) time complexity
       ✓ Shows advanced algorithm knowledge
       ✗ Very complex implementation
       ✗ Easy to make mistakes under pressure
       ⚠ Overkill for most interviews

    INTERVIEW STRATEGY:
    1. Start with problem understanding and examples
    2. Mention brute force briefly (but don't implement)
    3. Choose expand around centers as main solution
    4. Implement clean, readable code
    5. Trace through an example
    6. Discuss optimizations (Manacher's) if asked
    7. Handle edge cases properly

    WHY EXPAND AROUND CENTERS IS BEST FOR INTERVIEWS:
    - Balance of efficiency and simplicity
    - Demonstrates key insight about palindrome centers
    - Easy to verify correctness
    - Minimal chance of implementation bugs
    - Shows good algorithmic intuition

    COMMON INTERVIEW FOLLOW-UPS:
    - "Can you return the actual palindromes?" → modify to collect
    - "Can you do better than O(n²)?" → mention Manacher's
    - "What about space optimization?" → already O(1)
    - "Handle edge cases" → empty string, single char
    """
    
    print(analysis)


def demonstrate_center_concept():
    """Visualize the center concept with examples."""
    
    examples = ["abc", "racecar", "abccba"]
    
    print("UNDERSTANDING PALINDROME CENTERS:")
    print("=" * 40)
    
    for s in examples:
        print(f"\nString: '{s}' (length {len(s)})")
        
        n = len(s)
        print(f"Centers: {2*n-1} total")
        
        # Show odd centers
        print("Odd-length centers (at characters):")
        for i in range(n):
            print(f"  Position {i}: '{s[i]}'")
        
        # Show even centers
        print("Even-length centers (between characters):")
        for i in range(n-1):
            print(f"  Between {i} and {i+1}: '{s[i]}|{s[i+1]}'")
        
        # Count palindromes
        count = countSubstrings(s)
        print(f"Total palindromic substrings: {count}")
        
        # Show actual palindromes
        _, palindromes = countSubstrings_with_list(s)
        print(f"Palindromes: {palindromes}")


def performance_comparison():
    """Compare performance characteristics of different approaches."""
    
    comparison = """
    PERFORMANCE CHARACTERISTICS:

    Time Complexity:
    - Brute Force: O(n³) - check all O(n²) substrings, each takes O(n)
    - Expand Around Centers: O(n²) - n centers, each expands up to n/2
    - Dynamic Programming: O(n²) - fill n×n table, each cell O(1)
    - Manacher's: O(n) - linear pass with amortized constant work per position

    Space Complexity:
    - Brute Force: O(1) - only using temporary variables
    - Expand Around Centers: O(1) - only counters and pointers
    - Dynamic Programming: O(n²) - full n×n boolean table
    - Manacher's: O(n) - transformed string and radius array

    Practical Considerations:
    - For n ≤ 1000: All approaches except brute force work fine
    - For n ≤ 10000: Expand around centers preferred (simplicity + speed)
    - For n > 50000: Consider Manacher's if time is critical

    Interview Preference Ranking:
    1. Expand Around Centers - best balance of efficiency and clarity
    2. Dynamic Programming - good if you need to extend the problem
    3. Manacher's - only if specifically asked for O(n) solution
    4. Brute Force - only mention, don't implement
    """
    
    print(comparison)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70)
    trace_example("abccba")
    print("\n" + "="*70)
    demonstrate_center_concept()
    print("\n" + "="*70)
    analyze_approaches()
    print("\n" + "="*70)
    performance_comparison()
