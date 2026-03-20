import networkx as nx
import matplotlib.pyplot as plt
import random

nodes = 100
probability = 0.16

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

    if not conflicting_corners:
        return new_colors

    node = random.choice(conflicting_corners)
    best_colors = []
    min_conflicts = float('inf')

    for color in range(num_colors):
        local_conflicts = 0
        for neighbor in graph.neighbors(node):
            if new_colors[neighbor] == color:
                local_conflicts += 1

        if local_conflicts < min_conflicts:
            min_conflicts = local_conflicts
            best_colors = [color]
        elif local_conflicts == min_conflicts:
            best_colors.append(color)

    best_color = random.choice(best_colors)
    new_colors[node] = best_color

    return new_colors

num_colors_list = [2, 4, 6, 8,10,12,14,16]
all_results = []
lowest_c_with_zero_conflicts = int(1e9)  # A large number to track the lowest c that achieves zero conflicts
R = nx.gnp_random_graph(nodes, probability)
nx.draw(R, with_labels=True)


for c in num_colors_list:
    print("\n---------------Generating graph with ", c," colors------------------\n")
    num_conflicts_list = []

    random_colors = assign_random_colors(R, c)

    num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, random_colors)
    num_conflicts_list.append(num_conflicts)
    print("Initial number of conflicts:", num_conflicts)
    print("Conflicting nodes:", conflicting_nodes)
    print("Conflicting pairs:", conflicting_pairs)

    for i in range(500):
        random_colors = improve_colors(R, random_colors, conflicting_nodes, c)
        num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, random_colors)
        num_conflicts_list.append(num_conflicts)

        if num_conflicts ==0:
            if c < lowest_c_with_zero_conflicts :
                lowest_c_with_zero_conflicts = c



    print("Number of conflicts over iterations:", num_conflicts_list)
    all_results.append({
        "c": c,
        "conflicts": num_conflicts_list
    })

plt.figure(figsize=(12, 8))
if lowest_c_with_zero_conflicts == int(1e9):
    print("\nNo number of colors in the tested range achieved 0 conflicts.")
else:
    print("\nLowest number of colors that reached 0 conflicts:", lowest_c_with_zero_conflicts)
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