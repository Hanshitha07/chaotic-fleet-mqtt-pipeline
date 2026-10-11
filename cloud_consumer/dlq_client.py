import os
import json
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

SERVICEBUS_CONN_STR = os.getenv("SERVICEBUS_CONNECTION_STRING")
QUEUE_NAME = os.getenv("SERVICEBUS_QUEUE_NAME", "dlq-telemetry")

class DLQHandler:
    def __init__(self):
        self.conn_str = SERVICEBUS_CONN_STR
        self.queue_name = QUEUE_NAME

    def send_to_dlq(self, payload: dict, reason: str) -> bool:
        """Sends corrupted or invalid payloads to Azure Service Bus DLQ."""
        if not self.conn_str:
            print("⚠️ Service Bus connection string missing. Simulating DLQ routing...")
            return False

        try:
            dlq_package = {
                "poison_reason": reason,
                "raw_payload": payload
            }
            
            with ServiceBusClient.from_connection_string(self.conn_str) as client:
                with client.get_queue_sender(queue_name=self.queue_name) as sender:
                    message = ServiceBusMessage(json.dumps(dlq_package))
                    sender.send_messages(message)
                    print(f"🚨 [Dead Letter Queue] Quarantined poison payload into '{self.queue_name}'")
                    return True
        except Exception as e:
            print(f"❌ [Dead Letter Queue] Failed to push to Service Bus: {e}")
            return False