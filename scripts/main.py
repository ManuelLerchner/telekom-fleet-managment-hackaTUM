from ScenarioRunner import ScenarioRunner
from graph import Graph
from datetime import datetime

from time import sleep
import json
import re

with open('config.json') as f:
    config = json.load(f)
    scenarioID = config['scenarioID']


def init_example_scenario(filename: str, runner:  ScenarioRunner):
    with open('scenarios/'+filename) as f:
        exampleScenario = json.load(f)
    scenario = runner.initialize_scenario(exampleScenario)

    if 'error' in scenario:
        print(scenario['error'])
        id = re.search(
            r"Scenario with ID (.+?) is already running", scenario['error']).group(1)

        scenario = runner.get_scenario(id)
        return scenario
    else:
        print(scenario['message'])

        return scenario['scenario']


def show_progress(scenario):
    for vehicle in scenario['vehicles']:
        print(f"Vehicle {vehicle['id']} isAvailable {vehicle['isAvailable']}, remainingTravelTime {vehicle['remainingTravelTime']}, customerId {vehicle['customerId']}")

def show_scenario_results(scenario):
    print(f"Scenario '{scenario['id']}' completed")
    print(f"├── Start time: {scenario['startTime']}")
    print(f"├── End time: {scenario['endTime']}")
    print(f"└── Duration: {datetime.fromisoformat(scenario['endTime']) - datetime.fromisoformat(scenario['startTime'])}\n")
    for vehicle in scenario['vehicles']:
        print(f"Vehicle '{vehicle['id']}'")
        print(f"├── Number of trips: {vehicle['numberOfTrips']}")
        print(f"├── Distance travelled: {vehicle['distanceTravelled']}")
        print(f"└── Active time: {vehicle['activeTime']}\n")

def main():
    runner = ScenarioRunner(config)
    scenario = init_example_scenario('twoCarSixCustomers.json', runner)
    print(json.dumps(scenario, indent=4))

    graph = Graph(scenario)
    print(graph)

    # TODO Find optimal routes

    # Test route for 2 vehicles and 6 customers scenario
    # Cars: 
    #   0be5d3b3-7dc9-4344-9f22-fc2b188298f8 
    #   85d3f1da-2747-4e6c-970f-c07be28f2ea7
    # Customers: 
    #   bc2ea0fd-e77f-486c-a15e-da4b39701f02
    #   eced552d-e65a-481a-9f8b-2edd66639a5a
    #   fb85591f-43c0-446c-8dd4-6f3a2573946a
    #   3a1dca9f-e933-40d0-b730-d359b6fbc406
    #   bda663b9-f082-45bd-b64e-193d05e4375d
    #   af9d6c7c-9e04-4f03-8f45-8ece703d49bb
    route_list = {
        "0be5d3b3-7dc9-4344-9f22-fc2b188298f8": [
                "bc2ea0fd-e77f-486c-a15e-da4b39701f02",
                "eced552d-e65a-481a-9f8b-2edd66639a5a",
                "fb85591f-43c0-446c-8dd4-6f3a2573946a",
                "3a1dca9f-e933-40d0-b730-d359b6fbc406"
            ],
        "85d3f1da-2747-4e6c-970f-c07be28f2ea7": [
                "bda663b9-f082-45bd-b64e-193d05e4375d",
                "af9d6c7c-9e04-4f03-8f45-8ece703d49bb"
            ]
    }

    print(f"Optimal routes: {route_list}")

    launch = runner.launch_scenario(scenario['id'], speed=5)
    print(f"Launched scenario {launch['scenario_id']} at {launch['startTime']}")

    while(scenario['status'] != 'COMPLETED'):
        scenario = runner.get_scenario(launch['scenario_id'])
        show_progress(scenario)
        
        vehicle_updates = []
        for vehicle in scenario['vehicles']:
            if vehicle['isAvailable'] and vehicle['customerId'] is None and len(route_list[vehicle['id']]) > 0:
                vehicle_updates.append({
                    "id": vehicle['id'],
                    "customerId": route_list[vehicle['id']].pop(0)
                })

        if len(vehicle_updates) > 0:
            res = runner.update_scenario(launch['scenario_id'], {"vehicles": vehicle_updates})
            print(f"------->>> Updated {len(res['updatedVehicles'])} vehicles")
        
        sleep(0.5)

    print("Scenario completed")
    


if __name__ == "__main__":
    main()
