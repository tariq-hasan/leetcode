from typing import List


class Solution:
    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        """
        The time complexity is O(n log n).
        The space complexity is O(1).
        """
        boxTypes = sorted(boxTypes, key=lambda x: x[1], reverse=True)
        num_units = 0
        for box_type in boxTypes:
            box_count = min(truckSize, box_type[0])
            num_units = num_units + (box_count * box_type[1])
            truckSize = truckSize - box_count
            if truckSize == 0:
                break
        return num_units
