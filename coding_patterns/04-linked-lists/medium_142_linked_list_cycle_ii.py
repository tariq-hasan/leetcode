# Definition for singly-linked list
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def detectCycle(self, head):
        """
        FLOYD'S CYCLE DETECTION + MATHEMATICAL APPROACH (OPTIMAL)
        
        Two-Phase Algorithm:
        Phase 1: Detect if cycle exists (same as problem 141)
        Phase 2: Find the start of the cycle using mathematical insight
        
        Mathematical Proof:
        - Let a = distance from head to cycle start
        - Let b = distance from cycle start to meeting point
        - Let c = remaining distance in cycle (cycle_length = b + c)
        
        When pointers meet:
        - Slow traveled: a + b
        - Fast traveled: a + b + c (one full cycle more than slow)
        - Since fast moves 2x speed: 2(a + b) = a + b + c
        - Solving: a = c
        
        This means: distance from head to cycle start = remaining cycle distance
        
        Time: O(n) - two passes through the list
        Space: O(1) - only use constant extra pointers
        """
        if not head or not head.next:
            return None
        
        # Phase 1: Detect cycle using Floyd's algorithm
        slow = fast = head
        
        # Find meeting point
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                break  # Cycle detected
        else:
            return None  # No cycle found
        
        # Phase 2: Find cycle start
        # Key insight: distance from head to start = remaining cycle distance
        slow = head  # Reset slow to head
        # Keep fast at meeting point
        
        # Move both pointers one step at a time until they meet
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow  # This is the start of the cycle

class SolutionHashSet:
    def detectCycle(self, head):
        """
        HASH SET SOLUTION (BRUTE FORCE BUT INTUITIVE)
        
        Approach: Track visited nodes with their order
        - Store each node in hash set as we visit
        - First node we've seen before is the cycle start
        
        Time: O(n) - visit each node once
        Space: O(n) - store up to n nodes in hash set
        """
        visited = set()
        current = head
        
        while current:
            if current in visited:
                return current  # First revisited node is cycle start
            
            visited.add(current)
            current = current.next
        
        return None  # No cycle

class SolutionWithDetails:
    def detectCycleWithInfo(self, head):
        """
        EXTENDED SOLUTION: Returns cycle start, length, and meeting point
        Useful for understanding the algorithm deeply
        """
        if not head or not head.next:
            return {"start": None, "length": 0, "meeting_point": None}
        
        # Phase 1: Detect cycle
        slow = fast = head
        meeting_point = None
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                meeting_point = slow
                break
        else:
            return {"start": None, "length": 0, "meeting_point": None}
        
        # Phase 2: Find cycle start
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        cycle_start = slow
        
        # Phase 3: Calculate cycle length
        cycle_length = 1
        current = cycle_start.next
        while current != cycle_start:
            current = current.next
            cycle_length += 1
        
        return {
            "start": cycle_start,
            "length": cycle_length,
            "meeting_point": meeting_point
        }

# Visual explanation helper
class SolutionWithVisualization:
    def detectCycleVisual(self, head):
        """
        SOLUTION WITH STEP-BY-STEP VISUALIZATION
        Helps understand the algorithm by showing each step
        """
        if not head or not head.next:
            print("Empty list or single node - no cycle possible")
            return None
        
        print("Phase 1: Detecting cycle...")
        slow = fast = head
        step = 0
        
        while fast and fast.next:
            print(f"Step {step}: slow at {slow.val}, fast at {fast.val}")
            slow = slow.next
            fast = fast.next.next
            step += 1
            
            if slow == fast:
                print(f"Cycle detected! Meeting point: {slow.val}")
                break
        else:
            print("No cycle found")
            return None
        
        print("\nPhase 2: Finding cycle start...")
        print("Mathematical insight: distance from head to start = remaining cycle distance")
        
        slow = head
        step = 0
        print(f"Reset: slow at head ({slow.val}), fast at meeting point ({fast.val})")
        
        while slow != fast:
            print(f"Step {step}: slow at {slow.val}, fast at {fast.val}")
            slow = slow.next
            fast = fast.next
            step += 1
        
        print(f"Found cycle start at: {slow.val}")
        return slow

# Test utilities
def create_cycle_list(values, cycle_pos):
    """Create a linked list with cycle at specified position"""
    if not values:
        return None
    
    nodes = [ListNode(val) for val in values]
    
    # Link nodes
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if specified
    if cycle_pos >= 0 and cycle_pos < len(nodes):
        nodes[-1].next = nodes[cycle_pos]
    
    return nodes[0]

def print_cycle_info(head, solution_result):
    """Print detailed information about the cycle"""
    if solution_result is None:
        print("No cycle detected")
    else:
        print(f"Cycle starts at node with value: {solution_result.val}")

# Test all solutions
if __name__ == "__main__":
    solution = Solution()
    hash_solution = SolutionHashSet()
    detailed_solution = SolutionWithDetails()
    
    # Test case 1: [3,2,0,-4] with cycle starting at position 1 (value 2)
    print("=== Test Case 1: [3,2,0,-4] with cycle at pos 1 ===")
    head1 = create_cycle_list([3, 2, 0, -4], 1)
    
    result1 = solution.detectCycle(head1)
    print(f"Floyd's Algorithm: Cycle starts at {result1.val if result1 else None}")
    
    # Test with hash set
    head1_hash = create_cycle_list([3, 2, 0, -4], 1)
    result1_hash = hash_solution.detectCycle(head1_hash)
    print(f"Hash Set: Cycle starts at {result1_hash.val if result1_hash else None}")
    
    # Test with detailed info
    head1_detail = create_cycle_list([3, 2, 0, -4], 1)
    detail_result = detailed_solution.detectCycleWithInfo(head1_detail)
    print(f"Detailed Analysis:")
    print(f"  Start: {detail_result['start'].val if detail_result['start'] else None}")
    print(f"  Cycle Length: {detail_result['length']}")
    print(f"  Meeting Point: {detail_result['meeting_point'].val if detail_result['meeting_point'] else None}")
    
    # Test case 2: [1,2] with cycle at position 0
    print("\n=== Test Case 2: [1,2] with cycle at pos 0 ===")
    head2 = create_cycle_list([1, 2], 0)
    result2 = solution.detectCycle(head2)
    print(f"Cycle starts at: {result2.val if result2 else None}")
    
    # Test case 3: [1] with no cycle
    print("\n=== Test Case 3: [1] with no cycle ===")
    head3 = create_cycle_list([1], -1)
    result3 = solution.detectCycle(head3)
    print(f"Cycle starts at: {result3.val if result3 else None}")
    
    # Visual demonstration
    print("\n=== Visual Demonstration ===")
    visual_solution = SolutionWithVisualization()
    head_visual = create_cycle_list([3, 2, 0, -4], 1)
    visual_result = visual_solution.detectCycleVisual(head_visual)

"""
INTERVIEW TALKING POINTS:

1. PROBLEM BREAKDOWN:
   "This builds on cycle detection (problem 141) but now we need to find WHERE the cycle starts"
   "Two-phase approach: detect cycle, then find start point"

2. MATHEMATICAL INSIGHT (CRITICAL TO EXPLAIN):
   "Let me draw this out and prove why the algorithm works..."
   
   Head -> ... -> CycleStart -> ... -> MeetingPoint -> ... -> back to CycleStart
           a           b                    c
   
   - Distance head to cycle start: a
   - Distance cycle start to meeting: b  
   - Remaining cycle distance: c
   - When they meet: slow = a+b, fast = a+b+c (fast went one extra cycle)
   - Since fast = 2×slow: a+b+c = 2(a+b) → c = a+b → a = c
   
   "So distance from head to start equals remaining cycle distance!"

3. ALGORITHM PHASES:
   Phase 1: Standard Floyd's detection (same as problem 141)
   Phase 2: Reset slow to head, move both one step until they meet

4. WHY THIS WORKS:
   "After reset, slow needs 'a' steps to reach cycle start"
   "Fast needs 'c' steps to complete the cycle and reach start"
   "Since a = c, they meet exactly at the cycle start!"

5. EDGE CASES:
   - No cycle → return null
   - Single node → return null (no self-loop)
   - Cycle at head → return head
   - Multiple cycles → impossible in singly-linked list

6. COMPLEXITY ANALYSIS:
   - Time: O(n) - at most 2 passes through the list
   - Space: O(1) - only use a few pointers

7. ALTERNATIVE APPROACHES:
   - Hash set: O(n) space but more intuitive
   - Node modification: destructive but O(1) space

8. FOLLOW-UP VARIATIONS:
   - "Find cycle length?" → Count after finding start
   - "Remove the cycle?" → Find node before start, set next to null
   - "Multiple cycles?" → Not possible in singly-linked list
   - "Doubly-linked list?" → Same algorithm works

9. IMPLEMENTATION DETAILS:
   - Always check null pointers (fast.next)
   - Two separate while loops for two phases
   - Reset slow to head after detection
   - Both pointers move one step in phase 2

10. MATHEMATICAL PROOF IMPORTANCE:
    "Interviewers love this problem because it combines algorithms with mathematical reasoning"
    "The key insight a = c is what makes this elegant and optimal"
"""
