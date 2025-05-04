class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        """
        Find the letter that was added to string t which was formed by randomly shuffling string s
        and adding one more letter.

        This solution uses a frequency counter approach:
        1. Count the frequency of each character in s
        2. Decrement the frequency for each character in t
        3. Return the character with frequency of -1

        Args:
            s: The original string
            t: The modified string with one extra character

        Returns:
            The character that was added to string t

        Time Complexity: O(n) - We iterate through both strings once
        Space Complexity: O(1) - We use at most 26 entries in the hash map (for lowercase letters)
        """
        # Create a frequency counter for characters in s
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        # Check each character in t
        for char in t:
            # If char isn't in s or its frequency is already 0, it's the added character
            if char not in freq or freq[char] == 0:
                return char
            # Otherwise, decrement its frequency
            freq[char] -= 1

        # This should never happen if the input is valid
        return ""


class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        """
        Find the letter that was added to string t which was formed by randomly shuffling string s
        and adding one more letter.

        This solution uses the XOR operation:
        1. XOR all characters in both strings
        2. Since each character in s has a matching character in t (which XOR to 0)
        3. The only remaining value will be the added character

        Args:
            s: The original string
            t: The modified string with one extra character

        Returns:
            The character that was added to string t

        Time Complexity: O(n) - We iterate through both strings once
        Space Complexity: O(1) - We use only one variable regardless of input size
        """
        # Initialize result to 0
        result = 0

        # XOR all characters from both strings
        for char in s + t:
            # Convert char to ASCII and XOR with result
            result ^= ord(char)

        # Convert the final result back to a character
        return chr(result)
