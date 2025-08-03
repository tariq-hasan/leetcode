from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Find the minimum cost to reach the top of the floor where:
        - You can either start from step 0 or step 1
        - You pay the cost at each step you climb
        - You can climb 1 or 2 steps at a time

        Args:
            cost: List of costs for each step

        Returns:
            The minimum cost to reach the top

        Time Complexity: O(n) - We process each step once in a linear pass
        Space Complexity: O(1) - We only store two variables regardless of input size
        """
        # Initialize min costs to reach steps 0 and 1
        min_cost_prev, min_cost_curr = 0, 0

        # Calculate min cost to reach each subsequent position
        for i in range(2, len(cost) + 1):
            # Can reach current position from either i-1 or i-2
            min_cost_prev, min_cost_curr = min_cost_curr, min(
                min_cost_prev + cost[i - 2],  # Cost if coming from i-2
                min_cost_curr + cost[i - 1]   # Cost if coming from i-1
            )

        return min_cost_curr
