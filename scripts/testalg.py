import math

from algorithm.graph import *

def distance(node1, node2):
    return math.sqrt((node2['coord_x'] - node1['coord_x']) ** 2 + (node2['coord_y'] - node1['coord_y']) ** 2)

def findBestOption(options):
    
    curbest = None
    curmin = 10000000
    
    for option in options:
        if (curbest is None or option["distance"] < curmin):
            curbest = option
            curmin = option["distance"]

    return curbest


class decisionGraph:
    
    graph: Graph
    L1: any
    L2: any

    def __init__(self, graph: Graph):
        
        self.graph = graph
        self.L1, self.L2 = self.initialize()
        #print(self.L1)
        #print(self.L2)

    def findNextMove(self):
        
        currentBest = {"vehicleID": "", "customerID": "", "distance": 1000000.0}
        #print("L1start\n", self.L1)
        #print("L2start\n", self.L2)
        if(self.L2 == []):
            return None
        for l1 in self.L1:
            
            currentWorkload = l1["currentWeight"]
            bestOption = findBestOption(l1["options"])

            if(bestOption is None):
                continue

            if (bestOption["distance"] + currentWorkload < currentBest["distance"]):
                currentBest = {"vehicleID": l1["vehicleID"], "customerID": 
                               bestOption["customerID"], "distance": bestOption["distance"] + currentWorkload}

        if(currentBest == {"vehicleID": "", "customerID": "", "distance": 1000000.0}):
            return None

        for l1 in self.L1:
            for option in l1["options"]:
                if option["customerID"] == currentBest["customerID"]:
                    l1["options"].remove(option)

            if(l1["vehicleID"] == currentBest["vehicleID"]):
                l1["currentWeight"] = currentBest["distance"]
                
                for opts in self.L2:
                    
                    if (opts["from"] == currentBest["customerID"]):
                        l1["options"] = opts["to"].copy()
                        #print("OPTS22222", opts["to"])
                        #print(l1["options"])
        

        for l2 in self.L2:
            for x in l2["to"]:
                if (x["customerID"] == currentBest["customerID"]):
                    l2["to"].remove(x)
        
        #print("CHOSEN TRIP: ", currentBest)
        #print("L1end\n", self.L1)
        #print("L2end\n", self.L2)
        return currentBest

    def returnAll(self):
        moves = []
        
        while(True):
            move = self.findNextMove()
            if(move is None):
                break
            else: 
                moves.append(move)

        print("Moves", moves)
        
        d = dict()
        for element in moves:
            if(not element["vehicleID"] in d):
                d[element["vehicleID"]] = []
            d[element["vehicleID"]].append(element["customerID"])    

        return d

             

    
    def initialize(self):

        vehicleNodes = list(filter(lambda node: node.type == "vehicle" , self.graph.vertices))
        startNodes = list(filter(lambda node: node.type == "start" , self.graph.vertices))
        destinationNodes = list(filter(lambda node: node.type == "destination" , self.graph.vertices))

        L1edges = []

        for vehicle in vehicleNodes: 
            cur = {"vehicleID": vehicle.name, "currentWeight": 0.0 ,"options": []}

            for customer in startNodes:
                a = filter(lambda x: (x[0].name == vehicle.name) & (x[2].name == customer.name), self.graph.w_edges)
                b = filter(lambda x: (x[0].name == customer.name) & (x[2].name == (customer.name + "-dest")), self.graph.w_edges)
               
                distance_car_to_start = list(a)[0][1]
                distance_start_to_end = list(b)[0][1]

                cur["options"].append({"customerID": customer.name, "distance": distance_car_to_start + distance_start_to_end})

            L1edges.append(cur)

        L2edges = []

        for customer1 in startNodes: 
            
            cur = {"from": customer1.name, "to": []}

            for customer2 in startNodes:

                if(customer1 == customer2):
                    continue

                a = filter(lambda x: (x[0].name == customer1.name + "-dest") & (x[2].name == customer2.name), self.graph.w_edges)
                b = filter(lambda x: (x[0].name == customer2.name) & (x[2].name == customer2.name + "-dest"), self.graph.w_edges)
                
                distance_from_to = list(a)[0][1]
                distance_to_end = list(b)[0][1]
                
                cur["to"].append({"customerID": customer2.name, "distance": distance_from_to + distance_to_end})

            L2edges.append(cur)

        return L1edges, L2edges