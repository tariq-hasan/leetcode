"""
LeetCode 502 - IPO
Difficulty: Hard

Problem:
You are given n projects where the ith project has a pure profit profits[i] and a minimum 
capital of capital[i] needed to start it. Initially, you have w capital. When you finish 
a project, you will obtain its pure profit and the profit will be added to your total capital.

Pick a list of at most k distinct projects from given projects to maximize your final capital, 
and return the final maximized capital.

Example 1:
Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
Output: 4
Explanation: Since your initial capital is 0, you can only start the project indexed 0.
After finishing it you will obtain profit 1 and your capital becomes 1.
With capital 1, you can either start the project indexed 1 or the project indexed 2.
Since you can choose at most 2 projects, you need to finish projects 0 and 2 to get 
the maximum capital. Therefore, output the final maximized capital, which is 0 + 1 + 3 = 4.

Solution Strategy:
1. Use a greedy approach with two heaps
2. Min-heap for projects by capital requirement (affordable projects)
3. Max-heap for profits of affordable projects
4. Always pick the most profitable project we can afford
"""

import heapq
from typing import List

def findMaximizedCapital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    """
    Time Complexity: O(n log n + k log n) where n is number of projects
    Space Complexity: O(n)
    
    Args:
        k: Maximum number of projects we can do
        w: Initial capital
        profits: List of profits for each project
        capital: List of capital requirements for each project
    
    Returns:
        Maximum capital after completing at most k projects
    """
    n = len(profits)
    
    # Create list of (capital_required, profit) and sort by capital
    projects = [(capital[i], profits[i]) for i in range(n)]
    projects.sort()  # Sort by capital requirement
    
    # Max heap for profits of affordable projects
    max_profit_heap = []
    
    current_capital = w
    project_idx = 0
    
    # Do at most k projects
    for _ in range(k):
        # Add all affordable projects to the profit heap
        while project_idx < n and projects[project_idx][0] <= current_capital:
            # Python uses min-heap, so negate profit for max-heap behavior
            heapq.heappush(max_profit_heap, -projects[project_idx][1])
            project_idx += 1
        
        # If no affordable projects, break
        if not max_profit_heap:
            break
            
        # Take the most profitable affordable project
        max_profit = -heapq.heappop(max_profit_heap)
        current_capital += max_profit
    
    return current_capital


# Alternative implementation with cleaner heap usage
def findMaximizedCapitalV2(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    """
    Alternative implementation using separate heaps more explicitly
    """
    import heapq
    
    # Min heap for (capital_required, profit) - projects we can't afford yet
    min_capital_heap = []
    # Max heap for profits - projects we can afford
    max_profit_heap = []
    
    # Initialize with all projects in capital heap
    for i in range(len(profits)):
        heapq.heappush(min_capital_heap, (capital[i], profits[i]))
    
    current_capital = w
    
    for _ in range(k):
        # Move all affordable projects to profit heap
        while min_capital_heap and min_capital_heap[0][0] <= current_capital:
            cap, profit = heapq.heappop(min_capital_heap)
            heapq.heappush(max_profit_heap, -profit)  # Negative for max heap
        
        # If no affordable projects, we're done
        if not max_profit_heap:
            break
        
        # Take most profitable project
        best_profit = -heapq.heappop(max_profit_heap)
        current_capital += best_profit
    
    return current_capital


# Test cases
def test_ipo():
    """Test the IPO solution with various cases"""
    
    # Test case 1: Basic example
    k, w = 2, 0
    profits = [1, 2, 3]
    capital = [0, 1, 1]
    result = findMaximizedCapital(k, w, profits, capital)
    print(f"Test 1 - Expected: 4, Got: {result}")
    
    # Test case 2: Can't afford any projects initially
    k, w = 1, 0
    profits = [1, 2, 3]
    capital = [1, 1, 2]
    result = findMaximizedCapital(k, w, profits, capital)
    print(f"Test 2 - Expected: 0, Got: {result}")
    
    # Test case 3: Can do more projects than available
    k, w = 10, 0
    profits = [1, 2, 3]
    capital = [0, 1, 1]
    result = findMaximizedCapital(k, w, profits, capital)
    print(f"Test 3 - Expected: 6, Got: {result}")
    
    # Test case 4: Large capital initially
    k, w = 2, 3
    profits = [1, 2, 3]
    capital = [0, 1, 1]
    result = findMaximizedCapital(k, w, profits, capital)
    print(f"Test 4 - Expected: 8, Got: {result}")

if __name__ == "__main__":
    test_ipo()


"""
Key Insights for Interview:

1. **Greedy Strategy**: Always pick the most profitable project you can currently afford
2. **Two-Heap Approach**: 
   - Min-heap for projects by capital (what we might afford later)
   - Max-heap for profits (what we can afford now)
3. **Time Complexity**: O(n log n + k log n) - sorting + k iterations with heap ops
4. **Space Complexity**: O(n) for the heaps

Interview Tips:
- Start by explaining the greedy intuition
- Draw out the heap states for a small example
- Mention edge cases (k=0, no affordable projects, etc.)
- Discuss why greedy works (optimal substructure)
- Be ready to implement both versions and explain trade-offs

Common Follow-ups:
- What if we want to track which projects were selected?
- How would you modify for minimum projects needed to reach target capital?
- What if projects have dependencies?
"""
