import dataclasses
import requests
from datatypes import *
from typing import TypedDict, Dict, Any
import json


class ScenarioRunner:
    def __init__(self, config: Config):
        self.config = config
        self.backend_url = config['backend_url']

    def get_scenario(self, scenario_id: str) -> Scenario:
        response = requests.get(
            f'{self.backend_url}/Scenarios/get_scenario/{scenario_id}'
        ).json()
        return response

    def update_scenario(self, scenario_id: str, data: UpdateScenario) -> UpdateScenarioResponse:
        response = requests.put(
            f'{self.backend_url}/Scenarios/update_scenario/{scenario_id}',
            json=data
        ).json()
        return response

    def initialize_scenario_by_id(self, scenario_id: str) -> InitializeScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Scenarios/initialize_scenario/{scenario_id}'
        ).json()
        return response

    def initialize_scenario(self, body: Dict[str, Any]) -> InitializeScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Scenarios/initialize_scenario',
            json=body
        ).json()
        return response

    def launch_scenario(self, scenario_id: str, speed: float = 0.2) -> LaunchScenarioResponse:
        response = requests.post(
            f'{self.backend_url}/Runner/launch_scenario/{scenario_id}?speed={speed}'
        ).json()
        return response
