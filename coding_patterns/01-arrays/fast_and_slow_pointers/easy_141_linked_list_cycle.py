from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        seen = set()
        current = head
        while current is not None:
            if current in seen:
                return True
            seen.add(current)
            current = current.next
        return False


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        slow = fast = head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
            if slow == fast:
                return True
        return False
