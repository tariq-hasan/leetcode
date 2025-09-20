# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import deque

class Codec:
    """
    Optimal Solution - Preorder with Null Markers (Most Common)
    
    Key insight: Preorder traversal with explicit null markers allows
    unique reconstruction of any binary tree.
    
    Time Complexity: O(n) for both serialize and deserialize
    Space Complexity: O(n) for storage, O(h) for recursion
    """
    
    def serialize(self, root):
        """Encodes a tree to a single string."""
        def preorder(node):
            if not node:
                vals.append("null")
                return
            
            vals.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        vals = []
        preorder(root)
        return ",".join(vals)
    
    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        def build_tree():
            val = next(vals)
            if val == "null":
                return None
            
            root = TreeNode(int(val))
            root.left = build_tree()
            root.right = build_tree()
            return root
        
        vals = iter(data.split(","))
        return build_tree()

class CodecLevelOrder:
    """
    Level Order (BFS) Solution (Very Intuitive)
    
    Uses level-by-level serialization, easy to understand and debug
    Time Complexity: O(n)
    Space Complexity: O(w) where w is maximum width of tree
    """
    
    def serialize(self, root):
        """Level order traversal with null markers"""
        if not root:
            return "null"
        
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
        
        # Remove trailing nulls for efficiency
        while result and result[-1] == "null":
            result.pop()
        
        return ",".join(result)
    
    def deserialize(self, data):
        """Reconstruct from level order"""
        if data == "null":
            return None
        
        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            # Process left child
            if i < len(values) and values[i] != "null":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # Process right child
            if i < len(values) and values[i] != "null":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        
        return root

class CodecPostorder:
    """
    Postorder Solution (Alternative Approach)
    
    Uses postorder traversal, builds tree from right to left
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    
    def serialize(self, root):
        """Postorder traversal"""
        def postorder(node):
            if not node:
                vals.append("null")
                return
            
            postorder(node.left)
            postorder(node.right)
            vals.append(str(node.val))
        
        vals = []
        postorder(root)
        return ",".join(vals)
    
    def deserialize(self, data):
        """Reconstruct from postorder (right to left)"""
        def build_tree():
            val = vals.pop()
            if val == "null":
                return None
            
            root = TreeNode(int(val))
            # Important: build right first, then left (reverse of postorder)
            root.right = build_tree()
            root.left = build_tree()
            return root
        
        vals = data.split(",")
        return build_tree()

class CodecIterativePreorder:
    """
    Iterative Preorder Solution (Non-Recursive)
    
    Uses explicit stack instead of recursion
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    
    def serialize(self, root):
        """Iterative preorder serialization"""
        if not root:
            return "null"
        
        result = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            if node:
                result.append(str(node.val))
                # Push right first so left is processed first
                stack.append(node.right)
                stack.append(node.left)
            else:
                result.append("null")
        
        return ",".join(result)
    
    def deserialize(self, data):
        """Iterative deserialization"""
        if data == "null":
            return None
        
        values = data.split(",")
        root = TreeNode(int(values[0]))
        stack = [root]
        i = 1
        
        while stack and i < len(values):
            node = stack.pop()
            
            # Process left child
            if i < len(values):
                if values[i] != "null":
                    node.left = TreeNode(int(values[i]))
                    stack.append(node.left)
                i += 1
            
            # Process right child
            if i < len(values):
                if values[i] != "null":
                    node.right = TreeNode(int(values[i]))
                    stack.append(node.right)
                i += 1
        
        return root

class CodecCompact:
    """
    Space-Optimized Solution (Advanced)
    
    Uses more compact encoding to save space
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    
    def serialize(self, root):
        """Compact serialization with custom encoding"""
        def encode_preorder(node):
            if not node:
                return "#"
            
            left_str = encode_preorder(node.left)
            right_str = encode_preorder(node.right)
            
            return f"{node.val}({left_str},{right_str})"
        
        return encode_preorder(root)
    
    def deserialize(self, data):
        """Parse compact format"""
        def parse():
            nonlocal index
            if index >= len(data) or data[index] == '#':
                if index < len(data):
                    index += 1
                return None
            
            # Parse number
            start = index
            if data[index] == '-':
                index += 1
            while index < len(data) and data[index].isdigit():
                index += 1
            
            val = int(data[start:index])
            root = TreeNode(val)
            
            # Skip '('
            index += 1
            root.left = parse()
            # Skip ','
            index += 1
            root.right = parse()
            # Skip ')'
            index += 1
            
            return root
        
        index = 0
        return parse()

class CodecWithIndex:
    """
    Index-Based Solution (Clean Implementation)
    
    Uses explicit index tracking instead of iterator
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    
    def serialize(self, root):
        """Standard preorder"""
        def preorder(node):
            if not node:
                result.append("null")
                return
            
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        result = []
        preorder(root)
        return ",".join(result)
    
    def deserialize(self, data):
        """Deserialize with explicit index"""
        self.index = 0
        values = data.split(",")
        
        def build_tree():
            if self.index >= len(values) or values[self.index] == "null":
                self.index += 1
                return None
            
            root = TreeNode(int(values[self.index]))
            self.index += 1
            root.left = build_tree()
            root.right = build_tree()
            return root
        
        return build_tree()

class CodecBinary:
    """
    Binary Encoding Solution (Production-Quality)
    
    Uses binary format instead of strings for efficiency
    Much more space-efficient for large trees
    """
    
    def serialize(self, root):
        """Binary serialization"""
        import struct
        
        def preorder(node):
            if not node:
                data.append(struct.pack('?', False))  # Boolean marker
                return
            
            data.append(struct.pack('?', True))       # Node exists
            data.append(struct.pack('i', node.val))   # Integer value
            preorder(node.left)
            preorder(node.right)
        
        data = []
        preorder(root)
        return b''.join(data)
    
    def deserialize(self, data):
        """Binary deserialization"""
        import struct
        
        self.index = 0
        
        def build_tree():
            if self.index >= len(data):
                return None
            
            # Read boolean marker
            exists = struct.unpack('?', data[self.index:self.index+1])[0]
            self.index += 1
            
            if not exists:
                return None
            
            # Read integer value
            val = struct.unpack('i', data[self.index:self.index+4])[0]
            self.index += 4
            
            root = TreeNode(val)
            root.left = build_tree()
            root.right = build_tree()
            return root
        
        return build_tree()

# Test cases and utility functions
def build_test_tree1():
    """
    Build tree:     1
                   / \
                  2   3
                     / \
                    4   5
    
    Preorder: [1, 2, null, null, 3, 4, null, null, 5, null, null]
    Level order: [1, 2, 3, null, null, 4, 5]
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    return root

def build_test_tree2():
    """
    Build tree:     1
                   / \
                  2   3
                 /
                4
               /
              5
    
    Skewed tree to test different patterns
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.left.left = TreeNode(5)
    return root

def build_single_node():
    """Single node tree"""
    return TreeNode(42)

def tree_to_list_preorder(root):
    """Convert tree to preorder list for comparison"""
    result = []
    def preorder(node):
        if not node:
            result.append(None)
            return
        result.append(node.val)
        preorder(node.left)
        preorder(node.right)
    preorder(root)
    return result

def tree_to_list_levelorder(root):
    """Convert tree to level order list for comparison"""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result

def test_codec(codec_class, tree, test_name):
    """Test a codec implementation"""
    codec = codec_class()
    
    # Get original tree representation
    original = tree_to_list_preorder(tree)
    
    # Serialize
    serialized = codec.serialize(tree)
    print(f"{test_name}:")
    print(f"  Serialized: {serialized}")
    
    # Deserialize
    deserialized = codec.deserialize(serialized)
    reconstructed = tree_to_list_preorder(deserialized)
    
    # Verify
    print(f"  Original: {original}")
    print(f"  Reconstructed: {reconstructed}")
    print(f"  Correct: {original == reconstructed}")
    print()

def test_solutions():
    # Test tree 1
    tree1 = build_test_tree1()
    print("Test 1 - Standard tree [1,2,3,null,null,4,5]:")
    test_codec(Codec, tree1, "  Preorder")
    test_codec(CodecLevelOrder, tree1, "  Level Order")
    test_codec(CodecPostorder, tree1, "  Postorder")
    
    # Test tree 2 - skewed
    tree2 = build_test_tree2()
    print("Test 2 - Skewed tree:")
    test_codec(Codec, tree2, "  Preorder")
    test_codec(CodecIterativePreorder, tree2, "  Iterative Preorder")
    
    # Test single node
    tree3 = build_single_node()
    print("Test 3 - Single node:")
    test_codec(Codec, tree3, "  Preorder")
    
    # Test empty tree
    print("Test 4 - Empty tree:")
    codec = Codec()
    serialized_empty = codec.serialize(None)
    deserialized_empty = codec.deserialize(serialized_empty)
    print(f"  Serialized: '{serialized_empty}'")
    print(f"  Deserialized is None: {deserialized_empty is None}")
    print()
    
    # Compare serialization sizes
    tree = build_test_tree1()
    print("Serialization size comparison:")
    
    codec1 = Codec()
    s1 = codec1.serialize(tree)
    print(f"  Preorder: {len(s1)} chars - '{s1}'")
    
    codec2 = CodecLevelOrder()
    s2 = codec2.serialize(tree)
    print(f"  Level order: {len(s2)} chars - '{s2}'")
    
    codec3 = CodecCompact()
    s3 = codec3.serialize(tree)
    print(f"  Compact: {len(s3)} chars - '{s3}'")

if __name__ == "__main__":
    test_solutions()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Design functions to convert binary tree to string and back
   - Must preserve exact structure (including null nodes)
   - Serialization should be unambiguous and parseable
   - This is for ANY binary tree (not just BST)

2. KEY INSIGHT - TRAVERSAL + NULL MARKERS:
   - Need traversal order + explicit null markers
   - Preorder is most natural (parent before children)
   - Null markers prevent ambiguity during reconstruction
   - Different from BST version (which doesn't need nulls)

3. SOLUTION APPROACHES:

   APPROACH 1 - Preorder with Nulls (RECOMMENDED):
   - Most intuitive and commonly expected
   - Easy to implement and understand
   - Natural recursive structure

   APPROACH 2 - Level Order (BFS):
   - Very intuitive, matches tree visualization
   - Good for wide trees
   - Easy to debug and verify

   APPROACH 3 - Postorder:
   - Less common but valid
   - Requires building right-to-left during deserialization

   APPROACH 4 - Iterative versions:
   - Show non-recursive thinking
   - More complex but avoids recursion stack

4. SOLUTION CHOICE FOR INTERVIEW:
   - Start with preorder + null markers
   - Clean, recursive, expected solution
   - Mention level order as alternative if asked

5. IMPLEMENTATION DETAILS:
   - Use comma as delimiter
   - "null" string for null nodes
   - Handle empty tree edge case
   - Use iterator or index for deserialization

6. WHY PREORDER WORKS:
   - Parent processed before children
   - Natural tree-building order during reconstruction
   - Recursive structure matches traversal

7. COMPLEXITY ANALYSIS:
   - Time: O(n) for both operations
   - Space: O(n) for serialized string + O(h) for recursion
   - Optimal for this problem

8. STRING FORMAT EXAMPLES:
   - Tree [1,2,3,null,null,4,5] → "1,2,null,null,3,4,null,null,5,null,null"
   - Unambiguous reconstruction possible

9. EDGE CASES:
   - Empty tree → "null"
   - Single node → "1,null,null"
   - Linear tree → many nulls
   - Negative numbers → handle properly

10. INTERVIEW PRESENTATION:
    - Clarify: "This is for any binary tree, so I need null markers"
    - Explain preorder choice: "Parent before children is natural"
    - Code the recursive solution
    - Walk through example showing serialization format
    - Mention alternatives if time permits

11. FOLLOW-UP QUESTIONS:
    - "What if tree is very large?" → Streaming, chunked processing
    - "How to make more space-efficient?" → Binary encoding, compression
    - "Thread safety concerns?" → Immutable approach
    - "What about BST specifically?" → Mention problem 449 optimization

12. COMPARISON WITH BST VERSION (449):
    - General tree: needs null markers
    - BST: can skip nulls using ordering property
    - This problem is more general, less optimal

13. OPTIMIZATION OPPORTUNITIES:
    - Binary encoding instead of strings
    - Compression for repeated patterns
    - Custom delimiters to save space
    - Streaming for very large trees

14. WHY THIS IS IMPORTANT:
    - Fundamental serialization problem
    - Tests tree traversal understanding
    - Real-world application (saving/loading trees)
    - Foundation for more complex tree problems

15. COMMON MISTAKES:
    - Forgetting null markers (leads to ambiguity)
    - Wrong traversal order
    - Not handling empty tree
    - Iterator/index management issues in deserialization

16. KEY INSIGHT TO ARTICULATE:
    "The key insight is that I need both a traversal order AND explicit null 
    markers to uniquely identify any binary tree. Preorder traversal is most 
    natural because I process the parent before children, which matches the 
    tree construction order during deserialization. The null markers prevent 
    ambiguity that would arise from just storing the non-null values."

17. PRODUCTION CONSIDERATIONS:
    - Error handling for malformed input
    - Version compatibility
    - Performance for large trees
    - Memory usage optimization
    - Streaming for real-time applications

18. RELATED PROBLEMS:
    - Problem 449: BST-specific optimization
    - Tree cloning problems
    - Tree comparison problems
    - General graph serialization
"""
