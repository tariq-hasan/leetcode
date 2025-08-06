"""
LeetCode 705: Design HashSet

Design a HashSet without using any built-in hash table libraries.

Implement MyHashSet class:
- MyHashSet() initializes the HashSet object.
- void add(key) inserts the value key into the HashSet.
- bool contains(key) returns whether the value key exists in the HashSet or not.
- void remove(key) removes the value key in the HashSet. If key does not exist, do nothing.

Example:
hashSet = MyHashSet()
hashSet.add(1)      
hashSet.add(2)      
hashSet.contains(1) # return True
hashSet.contains(3) # return False (not found)
hashSet.add(2)      
hashSet.contains(2) # return True
hashSet.remove(2)   
hashSet.contains(2) # return False (removed)

Note:
- 0 <= key <= 10^6
- At most 10^4 calls will be made to add, remove, and contains.
"""

# Solution 1: Chaining with Dynamic Resizing - RECOMMENDED for interviews
class MyHashSet1:
    """
    Approach: Hash table with chaining (separate chaining) and dynamic resizing
    
    Key concepts:
    - Hash function: key % bucket_count
    - Collision resolution: Chaining (each bucket is a list)
    - Dynamic resizing: Double size when load factor > threshold
    - Load factor: total_elements / bucket_count
    
    Time Complexity:
    - Average: O(1) for all operations
    - Worst case: O(n) if all keys hash to same bucket
    
    Space Complexity: O(n) where n is number of elements
    """
    
    def __init__(self):
        self.initial_capacity = 16
        self.load_factor_threshold = 0.75
        self.buckets = [[] for _ in range(self.initial_capacity)]
        self.size = 0  # Number of elements
    
    def _hash(self, key: int) -> int:
        """Hash function: simple modulo"""
        return key % len(self.buckets)
    
    def _resize(self):
        """
        Resize hash table when load factor exceeds threshold
        Double the capacity and rehash all elements
        """
        old_buckets = self.buckets
        self.buckets = [[] for _ in range(len(old_buckets) * 2)]
        old_size = self.size
        self.size = 0
        
        # Rehash all existing elements
        for bucket in old_buckets:
            for key in bucket:
                self.add(key)
        
        # Restore size (add() increments it)
        self.size = old_size
    
    def add(self, key: int) -> None:
        """Add key to HashSet"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        # Check if key already exists
        if key not in bucket:
            bucket.append(key)
            self.size += 1
            
            # Check if resize is needed
            if self.size > len(self.buckets) * self.load_factor_threshold:
                self._resize()
    
    def remove(self, key: int) -> None:
        """Remove key from HashSet"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        if key in bucket:
            bucket.remove(key)
            self.size -= 1
    
    def contains(self, key: int) -> bool:
        """Check if key exists in HashSet"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        return key in bucket
    
    def get_stats(self):
        """Helper method to show internal statistics"""
        return {
            "capacity": len(self.buckets),
            "size": self.size,
            "load_factor": self.size / len(self.buckets),
            "bucket_distribution": [len(bucket) for bucket in self.buckets]
        }


# Solution 2: Fixed Size with Chaining - Simpler Implementation
class MyHashSet2:
    """
    Approach: Fixed size hash table with chaining
    
    Simpler implementation without dynamic resizing.
    Good for explaining basic concepts but less efficient for large datasets.
    
    Time Complexity: O(n/k) average where k is number of buckets
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self.bucket_count = 1000  # Fixed size
        self.buckets = [[] for _ in range(self.bucket_count)]
    
    def _hash(self, key: int) -> int:
        """Hash function"""
        return key % self.bucket_count
    
    def add(self, key: int) -> None:
        """Add key to HashSet"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        if key not in bucket:
            bucket.append(key)
    
    def remove(self, key: int) -> None:
        """Remove key from HashSet"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        if key in bucket:
            bucket.remove(key)
    
    def contains(self, key: int) -> bool:
        """Check if key exists"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        return key in bucket


# Solution 3: Open Addressing with Linear Probing
class MyHashSet3:
    """
    Approach: Open addressing with linear probing
    
    All elements stored in single array. When collision occurs,
    linearly probe for next available slot.
    
    Pros: Better cache locality, no extra memory for pointers
    Cons: More complex deletion, clustering issues
    
    Time Complexity: O(1) average, O(n) worst case
    Space Complexity: O(capacity)
    """
    
    def __init__(self):
        self.capacity = 1000
        self.size = 0
        # Use None for empty, -1 for deleted (tombstone)
        self.table = [None] * self.capacity
    
    def _hash(self, key: int) -> int:
        """Hash function"""
        return key % self.capacity
    
    def _find_slot(self, key: int) -> int:
        """
        Find slot for key using linear probing
        Returns index where key is or should be placed
        """
        index = self._hash(key)
        original_index = index
        
        while True:
            if self.table[index] is None or self.table[index] == -1:
                # Empty or deleted slot
                return index
            elif self.table[index] == key:
                # Key found
                return index
            
            # Linear probe
            index = (index + 1) % self.capacity
            
            # Prevent infinite loop (table full)
            if index == original_index:
                raise Exception("HashSet is full")
    
    def add(self, key: int) -> None:
        """Add key to HashSet"""
        if self.size >= self.capacity * 0.7:  # Prevent high load factor
            raise Exception("HashSet approaching capacity limit")
        
        index = self._find_slot(key)
        if self.table[index] != key:  # Key not already present
            self.table[index] = key
            self.size += 1
    
    def remove(self, key: int) -> None:
        """Remove key from HashSet"""
        index = self._find_slot(key)
        if self.table[index] == key:
            self.table[index] = -1  # Mark as deleted (tombstone)
            self.size -= 1
    
    def contains(self, key: int) -> bool:
        """Check if key exists"""
        index = self._find_slot(key)
        return self.table[index] == key


# Solution 4: Simple Boolean Array (for specific constraints)
class MyHashSet4:
    """
    Approach: Direct indexing using boolean array
    
    Since keys are limited to 0 <= key <= 10^6, we can use direct indexing.
    Not a general hash table solution but works for this specific problem.
    
    Pros: O(1) guaranteed for all operations, simple
    Cons: Wastes space, only works for small, dense key ranges
    
    Time Complexity: O(1) for all operations
    Space Complexity: O(max_key)
    """
    
    def __init__(self):
        self.max_key = 1000001  # 0 to 10^6 inclusive
        self.data = [False] * self.max_key
    
    def add(self, key: int) -> None:
        """Add key to HashSet"""
        self.data[key] = True
    
    def remove(self, key: int) -> None:
        """Remove key from HashSet"""
        self.data[key] = False
    
    def contains(self, key: int) -> bool:
        """Check if key exists"""
        return self.data[key]


# Solution 5: Two-Level Hashing (Square Root Decomposition)
class MyHashSet5:
    """
    Approach: Two-level hashing using square root decomposition
    
    Divide key space into √(max_key) buckets, each with √(max_key) slots.
    First level: key // √(max_key), Second level: key % √(max_key)
    
    Good compromise between time and space for sparse datasets.
    
    Time Complexity: O(1) for all operations
    Space Complexity: O(√(max_key)) + O(number of elements)
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
    
    def add(self, key: int) -> None:
        """Add key to HashSet"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        # Initialize bucket if needed
        if self.buckets[bucket_idx] is None:
            self.buckets[bucket_idx] = [False] * self.bucket_size
        
        self.buckets[bucket_idx][item_idx] = True
    
    def remove(self, key: int) -> None:
        """Remove key from HashSet"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        if self.buckets[bucket_idx] is not None:
            self.buckets[bucket_idx][item_idx] = False
    
    def contains(self, key: int) -> bool:
        """Check if key exists"""
        bucket_idx = self._get_bucket_index(key)
        item_idx = self._get_item_index(key)
        
        if self.buckets[bucket_idx] is None:
            return False
        
        return self.buckets[bucket_idx][item_idx]


def test_hash_set_implementations():
    """Test all HashSet implementations"""
    
    implementations = [
        ("Chaining with Dynamic Resize", MyHashSet1),
        ("Fixed Size Chaining", MyHashSet2),
        ("Linear Probing", MyHashSet3),
        ("Boolean Array", MyHashSet4),
        ("Two-Level Hashing", MyHashSet5)
    ]
    
    test_operations = [
        ("add", 1),
        ("add", 2),
        ("contains", 1),    # True
        ("contains", 3),    # False
        ("add", 2),         # Duplicate
        ("contains", 2),    # True
        ("remove", 2),
        ("contains", 2),    # False
        ("add", 1000000),   # Large key
        ("contains", 1000000), # True
        ("remove", 1000000),
        ("contains", 1000000), # False
    ]
    
    for name, HashSetClass in implementations:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        
        try:
            hashset = HashSetClass()
            
            for operation, key in test_operations:
                if operation == "add":
                    hashset.add(key)
                    print(f"add({key}) -> Added")
                elif operation == "remove":
                    hashset.remove(key)
                    print(f"remove({key}) -> Removed")
                elif operation == "contains":
                    result = hashset.contains(key)
                    print(f"contains({key}) -> {result}")
                    
        except Exception as e:
            print(f"Error in {name}: {e}")


def demonstrate_hash_collisions():
    """
    Demonstrate hash collisions and how chaining handles them
    """
    print("\n" + "="*60)
    print("HASH COLLISION DEMONSTRATION")
    print("="*60)
    
    # Use small bucket count to force collisions
    class DemoHashSet:
        def __init__(self):
            self.buckets = [[] for _ in range(5)]  # Only 5 buckets
        
        def _hash(self, key):
            return key % len(self.buckets)
        
        def add(self, key):
            bucket_idx = self._hash(key)
            if key not in self.buckets[bucket_idx]:
                self.buckets[bucket_idx].append(key)
            print(f"add({key}) -> hash={bucket_idx}, bucket={self.buckets[bucket_idx]}")
    
    demo = DemoHashSet()
    
    # These keys will cause collisions
    keys = [1, 6, 11, 2, 7, 12]  # 1,6,11 -> bucket 1; 2,7,12 -> bucket 2
    
    for key in keys:
        demo.add(key)
    
    print(f"\nFinal bucket state:")
    for i, bucket in enumerate(demo.buckets):
        print(f"Bucket {i}: {bucket}")


def analyze_time_complexity():
    """
    Analyze time complexity of different approaches
    """
    print("\n" + "="*60) 
    print("TIME COMPLEXITY ANALYSIS")
    print("="*60)
    
    approaches = [
        {
            "name": "Chaining with Resizing",
            "add": "O(1) amortized",
            "remove": "O(1) average", 
            "contains": "O(1) average",
            "worst_case": "O(n) if all collide",
            "notes": "Best general solution"
        },
        {
            "name": "Fixed Size Chaining", 
            "add": "O(n/k) average",
            "remove": "O(n/k) average",
            "contains": "O(n/k) average", 
            "worst_case": "O(n) if all collide",
            "notes": "Simple but degrades with load"
        },
        {
            "name": "Linear Probing",
            "add": "O(1) average",
            "remove": "O(1) average", 
            "contains": "O(1) average",
            "worst_case": "O(n) clustering",
            "notes": "Good cache locality"
        },
        {
            "name": "Boolean Array",
            "add": "O(1) guaranteed",
            "remove": "O(1) guaranteed",
            "contains": "O(1) guaranteed", 
            "worst_case": "O(1) always",
            "notes": "Perfect but uses O(max_key) space"
        },
        {
            "name": "Two-Level Hashing",
            "add": "O(1) guaranteed", 
            "remove": "O(1) guaranteed",
            "contains": "O(1) guaranteed",
            "worst_case": "O(1) always", 
            "notes": "Space efficient for sparse data"
        }
    ]
    
    print(f"{'Approach':<25} {'Add':<15} {'Remove':<15} {'Contains':<15} {'Notes'}")
    print("-" * 90)
    
    for approach in approaches:
        print(f"{approach['name']:<25} {approach['add']:<15} {approach['remove']:<15} {approach['contains']:<15} {approach['notes']}")


def show_load_factor_impact():
    """
    Demonstrate impact of load factor on performance
    """
    print("\n" + "="*60)
    print("LOAD FACTOR IMPACT DEMONSTRATION") 
    print("="*60)
    
    print("Load Factor = (Number of Elements) / (Number of Buckets)")
    print("\nTypical thresholds:")
    print("- Load Factor < 0.75: Good performance")
    print("- Load Factor > 0.75: Start to see degradation") 
    print("- Load Factor > 1.0: Significant degradation")
    print("\nDynamic resizing keeps load factor low by doubling capacity")
    
    # Show example
    hashset = MyHashSet1()
    
    print(f"\nInitial state: {hashset.get_stats()}")
    
    # Add elements to trigger resize
    for i in range(20):
        hashset.add(i)
        if i in [12, 16, 19]:  # Show stats at interesting points
            stats = hashset.get_stats()
            print(f"After adding {i+1} elements: Load factor = {stats['load_factor']:.3f}, Capacity = {stats['capacity']}")


if __name__ == "__main__":
    test_hash_set_implementations()
    demonstrate_hash_collisions()
    analyze_time_complexity()
    show_load_factor_impact()


"""
INTERVIEW STRATEGY:

1. Problem Understanding (2-3 minutes):
   - "Need to implement HashSet from scratch without built-in hash tables"
   - "Core operations: add, remove, contains - want O(1) average time"
   - "Key challenge: Handle hash collisions efficiently"

2. Approach Discussion (5-7 minutes):
   - Start with basic concepts:
     * Hash function: maps keys to bucket indices
     * Collision resolution: chaining vs open addressing
     * Load factor: ratio of elements to buckets
   
   - Discuss trade-offs:
     * Chaining: Simple, handles high load well
     * Open addressing: Better cache locality, more complex deletion
     * Dynamic resizing: Maintains performance as dataset grows

3. Implementation Choice (8-12 minutes):
   - Recommend Solution 1 (chaining with dynamic resizing)
   - Implement core methods: add, remove, contains
   - Explain hash function choice and collision handling
   - Show dynamic resizing logic

4. Optimization Discussion (3-5 minutes):
   - "Could use different hash functions (multiply-shift, etc.)"
   - "Could implement open addressing with linear/quadratic probing"
   - "For this specific problem, could use boolean array"

5. Complexity Analysis (2-3 minutes):
   - Average case: O(1) all operations
   - Worst case: O(n) if all keys hash to same bucket
   - Amortized O(1) with dynamic resizing

KEY CONCEPTS TO MENTION:
- "Hash function distributes keys across buckets"
- "Chaining handles collisions by storing lists in each bucket"
- "Load factor determines when to resize"
- "Dynamic resizing maintains O(1) average performance"

ALTERNATIVE APPROACHES:
- Fixed size: Simpler but degrades with load
- Linear probing: Better cache performance
- Boolean array: Perfect for dense, bounded keys
- Two-level hashing: Space efficient for sparse data

FOLLOW-UP QUESTIONS:
- "What if keys aren't integers?" → Discuss string hashing
- "How to handle deletions in open addressing?" → Tombstone markers
- "What's a good hash function?" → Division, multiplication, universal hashing
- "Thread safety?" → Discuss locking strategies
- "Memory usage optimization?" → Mention Robin Hood hashing, cuckoo hashing

COMMON MISTAKES:
- Forgetting to handle collisions
- Not considering load factor impact
- Poor hash function choice
- Not handling edge cases (empty set, duplicates)
"""
