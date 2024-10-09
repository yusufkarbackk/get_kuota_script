import requests


client = "sxtstock1"
password = "batiku232"
number = "081119026097"
chrome_profile = "52"
company = "sxtstock1"
team_flag = "bati"

profile_dir = (
    f"/Users/yusufkarback/Library/Application Support/Google/Chrome/profile-{client}"
)
data = {
    "client": client,
    "company": company,
    "team_flag": team_flag,
    "number": number,
    "quota": float(18.6),
    "chrome_profile": chrome_profile,
    "profile_path": profile_dir,
}
try:
    response = requests.post("http://localhost:8080/automation/store", json=data)

    # Checking if the request was successful
    if response.status_code == 200:
        print("Client inserted successfully:", response.json())
    else:
        print(f"Failed to insert client. Status code: {response.status_code}")
        print(f"Response content: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
