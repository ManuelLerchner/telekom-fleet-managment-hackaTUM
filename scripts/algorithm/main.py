import solver
from graph import *


A1 = Vertex("A1", (-5, 1), "vehicle")
A2 = Vertex("A2", (2, -1), "vehicle")

K1 = Vertex("K1", (-4, -0.5), "start")
K2 = Vertex("K2", (0, -1), "start")
K3 = Vertex("K3", (4, -1), "start")

Z1 = Vertex("Z1", (0, 1), "destination")
Z2 = Vertex("Z2", (-2, -2), "destination")
Z3 = Vertex("Z3", (3, 5), "destination")

cars = [A1, A2]
customers = [(K1, Z1), (K2, Z2), (K3, Z3)]

edges = []
for (c_start, c_goal) in customers:
    edges.append((c_start, c_goal))
    for car in cars:
        edges.append((car, c_start))

# connect goals of customer to start of next customer
for (c_start1, c_goal1) in customers:
    for (c_start2, _) in customers:
        if c_start1 == c_start2:
            continue
        edges.append((c_goal1, c_start2))

g = Graph(cars + [c[0] for c in customers] + [c[1]
                                              for c in customers], edges)

print(g)

g.draw_graph(output_file="graph.png")


(graph, total_distance, solution) = solver.solve(g, max_checks=10000)

solver.print_solution(solution.car_paths, total_distance)

g.draw_graph(solution=solution, output_file="solution.png")

print(solution.convertToTöbbe())
