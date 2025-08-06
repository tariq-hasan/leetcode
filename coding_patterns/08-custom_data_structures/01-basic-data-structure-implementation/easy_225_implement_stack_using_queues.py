"""
LeetCode 225: Implement Stack using Queues

Implement a last-in-first-out (LIFO) stack using only queues.
The implemented stack should support all the functions of a normal stack:
- push(x): Push element x to the top of the stack
- pop(): Remove and return the top element of the stack
- top(): Return the top element of the stack
- empty(): Return true if the stack is empty, false otherwise

Notes:
- You must use only standard operations of a queue (push to back, peek/pop from front, size, empty)
- Depending on your language, the queue may not be supported natively

Example:
stack = MyStack()
stack.push(1)
stack.push(2)
stack.top()    # returns 2
stack.pop()    # returns 2
stack.empty()  # returns False
"""

from collections import deque

# Solution 1: Two Queues - Push O(n), Pop O(1) - RECOMMENDED for interviews
class MyStack1:
    """
    Approach: Use two queues, make push operation expensive
    
    Key idea: Always keep the main queue in reverse order (stack order)
    Push: O(n) - need to reverse the queue
    Pop: O(1) - just dequeue from front
    Top: O(1) - peek front
    Empty: O(1) - check if queue empty
    """
    
    def __init__(self):
        self.q1 = deque()  # Main queue (stores elements in stack order)
        self.q2 = deque()  # Helper queue for push operation
    
    def push(self, x: int) -> None:
        """
        Push element to top of stack
        Strategy: Add new element to empty queue, then move all existing elements
        """
        # Step 1: Add new element to empty helper queue
        self.q2.append(x)
        
        # Step 2: Move all elements from main queue to helper queue
        while self.q1:
            self.q2.append(self.q1.popleft())
        
        # Step 3: Swap the queues (helper becomes main)
        self.q1, self.q2 = self.q2, self.q1
    
    def pop(self) -> int:
        """Remove and return top element"""
        if self.empty():
            raise IndexError("pop from empty stack")
        return self.q1.popleft()
    
    def top(self) -> int:
        """Return top element without removing it"""
        if self.empty():
            raise IndexError("top from empty stack")
        return self.q1[0]
    
    def empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.q1) == 0


# Solution 2: One Queue - Push O(n), Pop O(1)
class MyStack2:
    """
    Approach: Use only one queue, rotate during push
    
    More space efficient but same time complexity
    Push: O(n) - rotate queue after adding element
    Pop: O(1) - dequeue from front
    Top: O(1) - peek front  
    Empty: O(1) - check if queue empty
    """
    
    def __init__(self):
        self.queue = deque()
    
    def push(self, x: int) -> None:
        """
        Push element and rotate queue to maintain stack order
        """
        # Add element to back
        self.queue.append(x)
        
        # Rotate queue so new element is at front
        # Move all elements that were before the new element to the back
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())
    
    def pop(self) -> int:
        """Remove and return top element"""
        if self.empty():
            raise IndexError("pop from empty stack")
        return self.queue.popleft()
    
    def top(self) -> int:
        """Return top element without removing it"""
        if self.empty():
            raise IndexError("top from empty stack")
        return self.queue[0]
    
    def empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.queue) == 0


# Solution 3: Two Queues - Pop O(n), Push O(1)
class MyStack3:
    """
    Alternative approach: Make pop expensive instead of push
    
    Push: O(1) - just add to queue
    Pop: O(n) - need to move elements to get last one
    Top: O(n) - need to find last element
    Empty: O(1) - check if queue empty
    
    Generally less preferred since pop/top are more frequent operations
    """
    
    def __init__(self):
        self.q1 = deque()  # Main queue
        self.q2 = deque()  # Helper queue
    
    def push(self, x: int) -> None:
        """Simply add to back of queue"""
        self.q1.append(x)
    
    def pop(self) -> int:
        """
        Move all elements except last to helper queue,
        pop the last element, then move everything back
        """
        if self.empty():
            raise IndexError("pop from empty stack")
        
        # Move all but last element to helper queue
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        
        # Get the last element (top of stack)
        result = self.q1.popleft()
        
        # Move everything back to main queue
        self.q1, self.q2 = self.q2, self.q1
        
        return result
    
    def top(self) -> int:
        """
        Similar to pop but put the element back
        """
        if self.empty():
            raise IndexError("top from empty stack")
        
        # Move all but last element to helper queue
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        
        # Get the last element (top of stack)
        result = self.q1[0]
        
        # Move the top element to helper queue too
        self.q2.append(self.q1.popleft())
        
        # Swap queues
        self.q1, self.q2 = self.q2, self.q1
        
        return result
    
    def empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.q1) == 0


# Solution 4: Using Python list as queue (for demonstration)
class MyStack4:
    """
    Using Python list to simulate queue operations
    Note: This is less efficient as list.pop(0) is O(n)
    Only for educational purposes - don't use in real interviews
    """
    
    def __init__(self):
        self.queue = []
    
    def push(self, x: int) -> None:
        """Add element and rotate to maintain stack order"""
        self.queue.append(x)
        # Rotate: move all previous elements to back
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.pop(0))
    
    def pop(self) -> int:
        """Remove from front"""
        if self.empty():
            raise IndexError("pop from empty stack")
        return self.queue.pop(0)
    
    def top(self) -> int:
        """Peek front"""
        if self.empty():
            raise IndexError("top from empty stack")
        return self.queue[0]
    
    def empty(self) -> bool:
        """Check if empty"""
        return len(self.queue) == 0


def test_stack_implementation():
    """Test all stack implementations"""
    
    implementations = [
        ("Two Queues - Push O(n)", MyStack1),
        ("One Queue - Push O(n)", MyStack2),
        ("Two Queues - Pop O(n)", MyStack3),
        ("List as Queue", MyStack4)
    ]
    
    test_operations = [
        ("push", 1),
        ("push", 2),
        ("push", 3),
        ("top", None),    # Should return 3
        ("pop", None),    # Should return 3
        ("top", None),    # Should return 2
        ("pop", None),    # Should return 2
        ("empty", None),  # Should return False
        ("pop", None),    # Should return 1
        ("empty", None),  # Should return True
    ]
    
    for name, StackClass in implementations:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        
        stack = StackClass()
        
        for operation, value in test_operations:
            try:
                if operation == "push":
                    stack.push(value)
                    print(f"push({value}) -> Stack state updated")
                elif operation == "pop":
                    result = stack.pop()
                    print(f"pop() -> {result}")
                elif operation == "top":
                    result = stack.top()
                    print(f"top() -> {result}")
                elif operation == "empty":
                    result = stack.empty()
                    print(f"empty() -> {result}")
            except IndexError as e:
                print(f"{operation}() -> Error: {e}")


def demonstrate_push_process():
    """
    Demonstrate step-by-step how push works in Solution 1 (Two Queues)
    """
    print("\n" + "="*60)
    print("STEP-BY-STEP PUSH DEMONSTRATION (Two Queues)")
    print("="*60)
    
    stack = MyStack1()
    
    def print_state():
        print(f"q1: {list(stack.q1)}")
        print(f"q2: {list(stack.q2)}")
        print()
    
    print("Initial state:")
    print_state()
    
    print("push(1):")
    print("1. Add 1 to q2")
    stack.q2.append(1)
    print_state()
    print("2. q1 is empty, so swap q1 and q2")
    stack.q1, stack.q2 = stack.q2, stack.q1
    print_state()
    
    print("push(2):")
    print("1. Add 2 to q2")
    stack.q2.append(2)
    print_state()
    print("2. Move all elements from q1 to q2")
    while stack.q1:
        stack.q2.append(stack.q1.popleft())
    print_state()
    print("3. Swap q1 and q2")
    stack.q1, stack.q2 = stack.q2, stack.q1
    print_state()
    
    print("push(3):")
    print("1. Add 3 to q2")
    stack.q2.append(3)
    print_state()
    print("2. Move all elements from q1 to q2")
    while stack.q1:
        stack.q2.append(stack.q1.popleft())
    print_state()
    print("3. Swap q1 and q2")
    stack.q1, stack.q2 = stack.q2, stack.q1
    print_state()
    
    print("Final stack order (front to back of q1): [3, 2, 1]")
    print("pop() will return 3, then 2, then 1 (LIFO order)")


if __name__ == "__main__":
    test_stack_implementation()
    demonstrate_push_process()


"""
INTERVIEW STRATEGY:

1. Problem Understanding (2-3 minutes):
   - "I need to implement LIFO (stack) using FIFO (queue) operations"
   - "Stack: push/pop from same end. Queue: push to back, pop from front"
   - "Key challenge: How to access the 'back' element of a queue?"

2. Approach Discussion (5-7 minutes):
   - Present both approaches:
     * Make push expensive: O(n) push, O(1) pop
     * Make pop expensive: O(1) push, O(n) pop
   - "Which is better? Depends on usage pattern, but usually push expensive is preferred"
   - "Why? Pop/top operations are typically more frequent"

3. Implementation Choice (8-10 minutes):
   - Recommend Solution 1 (Two Queues, Push O(n))
   - Walk through the push algorithm step by step
   - Show how it maintains stack order in the main queue

4. Optimization Discussion (2-3 minutes):
   - "Can use one queue instead of two with rotation"
   - "Same time complexity but saves space"

5. Complexity Analysis:
   - Time: O(n) for push, O(1) for pop/top/empty
   - Space: O(n) for storing elements

KEY INSIGHTS TO MENTION:
- "The trick is to maintain elements in reverse order in the queue"
- "We reverse the queue after every push to simulate stack behavior"
- "Queue gives us FIFO, we want LIFO, so we reverse the order"

FOLLOW-UP QUESTIONS:
- "What if push is more frequent than pop?" → Consider pop-expensive approach
- "Can you implement queue using stacks?" → Yes, reverse problem
- "What about thread safety?" → Would need synchronization
- "Space optimization?" → Single queue approach

COMMON MISTAKES:
- Forgetting to handle empty stack cases
- Not understanding that we need to reverse the queue order
- Confusing which operation should be expensive
"""
