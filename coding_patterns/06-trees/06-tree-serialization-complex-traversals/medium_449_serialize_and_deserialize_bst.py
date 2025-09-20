# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import deque

class Codec:
    """
    Optimal Solution - Preorder Traversal with BST Property
    
    Key insight: For BST, preorder traversal alone is sufficient to reconstruct.
    No need to store null markers since BST property determines structure.
    
    Time Complexity: O(n) for both serialize and deserialize
    Space Complexity: O(n) for storage, O(h) for recursion
    """
    
    def serialize(self, root):
        """Encodes a tree to a single string."""
        if not root:
            return ""
        
        values = []
        
        def preorder(node):
            if node:
                values.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        
        preorder(root)
        return ",".join(values)
    
    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data:
            return None
        
        values = list(map(int, data.split(",")))
        self.index = 0
        
        def build_tree(min_val, max_val):
            """Build BST within the given value range"""
            if self.index >= len(values):
                return None
            
            val = values[self.index]
            
            # Check if current value fits in valid range
            if val < min_val or val > max_val:
                return None
            
            # Use current value and advance index
            self.index += 1
            root = TreeNode(val)
            
            # Build left subtree (values < current)
            root.left = build_tree(min_val, val)
            # Build right subtree (values > current)
            root.right = build_tree(val, max_val)
            
            return root
        
        return build_tree(float('-inf'), float('inf'))

class CodecIterative:
    """
    Iterative Deserialize Version (Alternative Approach)
    
    Uses stack to deserialize without recursion
    """
    
    def serialize(self, root):
        """Same as above - preorder traversal"""
        if not root:
            return ""
        
        result = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            result.append(str(node.val))
            
            # Add right first, then left (for preorder)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return ",".join(result)
    
    def deserialize(self, data):
        """Iterative deserialize using stack"""
        if not data:
            return None
        
        values = list(map(int, data.split(",")))
        root = TreeNode(values[0])
        stack = [(root, float('-inf'), float('inf'))]
        i = 1
        
        while stack and i < len(values):
            node, min_val, max_val = stack.pop()
            
            # Try to add right child
            if i < len(values) and min_val < values[i] < max_val:
                if values[i] > node.val:
                    node.right = TreeNode(values[i])
                    stack.append((node, min_val, max_val))  # Push back for left child
                    stack.append((node.right, node.val, max_val))
                    i += 1
                    continue
            
            # Try to add left child
            if i < len(values) and min_val < values[i] < max_val:
                if values[i] < node.val:
                    node.left = TreeNode(values[i])
                    stack.append((node.left, min_val, node.val))
                    i += 1
        
        return root

class CodecWithNulls:
    """
    Alternative - Include Null Markers (Less Optimal for BST)
    
    This approach works for any binary tree, not just BST
    Uses more space than necessary for BST
    """
    
    def serialize(self, root):
        """Preorder with null markers"""
        if not root:
            return "null"
        
        return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)
    
    def deserialize(self, data):
        """Deserialize with null markers"""
        self.index = 0
        values = data.split(",")
        
        def build():
            if self.index >= len(values) or values[self.index] == "null":
                self.index += 1
                return None
            
            root = TreeNode(int(values[self.index]))
            self.index += 1
            root.left = build()
            root.right = build()
            return root
        
        return build()

class CodecPostorder:
    """
    Alternative - Using Postorder Traversal
    
    Shows different traversal approach, still leverages BST property
    """
    
    def serialize(self, root):
        """Postorder traversal"""
        if not root:
            return ""
        
        values = []
        
        def postorder(node):
            if node:
                postorder(node.left)
                postorder(node.right)
                values.append(str(node.val))
        
        postorder(root)
        return ",".join(values)
    
    def deserialize(self, data):
        """Deserialize from postorder"""
        if not data:
            return None
        
        values = list(map(int, data.split(",")))
        self.index = len(values) - 1
        
        def build_tree(min_val, max_val):
            if self.index < 0:
                return None
            
            val = values[self.index]
            if val < min_val or val > max_val:
                return None
            
            self.index -= 1
            root = TreeNode(val)
            
            # In postorder, build right first, then left
            root.right = build_tree(val, max_val)
            root.left = build_tree(min_val, val)
            
            return root
        
        return build_tree(float('-inf'), float('inf'))

class CodecLevelOrder:
    """
    Alternative - Level Order (BFS) Approach
    
    More intuitive for some, but requires null markers
    """
    
    def serialize(self, root):
        """Level order traversal"""
        if not root:
            return ""
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        
        # Remove trailing nulls
        while result and result[-1] == "null":
            result.pop()
        
        return ",".join(result)
    
    def deserialize(self, data):
        """Deserialize from level order"""
        if not data:
            return None
        
        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            # Left child
            if i < len(values) and values[i] != "null":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # Right child
            if i < len(values) and values[i] != "null":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        
        return root

class CodecMinimal:
    """
    Most Space-Efficient Solution
    
    Uses binary encoding instead of string representation
    Much more space-efficient for large integers
    """
    
    def serialize(self, root):
        """Binary encoding of preorder traversal"""
        if not root:
            return b""
        
        import struct
        values = []
        
        def preorder(node):
            if node:
                values.append(node.val)
                preorder(node.left)
                preorder(node.right)
        
        preorder(root)
        
        # Pack integers into binary format
        return struct.pack(f'{len(values)}i', *values)
    
    def deserialize(self, data):
        """Deserialize from binary data"""
        if not data:
            return None
        
        import struct
        values = list(struct.unpack(f'{len(data)//4}i', data))
        self.index = 0
        
        def build_tree(min_val, max_val):
            if self.index >= len(values):
                return None
            
            val = values[self.index]
            if val < min_val or val > max_val:
                return None
            
            self.index += 1
            root = TreeNode(val)
            root.left = build_tree(min_val, val)
            root.right = build_tree(val, max_val)
            return root
        
        return build_tree(float('-inf'), float('inf'))

# Test cases and utility functions
def build_test_bst1():
    """
    Build BST:     2
                  / \
                 1   3
    
    Preorder: [2, 1, 3]
    """
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    return root

def build_test_bst2():
    """
    Build BST:       5
                   /   \
                  2     7
                 / \   / \
                1   3 6   8
                     \
                      4
    
    Preorder: [5, 2, 1, 3, 4, 7, 6, 8]
    """
    root = TreeNode(5)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(8)
    root.left.right.right = TreeNode(4)
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

def inorder_traversal(root):
    """Helper to verify BST property after deserialization"""
    result = []
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result

def preorder_traversal(root):
    """Helper to verify preorder traversal"""
    result = []
    def preorder(node):
        if node:
            result.append(node.val)
            preorder(node.left)
            preorder(node.right)
    preorder(root)
    return result

def test_codec(codec_class, tree, test_name):
    """Test a codec implementation"""
    codec = codec_class()
    
    # Serialize
    serialized = codec.serialize(tree)
    print(f"{test_name}:")
    print(f"  Serialized: {serialized}")
    
    # Deserialize
    deserialized = codec.deserialize(serialized)
    
    # Verify correctness
    original_inorder = inorder_traversal(tree)
    reconstructed_inorder = inorder_traversal(deserialized)
    
    print(f"  Original inorder: {original_inorder}")
    print(f"  Reconstructed inorder: {reconstructed_inorder}")
    print(f"  Correct: {original_inorder == reconstructed_inorder}")
    print()

def test_solutions():
    # Test tree 1
    tree1 = build_test_bst1()
    print("Test 1 - Simple BST [2,1,3]:")
    test_codec(Codec, tree1, "  Optimal (Preorder)")
    test_codec(CodecIterative, tree1, "  Iterative")
    test_codec(CodecPostorder, tree1, "  Postorder")
    
    # Test tree 2
    tree2 = build_test_bst2()
    print("Test 2 - Complex BST:")
    test_codec(Codec, tree2, "  Optimal (Preorder)")
    test_codec(CodecWithNulls, tree2, "  With Nulls")
    
    # Test linear tree
    tree3 = build_linear_bst()
    print("Test 3 - Linear BST:")
    test_codec(Codec, tree3, "  Optimal (Preorder)")
    test_codec(CodecLevelOrder, tree3, "  Level Order")
    
    # Test empty tree
    print("Test 4 - Empty tree:")
    codec = Codec()
    serialized_empty = codec.serialize(None)
    deserialized_empty = codec.deserialize(serialized_empty)
    print(f"  Serialized: '{serialized_empty}'")
    print(f"  Deserialized is None: {deserialized_empty is None}")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Design functions to serialize BST to string and deserialize back
   - Serialization should be compact and efficient
   - Must preserve exact tree structure
   - Focus on BST-specific optimizations

2. KEY INSIGHT - BST PROPERTY:
   - For BST, preorder traversal alone is sufficient!
   - No need for null markers like in general binary trees
   - BST property determines where each node goes during reconstruction
   - This is the key optimization over general binary tree serialization

3. OPTIMAL APPROACH - PREORDER WITHOUT NULLS:

   SERIALIZE:
   - Simple preorder traversal
   - Store only non-null values
   - Join with delimiter (comma)

   DESERIALIZE:
   - Use preorder sequence with BST property
   - For each value, determine valid range based on BST constraints
   - Recursively build left and right subtrees

4. WHY THIS WORKS:
   - Preorder visits parent before children
   - BST property: left < parent < right
   - Each node has valid range based on ancestors
   - If value outside range, it belongs to different subtree

5. ALGORITHM WALKTHROUGH (DESERIALIZE):
   - Start with range (-∞, +∞)
   - For each value, check if it fits current range
   - If yes: create node, narrow ranges for children
   - If no: backtrack (value belongs to ancestor's other subtree)

6. COMPLEXITY ANALYSIS:
   - Serialize: O(n) time, O(n) space
   - Deserialize: O(n) time, O(h) space for recursion
   - String storage: O(n) characters
   - Optimal for BST serialization

7. ALTERNATIVE APPROACHES:

   APPROACH 1: Include Null Markers
   - Works for any binary tree
   - Less efficient for BST (unnecessary nulls)
   - Serialize: "2,1,null,null,3,null,null"

   APPROACH 2: Level Order Traversal
   - BFS with null markers
   - More intuitive but less efficient
   - Requires handling incomplete levels

   APPROACH 3: Postorder Traversal
   - Also leverages BST property
   - Build from right to left during deserialization
   - Same efficiency as preorder

8. SPACE OPTIMIZATIONS:
   - Binary encoding instead of strings
   - Variable-length encoding for integers
   - Bit packing for small ranges

9. INTERVIEW PRESENTATION:
   - Start with: "I'll leverage BST property to avoid null markers"
   - Explain preorder + range validation insight
   - Code the clean recursive solution
   - Walk through example showing range constraints
   - Mention alternatives if asked

10. FOLLOW-UP QUESTIONS:
    - "What if it's not BST?" → Need null markers for general binary tree
    - "How to make it more space-efficient?" → Binary encoding
    - "What about very large trees?" → Streaming/chunked serialization
    - "Thread safety?" → Immutable approach or synchronization

11. WHY THIS IS ELEGANT:
    - Leverages problem-specific constraints (BST property)
    - Much more compact than general tree serialization
    - Clean recursive structure
    - Optimal time and space complexity

12. EDGE CASES:
    - Empty tree → return empty string
    - Single node → just the value
    - Linear tree (all left or all right)
    - Large integers → consider overflow

13. COMMON MISTAKES:
    - Forgetting BST property optimization
    - Incorrect range management during deserialization
    - Not handling empty tree properly
    - Using unnecessary null markers

14. COMPARISON WITH PROBLEM 297:
    - Problem 297: Serialize any binary tree (needs nulls)
    - Problem 449: BST-specific (can skip nulls)
    - This problem allows more efficient solution

15. KEY INSIGHT TO ARTICULATE:
    "The key insight is that for BSTs, preorder traversal alone is sufficient 
    because the BST property determines the structure. During deserialization, 
    I can use range constraints to determine which subtree each value belongs 
    to, eliminating the need for null markers that would be required for 
    general binary trees."

16. IMPLEMENTATION TIPS:
    - Use instance variable for index in deserialization
    - Handle empty string case explicitly
    - Use appropriate data types (int vs string)
    - Consider delimiter choice (comma is standard)

17. OPTIMIZATION OPPORTUNITIES:
    - Binary format for production systems
    - Compression for repeated patterns
    - Streaming for very large trees
    - Custom encoding schemes
"""
