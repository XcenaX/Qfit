import requests
import json

data = requests.post("http://127.0.0.1:8000/api/token/", data={"username": "test", "password": "12345"})
token = json.loads(data.text)["access"]
token_parameter = "Bearer " + token
print(token_parameter)
data = requests.get("http://127.0.0.1:8000/api/services/", headers={"Authorization": token_parameter})
print(data.text)