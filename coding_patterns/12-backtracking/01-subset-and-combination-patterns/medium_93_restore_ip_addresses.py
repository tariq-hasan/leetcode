from typing import List

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        """
        Problem: Given string s containing digits, return all possible valid IP addresses
        that can be obtained from s. Do not reorder or remove digits.
        
        APPROACH 1: BACKTRACKING (Most Common Interview Solution)
        Time: O(3^4 * |s|) = O(81 * |s|) - at most 3 choices per segment, 4 segments
        Space: O(4) for recursion depth = O(1)
        
        This is the standard approach most interviewers expect.
        """
        result = []
        
        def is_valid_segment(segment):
            """Check if a segment is valid IP part (0-255, no leading zeros)"""
            if not segment or len(segment) > 3:
                return False
            
            # No leading zeros except for "0" itself
            if len(segment) > 1 and segment[0] == '0':
                return False
            
            # Must be between 0 and 255
            num = int(segment)
            return 0 <= num <= 255
        
        def backtrack(start_idx, segments):
            """
            start_idx: current position in string s
            segments: list of current IP segments being built
            """
            # Base case: if we have 4 segments and used all characters
            if len(segments) == 4:
                if start_idx == len(s):
                    result.append('.'.join(segments))
                return
            
            # Pruning: if we have 4 segments already or can't form remaining segments
            if len(segments) == 4 or start_idx >= len(s):
                return
            
            # Try segments of length 1, 2, and 3
            for length in range(1, 4):
                if start_idx + length > len(s):
                    break
                
                segment = s[start_idx:start_idx + length]
                
                if is_valid_segment(segment):
                    # Add this segment and recurse
                    segments.append(segment)
                    backtrack(start_idx + length, segments)
                    # Backtrack
                    segments.pop()
        
        backtrack(0, [])
        return result
    
    def restoreIpAddresses_iterative(self, s: str) -> List[str]:
        """
        APPROACH 2: ITERATIVE WITH TRIPLE NESTED LOOPS
        Time: O(1) - constant since we only have 3^4 = 81 possible combinations
        Space: O(1)
        
        More explicit about the 4-segment structure. Good for showing different thinking.
        """
        result = []
        n = len(s)
        
        # Early termination: IP needs 4-12 characters
        if n < 4 or n > 12:
            return result
        
        def is_valid(segment):
            if not segment or len(segment) > 3:
                return False
            if len(segment) > 1 and segment[0] == '0':
                return False
            return 0 <= int(segment) <= 255
        
        # Try all possible ways to split into 4 segments
        for i in range(1, min(4, n)):  # First segment end
            for j in range(i + 1, min(i + 4, n)):  # Second segment end
                for k in range(j + 1, min(j + 4, n)):  # Third segment end
                    # Fourth segment goes from k to end
                    if k < n and n - k <= 3:  # Fourth segment length check
                        seg1 = s[0:i]
                        seg2 = s[i:j]
                        seg3 = s[j:k]
                        seg4 = s[k:]
                        
                        if (is_valid(seg1) and is_valid(seg2) and 
                            is_valid(seg3) and is_valid(seg4)):
                            result.append(f"{seg1}.{seg2}.{seg3}.{seg4}")
        
        return result
    
    def restoreIpAddresses_optimized(self, s: str) -> List[str]:
        """
        APPROACH 3: OPTIMIZED BACKTRACKING (Best for interview)
        Time: O(1) - at most 3^4 combinations
        Space: O(1)
        
        Enhanced with better pruning and validation.
        """
        result = []
        n = len(s)
        
        # Early pruning: impossible cases
        if n < 4 or n > 12:
            return result
        
        def backtrack(start, path, segments_left):
            """
            start: current index in string
            path: current IP being built as list
            segments_left: how many more segments we need
            """
            # Pruning: impossible to form valid IP
            remaining_chars = n - start
            if remaining_chars < segments_left or remaining_chars > segments_left * 3:
                return
            
            # Base case: found valid IP
            if segments_left == 0:
                if start == n:
                    result.append('.'.join(path))
                return
            
            # Try different segment lengths (1, 2, 3)
            for length in range(1, 4):
                if start + length > n:
                    break
                
                segment = s[start:start + length]
                
                # Validate segment
                if length > 1 and segment[0] == '0':  # No leading zeros
                    continue
                if int(segment) > 255:  # Must be <= 255
                    continue
                
                # Recurse with this segment
                path.append(segment)
                backtrack(start + length, path, segments_left - 1)
                path.pop()
        
        backtrack(0, [], 4)
        return result

# INTERVIEW DEMONSTRATION CLASS
class InterviewSolution:
    """
    Clean, interview-ready solution with clear structure
    """
    
    def restoreIpAddresses(self, s: str) -> List[str]:
        """
        MAIN INTERVIEW SOLUTION - Clear and well-structured
        """
        result = []
        
        def is_valid_ip_segment(segment):
            """
            Validate IP segment:
            1. Length: 1-3 characters
            2. No leading zeros (except "0" itself)  
            3. Value: 0-255
            """
            if not segment or len(segment) > 3:
                return False
            
            if len(segment) > 1 and segment[0] == '0':
                return False
            
            return 0 <= int(segment) <= 255
        
        def dfs(index, current_segments):
            """
            DFS to build valid IP addresses
            index: current position in string s
            current_segments: segments built so far
            """
            # Found complete IP address
            if len(current_segments) == 4:
                if index == len(s):  # Used all characters
                    result.append('.'.join(current_segments))
                return
            
            # Pruning: can't form valid IP
            if len(current_segments) >= 4 or index >= len(s):
                return
            
            # Try segments of length 1, 2, 3
            for seg_len in range(1, 4):
                if index + seg_len > len(s):
                    break
                
                segment = s[index:index + seg_len]
                
                if is_valid_ip_segment(segment):
                    current_segments.append(segment)
                    dfs(index + seg_len, current_segments)
                    current_segments.pop()  # backtrack
        
        # Early termination for impossible cases
        if len(s) < 4 or len(s) > 12:
            return []
        
        dfs(0, [])
        return result

# TEST AND VALIDATION
def test_solutions():
    """Comprehensive test cases for interview validation"""
    solutions = [
        Solution().restoreIpAddresses,
        Solution().restoreIpAddresses_iterative,
        Solution().restoreIpAddresses_optimized,
        InterviewSolution().restoreIpAddresses
    ]
    
    test_cases = [
        # (input, expected_output_set for easy comparison)
        ("25525511135", {"255.255.11.135", "255.255.111.35"}),
        ("0000", {"0.0.0.0"}),
        ("101023", {"1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"}),
        ("1111", {"1.1.1.1"}),
        ("010010", {"0.10.0.10", "0.100.1.0"}),
        ("12345", set()),  # Too short for valid IP
        ("1234567890123", set()),  # Too long
    ]
    
    for i, solution_func in enumerate(solutions):
        print(f"Testing Solution {i+1}...")
        for s, expected in test_cases:
            result = set(solution_func(s))
            assert result == expected, f"Failed for input '{s}': got {result}, expected {expected}"
        print(f"Solution {i+1} passed all tests ✓")

# INTERVIEW TALKING POINTS AND STRATEGY
interview_guide = """
INTERVIEW WALKTHROUGH (6-8 minutes total):

1. PROBLEM UNDERSTANDING (1 minute):
   "I need to split a string into 4 parts that form a valid IP address."
   "Valid IP constraints: each part 0-255, no leading zeros except '0' itself."
   "I cannot reorder digits, only choose where to split."

2. APPROACH EXPLANATION (1 minute):
   "This is a classic backtracking problem."
   "I'll try all possible ways to split the string into 4 segments."
   "For each position, I can try segments of length 1, 2, or 3."
   "I'll validate each segment and backtrack if invalid."

3. IMPLEMENTATION STRATEGY (3 minutes):
   - Helper function to validate IP segments
   - Recursive function with backtracking
   - Base case: 4 segments formed, check if all characters used
   - Pruning: early termination for impossible cases

4. COMPLEXITY ANALYSIS (1 minute):
   "Time: O(3^4) = O(81) - constant since at most 3 choices per segment, 4 segments"
   "Space: O(4) = O(1) for recursion depth"
   "The constant factor makes this essentially O(1) time and space."

5. OPTIMIZATION DISCUSSION (1 minute):
   "Early pruning based on string length (must be 4-12 characters)"
   "Stop trying longer segments once we exceed 255"
   "Could use iterative approach with 3 nested loops"

KEY POINTS TO MENTION:
✓ Validate segments carefully (leading zeros, range 0-255)
✓ Backtracking pattern with proper cleanup
✓ Early termination/pruning for efficiency
✓ Handle edge cases (too short/long strings)

COMMON MISTAKES TO AVOID:
✗ Forgetting to check leading zeros
✗ Not validating segment length (max 3 digits)
✗ Not handling the "0" case properly
✗ Forgetting to backtrack (remove segment from path)
✗ Not checking if all characters are used

FOLLOW-UP QUESTIONS:
- "What if we wanted IPv6?" → Similar approach, different validation
- "How would you optimize further?" → Discuss iterative vs recursive trade-offs
- "What about invalid characters?" → Add character validation
"""

# COMMON EDGE CASES TO DISCUSS
edge_cases_explanation = """
CRITICAL EDGE CASES TO HANDLE:

1. Leading Zeros:
   - "01" is invalid (but "0" is valid)
   - "001" is invalid
   - Must check: len(segment) > 1 and segment[0] == '0'

2. Out of Range:
   - "256" is invalid (> 255)
   - Must check: int(segment) <= 255

3. String Length:
   - < 4 characters: impossible (need at least "1.1.1.1")
   - > 12 characters: impossible (max is "255.255.255.255")

4. Boundary Cases:
   - "0000" → "0.0.0.0" (valid)
   - "1111" → "1.1.1.1" (valid)
   - "12345" → multiple valid splits possible

5. Empty Segments:
   - Never generate empty segments in proper backtracking
   - But good to validate in helper function
"""

if __name__ == "__main__":
    test_solutions()
    print("\n" + "="*60)
    print(interview_guide)
    print("\n" + "="*60)
    print(edge_cases_explanation)
