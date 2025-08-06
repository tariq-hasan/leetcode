# LeetCode 155: Min Stack
# Design a stack that supports push, pop, top, and retrieving minimum element in constant time.

"""
Problem: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.
"""

# SOLUTION 1: Two Stacks Approach (Most Common Interview Answer)
class MinStack1:
    def __init__(self):
        """
        Initialize two stacks:
        - stack: stores all elements
        - min_stack: stores minimum values at each level
        """
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        """
        Push element onto stack and update minimum stack.
        Time: O(1), Space: O(1) per operation
        """
        self.stack.append(val)
        
        # If min_stack is empty or current val is <= current minimum
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        """
        Pop element from stack and update minimum stack if needed.
        Time: O(1), Space: O(1) per operation
        """
        if self.stack:
            popped = self.stack.pop()
            # If popped element was the minimum, remove it from min_stack
            if self.min_stack and popped == self.min_stack[-1]:
                self.min_stack.pop()
    
    def top(self) -> int:
        """
        Get top element of stack.
        Time: O(1), Space: O(1)
        """
        return self.stack[-1] if self.stack else None
    
    def getMin(self) -> int:
        """
        Get minimum element in stack.
        Time: O(1), Space: O(1)
        """
        return self.min_stack[-1] if self.min_stack else None


# SOLUTION 2: Single Stack with Tuples (Space Efficient)
class MinStack2:
    def __init__(self):
        """
        Use single stack storing tuples of (value, min_so_far)
        """
        self.stack = []
    
    def push(self, val: int) -> None:
        """
        Push tuple of (val, current_minimum) onto stack.
        Time: O(1), Space: O(1) per operation
        """
        if not self.stack:
            self.stack.append((val, val))
        else:
            current_min = min(val, self.stack[-1][1])
            self.stack.append((val, current_min))
    
    def pop(self) -> None:
        """
        Pop tuple from stack.
        Time: O(1), Space: O(1)
        """
        if self.stack:
            self.stack.pop()
    
    def top(self) -> int:
        """
        Get value from top tuple.
        Time: O(1), Space: O(1)
        """
        return self.stack[-1][0] if self.stack else None
    
    def getMin(self) -> int:
        """
        Get minimum from top tuple.
        Time: O(1), Space: O(1)
        """
        return self.stack[-1][1] if self.stack else None


# SOLUTION 3: Optimized Two Stacks (Memory Efficient)
class MinStack3:
    def __init__(self):
        """
        Optimized version that only stores minimums when they change.
        """
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        """
        Only push to min_stack when we have a new minimum.
        Time: O(1), Space: O(1) per operation (better average case)
        """
        self.stack.append(val)
        
        # Only store if it's a new minimum or equal to current minimum
        if not self.min_stack or val <= self.getMin():
            self.min_stack.append(val)
    
    def pop(self) -> None:
        """
        Pop from min_stack only if we're removing the current minimum.
        Time: O(1), Space: O(1)
        """
        if self.stack:
            popped = self.stack.pop()
            if self.min_stack and popped == self.getMin():
                self.min_stack.pop()
    
    def top(self) -> int:
        """
        Get top element.
        Time: O(1), Space: O(1)
        """
        return self.stack[-1] if self.stack else None
    
    def getMin(self) -> int:
        """
        Get current minimum.
        Time: O(1), Space: O(1)
        """
        return self.min_stack[-1] if self.min_stack else None


# SOLUTION 4: Single Stack with Difference Tracking (Advanced)
class MinStack4:
    def __init__(self):
        """
        Advanced solution using difference from minimum.
        Saves space but more complex logic.
        """
        self.stack = []
        self.min_val = None
    
    def push(self, val: int) -> None:
        """
        Store difference from minimum value.
        Time: O(1), Space: O(1) per operation
        """
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            # Store difference from current minimum
            diff = val - self.min_val
            self.stack.append(diff)
            
            # Update minimum if new value is smaller
            if val < self.min_val:
                self.min_val = val
    
    def pop(self) -> None:
        """
        Pop and update minimum if necessary.
        Time: O(1), Space: O(1)
        """
        if self.stack:
            diff = self.stack.pop()
            
            # If diff < 0, the popped element was the minimum
            if diff < 0:
                # Restore previous minimum
                self.min_val = self.min_val - diff
    
    def top(self) -> int:
        """
        Calculate top element from difference.
        Time: O(1), Space: O(1)
        """
        if not self.stack:
            return None
        
        diff = self.stack[-1]
        if diff < 0:
            return self.min_val
        else:
            return self.min_val + diff
    
    def getMin(self) -> int:
        """
        Return stored minimum.
        Time: O(1), Space: O(1)
        """
        return self.min_val


# Test cases and usage examples
def test_min_stack():
    """Test all implementations with example cases."""
    
    print("Testing MinStack implementations...")
    
    # Test each implementation
    for i, MinStackClass in enumerate([MinStack1, MinStack2, MinStack3, MinStack4], 1):
        print(f"\n--- Testing Solution {i} ---")
        
        stack = MinStackClass()
        
        # Test case from LeetCode
        stack.push(-2)
        stack.push(0)
        stack.push(-3)
        
        print(f"getMin(): {stack.getMin()}")  # Should be -3
        
        stack.pop()
        print(f"top(): {stack.top()}")        # Should be 0
        print(f"getMin(): {stack.getMin()}")  # Should be -2
        
        # Additional test case
        stack.push(-1)
        print(f"getMin(): {stack.getMin()}")  # Should be -2
        print(f"top(): {stack.top()}")        # Should be -1

if __name__ == "__main__":
    test_min_stack()


"""
INTERVIEW DISCUSSION POINTS:

1. TIME COMPLEXITY: All operations are O(1) for all solutions

2. SPACE COMPLEXITY:
   - Solution 1 (Two Stacks): O(n) worst case, O(n) average
   - Solution 2 (Tuples): O(n) always (stores min with each element)
   - Solution 3 (Optimized): O(n) worst case, better average case
   - Solution 4 (Difference): O(n) for stack, O(1) extra space

3. TRADE-OFFS:
   - Solution 1: Most intuitive and commonly expected
   - Solution 2: Simple but uses more memory
   - Solution 3: Memory efficient for many duplicate minimums
   - Solution 4: Most space-efficient but complex logic

4. FOLLOW-UP QUESTIONS TO EXPECT:
   - "Can you optimize for space?"
   - "What if we have many duplicate minimums?"
   - "How would you handle integer overflow?" (for Solution 4)
   - "Can you implement without using extra space proportional to input?"

5. IMPLEMENTATION CHOICE FOR INTERVIEW:
   Start with Solution 1 (two stacks) as it's most straightforward.
   If asked to optimize, mention Solution 3 or 4.
"""
