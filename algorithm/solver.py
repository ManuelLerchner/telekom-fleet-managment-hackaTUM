from graph import *


def get_possible_moves(graph: Graph):
    cars = [v for v in graph.vertices if v.type == "auto"]

    moves: list[tuple[Vertex, tuple[Vertex, float, Vertex]]] = []
    for car in cars:
        neighbors = graph.get_neighbors(car)
        for (startLocation, reachTime) in neighbors:
            (endLocation, travelTime) = graph.get_neighbors(startLocation)[0]
            moves.append(
                (car, (startLocation, reachTime+travelTime, endLocation)))

    # sort moves by travel time
    # moves.sort(key=lambda x: x[1][1], reverse=False)

    return moves


def perform_move(graph: Graph, move: tuple[Vertex, tuple[Vertex, float, Vertex]]):
    car = move[0]
    (customer, travelTime, customer_goal) = move[1]

    # print(f"Moving car {car.name} to {
    #       customer.name}->{customer_goal.name} with travel time {travelTime}")

    # remove car
    graph.removeVertex(car)

    # remove customer
    graph.removeVertex(customer)

    # set car to customer target
    connections = graph.get_neighbors(customer_goal)
    connections = list(map(lambda x: x[0], connections))

    graph.removeVertex(customer_goal)

    newcar = Vertex(car.name, customer_goal.pos, "auto")

    graph.addVertex(newcar, connections)

    return graph, travelTime, newcar


def undo_move(graph: Graph, move: tuple[Vertex, tuple[Vertex, float, Vertex]]):
    car = move[0]
    (customer, travelTime, customer_goal) = move[1]

    # print(f"Undoing move of car {car.name} to {
    #       customer.name}->{customer_goal.name} with travel time {travelTime}")

    # remove car
    graph.removeVertex(car)

    customers = [v for v in graph.vertices if v.type == "kunde"]
    goals = [v for v in graph.vertices if v.type == "ziel"]

    # add customer goal
    graph.addVertex(customer_goal, customers)

    # add customer
    graph.addVertex(customer, [customer_goal])

    # add edges from goals to customer
    for goal in goals:
        graph.addEdge(goal, customer)

    # add car
    graph.addVertex(car, customers + [customer])

    cars = [v for v in graph.vertices if v.type == "auto"]

    for other_car in cars:
        if other_car == car:
            continue
        graph.addEdge(other_car, customer)

    return graph


class Solution:
    def __init__(self, distance: float = float('inf'), graph: Graph = None, car_paths: dict = None, max_checks=float("inf")):
        self.distance = distance
        self.graph = graph
        self.car_paths = car_paths
        self.max_checks = max_checks

    def copy(self):
        new_solution = Solution()
        new_solution.distance = self.distance
        new_solution.graph = self.graph.copy() if self.graph else None
        new_solution.car_paths = {
            car: path.copy() for car, path in self.car_paths.items()
        }
        return new_solution

    def convertToTöbbe(self):
        d = dict()
        for car, path in self.car_paths.items():
            customers = list(map(lambda x: x[0].name, path.moves))
            d[car] = customers

        return d


class CarPath:
    def __init__(self, initial_car: Vertex):
        self.moves = []  # List of (customer, travel_time, goal) tuples
        self.current_position = initial_car

    def add_move(self, customer: Vertex, travel_time: float, goal: Vertex, new_position: Vertex):
        self.moves.append((customer, travel_time, goal))
        self.current_position = new_position

    def undo_last_move(self, original_position: Vertex):
        self.moves.pop()
        self.current_position = original_position

    def total_distance(self):
        return sum(time for _, time, _ in self.moves)

    def copy(self):
        new_path = CarPath(self.current_position)
        new_path.moves = self.moves.copy()
        return new_path


def solve(graph: Graph, car_paths: dict = None, best_solution: Solution = None, max_checks=float("inf")) -> tuple[Graph, float, Solution]:
    if best_solution is None:
        best_solution = Solution(max_checks=max_checks)

    if car_paths is None:
        # Initialize car paths for all cars
        car_paths = {
            car.name: CarPath(car)
            for car in graph.vertices if car.type == "auto"
        }

    # Check if we've found a solution (no more customers)
    customers = [v for v in graph.vertices if v.type == "kunde"]
    if not customers:
        best_solution.max_checks -= 1

        total_distance = sum(path.total_distance()
                             for path in car_paths.values())

        if total_distance < best_solution.distance:
            best_solution.distance = total_distance
            best_solution.car_paths = {
                car: path.copy() for car, path in car_paths.items()
            }

        return graph, best_solution.distance, best_solution

    # abort if max_checks is reached
    if best_solution.max_checks <= 0:
        return graph, best_solution.distance, best_solution

    moves = get_possible_moves(graph)
    for move in moves:
        car, (customer, travel_time, goal) = move

        # Perform move and track path
        g1, move_distance, new_car_pos = perform_move(graph, move)
        car_paths[car.name].add_move(
            customer, move_distance, goal, new_car_pos)

        # Recursive solve
        _, min_distance, best_paths = solve(g1, car_paths, best_solution)

        # Undo move and path tracking
        car_paths[car.name].undo_last_move(car)
        undo_move(graph, move)

    return graph, best_solution.distance, best_solution


def print_solution(car_paths: dict, total_distance: float):
    print(f"\nBest solution found with total distance: {total_distance}")
    for car_name, path in car_paths.items():
        print(f"\nCar {car_name} path (total distance: {
              path.total_distance()})")
        for i, (customer, time, goal) in enumerate(path.moves, 1):
            print(f"  {i}. Pick up customer {
                  customer.name} -> Drive to {goal.name} (time: {time})")
    print("\n")
    print("\n")
    print("\n")
