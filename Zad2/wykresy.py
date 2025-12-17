import matplotlib.pyplot as plt
import re

def read_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    points = []
    for i in range(1, n + 1):
        x, y = map(float, lines[i].split())
        points.append((x, y))
    return points

def read_output(filename):
    diagonals = []
    pattern = r"\((\d+),(\d+)\)\((\d+),(\d+)\)"
    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    diagonals.append(((x1, y1), (x2, y2)))
    except FileNotFoundError:
        print(f"Ostrzeżenie: Nie znaleziono pliku {filename}")
    return diagonals

def save_plot(vertices, diagonals, output_image="triangulacja.png"):
    plt.figure(figsize=(10, 10))
    
    polygon_points = vertices + [vertices[0]]
    xs, ys = zip(*polygon_points)
    plt.fill(xs, ys, 'skyblue', alpha=0.2)
    plt.plot(xs, ys, 'b-', lw=2, label='Krawędzie wielokąta')
    
    for i, (p1, p2) in enumerate(diagonals):
        label = 'Przekątne' if i == 0 else ""
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--', lw=1, label=label)
    
    v_xs, v_ys = zip(*vertices)
    plt.scatter(v_xs, v_ys, color='black', zorder=5)
    for i, (x, y) in enumerate(vertices):
        plt.text(x, y, f" V{i}", fontsize=10, fontweight='bold')

    plt.gca().set_aspect('equal')
    plt.title("Wizualizacja Triangulacji")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    plt.close() 
    print(f"Wykres został zapisany do pliku: {output_image}")

if __name__ == "__main__":
    v = read_input("input2.txt")
    d = read_output("output.txt")
    save_plot(v, d, "wynik_triangulacji.png")