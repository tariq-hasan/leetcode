"""
LeetCode 721: Accounts Merge

Problem: Given a list of accounts where each element accounts[i] is a list of strings, 
where the first element accounts[i][0] is a name, and the rest of the elements are 
emails representing emails of the account.

Now, two accounts definitely belong to the same person if there is some common email 
to both accounts. Note that even if two accounts have the same name, they may belong 
to different people as people could have the same name. A person can have any number 
of accounts initially, but all of their accounts definitely have some common email.

After merging the accounts, return the accounts in the following format: the first 
element of each account is the name, followed by a sorted list of emails. The accounts 
themselves can be returned in any order.

Example 1:
Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                   ["John","johnsmith@mail.com","john00@mail.com"],
                   ["Mary","mary@mail.com"],
                   ["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
         ["Mary","mary@mail.com"],
         ["John","johnnybravo@mail.com"]]
"""

# SOLUTION 1: Union-Find (Most Expected for Big Tech)
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}
    
    def find(self, x):
        """Find with path compression"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

def accountsMerge(accounts):
    """
    Use Union-Find to group emails that belong to the same person.
    
    Time: O(n * m * α(n*m)) where n is accounts, m is avg emails per account
          Practically O(n * m) due to inverse Ackermann function
    Space: O(n * m) - for Union-Find and mappings
    """
    uf = UnionFind()
    email_to_name = {}  # Map email to account name
    
    # Step 1: Union all emails within each account
    for account in accounts:
        name = account[0]
        emails = account[1:]
        
        for email in emails:
            email_to_name[email] = name
            if len(emails) > 1:
                # Union all emails in this account with the first email
                uf.union(emails[0], email)
    
    # Step 2: Group emails by their root parent
    groups = {}
    for email in email_to_name:
        root = uf.find(email)
        if root not in groups:
            groups[root] = []
        groups[root].append(email)
    
    # Step 3: Build result with sorted emails
    result = []
    for group in groups.values():
        name = email_to_name[group[0]]  # All emails in group have same name
        result.append([name] + sorted(group))
    
    return result


# SOLUTION 2: DFS Graph Traversal
def accountsMergeDFS(accounts):
    """
    Build a graph where emails are nodes and edges connect emails in same account.
    Use DFS to find connected components.
    
    Time: O(n * m + E) where E is total number of email connections
    Space: O(n * m) - for the graph and visited set
    """
    from collections import defaultdict
    
    # Build graph: email -> set of connected emails
    graph = defaultdict(set)
    email_to_name = {}
    
    # Step 1: Build the graph
    for account in accounts:
        name = account[0]
        emails = account[1:]
        
        for email in emails:
            email_to_name[email] = name
        
        # Connect all emails in this account
        for i in range(len(emails)):
            for j in range(i + 1, len(emails)):
                graph[emails[i]].add(emails[j])
                graph[emails[j]].add(emails[i])
    
    # Step 2: DFS to find connected components
    visited = set()
    result = []
    
    def dfs(email, component):
        """DFS to collect all emails in the same component"""
        visited.add(email)
        component.append(email)
        
        for neighbor in graph[email]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for email in email_to_name:
        if email not in visited:
            component = []
            dfs(email, component)
            name = email_to_name[email]
            result.append([name] + sorted(component))
    
    return result


# SOLUTION 3: BFS Graph Traversal
def accountsMergeBFS(accounts):
    """
    Similar to DFS but uses BFS for connected component detection.
    
    Time: O(n * m + E)
    Space: O(n * m)
    """
    from collections import defaultdict, deque
    
    graph = defaultdict(set)
    email_to_name = {}
    
    # Build graph
    for account in accounts:
        name = account[0]
        emails = account[1:]
        
        for email in emails:
            email_to_name[email] = name
        
        # Connect all emails in this account
        for i in range(len(emails)):
            for j in range(i + 1, len(emails)):
                graph[emails[i]].add(emails[j])
                graph[emails[j]].add(emails[i])
    
    # BFS to find connected components
    visited = set()
    result = []
    
    for email in email_to_name:
        if email not in visited:
            # BFS to find all emails in this component
            queue = deque([email])
            component = []
            
            while queue:
                current_email = queue.popleft()
                if current_email not in visited:
                    visited.add(current_email)
                    component.append(current_email)
                    
                    for neighbor in graph[current_email]:
                        if neighbor not in visited:
                            queue.append(neighbor)
            
            name = email_to_name[email]
            result.append([name] + sorted(component))
    
    return result


# SOLUTION 4: Union-Find with Email Indexing (Alternative implementation)
def accountsMergeIndexed(accounts):
    """
    Map emails to indices and use traditional array-based Union-Find.
    Sometimes preferred when you want to avoid dictionary-based Union-Find.
    
    Time: O(n * m * α(n*m))
    Space: O(n * m)
    """
    # Create email to index mapping
    email_to_index = {}
    index_to_email = {}
    email_to_name = {}
    index = 0
    
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_index:
                email_to_index[email] = index
                index_to_email[index] = email
                email_to_name[email] = name
                index += 1
    
    # Traditional array-based Union-Find
    parent = list(range(index))
    rank = [0] * index
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
    
    # Union emails within each account
    for account in accounts:
        emails = account[1:]
        if len(emails) > 1:
            first_email_idx = email_to_index[emails[0]]
            for email in emails[1:]:
                union(first_email_idx, email_to_index[email])
    
    # Group emails by root parent
    groups = {}
    for email, idx in email_to_index.items():
        root = find(idx)
        if root not in groups:
            groups[root] = []
        groups[root].append(email)
    
    # Build result
    result = []
    for group in groups.values():
        name = email_to_name[group[0]]
        result.append([name] + sorted(group))
    
    return result


# Test with examples
def run_examples():
    # Example 1
    accounts1 = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                 ["John","johnsmith@mail.com","john00@mail.com"],
                 ["Mary","mary@mail.com"],
                 ["John","johnnybravo@mail.com"]]
    
    print("Example 1:")
    print("Input:", accounts1)
    print("Output:", accountsMerge(accounts1))
    print()
    
    # Example 2
    accounts2 = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],
                 ["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],
                 ["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],
                 ["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],
                 ["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
    
    print("Example 2:")
    print("Input:", accounts2)
    print("Output:", accountsMerge(accounts2))

if __name__ == "__main__":
    run_examples()


"""
COMPLEXITY ANALYSIS:

Union-Find Approach (Recommended):
- Time: O(n * m * α(n*m)) where n = number of accounts, m = average emails per account
  The α (inverse Ackermann) function is practically constant, so this is effectively O(n*m)
- Space: O(n * m) for storing all emails and Union-Find structure

DFS/BFS Approaches:
- Time: O(n * m + E) where E is the number of email connections (could be O((n*m)²) worst case)
- Space: O(n * m) for the graph

INTERVIEW STRATEGY:
1. Recognize this as a "connected components" problem
2. Explain that emails are nodes, accounts create edges between emails
3. Implement Union-Find as the optimal solution
4. Mention DFS/BFS as alternatives but explain why Union-Find is preferred
5. Handle the sorting requirement and name mapping carefully
"""
