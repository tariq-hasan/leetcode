"""
LeetCode 706: Design HashMap

Design a HashMap without using any built-in hash table libraries.

Implement MyHashMap class:
- MyHashMap() initializes the HashMap object with an empty map.
- void put(key, value) inserts a (key, value) pair into the HashMap. 
  If the key already exists, update the corresponding value.
- int get(key) returns the value to which the specified key is mapped, 
  or -1 if this map contains no mapping for the key.
- void remove(key) removes the key and its corresponding value if the map contains the mapping for the key.

Example:
hashMap = MyHashMap()
hashMap.put(1, 1)    
hashMap.put(2, 2)    
hashMap.get(1)       # return 1
hashMap.get(3)       # return -1 (not found)
hashMap.put(2, 1)    # update existing value
hashMap.get(2)       # return 1 
hashMap.remove(2)    
hashMap.get(2)       # return -1 (removed)

Note:
- 0 <= key, value <= 10^6
- At most 10^4 calls will be made to put, get, and remove.
"""

# Solution 1: Chaining with Dynamic Resizing - RECOMMENDED for interviews
class MyHashMap1:
    """
    Approach: Hash table with separate chaining and dynamic resizing
    
    Key differences from HashSet:
    - Store (key, value) pairs instead of just keys
    - put() can update existing values
    - get() returns value or -1 if not found
    
    Time Complexity:
    - Average: O(1) for all operations
    - Worst case: O(n) if all keys hash to same bucket
    
    Space Complexity: O(n) where n is number of key-value pairs
    """
    
    def __init__(self):
        self.initial_capacity = 16
        self.load_factor_threshold = 0.75
        # Each bucket stores list of (key, value) tuples
        self.buckets = [[] for _ in range(self.initial_capacity)]
        self.size = 0
    
    def _hash(self, key: int) -> int:
        """Hash function using simple modulo"""
        return key % len(self.buckets)
    
    def _resize(self):
        """
        Resize hash table when load factor exceeds threshold
        Double capacity and rehash all key-value pairs
        """
        old_buckets = self.buckets
        self.buckets = [[] for _ in range(len(old_buckets) * 2)]
        old_size = self.size
        self.size = 0
        
        # Rehash all existing key-value pairs
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
        
        # Restore size (put() increments it for new keys)
        self.size = old_size
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        # Check if key already exists (update case)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Key doesn't exist, add new pair
        bucket.append((key, value))
        self.size += 1
        
        # Check if resize is needed
        if self.size > len(self.buckets) * self.load_factor_threshold:
            self._resize()
    
    def get(self, key: int) -> int:
        """Get value for key, return -1 if not found"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return -1  # Key not found
    
    def remove(self, key: int) -> None:
        """Remove key-value pair if exists"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
    
    def get_stats(self):
        """Helper method to show internal statistics"""
        bucket_sizes = [len(bucket) for bucket in self.buckets]
        return {
            "capacity": len(self.buckets),
            "size": self.size,
            "load_factor": self.size / len(self.buckets) if self.buckets else 0,
            "max_bucket_size": max(bucket_sizes) if bucket_sizes else 0,
            "avg_bucket_size": sum(bucket_sizes) / len(bucket_sizes) if bucket_sizes else 0
        }


# Solution 2: Fixed Size with Chaining - Simpler Implementation
class MyHashMap2:
    """
    Approach: Fixed size hash table with chaining
    
    Simpler implementation without dynamic resizing.
    Good for explaining basic concepts but less scalable.
    """
    
    def __init__(self):
        self.bucket_count = 1000  # Fixed size
        self.buckets = [[] for _ in range(self.bucket_count)]
    
    def _hash(self, key: int) -> int:
        """Hash function"""
        return key % self.bucket_count
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        # Check if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new pair
        bucket.append((key, value))
    
    def get(self, key: int) -> int:
        """Get value for key"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return -1
    
    def remove(self, key: int) -> None:
        """Remove key-value pair"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return


# Solution 3: Open Addressing with Linear Probing
class MyHashMap3:
    """
    Approach: Open addressing with linear probing
    
    Store key-value pairs directly in array slots.
    Use linear probing for collision resolution.
    
    Pros: Better cache locality, less memory overhead
    Cons: More complex deletion handling, clustering
    """
    
    def __init__(self):
        self.capacity = 1000
        self.size = 0
        # Use None for empty, special sentinel for deleted
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.deleted = [False] * self.capacity  # Tombstone markers
    
    def _hash(self, key: int) -> int:
        """Hash function"""
        return key % self.capacity
    
    def _find_slot(self, key: int) -> int:
        """
        Find slot for key using linear probing
        Returns index where key is found or should be placed
        """
        index = self._hash(key)
        original_index = index
        
        while True:
            if self.keys[index] is None and not self.deleted[index]:
                # Empty slot found
                return index
            elif self.keys[index] == key and not self.deleted[index]:
                # Key found
                return index
            elif self.keys[index] is None and self.deleted[index]:
                # Deleted slot, continue probing but remember this spot
                pass
            
            # Linear probe
            index = (index + 1) % self.capacity
            
            # Prevent infinite loop
            if index == original_index:
                raise Exception("HashMap is full")
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        if self.size >= self.capacity * 0.7:
            raise Exception("HashMap approaching capacity")
        
        index = self._find_slot(key)
        
        if self.keys[index] != key or self.deleted[index]:
            # New key
            self.size += 1
        
        self.keys[index] = key
        self.values[index] = value
        self.deleted[index] = False
    
    def get(self, key: int) -> int:
        """Get value for key"""
        index = self._find_slot(key)
        
        if self.keys[index] == key and not self.deleted[index]:
            return self.values[index]
        
        return -1
    
    def remove(self, key: int) -> None:
        """Remove key-value pair using tombstone"""
        index = self._find_slot(key)
        
        if self.keys[index] == key and not self.deleted[index]:
            self.deleted[index] = True  # Mark as deleted
            self.size -= 1


# Solution 4: Direct Indexing with Arrays (for specific constraints)
class MyHashMap4:
    """
    Approach: Direct indexing using parallel arrays
    
    Since keys are limited to 0 <= key <= 10^6, use direct indexing.
    Not a general hash map but works for this specific problem.
    
    Time: O(1) guaranteed for all operations
    Space: O(max_key) - can be wasteful for sparse data
    """
    
    def __init__(self):
        self.max_key = 1000001
        self.keys = [False] * self.max_key      # Track which keys exist
        self.values = [0] * self.max_key        # Store values
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        self.keys[key] = True
        self.values[key] = value
    
    def get(self, key: int) -> int:
        """Get value for key"""
        if self.keys[key]:
            return self.values[key]
        return -1
    
    def remove(self, key: int) -> None:
        """Remove key-value pair"""
        self.keys[key] = False


# Solution 5: Two-Level Hashing with Key-Value Storage
class MyHashMap5:
    """
    Approach: Two-level hashing using square root decomposition
    
    More space-efficient than direct indexing for sparse data.
    Each bucket contains its own hash table for key-value pairs.
    """
    
    def __init__(self):
        self.bucket_size = 1000  # √(10^6) ≈ 1000
        self.buckets = [None] * self.bucket_size
    
    def _get_bucket_index(self, key: int) -> int:
        """Get first level bucket index"""
        return key // self.bucket_size
    
    def _get_item_index(self, key: int) -> int:
        """Get second level item index"""
        return key % self.bucket_size
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        # Initialize bucket if needed
        if self.buckets[bucket_idx] is None:
            self.buckets[bucket_idx] = {}  # Use dict for simplicity
        
        self.buckets[bucket_idx][item_idx] = value
    
    def get(self, key: int) -> int:
        """Get value for key"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        if (self.buckets[bucket_idx] is not None and 
            item_idx in self.buckets[bucket_idx]):
            return self.buckets[bucket_idx][item_idx]
        
        return -1
    
    def remove(self, key: int) -> None:
        """Remove key-value pair"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        if (self.buckets[bucket_idx] is not None and 
            item_idx in self.buckets[bucket_idx]):
            del self.buckets[bucket_idx][item_idx]


def test_hashmap_implementations():
    """Test all HashMap implementations"""
    
    implementations = [
        ("Chaining with Dynamic Resize", MyHashMap1),
        ("Fixed Size Chaining", MyHashMap2),
        ("Linear Probing", MyHashMap3),
        ("Direct Indexing", MyHashMap4),
        ("Two-Level Hashing", MyHashMap5)
    ]
    
    test_operations = [
        ("put", 1, 10),
        ("put", 2, 20),
        ("get", 1),         # Should return 10
        ("get", 3),         # Should return -1
        ("put", 2, 25),     # Update existing
        ("get", 2),         # Should return 25
        ("remove", 2),
        ("get", 2),         # Should return -1
        ("put", 1000000, 99), # Large key
        ("get", 1000000),   # Should return 99
        ("remove", 1000000),
        ("get", 1000000),   # Should return -1
    ]
    
    for name, HashMapClass in implementations:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        
        try:
            hashmap = HashMapClass()
            
            for operation in test_operations:
                if operation[0] == "put":
                    _, key, value = operation
                    hashmap.put(key, value)
                    print(f"put({key}, {value}) -> Updated")
                elif operation[0] == "get":
                    _, key = operation
                    result = hashmap.get(key)
                    print(f"get({key}) -> {result}")
                elif operation[0] == "remove":
                    _, key = operation
                    hashmap.remove(key)
                    print(f"remove({key}) -> Removed")
                    
        except Exception as e:
            print(f"Error in {name}: {e}")


def demonstrate_collision_handling():
    """
    Demonstrate how HashMap handles collisions with key-value pairs
    """
    print("\n" + "="*60)
    print("COLLISION HANDLING DEMONSTRATION (Key-Value Pairs)")
    print("="*60)
    
    class DemoHashMap:
        def __init__(self):
            self.buckets = [[] for _ in range(5)]  # Small size for collisions
        
        def _hash(self, key):
            return key % len(self.buckets)
        
        def put(self, key, value):
            bucket_idx = self._hash(key)
            bucket = self.buckets[bucket_idx]
            
            # Check if key exists
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    bucket[i] = (key, value)  # Update
                    print(f"put({key}, {value}) -> hash={bucket_idx}, updated in bucket={bucket}")
                    return
            
            # Add new pair
            bucket.append((key, value))
            print(f"put({key}, {value}) -> hash={bucket_idx}, added to bucket={bucket}")
        
        def get(self, key):
            bucket_idx = self._hash(key)
            bucket = self.buckets[bucket_idx]
            
            for k, v in bucket:
                if k == key:
                    print(f"get({key}) -> hash={bucket_idx}, found value={v}")
                    return v
            
            print(f"get({key}) -> hash={bucket_idx}, not found, return -1")
            return -1
    
    demo = DemoHashMap()
    
    # Operations that cause collisions and updates
    operations = [
        ("put", 1, 100),   # bucket 1
        ("put", 6, 600),   # bucket 1 (collision)
        ("put", 1, 111),   # bucket 1 (update existing)
        ("get", 1),        # should return 111
        ("get", 6),        # should return 600
        ("get", 11),       # should return -1 (not exists)
    ]
    
    for op in operations:
        if op[0] == "put":
            demo.put(op[1], op[2])
        else:
            demo.get(op[1])


def compare_hashmap_vs_hashset():
    """
    Compare HashMap implementation differences from HashSet
    """
    print("\n" + "="*60)
    print("HASHMAP vs HASHSET COMPARISON")
    print("="*60)
    
    differences = [
        {
            "aspect": "Data Storage",
            "hashset": "Store keys only",
            "hashmap": "Store (key, value) pairs"
        },
        {
            "aspect": "Collision Storage", 
            "hashset": "List of keys: [key1, key2, ...]",
            "hashmap": "List of tuples: [(key1, val1), (key2, val2), ...]"
        },
        {
            "aspect": "Add/Put Operation",
            "hashset": "Check if key exists, add if not",
            "hashmap": "Check if key exists, update value if yes, add if not"
        },
        {
            "aspect": "Lookup Operation",
            "hashset": "contains(key) -> True/False",
            "hashmap": "get(key) -> value or -1"
        },
        {
            "aspect": "Remove Operation",
            "hashset": "Remove key from bucket",
            "hashmap": "Remove (key, value) pair from bucket"
        },
        {
            "aspect": "Space Usage",
            "hashset": "O(number of unique keys)",
            "hashmap": "O(number of key-value pairs)"
        }
    ]
    
    print(f"{'Aspect':<20} {'HashSet':<35} {'HashMap'}")
    print("-" * 85)
    
    for diff in differences:
        print(f"{diff['aspect']:<20} {diff['hashset']:<35} {diff['hashmap']}")


def analyze_performance_characteristics():
    """
    Analyze performance of different HashMap approaches
    """
    print("\n" + "="*60)
    print("PERFORMANCE CHARACTERISTICS")
    print("="*60)
    
    approaches = [
        {
            "name": "Chaining + Resize",
            "put": "O(1) amortized", 
            "get": "O(1) average",
            "remove": "O(1) average",
            "space": "O(n)",
            "pros": ["Handles high load well", "Simple collision handling", "Predictable performance"],
            "cons": ["Extra memory for pointers", "Cache misses in long chains"]
        },
        {
            "name": "Linear Probing",
            "put": "O(1) average",
            "get": "O(1) average", 
            "remove": "O(1) average",
            "space": "O(capacity)",
            "pros": ["Better cache locality", "No pointer overhead", "Memory efficient"],
            "cons": ["Clustering problems", "Complex deletion", "Performance degrades with load"]
        },
        {
            "name": "Direct Indexing",
            "put": "O(1) guaranteed",
            "get": "O(1) guaranteed",
            "remove": "O(1) guaranteed", 
            "space": "O(max_key)",
            "pros": ["Perfect O(1) performance", "Simplest implementation", "No collisions"],
            "cons": ["Wastes memory for sparse data", "Only works for bounded integer keys"]
        }
    ]
    
    for approach in approaches:
        print(f"\n{approach['name']}:")
        print(f"  Put: {approach['put']}, Get: {approach['get']}, Remove: {approach['remove']}")
        print(f"  Space: {approach['space']}")
        print(f"  Pros: {', '.join(approach['pros'])}")
        print(f"  Cons: {', '.join(approach['cons'])}")


if __name__ == "__main__":
    test_hashmap_implementations()
    demonstrate_collision_handling()
    compare_hashmap_vs_hashset()
    analyze_performance_characteristics()


"""
INTERVIEW STRATEGY:

1. Problem Understanding (2-3 minutes):
   - "HashMap stores key-value pairs with O(1) average access time"
   - "Main difference from HashSet: store values, not just keys"
   - "put() can update existing keys, get() returns values"

2. Approach Discussion (5-7 minutes):
   - "Build on HashSet concepts but store (key, value) pairs"
   - "Same collision resolution strategies: chaining vs open addressing"
   - "Key operations: put (insert/update), get (lookup), remove"
   
   - Collision handling for key-value pairs:
     * Chaining: List of (key, value) tuples in each bucket
     * Open addressing: Parallel arrays for keys and values

3. Implementation Choice (8-12 minutes):
   - Recommend Solution 1 (chaining with dynamic resizing)
   - Show how put() handles both insert and update cases
   - Explain collision resolution with (key, value) tuples
   - Demonstrate dynamic resizing for performance

4. Key Differences from HashSet (3-4 minutes):
   - "Store tuples instead of single keys"
   - "put() must check for existing key to update value"
   - "get() searches and returns value, not boolean"
   - "Same time complexity but slightly more space overhead"

5. Alternative Approaches (2-3 minutes):
   - Fixed size chaining: simpler but less scalable
   - Linear probing: better cache performance
   - Direct indexing: perfect for this problem's constraints

CORE CONCEPTS TO EMPHASIZE:
- "HashMap extends HashSet by storing values with keys"
- "put() operation handles both insert and update cases"
- "Collision resolution stores (key, value) pairs instead of just keys"
- "Same O(1) average performance as HashSet"

KEY IMPLEMENTATION DETAILS:
- "Check if key exists before adding to avoid duplicates"
- "Update existing value if key found, otherwise add new pair"
- "Dynamic resizing maintains performance as dataset grows"
- "Hash collisions handled by storing multiple pairs per bucket"

FOLLOW-UP QUESTIONS:
- "How to handle non-integer keys?" → Different hash functions
- "What about thread safety?" → Synchronization strategies
- "Memory optimization?" → Discuss load factor, open addressing
- "Hash function quality?" → Distribution, collision minimization

COMPARISON POINTS:
- HashSet vs HashMap: keys only vs key-value pairs
- Chaining vs Open Addressing: simplicity vs cache performance
- Fixed vs Dynamic sizing: simplicity vs scalability
- Direct indexing vs Hashing: perfect performance vs general solution

COMMON MISTAKES:
- Forgetting to handle key updates in put()
- Not returning -1 for missing keys in get()
- Inefficient collision resolution
- Not considering load factor impact
"""
