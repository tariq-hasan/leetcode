# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head, n):
        """
        TWO-POINTER ONE-PASS SOLUTION (OPTIMAL FOR INTERVIEWS)
        
        Key Insight: Use two pointers with n+1 gap to find the node before target
        - Fast pointer moves n+1 steps ahead
        - Then both pointers move together until fast reaches end
        - Slow pointer will be at the node BEFORE the target to remove
        - Use dummy node to handle edge case of removing first node
        
        Why n+1 gap?
        - We need slow to point to the node BEFORE the one to remove
        - If gap is n, slow points to the node to remove
        - If gap is n+1, slow points to the node before target
        
        Time: O(L) where L is length of list - single pass
        Space: O(1) - only use constant extra space
        """
        # Dummy node simplifies edge case handling
        dummy = ListNode(0)
        dummy.next = head
        
        # Initialize both pointers at dummy
        slow = dummy
        fast = dummy
        
        # Move fast pointer n+1 steps ahead
        # This creates a gap of n+1 between slow and fast
        for _ in range(n + 1):
            fast = fast.next
        
        # Move both pointers until fast reaches the end
        # When fast is None, slow will be at the node before target
        while fast:
            slow = slow.next
            fast = fast.next
        
        # Remove the nth node from end
        slow.next = slow.next.next
        
        # Return the head (skip dummy node)
        return dummy.next

class SolutionTwoPass:
    def removeNthFromEnd(self, head, n):
        """
        TWO-PASS SOLUTION (MORE INTUITIVE)
        
        Approach: Calculate length first, then find target
        1. First pass: calculate total length of list
        2. Second pass: find and remove the (length - n)th node from start
        
        Time: O(L) - two passes through the list
        Space: O(1) - only use a few variables
        """
        # Handle edge case
        if not head:
            return None
        
        # First pass: calculate length
        length = 0
        current = head
        while current:
            length += 1
            current = current.next
        
        # Edge case: removing the first node
        if length == n:
            return head.next
        
        # Second pass: find the node before target
        # Target is at position (length - n) from start (0-indexed)
        # So we need to stop at position (length - n - 1)
        current = head
        for _ in range(length - n - 1):
            current = current.next
        
        # Remove the target node
        current.next = current.next.next
        
        return head

class SolutionStack:
    def removeNthFromEnd(self, head, n):
        """
        STACK SOLUTION (ALTERNATIVE APPROACH)
        
        Approach: Use stack to track nodes, then pop n times
        - Push all nodes onto stack
        - Pop n times to get to the nth node from end
        - Remove that node by updating previous node's next pointer
        
        Time: O(L) - visit each node twice
        Space: O(L) - store all nodes in stack
        """
        if not head:
            return None
        
        # Push all nodes onto stack
        stack = []
        current = head
        while current:
            stack.append(current)
            current = current.next
        
        # Edge case: removing the first node
        if len(stack) == n:
            return head.next
        
        # Pop n times to get the nth node from end
        for _ in range(n):
            stack.pop()
        
        # The top of stack is now the node before target
        if stack:
            stack[-1].next = stack[-1].next.next
        
        return head

class SolutionRecursive:
    def removeNthFromEnd(self, head, n):
        """
        RECURSIVE SOLUTION (ELEGANT BUT USES STACK SPACE)
        
        Approach: Use recursion to count from end
        - Recursively traverse to the end
        - Count backwards while returning
        - Remove node when count equals n
        
        Time: O(L) - visit each node once
        Space: O(L) - recursion stack
        """
        def helper(node):
            if not node:
                return 0
            
            # Get count from rest of the list
            count = helper(node.next)
            
            # If this is the (n+1)th node from end, remove the next node
            if count == n:
                node.next = node.next.next
            
            return count + 1
        
        # Handle edge case: removing first node
        dummy = ListNode(0)
        dummy.next = head
        helper(dummy)
        
        return dummy.next

class SolutionWithValidation:
    def removeNthFromEnd(self, head, n):
        """
        SOLUTION WITH INPUT VALIDATION
        Shows good engineering practices for interviews
        """
        # Input validation
        if not head or n <= 0:
            return head
        
        # Quick check if n is larger than list length
        # This is optional but shows thoughtful programming
        temp = head
        length = 0
        while temp:
            length += 1
            temp = temp.next
        
        if n > length:
            return head  # or could raise exception
        
        # Use the standard two-pointer approach
        dummy = ListNode(0)
        dummy.next = head
        slow = fast = dummy
        
        # Move fast n+1 steps ahead
        for _ in range(n + 1):
            fast = fast.next
        
        # Move both until fast reaches end
        while fast:
            slow = slow.next
            fast = fast.next
        
        # Remove target node
        slow.next = slow.next.next
        
        return dummy.next

# Test utilities
def create_linked_list(values):
    """Create linked list from list of values"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def linked_list_to_list(head):
    """Convert linked list to Python list for easy viewing"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

def print_list(head, name="List"):
    """Print linked list in readable format"""
    values = linked_list_to_list(head)
    if values:
        print(f"{name}: {' -> '.join(map(str, values))}")
    else:
        print(f"{name}: Empty")

# Test all solutions
if __name__ == "__main__":
    solution = Solution()
    two_pass_solution = SolutionTwoPass()
    
    # Test case 1: [1,2,3,4,5], n = 2 (remove 4)
    print("=== Test Case 1: [1,2,3,4,5], remove 2nd from end ===")
    head1 = create_linked_list([1, 2, 3, 4, 5])
    print_list(head1, "Original")
    
    result1 = solution.removeNthFromEnd(head1, 2)
    print_list(result1, "After removal (two-pointer)")
    
    # Test two-pass approach
    head1_two = create_linked_list([1, 2, 3, 4, 5])
    result1_two = two_pass_solution.removeNthFromEnd(head1_two, 2)
    print_list(result1_two, "After removal (two-pass)")
    
    # Test case 2: [1], n = 1 (remove only node)
    print("\n=== Test Case 2: [1], remove 1st from end ===")
    head2 = create_linked_list([1])
    print_list(head2, "Original")
    
    result2 = solution.removeNthFromEnd(head2, 1)
    print_list(result2, "After removal")
    
    # Test case 3: [1,2], n = 1 (remove last node)
    print("\n=== Test Case 3: [1,2], remove 1st from end ===")
    head3 = create_linked_list([1, 2])
    print_list(head3, "Original")
    
    result3 = solution.removeNthFromEnd(head3, 1)
    print_list(result3, "After removal")
    
    # Test case 4: [1,2], n = 2 (remove first node)
    print("\n=== Test Case 4: [1,2], remove 2nd from end ===")
    head4 = create_linked_list([1, 2])
    print_list(head4, "Original")
    
    result4 = solution.removeNthFromEnd(head4, 2)
    print_list(result4, "After removal")
    
    # Test edge case: single node list
    print("\n=== Test Case 5: [5], remove 1st from end ===")
    head5 = create_linked_list([5])
    print_list(head5, "Original")
    
    result5 = solution.removeNthFromEnd(head5, 1)
    print_list(result5, "After removal")

"""
INTERVIEW TALKING POINTS:

1. PROBLEM ANALYSIS:
   "We need to remove the nth node from the END of the list"
   "Key challenge: we don't know the length in advance"
   "Need to handle edge case of removing the first node"

2. TWO-POINTER APPROACH (PREFERRED):
   "Use two pointers with a gap of n+1 positions"
   "Why n+1? We need slow to point to the node BEFORE the target"
   "Move fast pointer n+1 steps first, then move both together"

3. DUMMY NODE PATTERN:
   "Dummy node simplifies the edge case of removing first node"
   "Without dummy: need special handling for head removal"
   "With dummy: uniform logic for all removals"

4. STEP-BY-STEP WALKTHROUGH:
   List: [1,2,3,4,5], n=2 (remove 4)
   
   Initial: dummy->1->2->3->4->5, slow=dummy, fast=dummy
   Step 1: Move fast 3 positions: fast points to 3
   Step 2: Move both until fast reaches end:
           slow=1, fast=4
           slow=2, fast=5
           slow=3, fast=null
   Step 3: slow.next.next removes 4: 1->2->3->5

5. EDGE CASES:
   - Remove first node (n equals list length)
   - Single node list
   - Remove last node
   - Empty list (though constraints usually prevent this)

6. ALTERNATIVE APPROACHES:
   - Two-pass: Calculate length first, then find target
   - Stack: Push all nodes, pop n times
   - Recursive: Count backwards while returning

7. COMPLEXITY ANALYSIS:
   - Two-pointer: O(L) time, O(1) space ✅ (optimal)
   - Two-pass: O(L) time, O(1) space (but 2 passes)
   - Stack: O(L) time, O(L) space
   - Recursive: O(L) time, O(L) space (call stack)

8. WHY TWO-POINTER IS PREFERRED:
   - Single pass through the list
   - Constant extra space
   - Handles all edge cases elegantly with dummy node
   - Clean, readable code

9. COMMON MISTAKES:
   - Using gap of n instead of n+1 (points to wrong node)
   - Forgetting dummy node (complex first node handling)
   - Not handling edge case of removing first node
   - Off-by-one errors in counting

10. FOLLOW-UP QUESTIONS:
    - "What if n is invalid (> list length)?" → Add validation
    - "Remove nth node from start instead?" → Simpler problem
    - "Remove multiple nodes from end?" → Extend the algorithm
    - "What about doubly-linked lists?" → Easier with prev pointers
"""
