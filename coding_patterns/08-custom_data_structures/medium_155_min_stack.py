class MinStack:
    """
    Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

    The key insight is to maintain a parallel stack that tracks the minimum value at each level.
    This allows us to achieve O(1) time complexity for all operations including getMin().

    Approach:
    - Use two stacks: one for actual values, another for tracking minimums
    - For each push operation, store the current minimum in the min_stack
    - Both stacks grow and shrink together, maintaining synchronization

    Time Complexity: O(1) for all operations - push, pop, top, getMin
    Space Complexity: O(n) where n is the number of elements in the stack
    """

    def __init__(self):
        """
        Initialize the MinStack data structure.
        """
        # Main stack to store actual values
        self.stack = []
        # Auxiliary stack to track minimum values at each level
        self.min_stack = []

    def push(self, val: int) -> None:
        """
        Push element val onto the stack.

        Args:
            val: The integer value to push onto the stack
        """
        # Add value to main stack
        self.stack.append(val)

        # Add current minimum to min_stack
        if not self.min_stack:
            # First element is the minimum by default
            self.min_stack.append(val)
        else:
            # Store the smaller of current value and previous minimum
            current_min = min(val, self.min_stack[-1])
            self.min_stack.append(current_min)

    def pop(self) -> None:
        """
        Remove the element on the top of the stack.
        """
        # Remove from both stacks to maintain synchronization
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """
        Get the top element of the stack.

        Returns:
            The top element of the stack
        """
        return self.stack[-1]

    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack in constant time.

        Returns:
            The minimum element currently in the stack
        """
        return self.min_stack[-1]


# Alternative space-optimized implementation
class MinStackOptimized:
    """
    Space-optimized version that only stores minimum values when they change.

    This approach saves space by storing tuples of (value, minimum) only when
    a new minimum is encountered, rather than storing the minimum for every element.

    Time Complexity: O(1) for all operations
    Space Complexity: O(n) in worst case, but typically better than the basic approach
    """

    def __init__(self):
        """
        Initialize the optimized MinStack.
        """
        self.stack = []
        self.current_min = None

    def push(self, val: int) -> None:
        """
        Push element val onto the stack.

        Args:
            val: The integer value to push onto the stack
        """
        if self.current_min is None or val <= self.current_min:
            # Store both the old minimum and the new value
            if self.current_min is not None:
                self.stack.append(self.current_min)
            self.stack.append(val)
            self.current_min = val
        else:
            # Just store the value
            self.stack.append(val)

    def pop(self) -> None:
        """
        Remove the element on the top of the stack.
        """
        if self.stack[-1] == self.current_min:
            # Popping the minimum element
            self.stack.pop()
            if self.stack:
                # The previous minimum is now on top
                self.current_min = self.stack.pop()
            else:
                self.current_min = None
        else:
            self.stack.pop()

    def top(self) -> int:
        """
        Get the top element of the stack.

        Returns:
            The top element of the stack
        """
        return self.stack[-1]

    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack.

        Returns:
            The minimum element currently in the stack
        """
        return self.current_min


# Usage example:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
