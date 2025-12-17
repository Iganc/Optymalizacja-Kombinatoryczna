from typing import List, Tuple

EPS = 1e-9

class Point:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
    def __repr__(self):
        return f"({int(self.x)},{int(self.y)})"
    def __lt__(self, other):
        if abs(self.x - other.x) < EPS:
            return self.y < other.y
        return self.x < other.x

class Polygon:
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices
        self.n = len(vertices)

def orient(a: Point, b: Point, c: Point) -> float:
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def identify_chains(poly: Polygon) -> Tuple[List[int], List[int]]:
    n = poly.n
    left_idx = min(range(n), key=lambda i: (poly.vertices[i].x, poly.vertices[i].y))
    right_idx = max(range(n), key=lambda i: (poly.vertices[i].x, poly.vertices[i].y))
    upper_chain = []
    lower_chain = []
    i = left_idx
    while True:
        upper_chain.append(i)
        if i == right_idx:
            break
        i = (i + 1) % n
    i = left_idx
    while True:
        lower_chain.append(i)
        if i == right_idx:
            break
        i = (i - 1) % n
    if poly.vertices[upper_chain[1]].y > poly.vertices[lower_chain[1]].y:
        return upper_chain, lower_chain
    else:
        return lower_chain, upper_chain

def zipper_triangulation(poly: Polygon) -> List[Tuple[Point, Point]]:
    n = poly.n
    if n < 3:
        return []
    upper_chain, lower_chain = identify_chains(poly)
    if upper_chain[0] == lower_chain[0]:
        lower_chain = lower_chain[1:]
    if upper_chain[-1] == lower_chain[-1]:
        lower_chain = lower_chain[:-1]
    diagonals = []
    indices = list(range(n))
    indices.sort(key=lambda i: (poly.vertices[i].x, poly.vertices[i].y))
    stack = [indices[0], indices[1]]
    for i in range(2, n-1):
        current = indices[i]
        top = stack[-1]
        current_on_upper = current in upper_chain
        top_on_upper = top in upper_chain
        if current_on_upper != top_on_upper:
            popped = stack[1:]
            stack = [stack[0]]
            for v in popped[:-1]:
                diagonals.append((poly.vertices[v], poly.vertices[current]))
            stack.append(popped[-1])
            stack.append(current)
        else:
            last = stack.pop()
            while stack:
                top_idx = stack[-1]
                if (current_on_upper and orient(poly.vertices[top_idx], poly.vertices[last], poly.vertices[current]) < -EPS) or \
                   (not current_on_upper and orient(poly.vertices[top_idx], poly.vertices[last], poly.vertices[current]) > EPS):
                    diagonals.append((poly.vertices[top_idx], poly.vertices[current]))
                    last = stack.pop()
                else:
                    break
            stack.append(last)
            stack.append(current)
    last_vertex = indices[n-1]
    if len(stack) >= 3:
        for j in range(1, len(stack)-1):
            diagonals.append((poly.vertices[stack[j]], poly.vertices[last_vertex]))
    return diagonals

def read_input(filename: str) -> Polygon:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    pts = [Point(*map(float, lines[i].split())) for i in range(1, n+1)]
    return Polygon(pts)

def save_output(diagonals: List[Tuple[Point, Point]], filename: str):
    with open(filename, 'w') as f:
        for a, b in diagonals:
            f.write(f"({int(a.x)},{int(a.y)})({int(b.x)},{int(b.y)})\n")

def main():
    chosen_file = 2
    filename = "input1.txt" if chosen_file == 1 else "input2.txt"
    try:
        poly = read_input(filename)
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {filename}")
        return
    diagonals = zipper_triangulation(poly)
    normalized_diagonals = []
    for (a, b) in diagonals:
        if a < b:
            normalized_diagonals.append((a, b))
        else:
            normalized_diagonals.append((b, a))
    sorted_diagonals = sorted(normalized_diagonals, key=lambda d: (d[0].x, d[0].y, d[1].x, d[1].y))
    if len(sorted_diagonals) != poly.n - 3:
        print(f"Uwaga: wygenerowano {len(sorted_diagonals)} przekątnych (oczekiwano {poly.n-3})")
    save_output(sorted_diagonals, "output.txt")
    print(f"Gotowe. Zapisano {len(sorted_diagonals)} przekątnych do output.txt")

if __name__ == "__main__":
    main()
