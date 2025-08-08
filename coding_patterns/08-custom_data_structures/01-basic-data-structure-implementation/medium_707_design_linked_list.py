# LeetCode 707: Design Linked List
# Design your implementation of the linked list.

"""
Problem: Design your implementation of the linked list. You can choose to use a singly 
or doubly linked list. A node in a singly linked list should have two attributes: 
val and next. A node in a doubly linked list should have three attributes: val, next and prev.

Implement the MyLinkedList class:
- MyLinkedList() Initializes the MyLinkedList object.
- int get(int index) Get the value of the indexth node in the linked list. If invalid, return -1.
- void addAtHead(int val) Add a node of value val before the first element of the linked list.
- void addAtTail(int val) Add a node of value val as the last element of the linked list.
- void addAtIndex(int index, int val) Add a node of value val before the indexth node.
- void deleteAtIndex(int index) Delete the indexth node in the linked list, if the index is valid.
"""

# SOLUTION 1: Singly Linked List (Most Common Interview Answer)
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None

class MyLinkedList1:
    def __init__(self):
        """
        Initialize the linked list with a dummy head.
        Time: O(1), Space: O(1)
        """
        self.head = ListNode(0)  # Dummy head for easier operations
        self.size = 0
    
    def get(self, index: int) -> int:
        """
        Get the value of the index-th node.
        Time: O(index), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return -1
        
        curr = self.head.next  # Start from first real node
        for _ in range(index):
            curr = curr.next
        return curr.val
    
    def addAtHead(self, val: int) -> None:
        """
        Add a node at the beginning of the list.
        Time: O(1), Space: O(1)
        """
        new_node = ListNode(val)
        new_node.next = self.head.next
        self.head.next = new_node
        self.size += 1
    
    def addAtTail(self, val: int) -> None:
        """
        Add a node at the end of the list.
        Time: O(n), Space: O(1)
        """
        new_node = ListNode(val)
        curr = self.head
        
        # Traverse to the last node
        while curr.next:
            curr = curr.next
        
        curr.next = new_node
        self.size += 1
    
    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node before the index-th node.
        Time: O(index), Space: O(1)
        """
        if index > self.size:
            return
        
        if index < 0:
            index = 0
        
        new_node = ListNode(val)
        curr = self.head
        
        # Find the node before insertion point
        for _ in range(index):
            curr = curr.next
        
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1
    
    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node.
        Time: O(index), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return
        
        curr = self.head
        
        # Find the node before deletion point
        for _ in range(index):
            curr = curr.next
        
        curr.next = curr.next.next
        self.size -= 1


# SOLUTION 2: Doubly Linked List (More Efficient for Some Operations)
class DoublyListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None
        self.prev = None

class MyLinkedList2:
    def __init__(self):
        """
        Initialize with dummy head and tail for easier operations.
        Time: O(1), Space: O(1)
        """
        self.head = DoublyListNode(0)  # Dummy head
        self.tail = DoublyListNode(0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def get(self, index: int) -> int:
        """
        Get value with optimization to search from closer end.
        Time: O(min(index, size-index)), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return -1
        
        # Optimize: search from head or tail based on index
        if index < self.size // 2:
            # Search from head
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            # Search from tail
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        
        return curr.val
    
    def addAtHead(self, val: int) -> None:
        """
        Add node at head.
        Time: O(1), Space: O(1)
        """
        self._add_after(self.head, val)
    
    def addAtTail(self, val: int) -> None:
        """
        Add node at tail.
        Time: O(1), Space: O(1)
        """
        self._add_before(self.tail, val)
    
    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add node at specific index.
        Time: O(min(index, size-index)), Space: O(1)
        """
        if index > self.size:
            return
        
        if index < 0:
            index = 0
        
        if index < self.size // 2:
            # Find position from head
            curr = self.head
            for _ in range(index):
                curr = curr.next
            self._add_after(curr, val)
        else:
            # Find position from tail
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
            self._add_before(curr, val)
    
    def deleteAtIndex(self, index: int) -> None:
        """
        Delete node at specific index.
        Time: O(min(index, size-index)), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return
        
        if index < self.size // 2:
            # Find from head
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            # Find from tail
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        
        self._remove_node(curr)
    
    def _add_after(self, node: DoublyListNode, val: int) -> None:
        """Helper: Add new node after given node."""
        new_node = DoublyListNode(val)
        new_node.next = node.next
        new_node.prev = node
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
    
    def _add_before(self, node: DoublyListNode, val: int) -> None:
        """Helper: Add new node before given node."""
        new_node = DoublyListNode(val)
        new_node.next = node
        new_node.prev = node.prev
        node.prev.next = new_node
        node.prev = new_node
        self.size += 1
    
    def _remove_node(self, node: DoublyListNode) -> None:
        """Helper: Remove given node."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1


# SOLUTION 3: Singly Linked List with Tail Pointer (Optimized)
class MyLinkedList3:
    def __init__(self):
        """
        Initialize with dummy head and tail pointer for O(1) tail operations.
        Time: O(1), Space: O(1)
        """
        self.head = ListNode(0)  # Dummy head
        self.tail = self.head    # Points to last node
        self.size = 0
    
    def get(self, index: int) -> int:
        """
        Get value at index.
        Time: O(index), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return -1
        
        curr = self.head.next
        for _ in range(index):
            curr = curr.next
        return curr.val
    
    def addAtHead(self, val: int) -> None:
        """
        Add at head.
        Time: O(1), Space: O(1)
        """
        new_node = ListNode(val)
        new_node.next = self.head.next
        self.head.next = new_node
        
        # Update tail if this is first node
        if self.size == 0:
            self.tail = new_node
        
        self.size += 1
    
    def addAtTail(self, val: int) -> None:
        """
        Add at tail with O(1) complexity.
        Time: O(1), Space: O(1)
        """
        new_node = ListNode(val)
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1
    
    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add at specific index.
        Time: O(index), Space: O(1)
        """
        if index > self.size:
            return
        
        if index < 0:
            index = 0
        
        if index == self.size:
            self.addAtTail(val)
            return
        
        new_node = ListNode(val)
        curr = self.head
        
        for _ in range(index):
            curr = curr.next
        
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1
    
    def deleteAtIndex(self, index: int) -> None:
        """
        Delete at specific index.
        Time: O(index), Space: O(1)
        """
        if index < 0 or index >= self.size:
            return
        
        curr = self.head
        
        for _ in range(index):
            curr = curr.next
        
        # Update tail if deleting last node
        if curr.next == self.tail:
            self.tail = curr
        
        curr.next = curr.next.next
        self.size -= 1


# SOLUTION 4: Array-based Implementation (Alternative Approach)
class MyLinkedList4:
    def __init__(self):
        """
        Array-based implementation for comparison.
        Time: O(1), Space: O(1)
        """
        self.data = []
    
    def get(self, index: int) -> int:
        """
        Get value at index.
        Time: O(1), Space: O(1)
        """
        if index < 0 or index >= len(self.data):
            return -1
        return self.data[index]
    
    def addAtHead(self, val: int) -> None:
        """
        Insert at beginning.
        Time: O(n), Space: O(1)
        """
        self.data.insert(0, val)
    
    def addAtTail(self, val: int) -> None:
        """
        Append at end.
        Time: O(1) amortized, Space: O(1)
        """
        self.data.append(val)
    
    def addAtIndex(self, index: int, val: int) -> None:
        """
        Insert at specific index.
        Time: O(n-index), Space: O(1)
        """
        if index > len(self.data):
            return
        
        if index < 0:
            index = 0
        
        self.data.insert(index, val)
    
    def deleteAtIndex(self, index: int) -> None:
        """
        Delete at specific index.
        Time: O(n-index), Space: O(1)
        """
        if index < 0 or index >= len(self.data):
            return
        
        self.data.pop(index)


# Comprehensive test function
def test_linked_list():
    """Test all implementations with various scenarios."""
    
    print("Testing Linked List implementations...")
    
    implementations = [
        ("Singly Linked List", MyLinkedList1),
        ("Doubly Linked List", MyLinkedList2),
        ("Singly + Tail Pointer", MyLinkedList3),
        ("Array-based", MyLinkedList4)
    ]
    
    for name, ListClass in implementations:
        print(f"\n--- Testing {name} ---")
        
        linked_list = ListClass()
        
        # Test sequence from LeetCode example
        linked_list.addAtHead(7)
        linked_list.addAtHead(2)
        linked_list.addAtHead(1)
        
        print(f"After adding 1,2,7 at head:")
        for i in range(3):
            print(f"get({i}): {linked_list.get(i)}")
        
        linked_list.addAtIndex(3, 0)
        linked_list.deleteAtIndex(2)
        
        print(f"After addAtIndex(3,0) and deleteAtIndex(2):")
        for i in range(3):
            print(f"get({i}): {linked_list.get(i)}")
        
        linked_list.addAtHead(6)
        linked_list.addAtTail(4)
        
        print(f"After addAtHead(6) and addAtTail(4):")
        for i in range(5):
            print(f"get({i}): {linked_list.get(i)}")
        
        # Test edge cases
        print(f"get(-1): {linked_list.get(-1)}")  # Should be -1
        print(f"get(10): {linked_list.get(10)}")  # Should be -1


def performance_analysis():
    """Analyze time complexity of different implementations."""
    print("\n" + "="*70)
    print("PERFORMANCE ANALYSIS")
    print("="*70)
    
    operations = [
        ("get(index)", "O(n)", "O(min(i,n-i))", "O(n)", "O(1)"),
        ("addAtHead", "O(1)", "O(1)", "O(1)", "O(n)"),
        ("addAtTail", "O(n)", "O(1)", "O(1)", "O(1)"),
        ("addAtIndex", "O(i)", "O(min(i,n-i))", "O(i)", "O(n-i)"),
        ("deleteAtIndex", "O(i)", "O(min(i,n-i))", "O(i)", "O(n-i)")
    ]
    
    headers = ["Operation", "Singly", "Doubly", "Singly+Tail", "Array"]
    print(f"{headers[0]:<15} {headers[1]:<10} {headers[2]:<15} {headers[3]:<12} {headers[4]:<10}")
    print("-" * 70)
    
    for op_data in operations:
        print(f"{op_data[0]:<15} {op_data[1]:<10} {op_data[2]:<15} {op_data[3]:<12} {op_data[4]:<10}")


def visualize_operations():
    """Visual demonstration of linked list operations."""
    print("\n" + "="*50)
    print("VISUAL DEMONSTRATION")
    print("="*50)
    
    ll = MyLinkedList1()
    
    def print_list():
        """Helper to print current list state."""
        if ll.size == 0:
            print("List: []")
            return
        
        values = []
        curr = ll.head.next
        while curr:
            values.append(str(curr.val))
            curr = curr.next
        print(f"List: [{'->'.join(values)}] (size: {ll.size})")
    
    print("Initial state:")
    print_list()
    
    print("\naddAtHead(1):")
    ll.addAtHead(1)
    print_list()
    
    print("\naddAtTail(3):")
    ll.addAtTail(3)
    print_list()
    
    print("\naddAtIndex(1, 2):")
    ll.addAtIndex(1, 2)
    print_list()
    
    print("\nget(1):", ll.get(1))
    
    print("\ndeleteAtIndex(1):")
    ll.deleteAtIndex(1)
    print_list()
    
    print("\nget(1):", ll.get(1))


if __name__ == "__main__":
    test_linked_list()
    performance_analysis()
    visualize_operations()


"""
INTERVIEW DISCUSSION POINTS:

1. IMPLEMENTATION CHOICES:
   - Singly vs Doubly: Trade-off between space and time
   - Dummy head: Simplifies edge case handling
   - Size tracking: Enables O(1) size queries and bounds checking

2. TIME COMPLEXITY ANALYSIS:
   - Singly: get/add/delete at index = O(index)
   - Doubly: Optimized to O(min(index, size-index))
   - Array: Random access O(1), but insertions expensive

3. SPACE COMPLEXITY:
   - Singly: O(1) per node
   - Doubly: O(1) per node + extra prev pointer
   - Array: O(1) per element + potential waste from dynamic array

4. KEY DESIGN DECISIONS:
   - Dummy head eliminates special cases for head operations
   - Size tracking prevents index out of bounds errors
   - Helper methods in doubly linked list reduce code duplication

5. COMMON PITFALLS:
   - Forgetting to update size counter
   - Not handling negative indices correctly
   - Edge cases: empty list, single element, boundary indices
   - Memory leaks (not applicable in Python but mention for C++)

6. FOLLOW-UP QUESTIONS:
   - "How would you make it thread-safe?"
   - "Can you implement without dummy nodes?"
   - "How would you add iterator support?"
   - "What about memory optimization?"

7. IMPLEMENTATION PREFERENCE FOR INTERVIEW:
   - Start with Solution 1 (Singly with dummy head)
   - It's most straightforward and covers all requirements
   - Mention optimizations (Solution 2/3) if asked
   - Avoid Solution 4 unless specifically asked about array-based

8. TESTING STRATEGY:
   - Test with provided example
   - Edge cases: index 0, last index, out of bounds
   - Empty list operations
   - Single element list operations
   - Sequential operations to verify state consistency

9. CODE ORGANIZATION TIPS:
   - Use helper methods for complex operations (doubly linked list)
   - Consistent variable naming (curr, prev, next)
   - Clear comments for non-obvious operations
   - Proper error handling for invalid indices

10. OPTIMIZATION OPPORTUNITIES:
    - Doubly linked list for bidirectional access
    - Tail pointer for O(1) tail operations
    - Size tracking for bounds checking
    - Consider hybrid approaches for specific use cases
"""
