"""
LeetCode 678: Valid Parenthesis String

Problem: Given a string s containing only three types of characters: '(', ')' and '*', 
return true if s is a valid parenthesis string.

The '*' can be treated as:
1. A single right parenthesis ')'
2. A single left parenthesis '('  
3. An empty string ""

Time Complexity: O(n)
Space Complexity: O(1) for greedy, O(n²) for DP
"""

class Solution:
    def checkValidString(self, s: str) -> bool:
        """
        OPTIMAL GREEDY SOLUTION - Most efficient for interviews
        
        Key insight: Track the range of possible open parentheses count
        - min_open: minimum possible open parentheses (treat * as ')' or empty)
        - max_open: maximum possible open parentheses (treat * as '(')
        
        Time: O(n), Space: O(1)
        """
        min_open = 0  # Min possible open parens
        max_open = 0  # Max possible open parens
        
        for char in s:
            if char == '(':
                min_open += 1
                max_open += 1
            elif char == ')':
                min_open -= 1
                max_open -= 1
            else:  # char == '*'
                min_open -= 1  # Treat as ')' or empty
                max_open += 1  # Treat as '('
            
            # If max_open < 0, too many ')' - impossible to balance
            if max_open < 0:
                return False
            
            # min_open can't be negative (we have enough '*' to balance)
            min_open = max(min_open, 0)
        
        # Valid if we can have exactly 0 open parens
        return min_open <= 0 <= max_open

    def checkValidStringDP(self, s: str) -> bool:
        """
        DYNAMIC PROGRAMMING SOLUTION - Good for explaining approach
        
        dp[i][j] = True if s[0:i] can have exactly j open parentheses
        
        Time: O(n²), Space: O(n²)
        """
        n = len(s)
        # dp[i][j] = can s[0:i] result in exactly j open parens?
        dp = [[False] * n for _ in range(n + 1)]
        dp[0][0] = True  # Empty string has 0 open parens
        
        for i in range(1, n + 1):
            for j in range(i + 1):  # Can't have more open than characters
                char = s[i - 1]
                
                if char == '(':
                    if j > 0:
                        dp[i][j] = dp[i - 1][j - 1]
                elif char == ')':
                    if j < i:
                        dp[i][j] = dp[i - 1][j + 1]
                else:  # char == '*'
                    # Try all three possibilities
                    dp[i][j] = dp[i - 1][j]  # Empty string
                    if j > 0:
                        dp[i][j] |= dp[i - 1][j - 1]  # '('
                    if j < i:
                        dp[i][j] |= dp[i - 1][j + 1]  # ')'
        
        return dp[n][0]

    def checkValidStringStack(self, s: str) -> bool:
        """
        TWO-STACK SOLUTION - Alternative approach
        
        Use two stacks to track indices of '(' and '*'
        Try to match ')' with '(' first, then with '*'
        
        Time: O(n), Space: O(n)
        """
        open_stack = []  # Indices of '('
        star_stack = []  # Indices of '*'
        
        # First pass: match ')' with '(' or '*'
        for i, char in enumerate(s):
            if char == '(':
                open_stack.append(i)
            elif char == '*':
                star_stack.append(i)
            else:  # char == ')'
                if open_stack:
                    open_stack.pop()
                elif star_stack:
                    star_stack.pop()
                else:
                    return False
        
        # Second pass: match remaining '(' with '*' (star must come after '(')
        while open_stack and star_stack:
            if open_stack[-1] < star_stack[-1]:
                open_stack.pop()
                star_stack.pop()
            else:
                break
        
        return len(open_stack) == 0


# Test cases for interview
def test_solution():
    sol = Solution()
    
    test_cases = [
        ("()", True),           # Basic valid
        ("(*)", True),          # Star as ')'
        ("(*))", True),         # Star as empty
        ("(((*)", True),        # Star as ')'
        ")*(", False),          # Invalid order
        ("*)", True),           # Star as '('
        ("(((", False),         # Too many open
        ("(()", False),         # One unclosed
        ("***", True),          # All stars (can be empty)
        ("(*))", True),         # Mixed case
        ("(*()))", False),      # Extra closing
    ]
    
    print("Testing Greedy Solution:")
    for s, expected in test_cases:
        result = sol.checkValidString(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{s}' -> {result} (expected {expected})")

if __name__ == "__main__":
    test_solution()


"""
INTERVIEW TALKING POINTS:

1. APPROACH EXPLANATION:
   - Greedy is optimal: track min/max possible open parentheses
   - Key insight: '*' gives us flexibility - use range tracking
   
2. EDGE CASES TO MENTION:
   - Empty string (valid)
   - All stars (valid - can all be empty)
   - Stars before '(' (need careful handling)

3. COMPLEXITY ANALYSIS:
   - Greedy: O(n) time, O(1) space - best solution
   - DP: O(n²) time/space - good for explanation
   - Stack: O(n) time/space - intuitive alternative

4. WHY GREEDY WORKS:
   - We only care if final count can be 0
   - Track range [min_open, max_open] of possibilities
   - If range ever goes negative, impossible
   - If 0 is in final range, valid

5. FOLLOW-UP QUESTIONS:
   - What if we needed the actual valid assignment of '*'?
   - What if we had more wildcard characters?
   - How to modify for different bracket types?
"""
