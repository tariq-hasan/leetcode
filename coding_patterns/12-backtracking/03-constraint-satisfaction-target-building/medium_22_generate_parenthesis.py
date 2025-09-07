"""
LeetCode 22: Generate Parentheses

Problem: Given n pairs of parentheses, write a function to generate all combinations 
of well-formed parentheses.

Example 1:
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
Input: n = 1
Output: ["()"]

Example 3:
Input: n = 0
Output: [""]

KEY INSIGHTS:
1. This is a classic backtracking/recursion problem
2. Valid parentheses rules: 
   - Never have more ')' than '(' at any point
   - Use exactly n '(' and n ')'
3. Multiple approaches: Backtracking, DP, BFS - backtracking is most intuitive

Time: O(4^n / sqrt(n)) - Catalan number growth
Space: O(4^n / sqrt(n)) for output + O(n) recursion stack
"""

def generateParenthesis(n):
    """
    RECOMMENDED SOLUTION: Backtracking approach.
    
    This is the most intuitive and commonly expected solution in interviews.
    
    Key constraints for valid parentheses:
    1. At any point, count of ')' should not exceed count of '('
    2. Total '(' should not exceed n
    3. Total ')' should not exceed n
    
    Args:
        n: int - number of pairs of parentheses
    
    Returns:
        List[str] - all valid combinations
    """
    result = []
    
    def backtrack(current, open_count, close_count):
        # Base case: we've used all n pairs
        if len(current) == 2 * n:
            result.append(current)
            return
        
        # Add opening parenthesis if we haven't used all n
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)
        
        # Add closing parenthesis if it won't violate the constraint
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result


def generateParenthesis_optimized_params(n):
    """
    Slightly optimized version with cleaner parameter passing.
    
    Instead of tracking counts, we track remaining parentheses to place.
    Some find this more intuitive.
    """
    result = []
    
    def backtrack(current, left_remaining, right_remaining):
        # Base case: no more parentheses to place
        if left_remaining == 0 and right_remaining == 0:
            result.append(current)
            return
        
        # Add '(' if we have any left to place
        if left_remaining > 0:
            backtrack(current + "(", left_remaining - 1, right_remaining)
        
        # Add ')' if we have more right than left (to maintain balance)
        if right_remaining > left_remaining:
            backtrack(current + ")", left_remaining, right_remaining - 1)
    
    backtrack("", n, n)
    return result


def generateParenthesis_iterative_bfs(n):
    """
    Iterative BFS approach using queue.
    
    Good to mention as alternative to recursion. Demonstrates understanding
    of how recursion can be converted to iteration.
    
    Time: Same as recursive, Space: O(width of tree) instead of O(depth)
    """
    if n == 0:
        return [""]
    
    from collections import deque
    
    # Queue stores (current_string, open_count, close_count)
    queue = deque([("", 0, 0)])
    result = []
    
    while queue:
        current, open_count, close_count = queue.popleft()
        
        # If we've built a complete string
        if len(current) == 2 * n:
            result.append(current)
            continue
        
        # Add opening parenthesis if possible
        if open_count < n:
            queue.append((current + "(", open_count + 1, close_count))
        
        # Add closing parenthesis if possible
        if close_count < open_count:
            queue.append((current + ")", open_count, close_count + 1))
    
    return result


def generateParenthesis_dp(n):
    """
    Dynamic Programming approach.
    
    Based on the insight that valid parentheses can be constructed as:
    "(" + {valid parentheses with i pairs} + ")" + {valid parentheses with n-1-i pairs}
    
    This gives the recurrence relation for Catalan numbers.
    More complex but shows DP thinking.
    """
    if n == 0:
        return [""]
    
    # dp[i] = all valid parentheses combinations with i pairs
    dp = [[] for _ in range(n + 1)]
    dp[0] = [""]
    
    for i in range(1, n + 1):
        for j in range(i):
            # For each way to split i pairs: j pairs inside first (), (i-1-j) pairs after
            for left in dp[j]:
                for right in dp[i - 1 - j]:
                    dp[i].append("(" + left + ")" + right)
    
    return dp[n]


def generateParenthesis_with_validation(n):
    """
    Enhanced version that includes validation of generated parentheses.
    
    Useful for demonstrating understanding of the problem constraints
    and for debugging purposes.
    """
    def is_valid(s):
        """Check if parentheses string is valid"""
        count = 0
        for char in s:
            if char == '(':
                count += 1
            else:  # char == ')'
                count -= 1
                if count < 0:  # More ')' than '(' so far
                    return False
        return count == 0  # All parentheses matched
    
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            # Validate the result (should always be True with correct logic)
            if is_valid(current):
                result.append(current)
            return
        
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result


def generateParenthesis_generate_all_filter(n):
    """
    Alternative approach: Generate all possible combinations, then filter valid ones.
    
    NOT RECOMMENDED for interviews - inefficient!
    O(2^(2n)) time complexity vs O(4^n/sqrt(n)) for backtracking.
    Good to mention why this is worse.
    """
    def is_valid(s):
        count = 0
        for char in s:
            if char == '(':
                count += 1
            else:
                count -= 1
                if count < 0:
                    return False
        return count == 0
    
    def generate_all(pos, current):
        if pos == 2 * n:
            if is_valid(current):
                result.append(current)
            return
        
        # Try both '(' and ')' at each position
        generate_all(pos + 1, current + "(")
        generate_all(pos + 1, current + ")")
    
    result = []
    generate_all(0, "")
    return result


# Test cases and comprehensive analysis
def test_solution():
    """Test all solutions with comprehensive examples."""
    
    test_cases = [
        (0, [""]),
        (1, ["()"]),
        (2, ["(())", "()()"]),
        (3, ["((()))", "(()())", "(())()", "()(())", "()()()"]),
        (4, None)  # Too many to list, just check count
    ]
    
    solutions = [
        ("Backtracking (Recommended)", generateParenthesis),
        ("Backtracking Optimized", generateParenthesis_optimized_params),
        ("BFS Iterative", generateParenthesis_iterative_bfs),
        ("Dynamic Programming", generateParenthesis_dp),
        ("With Validation", generateParenthesis_with_validation)
    ]
    
    print("Testing all solutions:")
    for name, func in solutions:
        print(f"\n{name}:")
        for n, expected in test_cases:
            try:
                result = func(n)
                if expected is None:
                    # For n=4, just check we get the right count (Catalan number)
                    expected_count = catalan_number(n)
                    status = "✓" if len(result) == expected_count else "✗"
                    print(f"  {status} n={n} → Got {len(result)} combinations (expected {expected_count})")
                else:
                    # Sort both lists for comparison since order might differ
                    result_sorted = sorted(result)
                    expected_sorted = sorted(expected)
                    status = "✓" if result_sorted == expected_sorted else "✗"
                    print(f"  {status} n={n} → Expected: {expected}, Got: {result}")
            except Exception as e:
                print(f"  ✗ n={n} → Error: {e}")
    
    print("\n" + "="*70)
    print("Demonstrating inefficient approach:")
    try:
        # Show why generate-all-then-filter is bad
        import time
        n = 10
        
        start = time.time()
        result1 = generateParenthesis(n)
        time1 = time.time() - start
        
        print(f"Backtracking for n={n}: {len(result1)} results in {time1:.4f}s")
        print("Note: Generate-all-then-filter would be much slower!")
        
    except Exception as e:
        print(f"Performance test failed: {e}")


def catalan_number(n):
    """Calculate the nth Catalan number - number of valid parentheses combinations."""
    if n <= 1:
        return 1
    
    # C(n) = (2n)! / ((n+1)! * n!)
    # More stable calculation: C(n) = C(n-1) * 2 * (2n-1) / (n+1)
    catalan = 1
    for i in range(1, n + 1):
        catalan = catalan * 2 * (2 * i - 1) // (i + 1)
    
    return catalan


def trace_backtracking(n):
    """Step-by-step trace of the backtracking algorithm."""
    print(f"Tracing backtracking for n = {n}")
    
    result = []
    call_count = 0
    
    def backtrack(current, open_count, close_count, depth=0):
        nonlocal call_count
        call_count += 1
        
        indent = "  " * depth
        print(f"{indent}Call {call_count}: current='{current}', open={open_count}, close={close_count}")
        
        if len(current) == 2 * n:
            result.append(current)
            print(f"{indent}→ Found valid combination: '{current}'")
            return
        
        # Try adding '('
        if open_count < n:
            print(f"{indent}→ Trying '(' (open_count < n)")
            backtrack(current + "(", open_count + 1, close_count, depth + 1)
        
        # Try adding ')'
        if close_count < open_count:
            print(f"{indent}→ Trying ')' (close_count < open_count)")
            backtrack(current + ")", open_count, close_count + 1, depth + 1)
        
        print(f"{indent}← Backtracking from '{current}'")
    
    backtrack("", 0, 0)
    
    print(f"\nTotal recursive calls: {call_count}")
    print(f"Results found: {result}")
    return result


def analyze_approaches():
    """Comprehensive analysis of different solution approaches."""
    
    analysis = """
    APPROACH COMPARISON FOR GENERATE PARENTHESES:

    1. Backtracking (HIGHLY RECOMMENDED):
       ✓ Most intuitive and natural approach
       ✓ Easy to explain the logic and constraints
       ✓ Optimal time complexity O(4^n / sqrt(n))
       ✓ Clean recursive structure
       ✓ Easy to trace and debug
       ✓ Demonstrates strong problem-solving intuition
       
    2. BFS/Iterative:
       ✓ Shows ability to convert recursion to iteration
       ✓ Sometimes preferred if recursion depth is a concern
       ✓ Same time complexity as backtracking
       ⚠ Slightly more complex implementation
       ⚠ Uses more space (queue vs call stack)
       
    3. Dynamic Programming:
       ✓ Demonstrates DP thinking
       ✓ Shows understanding of Catalan number recurrence
       ✓ Can be more efficient for repeated calls
       ⚠ Less intuitive approach
       ⚠ More complex to derive and implement
       
    4. Generate All + Filter:
       ✗ NEVER use in interviews - too inefficient!
       ✗ O(2^(2n)) time complexity
       ✗ Shows poor algorithmic thinking
       ⚠ Good to mention why this is bad

    INTERVIEW STRATEGY:
    1. Start with problem understanding and examples
    2. Identify this as a backtracking problem
    3. Define the constraints for valid parentheses
    4. Implement clean backtracking solution
    5. Trace through small example (n=2)
    6. Discuss time complexity (Catalan numbers)
    7. Mention alternative approaches if time permits

    KEY INSIGHTS TO DEMONSTRATE:
    - "This is a classic backtracking problem"
    - "Key constraint: never have more ')' than '(' at any point"
    - "We can prune invalid paths early"
    - "Time complexity is related to Catalan numbers"

    COMMON INTERVIEW FOLLOW-UPS:
    - "Can you do this iteratively?" → BFS approach
    - "What's the time complexity?" → Catalan numbers
    - "Can you optimize space?" → discuss call stack vs iteration
    - "How would you validate parentheses?" → separate validation function
    """
    
    print(analysis)


def demonstrate_catalan_connection():
    """Show the connection to Catalan numbers."""
    
    print("CONNECTION TO CATALAN NUMBERS:")
    print("=" * 40)
    
    print("The number of valid parentheses combinations follows Catalan numbers:")
    print("C(n) = (2n)! / ((n+1)! * n!) = (2n choose n) / (n+1)")
    print()
    
    for i in range(6):
        actual_count = len(generateParenthesis(i))
        catalan = catalan_number(i)
        combinations = generateParenthesis(i)
        
        print(f"n = {i}:")
        print(f"  Catalan number C({i}) = {catalan}")
        print(f"  Actual combinations: {actual_count}")
        print(f"  Valid: {actual_count == catalan}")
        if i <= 3:  # Don't print too many for large n
            print(f"  Combinations: {combinations}")
        print()


def complexity_analysis():
    """Detailed complexity analysis."""
    
    analysis = """
    DETAILED COMPLEXITY ANALYSIS:

    Time Complexity: O(4^n / sqrt(n))
    - This is the nth Catalan number
    - Each valid combination requires O(n) time to build
    - Total combinations = C(n) = (1/(n+1)) * (2n choose n)
    - Asymptotically: C(n) ≈ 4^n / (sqrt(π) * n^(3/2))
    
    Why not O(2^(2n))?
    - We're not generating all possible combinations
    - Backtracking prunes invalid paths early
    - Many branches are eliminated when close_count >= open_count

    Space Complexity:
    - O(4^n / sqrt(n)) for storing the result
    - O(n) for recursion stack depth
    - Overall: O(4^n / sqrt(n))

    Practical Performance:
    - n=1: 1 combination
    - n=2: 2 combinations  
    - n=3: 5 combinations
    - n=4: 14 combinations
    - n=5: 42 combinations
    - n=10: 16,796 combinations
    - Growth is exponential but not as bad as 2^(2n)

    Comparison with naive approach:
    - Naive (generate all + filter): O(2^(2n)) time
    - Backtracking: O(4^n / sqrt(n)) time
    - For n=10: 2^20 = 1M vs 16.8K ≈ 60x improvement!
    """
    
    print(analysis)


if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70)
    trace_backtracking(2)
    print("\n" + "="*70)
    demonstrate_catalan_connection()
    print("\n" + "="*70)
    analyze_approaches()
    print("\n" + "="*70)
    complexity_analysis()
