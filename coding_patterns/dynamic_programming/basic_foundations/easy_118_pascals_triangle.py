from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        Generate Pascal's Triangle up to the specified number of rows.
        
        Pascal's Triangle is a triangular array where each number is the sum
        of the two numbers directly above it.
        
        Args:
            numRows: The number of rows to generate
            
        Returns:
            A list of lists representing Pascal's Triangle
            
        Time Complexity: O(numRows²) - We process each element in the triangle once
        Space Complexity: O(1) - We are not using additional data structures beyond the required output.
        """
        # Initialize the result list
        triangle = []
        
        for row_num in range(numRows):
            # Create new row with 1's at the edges
            current_row = [1] * (row_num + 1)
            
            # Fill in the middle elements using the previous row
            for j in range(1, row_num):
                current_row[j] = triangle[row_num - 1][j - 1] + triangle[row_num - 1][j]
                
            triangle.append(current_row)
            
        return triangle
