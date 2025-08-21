"""
LeetCode 528: Random Pick with Weight

Problem: You are given a 0-indexed array of positive integers w where w[i] describes 
the weight of the ith index. You need to implement the function pickIndex(), which 
randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it. 
The probability of picking an index i is w[i] / sum(w).

Key insights:
1. Convert weighted random selection to uniform random selection using cumulative sums
2. Use binary search to find the correct index efficiently
3. Handle edge cases and floating point precision carefully
"""

import random
import bisect

class Solution_CumulativeSum_BinarySearch:
    """
    Approach 1: Cumulative Sum + Binary Search (Optimal)
    
    Time Complexity: 
    - __init__: O(n)
    - pickIndex: O(log n)
    
    Space Complexity: O(n)
    
    Strategy:
    1. Build cumulative sum array during initialization
    2. Generate random number in [0, total_weight)
    3. Use binary search to find the correct bucket
    
    Best for: Most interviews - optimal and demonstrates multiple concepts
    """
    
    def __init__(self, w):
        """
        Initialize with weights array
        Build cumulative sum for O(log n) picking
        """
        self.cumulative_sums = []
        cumsum = 0
        
        # Build cumulative sum array
        for weight in w:
            cumsum += weight
            self.cumulative_sums.append(cumsum)
        
        self.total_weight = cumsum
    
    def pickIndex(self):
        """
        Pick index with probability proportional to weight
        
        Returns: index i with probability w[i] / sum(w)
        """
        # Generate random number in [0, total_weight)
        target = random.randint(0, self.total_weight - 1)
        
        # Binary search for the first cumulative sum > target
        left, right = 0, len(self.cumulative_sums) - 1
        
        while left < right:
            mid = (left + right) // 2
            if self.cumulative_sums[mid] > target:
                right = mid
            else:
                left = mid + 1
        
        return left


class Solution_Bisect:
    """
    Approach 2: Using Python's bisect module
    
    Time Complexity: 
    - __init__: O(n)
    - pickIndex: O(log n)
    
    Space Complexity: O(n)
    
    Cleaner implementation using built-in binary search
    """
    
    def __init__(self, w):
        self.cumulative_sums = []
        cumsum = 0
        
        for weight in w:
            cumsum += weight
            self.cumulative_sums.append(cumsum)
        
        self.total_weight = cumsum
    
    def pickIndex(self):
        # Generate random number in [1, total_weight] for bisect_left
        target = random.randint(1, self.total_weight)
        
        # Find leftmost position where cumsum >= target
        return bisect.bisect_left(self.cumulative_sums, target)


class Solution_AliasMethod:
    """
    Approach 3: Alias Method (Advanced)
    
    Time Complexity:
    - __init__: O(n)
    - pickIndex: O(1)
    
    Space Complexity: O(n)
    
    Advanced algorithm for O(1) picking after O(n) preprocessing
    Good for showing knowledge of advanced algorithms
    """
    
    def __init__(self, w):
        n = len(w)
        self.n = n
        
        # Normalize weights to probabilities
        total = sum(w)
        probs = [weight / total for weight in w]
        
        # Initialize alias method tables
        self.prob = [0.0] * n
        self.alias = [0] * n
        
        # Separate indices into small and large buckets
        small = []
        large = []
        
        # Scale probabilities by n
        scaled_probs = [p * n for p in probs]
        
        for i, p in enumerate(scaled_probs):
            if p < 1.0:
                small.append(i)
            else:
                large.append(i)
        
        # Build alias method tables
        while small and large:
            small_idx = small.pop()
            large_idx = large.pop()
            
            self.prob[small_idx] = scaled_probs[small_idx]
            self.alias[small_idx] = large_idx
            
            # Update the large probability
            scaled_probs[large_idx] = (scaled_probs[large_idx] + 
                                     scaled_probs[small_idx] - 1.0)
            
            if scaled_probs[large_idx] < 1.0:
                small.append(large_idx)
            else:
                large.append(large_idx)
        
        # Handle remaining elements
        while large:
            large_idx = large.pop()
            self.prob[large_idx] = 1.0
        
        while small:
            small_idx = small.pop()
            self.prob[small_idx] = 1.0
    
    def pickIndex(self):
        # Generate random column and coin flip
        col = random.randint(0, self.n - 1)
        coin_flip = random.random()
        
        if coin_flip < self.prob[col]:
            return col
        else:
            return self.alias[col]


class Solution_LinearSearch:
    """
    Approach 4: Linear Search (For comparison)
    
    Time Complexity:
    - __init__: O(n)
    - pickIndex: O(n)
    
    Space Complexity: O(n)
    
    Simple but inefficient approach
    Good for: Understanding the problem, very small inputs
    """
    
    def __init__(self, w):
        self.cumulative_sums = []
        cumsum = 0
        
        for weight in w:
            cumsum += weight
            self.cumulative_sums.append(cumsum)
        
        self.total_weight = cumsum
    
    def pickIndex(self):
        target = random.randint(1, self.total_weight)
        
        # Linear search for first cumulative sum >= target
        for i, cumsum in enumerate(self.cumulative_sums):
            if cumsum >= target:
                return i
        
        return len(self.cumulative_sums) - 1  # Should never reach here


def test_solutions():
    """Test all solutions with various test cases"""
    
    def test_solution_class(SolutionClass, name, weights, num_trials=10000):
        """Test a solution class and analyze distribution"""
        print(f"\nTesting {name}:")
        print(f"Weights: {weights}")
        
        solution = SolutionClass(weights)
        counts = [0] * len(weights)
        
        # Run trials
        for _ in range(num_trials):
            idx = solution.pickIndex()
            counts[idx] += 1
        
        # Calculate actual vs expected probabilities
        total_weight = sum(weights)
        expected_probs = [w / total_weight for w in weights]
        actual_probs = [count / num_trials for count in counts]
        
        print(f"Expected probabilities: {[f'{p:.3f}' for p in expected_probs]}")
        print(f"Actual probabilities:   {[f'{p:.3f}' for p in actual_probs]}")
        
        # Calculate chi-square goodness of fit (simplified)
        chi_square = sum((actual - expected) ** 2 / expected 
                        for actual, expected in zip(actual_probs, expected_probs))
        print(f"Chi-square value: {chi_square:.4f} (lower is better)")
        
        return actual_probs
    
    # Test cases
    test_cases = [
        [1, 3],           # Simple case
        [1, 1, 1, 1],     # Uniform distribution
        [10, 1, 1],       # Heavy bias towards first
        [1, 2, 3, 4],     # Increasing weights
        [5],              # Single element
    ]
    
    solutions = [
        (Solution_CumulativeSum_BinarySearch, "Cumulative Sum + Binary Search"),
        (Solution_Bisect, "Using Bisect"),
        (Solution_AliasMethod, "Alias Method"),
        (Solution_LinearSearch, "Linear Search")
    ]
    
    for weights in test_cases:
        print("=" * 60)
        print(f"TEST CASE: weights = {weights}")
        
        for SolutionClass, name in solutions:
            try:
                test_solution_class(SolutionClass, name, weights, 1000)
            except Exception as e:
                print(f"\n{name}: Error - {e}")


def demonstrate_algorithm():
    """Demonstrate how the cumulative sum + binary search works"""
    weights = [1, 3, 2]
    print("Algorithm Demonstration:")
    print("=" * 50)
    print(f"Weights: {weights}")
    
    # Build cumulative sums
    cumulative_sums = []
    cumsum = 0
    for i, weight in enumerate(weights):
        cumsum += weight
        cumulative_sums.append(cumsum)
        print(f"Index {i}: weight={weight}, cumsum={cumsum}")
    
    total_weight = cumsum
    print(f"\nTotal weight: {total_weight}")
    print(f"Cumulative sums: {cumulative_sums}")
    
    # Show probability ranges
    print(f"\nProbability ranges:")
    prev = 0
    for i, cumsum in enumerate(cumulative_sums):
        prob = weights[i] / total_weight
        print(f"Index {i}: range [{prev}, {cumsum-1}], probability = {prob:.3f}")
        prev = cumsum
    
    # Demonstrate some picks
    print(f"\nSample random picks:")
    random.seed(42)  # For reproducible demo
    
    for _ in range(10):
        target = random.randint(0, total_weight - 1)
        
        # Manual binary search
        left, right = 0, len(cumulative_sums) - 1
        while left < right:
            mid = (left + right) // 2
            if cumulative_sums[mid] > target:
                right = mid
            else:
                left = mid + 1
        
        picked_index = left
        print(f"Random target: {target} -> Index {picked_index}")


def analyze_approaches():
    """Compare different approaches"""
    print("Approach Comparison:")
    print("=" * 60)
    
    approaches = [
        ("Linear Search", "O(n)", "O(n)", "O(n)", "Simple but slow"),
        ("Cumulative + Binary", "O(n)", "O(log n)", "O(n)", "Optimal for most cases"),
        ("Using Bisect", "O(n)", "O(log n)", "O(n)", "Cleaner implementation"),
        ("Alias Method", "O(n)", "O(1)", "O(n)", "Advanced, O(1) picking"),
    ]
    
    print(f"{'Approach':<20} {'Init':<8} {'Pick':<10} {'Space':<8} {'Notes'}")
    print("-" * 75)
    
    for approach, init, pick, space, notes in approaches:
        print(f"{approach:<20} {init:<8} {pick:<10} {space:<8} {notes}")


def edge_cases_analysis():
    """Analyze edge cases and their handling"""
    print("Edge Cases Analysis:")
    print("=" * 50)
    
    edge_cases = [
        ("Single element", [5], "Always return 0"),
        ("All equal weights", [1, 1, 1], "Uniform distribution"),
        ("One dominant weight", [100, 1, 1], "Heavily biased"),
        ("Large weights", [1000000, 1], "Handle large numbers"),
        ("Minimum weights", [1, 1], "Handle small numbers"),
    ]
    
    for case_name, weights, expected in edge_cases:
        print(f"{case_name}: {weights} -> {expected}")


if __name__ == "__main__":
    demonstrate_algorithm()
    print("\n")
    analyze_approaches()
    print("\n")
    edge_cases_analysis()
    print("\n")
    test_solutions()


"""
INTERVIEW STRATEGY AND KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - Need to pick index i with probability w[i] / sum(w)
   - This is weighted random sampling problem
   - Multiple calls to pickIndex() expected

2. KEY INSIGHT:
   - Convert weighted sampling to uniform sampling using cumulative sums
   - Think of it as placing weights on a number line and picking a random point
   - Use binary search to find which "bucket" the random point falls into

3. APPROACH PROGRESSION:

   Step 1: Linear Search - O(n) per pick
   - Build cumulative sums
   - Generate random number, linear search for bucket
   - Good for understanding the problem
   
   Step 2: Binary Search - O(log n) per pick
   - Same cumulative sum idea
   - Use binary search instead of linear search
   - This is the optimal solution for most cases
   
   Step 3: Alias Method - O(1) per pick
   - Advanced algorithm with O(n) preprocessing
   - Shows knowledge of specialized algorithms

4. IMPLEMENTATION DETAILS:
   
   Cumulative Sum Array:
   - cumsum[i] = w[0] + w[1] + ... + w[i]
   - Total weight = cumsum[-1]
   
   Random Number Generation:
   - Generate in [0, total_weight) or [1, total_weight]
   - Be careful with inclusive/exclusive bounds
   
   Binary Search:
   - Looking for first cumsum > target (or >= target + 1)
   - Use bisect_left with appropriate target adjustment

5. BINARY SEARCH TEMPLATE:
   - Two variations possible:
     1. Generate target in [0, total_weight), find first cumsum > target
     2. Generate target in [1, total_weight], find first cumsum >= target
   
6. COMMON MISTAKES:
   - Off-by-one errors in random number generation
   - Wrong binary search bounds
   - Not handling single element case
   - Floating point precision issues

7. FOLLOW-UP QUESTIONS:
   - "What if weights can be updated?" → Need to rebuild cumulative sums
   - "What if we need O(1) picking?" → Alias method
   - "What about very large weights?" → Handle integer overflow
   - "Memory optimization?" → Can't do better than O(n)

8. EDGE CASES:
   - Single element (always return 0)
   - All weights equal (uniform distribution)
   - One very large weight (heavily biased)
   - Very large or very small weights

9. VARIATIONS:
   - Weighted random sampling without replacement
   - Reservoir sampling
   - Online weight updates
   - Multiple picks at once

10. REAL-WORLD APPLICATIONS:
    - Load balancing with server weights
    - A/B testing with different sample sizes
    - Monte Carlo simulations
    - Genetic algorithms (selection)

RECOMMENDED INTERVIEW FLOW:
1. Clarify problem (weighted random sampling)
2. Think about converting to uniform sampling
3. Explain cumulative sum approach with example
4. Start with linear search for clarity
5. Optimize with binary search
6. Code the solution cleanly
7. Handle edge cases
8. Discuss time/space complexity
9. Mention alias method if time permits

KEY INSIGHTS TO MENTION:
- "This is about converting weighted sampling to uniform sampling"
- "Cumulative sums create buckets of different sizes"
- "Binary search finds the right bucket efficiently"
- "Need to be careful with random number bounds"

This problem excellently tests:
- Understanding of probability and sampling
- Binary search implementation
- Cumulative sum techniques
- Edge case handling
- Algorithm optimization thinking
"""
