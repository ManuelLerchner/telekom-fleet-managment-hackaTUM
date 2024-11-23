import graphviz
import typing


class Vertex:
    def __init__(self, name, pos: tuple[float, float], type: typing.Literal["vehicle", "start", "destination"]):
        self.name = name
        self.pos = pos
        self.type = type

    def __str__(self):
        return f"[{self.name}: {self.pos}, {self.type}]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


class Graph:
    def __init__(self, vertices: list[Vertex], edges: list[tuple[Vertex, Vertex]]):
        self.vertices = vertices
        self.w_edges = self.calculate_edge_weights(edges)

    def get_neighbors(self, vertex: Vertex):
        neighbors: list[tuple[Vertex, float]] = []
        for (v1, w, v2) in self.w_edges:
            if v1 == vertex:
                neighbors.append((v2, w))
        return neighbors

    def distance(self, p1: Vertex, p2: Vertex):
        return ((p1.pos[0] - p2.pos[0])**2 + (p1.pos[1] - p2.pos[1])**2)**0.5

    def calculate_edge_weights(self, edges):
        w_edges: list[tuple[Vertex, float, Vertex]] = []

        for (v1, v2) in edges:
            w = self.distance(v1, v2)
            w_edges.append((v1, w, v2))
        return w_edges

    def removeVertex(self, vertex: Vertex):
        self.w_edges = [e for e in self.w_edges if e[0]
                        != vertex and e[2] != vertex]
        self.vertices.remove(vertex)

    def addVertex(self, vertex: Vertex, edges: list[Vertex]):
        self.vertices.append(vertex)
        w = self.calculate_edge_weights([(vertex, e) for e in edges])
        self.w_edges += w

    def addEdge(self, v1: Vertex, v2: Vertex):
        w = self.calculate_edge_weights([(v1, v2)])
        self.w_edges += w

    def copy(self):
        vertices = [Vertex(v.name, v.pos, v.type) for v in self.vertices]
        edges = [(e[0], e[2]) for e in self.w_edges]
        return Graph(vertices, edges)

    def draw_graph(self, output_file="graph.png", solution=None):
        def _get_color_for_type(vertex_type):
            if vertex_type == "vehicle":
                return "lightblue"
            elif vertex_type == "start":
                return "lightgreen"
            elif vertex_type == "destination":
                return "lightcoral"
            else:
                return "white"

        # Create a new directed graph
        dot = graphviz.Digraph(comment='Directed Graph', engine='neato')
        dot.attr(rankdir='LR')  # Left to right layout

        # Add vertices
        for vertex in self.vertices:
            # Create label with vertex information
            label = f"{vertex.name}\n({vertex.pos[0]:.1f}, {vertex.pos[1]:.1f})\n{
                vertex.type}"

            # Define node attributes based on vertex type
            attrs = {
                'label': label,
                'shape': 'box',
                'style': 'rounded,filled',
                'fillcolor': _get_color_for_type(vertex.type),
                'pos': f"{vertex.pos[0]},{vertex.pos[1]}!"  # Set position
            }

            dot.node(vertex.name, **attrs)

        # Add edges
        if not solution:
            for (v1, w, v2) in self.w_edges:
                dot.edge(v1.name, v2.name, label=f"{w:.1f}")

        # Highlight solution
        if solution:
            for car_name, path in solution.car_paths.items():
                pos = path.current_position
                for (customer, time, goal) in path.moves:
                    dot.edge(f"{pos.name}", f"{customer.name}")
                    dot.edge(f"{customer.name}", f"{goal.name}",
                             label=f"Car {car_name} -> Customer: {customer.name} (Time {time:.1f})")
                    pos = goal

        # Save the graph
        try:
            dot.render(output_file.rsplit('.', 1)[
                       0], format='png', cleanup=True)
            print(f"Graph has been saved to {output_file}")
        except Exception as e:
            print(f"Error saving graph: {e}")

    def __str__(self):
        vstring = ""
        for v in self.vertices:
            vstring += f"{v}\n"

        estring = ""
        for (v1, w, v2) in self.w_edges:
            estring += f"{v1} -- {w} -- {v2}\n"

        return f"Vertices:\n{vstring}\nEdges:\n{estring}"


########################################################################################
# Create a graph from a scenario
########################################################################################

def distance(p1: Vertex, p2: Vertex):
    return ((p1.pos[0] - p2.pos[0])**2 + (p1.pos[1] - p2.pos[1])**2)**0.5

def scenario_to_graph(scenario):
    vertices = []
    edges = []

    # Add nodes and edges for single customers (start, dest, way)
    for customer in scenario['customers']:
        start_vertex = Vertex(
            name=customer['id'],
            pos=(customer['coordX'], customer['coordY']),
            type='start'
        )

        dest_vertex = Vertex(
            name=customer['id'],
            pos=(customer['destinationX'],customer['destinationY']),
            type='destination'
        )

        vertices.append(start_vertex)
        vertices.append(dest_vertex)

        edges.append((
            start_vertex,
            distance(start_vertex, dest_vertex),
            dest_vertex,
        ))

    # Add nodes for vehicle starting points
    for vehicle in scenario['vehicles']:
        vertices.append(Vertex(
            name=vehicle['id'],
            pos=(vehicle['coordX'], vehicle['coordY']),
            type='vehicle'
        ))

    # Add edges from vehicle starting points to customer starting points
    for vehicle_node in filter(lambda node: node['type'] == 'vehicle', vertices):
        for start_vertex in filter(lambda node: node['type'] == 'start', vertices):
            edges.append((
                vehicle_node,
                distance(vehicle_node, start_vertex),
                start_vertex
            ))

    # Add edges from customer destination points to customer starting points (exclude same customer)
    for dest_vertex in filter(lambda node: node['type'] == 'destination', vertices):
        for start_vertex in filter(lambda node: node['type'] == 'start' and node['id'] != dest_vertex['id'], vertices):
            edges.append((
                dest_vertex,
                distance(dest_vertex, start_vertex),
                start_vertex,
            ))