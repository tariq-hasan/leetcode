# LeetCode 2166: Design Bitset
# A Bitset is a data structure that compactly stores bits.

"""
Problem: A Bitset is a data structure that compactly stores bits.

Implement the Bitset class:
- Bitset(int size) Initializes the Bitset with size bits, all initially set to 0.
- void fix(int idx) Sets the bit at index idx to 1. If the bit was already 1, no change.
- void unfix(int idx) Sets the bit at index idx to 0. If the bit was already 0, no change.
- void flip() Flips all bits (0 becomes 1, 1 becomes 0).
- boolean all() Returns true if all bits are set to 1, false otherwise.
- boolean one() Returns true if at least one bit is set to 1, false otherwise.
- int count() Returns the number of bits set to 1.
- String toString() Returns a string representation of the Bitset.

Constraints:
- 1 <= size <= 10^5
- 0 <= idx < size
- At most 10^5 calls in total will be made to fix, unfix, flip, all, one, count, and toString.
"""

# SOLUTION 1: Naive Approach - Direct Array Implementation
class Bitset1:
    def __init__(self, size: int):
        """
        Initialize bitset with all bits set to 0.
        Time: O(size), Space: O(size)
        """
        self.size = size
        self.bits = [0] * size
        self.ones_count = 0
    
    def fix(self, idx: int) -> None:
        """
        Set bit at idx to 1.
        Time: O(1), Space: O(1)
        """
        if self.bits[idx] == 0:
            self.bits[idx] = 1
            self.ones_count += 1
    
    def unfix(self, idx: int) -> None:
        """
        Set bit at idx to 0.
        Time: O(1), Space: O(1)
        """
        if self.bits[idx] == 1:
            self.bits[idx] = 0
            self.ones_count -= 1
    
    def flip(self) -> None:
        """
        Flip all bits.
        Time: O(size) - BOTTLENECK!
        """
        for i in range(self.size):
            self.bits[i] = 1 - self.bits[i]
        self.ones_count = self.size - self.ones_count
    
    def all(self) -> bool:
        """
        Check if all bits are 1.
        Time: O(1), Space: O(1)
        """
        return self.ones_count == self.size
    
    def one(self) -> bool:
        """
        Check if at least one bit is 1.
        Time: O(1), Space: O(1)
        """
        return self.ones_count > 0
    
    def count(self) -> int:
        """
        Count number of 1 bits.
        Time: O(1), Space: O(1)
        """
        return self.ones_count
    
    def toString(self) -> str:
        """
        Convert to string representation.
        Time: O(size), Space: O(size)
        """
        return ''.join(map(str, self.bits))


# SOLUTION 2: Optimized with Flip Flag (Key Optimization)
class Bitset2:
    def __init__(self, size: int):
        """
        Initialize with lazy flip mechanism.
        Time: O(size), Space: O(size)
        """
        self.size = size
        self.bits = [0] * size
        self.ones_count = 0
        self.flipped = False  # KEY: Lazy flip state
    
    def fix(self, idx: int) -> None:
        """
        Set bit at idx to 1, considering flip state.
        Time: O(1), Space: O(1)
        """
        # Determine current actual value
        actual_value = self.bits[idx] if not self.flipped else 1 - self.bits[idx]
        
        if actual_value == 0:  # Currently 0, need to set to 1
            if not self.flipped:
                self.bits[idx] = 1
            else:
                self.bits[idx] = 0  # Store opposite when flipped
            self.ones_count += 1
    
    def unfix(self, idx: int) -> None:
        """
        Set bit at idx to 0, considering flip state.
        Time: O(1), Space: O(1)
        """
        # Determine current actual value
        actual_value = self.bits[idx] if not self.flipped else 1 - self.bits[idx]
        
        if actual_value == 1:  # Currently 1, need to set to 0
            if not self.flipped:
                self.bits[idx] = 0
            else:
                self.bits[idx] = 1  # Store opposite when flipped
            self.ones_count -= 1
    
    def flip(self) -> None:
        """
        Lazy flip - just toggle the flip flag.
        Time: O(1) - OPTIMIZED!
        """
        self.flipped = not self.flipped
        self.ones_count = self.size - self.ones_count
    
    def all(self) -> bool:
        """
        Check if all bits are 1.
        Time: O(1), Space: O(1)
        """
        return self.ones_count == self.size
    
    def one(self) -> bool:
        """
        Check if at least one bit is 1.
        Time: O(1), Space: O(1)
        """
        return self.ones_count > 0
    
    def count(self) -> int:
        """
        Count number of 1 bits.
        Time: O(1), Space: O(1)
        """
        return self.ones_count
    
    def toString(self) -> str:
        """
        Generate string considering flip state.
        Time: O(size), Space: O(size)
        """
        if not self.flipped:
            return ''.join(map(str, self.bits))
        else:
            return ''.join(str(1 - bit) for bit in self.bits)


# SOLUTION 3: Bit Manipulation with Integer Arrays (More Memory Efficient)
class Bitset3:
    def __init__(self, size: int):
        """
        Use integers to pack multiple bits, with flip optimization.
        Time: O(size/32), Space: O(size/32)
        """
        self.size = size
        self.ones_count = 0
        self.flipped = False
        
        # Use 32-bit integers to pack bits
        self.num_ints = (size + 31) // 32
        self.data = [0] * self.num_ints
    
    def _get_bit(self, idx: int) -> int:
        """Helper: Get actual bit value at index."""
        int_idx = idx // 32
        bit_idx = idx % 32
        stored_bit = (self.data[int_idx] >> bit_idx) & 1
        return stored_bit if not self.flipped else 1 - stored_bit
    
    def _set_bit(self, idx: int, value: int) -> None:
        """Helper: Set stored bit value (considering flip state)."""
        int_idx = idx // 32
        bit_idx = idx % 32
        store_value = value if not self.flipped else 1 - value
        
        if store_value:
            self.data[int_idx] |= (1 << bit_idx)
        else:
            self.data[int_idx] &= ~(1 << bit_idx)
    
    def fix(self, idx: int) -> None:
        """
        Set bit at idx to 1.
        Time: O(1), Space: O(1)
        """
        if self._get_bit(idx) == 0:
            self._set_bit(idx, 1)
            self.ones_count += 1
    
    def unfix(self, idx: int) -> None:
        """
        Set bit at idx to 0.
        Time: O(1), Space: O(1)
        """
        if self._get_bit(idx) == 1:
            self._set_bit(idx, 0)
            self.ones_count -= 1
    
    def flip(self) -> None:
        """
        Lazy flip operation.
        Time: O(1), Space: O(1)
        """
        self.flipped = not self.flipped
        self.ones_count = self.size - self.ones_count
    
    def all(self) -> bool:
        """Check if all bits are 1."""
        return self.ones_count == self.size
    
    def one(self) -> bool:
        """Check if at least one bit is 1."""
        return self.ones_count > 0
    
    def count(self) -> int:
        """Count number of 1 bits."""
        return self.ones_count
    
    def toString(self) -> str:
        """Generate string representation."""
        result = []
        for i in range(self.size):
            result.append(str(self._get_bit(i)))
        return ''.join(result)


# SOLUTION 4: Dual Array Approach (Alternative Optimization)
class Bitset4:
    def __init__(self, size: int):
        """
        Maintain both original and flipped arrays.
        Time: O(size), Space: O(2*size)
        """
        self.size = size
        self.original = [0] * size
        self.flipped = [1] * size  # Pre-computed flipped version
        self.ones_count = 0
        self.is_flipped = False
    
    def _get_current_array(self):
        """Get the array representing current state."""
        return self.flipped if self.is_flipped else self.original
    
    def _get_opposite_array(self):
        """Get the array representing opposite state."""
        return self.original if self.is_flipped else self.flipped
    
    def fix(self, idx: int) -> None:
        """
        Set bit at idx to 1.
        Time: O(1), Space: O(1)
        """
        current = self._get_current_array()
        opposite = self._get_opposite_array()
        
        if current[idx] == 0:
            current[idx] = 1
            opposite[idx] = 0
            self.ones_count += 1
    
    def unfix(self, idx: int) -> None:
        """
        Set bit at idx to 0.
        Time: O(1), Space: O(1)
        """
        current = self._get_current_array()
        opposite = self._get_opposite_array()
        
        if current[idx] == 1:
            current[idx] = 0
            opposite[idx] = 1
            self.ones_count -= 1
    
    def flip(self) -> None:
        """
        Flip by swapping which array is current.
        Time: O(1), Space: O(1)
        """
        self.is_flipped = not self.is_flipped
        self.ones_count = self.size - self.ones_count
    
    def all(self) -> bool:
        """Check if all bits are 1."""
        return self.ones_count == self.size
    
    def one(self) -> bool:
        """Check if at least one bit is 1."""
        return self.ones_count > 0
    
    def count(self) -> int:
        """Count number of 1 bits."""
        return self.ones_count
    
    def toString(self) -> str:
        """Generate string from current array."""
        current = self._get_current_array()
        return ''.join(map(str, current))


# Comprehensive testing function
def test_bitset():
    """Test all implementations with various scenarios."""
    
    print("Testing Bitset implementations...")
    
    implementations = [
        ("Naive Array", Bitset1),
        ("Flip Flag Optimized", Bitset2),
        ("Bit Manipulation", Bitset3),
        ("Dual Array", Bitset4)
    ]
    
    for name, BitsetClass in implementations:
        print(f"\n--- Testing {name} ---")
        
        # Test case from LeetCode example
        bs = BitsetClass(5)
        
        bs.fix(3)
        bs.fix(1)
        print(f"After fix(3), fix(1): {bs.toString()}")  # "01010"
        
        bs.flip()
        print(f"After flip(): {bs.toString()}")  # "10101"
        print(f"all(): {bs.all()}")  # False
        print(f"one(): {bs.one()}")  # True  
        print(f"count(): {bs.count()}")  # 3
        
        bs.unfix(0)
        print(f"After unfix(0): {bs.toString()}")  # "00101"
        print(f"count(): {bs.count()}")  # 2
        
        bs.flip()
        print(f"After flip(): {bs.toString()}")  # "11010"
        print(f"all(): {bs.all()}")  # False


def visualize_flip_optimization():
    """Demonstrate how flip optimization works."""
    print("\n" + "="*70)
    print("FLIP OPTIMIZATION VISUALIZATION")
    print("="*70)
    
    bs = Bitset2(6)
    
    def print_state(operation=""):
        if operation:
            print(f"\nAfter {operation}:")
        print(f"Stored bits: {bs.bits}")
        print(f"Flipped flag: {bs.flipped}")
        print(f"Actual representation: {bs.toString()}")
        print(f"Ones count: {bs.count()}")
        print("-" * 50)
    
    print("Initial state:")
    print_state()
    
    # Set some bits
    bs.fix(1)
    bs.fix(4)
    print_state("fix(1), fix(4)")
    
    # First flip
    bs.flip()
    print_state("flip() - O(1) operation!")
    
    # Modify after flip
    bs.fix(0)  # This should set actual bit 0 to 1
    print_state("fix(0) - note stored vs actual")
    
    # Another flip
    bs.flip()
    print_state("flip() again")


def performance_comparison():
    """Compare time complexities of different operations."""
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    
    operations = [
        ("Operation", "Naive", "Flip Flag", "Bit Manip", "Dual Array"),
        ("fix(idx)", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("unfix(idx)", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("flip()", "O(n)", "O(1)", "O(1)", "O(1)"),
        ("all()", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("one()", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("count()", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("toString()", "O(n)", "O(n)", "O(n)", "O(1)"),
        ("Space", "O(n)", "O(n)", "O(n/32)", "O(2n)")
    ]
    
    for row in operations:
        print(f"{row[0]:<12} {row[1]:<8} {row[2]:<10} {row[3]:<12} {row[4]:<12}")


def edge_cases_test():
    """Test various edge cases."""
    print("\n" + "="*50)
    print("EDGE CASES TESTING")
    print("="*50)
    
    # Test with size 1
    print("Testing size 1:")
    bs = Bitset2(1)
    print(f"Initial: {bs.toString()}, all(): {bs.all()}, one(): {bs.one()}")
    
    bs.fix(0)
    print(f"After fix(0): {bs.toString()}, all(): {bs.all()}, one(): {bs.one()}")
    
    bs.flip()
    print(f"After flip(): {bs.toString()}, all(): {bs.all()}, one(): {bs.one()}")
    
    # Test multiple flips
    print("\nTesting multiple flips:")
    bs = Bitset2(3)
    bs.fix(1)
    original = bs.toString()
    print(f"Original: {original}")
    
    bs.flip()
    bs.flip()
    after_double_flip = bs.toString()
    print(f"After double flip: {after_double_flip}")
    print(f"Double flip preserves state: {original == after_double_flip}")
    
    # Test all ones and all zeros
    print("\nTesting boundary cases:")
    bs = Bitset2(3)
    
    # All zeros
    print(f"All zeros: all()={bs.all()}, one()={bs.one()}, count()={bs.count()}")
    
    # All ones
    bs.fix(0)
    bs.fix(1)
    bs.fix(2)
    print(f"All ones: all()={bs.all()}, one()={bs.one()}, count()={bs.count()}")


if __name__ == "__main__":
    test_bitset()
    visualize_flip_optimization()
    performance_comparison()
    edge_cases_test()


"""
INTERVIEW DISCUSSION POINTS:

1. KEY OPTIMIZATION - LAZY FLIP:
   - Problem: Naive flip() is O(n) which is expensive
   - Solution: Use flip flag + lazy evaluation
   - Insight: Don't actually flip bits, just remember that they're flipped

2. FLIP FLAG MECHANISM:
   - Store a boolean flag indicating if bitset is conceptually flipped
   - During fix/unfix: consider flip state to determine actual vs stored values
   - flip() becomes O(1): just toggle flag and update count
   - toString(): generate representation considering flip state

3. STORED VS ACTUAL VALUES:
   - When flipped=False: stored value = actual value
   - When flipped=True: stored value = opposite of actual value
   - fix(idx): ensure actual value becomes 1 (store appropriately)
   - unfix(idx): ensure actual value becomes 0 (store appropriately)

4. COUNT MANAGEMENT:
   - Track ones_count throughout all operations
   - fix(): increment if changing 0→1
   - unfix(): decrement if changing 1→0  
   - flip(): ones_count becomes (size - ones_count)

5. TIME COMPLEXITY ANALYSIS:
   - Solution 1 (Naive): flip() is O(n) bottleneck
   - Solutions 2-4 (Optimized): all operations O(1) except toString() O(n)
   - Space varies: O(n) to O(2n) depending on approach

6. IMPLEMENTATION CHOICES:
   - Solution 2 (Flip Flag): Most intuitive optimization
   - Solution 3 (Bit Manipulation): Memory efficient (32x compression)
   - Solution 4 (Dual Arrays): Simplest logic but double space

7. EDGE CASES TO HANDLE:
   - Size 1 bitset
   - All zeros/all ones scenarios
   - Multiple consecutive flips
   - Fix/unfix on already correct values

8. FOLLOW-UP QUESTIONS:
   - "Can you optimize memory usage?" → Show Solution 3
   - "What if flip() is called very frequently?" → Emphasize O(1) benefit
   - "How would you handle very large bitsets?" → Discuss bit packing
   - "Thread safety considerations?" → Synchronization needs

9. COMMON PITFALLS:
   - Forgetting to consider flip state in fix/unfix
   - Incorrect count management during operations
   - Off-by-one errors in bit manipulation
   - Not handling edge cases (size 1, empty operations)

10. IMPLEMENTATION PREFERENCE:
    - Start with Solution 1 to show understanding
    - Immediately identify O(n) flip limitation
    - Present Solution 2 as key optimization
    - Explain flip flag mechanism thoroughly

11. TESTING STRATEGY:
    - Use provided example for basic verification
    - Test multiple flips to verify correctness
    - Edge cases: size 1, all zeros, all ones
    - Verify that double flip preserves original state

12. KEY INSIGHT FOR INTERVIEWERS:
    The brilliant optimization is realizing we don't need to physically flip bits.
    Instead, we can maintain a conceptual flip state and interpret stored values
    accordingly. This transforms flip() from O(n) to O(1).

13. BIT MANIPULATION TECHNIQUES (Solution 3):
    - Bit packing: store 32 bits per integer
    - Set bit: data[i] |= (1 << pos)
    - Clear bit: data[i] &= ~(1 << pos)
    - Get bit: (data[i] >> pos) & 1

14. ALTERNATIVE APPROACHES TO MENTION:
    - Compressed sparse representations for very sparse bitsets
    - Hierarchical bit vectors for very large sizes
    - Hardware-specific optimizations (SIMD instructions)
"""
