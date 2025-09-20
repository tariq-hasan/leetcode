# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """
        Optimal Iterative Inorder Traversal (Most Efficient)
        
        Key insight: BST inorder traversal gives sorted order.
        Stop after finding kth element instead of traversing entire tree.
        
        Time Complexity: O(H + k) where H is height of tree
        Space Complexity: O(H) for stack
        """
        stack = []
        current = root
        
        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            k -= 1
            
            # If we've found the kth element, return it
            if k == 0:
                return current.val
            
            # Move to right subtree
            current = current.right
        
        return -1  # Should never reach here given problem constraints

    def kthSmallestRecursive(self, root: Optional[TreeNode], k: int) -> int:
        """
        Recursive Inorder Traversal (Clean but uses more space)
        
        Uses instance variable to track count and result
        Time Complexity: O(H + k)
        Space Complexity: O(H) for recursion stack
        """
        self.count = 0
        self.result = None
        
        def inorder(node):
            if not node or self.result is not None:
                return
            
            # Traverse left subtree
            inorder(node.left)
            
            # Process current node
            self.count += 1
            if self.count == k:
                self.result = node.val
                return
            
            # Traverse right subtree
            inorder(node.right)
        
        inorder(root)
        return self.result

    def kthSmallestList(self, root: Optional[TreeNode], k: int) -> int:
        """
        Simple Inorder to List (Not optimal but easy to understand)
        
        Generate complete inorder traversal, then return kth element
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        def inorder(node, result):
            if not node:
                return
            inorder(node.left, result)
            result.append(node.val)
            inorder(node.right, result)
        
        values = []
        inorder(root, values)
        return values[k - 1]

    def kthSmallestMorris(self, root: Optional[TreeNode], k: int) -> int:
        """
        Morris Traversal (O(1) Space Solution - Advanced)
        
        Uses threading to achieve O(1) space complexity
        Time Complexity: O(n) but each node visited at most 3 times
        Space Complexity: O(1)
        """
        current = root
        count = 0
        
        while current:
            if not current.left:
                # Process current node
                count += 1
                if count == k:
                    return current.val
                current = current.right
            else:
                # Find inorder predecessor
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right
                
                if not predecessor.right:
                    # Create thread
                    predecessor.right = current
                    current = current.left
                else:
                    # Remove thread and process current
                    predecessor.right = None
                    count += 1
                    if count == k:
                        return current.val
                    current = current.right
        
        return -1

    def kthSmallestBinarySearch(self, root: Optional[TreeNode], k: int) -> int:
        """
        Binary Search Approach (Good for Multiple Queries)
        
        Count nodes in left subtree to decide which direction to go
        Time Complexity: O(H * H) = O(H²) worst case
        Space Complexity: O(H) for recursion
        """
        def count_nodes(node):
            """Count total nodes in subtree"""
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        def kth_smallest_helper(node, k):
            if not node:
                return -1
            
            left_count = count_nodes(node.left)
            
            if k <= left_count:
                # kth smallest is in left subtree
                return kth_smallest_helper(node.left, k)
            elif k == left_count + 1:
                # Current node is the kth smallest
                return node.val
            else:
                # kth smallest is in right subtree
                return kth_smallest_helper(node.right, k - left_count - 1)
        
        return kth_smallest_helper(root, k)

    def kthSmallestWithRank(self, root: Optional[TreeNode], k: int) -> int:
        """
        Enhanced BST with Rank Information (Best for Multiple Queries)
        
        If we could augment BST nodes with subtree sizes, this would be O(H)
        This version simulates that by computing ranks on-demand
        Time Complexity: O(H) per query if ranks pre-computed
        Space Complexity: O(H)
        """
        def get_rank(node, target):
            """Get rank (1-indexed) of target in BST rooted at node"""
            if not node:
                return 0
            
            if target < node.val:
                return get_rank(node.left, target)
            elif target > node.val:
                left_size = self.get_subtree_size(node.left)
                return 1 + left_size + get_rank(node.right, target)
            else:
                return 1 + self.get_subtree_size(node.left)
        
        def get_subtree_size(node):
            """Get size of subtree rooted at node"""
            if not node:
                return 0
            return 1 + get_subtree_size(node.left) + get_subtree_size(node.right)
        
        self.get_subtree_size = get_subtree_size
        
        def find_kth(node, k):
            """Find kth smallest element"""
            if not node:
                return -1
            
            left_size = get_subtree_size(node.left)
            
            if k == left_size + 1:
                return node.val
            elif k <= left_size:
                return find_kth(node.left, k)
            else:
                return find_kth(node.right, k - left_size - 1)
        
        return find_kth(root, k)

# Test cases and utility functions
def build_bst1():
    """
    Build BST:     3
                  / \
                 1   4
                  \
                   2
    
    Inorder: [1, 2, 3, 4]
    kth smallest (k=1): 1
    kth smallest (k=2): 2
    """
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.right = TreeNode(2)
    return root

def build_bst2():
    """
    Build BST:       5
                   /   \
                  3     6
                 / \
                2   4
               /
              1
    
    Inorder: [1, 2, 3, 4, 5, 6]
    """
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(1)
    return root

def build_large_bst():
    """
    Build larger BST:      10
                         /    \
                        5      15
                       / \    /  \
                      3   7  12  20
                     / \   \   \   \
                    1   4   8  13  25
    """
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(12)
    root.right.right = TreeNode(20)
    root.left.left.left = TreeNode(1)
    root.left.left.right = TreeNode(4)
    root.left.right.right = TreeNode(8)
    root.right.left.right = TreeNode(13)
    root.right.right.right = TreeNode(25)
    return root

def print_inorder(root):
    """Helper to verify BST property"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def test_solutions():
    solution = Solution()
    
    # Test case 1
    bst1 = build_bst1()
    print("Test 1 - BST: [3,1,4,null,2]")
    print(f"Inorder: {print_inorder(bst1)}")
    print(f"  k=1: {solution.kthSmallest(bst1, 1)} (Expected: 1)")
    print(f"  k=2: {solution.kthSmallest(bst1, 2)} (Expected: 2)")
    print(f"  k=3: {solution.kthSmallest(bst1, 3)} (Expected: 3)")
    print()
    
    # Test case 2
    bst2 = build_bst2()
    print("Test 2 - Larger BST:")
    print(f"Inorder: {print_inorder(bst2)}")
    print(f"  k=1: {solution.kthSmallest(bst2, 1)} (Expected: 1)")
    print(f"  k=3: {solution.kthSmallest(bst2, 3)} (Expected: 3)")
    print(f"  k=5: {solution.kthSmallest(bst2, 5)} (Expected: 5)")
    print()
    
    # Test different implementations
    bst3 = build_large_bst()
    k_test = 4
    print("Test 3 - Comparing different implementations:")
    print(f"  Iterative: {solution.kthSmallest(bst3, k_test)}")
    print(f"  Recursive: {solution.kthSmallestRecursive(bst3, k_test)}")
    print(f"  List-based: {solution.kthSmallestList(bst3, k_test)}")
    print(f"  Morris: {solution.kthSmallestMorris(bst3, k_test)}")
    print(f"  Binary Search: {solution.kthSmallestBinarySearch(bst3, k_test)}")
    print(f"  Expected: 4th smallest from {print_inorder(bst3)}")
    print()
    
    # Edge cases
    single_node = TreeNode(1)
    print("Test 4 - Single node BST:")
    print(f"  k=1: {solution.kthSmallest(single_node, 1)} (Expected: 1)")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - BST property: left < root < right
   - Inorder traversal of BST gives sorted sequence
   - Want kth smallest element (1-indexed)
   - Need to leverage BST property for efficiency

2. KEY INSIGHT:
   - BST inorder traversal visits nodes in sorted order
   - Don't need to traverse entire tree - stop after finding kth element
   - This gives us O(H + k) instead of O(n) complexity

3. SOLUTION APPROACHES:

   APPROACH 1 - Iterative Inorder (RECOMMENDED):
   - Use stack to simulate inorder traversal
   - Stop as soon as we reach kth element
   - Time: O(H + k), Space: O(H)
   - Most efficient for single queries

   APPROACH 2 - Recursive Inorder:
   - Same logic but using recursion
   - Slightly more space due to recursion stack
   - Cleaner code but not necessarily better

   APPROACH 3 - Complete Inorder to List:
   - Simple but inefficient: O(n) time and space
   - Good to mention as baseline, but not optimal

   APPROACH 4 - Morris Traversal:
   - O(1) space solution using threading
   - Advanced technique, mention if space is critical

   APPROACH 5 - Binary Search on BST:
   - Count nodes in left subtree to decide direction
   - O(H²) time but good for multiple queries with augmentation

4. SOLUTION CHOICE FOR INTERVIEW:
   - Lead with iterative inorder traversal
   - Explain the BST property insight
   - Mention other approaches if asked
   - Emphasize early termination optimization

5. IMPLEMENTATION DETAILS:
   - Use stack for iterative inorder
   - Decrement k as we visit nodes
   - Return when k reaches 0
   - Handle edge cases (k > n, empty tree)

6. COMPLEXITY ANALYSIS:
   - Time: O(H + k) where H is height, k is parameter
   - Best case: O(log n + k) for balanced BST
   - Worst case: O(n + k) for skewed BST
   - Space: O(H) for stack

7. WHY THIS IS OPTIMAL:
   - Leverages BST property (inorder gives sorted sequence)
   - Early termination (don't visit unnecessary nodes)
   - Efficient space usage
   - Natural and intuitive approach

8. EDGE CASES:
   - k = 1 (smallest element)
   - k = n (largest element)
   - Single node tree
   - Skewed BST (essentially a linked list)

9. FOLLOW-UP QUESTIONS:
   - "What if we need to find kth element multiple times?" → Augment BST with subtree sizes
   - "What about kth largest?" → Reverse inorder or use (n-k+1)th smallest
   - "O(1) space solution?" → Morris traversal
   - "What if tree can be modified?" → Threading or parent pointers

10. COMPARISON WITH ALTERNATIVES:
    - Heap extraction: O(n log n) to build, O(k log n) to extract
    - Quickselect on array: O(n) average but need to convert BST to array first
    - Our solution: O(H + k) which is often much better

11. INTERVIEW PRESENTATION:
    - Start with: "I'll use BST's key property - inorder traversal gives sorted order"
    - Emphasize early termination: "I'll stop as soon as I find the kth element"
    - Code the iterative inorder solution
    - Walk through example showing the traversal
    - Discuss complexity and mention alternatives

12. COMMON MISTAKES:
    - Forgetting to leverage BST property (treating as general binary tree)
    - Not implementing early termination (traversing entire tree)
    - Off-by-one errors in k counting
    - Not handling edge cases properly

13. WHY INTERVIEWERS LOVE THIS PROBLEM:
    - Tests BST property understanding
    - Multiple valid approaches (shows problem-solving breadth)
    - Optimization opportunity (early termination)
    - Clean recursive vs iterative implementations

14. OPTIMIZATION INSIGHTS:
    - For single query: iterative inorder is best
    - For multiple queries: augment BST with subtree sizes
    - For space-critical: Morris traversal
    - For simplicity: recursive inorder

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is that BST inorder traversal visits nodes in sorted order,
    so I can perform inorder traversal and stop as soon as I reach the kth node.
    This gives me O(H + k) time complexity instead of O(n), which is optimal
    since I might not need to visit the entire tree."
"""
