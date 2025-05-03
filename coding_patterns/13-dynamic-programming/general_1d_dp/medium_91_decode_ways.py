class Solution:
    def numDecodings(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if s[0] == "0":
            return 0

        i = j = 1
        for k in range(len(s)):
            valid_one_digit = 1 <= int(s[k]) <= 9
            valid_two_digits = k > 0 and 10 <= int(s[k - 1 : k + 1]) <= 26
            i, j = j, (i if valid_two_digits else 0) + (j if valid_one_digit else 0) 
        return j
