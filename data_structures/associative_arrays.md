# Table of Contents

1. [Associative Arrays / Maps / Dictionaries](#associative-arrays--maps--dictionaries)
2. [Implementation of Associative Arrays](#implementation-of-associative-arrays)
   - [Hashing](#hashing)
     - [Hash Function](#hash-function)
     - [Collision Handling](#collision-handling)
     - [Efficiency](#efficiency)
   - [Balanced Trees](#balanced-trees)
2. [Hash Set](#hash-set)

# Associative Arrays / Maps / Dictionaries

- Data structures that store key-value pairs and allow for efficient retrieval of values based on their associated keys

# Implementation of Associative Arrays

## Hashing

- Hash tables are a common implementation of associative arrays that use a hash function to map keys to indices in an array.
- Indexing: The value associated with the key is stored at the array index generated by the hash function.
- Hash tables are widely used in scenarios where fast access and unordered key storage are sufficient, such as caches, database indexing, and sets.
- Pros: Average-case _O(1)_ performance for insertions, deletions, and lookups.
- Cons: Worst-case performance can degrade to _O(n)_ if many collisions occur or if the hash function is poor.

### Hash Function

- A hash function takes a key and converts it into an integer (the hash code). This integer is then mapped to an index in an array.
- Characteristics of a good hash function
  - Deterministic: For the same input key, the hash function should always produce the same output.
  - Uniform Distribution: It should distribute keys uniformly across the hash table to minimize collisions.
  - Efficient to Compute: It should be computationally efficient to calculate the hash value.
  - Minimize Collisions: It should minimize the likelihood of different keys producing the same hash value.

### Collision Handling

- Chaining
  - Chaining involves creating a linked list (or another data structure, such as a dynamic array) at each index of the hash table to store all elements that hash to the same index.
  - How Chaining Works:
    - Hashing: Compute the hash value for the key to find the index.
    - Collision Handling: If another key is already present at that index, the new key-value pair is added to the linked list at that index.
  - Advantages:
    - Flexibility: Easy to implement and can handle an unlimited number of collisions at each index.
    - Simplicity: Each index of the hash table simply points to a linked list of entries.
  - Disadvantages:
    - Extra Memory: Requires additional memory to store the pointers for the linked lists.
    - Performance: Can degrade to O(n) in the worst case (when all elements hash to the same index).

<br/>

- Open Addressing
  - Open addressing handles collisions by finding another open slot within the hash table.
  - When a collision occurs, the algorithm probes the table in a sequence to find an empty slot.
  - Types of Probing:
    - Linear Probing:
      - If a collision occurs at index _i_, check the next index _(i + 1) % table_size_, then _(i + 2) % table_size_, and so on.
      - This causes primary clustering, where a block of consecutive filled slots forms, making future insertions and searches within this block slower.
    - Quadratic Probing:
      - If a collision occurs at index _i_, check the indices _(i + 1^2) % table_size_, _(i + 2^2) % table_size_, and so on.
      - While quadratic probing reduces primary clustering by spreading out the probe sequence, it can still suffer from secondary clustering.
      - This happens when different keys that hash to the same initial index generate the same probe sequence.
      - Can be complex to ensure that the probing sequence covers all slots in the hash table, especially if the table size is not carefully chosen.
      - Offers a compromise between simple linear probing and more complex methods like double hashing.
      - Addresses primary clustering but requires careful consideration of table size and probe sequence to minimize secondary clustering.
    - Double Hashing:
      - Use a secondary hash function to calculate the step size.
      - If a collision occurs at index _i_, the next index is computed as _(i + j * h2(key)) % table_size_, where _h2_ is a secondary hash function and _j_ is the probe number.
      - This reduces clustering significantly and provides better distribution.
  - Clustering
    - Primary Clustering
      - Cause: When multiple elements hash to the same index (or close to it) and are placed consecutively due to the probing strategy, creating a cluster of filled slots.
      - Impact: New elements that hash to any index within this cluster must search through it sequentially. As the cluster grows, subsequent probes take longer, making insertions and lookups less efficient.
      - How to Mitigate: Use quadratic probing or double hashing instead of linear probing.
      - This occurs in linear probing when a collision leads to a sequence of filled slots forming a contiguous block.
    - Secondary Clustering
      - Cause: When two different keys hash to the same index, they follow the same probing sequence (in quadratic probing or double hashing). As a result, the same set of slots is checked, leading to smaller, localized clusters.
      - Impact: It isn’t as severe as primary clustering, but repeated collisions can still result in multiple keys following the same probing pattern and forming pockets of occupied slots.
      - How to Mitigate: Improve the hash function to distribute elements more uniformly. Use a good secondary hash function in double hashing to reduce repeated probing patterns.
  - Advantages:
    - Memory Efficient: No need for additional memory to store linked lists.
    - Performance: Can offer good performance with a well-designed hash function and probe sequence.
  - Disadvantages:
    - Clustering: Linear and quadratic probing can lead to clustering, where groups of filled slots form, degrading performance.
    - Table Size Dependency: The performance and behavior of open addressing depend heavily on the hash table's load factor (ratio of elements to table size). High load factors can significantly degrade performance.

Cause	Consecutive placement of collided elements	Same probing sequence for certain keys
Cluster Type	Large, continuous clusters	Smaller, non-continuous clusters
Impact	Slower insertions and lookups due to long clusters	Less severe but still creates inefficiencies
How to Avoid	Use quadratic probing or double hashing	Use better hash functions to spread elements

### Efficiency

- When the hash function distributes keys uniformly across the array, and the load factor (ratio of entries to the array size) is kept low, hash tables provide average-case _O(1)_ time complexity for insertions, deletions, and lookups.

## Balanced Trees

- Balanced trees such as Red-Black trees or AVL trees can also be used to implement associative arrays.

- Tree Structure: Keys are stored in nodes of a balanced tree, which maintains a sorted order of keys.

- Balancing: After every insertion or deletion, the tree is rebalanced to ensure that the height of the tree remains logarithmic relative to the number of nodes.

- Search: The balanced tree structure allows for binary search, leading to O(log n) time complexity for insertions, deletions, and lookups.

- Order Preservation: Unlike hash tables, balanced trees maintain the keys in sorted order, which can be beneficial for range queries and ordered traversals.

- Pros: Provide consistent O(log n) performance for all operations, regardless of input. Maintain keys in sorted order, allowing for efficient range queries.

- Cons: Typically slower than hash tables in average-case performance due to the overhead of maintaining balance.

- Balanced Trees are used when ordered key storage is necessary, such as in databases (e.g., B-trees and B+ trees in relational databases) and in-memory data structures that require efficient range queries.

# Hash Set

- How Sets are Implemented Internally
  - Hash Table Structure: Similar to dictionaries, sets use a hash table to store elements. Each element in a set is hashed to determine its position in the table.
  - No Key-Value Pairs: Unlike dictionaries, which store key-value pairs, sets store only keys (the elements themselves). The values are not needed in sets, so they are essentially using the keys of a hash table to represent the set elements.
  - Efficient Operations: Sets provide efficient _O(1)_ average time complexity for operations like membership testing, insertion, and deletion, due to the hash table implementation.

- Key Points
  - Hash Function: Both sets and dictionaries use a hash function to determine where to store elements.
  - Collision Handling: Both handle collisions in similar ways, such as using open addressing with probing.
  - Efficiency: Both provide average-case _O(1)_ time complexity for key operations due to their hash table implementations.

- What does it mean for a hash set to use a hash table as its underlying data structure?

- What does it mean for a hash set to employ a hash function to map elements to buckets (slots) in the hash table, where each bucket contains only one element (or a reference to the element)?

- Elements in a hash set are not stored in any particular order; their placement is determined by the hash function and the hash table's implementation. Explain.


<!-- Operations in Open Addressing:
Search: To find a key, the algorithm follows the same probing sequence it used during insertion, stopping either when the key is found or an empty slot is reached (indicating the key is not present).
Deletion: Special care is required during deletion to mark slots as "deleted" rather than empty. Otherwise, searches may incorrectly stop at the deleted slot, thinking the key doesn’t exist.

Advantages of Open Addressing:
Memory-efficient: No extra space is needed for linked lists or other structures. All elements are stored within the original hash table.
Cache-friendly: Since all data stays within the same array, it benefits from locality of reference (faster memory access).

Disadvantages:
Clustering: Linear probing can create "primary clustering," where consecutive slots are filled, degrading performance.
Load factor limitations: Open addressing requires that the table’s load factor (number of elements / table size) be kept low (typically ≤ 0.7) to avoid excessive probing.
Performance degrades with table fullness: As the table fills up, finding an empty slot becomes slower.

Summary: Open addressing mitigates collisions by storing all elements within the hash table itself and using a probing strategy to find an available slot. This avoids the overhead of maintaining linked lists or arrays, making it more memory-efficient. However, it requires careful management of load factors and can suffer from clustering problems, especially with linear probing. -->
