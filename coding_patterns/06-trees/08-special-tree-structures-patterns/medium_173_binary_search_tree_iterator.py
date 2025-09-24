# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class BSTIterator:
    """
    Optimal Solution - Controlled Inorder Traversal with Stack
    
    Key insight: Use stack to simulate inorder traversal without
    precomputing all values. Only maintain path to leftmost unvisited node.
    
    Time Complexity: 
    - __init__: O(h) where h is height
    - next(): Amortized O(1), worst case O(h)
    - hasNext(): O(1)
    
    Space Complexity: O(h) for stack
    """
    
    def __init__(self, root: Optional[TreeNode]):
        self.stack = []
        self._push_all_left(root)
    
    def _push_all_left(self, node):
        """Push all left children starting from node"""
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self) -> int:
        """Returns next smallest element"""
        # Get the next node (top of stack)
        node = self.stack.pop()
        
        # If it has right subtree, push all left children of right subtree
        if node.right:
            self._push_all_left(node.right)
        
        return node.val
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return len(self.stack) > 0

class BSTIteratorPrecomputed:
    """
    Alternative Solution - Precompute All Values
    
    Simple but uses O(n) space. Good for multiple iterations.
    
    Time Complexity:
    - __init__: O(n)
    - next(): O(1)
    - hasNext(): O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, root: Optional[TreeNode]):
        self.values = []
        self.index = 0
        self._inorder(root)
    
    def _inorder(self, node):
        """Standard inorder traversal to collect all values"""
        if node:
            self._inorder(node.left)
            self.values.append(node.val)
            self._inorder(node.right)
    
    def next(self) -> int:
        """Returns next smallest element"""
        val = self.values[self.index]
        self.index += 1
        return val
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return self.index < len(self.values)

class BSTIteratorRecursive:
    """
    Recursive Generator Approach (Python-Specific)
    
    Uses Python generators for elegant implementation
    Not recommended for interviews as it's language-specific
    
    Time Complexity: Amortized O(1) per next()
    Space Complexity: O(h)
    """
    
    def __init__(self, root: Optional[TreeNode]):
        self.generator = self._inorder_generator(root)
        self.next_val = None
        self._advance()
    
    def _inorder_generator(self, node):
        """Generator for inorder traversal"""
        if node:
            yield from self._inorder_generator(node.left)
            yield node.val
            yield from self._inorder_generator(node.right)
    
    def _advance(self):
        """Get next value from generator"""
        try:
            self.next_val = next(self.generator)
        except StopIteration:
            self.next_val = None
    
    def next(self) -> int:
        """Returns next smallest element"""
        val = self.next_val
        self._advance()
        return val
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return self.next_val is not None

class BSTIteratorTwoStacks:
    """
    Two-Stack Approach (Educational)
    
    Uses two stacks to maintain state, less elegant than single stack
    
    Time Complexity: Amortized O(1)
    Space Complexity: O(h)
    """
    
    def __init__(self, root: Optional[TreeNode]):
        self.nodes_stack = []
        self.visited_left = []
        if root:
            self.nodes_stack.append(root)
            self.visited_left.append(False)
    
    def next(self) -> int:
        """Returns next smallest element"""
        while self.nodes_stack:
            node = self.nodes_stack[-1]
            visited = self.visited_left[-1]
            
            if not visited:
                # First time visiting this node, go left
                self.visited_left[-1] = True
                if node.left:
                    self.nodes_stack.append(node.left)
                    self.visited_left.append(False)
            else:
                # Already visited left, process current and go right
                self.nodes_stack.pop()
                self.visited_left.pop()
                
                if node.right:
                    self.nodes_stack.append(node.right)
                    self.visited_left.append(False)
                
                return node.val
        
        return -1  # Should never reach here
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return len(self.nodes_stack) > 0

class BSTIteratorWithParent:
    """
    Parent Pointer Approach (If Tree Nodes Have Parent References)
    
    Assumes TreeNode has parent pointer. Not applicable to standard problem.
    
    Time Complexity: Amortized O(1)
    Space Complexity: O(1)
    """
    
    def __init__(self, root: Optional[TreeNode]):
        # Find the smallest node (leftmost)
        self.current = root
        if self.current:
            while self.current.left:
                self.current = self.current.left
    
    def next(self) -> int:
        """Returns next smallest element"""
        val = self.current.val
        
        if self.current.right:
            # Go to right subtree, then leftmost
            self.current = self.current.right
            while self.current.left:
                self.current = self.current.left
        else:
            # Go up until we're a left child
            while (self.current.parent and 
                   self.current == self.current.parent.right):
                self.current = self.current.parent
            self.current = self.current.parent
        
        return val
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return self.current is not None

class BSTIteratorFlattened:
    """
    Morris Traversal Approach (O(1) Space but Modifies Tree)
    
    Uses threading technique but modifies original tree structure
    Not recommended as it violates tree immutability
    
    Time Complexity: Amortized O(1)
    Space Complexity: O(1)
    """
    
    def __init__(self, root: Optional[TreeNode]):
        self.current = root
        self.next_val = None
        self._find_next()
    
    def _find_next(self):
        """Find next value using Morris traversal"""
        while self.current:
            if not self.current.left:
                # Process current and go right
                self.next_val = self.current.val
                self.current = self.current.right
                return
            else:
                # Find predecessor
                predecessor = self.current.left
                while predecessor.right and predecessor.right != self.current:
                    predecessor = predecessor.right
                
                if not predecessor.right:
                    # Create thread
                    predecessor.right = self.current
                    self.current = self.current.left
                else:
                    # Remove thread and process
                    predecessor.right = None
                    self.next_val = self.current.val
                    self.current = self.current.right
                    return
        
        self.next_val = None
    
    def next(self) -> int:
        """Returns next smallest element"""
        val = self.next_val
        self._find_next()
        return val
    
    def hasNext(self) -> bool:
        """Returns whether we have a next smallest element"""
        return self.next_val is not None

# Test cases and utility functions
def build_test_bst1():
    """
    Build BST:     7
                  / \
                 3  15
                   /  \
                  9   20
    
    Inorder: [3, 7, 9, 15, 20]
    """
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    return root

def build_test_bst2():
    """
    Build BST:    5
                 / \
                3   6
               / \   \
              2   4   7
             /
            1
    
    Inorder: [1, 2, 3, 4, 5, 6, 7]
    """
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(7)
    root.left.left.left = TreeNode(1)
    return root

def build_linear_bst():
    """
    Linear BST:  1
                  \
                   2
                    \
                     3
                      \
                       4
    """
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.right = TreeNode(3)
    root.right.right.right = TreeNode(4)
    return root

def build_single_node():
    """Single node BST"""
    return TreeNode(5)

def inorder_traversal(root):
    """Get inorder traversal for comparison"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def test_iterator_implementation(iterator_class, tree_builder, test_name):
    """Test an iterator implementation"""
    print(f"\n{test_name}:")
    
    # Get expected inorder sequence
    tree = tree_builder()
    expected = inorder_traversal(tree)
    print(f"Expected inorder: {expected}")
    
    # Test iterator
    tree = tree_builder()
    iterator = iterator_class(tree)
    
    result = []
    print("Iterator sequence: ", end="")
    while iterator.hasNext():
        val = iterator.next()
        result.append(val)
        print(val, end=" ")
    print()
    
    print(f"Iterator result: {result}")
    print(f"Correct: {result == expected}")
    
    return result == expected

def test_iterator_operations(tree_builder, test_name):
    """Test specific iterator operations"""
    print(f"\n{test_name} - Operation Testing:")
    
    tree = tree_builder()
    iterator = BSTIterator(tree)
    expected = inorder_traversal(tree)
    
    print(f"Expected sequence: {expected}")
    print("Testing mixed operations:")
    
    operations = []
    results = []
    
    # Test hasNext before any next()
    operations.append("hasNext()")
    results.append(iterator.hasNext())
    print(f"hasNext(): {results[-1]}")
    
    # Get first few elements
    for i in range(min(3, len(expected))):
        if iterator.hasNext():
            operations.append(f"next()")
            val = iterator.next()
            results.append(val)
            print(f"next(): {val}")
            
            operations.append("hasNext()")
            has_next = iterator.hasNext()
            results.append(has_next)
            print(f"hasNext(): {has_next}")
    
    # Get remaining elements
    remaining = []
    while iterator.hasNext():
        remaining.append(iterator.next())
    
    print(f"Remaining elements: {remaining}")
    
    # Verify we got all elements
    all_values = [r for i, r in enumerate(results) if operations[i].startswith("next")]
    all_values.extend(remaining)
    print(f"All values from iterator: {all_values}")
    print(f"Matches expected: {all_values == expected}")

def performance_analysis():
    """Analyze performance of different approaches"""
    print("\nPERFORMANCE ANALYSIS:")
    print("=" * 50)
    
    approaches = [
        ("Stack-based (Optimal)", "O(h)", "O(1) amortized", "O(h)"),
        ("Precomputed", "O(n)", "O(1)", "O(n)"),
        ("Two Stacks", "O(h)", "O(1) amortized", "O(h)"),
        ("Morris (Modifies Tree)", "O(1)", "O(1) amortized", "O(1)"),
    ]
    
    print(f"{'Approach':<25} {'Init':<8} {'next()':<15} {'Space':<8}")
    print("-" * 60)
    
    for name, init_time, next_time, space in approaches:
        print(f"{name:<25} {init_time:<8} {next_time:<15} {space:<8}")
    
    print("\nRECOMMENDATION:")
    print("✓ Stack-based approach is optimal for interviews")
    print("✓ Balances time/space complexity optimally") 
    print("✓ Clean implementation with clear logic")
    print("✓ Handles edge cases naturally")

def comprehensive_test():
    """Run comprehensive tests"""
    
    # Test different tree structures
    test_iterator_implementation(BSTIterator, build_test_bst1, 
                                "Test 1: Balanced BST")
    
    test_iterator_implementation(BSTIterator, build_test_bst2,
                                "Test 2: Complex BST")
    
    test_iterator_implementation(BSTIterator, build_linear_bst,
                                "Test 3: Linear BST")
    
    test_iterator_implementation(BSTIterator, build_single_node,
                                "Test 4: Single node")
    
    # Test mixed operations
    test_iterator_operations(build_test_bst1, "Test 5: Mixed Operations")
    
    # Compare different implementations
    print("\nCOMPARING IMPLEMENTATIONS:")
    tree = build_test_bst2()
    expected = inorder_traversal(tree)
    
    implementations = [
        ("Stack-based", BSTIterator),
        ("Precomputed", BSTIteratorPrecomputed),
        ("Recursive", BSTIteratorRecursive),
    ]
    
    for name, impl_class in implementations:
        tree = build_test_bst2()
        iterator = impl_class(tree)
        result = []
        while iterator.hasNext():
            result.append(iterator.next())
        
        print(f"{name}: {result == expected}")

if __name__ == "__main__":
    comprehensive_test()
    performance_analysis()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Design iterator for BST that returns elements in ascending order
   - Must support next() and hasNext() operations
   - next() should return next smallest element
   - hasNext() should return whether more elements exist
   - Should be space and time efficient

2. KEY INSIGHT - CONTROLLED INORDER TRAVERSAL:
   - BST inorder traversal gives ascending order
   - Instead of precomputing all values, do "lazy" traversal
   - Use stack to maintain state of partial inorder traversal
   - Only compute next element when requested

3. OPTIMAL APPROACH - STACK-BASED:
   - Use stack to simulate inorder traversal
   - Initialize: push all left children from root
   - next(): pop from stack, if has right child, push all its left children
   - hasNext(): check if stack is empty

4. WHY STACK APPROACH IS OPTIMAL:
   - Space: O(h) instead of O(n) - only stores path to current node
   - Time: next() is amortized O(1) - each node visited exactly once
   - Lazy evaluation: only computes values as needed
   - Clean implementation without complex state management

5. ALGORITHM WALKTHROUGH:
   - Initialize: Push path to leftmost node onto stack
   - next(): Top of stack is next smallest, handle its right subtree
   - hasNext(): Stack not empty means more elements available

6. COMPLEXITY ANALYSIS:
   - Space: O(h) where h is height of tree
   - next(): Amortized O(1), worst case O(h) per call
   - hasNext(): O(1)
   - Initialization: O(h)

7. ALTERNATIVE APPROACHES:

   APPROACH 1 - Stack-based (RECOMMENDED):
   - Optimal balance of time/space complexity
   - Clean implementation
   - Industry standard approach

   APPROACH 2 - Precompute all values:
   - Simple but uses O(n) space
   - Good if iterator used multiple times
   - next() and hasNext() are strict O(1)

   APPROACH 3 - Morris traversal:
   - O(1) space but modifies tree structure
   - Not recommended due to side effects

8. EDGE CASES:
   - Empty tree
   - Single node tree
   - Linear tree (all left or all right)
   - Calling next() when hasNext() is false

9. INTERVIEW PRESENTATION:
   - Clarify requirements: "I need ascending order iteration"
   - Key insight: "I'll use stack to do controlled inorder traversal"
   - Explain lazy evaluation benefit
   - Code the stack-based solution
   - Walk through example showing stack evolution

10. FOLLOW-UP QUESTIONS:
    - "Can you optimize space further?" → Morris traversal but mention drawbacks
    - "What if we need descending order?" → Use reverse inorder with stack
    - "Multiple iterators on same tree?" → Each iterator maintains own stack
    - "What's the amortized complexity?" → Explain why next() is O(1) amortized

11. WHY THIS PROBLEM IS IMPORTANT:
    - Tests iterator design pattern understanding
    - Combines BST properties with stack data structure
    - Shows lazy evaluation vs eager evaluation trade-offs
    - Common in system design and API design discussions

12. COMMON MISTAKES:
    - Precomputing all values (correct but not optimal)
    - Not handling right subtree correctly in next()
    - Incorrect stack management
    - Not understanding amortized complexity

13. IMPLEMENTATION DETAILS:
    - _push_all_left() helper function for clean code
    - Handle right subtree after processing current node
    - Stack contains TreeNode objects, not just values
    - Proper null checking throughout

14. OPTIMIZATION INSIGHTS:
    - Stack approach gives best time/space trade-off
    - Each node is pushed and popped exactly once
    - Amortized O(1) next() because total work is O(n) over n calls
    - Space proportional to tree height, not size

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is using a stack to perform controlled inorder traversal.
    Instead of computing all values upfront, I lazily evaluate only when next()
    is called. The stack maintains the path to the current position in the 
    traversal, giving me O(h) space and amortized O(1) next() operations."

16. DESIGN PATTERN RECOGNITION:
    - Iterator pattern implementation
    - Lazy evaluation vs eager evaluation
    - State management in iterative algorithms
    - Stack-based tree traversal simulation

17. PRODUCTION CONSIDERATIONS:
    - Thread safety for concurrent access
    - Error handling for invalid operations
    - Memory management
    - Iterator invalidation after tree modifications
"""
