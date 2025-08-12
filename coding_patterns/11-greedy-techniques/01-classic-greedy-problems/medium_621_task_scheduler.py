"""
LeetCode 621. Task Scheduler

Problem: You are given an array of CPU tasks, each represented by letters A-Z, 
and a cooling time, n. Each cycle, you can complete one task or sit idle. 
Tasks of the same type must be separated by at least n intervals.
Return the minimum number of intervals required to complete all tasks.

Key Insights:
1. The most frequent task determines the minimum time needed
2. We need to arrange tasks to minimize idle time
3. Greedy approach: always schedule the task with highest remaining frequency
4. Mathematical formula exists based on max frequency and count of max frequency tasks

Time Complexity: O(m log k) where m = total tasks, k = unique tasks (≤ 26)
Space Complexity: O(k) for frequency counting and heap
"""

import heapq
from collections import Counter, deque

# Approach 1: Greedy with Max-Heap (Most Intuitive)
def leastInterval_v1(tasks, n):
    """
    Greedy simulation approach using max-heap
    Always schedule the task with highest remaining count
    """
    if n == 0:
        return len(tasks)
    
    # Count frequency of each task
    freq = Counter(tasks)
    
    # Use max-heap (negate values for min-heap to work as max-heap)
    max_heap = [-count for count in freq.values()]
    heapq.heapify(max_heap)
    
    time = 0
    
    while max_heap:
        cycle = []
        
        # Try to schedule n+1 tasks in current cycle
        for _ in range(n + 1):
            if max_heap:
                # Schedule task with max frequency
                count = heapq.heappop(max_heap)
                cycle.append(count)
        
        # Put back tasks that still have remaining executions
        for count in cycle:
            if count < -1:  # Still has remaining executions
                heapq.heappush(max_heap, count + 1)
        
        # Add time for this cycle
        if max_heap:
            time += n + 1  # Full cycle needed
        else:
            time += len(cycle)  # Last cycle, only count actual tasks
    
    return time

# Approach 2: Mathematical Formula (Most Efficient)
def leastInterval_v2(tasks, n):
    """
    Mathematical approach - calculate based on max frequency
    Key insight: result is determined by the most frequent task(s)
    """
    if n == 0:
        return len(tasks)
    
    # Count frequencies
    freq = Counter(tasks)
    max_freq = max(freq.values())
    
    # Count how many tasks have the maximum frequency
    max_count = sum(1 for f in freq.values() if f == max_freq)
    
    # Calculate minimum intervals needed
    # Pattern: (max_freq - 1) * (n + 1) + max_count
    # This represents: full cycles + final tasks
    intervals = (max_freq - 1) * (n + 1) + max_count
    
    # Can't be less than total number of tasks
    return max(intervals, len(tasks))

# Approach 3: Detailed Simulation (For Understanding)
def leastInterval_v3(tasks, n):
    """
    Detailed simulation showing the actual scheduling
    Useful for explaining the algorithm step by step
    """
    if n == 0:
        return len(tasks)
    
    freq = Counter(tasks)
    time = 0
    
    while freq:
        # Schedule tasks for current cycle
        scheduled = []
        
        # Find up to n+1 tasks to schedule (to satisfy cooling period)
        available_tasks = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
        
        for i in range(min(n + 1, len(available_tasks))):
            task = available_tasks[i]
            scheduled.append(task)
            freq[task] -= 1
            if freq[task] == 0:
                del freq[task]
        
        # Calculate time for this cycle
        if freq:  # More tasks remaining
            time += n + 1  # Full cycle with possible idle time
        else:  # Last cycle
            time += len(scheduled)  # Only count actual tasks
    
    return time

# Approach 4: Queue-based Simulation (Alternative Implementation)
def leastInterval_v4(tasks, n):
    """
    Using queue to track tasks in cooling period
    More explicit about the cooling mechanism
    """
    if n == 0:
        return len(tasks)
    
    freq = Counter(tasks)
    max_heap = [-count for count in freq.values()]
    heapq.heapify(max_heap)
    
    queue = deque()  # (remaining_count, available_time)
    time = 0
    
    while max_heap or queue:
        time += 1
        
        # Add tasks back from cooling period
        if queue and queue[0][1] == time:
            count, _ = queue.popleft()
            heapq.heappush(max_heap, count)
        
        # Execute a task if available
        if max_heap:
            count = heapq.heappop(max_heap)
            if count < -1:  # Task still has remaining executions
                queue.append((count + 1, time + n))
    
    return time

def explain_mathematical_approach():
    """
    Detailed explanation of the mathematical formula
    """
    print("=== Mathematical Formula Explanation ===")
    print()
    print("Key insight: The answer depends on the most frequent task(s)")
    print()
    print("Pattern Analysis:")
    print("- Most frequent task appears max_freq times")
    print("- Between each execution, we need n cooling intervals")
    print("- This creates (max_freq - 1) full cycles of length (n + 1)")
    print("- Plus max_count tasks in the final execution")
    print()
    print("Formula: (max_freq - 1) * (n + 1) + max_count")
    print()
    print("Example: tasks = ['A','A','A','B','B','B'], n = 2")
    print("- max_freq = 3 (both A and B appear 3 times)")
    print("- max_count = 2 (both A and B have max frequency)")
    print("- Formula: (3-1) * (2+1) + 2 = 2 * 3 + 2 = 8")
    print("- Schedule: A B _ A B _ A B (8 intervals)")
    print()
    print("But we also need: max(formula_result, len(tasks))")
    print("Why? If we have many different tasks, we might not need idle time")

def demonstrate_scheduling(tasks, n):
    """
    Show actual task scheduling for interview explanation
    """
    print(f"\n=== Demonstrating Scheduling: tasks={tasks}, n={n} ===")
    
    if n == 0:
        print("No cooling needed, answer is", len(tasks))
        return len(tasks)
    
    freq = Counter(tasks)
    original_freq = freq.copy()
    print(f"Task frequencies: {dict(freq)}")
    
    schedule = []
    time = 0
    
    while freq:
        print(f"\nCycle starting at time {time}:")
        cycle_tasks = []
        
        # Schedule up to n+1 tasks
        available = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
        
        for i in range(min(n + 1, len(available))):
            task = available[i]
            cycle_tasks.append(task)
            freq[task] -= 1
            if freq[task] == 0:
                del freq[task]
        
        # Fill remaining slots with idle if needed
        while len(cycle_tasks) < n + 1 and freq:
            cycle_tasks.append('idle')
        
        # If this is the last cycle, don't add unnecessary idle
        if not freq:
            cycle_tasks = [t for t in cycle_tasks if t != 'idle']
        
        schedule.extend(cycle_tasks)
        time += len(cycle_tasks)
        
        print(f"Scheduled: {cycle_tasks}")
        print(f"Remaining frequencies: {dict(freq) if freq else 'None'}")
    
    print(f"\nFinal schedule: {schedule}")
    print(f"Total time: {len(schedule)}")
    
    return len(schedule)

def test_task_scheduler():
    """
    Test various scenarios to validate all approaches
    """
    test_cases = [
        (["A","A","A","B","B","B"], 2, 8),
        (["A","A","A","B","B","B"], 0, 6),
        (["A","A","A","A","A","A","B","C","D","E","F","G"], 2, 16),
        (["A","B","C","D","E","F"], 2, 6),
        (["A"], 2, 1),
        (["A","A"], 1, 3),
        (["A","B","A"], 2, 4)
    ]
    
    approaches = [
        ("Greedy Max-Heap", leastInterval_v1),
        ("Mathematical Formula", leastInterval_v2),
        ("Detailed Simulation", leastInterval_v3),
        ("Queue-based", leastInterval_v4)
    ]
    
    for i, (tasks, n, expected) in enumerate(test_cases):
        print(f"\n=== Test Case {i+1}: tasks={tasks}, n={n} ===")
        
        results = []
        for name, func in approaches:
            result = func(tasks[:], n)  # Pass copy to avoid modifications
            results.append(result)
            print(f"{name}: {result}")
        
        # Verify all approaches agree
        assert all(r == results[0] for r in results), f"Results disagree: {results}"
        
        # Verify against expected result
        if expected is not None:
            assert results[0] == expected, f"Expected {expected}, got {results[0]}"
        
        # Show detailed scheduling for small examples
        if len(tasks) <= 12:
            demonstrate_scheduling(tasks, n)

def analyze_complexity():
    """
    Detailed complexity analysis for different approaches
    """
    print("\n=== Complexity Analysis ===")
    print()
    print("APPROACH 1 - Greedy Max-Heap:")
    print("- Time: O(m log k) where m = total tasks, k = unique tasks")
    print("- Space: O(k) for heap and frequency counting")
    print("- Best for understanding the algorithm")
    print()
    print("APPROACH 2 - Mathematical Formula:")
    print("- Time: O(m) for counting frequencies")
    print("- Space: O(k) for frequency counting")
    print("- Most efficient, direct calculation")
    print()
    print("APPROACH 3 - Detailed Simulation:")
    print("- Time: O(m * k) in worst case")
    print("- Space: O(k) for frequency counting")
    print("- Good for explanation but less efficient")
    print()
    print("APPROACH 4 - Queue-based:")
    print("- Time: O(m log k) for heap operations")
    print("- Space: O(k) for heap and queue")
    print("- More explicit about cooling mechanism")
    print()
    print("RECOMMENDATION: Use mathematical approach for optimal efficiency")
    print("Use max-heap approach to demonstrate understanding")

if __name__ == "__main__":
    print("=== Task Scheduler Solutions ===")
    
    # Test all approaches
    test_task_scheduler()
    
    # Explain the mathematical insight
    explain_mathematical_approach()
    
    # Complexity analysis
    analyze_complexity()

"""
Critical Interview Discussion Points:

1. **Problem Understanding**:
   - Tasks of same type need n intervals of cooling time
   - Can choose to be idle if no task is available
   - Goal: minimize total time to complete all tasks
   - Greedy scheduling: always pick most frequent remaining task

2. **Key Insights**:
   - Most frequent task(s) determine the minimum time
   - We want to minimize idle time by interleaving different tasks
   - Mathematical pattern emerges from optimal scheduling

3. **Two Main Approaches**:
   - **Simulation**: Use max-heap to greedily schedule tasks
   - **Mathematical**: Calculate directly using max frequency formula

4. **Mathematical Formula Derivation**:
   ```
   result = (max_freq - 1) * (n + 1) + max_count
   but at least len(tasks)
   ```
   - (max_freq - 1): number of full cycles needed
   - (n + 1): length of each cycle (1 task + n cooling)
   - max_count: number of tasks in final execution

5. **Why Max-Heap Works**:
   - Always schedule task with highest remaining count
   - Minimizes idle time by balancing task frequencies
   - Natural greedy choice for load balancing

6. **Edge Cases**:
   - n = 0: no cooling needed, answer is len(tasks)
   - Single task type: answer is len(tasks) + (len(tasks)-1) * n
   - Many different tasks: might not need any idle time

7. **Complexity Trade-offs**:
   - Simulation: O(m log k) time, easier to understand
   - Mathematical: O(m) time, requires insight into pattern
   - Both use O(k) space for frequency counting

8. **Interview Strategy**:
   - Start with simulation approach to show understanding
   - Mention mathematical optimization for efficiency
   - Walk through examples to demonstrate both methods
   - Discuss trade-offs between clarity and efficiency

9. **Follow-up Questions**:
   - What if tasks have different execution times?
   - How to handle dynamic task arrival?
   - What if cooling times vary by task type?
   - Can you schedule to minimize maximum completion time?

10. **Real-world Applications**:
    - CPU task scheduling with thermal constraints
    - Job scheduling in distributed systems
    - Resource allocation with cooldown periods
    - Load balancing with recovery time

11. **Common Mistakes**:
    - Not handling the case where no idle time is needed
    - Incorrect calculation of cycles and remainders
    - Off-by-one errors in the mathematical formula
    - Not considering edge cases (n=0, single task type)
"""
