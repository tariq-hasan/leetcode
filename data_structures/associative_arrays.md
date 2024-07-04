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
- Hash Tables are widely used in scenarios where fast access and unordered key storage are sufficient, such as caches, database indexing, and sets.
- Pros: Generally faster average-case performance _O(1)_ for insertions, deletions, and lookups.
- Cons
  - Worst-case performance can degrade to _O(n)_ if many collisions occur or if the hash function is poor.
  - Do not maintain any order of keys.

### Hash Function

- A hash function takes a key and converts it into an integer (the hash code). This integer is then mapped to an index in an array.

- The hash function for a hash table is a crucial component that determines how keys are mapped to indices in the table.
- A good hash function minimizes collisions (where multiple keys hash to the same index) and distributes keys uniformly across the table.
- The choice and design of a hash function depend on the specific requirements and characteristics of the data.
- A well-designed hash function will ensure efficient performance of the hash table by minimizing collisions and evenly distributing keys across the table.

- Here’s how a hash function is generally determined:
  - Characteristics of a Good Hash Function
    - Deterministic: For the same input key, the hash function should always produce the same output.
    - Uniform Distribution: It should distribute keys uniformly across the hash table to minimize collisions.
    - Efficient to Compute: It should be computationally efficient to calculate the hash value.
    - Minimize Collisions: It should minimize the likelihood of different keys producing the same hash value.

- Common Techniques for Designing Hash Functions
  - Division Method (Modulo Method):
    - Formula: h(k) = k mod m
    - Here, k is the key and m is the size of the hash table.
    - Choose m (the table size) to be a prime number to reduce patterns that cause collisions.
  - Multiplication Method:
    - Formula: h(k) = ⌊ m (( kA mod 1 )) ⌋
    - Here, A is a constant (0 < A < 1) and m is the size of the hash table.
    - Often, A is chosen to be (sqrt(5) - 1) / 2 (the fractional part of the golden ratio) to help ensure a good distribution.
  - Universal Hashing:
    - A technique where the hash function is chosen randomly from a family of hash functions, which can help minimize the chance of collisions in a worst-case scenario.
    - This approach is often used in cryptographic applications or where a robust guarantee against collisions is needed.
  - String-Specific Hash Functions:
    - For string keys, hash functions often involve combining the character values in a way that considers the position of each character.
    - Example: Polynomial Rolling Hash
    - Formula: h(k) = ∑ (n - 1) (i = 0) k_i p^i mod m
    - Here, k_i is the i-th character of the string, p is a prime number, and m is the table size.

- Example Hash Functions
  - Java’s hashCode():
    - In Java, each object has a hashCode() method that computes an integer hash value.
    - For example, the String class computes the hash code using:

public int hashCode() {
    int h = 0;
    for (int i = 0; i < value.length; i++) {
        h = 31 * h + value[i];
    }
    return h;
}

    - This uses a polynomial accumulation with a base of 31.
  - Python’s hash():
    - Python’s built-in hash() function uses a combination of bit manipulation and arithmetic operations to produce hash values.

- Custom Hash Functions
  - In some cases, especially when dealing with complex or user-defined data types, you might need to define a custom hash function.
  - This involves:
    - Combining Key Components: For composite keys (e.g., tuples), combine the hash values of the components.
    - Handling Different Data Types: Convert keys to a common format (e.g., converting objects to strings) before hashing.
    - Balancing Simplicity and Distribution: Ensure the function is simple to compute but still provides a good distribution.

### Collision Handling

- Since multiple keys might hash to the same index (collisions), techniques such as chaining (storing a list of entries at each index) or open addressing (finding another open slot in the array) are used to handle these collisions.

- open addressing with probing

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