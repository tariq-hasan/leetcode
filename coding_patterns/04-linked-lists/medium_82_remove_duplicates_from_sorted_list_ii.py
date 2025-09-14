# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteDuplicates(self, head):
        """
        DUMMY NODE + TWO POINTER SOLUTION (OPTIMAL FOR INTERVIEWS)
        
        Key Insight: Use dummy node + prev pointer to handle edge cases
        - Dummy node helps when head needs to be removed
        - prev pointer tracks the last "clean" node
        - Skip entire sequences of duplicates
        
        Algorithm:
        1. Use dummy node to simplify edge case handling
        2. Track prev (last confirmed unique node) and curr (scanning pointer)
        3. When duplicates found, skip entire duplicate sequence
        4. Only connect prev to curr when curr is confirmed unique
        
        Time: O(n) - single pass through the list
        Space: O(1) - only use constant extra pointers
        """
        # Dummy node to handle edge case of removing head
        dummy = ListNode(0)
        dummy.next = head
        
        # prev: last confirmed non-duplicate node
        # curr: current node being examined
        prev = dummy
        curr = head
        
        while curr:
            # Check if current node has duplicates
            if curr.next and curr.val == curr.next.val:
                # Skip all nodes with this duplicate value
                duplicate_val = curr.val
                while curr and curr.val == duplicate_val:
                    curr = curr.next
                
                # Connect prev to the node after all duplicates
                prev.next = curr
            else:
                # Current node is unique, move prev forward
                prev = curr
                curr = curr.next
        
        return dummy.next

class SolutionIterative:
    def deleteDuplicates(self, head):
        """
        ALTERNATIVE ITERATIVE APPROACH
        
        Similar logic but different pointer management
        Focus on identifying and removing duplicate sequences
        """
        if not head or not head.next:
            return head
        
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        
        while head:
            # If duplicates found
            if head.next and head.val == head.next.val:
                # Find the end of duplicate sequence
                val = head.val
                while head and head.val == val:
                    head = head.next
                
                # Skip the entire duplicate sequence
                prev.next = head
            else:
                # No duplicate, move prev forward
                prev = head
                head = head.next
        
        return dummy.next

class SolutionRecursive:
    def deleteDuplicates(self, head):
        """
        RECURSIVE SOLUTION (ELEGANT BUT USES STACK SPACE)
        
        Recursive thinking:
        - If current node has duplicates, skip all and recurse on rest
        - If current node is unique, keep it and recurse on rest
        
        Time: O(n) - visit each node once
        Space: O(n) - recursion stack in worst case
        """
        if not head or not head.next:
            return head
        
        # If current node has duplicates
        if head.next and head.val == head.next.val:
            # Skip all nodes with this value
            val = head.val
            while head and head.val == val:
                head = head.next
            
            # Recursively process the rest
            return self.deleteDuplicates(head)
        else:
            # Current node is unique, keep it
            head.next = self.deleteDuplicates(head.next)
            return head

class SolutionWithCounting:
    def deleteDuplicates(self, head):
        """
        COUNTING APPROACH (LESS OPTIMAL BUT INTUITIVE)
        
        Two passes:
        1. Count frequency of each value
        2. Remove nodes with frequency > 1
        
        Time: O(n) - two passes
        Space: O(n) - store counts in dictionary
        """
        if not head:
            return None
        
        # First pass: count frequencies
        counts = {}
        current = head
        while current:
            counts[current.val] = counts.get(current.val, 0) + 1
            current = current.next
        
        # Second pass: remove nodes with count > 1
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        current = head
        
        while current:
            if counts[current.val] > 1:
                # Skip this node
                prev.next = current.next
            else:
                # Keep this node
                prev = current
            current = current.next
        
        return dummy.next

class SolutionWithVisualization:
    def deleteDuplicatesVisual(self, head):
        """
        SOLUTION WITH STEP-BY-STEP VISUALIZATION
        Helps understand the algorithm by showing each step
        """
        print("Starting duplicate removal process...")
        
        if not head:
            print("Empty list")
            return None
        
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        curr = head
        
        step = 0
        
        while curr:
            step += 1
            current_list = self.list_to_string(dummy.next)
            print(f"Step {step}: Current list: {current_list}")
            print(f"         prev at {prev.val if prev != dummy else 'dummy'}, curr at {curr.val}")
            
            if curr.next and curr.val == curr.next.val:
                duplicate_val = curr.val
                print(f"         Found duplicates with value {duplicate_val}")
                
                # Skip all duplicates
                while curr and curr.val == duplicate_val:
                    print(f"         Skipping node {curr.val}")
                    curr = curr.next
                
                print(f"         Connecting prev to {curr.val if curr else 'None'}")
                prev.next = curr
            else:
                print(f"         Node {curr.val} is unique, moving prev forward")
                prev = curr
                curr = curr.next
        
        final_list = self.list_to_string(dummy.next)
        print(f"Final result: {final_list}")
        return dummy.next
    
    def list_to_string(self, head):
        """Helper to convert list to string for visualization"""
        if not head:
            return "Empty"
        
        values = []
        current = head
        while current and len(values) < 10:  # Prevent infinite loops
            values.append(str(current.val))
            current = current.next
        
        return " -> ".join(values)

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
    recursive_solution = SolutionRecursive()
    counting_solution = SolutionWithCounting()
    
    # Test case 1: [1,2,3,3,4,4,5] -> [1,2,5]
    print("=== Test Case 1: [1,2,3,3,4,4,5] ===")
    head1 = create_linked_list([1, 2, 3, 3, 4, 4, 5])
    print_list(head1, "Original")
    
    result1 = solution.deleteDuplicates(head1)
    print_list(result1, "After removal (iterative)")
    
    # Test recursive approach
    head1_rec = create_linked_list([1, 2, 3, 3, 4, 4, 5])
    result1_rec = recursive_solution.deleteDuplicates(head1_rec)
    print_list(result1_rec, "After removal (recursive)")
    
    # Test case 2: [1,1,1,2,3] -> [2,3]
    print("\n=== Test Case 2: [1,1,1,2,3] ===")
    head2 = create_linked_list([1, 1, 1, 2, 3])
    print_list(head2, "Original")
    
    result2 = solution.deleteDuplicates(head2)
    print_list(result2, "After removal")
    
    # Test case 3: [1,1,2,2] -> []
    print("\n=== Test Case 3: [1,1,2,2] ===")
    head3 = create_linked_list([1, 1, 2, 2])
    print_list(head3, "Original")
    
    result3 = solution.deleteDuplicates(head3)
    print_list(result3, "After removal")
    
    # Test case 4: [1,2,3] -> [1,2,3] (no duplicates)
    print("\n=== Test Case 4: [1,2,3] ===")
    head4 = create_linked_list([1, 2, 3])
    print_list(head4, "Original")
    
    result4 = solution.deleteDuplicates(head4)
    print_list(result4, "After removal")
    
    # Test case 5: [1,1] -> []
    print("\n=== Test Case 5: [1,1] ===")
    head5 = create_linked_list([1, 1])
    print_list(head5, "Original")
    
    result5 = solution.deleteDuplicates(head5)
    print_list(result5, "After removal")
    
    # Visual demonstration
    print("\n=== Visual Demonstration ===")
    visual_solution = SolutionWithVisualization()
    head_visual = create_linked_list([1, 2, 3, 3, 4, 4, 5])
    visual_result = visual_solution.deleteDuplicatesVisual(head_visual)

"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   "Remove ALL nodes that have duplicates, not just extra copies"
   "Different from problem 83 which keeps one copy of each duplicate"
   "If a value appears multiple times, remove ALL occurrences"

2. KEY INSIGHTS:
   - Need dummy node because head might be removed
   - Track 'prev' pointer to maintain connection to clean nodes
   - When duplicates found, skip entire sequence
   - Only advance 'prev' when current node is confirmed unique

3. ALGORITHM WALKTHROUGH:
   [1,2,3,3,4,4,5]
   
   dummy -> 1 -> 2 -> 3 -> 3 -> 4 -> 4 -> 5
   prev=dummy, curr=1
   
   Step 1: 1 is unique, prev=1, curr=2
   Step 2: 2 is unique, prev=2, curr=3
   Step 3: 3 has duplicates, skip all 3's, prev.next=4
   Step 4: 4 has duplicates, skip all 4's, prev.next=5
   Step 5: 5 is unique, prev=5, curr=None
   
   Result: dummy -> 1 -> 2 -> 5

4. CRITICAL EDGE CASES:
   - All nodes are duplicates → return empty list
   - Head nodes are duplicates → dummy node handles this
   - No duplicates → return original list
   - Single node → return as is

5. DUMMY NODE IMPORTANCE:
   "Without dummy node, removing head becomes complex"
   "Dummy provides consistent starting point for prev pointer"
   "Simplifies logic for all edge cases"

6. ALTERNATIVE APPROACHES:
   - Recursive: Elegant but O(n) space
   - Counting: Two-pass with hash map
   - All have same time complexity but different space/passes

7. COMPLEXITY ANALYSIS:
   - Time: O(n) - single pass through list
   - Space: O(1) - only constant extra pointers

8. COMMON MISTAKES:
   - Trying to modify nodes instead of skipping them
   - Not using dummy node (complex head handling)
   - Advancing prev pointer too early
   - Not skipping entire duplicate sequences

9. DIFFERENCE FROM PROBLEM 83:
   Problem 83: [1,1,2,3,3] → [1,2,3] (keep one of each)
   Problem 82: [1,1,2,3,3] → [2] (remove ALL duplicates)

10. FOLLOW-UP QUESTIONS:
    - "What if list wasn't sorted?" → Would need different approach
    - "Remove duplicates but keep one copy?" → That's problem 83
    - "What about doubly-linked lists?" → Similar logic, easier bookkeeping
    - "Space complexity optimization?" → Already O(1) with iterative approach

11. IMPLEMENTATION TIPS:
    - Use dummy node pattern for head modification problems
    - Track two pointers: prev (safe) and curr (exploring)
    - Skip entire sequences, don't try to modify individual nodes
    - Test with edge cases: all duplicates, no duplicates, single node
"""
