from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = [0] * n
        self.ptr = [0] * n

    def add_edge(self, u, v, cap):
        index1 = len(self.graph[u])
        index2 = len(self.graph[v])
        self.graph[u].append([v, cap, 0, index2])
        self.graph[v].append([u, 0, 0, index1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque()
        self.level[s] = 0
        q.append(s)
        while q:
            u = q.popleft()
            for edge in self.graph[u]:
                v, cap, flow, rev_index = edge
                if cap - flow > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] != -1

    def dfs(self, u, flow, t):
        if u == t:
            return flow
        for i in range(self.ptr[u], len(self.graph[u])):
            edge = self.graph[u][i]
            v, cap, flow_edge, rev_index = edge
            if self.level[v] == self.level[u] + 1 and cap - flow_edge > 0:
                pushed = self.dfs(v, min(flow, cap - flow_edge), t)
                if pushed > 0:
                    edge[2] += pushed
                    rev_edge = self.graph[v][rev_index]
                    rev_edge[2] -= pushed
                    return pushed
            self.ptr[u] += 1
        return 0

    def max_flow(self, s, t, verbose=False):
        total_flow = 0
        step = 0
        while self.bfs(s, t):
            
            step += 1
            if verbose:
                print(f"Krok {step}: po BFS - warstwy: {self.level}")
            self.ptr = [0] * self.n
            inner_step = 0
            while True:
                pushed = self.dfs(s, float('inf'), t)
                if pushed == 0:
                    break
                total_flow += pushed
                inner_step += 1
                if verbose:
                    print(f"  Krok {step}.{inner_step}: wysłano przepływ {pushed}, całkowity przepływ: {total_flow}")
        if verbose:
            print(f"Ostateczny maksymalny przepływ: {total_flow}")
        return total_flow

def load_graph_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    n = int(lines[0])
    dinic = Dinic(n)
    for u, line in enumerate(lines[1:]):
        parts = list(map(int, line.strip().split()))
        k = parts[0]
        for i in range(k):
            v = parts[1 + 2 * i] - 1
            cap = parts[2 + 2 * i]
            dinic.add_edge(u, v, cap)
    return dinic

if __name__ == "__main__":
    # Przykład 1
    n1 = 4
    dinic1 = Dinic(n1)
    dinic1.add_edge(0, 1, 10)
    dinic1.add_edge(0, 2, 10)
    dinic1.add_edge(1, 2, 2)
    dinic1.add_edge(1, 3, 15)
    dinic1.add_edge(2, 3, 10)
    print("Przykład 1:")
    print("Maksymalny przepływ:", dinic1.max_flow(0, 3, verbose=True))
    print()

    # Przykład 2
    n2 = 4
    dinic2 = Dinic(n2)
    dinic2.add_edge(0, 1, 3)
    dinic2.add_edge(0, 2, 2)
    dinic2.add_edge(1, 2, 5)
    dinic2.add_edge(1, 3, 2)
    dinic2.add_edge(2, 3, 3)
    print("Przykład 2:")
    print("Maksymalny przepływ:", dinic2.max_flow(0, 3, verbose=True))
    print()

    try:
        dinic_file = load_graph_from_file("graf.txt")
        if dinic_file:
            print("Maksymalny przepływ z pliku:", dinic_file.max_flow(0, dinic_file.n - 1, verbose=True))
    except FileNotFoundError:
        print("Plik 'graf.txt' nie został znaleziony — pomijam test z pliku.")

