import requests


def update_kuota_request(username, quota):
    url = "http://172.31.254.55:8080/automation"
    data = {"username": username, "quota": quota, "user": "system"}

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print("Client updated successfully:\n")
        print(response.json())  # JSON response from the API
    else:
        print(f"Failed to update user. Status code: {response.status_code}\n")
        print(response.text)  # Detailed error message from the API