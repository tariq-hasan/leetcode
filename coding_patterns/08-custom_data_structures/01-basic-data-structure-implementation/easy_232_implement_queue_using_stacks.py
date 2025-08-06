"""
LeetCode 232: Implement Queue using Stacks

Implement a first-in-first-out (FIFO) queue using only stacks.
The implemented queue should support all the functions of a normal queue:
- push(x): Push element x to the back of the queue
- pop(): Remove and return the element from the front of the queue
- peek(): Return the element at the front of the queue
- empty(): Return true if the queue is empty, false otherwise

Notes:
- You must use only standard operations of a stack (push, pop, top, empty)
- You can assume all operations are valid (no pop/peek on empty queue)

Example:
queue = MyQueue()
queue.push(1)
queue.push(2)
queue.peek()   # returns 1
queue.pop()    # returns 1
queue.empty()  # returns False
"""

# Solution 1: Two Stacks with Lazy Transfer - OPTIMAL & RECOMMENDED
class MyQueue1:
    """
    Approach: Use two stacks with lazy transfer strategy
    
    Key insight: Only transfer from input to output when output is empty
    This amortizes the cost of transfers across operations.
    
    Push: O(1) - always push to input stack
    Pop: O(1) amortized - occasionally O(n) when transferring
    Peek: O(1) amortized - occasionally O(n) when transferring
    Empty: O(1) - check both stacks
    
    Space: O(n) - store n elements across two stacks
    """
    
    def __init__(self):
        self.input_stack = []   # For push operations
        self.output_stack = []  # For pop/peek operations
    
    def push(self, x: int) -> None:
        """
        Push element to back of queue
        Always push to input stack - O(1)
        """
        self.input_stack.append(x)
    
    def pop(self) -> int:
        """
        Remove and return element from front of queue
        Amortized O(1) - each element is moved at most once
        """
        self._ensure_output_has_elements()
        return self.output_stack.pop()
    
    def peek(self) -> int:
        """
        Return element at front of queue without removing
        Amortized O(1) - same as pop but don't remove
        """
        self._ensure_output_has_elements()
        return self.output_stack[-1]
    
    def empty(self) -> bool:
        """
        Check if queue is empty
        O(1) - queue is empty when both stacks are empty
        """
        return len(self.input_stack) == 0 and len(self.output_stack) == 0
    
    def _ensure_output_has_elements(self):
        """
        Helper method: Transfer elements from input to output if output is empty
        This is the key optimization - only transfer when necessary
        """
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())


# Solution 2: Two Stacks with Eager Transfer
class MyQueue2:
    """
    Approach: Always maintain queue order in output stack
    
    Less efficient but simpler to understand
    Push: O(n) - need to transfer elements for each push
    Pop: O(1) - just pop from output stack
    Peek: O(1) - just peek output stack
    Empty: O(1) - check output stack only
    """
    
    def __init__(self):
        self.input_stack = []   # Temporary stack for transfers
        self.output_stack = []  # Main stack maintaining queue order
    
    def push(self, x: int) -> None:
        """
        Push element to back of queue
        O(n) - need to maintain queue order
        """
        # Move all elements from output to input
        while self.output_stack:
            self.input_stack.append(self.output_stack.pop())
        
        # Add new element to input
        self.input_stack.append(x)
        
        # Move everything back to output
        while self.input_stack:
            self.output_stack.append(self.input_stack.pop())
    
    def pop(self) -> int:
        """Remove and return front element - O(1)"""
        return self.output_stack.pop()
    
    def peek(self) -> int:
        """Return front element - O(1)"""
        return self.output_stack[-1]
    
    def empty(self) -> bool:
        """Check if empty - O(1)"""
        return len(self.output_stack) == 0


# Solution 3: Single Stack with Recursion (Creative but not practical)
class MyQueue3:
    """
    Approach: Use single stack with recursion to access bottom element
    
    This is more of a theoretical solution - not recommended for interviews
    Push: O(1)
    Pop: O(n) - need to recursively access bottom
    Peek: O(n) - need to recursively access bottom
    Empty: O(1)
    """
    
    def __init__(self):
        self.stack = []
    
    def push(self, x: int) -> None:
        """Push to stack - O(1)"""
        self.stack.append(x)
    
    def pop(self) -> int:
        """
        Remove bottom element using recursion
        O(n) - need to pop all elements, get bottom, then restore
        """
        if len(self.stack) == 1:
            return self.stack.pop()
        
        # Remove top element
        top = self.stack.pop()
        # Recursively get bottom element
        result = self.pop()
        # Restore top element
        self.stack.append(top)
        
        return result
    
    def peek(self) -> int:
        """
        Get bottom element using recursion without removing
        O(n) - similar to pop but restore the bottom element too
        """
        if len(self.stack) == 1:
            return self.stack[-1]
        
        # Remove top element
        top = self.stack.pop()
        # Recursively get bottom element
        result = self.peek()
        # Restore top element
        self.stack.append(top)
        
        return result
    
    def empty(self) -> bool:
        """Check if empty - O(1)"""
        return len(self.stack) == 0


def demonstrate_lazy_transfer():
    """
    Demonstrate how the lazy transfer strategy works in Solution 1
    """
    print("="*60)
    print("LAZY TRANSFER DEMONSTRATION (Optimal Solution)")
    print("="*60)
    
    queue = MyQueue1()
    
    def print_state():
        print(f"Input stack:  {queue.input_stack} (top on right)")
        print(f"Output stack: {queue.output_stack} (top on right)")
        print()
    
    print("Initial state:")
    print_state()
    
    print("push(1), push(2), push(3):")
    queue.push(1)
    queue.push(2)
    queue.push(3)
    print("All pushes go to input stack")
    print_state()
    
    print("peek() - need to transfer since output is empty:")
    print("1. Transfer all elements from input to output")
    result = queue.peek()
    print(f"2. peek() returns {result}")
    print_state()
    
    print("pop() - output has elements, no transfer needed:")
    result = queue.pop()
    print(f"pop() returns {result}")
    print_state()
    
    print("push(4) - just add to input:")
    queue.push(4)
    print_state()
    
    print("pop() - output still has elements, no transfer needed:")
    result = queue.pop()
    print(f"pop() returns {result}")
    print_state()
    
    print("pop() - output still has elements:")
    result = queue.pop()
    print(f"pop() returns {result}")
    print_state()
    
    print("pop() - output empty, need to transfer:")
    print("Transfer 4 from input to output")
    result = queue.pop()
    print(f"pop() returns {result}")
    print_state()


def analyze_amortized_complexity():
    """
    Analyze why lazy transfer gives amortized O(1) complexity
    """
    print("\n" + "="*60)
    print("AMORTIZED COMPLEXITY ANALYSIS")
    print("="*60)
    
    print("Key insight: Each element is moved at most twice:")
    print("1. From input stack to output stack (at most once)")
    print("2. From output stack when popped (exactly once)")
    print()
    
    print("Example with n operations:")
    print("- Push n elements: n operations, each O(1) = O(n) total")
    print("- Pop n elements: n operations")
    print("  * Each element transferred once: O(n) total transfer cost") 
    print("  * Each element popped once: O(n) total pop cost")
    print("  * Total: O(n) for n pops")
    print()
    
    print("Total cost for 2n operations: O(n) + O(n) = O(n)")
    print("Amortized cost per operation: O(n) / 2n = O(1)")
    print()
    
    print("Worst case single operation: O(n) (when transferring)")
    print("Average case per operation: O(1)")


def test_queue_implementations():
    """Test all queue implementations"""
    
    implementations = [
        ("Two Stacks - Lazy Transfer (Optimal)", MyQueue1),
        ("Two Stacks - Eager Transfer", MyQueue2),
        ("Single Stack - Recursive", MyQueue3)
    ]
    
    test_operations = [
        ("push", 1),
        ("push", 2),
        ("push", 3),
        ("peek", None),   # Should return 1
        ("pop", None),    # Should return 1
        ("push", 4),
        ("peek", None),   # Should return 2
        ("pop", None),    # Should return 2
        ("pop", None),    # Should return 3
        ("empty", None),  # Should return False
        ("pop", None),    # Should return 4
        ("empty", None),  # Should return True
    ]
    
    for name, QueueClass in implementations:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        
        queue = QueueClass()
        
        for operation, value in test_operations:
            try:
                if operation == "push":
                    queue.push(value)
                    print(f"push({value}) -> Queue updated")
                elif operation == "pop":
                    result = queue.pop()
                    print(f"pop() -> {result}")
                elif operation == "peek":
                    result = queue.peek()
                    print(f"peek() -> {result}")
                elif operation == "empty":
                    result = queue.empty()
                    print(f"empty() -> {result}")
            except (IndexError, RecursionError) as e:
                print(f"{operation}() -> Error: {e}")


def compare_approaches():
    """
    Compare different approaches for interview discussion
    """
    print("\n" + "="*60)
    print("APPROACH COMPARISON")
    print("="*60)
    
    approaches = [
        {
            "name": "Lazy Transfer (Optimal)",
            "push": "O(1)",
            "pop": "O(1) amortized, O(n) worst",
            "peek": "O(1) amortized, O(n) worst", 
            "empty": "O(1)",
            "pros": ["Best overall performance", "Amortized O(1) for all ops", "Intuitive"],
            "cons": ["Worst case O(n) for pop/peek", "Uses two stacks"]
        },
        {
            "name": "Eager Transfer", 
            "push": "O(n)",
            "pop": "O(1)",
            "peek": "O(1)",
            "empty": "O(1)",
            "pros": ["Simple to understand", "Guaranteed O(1) pop/peek"],
            "cons": ["O(n) push is expensive", "Poor if push-heavy workload"]
        },
        {
            "name": "Single Stack Recursive",
            "push": "O(1)", 
            "pop": "O(n)",
            "peek": "O(n)",
            "empty": "O(1)",
            "pros": ["Uses only one stack", "Creative solution"],
            "cons": ["O(n) for common ops", "Recursion overhead", "Not practical"]
        }
    ]
    
    for approach in approaches:
        print(f"\n{approach['name']}:")
        print(f"  Push: {approach['push']}")
        print(f"  Pop:  {approach['pop']}")
        print(f"  Peek: {approach['peek']}")
        print(f"  Empty: {approach['empty']}")
        print(f"  Pros: {', '.join(approach['pros'])}")
        print(f"  Cons: {', '.join(approach['cons'])}")


if __name__ == "__main__":
    test_queue_implementations()
    demonstrate_lazy_transfer()
    analyze_amortized_complexity() 
    compare_approaches()


"""
INTERVIEW STRATEGY:

1. Problem Understanding (2-3 minutes):
   - "Need to implement FIFO (queue) using LIFO (stack) operations"
   - "Queue: add to back, remove from front. Stack: add/remove from top"
   - "Challenge: How to access the 'first' element using only stack operations?"

2. Approach Discussion (5-7 minutes):
   - Present main approaches:
     * Two stacks with lazy transfer (optimal)
     * Two stacks with eager transfer  
     * Single stack with recursion (mention but don't implement)
   
   - "Key insight: Use one stack for input, one for output"
   - "Lazy vs eager transfer trade-offs"

3. Implementation (8-10 minutes):
   - Implement Solution 1 (lazy transfer)
   - Explain the _ensure_output_has_elements helper
   - Walk through example operations

4. Complexity Analysis (3-4 minutes):
   - "Why is it amortized O(1)? Each element moved at most once"
   - "Worst case single operation: O(n), but rare"
   - "Total cost for n operations: O(n), so average O(1)"

5. Follow-up Discussion (2-3 minutes):
   - Compare with eager transfer approach
   - Mention single stack recursive solution
   - Discuss when each might be preferred

KEY INSIGHTS TO EMPHASIZE:
- "Two stacks naturally reverse the order twice, giving us FIFO"
- "Lazy transfer is key optimization - only move when necessary"
- "Each element is moved at most once, giving amortized O(1)"
- "Input stack handles pushes, output stack handles pops/peeks"

AMORTIZED ANALYSIS:
- "Think of it like a bank account - sometimes you pay extra (transfer cost)"
- "But over many operations, the average cost is constant"
- "Each element pays for its transfer once, amortized over its lifetime"

FOLLOW-UP QUESTIONS:
- "What if pop/peek are rare?" → Eager transfer might be better
- "Memory usage?" → Two stacks use same space as queue
- "Thread safety?" → Would need synchronization
- "Can you implement stack using queues?" → Yes, previous problem!

COMMON MISTAKES:
- Forgetting to handle empty cases
- Not understanding amortized analysis
- Implementing eager transfer thinking it's better
- Trying to maintain queue order in input stack
"""
