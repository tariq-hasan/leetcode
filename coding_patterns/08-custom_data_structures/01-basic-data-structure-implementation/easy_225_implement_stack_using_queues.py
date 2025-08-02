from collections import deque

# SOLUTION 1: Two Queues - Push O(n), Pop O(1) 
# This is the most common approach asked in interviews
class MyStack:
    def __init__(self):
        self.q1 = deque()  # Main queue
        self.q2 = deque()  # Helper queue
        
    def push(self, x: int) -> None:
        # Add new element to q2
        self.q2.append(x)
        
        # Move all elements from q1 to q2
        while self.q1:
            self.q2.append(self.q1.popleft())
        
        # Swap q1 and q2 so q1 is always the main queue
        self.q1, self.q2 = self.q2, self.q1
        
    def pop(self) -> int:
        return self.q1.popleft()
        
    def top(self) -> int:
        return self.q1[0]
        
    def empty(self) -> bool:
        return len(self.q1) == 0


# SOLUTION 2: One Queue - Push O(n), Pop O(1)
# More space efficient, also commonly asked
class MyStackOneQueue:
    def __init__(self):
        self.q = deque()
        
    def push(self, x: int) -> None:
        size = len(self.q)
        self.q.append(x)
        
        # Rotate the queue so the new element is at front
        for _ in range(size):
            self.q.append(self.q.popleft())
            
    def pop(self) -> int:
        return self.q.popleft()
        
    def top(self) -> int:
        return self.q[0]
        
    def empty(self) -> bool:
        return len(self.q) == 0


# SOLUTION 3: Two Queues - Push O(1), Pop O(n)
# Alternative approach, less common but good to know
class MyStackPushOptimized:
    def __init__(self):
        self.q1 = deque()  # Main queue
        self.q2 = deque()  # Helper queue
        
    def push(self, x: int) -> None:
        self.q1.append(x)
        
    def pop(self) -> int:
        # Move all but last element to q2
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        
        # Pop the last element (top of stack)
        result = self.q1.popleft()
        
        # Swap queues
        self.q1, self.q2 = self.q2, self.q1
        
        return result
        
    def top(self) -> int:
        # Move all but last element to q2
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        
        # Get the last element
        result = self.q1[0]
        self.q2.append(self.q1.popleft())
        
        # Swap queues
        self.q1, self.q2 = self.q2, self.q1
        
        return result
        
    def empty(self) -> bool:
        return len(self.q1) == 0


# Test all solutions
def test_stack_implementations():
    print("Testing Solution 1: Two Queues (Push O(n), Pop O(1))")
    stack1 = MyStack()
    stack1.push(1)
    stack1.push(2)
    print(f"top(): {stack1.top()}")  # 2
    print(f"pop(): {stack1.pop()}")  # 2
    print(f"empty(): {stack1.empty()}")  # False
    print()
    
    print("Testing Solution 2: One Queue (Push O(n), Pop O(1))")
    stack2 = MyStackOneQueue()
    stack2.push(1)
    stack2.push(2)
    print(f"top(): {stack2.top()}")  # 2
    print(f"pop(): {stack2.pop()}")  # 2
    print(f"empty(): {stack2.empty()}")  # False
    print()
    
    print("Testing Solution 3: Two Queues (Push O(1), Pop O(n))")
    stack3 = MyStackPushOptimized()
    stack3.push(1)
    stack3.push(2)
    print(f"top(): {stack3.top()}")  # 2
    print(f"pop(): {stack3.pop()}")  # 2
    print(f"empty(): {stack3.empty()}")  # False

test_stack_implementations()

# INTERVIEW TALKING POINTS:

"""
Key Discussion Points for Interviews:

1. APPROACH COMPARISON:
   - Solution 1 & 2: Push O(n), Pop O(1) - Better for pop-heavy workloads
   - Solution 3: Push O(1), Pop O(n) - Better for push-heavy workloads

2. TRADE-OFFS:
   - Time vs Space: One queue saves space but same time complexity
   - Operation frequency: Choose based on which operation is more frequent

3. WHY QUEUES ARE HARDER FOR STACK:
   - Queue: FIFO (First In, First Out)
   - Stack: LIFO (Last In, First Out)
   - Need to reverse the order, hence the complexity

4. FOLLOW-UP QUESTIONS TO EXPECT:
   - "What if we used a list instead of deque?" (Discuss O(n) for popleft)
   - "How would you implement queue using stacks?" (Reverse problem)
   - "Which approach would you choose in production?" (Depends on usage pattern)

5. OPTIMIZATION NOTES:
   - deque is preferred over list for O(1) popleft operations
   - Could use two lists but popleft would be O(n)
   - In practice, just use a list for stack implementation
"""
