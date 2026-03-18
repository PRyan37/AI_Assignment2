import networkx as nx
import matplotlib.pyplot as plt
import random



nodes=100
edges=90
probability=0.12
num_colors=6
conflicting_nodes = []

def assign_random_colors(graph, num_colors):
    colors = [0]*graph.number_of_nodes()
    for node in graph.nodes():
        colors[node] = random.randint(0, num_colors - 1)
    return colors

def count_conflicts(graph, colors):
    conflicts = 0
    conflicting_nodes = []
    for u, v in graph.edges():
        if colors[u] == colors[v]:
            conflicts += 1
            if  u not in conflicting_nodes:
                conflicting_nodes.append(u)
            if v not in conflicting_nodes:
                conflicting_nodes.append(v)
    return conflicts , conflicting_nodes

def draw_graph(graph, colors,title):
    color_map = [colors[node] for node in graph.nodes()]
    plt.figure(figsize=(8, 6))
    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.title(title)
    plt.show()

def fix_conflicts(graph, colors,conflicting_nodes):
    for node in conflicting_nodes:
        best_color= colors[node]
        min_conflicts=float('inf')

        for color in colors:
            local_conflicts=0
            for neighbor in graph.neighbors(node):
                if colors[neighbor] == color:
                    local_conflicts += 1
            if local_conflicts < min_conflicts:
                min_conflicts = local_conflicts
                best_color = color
        colors[node] = best_color


    return colors

R = nx.gnp_random_graph(nodes, probability)

while not nx.is_connected(R):
    R = nx.gnm_random_graph(nodes, edges)



random_colors = assign_random_colors(R, num_colors)

num_conflicts,conflicting_nodes =count_conflicts(R, random_colors)
print("Number of conflicts: ", num_conflicts)
print("Conflicting nodes: ", conflicting_nodes)

#Erdos-Renyi Random Graph
draw_graph(R, random_colors, "Random Graph")

fix_colors=fix_conflicts(R, random_colors , conflicting_nodes)
num_conflicts, conflicting_nodes = count_conflicts(R, fix_colors)
print("Iteration 1 - Number of conflicts: ", num_conflicts)
print("Iteration 1 - Conflicting nodes: ", conflicting_nodes)



for i in range(4):
    fix_colors = fix_conflicts(R, fix_colors , conflicting_nodes)
    num_conflicts, conflicting_nodes = count_conflicts(R, fix_colors)
    print(f"Iteration {i+2} - Number of conflicts: ", num_conflicts)
    print(f"Iteration {i+2} - Conflicting nodes: ", conflicting_nodes)

draw_graph(R, fix_colors, "Fixed Random Graph")


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