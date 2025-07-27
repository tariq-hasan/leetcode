"""
LeetCode 17: Letter Combinations of a Phone Number

Problem: Given a string containing digits from 2-9 inclusive, return all possible 
letter combinations that the number could represent. Return the answer in any order.

Phone keypad mapping:
2: abc, 3: def, 4: ghi, 5: jkl, 6: mno, 7: pqrs, 8: tuv, 9: wxyz

Key Insight: This is a classic backtracking problem where we build combinations
character by character, exploring all possibilities.

Time Complexity: O(3^N × 4^M) where N is digits with 3 letters, M is digits with 4 letters
Space Complexity: O(3^N × 4^M) for result storage + O(N) for recursion stack
"""

class Solution:
    def letterCombinations(self, digits):
        """
        Backtracking Solution - Most intuitive and popular for interviews
        """
        if not digits:
            return []
        
        # Phone keypad mapping
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        result = []
        
        def backtrack(index, current_combination):
            # Base case: built complete combination
            if index == len(digits):
                result.append(current_combination)
                return
            
            # Get current digit and its corresponding letters
            digit = digits[index]
            letters = phone_map[digit]
            
            # Try each letter for current digit
            for letter in letters:
                # Choose: add letter to current combination
                backtrack(index + 1, current_combination + letter)
                # Unchoose: implicit (no explicit removal needed)
        
        backtrack(0, "")
        return result

    def letterCombinationsIterative(self, digits):
        """
        Iterative Solution using BFS approach
        Good alternative to show different thinking
        """
        if not digits:
            return []
        
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        from collections import deque
        queue = deque([''])
        
        for digit in digits:
            letters = phone_map[digit]
            queue_size = len(queue)
            
            # Process all current combinations
            for _ in range(queue_size):
                combination = queue.popleft()
                
                # Add each possible letter
                for letter in letters:
                    queue.append(combination + letter)
        
        return list(queue)

    def letterCombinationsOptimized(self, digits):
        """
        Optimized backtracking with list manipulation for better performance
        """
        if not digits:
            return []
        
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        result = []
        current = [''] * len(digits)  # Pre-allocate for efficiency
        
        def backtrack(index):
            if index == len(digits):
                result.append(''.join(current))
                return
            
            digit = digits[index]
            for letter in phone_map[digit]:
                current[index] = letter  # Choose
                backtrack(index + 1)
                # No explicit unchoose needed (will be overwritten)
        
        backtrack(0)
        return result

    def letterCombinationsCartesianProduct(self, digits):
        """
        Using itertools.product for Cartesian product approach
        Elegant but might not be allowed in interviews
        """
        if not digits:
            return []
        
        import itertools
        
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        # Get all letter groups
        letter_groups = [phone_map[digit] for digit in digits]
        
        # Generate Cartesian product
        combinations = itertools.product(*letter_groups)
        
        # Convert tuples to strings
        return [''.join(combo) for combo in combinations]

    def letterCombinationsDFS(self, digits):
        """
        DFS with explicit path tracking (alternative backtracking style)
        """
        if not digits:
            return []
        
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        def dfs(index, path, result):
            # Base case
            if index == len(digits):
                result.append(path)
                return
            
            # Explore all possibilities for current digit
            digit = digits[index]
            for letter in phone_map[digit]:
                dfs(index + 1, path + letter, result)
        
        result = []
        dfs(0, "", result)
        return result

    def letterCombinationsGenerative(self, digits):
        """
        Generator approach - memory efficient for large results
        Good for follow-up discussion about memory optimization
        """
        if not digits:
            return []
        
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        def generate_combinations():
            def backtrack(index, current):
                if index == len(digits):
                    yield current
                    return
                
                digit = digits[index]
                for letter in phone_map[digit]:
                    yield from backtrack(index + 1, current + letter)
            
            yield from backtrack(0, "")
        
        return list(generate_combinations())


# Test cases for interview
def test_letter_combinations():
    solution = Solution()
    
    # Test case 1: Standard case
    digits1 = "23"
    result1 = solution.letterCombinations(digits1)
    print(f"Test 1 ('{digits1}'): {result1}")
    # Expected: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    
    # Test case 2: Single digit
    digits2 = "2"
    result2 = solution.letterCombinations(digits2)
    print(f"Test 2 ('{digits2}'): {result2}")
    # Expected: ["a","b","c"]
    
    # Test case 3: Empty string
    digits3 = ""
    result3 = solution.letterCombinations(digits3)
    print(f"Test 3 ('{digits3}'): {result3}")
    # Expected: []
    
    # Test case 4: Digit with 4 letters (7 or 9)
    digits4 = "79"
    result4 = solution.letterCombinations(digits4)
    print(f"Test 4 ('{digits4}'): {result4[:8]}...")  # Show first 8
    # Expected: 4 * 4 = 16 combinations total
    
    # Test case 5: Longer input
    digits5 = "234"
    result5 = solution.letterCombinations(digits5)
    print(f"Test 5 ('{digits5}'): {len(result5)} combinations")
    # Expected: 3 * 3 * 3 = 27 combinations

if __name__ == "__main__":
    test_letter_combinations()


"""
Key Interview Points to Discuss:

1. PROBLEM UNDERSTANDING:
   - Generate all possible combinations from phone keypad mapping
   - Each digit maps to 3-4 letters
   - Order of combinations doesn't matter
   - Classic combinatorial problem

2. BACKTRACKING APPROACH:
   - Build combinations character by character
   - At each step, try all possible letters for current digit
   - When reach end of digits, add combination to result
   - Implicit backtracking (no explicit removal needed)

3. ALGORITHM STEPS:
   - Base case: when index equals digits length, add combination
   - For each digit, try all its corresponding letters
   - Recursively build rest of combination
   - Backtrack naturally through recursion unwinding

4. WHY BACKTRACKING WORKS:
   - Systematic exploration of all possibilities
   - Builds solution incrementally
   - Naturally handles variable number of choices per digit
   - Efficient - no redundant work

5. EDGE CASES TO MENTION:
   - Empty input string
   - Single digit
   - Digits with different letter counts (2-4 letters)
   - No invalid digits (problem guarantees 2-9)

6. TIME/SPACE COMPLEXITY:
   - Time: O(3^N × 4^M) where N = digits with 3 letters, M = digits with 4 letters
   - Space: O(3^N × 4^M) for result + O(N) recursion stack
   - In worst case: O(4^N) if all digits are 7 or 9

7. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you solve iteratively?" -> BFS approach
   - "Memory constraints?" -> Generator approach
   - "What if keypad mapping changes?" -> Make mapping parameter
   - "Can you optimize?" -> Pre-allocate arrays, avoid string concatenation
   - "Handle invalid digits?" -> Add validation

8. ALTERNATIVE APPROACHES:
   - Iterative BFS: Build level by level
   - Cartesian product: Using itertools (if allowed)
   - DFS with explicit stack: Non-recursive version

9. OPTIMIZATION OPPORTUNITIES:
   - Use list instead of string concatenation
   - Pre-allocate result size if known
   - Generator for memory efficiency
   - Iterative to avoid recursion overhead

10. REAL-WORLD APPLICATIONS:
    - T9 predictive text
    - Password generation
    - Code generation
    - Combinatorial testing

11. BACKTRACKING TEMPLATE:
    ```
    def backtrack(index, current_state):
        if base_case:
            process_solution(current_state)
            return
        
        for choice in get_choices(index):
            make_choice(choice)
            backtrack(index + 1, new_state)
            unmake_choice(choice)  # if needed
    ```

12. COMPARISON WITH SIMILAR PROBLEMS:
    - Permutations: Fixed elements, different orders
    - Combinations: Choose subset, order doesn't matter
    - This problem: Cartesian product of character sets

13. INTERVIEW TIPS:
    - Start with simple example (e.g., "23")
    - Draw recursion tree to visualize
    - Mention time complexity upfront
    - Code cleanly with good variable names
    - Test with edge cases
"""
