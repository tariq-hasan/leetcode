from typing import List


class Solution:
    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        """
        The time complexity is O(1).
        The space complexity is O(1).
        """
        out = []
        for h in range(12):
            for m in range(60):
                if bin(h).count('1') + bin(m).count('1') == turnedOn:
                    out.append(f"{h}:{m:02d}")
        return out
