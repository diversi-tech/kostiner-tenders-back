import os
from dotenv import load_dotenv
from pymongo import MongoClient

# טעינת משתני הסביבה מהקובץ .env
load_dotenv()

# השגת משתני הסביבה
public_key = os.getenv("MONGO_ATLAS_PUBLIC_KEY")
private_key = os.getenv("MONGO_ATLAS_PRIVATE_KEY")
organization_name = os.getenv("ORGANIZATION_NAME")
project_name = os.getenv("PROJECT_NAME")
cluster_name = os.getenv("CLUSTER_NAME")
database_name = os.getenv("DATABASE_NAME")
collection_name = os.getenv("COLLECTION_NAME")
cloud_provider = os.getenv("MONGO_ATLAS_CLOUD_PROVIDER")  # ענן שבו ייצור ה-Cluster, לדוגמה "AWS" או "GCP"
instance_size_name = os.getenv("INSTANCE_SIZE_NAME")
region_name = os.getenv("REGION_NAME")

# בדיקת תקינות משתני הסביבה הנדרשים
required_env_vars = [
    public_key, private_key, organization_name, project_name, cluster_name, database_name, collection_name
]

if not all(required_env_vars):
    raise ValueError("One or more required environment variables are not set")

# יבוא של הפונקציות הקיימות שלך
from CreateDB.create_with_pay.create_organization import create_organization
from CreateDB.create_with_pay.create_project import create_project
from CreateDB.create_with_pay.create_cluster import create_cluster
from CreateDB.create_with_pay.create_database import create_database
from CreateDB.create_with_pay.create_collection import create_collection
from get_existing_resources import get_organization_id, get_project_id, get_cluster_id

# פונקציה לבדיקה אם ה-DB וה-COLLECTION כבר קיימים
def check_database_and_collection_existence(mongo_uri, database_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[database_name]
    if collection_name in db.list_collection_names():
        print(f"Collection '{collection_name}' already exists in database '{database_name}'.")
        return True
    else:
        return False

# פונקציה מרכזית לניהול כל התהליך
org_payment = {
    "payment": {
        "billingStartDate": "2024-07-01",
        "billingFrequencyMonths": 1,
        "currency": "USD",
        "invoicingEnabled": False
    }
}
def main():
    # בדיקת קיום ארגון
    org_id = get_organization_id(organization_name, public_key, private_key)
    if not org_id:
        org_id = create_organization(organization_name,public_key, private_key)
        if not org_id:
            print(f"Failed to create or retrieve organization '{organization_name}'")
            return

    # בדיקת קיום פרויקט
    project_id = get_project_id(project_name, org_id, public_key, private_key)
    if not project_id:
        project_id = create_project(org_id, project_name, public_key, private_key)
        if not project_id:
            print(f"Failed to create or retrieve project '{project_name}'")
            return

    # בדיקת קיום Cluster
    cluster_id, mongo_uri = get_cluster_id(cluster_name, project_id, public_key, private_key)
    if not cluster_id:
        cluster_id, mongo_uri = create_cluster(cluster_name, project_id, public_key, private_key, region_name)
        #cluster_id, mongo_uri = create_cluster(cluster_name, project_id, public_key, private_key, cloud_provider, instance_size_name, region_name)
        if not cluster_id:
            print(f"Failed to create or retrieve cluster '{cluster_name}'")
            return

    # התחברות ויצירת Database ו-Collection אם לא קיימים
    if not check_database_and_collection_existence(mongo_uri, database_name, collection_name):
        client = MongoClient(mongo_uri)
        db = create_database(client, database_name)
        create_collection(db, collection_name)
        print(f"Database '{database_name}' and collection '{collection_name}' created successfully.")
    else:
        print(f"Database '{database_name}' and collection '{collection_name}' already exist.")

if __name__ == "__main__":
    main()
