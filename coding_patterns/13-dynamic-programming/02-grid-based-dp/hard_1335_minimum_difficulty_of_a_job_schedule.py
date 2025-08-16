"""
LeetCode 1335: Minimum Difficulty of a Job Schedule

Problem: You want to schedule a list of jobs in d days. Jobs are dependent 
(you have to finish job i before job i+1). The difficulty of a day is the 
maximum difficulty of a job done on that day. Return the minimum difficulty 
of a job schedule.

Key Insights:
1. Jobs must be done in order (can't skip or reorder)
2. Each day's difficulty = max difficulty of jobs done that day
3. Must use exactly d days (can't finish early)
4. Need at least d jobs to schedule d days

State: dp[i][d] = minimum difficulty to schedule first i jobs in d days
Transition: Try all possible ways to split the last day's jobs

Time Complexity: O(n^2 * d)
Space Complexity: O(n * d) -> can be optimized to O(n)
"""

class Solution:
    def minDifficulty(self, jobDifficulty: list[int], d: int) -> int:
        """
        Top-down DP with memoization approach.
        
        State: (job_index, days_left)
        Returns: minimum difficulty to schedule jobs[job_index:] in days_left days
        """
        n = len(jobDifficulty)
        
        # Edge case: impossible to schedule
        if n < d:
            return -1
        
        memo = {}
        
        def dp(start: int, days_left: int) -> int:
            """
            Returns minimum difficulty to schedule jobs[start:] in days_left days
            
            Args:
                start: starting job index
                days_left: number of days remaining
            """
            # Base case: no days left
            if days_left == 0:
                return 0 if start == n else float('inf')
            
            # Base case: not enough jobs for remaining days
            if n - start < days_left:
                return float('inf')
            
            # Memoization
            if (start, days_left) in memo:
                return memo[(start, days_left)]
            
            # If only one day left, must do all remaining jobs today
            if days_left == 1:
                result = max(jobDifficulty[start:])
                memo[(start, days_left)] = result
                return result
            
            # Try different ways to split jobs for today
            min_difficulty = float('inf')
            max_today = 0
            
            # Try ending today after job i (at least 1 job today)
            # Leave at least (days_left - 1) jobs for remaining days
            for i in range(start, n - days_left + 2):
                max_today = max(max_today, jobDifficulty[i])
                
                # Difficulty = today's max + optimal for remaining jobs/days
                remaining_difficulty = dp(i + 1, days_left - 1)
                if remaining_difficulty != float('inf'):
                    min_difficulty = min(min_difficulty, 
                                       max_today + remaining_difficulty)
            
            memo[(start, days_left)] = min_difficulty
            return min_difficulty
        
        result = dp(0, d)
        return result if result != float('inf') else -1


class SolutionBottomUp:
    def minDifficulty(self, jobDifficulty: list[int], d: int) -> int:
        """
        Bottom-up DP solution for better understanding of state transitions.
        
        dp[i][j] = minimum difficulty to schedule first i jobs in j days
        """
        n = len(jobDifficulty)
        
        if n < d:
            return -1
        
        # dp[i][j] = min difficulty for first i jobs in j days
        dp = [[float('inf')] * (d + 1) for _ in range(n + 1)]
        
        # Base case: 0 jobs in 0 days = 0 difficulty
        dp[0][0] = 0
        
        # Fill the DP table
        for i in range(1, n + 1):  # jobs
            for j in range(1, min(i, d) + 1):  # days
                # Try all possible last day job ranges
                max_difficulty = 0
                
                # Last day includes jobs from k to i-1 (0-indexed)
                for k in range(i - 1, j - 2, -1):  # at least j-1 jobs before
                    max_difficulty = max(max_difficulty, jobDifficulty[k])
                    
                    if dp[k][j - 1] != float('inf'):
                        dp[i][j] = min(dp[i][j], 
                                     dp[k][j - 1] + max_difficulty)
        
        return dp[n][d] if dp[n][d] != float('inf') else -1


class SolutionSpaceOptimized:
    def minDifficulty(self, jobDifficulty: list[int], d: int) -> int:
        """
        Space-optimized version using 1D arrays.
        Space: O(n) instead of O(n * d)
        """
        n = len(jobDifficulty)
        
        if n < d:
            return -1
        
        # Only need previous day's results
        prev = [float('inf')] * (n + 1)
        curr = [float('inf')] * (n + 1)
        
        prev[0] = 0  # 0 jobs in 0 days
        
        for day in range(1, d + 1):
            for i in range(day, n + 1):  # need at least 'day' jobs
                curr[i] = float('inf')
                max_difficulty = 0
                
                # Try all possible ranges for current day
                for k in range(i - 1, day - 2, -1):
                    max_difficulty = max(max_difficulty, jobDifficulty[k])
                    
                    if prev[k] != float('inf'):
                        curr[i] = min(curr[i], prev[k] + max_difficulty)
            
            # Swap arrays
            prev, curr = curr, [float('inf')] * (n + 1)
        
        return prev[n] if prev[n] != float('inf') else -1


class SolutionMonotonicStack:
    def minDifficulty(self, jobDifficulty: list[int], d: int) -> int:
        """
        Advanced solution using monotonic stack optimization.
        
        Key insight: When we extend the current day by one job, we can 
        efficiently update the maximum using a monotonic stack.
        
        Time: O(n * d), Space: O(n)
        """
        n = len(jobDifficulty)
        
        if n < d:
            return -1
        
        # dp[i] = minimum difficulty to finish first i jobs
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        for day in range(1, d + 1):
            new_dp = [float('inf')] * (n + 1)
            
            # Monotonic decreasing stack: (job_index, max_difficulty_so_far)
            stack = []
            
            for i in range(day, n + 1):  # need at least 'day' jobs
                # Current job difficulty
                curr_difficulty = jobDifficulty[i - 1]
                min_cost = dp[i - 1] + curr_difficulty  # single job today
                
                # Use stack to find minimum cost efficiently
                while stack and stack[-1][1] <= curr_difficulty:
                    j, max_diff = stack.pop()
                    min_cost = min(min_cost, dp[j] + curr_difficulty)
                
                if stack:
                    j, max_diff = stack[-1]
                    min_cost = min(min_cost, new_dp[j] + max_diff)
                
                new_dp[i] = min_cost
                stack.append((i - 1, curr_difficulty))
            
            dp = new_dp
        
        return dp[n] if dp[n] != float('inf') else -1


def test_solutions():
    """Comprehensive test cases"""
    
    # Test case 1
    jobs1, d1 = [6,5,4,3,2,1], 2
    # Expected: 7
    # Day 1: [6,5,4,3,2] -> max = 6, Day 2: [1] -> max = 1, Total = 7
    
    # Test case 2
    jobs2, d2 = [9,9,9], 4
    # Expected: -1 (impossible: 3 jobs, 4 days)
    
    # Test case 3
    jobs3, d3 = [1,1,1], 3
    # Expected: 3 (each job on separate day)
    
    # Test case 4
    jobs4, d4 = [7,1,7,1,7,1], 3
    # Expected: 15
    # Day 1: [7,1,7] -> max=7, Day 2: [1,7] -> max=7, Day 3: [1] -> max=1
    
    solutions = [
        ("Top-down DP", Solution()),
        ("Bottom-up DP", SolutionBottomUp()),
        ("Space Optimized", SolutionSpaceOptimized()),
        ("Monotonic Stack", SolutionMonotonicStack())
    ]
    
    test_cases = [
        ("Test 1", jobs1, d1, 7),
        ("Test 2", jobs2, d2, -1),
        ("Test 3", jobs3, d3, 3),
        ("Test 4", jobs4, d4, 15)
    ]
    
    for name, jobs, d, expected in test_cases:
        print(f"\n{name} - Jobs: {jobs}, Days: {d} (Expected: {expected}):")
        for sol_name, solution in solutions:
            try:
                result = solution.minDifficulty(jobs, d)
                status = "✓" if result == expected else "✗"
                print(f"  {sol_name}: {result} {status}")
            except Exception as e:
                print(f"  {sol_name}: ERROR - {e}")


def explain_approach():
    """Visual explanation of the approach"""
    print("\nPROBLEM BREAKDOWN:")
    print("Jobs: [6,5,4,3,2,1], Days: 2")
    print("\nPossible schedules:")
    print("Day 1: [6] -> max=6, Day 2: [5,4,3,2,1] -> max=5, Total=11")
    print("Day 1: [6,5] -> max=6, Day 2: [4,3,2,1] -> max=4, Total=10") 
    print("Day 1: [6,5,4] -> max=6, Day 2: [3,2,1] -> max=3, Total=9")
    print("Day 1: [6,5,4,3] -> max=6, Day 2: [2,1] -> max=2, Total=8")
    print("Day 1: [6,5,4,3,2] -> max=6, Day 2: [1] -> max=1, Total=7 ← OPTIMAL")
    
    print("\nDP State Transition:")
    print("dp(start, days_left) = minimum difficulty for jobs[start:] in days_left days")
    print("Try all possible splits for the first day:")
    print("dp(0,2) = min(max(jobs[0:i]) + dp(i, 1)) for all valid i")


def complexity_analysis():
    """Detailed complexity analysis"""
    print("\nCOMPLEXITY ANALYSIS:")
    print("\n1. Top-down DP:")
    print("   - States: O(n * d)")
    print("   - Transitions: O(n) per state")  
    print("   - Time: O(n^2 * d)")
    print("   - Space: O(n * d)")
    
    print("\n2. Space Optimized:")
    print("   - Only store previous day's results")
    print("   - Time: O(n^2 * d)")
    print("   - Space: O(n)")
    
    print("\n3. Monotonic Stack:")
    print("   - Use stack to optimize range maximum queries")
    print("   - Time: O(n * d)")
    print("   - Space: O(n)")


# Interview talking points
"""
INTERVIEW DISCUSSION POINTS:

1. Problem Understanding:
   - Must do jobs in order (dependency constraint)
   - Each day's difficulty = maximum job difficulty that day
   - Must use exactly d days
   - Impossible if fewer jobs than days

2. State Design:
   - dp[i][j] = min difficulty for first i jobs in j days
   - OR dp(start, days_left) = min difficulty for jobs[start:] in days_left days

3. Key Insights:
   - For each state, try all possible ways to split the last day
   - Range maximum can be computed incrementally
   - Monotonic stack can optimize range queries

4. Edge Cases:
   - n < d (impossible case)
   - d = 1 (all jobs in one day)
   - d = n (one job per day)
   - All jobs have same difficulty

5. Optimizations:
   - Space: Use 1D array instead of 2D
   - Time: Monotonic stack for O(n*d) complexity
   - Precompute range maximums if needed

6. Follow-up Questions:
   - What if jobs can be reordered? (becomes assignment problem)
   - What if we want to maximize difficulty? (similar DP)
   - What if each day has different capacity? (knapsack variant)

7. Similar Problems:
   - Burst Balloons (interval DP)
   - Matrix Chain Multiplication
   - Optimal Binary Search Tree

Recommended Interview Solution: Top-down DP (most intuitive)
Advanced Optimization: Monotonic Stack (shows algorithmic depth)
"""

if __name__ == "__main__":
    test_solutions()
    explain_approach() 
    complexity_analysis()
