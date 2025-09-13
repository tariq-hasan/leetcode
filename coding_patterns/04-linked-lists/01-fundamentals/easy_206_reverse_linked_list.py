# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head):
        """
        ITERATIVE SOLUTION (PREFERRED FOR INTERVIEWS)
        
        Approach: Three-pointer technique
        - prev: points to previous node (starts as None)
        - curr: current node being processed
        - next_temp: temporarily stores next node to avoid losing it
        
        Time: O(n) - visit each node once
        Space: O(1) - only use constant extra space
        """
        prev = None
        curr = head
        
        while curr:
            # Store next node before we lose it
            next_temp = curr.next
            
            # Reverse the link
            curr.next = prev
            
            # Move pointers forward
            prev = curr
            curr = next_temp
        
        # prev is now the new head
        return prev

class SolutionRecursive:
    def reverseList(self, head):
        """
        RECURSIVE SOLUTION (ELEGANT BUT USES O(n) SPACE)
        
        Base case: empty list or single node
        Recursive case: reverse rest of list, then fix connections
        
        Time: O(n) - visit each node once
        Space: O(n) - recursion stack
        """
        # Base case: empty list or single node
        if not head or not head.next:
            return head
        
        # Recursively reverse the rest of the list
        new_head = self.reverseList(head.next)
        
        # Reverse the current connection
        # head.next is the last node of the reversed part
        head.next.next = head
        head.next = None
        
        return new_head

class SolutionStack:
    def reverseList(self, head):
        """
        STACK SOLUTION (INTUITIVE BUT USES EXTRA SPACE)
        
        Push all nodes onto stack, then pop to create reversed list
        
        Time: O(n) - two passes through the list
        Space: O(n) - stack storage
        """
        if not head:
            return None
        
        stack = []
        curr = head
        
        # Push all nodes onto stack
        while curr:
            stack.append(curr)
            curr = curr.next
        
        # Pop nodes to create reversed list
        new_head = stack.pop()
        curr = new_head
        
        while stack:
            curr.next = stack.pop()
            curr = curr.next
        
        curr.next = None  # Important: set last node's next to None
        return new_head

# Advanced: Reverse in groups of k (follow-up question)
class SolutionGroups:
    def reverseKGroup(self, head, k):
        """
        Advanced follow-up: Reverse nodes in groups of k
        """
        # Count nodes to see if we have k nodes left
        count = 0
        curr = head
        while curr and count < k:
            curr = curr.next
            count += 1
        
        # If we have k nodes, reverse them
        if count == k:
            # Reverse first k nodes
            curr = self.reverseKGroup(curr, k)  # Recursively reverse rest
            
            # Reverse current group
            while count > 0:
                next_temp = head.next
                head.next = curr
                curr = head
                head = next_temp
                count -= 1
            
            head = curr
        
        return head

# Utility functions for testing
def create_linked_list(values):
    """Create linked list from list of values"""
    if not values:
        return None
    
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def linked_list_to_list(head):
    """Convert linked list to Python list for easy viewing"""
    result = []
    curr = head
    while curr:
        result.append(curr.val)
        curr = curr.next
    return result

def print_list(head, name="List"):
    """Print linked list in readable format"""
    values = linked_list_to_list(head)
    print(f"{name}: {' -> '.join(map(str, values)) if values else 'Empty'}")

# Test all solutions
if __name__ == "__main__":
    # Test case 1: [1,2,3,4,5]
    print("=== Test Case 1: [1,2,3,4,5] ===")
    head1 = create_linked_list([1, 2, 3, 4, 5])
    print_list(head1, "Original")
    
    # Test iterative solution
    solution = Solution()
    reversed1 = solution.reverseList(head1)
    print_list(reversed1, "Reversed")
    
    # Test case 2: [1,2]
    print("\n=== Test Case 2: [1,2] ===")
    head2 = create_linked_list([1, 2])
    print_list(head2, "Original")
    
    solution_rec = SolutionRecursive()
    reversed2 = solution_rec.reverseList(head2)
    print_list(reversed2, "Reversed")
    
    # Test case 3: Single node [1]
    print("\n=== Test Case 3: [1] ===")
    head3 = create_linked_list([1])
    print_list(head3, "Original")
    
    solution_stack = SolutionStack()
    reversed3 = solution_stack.reverseList(head3)
    print_list(reversed3, "Reversed")
    
    # Test case 4: Empty list
    print("\n=== Test Case 4: Empty List ===")
    head4 = None
    print_list(head4, "Original")
    
    solution2 = Solution()
    reversed4 = solution2.reverseList(head4)
    print_list(reversed4, "Reversed")

"""
INTERVIEW TALKING POINTS:

1. APPROACH SELECTION:
   - Start with iterative (most common in interviews)
   - Mention recursive as alternative
   - Stack solution shows different thinking

2. KEY INSIGHTS:
   - Need to keep track of previous node to reverse links
   - Careful not to lose nodes when changing pointers
   - Three pointers: prev, curr, next_temp

3. STEP-BY-STEP WALKTHROUGH:
   Original: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
   Step 1:   NULL <- 1    2 -> 3 -> 4 -> 5 -> NULL
   Step 2:   NULL <- 1 <- 2    3 -> 4 -> 5 -> NULL
   Step 3:   NULL <- 1 <- 2 <- 3    4 -> 5 -> NULL
   Step 4:   NULL <- 1 <- 2 <- 3 <- 4    5 -> NULL
   Step 5:   NULL <- 1 <- 2 <- 3 <- 4 <- 5

4. EDGE CASES:
   - Empty list (return None)
   - Single node (return as is)
   - Two nodes (simple swap)

5. COMPLEXITY ANALYSIS:
   - Iterative: O(n) time, O(1) space ✅
   - Recursive: O(n) time, O(n) space (stack)
   - Stack: O(n) time, O(n) space

6. FOLLOW-UP QUESTIONS:
   - "Can you do it recursively?"
   - "Reverse in groups of k nodes?"
   - "Reverse between positions m and n?"
   - "How would you test this?"

7. IMPLEMENTATION TIPS:
   - Always handle edge cases first
   - Draw out the pointer movements
   - Test with multiple cases
   - Consider both iterative and recursive
"""
