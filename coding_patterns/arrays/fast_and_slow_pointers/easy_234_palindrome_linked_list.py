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
