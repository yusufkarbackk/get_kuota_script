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

def insert_new_client(username, quota, nomor, profile_path, company, site, chrome_profile):
    url = "http://172.31.254.55:8080/automation/store"
    data = {"username": username, 
            "quota": quota, 
            "nomor": nomor,
            "profile_path":profile_path,
            "company": company,
            "site": site,
            "chrome_profile": chrome_profile
            }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Client updated successfully:\n")
        print(response.json())  # JSON response from the API
    else:
        print(f"Failed to update user. Status code: {response.status_code}\n")
        print(response.text)  # Detailed error message from the API
