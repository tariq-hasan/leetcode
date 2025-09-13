# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1, list2):
        """
        ITERATIVE SOLUTION WITH DUMMY NODE (PREFERRED FOR INTERVIEWS)
        
        Approach: Two-pointer technique with dummy node
        - Use dummy node to simplify edge case handling
        - Compare values and attach smaller node
        - Move pointer in the list we took from
        - Attach remaining nodes at the end
        
        Time: O(n + m) where n, m are lengths of the lists
        Space: O(1) - only use constant extra space
        """
        # Create dummy node to simplify code
        dummy = ListNode(0)
        current = dummy
        
        # Merge while both lists have nodes
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Attach remaining nodes (at most one list will have remaining nodes)
        current.next = list1 or list2
        
        # Return the merged list (skip dummy node)
        return dummy.next

class SolutionRecursive:
    def mergeTwoLists(self, list1, list2):
        """
        RECURSIVE SOLUTION (ELEGANT AND CLEAN)
        
        Base cases: if one list is empty, return the other
        Recursive case: choose smaller head, recursively merge rest
        
        Time: O(n + m) - visit each node once
        Space: O(n + m) - recursion stack depth
        """
        # Base cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Choose the smaller head and recursively merge the rest
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2

class SolutionWithoutDummy:
    def mergeTwoLists(self, list1, list2):
        """
        ITERATIVE WITHOUT DUMMY NODE (MORE COMPLEX EDGE HANDLING)
        
        Shows how dummy node simplifies the problem
        Need to handle the first node selection separately
        
        Time: O(n + m)
        Space: O(1)
        """
        # Handle edge cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Determine the head of merged list
        if list1.val <= list2.val:
            head = list1
            list1 = list1.next
        else:
            head = list2
            list2 = list2.next
        
        current = head
        
        # Merge the rest
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Attach remaining nodes
        current.next = list1 or list2
        
        return head

# Advanced: Merge k sorted lists (common follow-up)
class SolutionMergeK:
    def mergeKLists(self, lists):
        """
        FOLLOW-UP: Merge k sorted lists
        Using divide and conquer approach
        
        Time: O(N log k) where N is total number of nodes, k is number of lists
        Space: O(log k) for recursion stack
        """
        if not lists:
            return None
        
        def merge_two(l1, l2):
            dummy = ListNode(0)
            current = dummy
            
            while l1 and l2:
                if l1.val <= l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next
            
            current.next = l1 or l2
            return dummy.next
        
        # Divide and conquer
        while len(lists) > 1:
            merged_lists = []
            
            # Merge pairs of lists
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(merge_two(l1, l2))
            
            lists = merged_lists
        
        return lists[0]

# Utility functions for testing
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
    solution_rec = SolutionRecursive()
    
    # Test case 1: [1,2,4] and [1,3,4]
    print("=== Test Case 1: [1,2,4] and [1,3,4] ===")
    list1 = create_linked_list([1, 2, 4])
    list2 = create_linked_list([1, 3, 4])
    print_list(list1, "List1")
    print_list(list2, "List2")
    
    # Test iterative solution
    merged1 = solution.mergeTwoLists(list1, list2)
    print_list(merged1, "Merged (Iterative)")
    
    # Recreate lists for recursive test
    list1_rec = create_linked_list([1, 2, 4])
    list2_rec = create_linked_list([1, 3, 4])
    merged1_rec = solution_rec.mergeTwoLists(list1_rec, list2_rec)
    print_list(merged1_rec, "Merged (Recursive)")
    
    # Test case 2: Empty lists
    print("\n=== Test Case 2: [] and [] ===")
    list3 = None
    list4 = None
    merged2 = solution.mergeTwoLists(list3, list4)
    print_list(merged2, "Merged")
    
    # Test case 3: One empty, one non-empty
    print("\n=== Test Case 3: [] and [0] ===")
    list5 = None
    list6 = create_linked_list([0])
    print_list(list6, "List6")
    merged3 = solution.mergeTwoLists(list5, list6)
    print_list(merged3, "Merged")
    
    # Test case 4: Different lengths
    print("\n=== Test Case 4: [1,2,3,4,5] and [6,7] ===")
    list7 = create_linked_list([1, 2, 3, 4, 5])
    list8 = create_linked_list([6, 7])
    print_list(list7, "List7")
    print_list(list8, "List8")
    merged4 = solution.mergeTwoLists(list7, list8)
    print_list(merged4, "Merged")

"""
INTERVIEW TALKING POINTS:

1. APPROACH SELECTION:
   - Iterative with dummy node is most common and preferred
   - Dummy node simplifies edge case handling significantly
   - Recursive solution is more elegant but uses O(n+m) space

2. KEY INSIGHTS:
   - Two-pointer technique: maintain one pointer per list
   - Always choose the smaller value to maintain sorted order
   - Dummy node eliminates special case handling for first node
   - Remaining nodes can be attached directly (one list will be empty)

3. STEP-BY-STEP WALKTHROUGH:
   List1: 1 -> 2 -> 4
   List2: 1 -> 3 -> 4
   
   Step 1: Compare 1 and 1, choose first 1 -> merged: 1
   Step 2: Compare 2 and 1, choose 1 -> merged: 1 -> 1
   Step 3: Compare 2 and 3, choose 2 -> merged: 1 -> 1 -> 2
   Step 4: Compare 4 and 3, choose 3 -> merged: 1 -> 1 -> 2 -> 3
   Step 5: List2 empty, attach rest of List1 -> merged: 1 -> 1 -> 2 -> 3 -> 4

4. WHY DUMMY NODE?
   - Without dummy: need special handling for first node
   - With dummy: uniform handling for all nodes
   - Simplifies code and reduces bugs

5. EDGE CASES:
   - Both lists empty
   - One list empty
   - Lists of different lengths
   - All elements in one list smaller than the other

6. COMPLEXITY ANALYSIS:
   - Time: O(n + m) - visit each node exactly once
   - Space: O(1) for iterative, O(n + m) for recursive

7. FOLLOW-UP QUESTIONS:
   - "How would you merge k sorted lists?" (LeetCode 23)
   - "What if the lists weren't sorted?"
   - "Can you do it in-place without creating new nodes?"
   - "How would you handle duplicates differently?"

8. IMPLEMENTATION TIPS:
   - Use dummy node to simplify logic
   - Handle remaining nodes with "list1 or list2"
   - Test with edge cases (empty lists, single elements)
   - Consider both iterative and recursive approaches
   - Draw out the merging process step by step
"""
