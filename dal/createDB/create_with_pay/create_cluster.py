import requests
from requests.auth import HTTPDigestAuth

def create_cluster(cluster_name, project_id, public_key, private_key, region_name):
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{project_id}/clusters"
    payload = {
        "name": cluster_name,
        "providerSettings": {
            "providerName": "AWS",
            "regionName": region_name,
            "instanceSizeName": "M0 Sandbox"
        },
        "clusterType": "SHARDED",  # סוג ה-Cluster הוא SHARDED למסלול M0
        "replicationSpecs": [
            {
                "numShards": 1,
                "regionsConfig": {
                    "US_EAST_1": {
                        "analyticsNodes": 0,
                        "electableNodes": 3,
                        "priority": 7,
                        "readOnlyNodes": 0
                    }
                },
                "zoneName": "Zone 1"
            }
        ],
        "diskSizeGB": 2,
        "backupEnabled": False
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url, auth=HTTPDigestAuth(public_key, private_key), headers=headers, json=payload)
    if response.status_code == 201:
        cluster_info = response.json()
        #mongo_uri = f"{cluster_info['connectionStrings']['standardSrv']}"
        mongo_uri = cluster_info['mongoURI']
        return cluster_info['id'], mongo_uri
    else:
        print(f"Failed to create cluster: {response.status_code}")
        print(response.json())
        return None, None

# # קריאה לפונקציה עם הפרמטרים המתאימים
# cluster_id, mongo_uri = create_cluster("DevCluster", "my_project_id", "my_public_key", "my_private_key", "US_EAST_1")
#
# if cluster_id and mongo_uri:
#     print(f"Cluster created successfully with ID: {cluster_id}")
#     print(f"MongoDB URI: {mongo_uri}")
# else:
#     print("Cluster creation failed.")

# import requests
# from requests.auth import HTTPDigestAuth
#
# def create_cluster(cluster_name, project_id, public_key, private_key, cloud_provider, instance_size_name, region_name):
#     url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{project_id}/clusters"
#     payload = {
#         "name": cluster_name,
#         "providerSettings": {
#             "providerName": cloud_provider,
#             "instanceSizeName": instance_size_name,
#             "regionName": region_name
#         },
#         "clusterType": "REPLICASET",
#         "replicationSpecs": [
#             {
#                 "numShards": 1,
#                 "regionsConfig": {
#                     region_name: {
#                         "analyticsNodes": 0,
#                         "electableNodes": 3,
#                         "priority": 7,
#                         "readOnlyNodes": 0
#                     }
#                 },
#                 "zoneName": "Zone 1"
#             }
#         ],
#         "diskSizeGB": 2,
#         "backupEnabled": False
#     }
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
#     response = requests.post(url, auth=HTTPDigestAuth(public_key, private_key), headers=headers, json=payload)
#     if response.status_code == 201:
#         cluster_info = response.json()
#         mongo_uri = f"mongodb+srv://{cluster_info['connectionStrings']['standardSrv']}"
#         return cluster_info['id'], mongo_uri
#     else:
#         print(f"Failed to create_with_pay cluster: {response.status_code}")
#         print(response.json())
#         return None, None

