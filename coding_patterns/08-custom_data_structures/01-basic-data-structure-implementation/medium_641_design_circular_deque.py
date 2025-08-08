# LeetCode 641: Design Circular Deque
# Design your implementation of the circular double-ended queue (deque).

"""
Problem: Design your implementation of the circular double-ended queue (deque).

Implement the MyCircularDeque class:
- MyCircularDeque(k) Initializes the deque with a maximum size of k.
- boolean insertFront(int value) Adds an item at the front of Deque. Return true if successful.
- boolean insertLast(int value) Adds an item at the rear of Deque. Return true if successful.
- boolean deleteFront() Deletes an item from the front of Deque. Return true if successful.
- boolean deleteLast() Deletes an item from the rear of Deque. Return true if successful.
- int getFront() Gets the front item from the Deque. If the deque is empty, return -1.
- int getRear() Gets the last item from Deque. If the deque is empty, return -1.
- boolean isEmpty() Checks whether Deque is empty or not.
- boolean isFull() Checks whether Deque is full or not.
"""

# SOLUTION 1: Array-based with Head/Tail and Size Counter (Most Common)
class MyCircularDeque1:
    def __init__(self, k: int):
        """
        Initialize circular deque with capacity k.
        Time: O(1), Space: O(k)
        """
        self.capacity = k
        self.deque = [0] * k
        self.head = 0    # Points to front element
        self.tail = 0    # Points to position after last element
        self.size = 0    # Current number of elements
    
    def insertFront(self, value: int) -> bool:
        """
        Insert element at front of deque.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        # Move head backwards (with wrap-around)
        self.head = (self.head - 1 + self.capacity) % self.capacity
        self.deque[self.head] = value
        self.size += 1
        return True
    
    def insertLast(self, value: int) -> bool:
        """
        Insert element at rear of deque.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.deque[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        return True
    
    def deleteFront(self) -> bool:
        """
        Delete element from front of deque.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True
    
    def deleteLast(self) -> bool:
        """
        Delete element from rear of deque.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.tail = (self.tail - 1 + self.capacity) % self.capacity
        self.size -= 1
        return True
    
    def getFront(self) -> int:
        """
        Get front element of deque.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.deque[self.head]
    
    def getRear(self) -> int:
        """
        Get rear element of deque.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        # Rear is at (tail - 1) position
        rear_index = (self.tail - 1 + self.capacity) % self.capacity
        return self.deque[rear_index]
    
    def isEmpty(self) -> bool:
        """
        Check if deque is empty.
        Time: O(1), Space: O(1)
        """
        return self.size == 0
    
    def isFull(self) -> bool:
        """
        Check if deque is full.
        Time: O(1), Space: O(1)
        """
        return self.size == self.capacity


# SOLUTION 2: Array-based without Size Counter (Space Optimized)
class MyCircularDeque2:
    def __init__(self, k: int):
        """
        Initialize with k+1 capacity to distinguish full from empty.
        Time: O(1), Space: O(k)
        """
        self.capacity = k + 1  # Extra space to distinguish full/empty
        self.deque = [0] * self.capacity
        self.head = 0
        self.tail = 0
    
    def insertFront(self, value: int) -> bool:
        """
        Insert element at front.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.head = (self.head - 1 + self.capacity) % self.capacity
        self.deque[self.head] = value
        return True
    
    def insertLast(self, value: int) -> bool:
        """
        Insert element at rear.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.deque[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity
        return True
    
    def deleteFront(self) -> bool:
        """
        Delete element from front.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.head = (self.head + 1) % self.capacity
        return True
    
    def deleteLast(self) -> bool:
        """
        Delete element from rear.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.tail = (self.tail - 1 + self.capacity) % self.capacity
        return True
    
    def getFront(self) -> int:
        """
        Get front element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.deque[self.head]
    
    def getRear(self) -> int:
        """
        Get rear element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        rear_index = (self.tail - 1 + self.capacity) % self.capacity
        return self.deque[rear_index]
    
    def isEmpty(self) -> bool:
        """
        Deque is empty when head equals tail.
        Time: O(1), Space: O(1)
        """
        return self.head == self.tail
    
    def isFull(self) -> bool:
        """
        Deque is full when next tail position equals head.
        Time: O(1), Space: O(1)
        """
        return (self.tail + 1) % self.capacity == self.head


# SOLUTION 3: Doubly Linked List Implementation (Dynamic)
class DoublyListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class MyCircularDeque3:
    def __init__(self, k: int):
        """
        Initialize using doubly circular linked list with sentinel.
        Time: O(1), Space: O(1)
        """
        self.capacity = k
        self.size = 0
        
        # Create sentinel node for easier implementation
        self.sentinel = DoublyListNode()
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel
    
    def _add_after(self, node: DoublyListNode, value: int) -> None:
        """Helper: Add new node after given node."""
        new_node = DoublyListNode(value)
        new_node.next = node.next
        new_node.prev = node
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
    
    def _remove_node(self, node: DoublyListNode) -> None:
        """Helper: Remove given node."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
    
    def insertFront(self, value: int) -> bool:
        """
        Insert at front (after sentinel).
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self._add_after(self.sentinel, value)
        return True
    
    def insertLast(self, value: int) -> bool:
        """
        Insert at rear (before sentinel).
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self._add_after(self.sentinel.prev, value)
        return True
    
    def deleteFront(self) -> bool:
        """
        Delete from front.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self._remove_node(self.sentinel.next)
        return True
    
    def deleteLast(self) -> bool:
        """
        Delete from rear.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self._remove_node(self.sentinel.prev)
        return True
    
    def getFront(self) -> int:
        """
        Get front element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.sentinel.next.val
    
    def getRear(self) -> int:
        """
        Get rear element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.sentinel.prev.val
    
    def isEmpty(self) -> bool:
        """
        Check if empty.
        Time: O(1), Space: O(1)
        """
        return self.size == 0
    
    def isFull(self) -> bool:
        """
        Check if full.
        Time: O(1), Space: O(1)
        """
        return self.size == self.capacity


# SOLUTION 4: Alternative Array Implementation with Clear Semantics
class MyCircularDeque4:
    def __init__(self, k: int):
        """
        Alternative implementation with clearer variable naming.
        Time: O(1), Space: O(k)
        """
        self.capacity = k
        self.buffer = [0] * k
        self.front_idx = 0  # Index of front element
        self.rear_idx = 0   # Index of rear element
        self.count = 0      # Number of elements
    
    def insertFront(self, value: int) -> bool:
        """
        Insert at front by moving front_idx backwards.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        if self.isEmpty():
            # First element
            self.buffer[self.front_idx] = value
        else:
            # Move front backwards and insert
            self.front_idx = (self.front_idx - 1 + self.capacity) % self.capacity
            self.buffer[self.front_idx] = value
        
        self.count += 1
        return True
    
    def insertLast(self, value: int) -> bool:
        """
        Insert at rear by moving rear_idx forwards.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        if self.isEmpty():
            # First element
            self.buffer[self.rear_idx] = value
        else:
            # Move rear forwards and insert
            self.rear_idx = (self.rear_idx + 1) % self.capacity
            self.buffer[self.rear_idx] = value
        
        self.count += 1
        return True
    
    def deleteFront(self) -> bool:
        """
        Delete from front.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        if self.count == 1:
            # Last element, reset indices
            self.front_idx = 0
            self.rear_idx = 0
        else:
            # Move front forwards
            self.front_idx = (self.front_idx + 1) % self.capacity
        
        self.count -= 1
        return True
    
    def deleteLast(self) -> bool:
        """
        Delete from rear.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        if self.count == 1:
            # Last element, reset indices
            self.front_idx = 0
            self.rear_idx = 0
        else:
            # Move rear backwards
            self.rear_idx = (self.rear_idx - 1 + self.capacity) % self.capacity
        
        self.count -= 1
        return True
    
    def getFront(self) -> int:
        """
        Get front element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.buffer[self.front_idx]
    
    def getRear(self) -> int:
        """
        Get rear element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.buffer[self.rear_idx]
    
    def isEmpty(self) -> bool:
        """
        Check if empty.
        Time: O(1), Space: O(1)
        """
        return self.count == 0
    
    def isFull(self) -> bool:
        """
        Check if full.
        Time: O(1), Space: O(1)
        """
        return self.count == self.capacity


# Comprehensive test function
def test_circular_deque():
    """Test all implementations with various scenarios."""
    
    print("Testing Circular Deque implementations...")
    
    # Test each implementation
    for i, DequeClass in enumerate([MyCircularDeque1, MyCircularDeque2, MyCircularDeque3, MyCircularDeque4], 1):
        print(f"\n--- Testing Solution {i}: {DequeClass.__name__} ---")
        
        deque = DequeClass(3)
        
        print(f"isEmpty(): {deque.isEmpty()}")  # True
        
        # Test insertions
        print(f"insertLast(1): {deque.insertLast(1)}")    # True
        print(f"insertLast(2): {deque.insertLast(2)}")    # True
        print(f"insertFront(3): {deque.insertFront(3)}")  # True
        print(f"insertFront(4): {deque.insertFront(4)}")  # False (full)
        
        print(f"isFull(): {deque.isFull()}")     # True
        print(f"getRear(): {deque.getRear()}")   # 2
        print(f"getFront(): {deque.getFront()}") # 3
        
        # Test deletions
        print(f"deleteLast(): {deque.deleteLast()}")   # True
        print(f"insertFront(4): {deque.insertFront(4)}")  # True
        print(f"getFront(): {deque.getFront()}")  # 4
        print(f"getRear(): {deque.getRear()}")    # 1


def visualize_deque_operations():
    """Visual demonstration of circular deque operations."""
    print("\n" + "="*60)
    print("VISUAL DEMONSTRATION - CIRCULAR DEQUE")
    print("="*60)
    
    deque = MyCircularDeque1(4)
    
    def print_state(operation=""):
        if operation:
            print(f"\nAfter {operation}:")
        print(f"Array: {deque.deque}")
        print(f"Head: {deque.head}, Tail: {deque.tail}, Size: {deque.size}")
        print(f"Empty: {deque.isEmpty()}, Full: {deque.isFull()}")
        if not deque.isEmpty():
            print(f"Front: {deque.getFront()}, Rear: {deque.getRear()}")
        
        # Visual representation
        visual = ['_'] * deque.capacity
        if not deque.isEmpty():
            # Mark elements
            curr = deque.head
            for i in range(deque.size):
                visual[curr] = str(deque.deque[curr])
                curr = (curr + 1) % deque.capacity
            
            # Mark head and tail
            head_marker = f"H({deque.head})"
            tail_marker = f"T({deque.tail})"
        
        print(f"Visual: {visual}")
        print("-" * 40)
    
    print("Initial state:")
    print_state()
    
    # Demonstrate different insertion patterns
    print_state("insertLast(1)")
    deque.insertLast(1)
    
    print_state("insertFront(2)")
    deque.insertFront(2)
    
    print_state("insertLast(3)")
    deque.insertLast(3)
    
    print_state("insertFront(4) - should be full")
    deque.insertFront(4)
    
    print_state("deleteFront()")
    deque.deleteFront()
    
    print_state("deleteLast()")
    deque.deleteLast()
    
    print_state("insertFront(5) - demonstrating wrap-around")
    deque.insertFront(5)
    
    print_state("insertLast(6)")
    deque.insertLast(6)


def performance_comparison():
    """Compare different implementations for educational purposes."""
    print("\n" + "="*50)
    print("IMPLEMENTATION COMPARISON")
    print("="*50)
    
    implementations = [
        ("Array + Size Counter", "O(k)", "Simple, intuitive"),
        ("Array + Extra Space", "O(k+1)", "No size counter needed"),
        ("Doubly Linked List", "O(1) extra", "Dynamic, more complex"),
        ("Array + Clear Semantics", "O(k)", "Explicit front/rear indices")
    ]
    
    print(f"{'Implementation':<25} {'Space':<10} {'Notes'}")
    print("-" * 55)
    for impl, space, notes in implementations:
        print(f"{impl:<25} {space:<10} {notes}")


if __name__ == "__main__":
    test_circular_deque()
    visualize_deque_operations()
    performance_comparison()


"""
INTERVIEW DISCUSSION POINTS:

1. TIME COMPLEXITY: All operations are O(1) for all solutions

2. SPACE COMPLEXITY:
   - Solution 1: O(k) + O(1) for size counter
   - Solution 2: O(k+1), no size counter
   - Solution 3: O(1) extra space, O(k) for nodes
   - Solution 4: O(k) + clearer semantics

3. KEY DEQUE CONCEPTS:
   - Double-ended operations: insert/delete from both ends
   - Circular buffer: wrap-around for both directions
   - Backward indexing: (index - 1 + capacity) % capacity
   - Forward indexing: (index + 1) % capacity

4. CRITICAL IMPLEMENTATION DETAILS:
   - insertFront: Move head backwards before inserting
   - deleteLast: Move tail backwards after deleting
   - getRear: Always at (tail - 1 + capacity) % capacity
   - Handle empty/full states correctly

5. COMMON PITFALLS:
   - Forgetting + capacity in backward modulo operations
   - Incorrect head/tail updates in front operations
   - Edge cases with single element
   - Off-by-one errors in index calculations

6. FOLLOW-UP QUESTIONS:
   - "Implement using only insertLast and deleteFront operations"
   - "How would you make it thread-safe?"
   - "Can you implement with better cache locality?"
   - "What about resizable circular deque?"

7. IMPLEMENTATION CHOICE FOR INTERVIEW:
   - Start with Solution 1 (most intuitive)
   - Mention Solution 2 if asked about space optimization
   - Solution 3 for dynamic sizing discussions
   - Solution 4 for cleaner code organization

8. TESTING STRATEGY:
   - Test all four operations extensively
   - Test with capacity 1, 2, and larger sizes
   - Test alternating front/rear operations
   - Verify wrap-around behavior
   - Check empty/full boundary conditions

9. COMPLEXITY ANALYSIS:
   - Time: O(1) for all operations
   - Space: O(k) where k is the capacity
   - No additional space complexity for operations

10. ADVANTAGES OF CIRCULAR DEQUE:
    - Constant time operations at both ends
    - Fixed memory usage
    - Cache-friendly array implementation
    - Suitable for sliding window problems
"""
