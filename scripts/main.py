import dataclasses
from ScenarioRunner import ScenarioRunner
import json
import re

with open('config.json') as f:
    config = json.load(f)
    scenarioID = config['scenarioID']


def init_example_scenario(runner:  ScenarioRunner):
    with open('exampleScenario.json') as f:
        exampleScenario = json.load(f)
    scenario = runner.initialize_scenario(exampleScenario)


    if scenario['error'] is not None:
        print(scenario['error'])
        id = re.search(
            r"Scenario with ID (.+?) is already running", scenario['error']).group(1)

        scenario = runner.get_scenario(id)
        return scenario
    else:
        print(scenario.message)

        return scenario.scenario


def main():
    runner = ScenarioRunner(config)

    scenario = init_example_scenario(runner)

    print(json.dumps(dataclasses.asdict(scenario), indent=4))

    launch = runner.launch_scenario(scenario.id, speed=0.2)

    print(f"Launched scenario {launch.scenario_id} at {launch.startTime}")


if __name__ == "__main__":
    main()
