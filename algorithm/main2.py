import solver
from graph import *
import random

random.seed(42)

cars = []
for i in range(5):
    rx = random.uniform(-10, 10)
    ry = random.uniform(-10, 10)

    cars.append(Vertex(f"A{i}", (rx, ry), "vehicle"))

customers = []
for i in range(10):
    kx = random.uniform(-10, 10)
    ky = random.uniform(-10, 10)

    zx = random.uniform(-10, 10)
    zy = random.uniform(-10, 10)

    c = Vertex(f"K{i}", (kx, ky), "start")
    z = Vertex(f"Z{i}", (zx, zy), "destination")

    customers.append((c, z))


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


g.draw_graph(output_file="graph.png")

for i in range(1, 10):
    checks = i * 100000

    (graph, total_distance, solution) = solver.solve(g, max_checks=checks)

    # solver.print_solution(solution.car_paths, total_distance)

    g.draw_graph(solution=solution, output_file="solution.png")

    print(f"Checks: {checks}, Distance: {total_distance}")
