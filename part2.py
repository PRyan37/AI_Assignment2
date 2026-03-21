import networkx as nx
import matplotlib.pyplot as plt
import random

# the number of nodes and fixed number of colours for Part 2
nodes = 100
num_colors = 8

# list of probabilities to test for graph density
probability_list = [0.05, 0.10, 0.15, 0.18, 0.20, 0.25]
num_trials = 10

#makes a random color map for the graph
def assign_random_colors(graph, number_of_colors):
    colors = [0] * graph.number_of_nodes()
    for node in graph.nodes():
        colors[node] = random.randint(0, number_of_colors - 1)
    return colors

#Counts the number of conflicts in the graph
def count_conflicts(graph, colors):
    conflicts = 0
    conflicting_edges = []
    conflicting_corners = []

    for u, v in graph.edges():
        if colors[u] == colors[v]:
            conflicts += 1
            conflicting_edges.append((u, v))

            #assures there are no repeats in conflicting corners
            if u not in conflicting_corners:
                conflicting_corners.append(u)
            if v not in conflicting_corners:
                conflicting_corners.append(v)

    #returns the total number of conflicts, the list of conflicting nodes (corners), and the list of conflicting edges
    return conflicts, conflicting_corners, conflicting_edges

def draw_graph(graph, colors, title):
    color_map = [colors[node] for node in graph.nodes()]
    plt.figure(figsize=(8, 6))
    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.title(title)
    plt.show()

def improve_colors(graph, colors_set, conflicting_corners, num_colors):
    #this function changes one of the conflicting nodes at a time
    #it tries each possible color on a conflicting node
    #the color with the lowest number of conflicts is chosen
    #if there are multiple best colors it randomly chooses one
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


#TESTING PHASE

all_results = []

for probability in probability_list:
    print("\n---------------Generating graph with probability", probability, "------------------\n")

    success_count = 0
    total_final_conflicts = 0
    total_success_iterations = 0
    first_trial_conflicts = []

    for trial in range(num_trials):
        num_conflicts_list = []

        # generate a new random graph for each trial
        R = nx.gnp_random_graph(nodes, probability)
        random_colors = assign_random_colors(R, num_colors)
        improved_colors = random_colors

        num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, improved_colors)
        num_conflicts_list.append(num_conflicts)

        for i in range(400):
            improved_colors = improve_colors(R, improved_colors, conflicting_nodes, num_colors)
            num_conflicts, conflicting_nodes, conflicting_pairs = count_conflicts(R, improved_colors)
            num_conflicts_list.append(num_conflicts)

            if num_conflicts == 0:
                success_count += 1
                total_success_iterations += (i + 1)
                break

        total_final_conflicts += num_conflicts_list[-1]

        if trial == 0:
            first_trial_conflicts = num_conflicts_list

    average_final_conflicts = total_final_conflicts / num_trials
    average_success_iterations = (
        total_success_iterations / success_count if success_count > 0 else None
    )

    print("Successes:", success_count, "out of", num_trials)
    print("Average final conflicts:", average_final_conflicts)
    if average_success_iterations is not None:
        print("Average iterations to success:", average_success_iterations)
    else:
        print("Average iterations to success: No successful trials")

    all_results.append({
        "p": probability,
        "conflicts": first_trial_conflicts,
        "success_count": success_count,
        "avg_final_conflicts": average_final_conflicts,
        "avg_success_iterations": average_success_iterations
    })


#EVALUATION PHASE

plt.figure(figsize=(12, 8))
for result in all_results:
    iterations = list(range(1, len(result["conflicts"]) + 1))
    label = f'p={result["p"]}'
    plt.plot(iterations, result["conflicts"], marker='o', label=label)

plt.xlabel("Iteration")
plt.ylabel("Number of Conflicts")
plt.title(f"Conflicts Over Iterations for Different Probabilities (c={num_colors})")
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