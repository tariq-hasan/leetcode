"""
LeetCode 784. Letter Case Permutation

Problem: Given a string s, you can transform every letter individually to be 
lowercase or uppercase to create another string. Return a list of all possible 
strings we can create. Return the output in any order.

Key Insights:
1. Only letters can be transformed, digits remain unchanged
2. Each letter has exactly 2 choices: lowercase or uppercase
3. If there are k letters, there are 2^k total permutations
4. This is a classic backtracking problem with binary choices

Time Complexity: O(2^k * n) where k = number of letters, n = string length
Space Complexity: O(2^k * n) for storing all permutations + O(n) recursion depth
"""

# Approach 1: Backtracking (Most Common & Recommended)
def letterCasePermutation_v1(s):
    """
    Standard backtracking approach - make choice for each letter
    """
    result = []
    
    def backtrack(index, current):
        # Base case: processed all characters
        if index == len(s):
            result.append(current)
            return
        
        char = s[index]
        
        if char.isalpha():
            # Choice 1: lowercase
            backtrack(index + 1, current + char.lower())
            
            # Choice 2: uppercase
            backtrack(index + 1, current + char.upper())
        else:
            # Digit: no choice, just add as-is
            backtrack(index + 1, current + char)
    
    backtrack(0, "")
    return result

# Approach 2: Iterative Building (Alternative)
def letterCasePermutation_v2(s):
    """
    Build permutations iteratively by processing each character
    """
    result = [""]  # Start with empty string
    
    for char in s:
        if char.isalpha():
            # For each existing permutation, create two versions
            new_result = []
            for perm in result:
                new_result.append(perm + char.lower())
                new_result.append(perm + char.upper())
            result = new_result
        else:
            # Digit: just append to all existing permutations
            result = [perm + char for perm in result]
    
    return result

# Approach 3: Bitmask Enumeration (Advanced)
def letterCasePermutation_v3(s):
    """
    Use bitmask to represent all possible case combinations
    Advanced approach showing bit manipulation thinking
    """
    # Find all letter positions
    letter_positions = []
    for i, char in enumerate(s):
        if char.isalpha():
            letter_positions.append(i)
    
    result = []
    num_letters = len(letter_positions)
    
    # Generate all 2^k combinations using bitmask
    for mask in range(1 << num_letters):
        chars = list(s.lower())  # Start with all lowercase
        
        # Apply uppercase based on bitmask
        for bit_pos in range(num_letters):
            if mask & (1 << bit_pos):
                chars[letter_positions[bit_pos]] = chars[letter_positions[bit_pos]].upper()
        
        result.append(''.join(chars))
    
    return result

# Approach 4: Functional/Recursive (Clean Implementation)
def letterCasePermutation_v4(s):
    """
    Clean recursive implementation without explicit backtracking
    """
    if not s:
        return [""]
    
    # Get permutations for the rest of the string
    rest_permutations = letterCasePermutation_v4(s[1:])
    
    first_char = s[0]
    result = []
    
    if first_char.isalpha():
        # Add both cases for each rest permutation
        for perm in rest_permutations:
            result.append(first_char.lower() + perm)
            result.append(first_char.upper() + perm)
    else:
        # Just add digit to each rest permutation
        for perm in rest_permutations:
            result.append(first_char + perm)
    
    return result

# Approach 5: Generator Version (Memory Efficient)
def letterCasePermutation_generator(s):
    """
    Generator version for memory efficiency - useful for large inputs
    """
    def backtrack(index, current):
        if index == len(s):
            yield current
            return
        
        char = s[index]
        
        if char.isalpha():
            yield from backtrack(index + 1, current + char.lower())
            yield from backtrack(index + 1, current + char.upper())
        else:
            yield from backtrack(index + 1, current + char)
    
    return list(backtrack(0, ""))

# Detailed explanation version for interviews
def letterCasePermutation_explained(s):
    """
    Version with detailed logging for interview explanation
    """
    result = []
    
    def backtrack(index, current, depth=0):
        indent = "  " * depth
        print(f"{indent}Processing index {index}, current = '{current}'")
        
        if index == len(s):
            print(f"{indent}✓ Complete permutation: '{current}'")
            result.append(current)
            return
        
        char = s[index]
        print(f"{indent}Character: '{char}'")
        
        if char.isalpha():
            print(f"{indent}Letter found - trying both cases:")
            
            # Lowercase choice
            print(f"{indent}  Choice 1: lowercase '{char.lower()}'")
            backtrack(index + 1, current + char.lower(), depth + 1)
            
            # Uppercase choice
            print(f"{indent}  Choice 2: uppercase '{char.upper()}'")
            backtrack(index + 1, current + char.upper(), depth + 1)
        else:
            print(f"{indent}Digit found - no choice, adding '{char}'")
            backtrack(index + 1, current + char, depth + 1)
        
        print(f"{indent}Finished processing index {index}")
    
    backtrack(0, "")
    return result

def count_expected_permutations(s):
    """Calculate expected number of permutations without generating them"""
    letter_count = sum(1 for char in s if char.isalpha())
    return 2 ** letter_count

def analyze_string_structure(s):
    """Analyze the input string for interview discussion"""
    print(f"\n=== String Analysis: '{s}' ===")
    
    letters = []
    digits = []
    
    for i, char in enumerate(s):
        if char.isalpha():
            letters.append((i, char))
        else:
            digits.append((i, char))
    
    print(f"Length: {len(s)}")
    print(f"Letters: {len(letters)} at positions {[pos for pos, _ in letters]}")
    print(f"Digits: {len(digits)} at positions {[pos for pos, _ in digits]}")
    print(f"Expected permutations: 2^{len(letters)} = {2**len(letters)}")

def test_letter_case_permutation():
    """Test all approaches with various inputs"""
    test_cases = [
        "a1b2",      # Basic case
        "3z4",       # Single letter
        "12345",     # No letters
        "abc",       # All letters
        "a1B2c3D",   # Mixed case input
        "",          # Empty string
        "1",         # Single digit
        "A"          # Single letter
    ]
    
    for s in test_cases:
        print(f"\n=== Testing: '{s}' ===")
        
        # Test different approaches
        result1 = letterCasePermutation_v1(s)
        result2 = letterCasePermutation_v2(s)
        result3 = letterCasePermutation_v3(s)
        result4 = letterCasePermutation_v4(s)
        result5 = letterCasePermutation_generator(s)
        
        # Sort results for comparison (order doesn't matter)
        results = [sorted(result1), sorted(result2), sorted(result3), 
                  sorted(result4), sorted(result5)]
        
        print(f"Backtracking: {len(result1)} permutations")
        print(f"Iterative: {len(result2)} permutations")
        print(f"Bitmask: {len(result3)} permutations")
        print(f"Recursive: {len(result4)} permutations")
        print(f"Generator: {len(result5)} permutations")
        
        # Verify all approaches give same results
        assert all(r == results[0] for r in results), f"Results don't match for '{s}'"
        
        # Show actual permutations for small inputs
        if len(result1) <= 8:
            print(f"All permutations: {sorted(result1)}")
        
        # Verify expected count
        expected = count_expected_permutations(s)
        assert len(result1) == expected, f"Expected {expected}, got {len(result1)}"
        
        analyze_string_structure(s)

def demonstrate_decision_tree(s):
    """Show the decision tree for interview explanation"""
    if len([c for c in s if c.isalpha()]) > 3:
        print(f"Decision tree too large for '{s}' (too many letters)")
        return
    
    print(f"\n=== Decision Tree for '{s}' ===")
    
    def print_tree(index, current, choices, depth=0):
        indent = "  " * depth
        
        if index == len(s):
            print(f"{indent}→ '{current}' {choices}")
            return
        
        char = s[index]
        
        if char.isalpha():
            print(f"{indent}Pos {index}: '{char}' (letter)")
            print_tree(index + 1, current + char.lower(), choices + [f"{char}→{char.lower()}"], depth + 1)
            print_tree(index + 1, current + char.upper(), choices + [f"{char}→{char.upper()}"], depth + 1)
        else:
            print(f"{indent}Pos {index}: '{char}' (digit)")
            print_tree(index + 1, current + char, choices + [f"{char}→{char}"], depth + 1)
    
    print_tree(0, "", [])

if __name__ == "__main__":
    print("=== Letter Case Permutation Solutions ===")
    test_letter_case_permutation()
    
    print("\n=== Detailed Walkthrough for 'a1B' ===")
    result = letterCasePermutation_explained("a1B")
    print(f"Final result: {result}")
    
    print("\n=== Decision Tree Examples ===")
    demonstrate_decision_tree("a1B")
    demonstrate_decision_tree("ab")

"""
Critical Interview Discussion Points:

1. **Problem Understanding**:
   - Only letters can be transformed (uppercase/lowercase)
   - Digits remain unchanged
   - Each letter has exactly 2 choices
   - Order doesn't matter in the output

2. **Key Insight - Binary Decision Tree**:
   - For each letter: binary choice (upper/lower)
   - k letters → 2^k total permutations
   - This naturally maps to backtracking

3. **Algorithm Choice**:
   - Backtracking: Most intuitive, explores decision tree
   - Iterative: Builds permutations step by step
   - Bitmask: Advanced approach using bit manipulation
   - All have same complexity but different perspectives

4. **Why Backtracking Works Well**:
   - Clear binary choices at each step
   - No need for complex constraint checking
   - Natural pruning (though not needed here)
   - Easy to implement and understand

5. **Complexity Analysis**:
   - Time: O(2^k * n) where k = letters, n = string length
   - Space: O(2^k * n) for storing results + O(n) recursion
   - Can't do better than O(2^k) since that's output size

6. **Implementation Considerations**:
   - String manipulation vs character array
   - Recursive vs iterative approach
   - Memory usage for large inputs (generator pattern)

7. **Edge Cases**:
   - Empty string → [""]
   - No letters (all digits) → [original string]
   - All letters → 2^n permutations
   - Mixed case input (should work the same)

8. **Follow-up Questions**:
   - What if we only want permutations with specific patterns?
   - How would you modify for other transformations?
   - Can we generate the kth permutation without generating all?
   - Memory optimization for very large inputs?

9. **Alternative Approaches**:
   - Bitmask enumeration (shows bit manipulation skills)
   - Functional/recursive style (clean implementation)
   - Generator pattern (memory efficient)

10. **Why This Problem is Good for Interviews**:
    - Tests backtracking fundamentals
    - Has multiple valid approaches
    - Clear complexity analysis
    - Easy to extend with follow-ups
    - Not too complex but shows algorithmic thinking
"""
