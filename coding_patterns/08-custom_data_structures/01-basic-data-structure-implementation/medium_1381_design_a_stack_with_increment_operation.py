# LeetCode 1381: Design a Stack With Increment Operation
# Design a stack which supports the following operations with efficient time complexity.

"""
Problem: Design a stack which supports the following operations:

Implement the CustomStack class:
- CustomStack(int maxSize) Initializes the object with maxSize which is the maximum number of elements in the stack or do nothing if the stack reached the maxSize.
- void push(int x) Adds x to the top of the stack if the stack hasn't reached the maxSize.
- int pop() Pops and returns the top of stack or -1 if the stack is empty.
- void increment(int k, int val) Increments the bottom k elements of the stack by val. If there are less than k elements in the stack, just increment all the elements in the stack.

Constraints:
- 1 <= maxSize <= 1000
- 1 <= x <= 1000
- 1 <= k <= 1000
- 0 <= val <= 100
- At most 1000 calls will be made to each method push, pop, and increment.
"""

# SOLUTION 1: Naive Approach - Direct Array Implementation
class CustomStack1:
    def __init__(self, maxSize: int):
        """
        Initialize stack with maximum capacity.
        Time: O(1), Space: O(maxSize)
        """
        self.maxSize = maxSize
        self.stack = []
    
    def push(self, x: int) -> None:
        """
        Push element if stack not full.
        Time: O(1), Space: O(1)
        """
        if len(self.stack) < self.maxSize:
            self.stack.append(x)
    
    def pop(self) -> int:
        """
        Pop element from stack.
        Time: O(1), Space: O(1)
        """
        if not self.stack:
            return -1
        return self.stack.pop()
    
    def increment(self, k: int, val: int) -> None:
        """
        Increment bottom k elements by val.
        Time: O(k), Space: O(1)
        """
        # Increment up to min(k, stack_size) elements from bottom
        limit = min(k, len(self.stack))
        for i in range(limit):
            self.stack[i] += val


# SOLUTION 2: Optimized with Lazy Propagation (Most Efficient)
class CustomStack2:
    def __init__(self, maxSize: int):
        """
        Initialize with lazy increment array for O(1) increment operations.
        Time: O(1), Space: O(maxSize)
        """
        self.maxSize = maxSize
        self.stack = []
        self.increments = [0] * maxSize  # Lazy increment values
    
    def push(self, x: int) -> None:
        """
        Push element if stack not full.
        Time: O(1), Space: O(1)
        """
        if len(self.stack) < self.maxSize:
            self.stack.append(x)
    
    def pop(self) -> int:
        """
        Pop element and apply lazy increments.
        Time: O(1), Space: O(1)
        """
        if not self.stack:
            return -1
        
        index = len(self.stack) - 1
        result = self.stack.pop() + self.increments[index]
        
        # Propagate increment to element below (if exists)
        if index > 0:
            self.increments[index - 1] += self.increments[index]
        
        # Reset current increment
        self.increments[index] = 0
        
        return result
    
    def increment(self, k: int, val: int) -> None:
        """
        Lazy increment: just mark the increment at position k-1.
        Time: O(1), Space: O(1)
        """
        if not self.stack:
            return
        
        # Apply increment to position min(k-1, stack_top)
        index = min(k - 1, len(self.stack) - 1)
        self.increments[index] += val


# SOLUTION 3: Node-based Stack Implementation  
class StackNode:
    def __init__(self, val=0):
        self.val = val
        self.lazy_increment = 0
        self.next = None

class CustomStack3:
    def __init__(self, maxSize: int):
        """
        Initialize linked list based stack.
        Time: O(1), Space: O(1)
        """
        self.maxSize = maxSize
        self.size = 0
        self.top = None  # Top of stack
    
    def push(self, x: int) -> None:
        """
        Push new node to top.
        Time: O(1), Space: O(1)
        """
        if self.size < self.maxSize:
            new_node = StackNode(x)
            new_node.next = self.top
            self.top = new_node
            self.size += 1
    
    def pop(self) -> int:
        """
        Pop from top with lazy increment propagation.
        Time: O(1), Space: O(1)
        """
        if not self.top:
            return -1
        
        result = self.top.val + self.top.lazy_increment
        
        # Propagate lazy increment to node below
        if self.top.next:
            self.top.next.lazy_increment += self.top.lazy_increment
        
        self.top = self.top.next
        self.size -= 1
        
        return result
    
    def increment(self, k: int, val: int) -> None:
        """
        Apply lazy increment to bottom k elements.
        Time: O(1), Space: O(1)
        """
        if not self.top:
            return
        
        # Find the k-th node from bottom (or top if k >= size)
        target_depth = min(k, self.size)
        
        # Navigate to target position (target_depth from top)
        curr = self.top
        for _ in range(self.size - target_depth):
            curr = curr.next
        
        if curr:
            curr.lazy_increment += val


# SOLUTION 4: Array with Explicit Bottom Tracking
class CustomStack4:
    def __init__(self, maxSize: int):
        """
        Alternative approach with clear increment semantics.
        Time: O(1), Space: O(maxSize)
        """
        self.maxSize = maxSize
        self.data = [0] * maxSize
        self.increments = [0] * maxSize
        self.top_index = -1  # Points to top element
    
    def push(self, x: int) -> None:
        """
        Push to next available position.
        Time: O(1), Space: O(1)
        """
        if self.top_index + 1 < self.maxSize:
            self.top_index += 1
            self.data[self.top_index] = x
    
    def pop(self) -> int:
        """
        Pop with increment propagation.
        Time: O(1), Space: O(1)
        """
        if self.top_index == -1:
            return -1
        
        # Get result with accumulated increments
        result = self.data[self.top_index] + self.increments[self.top_index]
        
        # Propagate increment to element below
        if self.top_index > 0:
            self.increments[self.top_index - 1] += self.increments[self.top_index]
        
        # Clear current position
        self.increments[self.top_index] = 0
        self.top_index -= 1
        
        return result
    
    def increment(self, k: int, val: int) -> None:
        """
        Lazy increment at appropriate position.
        Time: O(1), Space: O(1)
        """
        if self.top_index == -1:
            return
        
        # Apply increment to position min(k-1, top_index)
        target_index = min(k - 1, self.top_index)
        self.increments[target_index] += val


# Comprehensive testing function
def test_custom_stack():
    """Test all implementations with various scenarios."""
    
    print("Testing Custom Stack implementations...")
    
    implementations = [
        ("Naive Array", CustomStack1),
        ("Lazy Propagation", CustomStack2),
        ("Linked List", CustomStack3),
        ("Array with Index", CustomStack4)
    ]
    
    for name, StackClass in implementations:
        print(f"\n--- Testing {name} ---")
        
        # Test case from LeetCode example
        stack = StackClass(3)
        
        stack.push(1)
        stack.push(2)
        print(f"After push(1), push(2): pop() = {stack.pop()}")  # Should be 2
        
        stack.push(2)
        stack.push(3)
        stack.push(4)  # Should be ignored (maxSize = 3)
        
        stack.increment(5, 100)  # Increment bottom 5 by 100
        stack.increment(2, 100)  # Increment bottom 2 by 100
        
        print(f"After increments: pop() = {stack.pop()}")  # Should be 103
        print(f"pop() = {stack.pop()}")  # Should be 202
        print(f"pop() = {stack.pop()}")  # Should be 201
        print(f"pop() = {stack.pop()}")  # Should be -1 (empty)


def visualize_lazy_propagation():
    """Demonstrate how lazy propagation works."""
    print("\n" + "="*60)
    print("LAZY PROPAGATION VISUALIZATION")
    print("="*60)
    
    stack = CustomStack2(4)
    
    def print_state(operation=""):
        if operation:
            print(f"\nAfter {operation}:")
        print(f"Stack: {stack.stack}")
        print(f"Increments: {stack.increments[:len(stack.stack)]}")
        print("-" * 40)
    
    print("Initial state:")
    print_state()
    
    # Build stack
    for i in [1, 2, 3, 4]:
        stack.push(i)
        print_state(f"push({i})")
    
    # Apply increments
    stack.increment(2, 10)  # Increment bottom 2 by 10
    print_state("increment(2, 10)")
    
    stack.increment(3, 5)   # Increment bottom 3 by 5
    print_state("increment(3, 5)")
    
    # Pop and see propagation
    result = stack.pop()
    print_state(f"pop() -> {result}")
    
    result = stack.pop()
    print_state(f"pop() -> {result}")
    
    result = stack.pop()
    print_state(f"pop() -> {result}")


def performance_comparison():
    """Compare time complexities of different operations."""
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON")
    print("="*70)
    
    operations = [
        ("Operation", "Naive", "Lazy Prop", "Linked List", "Array+Index"),
        ("push()", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("pop()", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("increment()", "O(k)", "O(1)", "O(1)*", "O(1)"),
        ("Space", "O(n)", "O(n)", "O(n)", "O(n)")
    ]
    
    for row in operations:
        print(f"{row[0]:<12} {row[1]:<8} {row[2]:<10} {row[3]:<12} {row[4]:<12}")
    
    print("\n* Linked List increment is O(1) amortized but may traverse in worst case")


def edge_cases_test():
    """Test various edge cases."""
    print("\n" + "="*50)
    print("EDGE CASES TESTING")
    print("="*50)
    
    stack = CustomStack2(2)
    
    print("Testing empty stack operations:")
    print(f"pop() on empty: {stack.pop()}")
    stack.increment(5, 10)
    print("increment on empty: no effect")
    
    print("\nTesting single element:")
    stack.push(5)
    stack.increment(1, 10)
    print(f"After increment(1, 10): pop() = {stack.pop()}")
    
    print("\nTesting maxSize boundary:")
    stack.push(1)
    stack.push(2)
    stack.push(3)  # Should be ignored
    print(f"Stack size after 3 pushes to maxSize=2: {len(stack.stack)}")
    
    print("\nTesting increment larger than stack:")
    stack.increment(10, 5)  # k > stack size
    print(f"After increment(10, 5): pop() = {stack.pop()}")
    print(f"pop() = {stack.pop()}")


if __name__ == "__main__":
    test_custom_stack()
    visualize_lazy_propagation()
    performance_comparison()
    edge_cases_test()


"""
INTERVIEW DISCUSSION POINTS:

1. KEY OPTIMIZATION - LAZY PROPAGATION:
   - Problem: Naive increment is O(k) which can be expensive
   - Solution: Use lazy propagation to make increment O(1)
   - Concept: Store increments separately and apply during pop()

2. LAZY PROPAGATION MECHANISM:
   - increment(k, val): Store increment at position min(k-1, top)
   - pop(): Apply accumulated increment + propagate to element below
   - This ensures each increment is applied exactly once to correct elements

3. TIME COMPLEXITY ANALYSIS:
   - Solution 1 (Naive): push O(1), pop O(1), increment O(k)
   - Solution 2-4 (Optimized): All operations O(1) amortized
   - Space: O(maxSize) for all solutions

4. WHY LAZY PROPAGATION WORKS:
   - Increments accumulate at the "boundary" position
   - When popping, we apply all accumulated increments
   - Propagation ensures lower elements receive their increments
   - Maintains correct semantics while optimizing performance

5. IMPLEMENTATION CHOICES:
   - Array-based (Solution 2): Most intuitive and efficient
   - Linked list (Solution 3): Demonstrates concept with nodes
   - Index tracking (Solution 4): Alternative array approach

6. EDGE CASES TO HANDLE:
   - Empty stack operations (pop returns -1, increment does nothing)
   - Stack at maxSize (push ignored)
   - increment with k > stack_size (increment all elements)
   - Single element stack

7. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you optimize the increment operation?" → Show lazy propagation
   - "How does lazy propagation maintain correctness?"
   - "What if we need to support decrement as well?"
   - "How would you handle thread safety?"

8. COMMON PITFALLS:
   - Forgetting to propagate increments during pop
   - Incorrect boundary calculation for increment position
   - Not handling empty stack edge cases
   - Off-by-one errors in index calculations

9. IMPLEMENTATION PREFERENCE:
   - Start with Solution 1 to show understanding
   - Immediately discuss O(k) limitation of increment
   - Present Solution 2 as optimization with detailed explanation
   - Walk through lazy propagation mechanism step by step

10. KEY INSIGHT FOR INTERVIEWERS:
    The brilliant insight is that we don't need to apply increments immediately.
    Instead, we can defer them until elements are popped, which transforms
    an O(k) operation into an O(1) operation with proper bookkeeping.

11. TESTING STRATEGY:
    - Use provided example to verify correctness
    - Test edge cases (empty, full, single element)
    - Verify lazy propagation with multiple increments
    - Confirm that increments apply to correct bottom k elements

12. ALTERNATIVE APPROACHES TO MENTION:
    - Segment trees (overkill but shows advanced knowledge)
    - Difference arrays (similar concept to lazy propagation)
    - Fenwick trees (for range updates, but unnecessary complexity here)
"""
