"""
LeetCode 1029: Two City Scheduling

Problem Statement:
A company is planning to interview 2n people. Given the array costs where costs[i] = [aCosti, bCosti], 
the cost of flying the ith person to city A is aCosti, and the cost of flying the ith person to 
city B is bCosti.

Return the minimum cost to fly every person to a city such that exactly n people arrive in each city.

Example 1:
Input: costs = [[10,20],[30,200],[400,50],[30,20]]
Output: 110
Explanation: 
The first person goes to city A for a cost of 10.
The second person goes to city A for a cost of 30.
The third person goes to city B for a cost of 50.
The fourth person goes to city B for a cost of 20.
The total minimum cost is 10 + 30 + 50 + 20 = 110.

Example 2:
Input: costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]
Output: 1859
"""

def twoCitySchedCost(costs):
    """
    Approach: Greedy Algorithm - Sort by Cost Difference
    
    Key Insight: 
    The problem is equivalent to: if we send everyone to city A first, 
    then decide which n people to "refund" and send to city B instead.
    
    The refund amount for person i is: costs[i][0] - costs[i][1]
    (We save costs[i][0] but spend costs[i][1])
    
    We want to maximize our savings, so we pick the n people with the 
    largest refund amounts (most negative differences).
    
    Algorithm:
    1. Calculate the difference (A_cost - B_cost) for each person
    2. Sort by this difference (ascending order)
    3. Send first n people to city B, remaining n to city A
    
    Time Complexity: O(n log n) due to sorting
    Space Complexity: O(1) if we modify input, O(n) for auxiliary space
    """
    n = len(costs) // 2
    
    # Sort by the difference between cost A and cost B
    # People with most negative difference should go to city B
    costs.sort(key=lambda x: x[0] - x[1])
    
    total_cost = 0
    
    # First n people go to city B (they have the most savings)
    for i in range(n):
        total_cost += costs[i][1]
    
    # Remaining n people go to city A
    for i in range(n, 2 * n):
        total_cost += costs[i][0]
    
    return total_cost


def twoCitySchedCost_with_explanation(costs):
    """
    More detailed version that shows the decision process
    """
    n = len(costs) // 2
    
    # Calculate savings for each person if they go to B instead of A
    savings = []
    for i, (cost_a, cost_b) in enumerate(costs):
        savings.append((cost_a - cost_b, i))
    
    # Sort by savings (descending order of savings = ascending order of difference)
    savings.sort()
    
    total_cost = 0
    city_assignments = [''] * len(costs)
    
    # Send first n people (with most savings) to city B
    for i in range(n):
        person_idx = savings[i][1]
        total_cost += costs[person_idx][1]
        city_assignments[person_idx] = 'B'
    
    # Send remaining people to city A
    for i in range(n, 2 * n):
        person_idx = savings[i][1]
        total_cost += costs[person_idx][0]
        city_assignments[person_idx] = 'A'
    
    return total_cost, city_assignments


def twoCitySchedCost_alternative_thinking(costs):
    """
    Alternative way to think about the problem:
    What if we send everyone to city A first, then optimize?
    """
    n = len(costs) // 2
    
    # Start by sending everyone to city A
    total_cost = sum(cost[0] for cost in costs)
    
    # Calculate how much we save by sending each person to B instead
    refunds = []
    for i, (cost_a, cost_b) in enumerate(costs):
        refund = cost_a - cost_b  # We save cost_a but spend cost_b
        refunds.append((refund, i))
    
    # Sort by refund amount (descending - we want maximum savings first)
    refunds.sort(reverse=True)
    
    # Apply the top n refunds (send n people to city B)
    for i in range(n):
        total_cost -= refunds[i][0]
    
    return total_cost


def twoCitySchedCost_dp(costs):
    """
    Dynamic Programming Solution (less efficient but shows alternative approach)
    
    dp[i][j] = minimum cost to assign first i people with j people going to city A
    
    Time Complexity: O(n²)
    Space Complexity: O(n²)
    """
    n = len(costs) // 2
    
    # Initialize DP table
    # dp[i][j] = min cost for first i people with j going to city A
    dp = [[float('inf')] * (n + 1) for _ in range(len(costs) + 1)]
    dp[0][0] = 0
    
    for i in range(1, len(costs) + 1):
        for j in range(max(0, i - n), min(i, n) + 1):
            # Send person i-1 to city A (if we haven't sent n to A already)
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i-1][j-1] + costs[i-1][0])
            
            # Send person i-1 to city B (if we haven't sent n to B already)
            if i - j > 0 and i - j <= n:
                dp[i][j] = min(dp[i][j], dp[i-1][j] + costs[i-1][1])
    
    return dp[len(costs)][n]


# Test cases
def test_solution():
    """Test all solutions with provided examples and edge cases"""
    
    test_cases = [
        ([[10,20],[30,200],[400,50],[30,20]], 110),
        ([[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]], 1859),
        ([[10,20],[30,200]], 40),  # Minimum case: n=1
        ([[100,200],[200,100]], 300),  # Both have same total, different optimal
        ([[1,2],[3,4],[5,6],[7,8]], 18)  # Simple increasing case
    ]
    
    solutions = [
        ("Greedy (Sort by Difference)", twoCitySchedCost),
        ("Alternative Thinking", twoCitySchedCost_alternative_thinking),
        ("Dynamic Programming", twoCitySchedCost_dp)
    ]
    
    for sol_name, solution_func in solutions:
        print(f"\nTesting {sol_name}:")
        print("=" * 50)
        
        for i, (costs, expected) in enumerate(test_cases, 1):
            # Create a copy since some functions modify input
            costs_copy = [row[:] for row in costs]
            result = solution_func(costs_copy)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            
            print(f"Test Case {i}: {status}")
            print(f"  Input: {costs}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
        print()


def demonstrate_greedy_intuition():
    """
    Demonstrates why the greedy approach works with a detailed example
    """
    costs = [[10,20],[30,200],[400,50],[30,20]]
    print("Demonstrating Greedy Intuition:")
    print("=" * 50)
    print(f"Input: {costs}")
    print()
    
    print("Step 1: Calculate differences (A_cost - B_cost) for each person:")
    for i, (a, b) in enumerate(costs):
        diff = a - b
        print(f"Person {i}: A={a}, B={b}, Difference={diff}")
    print()
    
    print("Step 2: Sort by difference (people with most negative difference go to B):")
    indexed_costs = [(costs[i][0] - costs[i][1], i, costs[i]) for i in range(len(costs))]
    indexed_costs.sort()
    
    for diff, person_idx, (a, b) in indexed_costs:
        print(f"Person {person_idx}: Difference={diff}, Costs=[{a}, {b}]")
    print()
    
    n = len(costs) // 2
    total = 0
    print(f"Step 3: Send first {n} people to city B, remaining {n} to city A:")
    
    for i in range(n):
        diff, person_idx, (a, b) = indexed_costs[i]
        total += b
        print(f"Person {person_idx} → City B (cost: {b})")
    
    for i in range(n, 2 * n):
        diff, person_idx, (a, b) = indexed_costs[i]
        total += a
        print(f"Person {person_idx} → City A (cost: {a})")
    
    print(f"\nTotal minimum cost: {total}")


# Run tests and demonstration
if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70 + "\n")
    demonstrate_greedy_intuition()


"""
INTERVIEW DISCUSSION POINTS:

1. PROBLEM UNDERSTANDING:
   - This is an optimization problem with constraints
   - We need exactly n people in each city (balanced assignment)
   - Goal: minimize total cost

2. KEY INSIGHTS:
   - Greedy approach: sort by cost difference
   - People with largest savings (most negative A-B difference) should go to B
   - Alternative view: send everyone to A first, then optimize by switching n people to B

3. WHY GREEDY WORKS:
   - We want to minimize total cost
   - Each person's contribution to total cost is independent
   - The constraint is just "exactly n to each city"
   - So we should prioritize people who save the most money by going to their preferred city

4. TIME & SPACE COMPLEXITY:
   - Greedy: O(n log n) time, O(1) space (if we can modify input)
   - DP: O(n²) time, O(n²) space (included for completeness)

5. EDGE CASES:
   - Minimum input: n=1 (2 people total)
   - All people prefer same city (still need to split evenly)
   - Costs are equal for all people

6. FOLLOW-UP QUESTIONS:
   - What if we had 3 cities instead of 2?
   - What if we could send different numbers to each city?
   - How would you handle this with very large inputs?
   - Can you solve without sorting? (Answer: No, we need to find optimal assignment)

7. ALTERNATIVE APPROACHES:
   - Brute force: Try all C(2n,n) combinations - exponential time
   - DP: O(n²) solution shown above
   - Greedy is optimal for this specific problem structure
"""
