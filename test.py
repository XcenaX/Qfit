import requests

url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://google.com"
data = {    
    "user_id": 2,
    "company_id": 1,
    "password": "12345",
    "service_id": 2,
}
r = requests.post(url, data=data)
print(r.text)