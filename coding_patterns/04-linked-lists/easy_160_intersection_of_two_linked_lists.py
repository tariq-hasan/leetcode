# Definition for singly-linked list
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA, headB):
        """
        TWO-POINTER ELEGANT SOLUTION (MOST IMPRESSIVE FOR INTERVIEWS)
        
        Key Insight: Mathematical Beauty!
        - If lists intersect, they have a common tail
        - Let lenA = length of list A, lenB = length of list B
        - When pointer A reaches end, redirect to headB
        - When pointer B reaches end, redirect to headA
        - They will meet at intersection (or both reach None)
        
        Why it works:
        - PointerA travels: lenA + lenB - commonTail
        - PointerB travels: lenB + lenA - commonTail  
        - Both travel the same total distance!
        - They synchronize and meet at the intersection
        
        Visual:
        A: a1 -> a2 -> c1 -> c2 -> c3
        B: b1 -> b2 -> b3 -> c1 -> c2 -> c3
        
        After redirection:
        A: a1->a2->c1->c2->c3->b1->b2->b3->c1 (meets here)
        B: b1->b2->b3->c1->c2->c3->a1->a2->c1 (meets here)
        
        Time: O(m + n) where m, n are lengths of the lists
        Space: O(1) - only use two pointers
        """
        if not headA or not headB:
            return None
        
        # Two pointers starting at each head
        ptrA = headA
        ptrB = headB
        
        # Traverse until they meet or both reach None
        while ptrA != ptrB:
            # When ptrA reaches end, redirect to headB
            # When ptrB reaches end, redirect to headA
            # This ensures both travel the same total distance
            ptrA = headB if ptrA is None else ptrA.next
            ptrB = headA if ptrB is None else ptrB.next
        
        # Either they meet at intersection, or both are None (no intersection)
        return ptrA

class SolutionLengthDifference:
    def getIntersectionNode(self, headA, headB):
        """
        LENGTH CALCULATION SOLUTION (MORE INTUITIVE)
        
        Approach: Calculate length difference and align starting positions
        1. Calculate lengths of both lists
        2. Move longer list's pointer ahead by the difference
        3. Move both pointers together until they meet
        
        Time: O(m + n) - three passes through lists
        Space: O(1) - only use a few variables
        """
        if not headA or not headB:
            return None
        
        # Calculate lengths
        lenA = self.getLength(headA)
        lenB = self.getLength(headB)
        
        # Align starting positions
        ptrA = headA
        ptrB = headB
        
        # Move the longer list's pointer ahead by the difference
        if lenA > lenB:
            for _ in range(lenA - lenB):
                ptrA = ptrA.next
        else:
            for _ in range(lenB - lenA):
                ptrB = ptrB.next
        
        # Move both pointers together until they meet
        while ptrA and ptrB:
            if ptrA == ptrB:
                return ptrA
            ptrA = ptrA.next
            ptrB = ptrB.next
        
        return None
    
    def getLength(self, head):
        """Helper function to calculate list length"""
        length = 0
        while head:
            length += 1
            head = head.next
        return length

class SolutionHashSet:
    def getIntersectionNode(self, headA, headB):
        """
        HASH SET SOLUTION (BRUTE FORCE BUT INTUITIVE)
        
        Approach: Store all nodes from one list, check if any node from other list exists
        
        Time: O(m + n) - visit each node once
        Space: O(m) or O(n) - store one entire list in hash set
        """
        if not headA or not headB:
            return None
        
        # Store all nodes from list A
        visited = set()
        current = headA
        while current:
            visited.add(current)
            current = current.next
        
        # Check if any node from list B is in the set
        current = headB
        while current:
            if current in visited:
                return current
            current = current.next
        
        return None

class SolutionBruteForce:
    def getIntersectionNode(self, headA, headB):
        """
        BRUTE FORCE SOLUTION (FOR COMPLETENESS)
        
        For each node in list A, traverse entire list B to find match
        Not efficient but shows all possible approaches
        
        Time: O(m * n) - for each node in A, check all nodes in B
        Space: O(1) - only use pointers
        """
        if not headA or not headB:
            return None
        
        currentA = headA
        while currentA:
            currentB = headB
            while currentB:
                if currentA == currentB:
                    return currentA
                currentB = currentB.next
            currentA = currentA.next
        
        return None

class SolutionWithVisualization:
    def getIntersectionNodeVisual(self, headA, headB):
        """
        SOLUTION WITH STEP-BY-STEP VISUALIZATION
        Helps understand the elegant two-pointer approach
        """
        if not headA or not headB:
            print("One or both lists are empty")
            return None
        
        print("Demonstrating the elegant two-pointer approach...")
        print("Key insight: Both pointers travel the same total distance!")
        
        ptrA = headA
        ptrB = headB
        step = 0
        
        print(f"Initial: ptrA at {ptrA.val}, ptrB at {ptrB.val}")
        
        while ptrA != ptrB:
            step += 1
            
            # Show current positions
            next_A = "headB" if ptrA.next is None else str(ptrA.next.val)
            next_B = "headA" if ptrB.next is None else str(ptrB.next.val)
            
            print(f"Step {step}: ptrA at {ptrA.val} -> {next_A}, ptrB at {ptrB.val} -> {next_B}")
            
            # Move pointers
            ptrA = headB if ptrA.next is None else ptrA.next
            ptrB = headA if ptrB.next is None else ptrB.next
            
            # Safety check to avoid infinite loop in case of bugs
            if step > 20:
                print("Too many steps - possible infinite loop")
                break
        
        if ptrA == ptrB and ptrA is not None:
            print(f"Intersection found at node with value: {ptrA.val}")
        elif ptrA is None:
            print("No intersection found (both pointers reached None)")
        
        return ptrA

# Test utilities
def create_intersected_lists(valsA, valsB, intersectVal):
    """
    Create two linked lists with intersection
    intersectVal: value where intersection starts (None for no intersection)
    """
    # Create list A
    if not valsA:
        headA = None
    else:
        headA = ListNode(valsA[0])
        current = headA
        for val in valsA[1:]:
            current.next = ListNode(val)
            current = current.next
    
    # Create list B  
    if not valsB:
        headB = None
    else:
        headB = ListNode(valsB[0])
        current = headB
        for val in valsB[1:]:
            current.next = ListNode(val)
            current = current.next
    
    # Create intersection if specified
    if intersectVal is not None and headA and headB:
        # Find intersection point in list A
        currentA = headA
        while currentA and currentA.val != intersectVal:
            currentA = currentA.next
        
        if currentA:
            # Connect end of list B to intersection point
            currentB = headB
            while currentB.next:
                currentB = currentB.next
            currentB.next = currentA
    
    return headA, headB

def print_list(head, name="List", max_nodes=10):
    """Print linked list (with cycle detection)"""
    if not head:
        print(f"{name}: Empty")
        return
    
    values = []
    visited = set()
    current = head
    
    while current and len(values) < max_nodes:
        if current in visited:
            values.append(f"{current.val}(cycle)")
            break
        visited.add(current)
        values.append(str(current.val))
        current = current.next
    
    if current and len(values) == max_nodes:
        values.append("...")
    
    print(f"{name}: {' -> '.join(values)}")

# Test all solutions
if __name__ == "__main__":
    solution = Solution()
    length_solution = SolutionLengthDifference()
    hash_solution = SolutionHashSet()
    
    # Test case 1: Intersection at value 8
    print("=== Test Case 1: Lists intersect at value 8 ===")
    # listA: [4,1,8,4,5], listB: [5,6,1,8,4,5]
    # They intersect at node with value 8
    
    # Create the intersection manually for proper testing
    # Common tail: 8 -> 4 -> 5
    node8 = ListNode(8)
    node4 = ListNode(4)
    node5 = ListNode(5)
    node8.next = node4
    node4.next = node5
    
    # List A: 4 -> 1 -> 8(shared)
    headA = ListNode(4)
    headA.next = ListNode(1)
    headA.next.next = node8
    
    # List B: 5 -> 6 -> 1 -> 8(shared)
    headB = ListNode(5)
    headB.next = ListNode(6)
    headB.next.next = ListNode(1)
    headB.next.next.next = node8
    
    print_list(headA, "List A")
    print_list(headB, "List B")
    
    result1 = solution.getIntersectionNode(headA, headB)
    result1_len = length_solution.getIntersectionNode(headA, headB)
    result1_hash = hash_solution.getIntersectionNode(headA, headB)
    
    print(f"Two Pointer: Intersection at {result1.val if result1 else None}")
    print(f"Length Diff: Intersection at {result1_len.val if result1_len else None}")
    print(f"Hash Set: Intersection at {result1_hash.val if result1_hash else None}")
    
    # Test case 2: No intersection
    print("\n=== Test Case 2: No intersection ===")
    headA2 = ListNode(2)
    headA2.next = ListNode(6)
    headA2.next.next = ListNode(4)
    
    headB2 = ListNode(1)
    headB2.next = ListNode(5)
    
    print_list(headA2, "List A")
    print_list(headB2, "List B")
    
    result2 = solution.getIntersectionNode(headA2, headB2)
    print(f"Intersection: {result2.val if result2 else None}")
    
    # Visual demonstration
    print("\n=== Visual Demonstration ===")
    visual_solution = SolutionWithVisualization()
    visual_result = visual_solution.getIntersectionNodeVisual(headA, headB)

"""
INTERVIEW TALKING POINTS:

1. PROBLEM UNDERSTANDING:
   "We need to find the node where two linked lists intersect"
   "Key insight: intersection means same node object, not just same value"
   "After intersection, both lists share the same tail"

2. ELEGANT SOLUTION EXPLANATION:
   "The beautiful insight: make both pointers travel the same total distance"
   "When ptrA finishes list A, redirect to headB"
   "When ptrB finishes list B, redirect to headA"
   "They'll meet at intersection or both reach None"

3. MATHEMATICAL PROOF:
   "Let's say lists have lengths m and n with intersection"
   "ptrA travels: m + (n - common) = m + n - common"
   "ptrB travels: n + (m - common) = n + m - common"
   "Same total distance! They synchronize at intersection"

4. WHY THIS IS ELEGANT:
   - No need to calculate lengths
   - No extra space required
   - Handles all edge cases naturally
   - Beautiful mathematical insight

5. ALTERNATIVE APPROACHES:
   - Length difference: More intuitive but requires 3 passes
   - Hash set: Uses extra space but straightforward
   - Brute force: O(m*n) time but shows all approaches

6. EDGE CASES:
   - No intersection → both pointers reach None
   - One list empty → return None immediately
   - Same starting node → return immediately
   - Different length lists → algorithm handles automatically

7. COMPLEXITY ANALYSIS:
   - Two Pointer: O(m+n) time, O(1) space ✅ (optimal)
   - Length Diff: O(m+n) time, O(1) space
   - Hash Set: O(m+n) time, O(m) or O(n) space

8. FOLLOW-UP QUESTIONS:
   - "What if lists can have cycles?" → More complex detection needed
   - "Find the intersection in doubly-linked lists?" → Same algorithm works
   - "What if we need to preserve original lists?" → All solutions are non-destructive

9. IMPLEMENTATION DETAILS:
   - Use "is None" not "== None" for clarity
   - Handle null inputs at the start
   - The elegant solution is a single while loop
   - Both approaches redirect, creating equal path lengths

10. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests multiple algorithmic thinking approaches
    - Has an elegant mathematical solution
    - Shows understanding of pointer manipulation
    - Demonstrates optimization thinking (space vs time)
"""
