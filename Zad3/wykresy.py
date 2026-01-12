import matplotlib.pyplot as plt

def uv_to_xy(u, v):
    """Konwertuje współrzędne z powrotem na układ XY."""
    x = (u + v) / 2
    y = (u - v) / 2
    return x, y

def draw_l1_ball(ax, c_u, c_v, R, color='gray', alpha=0.1):
    """Rysuje diament (kulę L1) na płaszczyźnie XY."""
    # Wierzchołki diamentu w XY
    pts = [
        uv_to_xy(c_u + R, c_v), # góra-prawo w UV
        uv_to_xy(c_u, c_v - R), # dół-prawo w UV
        uv_to_xy(c_u - R, c_v), # dół-lewo w UV
        uv_to_xy(c_u, c_v + R), # góra-lewo w UV
    ]
    pts.append(pts[0]) # zamknij pętlę
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, linestyle=':', alpha=alpha)

def get_tree_edges(points, c_u, c_v, R):
    """
    Zwraca listę krawędzi (x1, y1, x2, y2) oraz listę kul (c_u, c_v, R).
    To jest zmodyfikowana wersja Twojego solve_recursive.
    """
    if not points: return [], []
    
    edges = []
    balls = [(c_u, c_v, R)]
    curr_x, curr_y = uv_to_xy(c_u, c_v)
    
    if len(points) == 1:
        # Lemat 3: Połączenie punktu ze środkiem
        p = points[0]
        edges.append((curr_x, curr_y, p.x, p.y))
        return edges, balls

    child_R = R / 2
    child_centers = [
        (c_u + child_R, c_v + child_R), (c_u + child_R, c_v - child_R),
        (c_u - child_R, c_v + child_R), (c_u - child_R, c_v - child_R)
    ]
    
    # Grupowanie (analogicznie do main.py)
    groups = [[] for _ in range(4)]
    assigned = [False] * len(points)
    EPS = 1e-9
    for i in range(4):
        cu_ch, cv_ch = child_centers[i]
        for idx, p in enumerate(points):
            if not assigned[idx] and abs(p.u-cu_ch) <= child_R+EPS and abs(p.v-cv_ch) <= child_R+EPS:
                groups[i].append(p)
                assigned[idx] = True

    for i in range(4):
        if groups[i]:
            child_x, child_y = uv_to_xy(child_centers[i][0], child_centers[i][1])
            edges.append((curr_x, curr_y, child_x, child_y)) # Krawędź do dziecka
            
            sub_edges, sub_balls = get_tree_edges(groups[i], child_centers[i][0], child_centers[i][1], child_R)
            edges.extend(sub_edges)
            balls.extend(sub_balls)
            
    return edges, balls

def save_tree_plot(points, c_u, c_v, R, output_image="drzewo.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    edges, balls = get_tree_edges(points, c_u, c_v, R)
    
    # 1. Rysuj kule L1 (diamenty)
    for b_u, b_v, b_r in balls:
        draw_l1_ball(ax, b_u, b_v, b_r)
        
    # 2. Rysuj krawędzie drzewa
    for x1, y1, x2, y2 in edges:
        ax.plot([x1, x2], [y1, y2], 'r-', lw=1.5, alpha=0.8)
        
    # 3. Rysuj punkty S
    px = [p.x for p in points]
    py = [p.y for p in points]
    ax.scatter(px, py, color='black', s=30, zorder=5, label='Punkty S (liście)')
    
    # Korzeń
    rx, ry = uv_to_xy(c_u, c_v)
    ax.scatter([rx], [ry], color='green', s=100, marker='*', zorder=6, label='Korzeń')

    ax.set_aspect('equal')
    plt.title(f"Zrównoważone Drzewo L1 (9-aproksymacja)\nKoszt całkowity: ~{sum(abs(x1-x2)+abs(y1-y2) for x1,y1,x2,y2 in edges):.2f}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Wykres zapisany jako: {output_image}")