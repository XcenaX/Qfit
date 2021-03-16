import requests
import json

data = requests.post("https://qrfit.herokuapp.com/api/token/", data={"username": "test", "password": "12345"})
print(data.text)
token = json.loads(data.text)["access"]
token_parameter = "Bearer " + token
print(token_parameter)
data = requests.get("https://qrfit.herokuapp.com/api/services/", headers={"Authorization": token_parameter})
print(data.text)