from ScenarioRunner import ScenarioRunner
import json


with open('config.json') as f:
    config = json.load(f)
    scenarioID = config['scenarioID']


def main():
    runner = ScenarioRunner(config)

    scenario = runner.get_scenario(scenarioID)

    print(json.dumps(scenario, indent=4))

    res = runner.update_scenario(scenarioID, {
        "vehicles": [
            {
                "id": "4b3f7259-6c10-4f94-9e31-d5693b61bc0f",
                "customerId": "62bb8ed7-4dcb-4ee8-8d30-fb57c2f40f85"
            }
        ]
    }
    )

    print(res)


if __name__ == "__main__":
    main()
