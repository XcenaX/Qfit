import requests
import json
#https://qrfit.herokuapp.com/api/token/
#https://qrfit.herokuapp.com/api/timers/
data = requests.post("http://127.0.0.1:8000/api/token/", data={"username": "XcenaX", "password": "Dagad582#"})
print(json.loads(data.text))
token = json.loads(data.text)["token"]
token_parameter = "Token " + token
print(token_parameter)
data = requests.get("http://127.0.0.1:8000/api/timers/", headers={"Authorization": token_parameter})
print(data.text)