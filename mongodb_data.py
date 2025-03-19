#collect data from mongodb

from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import paramiko
import pandas as pd

# SSH and MongoDB credentials
SSH_HOST = "34.227.15.111"  # Your MongoDB server
SSH_USERNAME = "ec2-user"
SSH_PRIVATE_KEY = r"C:\Users\rajesh.nagalingam\OneDrive - Oryx d.o.o\Documents\Script\RajeshOfficeLaptop.pem"  # Converted OpenSSH key

# Convert key if needed
private_key = paramiko.RSAKey(filename=SSH_PRIVATE_KEY)

MONGO_HOST = "127.0.0.1"  # Localhost since we're using an SSH tunnel
MONGO_PORT = 27017  # MongoDB port

# Establish SSH tunnel
with SSHTunnelForwarder(
    (SSH_HOST, 22),
    ssh_username=SSH_USERNAME,
    ssh_pkey=SSH_PRIVATE_KEY,
    remote_bind_address=('127.0.0.1', 27017)
) as tunnel:
    print("SSH Tunnel Established!")

    # Connect to MongoDB via SSH tunnel using provided URI
    MONGO_URI = f"mongodb://127.0.0.1:{tunnel.local_bind_port}/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.9"
    client = MongoClient(MONGO_URI)

    # Get all available databases
    databases = client.list_database_names()
    collection_name = "cycles"  # Target collection

    # Prepare list to store results
    data_list = []

    for db_name in databases:
        db = client[db_name]

        # Check if the collection exists in the current database
        if collection_name in db.list_collection_names():
            collection = db[collection_name]

            # Fetch documents sorted by _id in descending order
            cursor = collection.find({}, {"_id": 1, "created": 1}).sort("_id", -1)

            for doc in cursor:
                if "created" in doc:
                    data_list.append({"database_name": db_name, "created": doc["created"]})

    # Convert to DataFrame
    df = pd.DataFrame(data_list)

    # Save to CSV file
    output_file = "sorted_cycles_data_desc.csv"
    df.to_csv(output_file, index=False)

    print(f"Data saved to {output_file}")
