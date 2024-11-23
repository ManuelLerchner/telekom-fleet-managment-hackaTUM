from typing import TypedDict

import math as Math

def distance(node1, node2):
    return Math.sqrt((node2['coord_x'] - node1['coord_x']) ** 2 + (node2['coord_y'] - node1['coord_y']) ** 2)

class GraphNode(TypedDict, total=False):
    type: str       # Node type: 'start', 'destination', 'vehicle'
    id: str         # Customer ID or Vehicle ID
    coord_x: float
    coord_y: float

# Directed graph edge (from node1 to node2)
class GraphEdge(TypedDict, total=False):
    node1: GraphNode
    node2: GraphNode
    weight: float

class Graph:
    def __init__(self, scenario):
        self.nodes = []
        self.edges = []

        # Add nodes and edges for single customers (start, dest, way)
        for customer in scenario['customers']:
            start_node = GraphNode(
                type='start',
                id=customer['id'],
                coord_x=customer['coordX'],
                coord_y=customer['coordY']
            )

            dest_node = GraphNode(
                type='destination',
                id=customer['id'],
                coord_x=customer['destinationX'],
                coord_y=customer['destinationY']
            )

            self.nodes.append(start_node)
            self.nodes.append(dest_node)

            self.edges.append(GraphEdge(
                node1=start_node,
                node2=dest_node,
                weight=distance(start_node, dest_node)
            ))

        # Add nodes for vehicle starting points
        for vehicle in scenario['vehicles']:
            self.nodes.append(GraphNode(
                type='vehicle',
                id=vehicle['id'],
                coord_x=vehicle['coordX'],
                coord_y=vehicle['coordY']
            ))

        # Add edges from vehicle starting points to customer starting points
        for vehicle_node in filter(lambda node: node['type'] == 'vehicle', self.nodes):
            for start_node in filter(lambda node: node['type'] == 'start', self.nodes):
                self.edges.append(GraphEdge(
                    node1=vehicle_node,
                    node2=start_node,
                    weight=distance(vehicle_node, start_node)
                ))

        # Add edges from customer destination points to customer starting points (exclude same customer)
        for dest_node in filter(lambda node: node['type'] == 'destination', self.nodes):
            for start_node in filter(lambda node: node['type'] == 'start' and node['id'] != dest_node['id'], self.nodes):
                self.edges.append(GraphEdge(
                    node1=dest_node,
                    node2=start_node,
                    weight=distance(dest_node, start_node)
                ))

    def __str__(self):
        # Graph summary
        graph_summary = f"Graph Summary:\n- Nodes: {len(self.nodes)}\n- Edges: {len(self.edges)}\n"
        
        # Node list
        node_list = "Nodes:\n"
        for node in self.nodes:
            node_str = f"ID: {node.get('id', 'N/A')}, Type: {node['type']}, " \
                       f"Coordinates: ({node['coord_x']}, {node['coord_y']})"
            node_list += f"- {node_str}\n"
        
        # Edge list
        edge_list = "Edges:\n"
        for edge in self.edges:
            edge_str = f"Node1: {edge['node1']['id']} ({edge['node1']['type']}), " \
                       f"Node2: {edge['node2']['id']} ({edge['node2']['type']}), " \
                       f"Weight: {edge['weight']:.2f}"
            edge_list += f"- {edge_str}\n"
        
        return graph_summary + node_list + edge_list
