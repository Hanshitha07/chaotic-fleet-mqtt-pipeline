import json
from validator import validate_payload
from deduplicator import is_duplicate_message
from db_client import CosmosDBHandler
from dlq_client import DLQHandler

# Initialize database and DLQ handlers
db_handler = CosmosDBHandler()
dlq_handler = DLQHandler()

def process_telemetry_event(raw_event_body: str):
    """
    Core consumer function triggered by incoming stream.
    Routes data to Primary DB (Cosmos DB), DLQ (Service Bus), or drops duplicates.
    """
    # 1. Parse JSON
    try:
        data = json.loads(raw_event_body)
    except (json.JSONDecodeError, TypeError) as e:
        reason = f"Non-JSON or invalid string payload: {str(e)}"
        print("❌ [POISON PILL] Non-JSON payload received -> Routing to Dead Letter Queue")
        dlq_handler.send_to_dlq({"raw": str(raw_event_body)}, reason)
        return

    # 2. Check for Duplicate Messages (Idempotency Check)
    msg_id = data.get("message_id")
    if is_duplicate_message(msg_id):
        print(f"⚠️ [DUPLICATE DROPPED] Message ID '{msg_id}' already processed.")
        return

    # 3. Validate Schema Contract
    is_valid, reason = validate_payload(data)
    if not is_valid:
        device_id = data.get('device_id', 'UNKNOWN')
        print(f"❌ [SCHEMA CORRUPTED] Device {device_id} -> Reason: {reason} -> Routing to Dead Letter Queue")
        dlq_handler.send_to_dlq(data, reason)
        return

    # 4. Valid & Unique Payload -> Store in Azure Cosmos DB
    print(f"✅ [VALID STORED] Device {data['device_id']} | Msg {msg_id} -> Persisting to Cosmos DB")
    db_handler.save_telemetry(data)


# Local test run
if __name__ == "__main__":
    print("--- Testing Consumer Processing Pipeline Locally with Azure Cloud Storage ---\n")
    
    valid_payload = json.dumps({
        "message_id": "msg_001", "device_id": "SIM_01", 
        "timestamp": "2026-10-10T15:00:00Z", "sequence_number": 1,
        "telemetry": {"temperature_c": 22.4, "vibration_hz": 10.1},
        "chaos_metadata": {"is_corrupted": False, "is_duplicate": False}
    })
    
    corrupted_payload = json.dumps({
        "message_id": "msg_002", "device_id": "SIM_02", 
        "timestamp": "2026-10-10T15:00:00Z", "sequence_number": 2,
        "telemetry": {"temperature_c": "INVALID_STRING"},
        "chaos_metadata": {"is_corrupted": True, "is_duplicate": False}
    })

    process_telemetry_event(valid_payload)      # Saves to Cosmos DB
    process_telemetry_event(valid_payload)      # Drops as duplicate
    process_telemetry_event(corrupted_payload)  # Routes to Service Bus DLQ