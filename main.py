import networkx as nx
import matplotlib.pyplot as plt
import random

nodes = 100
probability = 0.08

def assign_random_colors(graph, number_of_colors):
    colors = [0] * graph.number_of_nodes()
    for node in graph.nodes():
        colors[node] = random.randint(0, number_of_colors - 1)
    return colors

def count_conflicts(graph, colors):
    conflicts = 0
    conflicting_edges = []
    conflicting_corners = []

    for u, v in graph.edges():
        if colors[u] == colors[v]:
            conflicts += 1
            conflicting_edges.append((u, v))

            if u not in conflicting_corners:
                conflicting_corners.append(u)
            if v not in conflicting_corners:
                conflicting_corners.append(v)

    return conflicts, conflicting_corners, conflicting_edges

def draw_graph(graph, colors, title):
    color_map = [colors[node] for node in graph.nodes()]
    plt.figure(figsize=(8, 6))
    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.title(title)
    plt.show()

def improve_colors(graph, colors_set, conflicting_corners, num_colors):
    new_colors = colors_set.copy()

    for node in conflicting_corners:
        best_color = colors_set[node]
        min_conflicts = float('inf')

        for color in range(num_colors):
            local_conflicts = 0
            for neighbor in graph.neighbors(node):
                if colors_set[neighbor] == color:
                    local_conflicts += 1

            if local_conflicts < min_conflicts:
                min_conflicts = local_conflicts
                best_color = color

        new_colors[node] = best_color

    return new_colors

num_colors_list = [2, 3, 4, 5, 6, 7, 8]
all_results = []

R = nx.gnp_random_graph(nodes, probability)
nx.draw(R, with_labels=True)


for c in num_colors_list:
    print("\nGenerating graph with c =", c)
    num_conflicts_list = []

    random_colors = assign_random_colors(R, c)

    num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, random_colors)
    num_conflicts_list.append(num_conflicts)
    print("Initial number of conflicts:", num_conflicts)
    print("Conflicting nodes:", conflicting_nodes)
    print("Conflicting pairs:", conflicting_pairs)

    for i in range(10):
        random_colors = improve_colors(R, random_colors, conflicting_nodes, c)
        num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, random_colors)
        num_conflicts_list.append(num_conflicts)

        print(f"Iteration {i + 1} - Number of conflicts: {num_conflicts}")
        print(f"Iteration {i + 1} - Conflicting nodes: {conflicting_nodes}")
        print(f"Iteration {i + 1} - Conflicting pairs: {conflicting_pairs}")

    all_results.append({
        "c": c,
        "conflicts": num_conflicts_list
    })

plt.figure(figsize=(12, 8))

for result in all_results:
    iterations = list(range(1, len(result["conflicts"]) + 1))
    label = f'c={result["c"]}'
    plt.plot(iterations, result["conflicts"], marker='o', label=label)

plt.xlabel("Iteration")
plt.ylabel("Number of Conflicts")
plt.title("Conflicts Over Iterations for Different Numbers of Colors")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()


#2D lattice/ Grid Graph
# grid = nx.grid_2d_graph(7, 7)
# gridGraph = nx.convert_node_labels_to_integers(grid)
# draw_graph(gridGraph, random_colors, "Grid Graph")
#
# #Ring/Cycle Graph
# cycleGraph = nx.cycle_graph(R)
# draw_graph(cycleGraph, random_colors, "Cycle Graph")
#
#
# #Random Geometric Graph
# closeGraph = nx.random_geometric_graph(R, radius=0.2)
# draw_graph(closeGraph, random_colors, "Close Graph")