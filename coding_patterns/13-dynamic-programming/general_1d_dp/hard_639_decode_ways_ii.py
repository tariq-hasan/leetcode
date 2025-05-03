class Solution:
    def numDecodings(self, s: str) -> int:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if s[0] == '0':
            return 0

        mod = (10 ** 9) + 7
        i = j = 1
        for k in range(len(s)):
            one_digit_variations = 9 if s[k] == '*' else 1 if s[k] != '0' else 0

            two_digit_variations = 0 if k == 0 \
                else 15 if s[k - 1: k + 1] == '**' \
                else 2 if s[k - 1] == '*' and 0 <= int(s[k]) <= 6 \
                else 1 if s[k - 1] == '*' and 7 <= int(s[k]) <= 9 \
                else 9 if int(s[k - 1]) == 1 and s[k] == '*' \
                else 6 if int(s[k - 1]) == 2 and s[k] == '*' \
                else 0 if (int(s[k - 1]) == 0 or 3 <= int(s[k - 1]) <= 9) and s[k] == '*' \
                else 1 if 10 <= int(s[k - 1: k + 1]) <= 26 \
                else 0
            i, j = j, ((i * two_digit_variations) + (j * one_digit_variations)) % mod
        return j
