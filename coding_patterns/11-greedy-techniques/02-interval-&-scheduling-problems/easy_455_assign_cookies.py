"""
LeetCode 455. Assign Cookies

Problem: Assume you are an awesome parent and want to give your children some cookies. 
But, you should give each child at most one cookie. Each child i has a greed factor g[i], 
which is the minimum size of the cookie that the child will be content with. 
Each cookie j has a size s[j]. If s[j] >= g[i], we can assign cookie j to child i, 
and the child i will be content. Your goal is to maximize the number of your content children.

Key Insights:
1. This is a classic greedy matching problem
2. Strategy: Give the smallest possible cookie that satisfies each child
3. Sort both arrays to enable greedy approach
4. Two pointers technique works perfectly here

Time Complexity: O(m log m + n log n) where m = children, n = cookies
Space Complexity: O(1) if sorting in-place, O(m + n) for copies
"""

# Approach 1: Greedy Two Pointers (Optimal Solution)
def findContentChildren_v1(g, s):
    """
    Greedy approach using two pointers after sorting
    Strategy: For each child, assign the smallest cookie that satisfies them
    """
    # Sort both arrays to enable greedy strategy
    g.sort()  # Children by greed factor (ascending)
    s.sort()  # Cookies by size (ascending)
    
    child = 0  # Pointer for children
    cookie = 0  # Pointer for cookies
    content_children = 0
    
    # Try to satisfy children one by one
    while child < len(g) and cookie < len(s):
        # If current cookie can satisfy current child
        if s[cookie] >= g[child]:
            content_children += 1
            child += 1  # Move to next child
        
        # Always move to next cookie (whether used or not)
        cookie += 1
    
    return content_children

# Approach 2: Greedy with Detailed Explanation
def findContentChildren_v2(g, s):
    """
    Same algorithm but with detailed step tracking for interview explanation
    """
    g_sorted = sorted(g)
    s_sorted = sorted(s)
    
    print(f"Children (sorted by greed): {g_sorted}")
    print(f"Cookies (sorted by size): {s_sorted}")
    
    child = 0
    cookie = 0
    content_children = 0
    assignments = []
    
    while child < len(g_sorted) and cookie < len(s_sorted):
        child_greed = g_sorted[child]
        cookie_size = s_sorted[cookie]
        
        print(f"\nTrying: child {child} (greed={child_greed}) with cookie {cookie} (size={cookie_size})")
        
        if cookie_size >= child_greed:
            print(f"✓ Assignment successful!")
            content_children += 1
            assignments.append((child, cookie, child_greed, cookie_size))
            child += 1
        else:
            print(f"✗ Cookie too small, trying next cookie")
        
        cookie += 1
    
    print(f"\nFinal assignments: {assignments}")
    print(f"Content children: {content_children}")
    
    return content_children

# Approach 3: Alternative Greedy Strategy
def findContentChildren_v3(g, s):
    """
    Alternative strategy: For each cookie, assign to the greediest child it can satisfy
    Less intuitive but also works
    """
    g.sort()  # Children by greed factor
    s.sort()  # Cookies by size
    
    used_children = [False] * len(g)
    content_children = 0
    
    # For each cookie, find the greediest child it can satisfy
    for cookie_size in s:
        # Find the greediest unsatisfied child this cookie can satisfy
        for i in range(len(g) - 1, -1, -1):  # Iterate from greediest to least greedy
            if not used_children[i] and cookie_size >= g[i]:
                used_children[i] = True
                content_children += 1
                break
    
    return content_children

# Approach 4: Using Binary Search (Over-engineered but shows thinking)
def findContentChildren_v4(g, s):
    """
    Using binary search - over-engineered for this problem but shows advanced thinking
    """
    import bisect
    
    g.sort()
    s.sort()
    
    used_cookies = [False] * len(s)
    content_children = 0
    
    for child_greed in g:
        # Find the smallest unused cookie that can satisfy this child
        found = False
        for i in range(len(s)):
            if not used_cookies[i] and s[i] >= child_greed:
                used_cookies[i] = True
                content_children += 1
                found = True
                break
        
        if not found:
            continue
    
    return content_children

# Approach 5: Recursive Solution (For Completeness)
def findContentChildren_v5(g, s):
    """
    Recursive approach - not optimal but shows different thinking
    """
    g = sorted(g)
    s = sorted(s)
    
    def helper(child_idx, cookie_idx):
        # Base cases
        if child_idx >= len(g) or cookie_idx >= len(s):
            return 0
        
        # Option 1: Skip current cookie
        skip_cookie = helper(child_idx, cookie_idx + 1)
        
        # Option 2: Try to assign current cookie to current child
        assign_cookie = 0
        if s[cookie_idx] >= g[child_idx]:
            assign_cookie = 1 + helper(child_idx + 1, cookie_idx + 1)
        
        return max(skip_cookie, assign_cookie)
    
    return helper(0, 0)

def prove_greedy_optimality():
    """
    Explain why the greedy approach is optimal
    """
    print("=== Why Greedy Strategy is Optimal ===")
    print()
    print("GREEDY STRATEGY:")
    print("- Sort children by greed factor (ascending)")
    print("- Sort cookies by size (ascending)")
    print("- For each child, assign smallest cookie that satisfies them")
    print()
    print("WHY IT'S OPTIMAL:")
    print("1. EXCHANGE ARGUMENT:")
    print("   - Suppose optimal solution assigns larger cookie to child when smaller would work")
    print("   - We can always exchange this with a future assignment")
    print("   - This doesn't decrease the number of satisfied children")
    print()
    print("2. GREEDY CHOICE PROPERTY:")
    print("   - Satisfying less greedy children first is always beneficial")
    print("   - Leaves more options for greedier children later")
    print()
    print("3. NO WORSE THAN OPTIMAL:")
    print("   - Our solution never uses 'more cookie than necessary'")
    print("   - Always leaves maximum flexibility for remaining assignments")
    print()
    print("MATHEMATICAL PROOF SKETCH:")
    print("- Let OPT be an optimal solution")
    print("- Let G be our greedy solution")  
    print("- If G ≠ OPT, we can transform OPT to G without losing optimality")
    print("- Therefore, G is optimal")

def analyze_examples():
    """
    Analyze examples step by step
    """
    examples = [
        ([1, 2, 3], [1, 1], 1),
        ([1, 2], [1, 2, 3], 2),
        ([1, 2, 7, 8, 9], [1, 3, 5, 9, 10], 4),
        ([10, 9, 8, 7], [5, 6, 7, 8], 2),
        ([], [1, 2, 3], 0),
        ([1, 2, 3], [], 0),
        ([5], [1, 2, 3, 4], 0)
    ]
    
    print("=== Example Analysis ===")
    
    for i, (children, cookies, expected) in enumerate(examples):
        print(f"\nExample {i+1}: Children={children}, Cookies={cookies}")
        
        # Test main approach
        result = findContentChildren_v1(children[:], cookies[:])
        print(f"Result: {result}, Expected: {expected}")
        
        # Show detailed walkthrough for smaller examples
        if len(children) <= 5 and len(cookies) <= 5:
            print("Detailed walkthrough:")
            findContentChildren_v2(children[:], cookies[:])
        
        assert result == expected, f"Mismatch in example {i+1}"

def test_edge_cases():
    """
    Test various edge cases
    """
    edge_cases = [
        ([], [], 0),                    # Both empty
        ([1], [], 0),                   # No cookies
        ([], [1], 0),                   # No children
        ([1], [1], 1),                  # Perfect match
        ([2], [1], 0),                  # Cookie too small
        ([1], [2], 1),                  # Cookie larger than needed
        ([1, 1, 1], [1], 1),           # More children than cookies
        ([1], [1, 1, 1], 1),           # More cookies than children
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5], 5), # All can be satisfied
        ([1, 2, 3, 4, 5], [5], 1),     # Only one child can be satisfied
        ([100], [1, 2, 3, 99], 0),     # No cookie big enough
    ]
    
    print("=== Edge Case Testing ===")
    
    for i, (children, cookies, expected) in enumerate(edge_cases):
        print(f"\nEdge case {i+1}: Children={children}, Cookies={cookies}")
        
        # Test multiple approaches
        approaches = [
            ("Two Pointers", findContentChildren_v1),
            ("Alternative Greedy", findContentChildren_v3),
            ("Recursive", findContentChildren_v5)
        ]
        
        results = []
        for name, func in approaches:
            result = func(children[:], cookies[:])
            results.append(result)
            print(f"{name}: {result}")
        
        # Verify all approaches agree
        assert all(r == results[0] for r in results), f"Approaches disagree on case {i+1}"
        
        # Verify against expected
        assert results[0] == expected, f"Expected {expected}, got {results[0]} for case {i+1}"

def complexity_comparison():
    """
    Compare different approaches' complexity
    """
    print("=== Complexity Comparison ===")
    print()
    print("APPROACH 1 - Two Pointers (Recommended):")
    print("- Time: O(m log m + n log n) for sorting")
    print("- Space: O(1) if sorting in-place")
    print("- Simple, efficient, easy to understand")
    print()
    print("APPROACH 3 - Alternative Greedy:")
    print("- Time: O(m log m + n log n + m*n) - nested loops")
    print("- Space: O(m) for tracking used children")
    print("- Less efficient due to nested iteration")
    print()
    print("APPROACH 5 - Recursive:")
    print("- Time: O(2^(m+n)) without memoization - exponential!")
    print("- Space: O(m+n) recursion depth")
    print("- Explores all possibilities, very inefficient")
    print()
    print("WINNER: Two pointers approach")
    print("- Optimal time complexity")
    print("- Minimal space usage")
    print("- Clear and intuitive logic")

def interview_tips():
    """
    Key points to mention during interview
    """
    print("=== Interview Discussion Points ===")
    print()
    print("1. PROBLEM RECOGNITION:")
    print("   - This is a bipartite matching problem")
    print("   - Greedy approach works due to problem structure")
    print("   - No complex constraints or dependencies")
    print()
    print("2. GREEDY STRATEGY:")
    print("   - Always assign smallest sufficient cookie")
    print("   - Process children from least to most greedy")
    print("   - Two pointers technique after sorting")
    print()
    print("3. WHY SORTING HELPS:")
    print("   - Enables greedy strategy to work optimally")
    print("   - Ensures we make best local choices")
    print("   - Allows efficient two-pointer traversal")
    print()
    print("4. ALTERNATIVE APPROACHES:")
    print("   - Could use dynamic programming (overkill)")
    print("   - Could try all permutations (exponential)")
    print("   - Greedy is both simple and optimal")
    print()
    print("5. EDGE CASES TO DISCUSS:")
    print("   - Empty arrays")
    print("   - No satisfiable children")
    print("   - All children satisfiable")
    print("   - Identical greed factors or cookie sizes")

if __name__ == "__main__":
    print("=== Assign Cookies Solutions ===")
    
    # Test with examples
    analyze_examples()
    
    # Test edge cases
    test_edge_cases()
    
    # Explain why greedy works
    prove_greedy_optimality()
    
    # Compare approaches
    complexity_comparison()
    
    # Interview tips
    interview_tips()

"""
Critical Interview Discussion Points:

1. **Problem Classification**:
   - Bipartite matching problem with constraints
   - Classic greedy algorithm application
   - Optimization problem: maximize satisfied children

2. **Greedy Strategy**:
   - Key insight: assign smallest possible cookie to each child
   - Why it works: preserves maximum options for future assignments
   - Sorting enables the greedy approach

3. **Algorithm Steps**:
   1. Sort children by greed factor (ascending)
   2. Sort cookies by size (ascending)
   3. Use two pointers to match greedily
   4. For each child, find smallest sufficient cookie

4. **Why Greedy is Optimal**:
   - Exchange argument: can always swap assignments without loss
   - Greedy choice property: satisfying less greedy children first is better
   - No subproblems overlap, so greedy works

5. **Complexity Analysis**:
   - Time: O(m log m + n log n) - dominated by sorting
   - Space: O(1) if sorting in-place
   - Cannot avoid sorting for optimal greedy strategy

6. **Two Pointers Technique**:
   - Efficient linear scan after sorting
   - Child pointer only advances on successful assignment
   - Cookie pointer always advances (used or discarded)

7. **Edge Cases**:
   - Empty arrays (no children or no cookies)
   - No satisfiable assignments
   - Perfect matches vs. no matches
   - Multiple children with same greed factor

8. **Alternative Approaches**:
   - Dynamic programming: overkill for this problem
   - Brute force: exponential time complexity
   - Different greedy strategies: less efficient

9. **Real-world Applications**:
   - Resource allocation problems
   - Task assignment with constraints
   - Matching problems in economics
   - Load balancing scenarios

10. **Interview Strategy**:
    - Start by recognizing this as a greedy problem
    - Explain why sorting is necessary
    - Walk through the two-pointer technique
    - Prove optimality with exchange argument
    - Discuss time/space complexity
    - Handle edge cases systematically
"""
