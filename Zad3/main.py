import sys
from wykresy import save_tree_plot

EPS = 1e-9

class Point:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.u = x + y
        self.v = x - y

    def __repr__(self):
        return f"({self.x},{self.y})"

def get_initial_params(points):
    if not points:
        return 0, 0, 0
    
    min_u = min(p.u for p in points)
    max_u = max(p.u for p in points)
    min_v = min(p.v for p in points)
    max_v = max(p.v for p in points)
    
    R = max(max_u - min_u, max_v - min_v) / 2
    c_u = (min_u + max_u) / 2
    c_v = (min_v + max_v) / 2
    
    return c_u, c_v, R

def solve_recursive(points, c_u, c_v, R):
    if not points:
        return 0.0
    
    if len(points) == 1:
        return float(R)

    total_cost = 0.0
    child_R = R / 2
    
    child_centers = [
        (c_u + child_R, c_v + child_R),
        (c_u + child_R, c_v - child_R),
        (c_u - child_R, c_v + child_R),
        (c_u - child_R, c_v - child_R)
    ]
    
    groups = [[] for _ in range(4)]
    assigned = [False] * len(points)
    
    for i in range(4):
        cu_child, cv_child = child_centers[i]
        for idx, p in enumerate(points):
            if not assigned[idx]:
                if abs(p.u - cu_child) <= child_R + EPS and abs(p.v - cv_child) <= child_R + EPS:
                    groups[i].append(p)
                    assigned[idx] = True

    for i in range(4):
        if groups[i]:
            total_cost += child_R
            total_cost += solve_recursive(groups[i], child_centers[i][0], child_centers[i][1], child_R)
            
    return total_cost

def read_input(filename: str):
    points = []
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                return []
            n = int(lines[0])
            for i in range(1, n + 1):
                coords = list(map(float, lines[i].split()))
                if len(coords) >= 2:
                    points.append(Point(coords[0], coords[1]))
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return []
    except Exception as e:
        print(f"Błąd podczas odczytu pliku: {e}")
        return []
    return points

def main():
    input_file = "input1.txt"
    points = read_input(input_file)
    
    if len(points) < 3:
        if not points: return
        
    c_u, c_v, R = get_initial_params(points)
    total_cost = solve_recursive(points, c_u, c_v, R)
    
    res_cost = int(total_cost) if total_cost.is_integer() else round(total_cost, 2)
    res_radius = int(R) if R.is_integer() else round(R, 2)
    
    print(f"({res_cost}, {res_radius})")
    save_tree_plot(points, c_u, c_v, R, "wynik_testu.png")

if __name__ == "__main__":
    main()