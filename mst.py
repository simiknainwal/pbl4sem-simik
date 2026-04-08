from sorting import merge_sort

class DisjointSet:
    def __init__(self, n):
        self.parent = []
        for i in range(n):
            self.parent.append(i)
            
    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i, j):
        up_i = self.find(i)
        up_j = self.find(j)
        if(up_i==up_j):return False
        else: 
            self.parent[up_j]=up_i
            return True
        
def kruskal_mst(graph):
    edges = graph.get_all_edges()
    
    def get_weight(item):
        return item[2]
        
    edges = merge_sort(edges, key=get_weight)
    n=graph.get_number_of_nodes()
    ds = DisjointSet(n)
    mst = []
    total_cost = 0
    
    for edge in edges:
        u = edge[0]
        v = edge[1]
        w = edge[2]
        
        if graph.is_blocked(u, v):
            continue
        if ds.union(u, v):
            mst.append((u, v, w))
            total_cost += w
            
    return mst, total_cost
