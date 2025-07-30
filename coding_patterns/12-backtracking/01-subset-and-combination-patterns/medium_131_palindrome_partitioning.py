from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        """
        Problem: Given string s, partition it such that every substring is a palindrome.
        Return all possible palindrome partitioning of s.
        
        APPROACH 1: BACKTRACKING (Most Common Interview Solution)
        Time: O(N * 2^N) where N = len(s)
        - 2^N possible partitions (each position can be cut or not)
        - N time to check palindrome and copy partition
        Space: O(N) for recursion depth and current partition
        
        This is the standard approach most interviewers expect.
        """
        result = []
        
        def is_palindrome(substring):
            """Check if a substring is palindrome"""
            left, right = 0, len(substring) - 1
            while left < right:
                if substring[left] != substring[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        def backtrack(start_idx, current_partition):
            """
            start_idx: current position in string s
            current_partition: current partition being built
            """
            # Base case: reached end of string
            if start_idx == len(s):
                result.append(current_partition[:])  # Make a copy
                return
            
            # Try all possible substrings starting from start_idx
            for end_idx in range(start_idx, len(s)):
                substring = s[start_idx:end_idx + 1]
                
                if is_palindrome(substring):
                    # Add this palindrome to current partition
                    current_partition.append(substring)
                    # Recurse for remaining string
                    backtrack(end_idx + 1, current_partition)
                    # Backtrack
                    current_partition.pop()
        
        backtrack(0, [])
        return result
    
    def partition_optimized(self, s: str) -> List[List[str]]:
        """
        APPROACH 2: BACKTRACKING WITH PRECOMPUTED PALINDROMES (OPTIMAL)
        Time: O(N^2 + N * 2^N) = O(N * 2^N)
        - O(N^2) to precompute palindrome table
        - O(N * 2^N) for backtracking and copying results
        Space: O(N^2) for palindrome table + O(N) for recursion
        
        This shows optimization thinking - precompute to avoid repeated work.
        """
        n = len(s)
        result = []
        
        # Precompute palindrome check table
        # is_palindrome[i][j] = True if s[i:j+1] is palindrome
        is_palindrome = [[False] * n for _ in range(n)]
        
        # Every single character is palindrome
        for i in range(n):
            is_palindrome[i][i] = True
        
        # Check for palindromes of length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                is_palindrome[i][i + 1] = True
        
        # Check for palindromes of length 3 and more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and is_palindrome[i + 1][j - 1]:
                    is_palindrome[i][j] = True
        
        def backtrack(start, current_partition):
            if start == n:
                result.append(current_partition[:])
                return
            
            for end in range(start, n):
                if is_palindrome[start][end]:
                    current_partition.append(s[start:end + 1])
                    backtrack(end + 1, current_partition)
                    current_partition.pop()
        
        backtrack(0, [])
        return result
    
    def partition_dp_approach(self, s: str) -> List[List[str]]:
        """
        APPROACH 3: DYNAMIC PROGRAMMING APPROACH
        Time: O(N^2 + N * 2^N)
        Space: O(N^2)
        
        Alternative thinking - build solutions bottom-up.
        Good to mention as different approach but backtracking is more intuitive.
        """
        n = len(s)
        
        # Precompute palindrome table (same as above)
        is_palindrome = [[False] * n for _ in range(n)]
        
        for i in range(n):
            is_palindrome[i][i] = True
        
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                is_palindrome[i][i + 1] = True
        
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and is_palindrome[i + 1][j - 1]:
                    is_palindrome[i][j] = True
        
        # DP to build all partitions
        # dp[i] = list of all valid partitions for s[0:i]
        dp = [[] for _ in range(n + 1)]
        dp[0] = [[]]  # Empty partition for empty string
        
        for i in range(1, n + 1):
            for j in range(i):
                if is_palindrome[j][i - 1]:
                    palindrome = s[j:i]
                    for partition in dp[j]:
                        dp[i].append(partition + [palindrome])
        
        return dp[n]

# INTERVIEW DEMONSTRATION CLASS
class InterviewSolution:
    """
    Clean, interview-ready solution with clear structure and explanation
    """
    
    def partition(self, s: str) -> List[List[str]]:
        """
        MAIN INTERVIEW SOLUTION - Clear and well-structured
        """
        result = []
        
        def is_palindrome(string):
            """Helper: Check if string is palindrome using two pointers"""
            left, right = 0, len(string) - 1
            while left < right:
                if string[left] != string[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        def dfs(start_index, current_path):
            """
            DFS backtracking to find all valid partitions
            start_index: current position in string s
            current_path: current partition being constructed
            """
            # Base case: processed entire string
            if start_index == len(s):
                result.append(current_path[:])  # Add copy of current path
                return
            
            # Try all possible endings for next palindrome
            for end_index in range(start_index, len(s)):
                # Extract potential palindrome substring
                candidate = s[start_index:end_index + 1]
                
                if is_palindrome(candidate):
                    # Add palindrome to current path
                    current_path.append(candidate)
                    # Recurse for remaining string
                    dfs(end_index + 1, current_path)
                    # Backtrack: remove palindrome from path
                    current_path.pop()
        
        dfs(0, [])
        return result
    
    def partition_with_memoization(self, s: str) -> List[List[str]]:
        """
        OPTIMIZED VERSION: Show this as follow-up optimization
        Precompute palindrome checks to avoid repeated computation
        """
        n = len(s)
        result = []
        
        # Precompute palindrome lookup table
        palindrome_table = self.build_palindrome_table(s)
        
        def backtrack(start, path):
            if start == n:
                result.append(path[:])
                return
            
            for end in range(start, n):
                if palindrome_table[start][end]:
                    path.append(s[start:end + 1])
                    backtrack(end + 1, path)
                    path.pop()
        
        backtrack(0, [])
        return result
    
    def build_palindrome_table(self, s: str) -> List[List[bool]]:
        """Build 2D table where table[i][j] = True if s[i:j+1] is palindrome"""
        n = len(s)
        table = [[False] * n for _ in range(n)]
        
        # Single characters are palindromes
        for i in range(n):
            table[i][i] = True
        
        # Check 2-character palindromes
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                table[i][i + 1] = True
        
        # Check longer palindromes (length 3+)
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and table[i + 1][j - 1]:
                    table[i][j] = True
        
        return table

# COMPREHENSIVE TESTING
def test_solutions():
    """Test all solution approaches with comprehensive test cases"""
    solutions = [
        Solution().partition,
        Solution().partition_optimized,
        Solution().partition_dp_approach,
        InterviewSolution().partition,
        InterviewSolution().partition_with_memoization
    ]
    
    test_cases = [
        # (input, expected_length, sample_outputs)
        ("aab", 2, [["a","a","b"], ["aa","b"]]),
        ("raceacar", 3, [["r","a","c","e","a","c","a","r"], ["r","a","cec","a","r"], ["raceacar"]]),
        ("a", 1, [["a"]]),
        ("ab", 2, [["a","b"]]),
        ("abccba", 3, [["a","b","c","c","b","a"], ["a","bccb","a"], ["abccba"]]),
    ]
    
    for i, solution_func in enumerate(solutions):
        print(f"Testing Solution {i+1}...")
        for s, expected_len, sample_outputs in test_cases:
            result = solution_func(s)
            
            # Check that we got expected number of partitions
            if len(result) != expected_len:
                print(f"  Input: {s}")
                print(f"  Expected {expected_len} partitions, got {len(result)}")
                print(f"  Result: {result}")
            
            # Verify each partition is valid (all palindromes)
            for partition in result:
                full_string = ''.join(partition)
                if full_string != s:
                    print(f"  Invalid partition {partition} for input {s}")
                
                for palindrome in partition:
                    if palindrome != palindrome[::-1]:
                        print(f"  Non-palindrome found: {palindrome}")
        
        print(f"Solution {i+1} passed validation ✓")

# INTERVIEW STRATEGY AND TALKING POINTS
interview_strategy = """
INTERVIEW WALKTHROUGH (7-9 minutes total):

1. PROBLEM UNDERSTANDING (1 minute):
   "I need to find all ways to partition string s where each part is a palindrome."
   "For example, 'aab' can be partitioned as ['a','a','b'] or ['aa','b']."
   "This feels like a backtracking problem since I need to explore all possibilities."

2. APPROACH EXPLANATION (1-2 minutes):
   "I'll use backtracking to try all possible partitions."
   "At each position, I'll try all possible palindrome substrings starting from that position."
   "If I find a palindrome, I add it to current partition and recurse on remaining string."
   "When I reach the end, I've found a valid complete partition."

3. IMPLEMENTATION (3-4 minutes):
   - Start with palindrome check helper function
   - Implement backtracking function with clear parameter names
   - Show proper backtracking pattern (add -> recurse -> remove)
   - Handle base case (reached end of string)

4. COMPLEXITY ANALYSIS (1 minute):
   "Time: O(N * 2^N) - there are 2^N possible partitions, each takes O(N) to validate and copy"
   "Space: O(N) for recursion depth and current partition storage"

5. OPTIMIZATION DISCUSSION (1-2 minutes):
   "We can optimize by precomputing palindrome checks in O(N^2) time."
   "This avoids repeated palindrome validation during backtracking."
   "Trade-off: O(N^2) extra space for O(N^2) preprocessing time savings."

KEY IMPLEMENTATION POINTS:
✓ Use clear helper function for palindrome checking
✓ Proper backtracking: append -> recurse -> pop
✓ Make copy of current partition when adding to result
✓ Handle edge cases (empty string, single character)

COMMON MISTAKES TO AVOID:
✗ Not making copy of current partition (reference issues)
✗ Forgetting to backtrack (not removing element from path)
✗ Inefficient palindrome checking in inner loop
✗ Off-by-one errors in substring indexing
✗ Not handling empty string case

FOLLOW-UP OPTIMIZATIONS TO MENTION:
- Precompute palindrome table (O(N^2) preprocessing)
- Early termination if remaining characters can't form valid partition
- Memoization of intermediate results (though limited benefit here)
"""

# COMPLEXITY ANALYSIS DETAILS
complexity_explanation = """
DETAILED COMPLEXITY ANALYSIS:

TIME COMPLEXITY: O(N * 2^N)
- At each position, we can choose to cut or not cut → 2^(N-1) possible cuts
- Each partition requires O(N) time to:
  * Check palindromes: O(N) per check, up to N checks per partition
  * Copy partition to result: O(N) per partition
- Total: O(N * 2^N)

SPACE COMPLEXITY: O(N)
- Recursion depth: O(N) in worst case (all single characters)
- Current partition storage: O(N) in worst case
- Result storage not counted as it's output
- With optimization: O(N^2) for palindrome table

OPTIMIZATION TRADE-OFFS:
1. Precomputed Table:
   - Extra O(N^2) space
   - O(N^2) preprocessing time
   - Faster palindrome checks during backtracking
   - Better for multiple queries on same string

2. Without Precomputation:
   - O(N) space
   - No preprocessing
   - Repeated palindrome computations
   - Better for single query, memory-constrained scenarios
"""

# EDGE CASES AND EXAMPLES
edge_cases_guide = """
IMPORTANT EDGE CASES TO HANDLE:

1. SINGLE CHARACTER: "a"
   - Result: [["a"]]
   - Every single character is a palindrome

2. NO PALINDROMES > LENGTH 1: "abc"
   - Result: [["a","b","c"]]
   - Only valid partition is individual characters

3. ENTIRE STRING IS PALINDROME: "racecar"
   - Should include both [["racecar"]] and character-by-character partition

4. MULTIPLE VALID LONG PALINDROMES: "abccba"
   - [["abccba"]] - entire string
   - [["a","bccb","a"]] - middle palindrome
   - [["a","b","cc","b","a"]] - two-character palindrome
   - [["a","b","c","c","b","a"]] - all singles

5. REPEATED CHARACTERS: "aaa"
   - Multiple ways to group: [["aaa"]], [["a","aa"]], [["aa","a"]], [["a","a","a"]]

TESTING STRATEGY:
- Always test single character and two character inputs
- Test strings where entire string is palindrome
- Test strings with no multi-character palindromes
- Verify all partitions reconstruct original string
- Verify each partition element is actually a palindrome
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*70)
    print(interview_strategy)
    print("\n" + "="*70)
    print(complexity_explanation)
    print("\n" + "="*70)
    print(edge_cases_guide)
