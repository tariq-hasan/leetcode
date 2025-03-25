from typing import List


class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        """
        The time complexity is O(n), where n is days[-1].
        The space complexity is O(n), where n is days[-1].
        """
        def solve(dp, curr_day):
            if curr_day > days[-1]:
                return 0

            if curr_day not in is_travel_needed:
                return solve(dp, curr_day + 1)

            if dp[curr_day] != -1:
                return dp[curr_day]

            one_day = costs[0] + solve(dp, curr_day + 1)
            seven_day = costs[1] + solve(dp, curr_day + 7)
            thirty_day = costs[2] + solve(dp, curr_day + 30)

            dp[curr_day] = min(one_day, min(seven_day, thirty_day))
            return dp[curr_day]

        dp = [-1] * (days[-1] + 1)
        is_travel_needed = set(days)

        return solve(dp, 1)
