import requests


class ScenarioRunner:
    def __init__(self, config):
        self.config = config
        self.backend_url = config['backend_url']

    def get_scenario(self, scenarioID):
        response = requests.get(
            f'{self.backend_url}/Scenarios/get_scenario/{scenarioID}').json()
        return response

    def update_scenario(self, scenarioID, data):
        response = requests.put(
            f'{self.backend_url}/Scenarios/{scenarioID}', json=data)
        return response
