# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Optimal Recursive Solution with Inorder Successor
        
        Key insight: Handle three cases based on node structure
        1. No children: Simply delete (return None)
        2. One child: Replace with that child
        3. Two children: Replace with inorder successor, then delete successor
        
        Time Complexity: O(h) where h is height of tree
        Space Complexity: O(h) due to recursion stack
        """
        if not root:
            return None
        
        # Find the node to delete
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # Found the node to delete
            
            # Case 1: Node has no left child
            if not root.left:
                return root.right
            
            # Case 2: Node has no right child
            elif not root.right:
                return root.left
            
            # Case 3: Node has both children
            else:
                # Find inorder successor (smallest in right subtree)
                successor = self.findMin(root.right)
                
                # Replace root's value with successor's value
                root.val = successor.val
                
                # Delete the successor
                root.right = self.deleteNode(root.right, successor.val)
        
        return root
    
    def findMin(self, root):
        """Find minimum value node in subtree (leftmost node)"""
        while root.left:
            root = root.left
        return root

    def deleteNodePredecessor(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Alternative: Using Inorder Predecessor Instead of Successor
        
        Same logic but replaces with largest value in left subtree
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        if not root:
            return None
        
        if key < root.val:
            root.left = self.deleteNodePredecessor(root.left, key)
        elif key > root.val:
            root.right = self.deleteNodePredecessor(root.right, key)
        else:
            # Found node to delete
            
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                # Use inorder predecessor (largest in left subtree)
                predecessor = self.findMax(root.left)
                root.val = predecessor.val
                root.left = self.deleteNodePredecessor(root.left, predecessor.val)
        
        return root
    
    def findMax(self, root):
        """Find maximum value node in subtree (rightmost node)"""
        while root.right:
            root = root.right
        return root

    def deleteNodeIterative(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Iterative Solution (More Complex but No Recursion)
        
        Uses explicit parent tracking instead of recursion
        Time Complexity: O(h)
        Space Complexity: O(1)
        """
        if not root:
            return None
        
        # Special case: deleting root
        if root.val == key:
            return self.deleteRoot(root)
        
        # Find the node to delete and its parent
        parent = None
        current = root
        
        while current and current.val != key:
            parent = current
            if key < current.val:
                current = current.left
            else:
                current = current.right
        
        # Node not found
        if not current:
            return root
        
        # Delete the node
        new_subtree = self.deleteRoot(current)
        
        # Update parent's pointer
        if parent.left == current:
            parent.left = new_subtree
        else:
            parent.right = new_subtree
        
        return root
    
    def deleteRoot(self, root):
        """Helper to delete a root node (no parent)"""
        if not root:
            return None
        
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        else:
            # Find successor and replace
            successor_parent = root
            successor = root.right
            
            # Find leftmost node in right subtree
            while successor.left:
                successor_parent = successor
                successor = successor.left
            
            # Replace root's value with successor's value
            root.val = successor.val
            
            # Delete successor
            if successor_parent == root:
                # Successor is root's right child
                root.right = successor.right
            else:
                # Successor is deeper in the tree
                successor_parent.left = successor.right
            
            return root

    def deleteNodeClean(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Clean Recursive Solution (Most Elegant)
        
        Simplified version with cleaner logic
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        if not root:
            return None
        
        if key < root.val:
            root.left = self.deleteNodeClean(root.left, key)
        elif key > root.val:
            root.right = self.deleteNodeClean(root.right, key)
        else:
            # Node to delete found
            
            # No children or one child cases
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            
            # Two children case
            # Find inorder successor (minimum in right subtree)
            min_node = root.right
            while min_node.left:
                min_node = min_node.left
            
            # Replace value and delete successor
            root.val = min_node.val
            root.right = self.deleteNodeClean(root.right, min_node.val)
        
        return root

    def deleteNodeWithParent(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Explicit Parent Tracking Version (Good for Understanding)
        
        Tracks parent explicitly for clearer logic
        Time Complexity: O(h)
        Space Complexity: O(1) iterative
        """
        if not root:
            return None
        
        # Find node and parent
        parent = None
        current = root
        
        while current and current.val != key:
            parent = current
            if key < current.val:
                current = current.left
            else:
                current = current.right
        
        if not current:  # Node not found
            return root
        
        # Case 1: Node has no children
        if not current.left and not current.right:
            if not parent:  # Deleting root
                return None
            elif parent.left == current:
                parent.left = None
            else:
                parent.right = None
        
        # Case 2: Node has one child
        elif not current.left or not current.right:
            child = current.left if current.left else current.right
            
            if not parent:  # Deleting root
                return child
            elif parent.left == current:
                parent.left = child
            else:
                parent.right = child
        
        # Case 3: Node has two children
        else:
            # Find inorder successor
            successor_parent = current
            successor = current.right
            
            while successor.left:
                successor_parent = successor
                successor = successor.left
            
            # Replace current node's value
            current.val = successor.val
            
            # Delete successor (which has at most one child)
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right
        
        return root

# Test cases and utility functions
def build_test_bst1():
    """
    Build BST:       5
                   /   \
                  3     6
                 / \     \
                2   4     7
    
    Test deletions: 3, 5, 7, 2, etc.
    """
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(7)
    return root

def build_test_bst2():
    """
    Build BST:         50
                     /    \
                   30      70
                  /  \    /  \
                20   40  60  80
    
    More complex tree for testing
    """
    root = TreeNode(50)
    root.left = TreeNode(30)
    root.right = TreeNode(70)
    root.left.left = TreeNode(20)
    root.left.right = TreeNode(40)
    root.right.left = TreeNode(60)
    root.right.right = TreeNode(80)
    return root

def build_complex_bst():
    """
    Complex BST:        20
                      /    \
                     10     30
                    /  \   /  \
                   5   15 25  35
                  /   /  \     \
                 1   12  18    40
    """
    root = TreeNode(20)
    root.left = TreeNode(10)
    root.right = TreeNode(30)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(15)
    root.right.left = TreeNode(25)
    root.right.right = TreeNode(35)
    root.left.left.left = TreeNode(1)
    root.left.right.left = TreeNode(12)
    root.left.right.right = TreeNode(18)
    root.right.right.right = TreeNode(40)
    return root

def build_single_node():
    """Single node BST"""
    return TreeNode(5)

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

def inorder_traversal(root):
    """Helper to verify BST property after deletion"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def print_tree_structure(root, level=0, prefix="Root: "):
    """Helper to visualize tree structure"""
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            if root.left:
                print_tree_structure(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_structure(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

def test_deletion(tree_builder, delete_key, test_name):
    """Test deletion on a tree"""
    solution = Solution()
    
    print(f"\n{test_name} - Deleting {delete_key}:")
    
    # Original tree
    original = tree_builder()
    original_inorder = inorder_traversal(original)
    print(f"Original inorder: {original_inorder}")
    
    # Delete node
    result = solution.deleteNode(original, delete_key)
    result_inorder = inorder_traversal(result)
    print(f"After deletion: {result_inorder}")
    
    # Verify BST property maintained
    is_sorted = all(result_inorder[i] <= result_inorder[i+1] 
                   for i in range(len(result_inorder)-1))
    print(f"BST property maintained: {is_sorted}")
    
    # Show structure
    print("Tree structure after deletion:")
    if result:
        print_tree_structure(result)
    else:
        print("Empty tree")

def comprehensive_test():
    """Run comprehensive tests"""
    
    # Test Case 1: Delete leaf node
    test_deletion(build_test_bst1, 2, "Test 1: Delete leaf node")
    
    # Test Case 2: Delete node with one child
    test_deletion(build_test_bst1, 6, "Test 2: Delete node with one child")
    
    # Test Case 3: Delete node with two children
    test_deletion(build_test_bst1, 3, "Test 3: Delete node with two children")
    
    # Test Case 4: Delete root
    test_deletion(build_test_bst1, 5, "Test 4: Delete root")
    
    # Test Case 5: Delete from single node tree
    test_deletion(build_single_node, 5, "Test 5: Delete single node")
    
    # Test Case 6: Delete non-existent node
    test_deletion(build_test_bst1, 99, "Test 6: Delete non-existent node")

def compare_methods():
    """Compare different deletion methods"""
    solution = Solution()
    
    # Test on complex tree
    tree = build_complex_bst()
    original = inorder_traversal(tree)
    print(f"Original tree inorder: {original}")
    
    # Method 1: Successor
    tree1 = build_complex_bst()
    result1 = solution.deleteNode(tree1, 20)
    inorder1 = inorder_traversal(result1)
    print(f"After deletion (successor): {inorder1}")
    
    # Method 2: Predecessor  
    tree2 = build_complex_bst()
    result2 = solution.deleteNodePredecessor(tree2, 20)
    inorder2 = inorder_traversal(result2)
    print(f"After deletion (predecessor): {inorder2}")
    
    # Both should maintain BST property
    print(f"Both maintain BST: {inorder1 == sorted(inorder1) and inorder2 == sorted(inorder2)}")

if __name__ == "__main__":
    comprehensive_test()
    print("\n" + "="*50)
    print("COMPARING SUCCESSOR VS PREDECESSOR METHODS:")
    compare_methods()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Delete node while maintaining BST property
   - Must handle three cases based on node's children
   - Tree structure changes but BST ordering must remain
   - Return root of modified tree

2. KEY INSIGHT - THREE DELETION CASES:
   
   CASE 1: Node has no children (leaf)
   - Simply remove the node (return None)
   
   CASE 2: Node has one child
   - Replace node with its child
   
   CASE 3: Node has two children (most complex)
   - Replace with inorder successor (or predecessor)
   - Delete the successor from its original position

3. INORDER SUCCESSOR STRATEGY:
   - Successor = smallest value in right subtree
   - Always has at most one child (right child)
   - Replacing with successor maintains BST property
   - Alternative: inorder predecessor (largest in left subtree)

4. ALGORITHM WALKTHROUGH:
   - Use BST search to find node to delete
   - Handle the three cases appropriately
   - Recursively update subtree roots
   - Return modified tree root

5. WHY SUCCESSOR WORKS:
   - Successor is next largest value after current node
   - Replacing maintains: left < new_root < right
   - Successor has at most right child (easy to delete)

6. COMPLEXITY ANALYSIS:
   - Time: O(h) where h is height of tree
   - Space: O(h) for recursion stack
   - Best case: O(log n) for balanced BST
   - Worst case: O(n) for skewed BST

7. IMPLEMENTATION APPROACHES:

   APPROACH 1 - Recursive (RECOMMENDED):
   - Clean and intuitive
   - Natural BST traversal pattern
   - Easy to understand and implement

   APPROACH 2 - Iterative:
   - Avoids recursion stack
   - More complex parent tracking
   - O(1) space complexity

8. SOLUTION CHOICE FOR INTERVIEW:
   - Lead with recursive approach (cleaner)
   - Mention iterative as space optimization
   - Focus on the three-case logic

9. EDGE CASES:
   - Deleting root node
   - Deleting from single-node tree
   - Node not found in tree
   - Empty tree
   - All nodes in chain (skewed BST)

10. INTERVIEW PRESENTATION:
    - Explain the three cases clearly
    - Show why successor replacement works
    - Code the recursive solution
    - Walk through example with two-children case
    - Discuss complexity and alternatives

11. FOLLOW-UP QUESTIONS:
    - "Can you do it iteratively?" → Show iterative version
    - "Why successor instead of predecessor?" → Both work, explain choice
    - "What if tree is very unbalanced?" → Discuss AVL/Red-Black trees
    - "How to delete multiple nodes efficiently?" → Batch operations

12. WHY THIS PROBLEM IS IMPORTANT:
    - Tests BST manipulation understanding
    - Combines search + tree restructuring
    - Multiple edge cases to handle correctly
    - Foundation for more advanced tree operations

13. COMMON MISTAKES:
    - Not handling all three cases properly
    - Forgetting to maintain BST property
    - Incorrect successor finding logic
    - Not returning modified tree root

14. OPTIMIZATION INSIGHTS:
    - Recursive approach is cleanest
    - Iterative saves space but adds complexity
    - Successor vs predecessor is implementation choice
    - Early termination when node not found

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is recognizing that BST deletion has three distinct cases
    based on the node's children. The most complex case (two children) is 
    handled by replacement with inorder successor, which maintains BST property
    because the successor is the next largest value. After replacement, we 
    recursively delete the successor from its original position."

16. RELATED PROBLEMS:
    - BST insertion (inverse operation)
    - BST search and validation
    - Tree balancing operations
    - BST to sorted array conversion

17. PRODUCTION CONSIDERATIONS:
    - Memory management (node deallocation)
    - Thread safety for concurrent operations
    - Balancing after deletions in self-balancing trees
    - Batch deletion optimization
"""
