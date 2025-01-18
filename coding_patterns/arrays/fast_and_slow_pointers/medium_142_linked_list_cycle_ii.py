from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        seen = set()
        node = head
        while node:
            if node in seen:
                return node
            else:
                seen.add(node)
                node = node.next
        return node


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        slow = fast = head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
            if slow == fast:
                break

        if not fast or not fast.next:
            return None

        fast = head
        while slow != fast:
            slow, fast = slow.next, fast.next

        return slow
