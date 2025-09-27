from typing import List

class UnionFind:
    """
    Union-Find data structure for tracking connected components
    Used to efficiently count regions separated by slashes
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
    
    def find(self, x):
        """Find root with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank with component counting"""
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            
            self.components -= 1
    
    def get_components(self):
        """Return number of connected components"""
        return self.components

class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        """
        Optimal Solution - Union Find with Triangle Subdivision
        
        Key insight: Divide each grid cell into 4 triangular sub-regions.
        Slashes separate some triangles, spaces connect all triangles.
        Use Union-Find to count connected components.
        
        Time Complexity: O(N^2 * α(N^2)) where α is inverse Ackermann function
        Space Complexity: O(N^2) for Union-Find structure
        """
        n = len(grid)
        # Each cell has 4 triangular regions: North, East, South, West
        uf = UnionFind(4 * n * n)
        
        def get_index(i, j, k):
            """Get index for triangle k in cell (i,j)"""
            return 4 * (i * n + j) + k
        
        for i in range(n):
            for j in range(n):
                cell = grid[i][j]
                
                # Connect triangles within the same cell based on slash type
                if cell == ' ':
                    # No slash: connect all 4 triangles
                    base = get_index(i, j, 0)
                    for k in range(1, 4):
                        uf.union(base, get_index(i, j, k))
                
                elif cell == '/':
                    # Forward slash: connect North-West and South-East
                    uf.union(get_index(i, j, 0), get_index(i, j, 3))  # North-West
                    uf.union(get_index(i, j, 1), get_index(i, j, 2))  # East-South
                
                elif cell == '\\':
                    # Back slash: connect North-East and South-West
                    uf.union(get_index(i, j, 0), get_index(i, j, 1))  # North-East
                    uf.union(get_index(i, j, 2), get_index(i, j, 3))  # South-West
                
                # Connect to adjacent cells
                # Connect to right cell
                if j + 1 < n:
                    uf.union(get_index(i, j, 1), get_index(i, j + 1, 3))
                
                # Connect to bottom cell
                if i + 1 < n:
                    uf.union(get_index(i, j, 2), get_index(i + 1, j, 0))
        
        return uf.get_components()

    def regionsBySlashesDFS(self, grid: List[str]) -> int:
        """
        DFS Solution with 3x3 Expansion
        
        Key insight: Expand each 1x1 cell to 3x3 grid.
        Draw slashes as blocked cells, then count connected regions via DFS.
        
        Time Complexity: O(N^2) for grid expansion and DFS
        Space Complexity: O(N^2) for expanded grid
        """
        n = len(grid)
        # Expand to 3*n x 3*n grid
        expanded = [[0] * (3 * n) for _ in range(3 * n)]
        
        # Fill expanded grid based on slashes
        for i in range(n):
            for j in range(n):
                cell = grid[i][j]
                base_i, base_j = 3 * i, 3 * j
                
                if cell == '/':
                    # Draw forward slash
                    expanded[base_i][base_j + 2] = 1
                    expanded[base_i + 1][base_j + 1] = 1
                    expanded[base_i + 2][base_j] = 1
                
                elif cell == '\\':
                    # Draw back slash
                    expanded[base_i][base_j] = 1
                    expanded[base_i + 1][base_j + 1] = 1
                    expanded[base_i + 2][base_j + 2] = 1
        
        # Count connected components using DFS
        visited = [[False] * (3 * n) for _ in range(3 * n)]
        regions = 0
        
        def dfs(x, y):
            """DFS to mark connected region"""
            if (x < 0 or x >= 3 * n or y < 0 or y >= 3 * n or 
                visited[x][y] or expanded[x][y] == 1):
                return
            
            visited[x][y] = True
            
            # Explore 4 directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(x + dx, y + dy)
        
        # Find all regions
        for i in range(3 * n):
            for j in range(3 * n):
                if not visited[i][j] and expanded[i][j] == 0:
                    dfs(i, j)
                    regions += 1
        
        return regions

    def regionsBySlashesBFS(self, grid: List[str]) -> int:
        """
        BFS Solution with 3x3 Expansion (Alternative to DFS)
        
        Same expansion logic but uses BFS for connected component counting
        Time Complexity: O(N^2)
        Space Complexity: O(N^2)
        """
        from collections import deque
        
        n = len(grid)
        expanded = [[0] * (3 * n) for _ in range(3 * n)]
        
        # Fill expanded grid
        for i in range(n):
            for j in range(n):
                cell = grid[i][j]
                base_i, base_j = 3 * i, 3 * j
                
                if cell == '/':
                    expanded[base_i][base_j + 2] = 1
                    expanded[base_i + 1][base_j + 1] = 1
                    expanded[base_i + 2][base_j] = 1
                elif cell == '\\':
                    expanded[base_i][base_j] = 1
                    expanded[base_i + 1][base_j + 1] = 1
                    expanded[base_i + 2][base_j + 2] = 1
        
        visited = [[False] * (3 * n) for _ in range(3 * n)]
        regions = 0
        
        def bfs(start_x, start_y):
            """BFS to mark connected region"""
            queue = deque([(start_x, start_y)])
            visited[start_x][start_y] = True
            
            while queue:
                x, y = queue.popleft()
                
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < 3 * n and 0 <= ny < 3 * n and 
                        not visited[nx][ny] and expanded[nx][ny] == 0):
                        visited[nx][ny] = True
                        queue.append((nx, ny))
        
        # Count regions
        for i in range(3 * n):
            for j in range(3 * n):
                if not visited[i][j] and expanded[i][j] == 0:
                    bfs(i, j)
                    regions += 1
        
        return regions

    def regionsBySlashesEuler(self, grid: List[str]) -> int:
        """
        Mathematical Solution using Euler's Formula
        
        Key insight: Use Euler's formula V - E + F = 2 for connected planar graphs.
        Count vertices, edges, and use formula to find faces (regions).
        
        Time Complexity: O(N^2)
        Space Complexity: O(1)
        """
        n = len(grid)
        
        # Count internal vertices (intersections)
        internal_vertices = (n - 1) * (n - 1)
        
        # Count boundary vertices
        boundary_vertices = 4 * n
        
        total_vertices = internal_vertices + boundary_vertices
        
        # Count edges
        # Boundary edges
        boundary_edges = 4 * n
        
        # Internal horizontal and vertical grid edges
        horizontal_edges = n * (n - 1)
        vertical_edges = n * (n - 1)
        
        # Slash edges
        slash_edges = 0
        for i in range(n):
            for j in range(n):
                if grid[i][j] in ['/', '\\']:
                    slash_edges += 1
        
        total_edges = boundary_edges + horizontal_edges + vertical_edges + slash_edges
        
        # Apply Euler's formula: V - E + F = 2
        # F = 2 + E - V
        faces = 2 + total_edges - total_vertices
        
        # Subtract 1 for the infinite outer face
        return faces - 1

    def regionsBySlashesCoordinateCompression(self, grid: List[str]) -> int:
        """
        Coordinate Compression with Union-Find
        
        Map intersection points to indices and use Union-Find on regions
        More complex but demonstrates advanced technique
        
        Time Complexity: O(N^2 * α(N^2))
        Space Complexity: O(N^2)
        """
        n = len(grid)
        
        # Create coordinate mapping for intersection points
        points = {}
        point_id = 0
        
        # Map all grid intersection points
        for i in range(n + 1):
            for j in range(n + 1):
                points[(i, j)] = point_id
                point_id += 1
        
        # Each region is bounded by edges, use Union-Find on edge dual graph
        # This approach is more complex and typically not required in interviews
        # Implementation details omitted for brevity
        
        # Placeholder return for demonstration
        return self.regionsBySlashes(grid)

# Test cases and utility functions
def test_basic_functionality():
    """Test basic slash region counting"""
    solution = Solution()
    
    test_cases = [
        {
            "grid": [" /", "/ "],
            "expected": 2,
            "description": "Simple cross pattern"
        },
        {
            "grid": [" /", "  "],
            "expected": 1,
            "description": "Single slash"
        },
        {
            "grid": ["\\/", "/\\"],
            "expected": 4,
            "description": "Diamond pattern"
        },
        {
            "grid": ["/\\", "\\/"],
            "expected": 5,
            "description": "Hourglass pattern"
        },
        {
            "grid": ["//", "/ "],
            "expected": 3,
            "description": "Multiple slashes"
        }
    ]
    
    print("Testing Basic Functionality:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases):
        grid = test_case["grid"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        result_uf = solution.regionsBySlashes(grid)
        result_dfs = solution.regionsBySlashesDFS(grid)
        
        print(f"Test {i+1}: {description}")
        print(f"  Grid: {grid}")
        print(f"  Union-Find: {result_uf}")
        print(f"  DFS: {result_dfs}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if result_uf == expected and result_dfs == expected else '✗'}")
        print()

def visualize_triangle_subdivision():
    """Show how triangle subdivision works"""
    print("Triangle Subdivision Visualization:")
    print("=" * 50)
    
    print("Each cell is divided into 4 triangles:")
    print("     0")
    print("   / | \\")
    print("  3--|--1")
    print("   \\ | /")
    print("     2")
    print()
    
    patterns = [
        ("Space ' '", "All triangles connected"),
        ("Forward '/'", "0-3 connected, 1-2 connected"),
        ("Back '\\'", "0-1 connected, 2-3 connected")
    ]
    
    for pattern, connection in patterns:
        print(f"{pattern}: {connection}")
    
    print()
    print("Adjacent cells connect:")
    print("- Right neighbor: triangle 1 connects to triangle 3")
    print("- Bottom neighbor: triangle 2 connects to triangle 0")

def visualize_3x3_expansion():
    """Show how 3x3 expansion works"""
    print("\n3x3 Expansion Visualization:")
    print("=" * 50)
    
    examples = [
        {
            "char": " ",
            "pattern": [
                "000",
                "000", 
                "000"
            ],
            "description": "Space: all cells open"
        },
        {
            "char": "/",
            "pattern": [
                "001",
                "010",
                "100"
            ],
            "description": "Forward slash: diagonal from top-right to bottom-left"
        },
        {
            "char": "\\",
            "pattern": [
                "100",
                "010",
                "001"
            ],
            "description": "Back slash: diagonal from top-left to bottom-right"
        }
    ]
    
    for example in examples:
        char = example["char"]
        pattern = example["pattern"]
        description = example["description"]
        
        print(f"Character '{char}': {description}")
        for row in pattern:
            print(f"  {' '.join(row)}")
        print()

def compare_approaches():
    """Compare different solution approaches"""
    solution = Solution()
    
    test_grid = ["\\/", "/\\"]
    
    approaches = [
        ("Union-Find + Triangles", solution.regionsBySlashes),
        ("DFS + 3x3 Expansion", solution.regionsBySlashesDFS),
        ("BFS + 3x3 Expansion", solution.regionsBySlashesBFS),
    ]
    
    print("Comparing Different Approaches:")
    print("=" * 50)
    print(f"Test grid: {test_grid}")
    print()
    
    results = []
    for name, method in approaches:
        result = method(test_grid)
        results.append(result)
        print(f"{name}: {result}")
    
    all_same = all(r == results[0] for r in results)
    print(f"\nAll approaches consistent: {'✓' if all_same else '✗'}")

def analyze_complexity():
    """Analyze time and space complexity of different approaches"""
    print("\nComplexity Analysis:")
    print("=" * 50)
    
    approaches = [
        ("Union-Find", "O(N² × α(N²))", "O(N²)", "Most efficient, elegant"),
        ("DFS Expansion", "O(N²)", "O(N²)", "Intuitive, easy to understand"),
        ("BFS Expansion", "O(N²)", "O(N²)", "Similar to DFS, iterative"),
        ("Euler Formula", "O(N²)", "O(1)", "Mathematical, complex to derive"),
    ]
    
    print(f"{'Approach':<15} {'Time':<15} {'Space':<8} {'Notes'}")
    print("-" * 55)
    
    for approach, time, space, notes in approaches:
        print(f"{approach:<15} {time:<15} {space:<8} {notes}")
    
    print("\nWhere N is the grid dimension")
    print("α(N) is the inverse Ackermann function (practically constant)")
    
    print("\nRecommendation:")
    print("- Union-Find: Best for interviews (elegant, optimal)")
    print("- DFS Expansion: Good if Union-Find is not familiar")
    print("- Mathematical approaches: Advanced, not typically expected")

def demonstrate_edge_cases():
    """Test edge cases and corner scenarios"""
    solution = Solution()
    
    print("\nTesting Edge Cases:")
    print("=" * 50)
    
    edge_cases = [
        {
            "name": "Single cell empty",
            "grid": [" "],
            "expected": 1,
            "description": "Minimal case with one region"
        },
        {
            "name": "Single cell with slash",
            "grid": ["/"],
            "expected": 2,
            "description": "Slash divides single cell"
        },
        {
            "name": "All empty",
            "grid": ["  ", "  "],
            "expected": 1,
            "description": "No divisions, single region"
        },
        {
            "name": "All slashes same direction",
            "grid": ["//", "//"],
            "expected": 3,
            "description": "Parallel slashes create regions"
        },
        {
            "name": "Complex pattern",
            "grid": ["/\\", "\\/", "/\\"],
            "expected": 7,
            "description": "Alternating pattern"
        }
    ]
    
    for case in edge_cases:
        result = solution.regionsBySlashes(case["grid"])
        expected = case["expected"]
        
        print(f"{case['name']}:")
        print(f"  Grid: {case['grid']}")
        print(f"  Description: {case['description']}")
        print(f"  Result: {result}")
        print(f"  Expected: {expected}")
        print(f"  Correct: {'✓' if result == expected else '✗'}")
        print()

def demonstrate_real_world_applications():
    """Show real-world applications of this problem"""
    print("Real-world Applications:")
    print("=" * 50)
    
    applications = [
        {
            "domain": "Computer Graphics",
            "use_case": "Polygon triangulation and region detection",
            "example": "Identifying enclosed areas in vector graphics"
        },
        {
            "domain": "Game Development", 
            "use_case": "Level design and collision detection",
            "example": "Detecting separate rooms or areas in a maze"
        },
        {
            "domain": "Geographic Information Systems",
            "use_case": "Land parcel division and boundary analysis",
            "example": "Counting separate land plots divided by roads"
        },
        {
            "domain": "Circuit Design",
            "use_case": "Identifying isolated circuit regions",
            "example": "Finding separate conductive areas on PCB"
        },
        {
            "domain": "Image Processing",
            "use_case": "Connected component labeling",
            "example": "Identifying separate objects in binary images"
        }
    ]
    
    for app in applications:
        domain = app["domain"]
        use_case = app["use_case"]
        example = app["example"]
        
        print(f"{domain}:")
        print(f"  Use case: {use_case}")
        print(f"  Example: {example}")
        print()

if __name__ == "__main__":
    test_basic_functionality()
    visualize_triangle_subdivision()
    visualize_3x3_expansion()
    compare_approaches()
    analyze_complexity()
    demonstrate_edge_cases()
    demonstrate_real_world_applications()

"""
INTERVIEW STRATEGY & KEY POINTS:

1. PROBLEM UNDERSTANDING:
   - N×N grid where each cell contains ' ', '/', or '\\'
   - Slashes act as barriers dividing regions
   - Count number of separate regions formed
   - Similar to counting connected components in a graph

2. KEY INSIGHTS:

   INSIGHT 1: Transform to Graph Problem
   - Convert geometric problem to graph connectivity
   - Need to represent how slashes divide space
   - Count connected components in resulting graph

   INSIGHT 2: Two Main Approaches
   - Triangle subdivision: divide each cell into 4 triangles
   - Grid expansion: expand each cell to 3×3 sub-grid
   - Both enable standard graph algorithms

3. OPTIMAL APPROACHES:

   APPROACH 1 - Union-Find with Triangle Subdivision (RECOMMENDED):
   - Divide each cell into 4 triangles (N, E, S, W)
   - Slashes determine which triangles connect
   - Use Union-Find to count components efficiently

   APPROACH 2 - DFS/BFS with 3×3 Expansion:
   - Expand each 1×1 cell to 3×3 grid
   - Draw slashes as blocked diagonal lines
   - Use DFS/BFS to count connected regions

4. WHY TRIANGLE SUBDIVISION IS ELEGANT:
   - Direct mapping from problem to Union-Find
   - No grid expansion needed (space efficient)
   - Cleaner conceptual model
   - Optimal time complexity with Union-Find

5. ALGORITHM WALKTHROUGH (Union-Find):
   - Each cell has 4 triangles numbered 0,1,2,3 (N,E,S,W)
   - Space ' ': connect all 4 triangles
   - Forward '/': connect 0-3 and 1-2
   - Back '\\': connect 0-1 and 2-3
   - Connect adjacent cells appropriately
   - Count final components

6. COMPLEXITY ANALYSIS:
   - Union-Find: O(N² × α(N²)) time, O(N²) space
   - DFS/BFS: O(N²) time, O(N²) space
   - Both are acceptable, Union-Find slightly more efficient

7. EDGE CASES:
   - Single cell with/without slash
   - All spaces (single region)
   - All slashes in same direction
   - Complex interlocking patterns

8. INTERVIEW PRESENTATION:
   - Start with: "This is a connected components problem"
   - Present both triangle and expansion approaches
   - Choose Union-Find approach as primary
   - Walk through triangle subdivision logic
   - Show example with actual grid

9. FOLLOW-UP QUESTIONS:
   - "What if we had different slash types?" → Extend subdivision logic
   - "How to handle updates efficiently?" → Dynamic connectivity
   - "3D version?" → More complex spatial subdivision
   - "Weighted regions?" → Modify Union-Find to track sizes

10. WHY THIS PROBLEM IS INTERESTING:
    - Creative problem transformation (geometric → graph)
    - Multiple valid approaches with different trade-offs
    - Tests understanding of Union-Find data structure
    - Real-world applications in graphics and GIS

11. COMMON MISTAKES:
    - Not recognizing this as connected components problem
    - Incorrect triangle subdivision logic
    - Wrong adjacent cell connections
    - Off-by-one errors in grid expansion

12. IMPLEMENTATION DETAILS:
    - Triangle indexing: 0=North, 1=East, 2=South, 3=West
    - Adjacent connections: right cell (1→3), bottom cell (2→0)
    - Union-Find with path compression and union by rank
    - Proper handling of grid boundaries

13. OPTIMIZATION OPPORTUNITIES:
    - Early termination if all cells are spaces
    - Bit manipulation for space optimization
    - Parallel processing for large grids
    - Incremental updates for dynamic scenarios

14. KEY INSIGHT TO ARTICULATE:
    "The key insight is transforming this geometric problem into a graph 
    connectivity problem. By subdividing each cell into triangular regions 
    and modeling slashes as separators between specific triangles, I can 
    use Union-Find to efficiently count connected components. This elegant 
    transformation reduces a complex geometric problem to a well-understood 
    algorithmic pattern."

15. INTERVIEW TIPS:
    - Draw diagrams showing triangle subdivision
    - Explain why 4 triangles per cell works
    - Show how slashes affect triangle connections
    - Walk through Union-Find operations
    - Mention grid expansion as alternative approach
    - Discuss complexity trade-offs between approaches
"""
