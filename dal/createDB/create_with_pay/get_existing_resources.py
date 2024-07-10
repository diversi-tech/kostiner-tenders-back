import requests
from requests.auth import HTTPDigestAuth

def get_organization_id(org_name, public_key, private_key):
    url = "https://cloud.mongodb.com/api/atlas/v2/orgs"
    response = requests.get(url, auth=HTTPDigestAuth(public_key, private_key), headers={'Accept': 'application/vnd.atlas.2023-01-01+json'})
    if response.status_code == 200:
        orgs = response.json()["results"]
        for org in orgs:
            if org["name"] == org_name:
                return org["id"]
    return None

def get_project_id(project_name, org_id, public_key, private_key):
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/orgs/{org_id}/groups"
    response = requests.get(url, auth=HTTPDigestAuth(public_key, private_key))
    if response.status_code == 200:
        projects = response.json()["results"]
        for project in projects:
            if project["name"] == project_name:
                return project["id"]
    return None

def get_cluster_id(cluster_name, project_id, public_key, private_key):
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{project_id}/clusters/{cluster_name}"
    response = requests.get(url, auth=HTTPDigestAuth(public_key, private_key))
    if response.status_code == 200:
        cluster_info = response.json()
        mongo_uri = cluster_info['mongoURI']
        return cluster_info["id"], mongo_uri
    else:
        return None, None
