import random

class Skiplist:
    """
    A probabilistic data structure that maintains elements in sorted order.
    Average time complexity: O(log n) for search, add, and erase operations.
    """
    
    class Node:
        def __init__(self, val=0, level=0):
            self.val = val
            self.forward = [None] * (level + 1)  # Array of forward pointers
    
    def __init__(self):
        # Maximum number of levels (typically 16-32 for practical purposes)
        self.MAX_LEVEL = 16
        # Probability factor for level generation (0.5 is standard)
        self.P = 0.5
        # Current maximum level in the skiplist
        self.level = 0
        # Header node with maximum possible level
        self.header = self.Node(-1, self.MAX_LEVEL)
    
    def _random_level(self):
        """Generate a random level for a new node."""
        level = 0
        while random.random() < self.P and level < self.MAX_LEVEL:
            level += 1
        return level
    
    def search(self, target: int) -> bool:
        """
        Search for target in the skiplist.
        Time: O(log n), Space: O(1)
        """
        current = self.header
        
        # Start from the highest level and go down
        for i in range(self.level, -1, -1):
            # Move forward while next node value is less than target
            while (current.forward[i] and 
                   current.forward[i].val < target):
                current = current.forward[i]
        
        # Move to the next node at level 0
        current = current.forward[0]
        
        # Check if we found the target
        return current is not None and current.val == target
    
    def add(self, num: int) -> None:
        """
        Add num to the skiplist.
        Time: O(log n), Space: O(log n) for update array
        """
        # Array to store nodes that need to be updated
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header
        
        # Find the position to insert by traversing from top level
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].val < num):
                current = current.forward[i]
            update[i] = current
        
        # Generate random level for the new node
        new_level = self._random_level()
        
        # If new level is greater than current level, update header references
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        # Create new node and insert it
        new_node = self.Node(num, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
    
    def erase(self, num: int) -> bool:
        """
        Remove one occurrence of num from skiplist.
        Returns True if num was found and removed, False otherwise.
        Time: O(log n), Space: O(log n) for update array
        """
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header
        
        # Find the node to delete
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].val < num):
                current = current.forward[i]
            update[i] = current
        
        # Get the node to be deleted
        current = current.forward[0]
        
        # If node not found
        if current is None or current.val != num:
            return False
        
        # Update forward pointers to skip the deleted node
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        
        # Update the level of skiplist if necessary
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        
        return True
    
    def display(self):
        """Helper method to visualize the skiplist structure."""
        print("Skiplist structure:")
        for i in range(self.level, -1, -1):
            current = self.header.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(f"{current.val} ", end="")
                current = current.forward[i]
            print()


# Test cases and usage example
if __name__ == "__main__":
    # Example from LeetCode
    skiplist = Skiplist()
    
    # Test operations
    print("Adding elements: 1, 2, 3")
    skiplist.add(1)
    skiplist.add(2) 
    skiplist.add(3)
    
    print(f"Search 0: {skiplist.search(0)}")  # False
    print(f"Search 1: {skiplist.search(1)}")  # True
    
    print(f"Erase 0: {skiplist.erase(0)}")    # False
    print(f"Erase 1: {skiplist.erase(1)}")    # True
    print(f"Search 1: {skiplist.search(1)}")  # False
    
    # Demonstrate with duplicates
    print("\nTesting with duplicates:")
    skiplist.add(1)
    skiplist.add(1)
    print(f"Search 1: {skiplist.search(1)}")  # True
    print(f"Erase 1: {skiplist.erase(1)}")    # True (removes one occurrence)
    print(f"Search 1: {skiplist.search(1)}")  # True (one still remains)
    
    # Display structure (uncomment to see)
    # skiplist.display()


"""
INTERVIEW TALKING POINTS:

1. TIME/SPACE COMPLEXITY:
   - Search: O(log n) expected, O(n) worst case
   - Add: O(log n) expected, O(n) worst case  
   - Erase: O(log n) expected, O(n) worst case
   - Space: O(n * log n) expected for all forward pointers

2. KEY INSIGHTS:
   - Skiplist is a probabilistic alternative to balanced trees
   - Uses multiple levels with decreasing density (geometric distribution)
   - Level 0 contains all elements, higher levels contain subset
   - Random level generation maintains balance probabilistically

3. DESIGN DECISIONS:
   - MAX_LEVEL = 16 is sufficient for most practical purposes (2^16 = 65k elements)
   - P = 0.5 gives good balance between space and time
   - Header node simplifies boundary conditions
   - Forward array size varies per node based on its level

4. EDGE CASES TO MENTION:
   - Empty skiplist
   - Duplicate values (problem allows multiple occurrences)
   - Single element
   - All elements at level 0 (worst case)

5. OPTIMIZATION POSSIBILITIES:
   - Use finger search for sequential operations
   - Adaptive MAX_LEVEL based on skiplist size
   - Memory pool for nodes to reduce allocation overhead
"""
