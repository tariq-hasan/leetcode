# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        self.first = head

        def check_palindrome(last):
            if last:
                if not check_palindrome(last.next):
                    return False
                if self.first.val != last.val:
                    return False
                self.first = self.first.next
            return True

        return check_palindrome(head)


class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        def end_of_first_half(head: ListNode) -> ListNode:
            slow = fast = head
            while fast.next and fast.next.next:
                slow = slow.next
                fast = fast.next.next
            return slow

        def reverse_list(head: ListNode) -> ListNode:
            prev, curr = None, head
            while curr:
                next_node, curr.next = curr.next, prev
                prev, curr = curr, next_node
            return prev

        first_half_end = end_of_first_half(head)
        second_half_start = reverse_list(first_half_end.next)

        result = True
        first, second = head, second_half_start
        while result and second:
            if first.val != second.val:
                result = False
            first, second = first.next, second.next

        first_half_end.next = reverse_list(second_half_start)
        return result
