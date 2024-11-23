import dataclasses
import requests
from datatypes import *


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field


class ScenarioRunner:
    def __init__(self, config):
        self.config = config
        self.backend_url = config['backend_url']

    def get_scenario(self, scenarioID) -> Scenario:
        response = requests.get(
            f'{self.backend_url}/Scenarios/get_scenario/{scenarioID}').json()
        return dataclass_from_dict(Scenario, response)

    def update_scenario(self, scenarioID, data) -> UpdateScenarioResponse:
        response = requests.put(
            f'{self.backend_url}/Scenarios/{scenarioID}', json=data).json()
        return dataclass_from_dict(UpdateScenarioResponse, response)

    def initialize_scenario(self, scenarioID) -> InitializeScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Scenarios/initialize_scenario/{scenarioID}').json()
        return dataclass_from_dict(InitializeScenarioResponse, response)

    def initialize_scenario(self, body) -> InitializeScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Scenarios/initialize_scenario', json=body).json()
        return dataclass_from_dict(InitializeScenarioResponse, response)

    def launch_scenario(self, scenarioID, speed=0.2) -> LaunchScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Runner/launch_scenario/{scenarioID}').json()
        return dataclass_from_dict(LaunchScenarioResponse, response)
