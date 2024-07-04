# Table of Contents

1. [Self-Balancing Trees](#associative-arrays--maps--dictionaries)
   - [Binary Tree](#binary-tree)
     - [AVL Tree](#avl-tree)
     - [Red-Black Tree](#red-black-tree)
   - [N-ary Tree](#n-ary-tree)
     - [B-Tree](#b-tree)
     - [B+-Tree](#b-tree-1)
2. [Binary Tree](#binary-tree-1)
   - [Binary Search Tree](#binary-search-tree)
3. [N-ary Tree](#n-ary-tree-1)
   - [Ternary Tree](#ternary-tree)
4. [Trie (Prefix Tree)](#trie-prefix-tree)
5. [Segment Tree](#segment-tree)
6. [Heap](#heap)
   - [Binary Heap](#binary-heap)
   - [Priority Queue](#priority-queue)

# Self-Balancing Trees

- Definition: The tree structure automatically adjusts to maintain a balanced height.

- This balancing is achieved by applying specific rules and mechanisms that adjust the tree's structure after modifications (like insertions or deletions) to maintain its balanced properties.

- Time complexity for insertion, deletion, and search operations: _O(log n)_

## Binary Tree

### AVL Tree

### Red-Black Tree

## N-ary Tree

### B-Tree

- maintain sorted data and allow searches, sequential access, insertions, and deletions in logarithmic time

- maintain balance by ensuring that all leaf nodes are at the same depth, which helps keep operations efficient

- each node can contain a variable number of keys and children, subject to certain constraints

- Properties: Nodes can have multiple children and store multiple keys. Designed to work well on storage systems that read and write large blocks of data.

- Usage: Commonly used in databases and file systems to manage large datasets.

- Advantages: Efficient disk reads/writes, keeps data balanced, and supports a large number of children per node.

### B+-Tree

- A variant of the B-tree that maintains balance to ensure efficient operations such as search, insertion, and deletion.

- Like B-trees, B++-trees keep all leaf nodes at the same depth, maintaining balance and ensuring logarithmic time complexity for operations.

- In B++-trees, all keys are stored in the leaf nodes, while internal nodes store only keys that direct the search. This means that each leaf node is linked to its successor leaf node, facilitating efficient range queries and sequential access.

- Similar to B-trees, nodes in B++-trees can have a variable number of children within a predefined range.

- Properties: A variant of the B-Tree where all values are stored at the leaf level, and internal nodes store only keys.

- Usage: Often used in database indexing due to its ability to handle range queries efficiently.

- Advantages: Better performance for sequential access and range queries compared to B-Trees.

# Binary Tree

- Definition: Each node has at most two children.

## Binary Search Tree

- Definition: For any given node, all elements in the left subtree are smaller, and all elements in the right subtree are larger.

- Time complexity for insertion, deletion, and search operations: _O(h)_
  - _h ~ log n_ in the average case of balanced trees
  - _h ~ n_ in the worst case of skewed trees

# N-ary Tree

## Ternary Tree

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
