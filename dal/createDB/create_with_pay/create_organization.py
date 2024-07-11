import requests
from requests.auth import HTTPDigestAuth
def create_organization(org_name, public_key, private_key):
    url = "https://cloud.mongodb.com/api/atlas/v1.0/orgs"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": org_name,
    }
    response = requests.post(url, json=payload, auth=HTTPDigestAuth(public_key, private_key), headers=headers)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Failed to create {org_name} organization: {response.status_code}\n")
        print(response.json())
        return None
