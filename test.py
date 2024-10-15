import requests
import db

url = "http://172.31.254.55:8080/automation"
data = {"username": "dimaserang", "quota": 11.56, "user": "system"}

response = requests.patch(url, json=data)