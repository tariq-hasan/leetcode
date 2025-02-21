class Solution:
    def smallestNumber(self, pattern: str) -> str:
        """
        The time complexity is O(n).
        The space complexity is O(n).
        """
        def build_sequence(current_index, current_count, pattern):
            if current_index != len(pattern):
                if pattern[current_index] == "I":
                    build_sequence(current_index + 1, current_index + 1, pattern)
                else:
                    current_count = build_sequence(current_index + 1, current_count, pattern)
            out.append(str(current_count + 1))
            return current_count + 1

        out = []
        build_sequence(0, 0, pattern)
        return "".join(out[::-1])
