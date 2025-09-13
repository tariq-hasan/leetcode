# Definition for singly-linked list
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head):
        """
        FLOYD'S CYCLE DETECTION (TWO POINTERS) - PREFERRED SOLUTION
        
        Approach: Tortoise and Hare Algorithm
        - Slow pointer moves 1 step at a time
        - Fast pointer moves 2 steps at a time
        - If there's a cycle, fast will eventually meet slow
        - If no cycle, fast will reach the end (None)
        
        Why it works:
        - In a cycle, fast pointer gains 1 step on slow pointer each iteration
        - Eventually fast will "lap" slow and they'll meet
        
        Time: O(n) - at most n steps for fast pointer to meet slow
        Space: O(1) - only use two pointers
        """
        if not head or not head.next:
            return False
        
        slow = head
        fast = head
        
        # Move pointers until they meet or fast reaches end
        while fast and fast.next:
            slow = slow.next        # Move 1 step
            fast = fast.next.next   # Move 2 steps
            
            # If they meet, there's a cycle
            if slow == fast:
                return True
        
        # Fast reached end, no cycle
        return False

class SolutionHashSet:
    def hasCycle(self, head):
        """
        HASH SET SOLUTION (BRUTE FORCE BUT INTUITIVE)
        
        Approach: Track visited nodes
        - Store each visited node in a hash set
        - If we encounter a node we've seen before, there's a cycle
        - If we reach the end, no cycle
        
        Time: O(n) - visit each node once
        Space: O(n) - store up to n nodes in hash set
        """
        visited = set()
        current = head
        
        while current:
            # If we've seen this node before, there's a cycle
            if current in visited:
                return True
            
            # Mark this node as visited
            visited.add(current)
            current = current.next
        
        # Reached end without revisiting any node
        return False

class SolutionModification:
    def hasCycle(self, head):
        """
        NODE MODIFICATION SOLUTION (DESTRUCTIVE)
        
        WARNING: This modifies the original list structure!
        Only use if explicitly allowed by interviewer.
        
        Approach: Mark visited nodes by modifying them
        - Change each node's next to point to a sentinel value
        - If we encounter the sentinel, there's a cycle
        
        Time: O(n)
        Space: O(1)
        """
        if not head:
            return False
        
        sentinel = ListNode(-999999)  # Unique marker
        
        while head:
            if head.next == sentinel:
                return True
            
            next_node = head.next
            head.next = sentinel
            head = next_node
        
        return False

# Advanced: Find the start of the cycle (LeetCode 142)
class SolutionFindCycleStart:
    def detectCycle(self, head):
        """
        FIND CYCLE START POSITION (COMMON FOLLOW-UP)
        
        Algorithm:
        1. Use Floyd's algorithm to detect cycle
        2. If cycle found, place one pointer at head, keep other at meeting point
        3. Move both one step at a time until they meet
        4. Meeting point is the start of the cycle
        
        Mathematical proof:
        - Distance from head to cycle start: a
        - Distance from cycle start to meeting point: b
        - Cycle length: c
        - When they meet: slow traveled a+b, fast traveled a+b+c
        - Since fast = 2*slow: a+b+c = 2(a+b) → c = a+b → a = c-b
        """
        if not head or not head.next:
            return None
        
        # Phase 1: Detect if cycle exists
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None  # No cycle
        
        # Phase 2: Find cycle start
        # Move one pointer to head, keep other at meeting point
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow  # This is the start of the cycle

class SolutionCycleLength:
    def getCycleLength(self, head):
        """
        FIND CYCLE LENGTH (ANOTHER FOLLOW-UP)
        """
        if not head or not head.next:
            return 0
        
        # First detect cycle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return 0  # No cycle
        
        # Count cycle length
        length = 1
        current = slow.next
        while current != slow:
            current = current.next
            length += 1
        
        return length

# Test utilities
def create_cycle_list(values, cycle_pos):
    """
    Create a linked list with cycle
    cycle_pos: index where cycle starts (-1 for no cycle)
    """
    if not values:
        return None
    
    # Create nodes
    nodes = [ListNode(val) for val in values]
    
    # Link nodes
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if specified
    if cycle_pos >= 0:
        nodes[-1].next = nodes[cycle_pos]
    
    return nodes[0]

# Test all solutions
if __name__ == "__main__":
    solution = Solution()
    hash_solution = SolutionHashSet()
    cycle_detector = SolutionFindCycleStart()
    
    # Test case 1: [3,2,0,-4] with cycle at position 1
    print("=== Test Case 1: [3,2,0,-4] with cycle at pos 1 ===")
    head1 = create_cycle_list([3, 2, 0, -4], 1)
    print(f"Two Pointers: {solution.hasCycle(head1)}")
    
    # Recreate for hash set test (since we can't reuse after modification)
    head1_hash = create_cycle_list([3, 2, 0, -4], 1)
    print(f"Hash Set: {hash_solution.hasCycle(head1_hash)}")
    
    # Test cycle start detection
    head1_start = create_cycle_list([3, 2, 0, -4], 1)
    cycle_start = cycle_detector.detectCycle(head1_start)
    print(f"Cycle starts at node with value: {cycle_start.val if cycle_start else None}")
    
    # Test case 2: [1,2] with cycle at position 0
    print("\n=== Test Case 2: [1,2] with cycle at pos 0 ===")
    head2 = create_cycle_list([1, 2], 0)
    print(f"Has Cycle: {solution.hasCycle(head2)}")
    
    # Test case 3: [1] with no cycle
    print("\n=== Test Case 3: [1] with no cycle ===")
    head3 = create_cycle_list([1], -1)
    print(f"Has Cycle: {solution.hasCycle(head3)}")
    
    # Test case 4: Empty list
    print("\n=== Test Case 4: Empty list ===")
    head4 = None
    print(f"Has Cycle: {solution.hasCycle(head4)}")

"""
INTERVIEW TALKING POINTS:

1. ALGORITHM CHOICE:
   - Two pointers (Floyd's) is optimal: O(1) space
   - Hash set is intuitive but uses O(n) space
   - Always mention both approaches and their trade-offs

2. FLOYD'S ALGORITHM INTUITION:
   - Think of it as a race track
   - Slow runner (1 step) vs Fast runner (2 steps)
   - If there's a loop, fast will eventually lap slow
   - If no loop, fast reaches the finish line (null)

3. WHY FLOYD'S WORKS:
   - In each iteration, gap between fast and slow decreases by 1
   - If cycle length is C, they'll meet within C iterations after slow enters cycle
   - Mathematical proof ensures they will meet, not just pass each other

4. EDGE CASES:
   - Empty list → False
   - Single node → False (no self-loop in this problem)
   - Two nodes with cycle → True
   - No cycle → False

5. STEP-BY-STEP WALKTHROUGH:
   List: 3 -> 2 -> 0 -> 4
                  ^         |
                  |_________|
   
   Initial: slow=3, fast=3
   Step 1:  slow=2, fast=0
   Step 2:  slow=0, fast=2
   Step 3:  slow=4, fast=4  ← They meet! Cycle detected

6. COMPLEXITY ANALYSIS:
   - Two Pointers: O(n) time, O(1) space ✅
   - Hash Set: O(n) time, O(n) space
   - Both are correct, but two pointers is preferred

7. FOLLOW-UP QUESTIONS:
   - "Find where the cycle starts?" → Floyd's + math
   - "Find the length of the cycle?" → Count after detection
   - "Remove the cycle?" → Find start, break the link
   - "What if nodes could have duplicate values?" → Same algorithm works

8. COMMON MISTAKES:
   - Not checking for null pointers (fast.next)
   - Starting slow and fast at different positions
   - Forgetting edge cases (empty list, single node)
   - Not understanding why the algorithm works mathematically
"""
