"""
LeetCode 1353: Maximum Number of Events That Can Be Attended

Problem Statement:
You are given an array of events where events[i] = [startDayi, endDayi]. Every event i starts at 
startDayi and ends at endDayi.

You can attend an event i at any day d where startTime <= d <= endTime. You can only attend one 
event per day.

Return the maximum number of events you can attend.

Example 1:
Input: events = [[1,2],[2,3],[3,4]]
Output: 3
Explanation: You can attend all three events.
One way to attend them is:
- Attend first event on day 1.
- Attend second event on day 2.
- Attend third event on day 3.

Example 2:
Input: events = [[1,2],[2,3],[3,4],[1,2]]
Output: 4

Example 3:
Input: events = [[1,4],[4,4],[2,2],[3,4],[1,1]]
Output: 4
Explanation: The maximum number of events you can attend is 4.
Here is a feasible schedule:
- Attend event 3 on day 2.
- Attend event 0 on day 3.
- Attend event 4 on day 1.
- Attend event 1 on day 4.
It can be shown that you can't attend event 2 since day 2 is already taken by event 3.
"""

import heapq
from collections import defaultdict

def maxEvents(events):
    """
    Optimal Solution: Greedy Algorithm with Min-Heap
    
    Key Insights:
    1. Process days in chronological order (1, 2, 3, ...)
    2. For each day, consider all events that can start on that day
    3. Among available events, prioritize those that end earliest (greedy choice)
    4. Remove expired events from consideration
    
    Why this works:
    - We want to attend as many events as possible
    - If we have multiple choices on a day, pick the event ending soonest
    - This leaves more flexibility for future days
    
    Algorithm:
    1. Sort events by start day
    2. Use min-heap to track available events (prioritized by end day)
    3. For each day from 1 to max_end_day:
       - Add all events starting on this day to heap
       - Remove expired events from heap
       - If heap not empty, attend event with earliest end day
    
    Time Complexity: O(N log N + D log N) where N = events, D = max end day
    Space Complexity: O(N)
    """
    
    if not events:
        return 0
    
    # Sort events by start day
    events.sort()
    
    # Find the last day we need to consider
    max_day = max(event[1] for event in events)
    
    # Min-heap to store end days of available events
    available_events = []
    event_idx = 0
    attended_events = 0
    
    # Process each day from 1 to max_day
    for day in range(1, max_day + 1):
        # Add all events that start on this day to our available events
        while event_idx < len(events) and events[event_idx][0] <= day:
            # Add end day to min-heap
            heapq.heappush(available_events, events[event_idx][1])
            event_idx += 1
        
        # Remove all expired events (events that ended before today)
        while available_events and available_events[0] < day:
            heapq.heappop(available_events)
        
        # If we have available events, attend the one ending soonest
        if available_events:
            heapq.heappop(available_events)
            attended_events += 1
    
    return attended_events


def maxEvents_alternative_grouping(events):
    """
    Alternative approach: Group events by start day
    
    Sometimes easier to understand the logic this way
    """
    if not events:
        return 0
    
    # Group events by their start day
    events_by_start = defaultdict(list)
    max_day = 0
    
    for start, end in events:
        events_by_start[start].append(end)
        max_day = max(max_day, end)
    
    # Sort end days within each start day group
    for start_day in events_by_start:
        events_by_start[start_day].sort()
    
    available_events = []  # Min-heap of end days
    attended_events = 0
    
    for day in range(1, max_day + 1):
        # Add all events starting today
        for end_day in events_by_start[day]:
            heapq.heappush(available_events, end_day)
        
        # Remove expired events
        while available_events and available_events[0] < day:
            heapq.heappop(available_events)
        
        # Attend event ending soonest
        if available_events:
            heapq.heappop(available_events)
            attended_events += 1
    
    return attended_events


def maxEvents_brute_force(events):
    """
    Brute Force Solution for comparison (Time Limit Exceeded for large inputs)
    
    Try all possible ways to attend events using backtracking
    
    Time Complexity: O(2^N) - exponential
    Space Complexity: O(N) - recursion depth
    """
    def backtrack(event_idx, occupied_days):
        if event_idx == len(events):
            return 0
        
        max_attended = 0
        start, end = events[event_idx]
        
        # Try attending this event on each possible day
        for day in range(start, end + 1):
            if day not in occupied_days:
                occupied_days.add(day)
                attended = 1 + backtrack(event_idx + 1, occupied_days)
                max_attended = max(max_attended, attended)
                occupied_days.remove(day)
        
        # Try not attending this event
        max_attended = max(max_attended, backtrack(event_idx + 1, occupied_days))
        
        return max_attended
    
    return backtrack(0, set())


def maxEvents_dp_approach(events):
    """
    Dynamic Programming approach (less efficient than greedy for this problem)
    
    State: dp[i][day] = max events we can attend from events[i:] starting from day
    
    Time Complexity: O(N * D) where D is max end day
    Space Complexity: O(N * D)
    """
    if not events:
        return 0
    
    events.sort()
    max_day = max(event[1] for event in events)
    
    # Memoization
    memo = {}
    
    def dp(event_idx, current_day):
        if event_idx == len(events) or current_day > max_day:
            return 0
        
        if (event_idx, current_day) in memo:
            return memo[(event_idx, current_day)]
        
        start, end = events[event_idx]
        
        # If current event has already ended, skip it
        if end < current_day:
            result = dp(event_idx + 1, current_day)
        else:
            # Option 1: Skip this event
            skip = dp(event_idx + 1, current_day)
            
            # Option 2: Attend this event (if possible)
            attend = 0
            if start <= current_day <= end:
                attend = 1 + dp(event_idx + 1, current_day + 1)
            elif start > current_day:
                # Fast forward to when this event starts
                attend = 1 + dp(event_idx + 1, start + 1)
            
            result = max(skip, attend)
        
        memo[(event_idx, current_day)] = result
        return result
    
    return dp(0, 1)


def demonstrate_algorithm():
    """
    Step-by-step demonstration of the greedy algorithm
    """
    events = [[1,4],[4,4],[2,2],[3,4],[1,1]]
    print("Demonstrating Greedy Algorithm:")
    print("=" * 50)
    print(f"Input: {events}")
    print()
    
    # Sort events by start day
    events.sort()
    print(f"After sorting by start day: {events}")
    print()
    
    max_day = max(event[1] for event in events)
    available_events = []
    event_idx = 0
    attended_events = 0
    schedule = {}
    
    print("Processing each day:")
    for day in range(1, max_day + 1):
        print(f"\nDay {day}:")
        
        # Add events starting today
        events_added = []
        while event_idx < len(events) and events[event_idx][0] <= day:
            heapq.heappush(available_events, events[event_idx][1])
            events_added.append(events[event_idx])
            event_idx += 1
        
        if events_added:
            print(f"  Added events: {events_added}")
        
        # Remove expired events
        expired = []
        while available_events and available_events[0] < day:
            expired.append(heapq.heappop(available_events))
        
        if expired:
            print(f"  Removed expired events ending on days: {expired}")
        
        print(f"  Available events (by end day): {sorted(available_events)}")
        
        # Attend event ending soonest
        if available_events:
            earliest_end = heapq.heappop(available_events)
            schedule[day] = earliest_end
            attended_events += 1
            print(f"  ✓ Attended event ending on day {earliest_end}")
        else:
            print(f"  ✗ No events available")
    
    print(f"\nFinal Schedule: {schedule}")
    print(f"Total events attended: {attended_events}")


# Test cases
def test_solution():
    """Test all solutions with provided examples and edge cases"""
    
    test_cases = [
        ([[1,2],[2,3],[3,4]], 3),
        ([[1,2],[2,3],[3,4],[1,2]], 4),
        ([[1,4],[4,4],[2,2],[3,4],[1,1]], 4),
        ([[1,1],[1,2],[1,3],[1,4],[1,5]], 5),  # All start same day
        ([[1,5],[1,5],[1,5],[2,3],[2,3]], 3),  # Multiple identical events
        ([[1,1]], 1),  # Single event
        ([], 0),  # Empty input
        ([[1,100000]], 1)  # Large range
    ]
    
    solutions = [
        ("Greedy with Min-Heap", maxEvents),
        ("Alternative Grouping", maxEvents_alternative_grouping),
        ("Dynamic Programming", maxEvents_dp_approach)
    ]
    
    for sol_name, solution_func in solutions:
        print(f"\nTesting {sol_name}:")
        print("=" * 50)
        
        for i, (events, expected) in enumerate(test_cases, 1):
            try:
                result = solution_func(events.copy())  # Copy to avoid modification
                status = "✓ PASS" if result == expected else "✗ FAIL"
                
                print(f"Test Case {i}: {status}")
                print(f"  Input: {events}")
                print(f"  Expected: {expected}")
                print(f"  Got:      {result}")
            except Exception as e:
                print(f"Test Case {i}: ✗ ERROR - {str(e)}")
        print()


# Run tests and demonstration
if __name__ == "__main__":
    test_solution()
    print("\n" + "="*70 + "\n")
    demonstrate_algorithm()


"""
INTERVIEW DISCUSSION POINTS:

1. PROBLEM CLASSIFICATION:
   - Greedy algorithm with heap optimization
   - Event scheduling problem
   - Similar to interval scheduling, but with flexibility

2. KEY INSIGHTS:
   - Process days chronologically (can't go back in time)
   - Among available events, always pick the one ending soonest
   - This maximizes future flexibility
   - Use heap to efficiently get event with earliest end time

3. WHY GREEDY WORKS:
   - We want to maximize number of events attended
   - If multiple events are available on a day, picking the one ending soonest 
     leaves more options for future days
   - This is the "exchange argument" - any optimal solution can be modified 
     to use our greedy choices without losing optimality

4. COMPLEXITY ANALYSIS:
   - Time: O(N log N + D log N) where N=events, D=max end day
   - Space: O(N) for the heap
   - The D factor comes from iterating through days, but in practice D ≤ N*max_duration

5. EDGE CASES:
   - No events
   - Single event
   - All events on same day
   - Events with very large time ranges
   - Multiple identical events

6. ALTERNATIVE APPROACHES:
   - Brute force: Try all combinations - O(2^N)
   - DP: Process events with memoization - O(N*D)
   - Greedy is optimal for this specific problem

7. FOLLOW-UP QUESTIONS:
   - "What if you could attend multiple events per day?" (Different problem entirely)
   - "What if events had different values/priorities?" (Weighted interval scheduling)
   - "What if you had constraints on consecutive days?" (Add state tracking)
   - "How would you handle millions of events?" (Consider approximation algorithms)

8. IMPLEMENTATION DETAILS:
   - Sort events by start time for efficient processing
   - Use min-heap to maintain available events sorted by end time
   - Clean up expired events to maintain heap efficiency
   - Process days sequentially to ensure optimal scheduling

9. COMMON MISTAKES:
   - Not handling expired events properly
   - Sorting by wrong criteria (should sort by start time)
   - Not using heap for efficient selection of earliest-ending event
   - Off-by-one errors in day ranges
"""
