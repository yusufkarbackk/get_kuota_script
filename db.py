import requests


def update_kuota_request(nomor, quota):
    url = "http://localhost:8080/client"
    data = {"nomor": nomor, "quota": quota, "user": "system"}

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print("User updated successfully:\n")
        print(response.json())  # JSON response from the API
    else:
        print(f"Failed to update user. Status code: {response.status_code}\n")
        print(response.text)  # Detailed error message from the API
