import requests


def update_kuota_request(nomor, quota):
    url = "http://localhost:8080/automation"
    data = {"nomor": nomor, "quota": quota, "user": "system"}

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print("User updated successfully:\n")
        print(response.json())  # JSON response from the API
    else:
        print(f"Failed to update user. Status code: {response.status_code}\n")
        print(response.text)  # Detailed error message from the API


def insert_client(
    client, company, team_flag, nomor, kuota, chrome_profile, profile_path
):
    # determine status here from kuota parameter
    url = "http://localhost:8080/client"
    data = {
        "client": client,
        "company": company,
        "team_flag": team_flag,
        "nomor": nomor,
        "quota": kuota,
        "chrome_profile": chrome_profile,
        "profile_path": profile_path,
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Client inserted successfully:\n")
        # print(response.json())  # JSON response from the API
    else:
        print(f"Failed to insert client. Status code: {response.status_code}\n")
        print(response.text)  # Detailed error message from the API
