import requests
from requests.auth import HTTPDigestAuth

def create_project(org_id, project_name, public_key, private_key):
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "orgId": org_id,
        "name": project_name
    }
    response = requests.post(url, json=payload, auth=HTTPDigestAuth(public_key, private_key), headers=headers)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Failed to create project: {response.status_code}")
        print(response.json())
        return None
