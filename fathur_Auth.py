import requests
import json

def request_token():
    # Define the URL and headers
    requesst_token_url = "https://103.18.134.70:5000/v3/auth/tokens"
    headers = {
        "Content-Type": "application/json"
    }

    # Define the payload for requesting token
    data =  {
        "auth":{
            "identity":{
                "methods":["password"],
                "password":{
                    "user":{
                        "name":"admin","domain":{"name":"Default"},"password":"kiclikKINI#131Z!1"
                        }
                    }
                },
            "scope":{
                "project":{"id":"6d0d5af6b3c84c9db82fe761d8187ff2"}
                }
            }
        }

    # Send the POST request for requesting token
    request_token_response = requests.post(requesst_token_url, headers=headers, data=json.dumps(data), verify=False)  # verify=False to skip SSL verification

    # Print the headers to extract the token
    # print("Status Code:", request_token_response.status_code)
    if request_token_response.status_code == 201:  # 201 indicates the token was created
        token = request_token_response.headers.get("X-Subject-Token")  # Token is returned in the headers
        print("Authentication Token:", token)
        return token
    else:
        print("Error:", request_token_response.text)

auth_token = request_token()

def shelve_power_off():
    # Define the URL and headers
    url = "https://103.18.134.70:8774/v2.1/servers/2dd105a2-9a9c-492d-b34c-f21800fb58a1/action"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": auth_token  # Replace with your actual token
    }

    # Define the body for shelving the VM
    data = {
        "shelve": None
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)  # Skip SSL verification for testing

    # Handle the response
    print("Status Code:", response.status_code)
    if response.status_code == 202:  # 202 Accepted indicates success
        print("The VM has been successfully shelved.")
    else:
        print("Error:", response.text)
        
shelve_power_off()
