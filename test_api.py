import requests
import json

data = requests.post("https://qrfit.herokuapp.com/api/token/", data={"username": "test", "password": "12345"})
token = json.loads(data.text)["token"]
token_parameter = "Token " + token
print(token_parameter)
data = requests.get("https://qrfit.herokuapp.com/api/services/", headers={"Authorization": token_parameter})
print(data.text)