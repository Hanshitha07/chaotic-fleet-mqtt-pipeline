import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, exceptions

load_dotenv()

COSMOS_CONN_STR = os.getenv("COSMOS_DB_CONNECTION_STRING")
DATABASE_NAME = os.getenv("COSMOS_DB_NAME", "chaotic-fleet-db")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "processed-telemetry")

class CosmosDBHandler:
    def __init__(self):
        self.client = None
        self.container = None
        if COSMOS_CONN_STR:
            try:
                self.client = CosmosClient.from_connection_string(COSMOS_CONN_STR)
                database = self.client.get_database_client(DATABASE_NAME)
                self.container = database.get_container_client(CONTAINER_NAME)
                print("⚡ [Azure Cosmos DB] Connected successfully.")
            except Exception as e:
                print(f"⚠️ [Azure Cosmos DB] Connection notice: {e}")

    def save_telemetry(self, payload: dict) -> bool:
        """Saves clean, validated telemetry payload to Cosmos DB."""
        if not self.container:
            print("⚠️ Cosmos DB container not initialized. Simulating local save.")
            return True

        try:
            document = payload.copy()
            document["id"] = payload["message_id"]  # Cosmos DB requires an 'id' field
            
            # Map partition key if needed
            if "vehicle_id" not in document and "device_id" in document:
                document["vehicle_id"] = document["device_id"]
                
            self.container.create_item(body=document)
            print(f"💾 [Cosmos DB] Saved item successfully: {document['id']}")
            return True
        except exceptions.CosmosResourceExistsError:
            print(f"⚠️ [Cosmos DB] Duplicate item ID already in DB: {payload['message_id']}")
            return False
        except Exception as e:
            print(f"❌ [Cosmos DB] Write failed: {e}")
            return False