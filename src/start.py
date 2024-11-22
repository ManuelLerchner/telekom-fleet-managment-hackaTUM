import requests
import json 

res = requests.get("http://localhost:8090/Scenarios/get_scenario/4846253b-8021-461c-93da-3fef8135a026")
response = json.loads(res.text)


print(response)