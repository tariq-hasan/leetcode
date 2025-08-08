# LeetCode 622: Design Circular Queue
# Design your implementation of the circular queue data structure.

"""
Problem: Design your implementation of the circular queue data structure.

The circular queue is a linear data structure in which the operations are performed 
based on FIFO (First In First Out) principle and the last position is connected 
back to the first position to make a circle.

Implement the MyCircularQueue class:
- MyCircularQueue(k) Initializes the object with the size of the queue to be k.
- boolean enQueue(int value) Inserts an element into the circular queue. Return true if successful.
- boolean deQueue() Deletes an element from the circular queue. Return true if successful.
- int Front() Gets the front item from the queue. If the queue is empty, return -1.
- int Rear() Gets the last item from the queue. If the queue is empty, return -1.
- boolean isEmpty() Checks whether the circular queue is empty or not.
- boolean isFull() Checks whether the circular queue is full or not.

You must solve the problem without using the built-in queue data structure.
"""

# SOLUTION 1: Array-based with Head/Tail Pointers (Most Common)
class MyCircularQueue1:
    def __init__(self, k: int):
        """
        Initialize circular queue with capacity k.
        Time: O(1), Space: O(k)
        """
        self.capacity = k
        self.queue = [0] * k  # Fixed-size array
        self.head = 0         # Points to front element
        self.tail = 0         # Points to next insertion position
        self.size = 0         # Track current number of elements
    
    def enQueue(self, value: int) -> bool:
        """
        Insert element at rear of queue.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.queue[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity  # Circular increment
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        """
        Delete element from front of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.head = (self.head + 1) % self.capacity  # Circular increment
        self.size -= 1
        return True
    
    def Front(self) -> int:
        """
        Get front element of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.queue[self.head]
    
    def Rear(self) -> int:
        """
        Get rear element of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        # Rear is at (tail - 1) position (with wrap-around)
        rear_index = (self.tail - 1 + self.capacity) % self.capacity
        return self.queue[rear_index]
    
    def isEmpty(self) -> bool:
        """
        Check if queue is empty.
        Time: O(1), Space: O(1)
        """
        return self.size == 0
    
    def isFull(self) -> bool:
        """
        Check if queue is full.
        Time: O(1), Space: O(1)
        """
        return self.size == self.capacity


# SOLUTION 2: Array-based without Size Counter (Space Optimized)
class MyCircularQueue2:
    def __init__(self, k: int):
        """
        Initialize with k+1 capacity to distinguish full from empty.
        Time: O(1), Space: O(k)
        """
        self.capacity = k + 1  # Extra space to distinguish full/empty
        self.queue = [0] * self.capacity
        self.head = 0
        self.tail = 0
    
    def enQueue(self, value: int) -> bool:
        """
        Insert element at rear of queue.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.queue[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity
        return True
    
    def deQueue(self) -> bool:
        """
        Delete element from front of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.head = (self.head + 1) % self.capacity
        return True
    
    def Front(self) -> int:
        """
        Get front element of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.queue[self.head]
    
    def Rear(self) -> int:
        """
        Get rear element of queue.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        rear_index = (self.tail - 1 + self.capacity) % self.capacity
        return self.queue[rear_index]
    
    def isEmpty(self) -> bool:
        """
        Queue is empty when head equals tail.
        Time: O(1), Space: O(1)
        """
        return self.head == self.tail
    
    def isFull(self) -> bool:
        """
        Queue is full when next tail position equals head.
        Time: O(1), Space: O(1)
        """
        return (self.tail + 1) % self.capacity == self.head


# SOLUTION 3: Linked List Implementation (Dynamic Size)
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None

class MyCircularQueue3:
    def __init__(self, k: int):
        """
        Initialize using circular linked list.
        Time: O(1), Space: O(1)
        """
        self.capacity = k
        self.size = 0
        self.head = None
        self.tail = None
    
    def enQueue(self, value: int) -> bool:
        """
        Insert element using linked list.
        Time: O(1), Space: O(1) per element
        """
        if self.isFull():
            return False
        
        new_node = ListNode(value)
        
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node  # Point to itself (circular)
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        """
        Delete element from linked list.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.tail.next = self.head.next
            self.head = self.head.next
        
        self.size -= 1
        return True
    
    def Front(self) -> int:
        """
        Get front element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.head.val
    
    def Rear(self) -> int:
        """
        Get rear element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.tail.val
    
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


# SOLUTION 4: Using Python List as Circular Buffer (Alternative)
class MyCircularQueue4:
    def __init__(self, k: int):
        """
        Alternative implementation with clear separation of concerns.
        Time: O(1), Space: O(k)
        """
        self.capacity = k
        self.buffer = [None] * k
        self.write_idx = 0
        self.read_idx = 0
        self.count = 0
    
    def enQueue(self, value: int) -> bool:
        """
        Insert element with clear write pointer logic.
        Time: O(1), Space: O(1)
        """
        if self.isFull():
            return False
        
        self.buffer[self.write_idx] = value
        self.write_idx = (self.write_idx + 1) % self.capacity
        self.count += 1
        return True
    
    def deQueue(self) -> bool:
        """
        Remove element with clear read pointer logic.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return False
        
        self.buffer[self.read_idx] = None  # Optional: clear for debugging
        self.read_idx = (self.read_idx + 1) % self.capacity
        self.count -= 1
        return True
    
    def Front(self) -> int:
        """
        Get front element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        return self.buffer[self.read_idx]
    
    def Rear(self) -> int:
        """
        Get rear element.
        Time: O(1), Space: O(1)
        """
        if self.isEmpty():
            return -1
        rear_idx = (self.write_idx - 1 + self.capacity) % self.capacity
        return self.buffer[rear_idx]
    
    def isEmpty(self) -> bool:
        """
        Check if empty using count.
        Time: O(1), Space: O(1)
        """
        return self.count == 0
    
    def isFull(self) -> bool:
        """
        Check if full using count.
        Time: O(1), Space: O(1)
        """
        return self.count == self.capacity


# Comprehensive test function
def test_circular_queue():
    """Test all implementations with various scenarios."""
    
    print("Testing Circular Queue implementations...")
    
    # Test each implementation
    for i, QueueClass in enumerate([MyCircularQueue1, MyCircularQueue2, MyCircularQueue3, MyCircularQueue4], 1):
        print(f"\n--- Testing Solution {i}: {QueueClass.__name__} ---")
        
        # Test basic operations
        queue = QueueClass(3)
        
        print(f"isEmpty(): {queue.isEmpty()}")  # True
        print(f"enQueue(1): {queue.enQueue(1)}")  # True
        print(f"enQueue(2): {queue.enQueue(2)}")  # True
        print(f"enQueue(3): {queue.enQueue(3)}")  # True
        print(f"enQueue(4): {queue.enQueue(4)}")  # False (full)
        
        print(f"isFull(): {queue.isFull()}")  # True
        print(f"Rear(): {queue.Rear()}")      # 3
        print(f"Front(): {queue.Front()}")    # 1
        
        print(f"deQueue(): {queue.deQueue()}") # True
        print(f"enQueue(4): {queue.enQueue(4)}")  # True
        print(f"Rear(): {queue.Rear()}")      # 4
        
        # Test edge cases
        print("\n--- Edge Cases ---")
        empty_queue = QueueClass(1)
        print(f"Empty Front(): {empty_queue.Front()}")  # -1
        print(f"Empty Rear(): {empty_queue.Rear()}")    # -1
        print(f"Empty deQueue(): {empty_queue.deQueue()}")  # False


def visualize_operations():
    """Visual demonstration of circular queue operations."""
    print("\n" + "="*50)
    print("VISUAL DEMONSTRATION")
    print("="*50)
    
    queue = MyCircularQueue1(4)
    
    def print_state():
        print(f"Array: {queue.queue}")
        print(f"Head: {queue.head}, Tail: {queue.tail}, Size: {queue.size}")
        print(f"Empty: {queue.isEmpty()}, Full: {queue.isFull()}")
        if not queue.isEmpty():
            print(f"Front: {queue.Front()}, Rear: {queue.Rear()}")
        print("-" * 30)
    
    print("Initial state:")
    print_state()
    
    print("After enQueue(1):")
    queue.enQueue(1)
    print_state()
    
    print("After enQueue(2), enQueue(3):")
    queue.enQueue(2)
    queue.enQueue(3)
    print_state()
    
    print("After enQueue(4) - should be full:")
    queue.enQueue(4)
    print_state()
    
    print("After deQueue() twice:")
    queue.deQueue()
    queue.deQueue()
    print_state()
    
    print("After enQueue(5), enQueue(6) - demonstrating circular nature:")
    queue.enQueue(5)
    queue.enQueue(6)
    print_state()


if __name__ == "__main__":
    test_circular_queue()
    visualize_operations()


"""
INTERVIEW DISCUSSION POINTS:

1. TIME COMPLEXITY: All operations are O(1) for all solutions

2. SPACE COMPLEXITY:
   - Solution 1: O(k) for array + O(1) for size counter
   - Solution 2: O(k+1) for array, no size counter needed
   - Solution 3: O(k) for nodes, truly dynamic
   - Solution 4: O(k) for array, clearer variable naming

3. KEY CONCEPTS TO EXPLAIN:
   - Modular arithmetic for circular indexing: (index + 1) % capacity
   - Distinguishing full vs empty states
   - Why we need head and tail pointers
   - How rear index is calculated: (tail - 1 + capacity) % capacity

4. TRADE-OFFS:
   - Array vs Linked List: Cache locality vs dynamic allocation
   - Size counter vs extra space: Memory vs logic complexity
   - Fixed vs dynamic capacity

5. COMMON PITFALLS TO AVOID:
   - Forgetting modular arithmetic for wrap-around
   - Incorrect rear index calculation
   - Not handling empty queue edge cases
   - Off-by-one errors in full/empty detection

6. FOLLOW-UP QUESTIONS TO EXPECT:
   - "How would you make it thread-safe?"
   - "Can you implement without the size counter?"
   - "What if we need to resize the queue dynamically?"
   - "How would you optimize for cache performance?"

7. IMPLEMENTATION CHOICE FOR INTERVIEW:
   Start with Solution 1 (with size counter) - most intuitive
   If asked to optimize space, show Solution 2
   Mention Solution 3 for dynamic sizing requirements

8. DEBUGGING TIPS:
   - Always test with capacity 1 and 2
   - Test fill-empty-fill cycles
   - Verify wrap-around behavior
   - Check edge cases (empty Front/Rear calls)
"""
