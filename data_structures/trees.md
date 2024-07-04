# Table of Contents

1. [Binary Tree](#binary-tree)
   - [Binary Search Tree](#binary-search-tree)
2. [N-ary Tree](#n-ary-tree)
   - [Ternary Tree](#ternary-tree)
3. [Self-Balancing Trees](#self-balancing-trees)
   - [Binary Tree: AVL Tree](#binary-tree-avl-tree)
   - [Binary Tree: Red-Black Tree](#binary-tree-red-black-tree)
   - [N-ary Tree: B-Tree](#n-ary-tree-b-tree)
   - [N-ary Tree: B+-Tree](#n-ary-tree-b-tree-1)
4. [Trie (Prefix Tree)](#trie-prefix-tree)
5. [Segment Tree](#segment-tree)
6. [Heap](#heap)
   - [Binary Heap](#binary-heap)
   - [Priority Queue](#priority-queue)

# Binary Tree

- Definition: Each node has at most two children.

## Binary Search Tree

- Definition: For any given node, all elements in the left subtree are smaller, and all elements in the right subtree are larger.

- Time complexity for insertion, deletion, and search operations: _O(h)_
  - _h ~ log n_ in the average case of balanced trees
  - _h ~ n_ in the worst case of skewed trees

# N-ary Tree

## Ternary Tree

# Self-Balancing Trees

- Definition: The tree structure automatically adjusts to maintain a balanced height.

- This balancing is achieved by applying specific rules and mechanisms that adjust the tree's structure after modifications (like insertions or deletions) to maintain its balanced properties.

- Time complexity for insertion, deletion, and search operations: _O(log n)_

- Key characteristics of self-balancing trees include:
  - Height Maintenance: The height of the tree remains approximately log n, where n is the number of nodes. This ensures that the tree's depth does not become too large, preventing operations from degrading to linear time complexity.
  - Rebalancing Operations: After insertions or deletions, the tree performs rotations or restructuring to maintain balance. These operations ensure that the tree's height remains optimal.
  - Uniform Depth: In self-balancing trees, the path lengths from the root to any leaf node are kept as uniform as possible. This minimizes the difference in heights between the shortest and longest paths, ensuring efficient access times.

- Examples of self-balancing trees include:
  - AVL Trees: These trees maintain balance by ensuring that the height difference between the left and right subtrees of any node is at most one. Rotations are used to rebalance the tree after insertions or deletions.
  - Red-Black Trees: These trees enforce a set of properties (involving node colors and their relationships) to ensure that the longest path from the root to a leaf is no more than twice the length of the shortest path. Rotations and color changes are used to maintain these properties.
  - B-Trees and B++-Trees: These generalize binary search trees by allowing nodes to have more than two children and ensuring that all leaf nodes are at the same depth. They use splitting and merging of nodes to maintain balance during insertions and deletions.

- By maintaining balance, balanced trees prevent worst-case scenarios where the tree could degrade into a structure with linear time complexity operations, ensuring consistent performance. Explain.

- The balance in a balanced tree ensures that the tree remains relatively balanced and avoids degenerating into a linear structure (like a linked list), which would degrade its efficiency for operations like insertion, deletion, and search. Explain.

- The balance in a balanced tree helps maintain efficient operations by ensuring that the tree remains relatively shallow, thereby optimizing the time complexity of operations. Explain.

- If not properly balanced, the tree can degenerate into a linked list, leading to degraded performance (worst-case O(n) time complexity for operations). Explain.

## Binary Tree: AVL Tree

- Balancing Method: Ensures that the heights of the left and right subtrees of any node differ by at most one.

- Rotations: Uses single and double rotations to maintain balance after insertions and deletions.

- Properties: Heights of the left and right subtrees of any node differ by at most one.

- Balancing: Rotations (single and double) are used to maintain balance after insertions and deletions.

- Advantages: Guarantees strict balance, leading to efficient operations.

- Disadvantages: Requires more rotations and balancing operations compared to other self-balancing trees.

- What is an AVL tree?

- What is the AVL property?

## Binary Tree: Red-Black Tree

- Balancing Method: Nodes are colored red or black to ensure that the tree remains approximately balanced.

- Properties: No two consecutive red nodes, and the number of black nodes on any path from the root to a leaf is the same.

- Properties: Each node is colored either red or black. The tree maintains balance using specific rules that ensure no two red nodes are adjacent, and every path from a node to its descendant leaves has the same number of black nodes.

- Balancing: Requires fewer rotations than AVL trees, making insertions and deletions generally faster.

- Advantages: Widely used in practice, including in the implementation of standard libraries (e.g., Java's TreeMap, C++'s map).

- Disadvantages: Slightly less balanced than AVL trees, but still ensures O(log n) operations.

- What is a red-black tree?

- What does it mean for a red-black tree to guarantee balance using a set of color constraints on nodes?

## N-ary Tree: B-Tree

- maintain sorted data and allow searches, sequential access, insertions, and deletions in logarithmic time

- maintain balance by ensuring that all leaf nodes are at the same depth, which helps keep operations efficient

- each node can contain a variable number of keys and children, subject to certain constraints

- Properties: Nodes can have multiple children and store multiple keys. Designed to work well on storage systems that read and write large blocks of data.

- Usage: Commonly used in databases and file systems to manage large datasets.

- Advantages: Efficient disk reads/writes, keeps data balanced, and supports a large number of children per node.

- What is a B-tree?

- What does it mean for a B-tree to have a variable number of children per node and be balanced in terms of the number of keys per node?

### N-ary Tree: B+-Tree

- A variant of the B-tree that maintains balance to ensure efficient operations such as search, insertion, and deletion.

- Like B-trees, B++-trees keep all leaf nodes at the same depth, maintaining balance and ensuring logarithmic time complexity for operations.

- In B++-trees, all keys are stored in the leaf nodes, while internal nodes store only keys that direct the search. This means that each leaf node is linked to its successor leaf node, facilitating efficient range queries and sequential access.

- Similar to B-trees, nodes in B++-trees can have a variable number of children within a predefined range.

- Properties: A variant of the B-Tree where all values are stored at the leaf level, and internal nodes store only keys.

- Usage: Often used in database indexing due to its ability to handle range queries efficiently.

- Advantages: Better performance for sequential access and range queries compared to B-Trees.

# Trie (Prefix Tree)

- used to store associative data structures where the keys are usually strings

# Segment Tree

- used for storing intervals or segments of data
- efficiently supports queries like range sum, range minimum/maximum, and updates in logarithmic time complexity

# Heap

- satisfies the heap property

## Binary Heap

- complete binary tree where every parent node has a value less than or equal to its children (min-heap) or greater than or equal to its children (max-heap)

## Priority Queue

- implemented using a heap to efficiently retrieve the highest (or lowest) priority element
