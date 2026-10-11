import json
from validator import validate_payload
from deduplicator import is_duplicate_message

from config import EVENT_HUB_CONNECTION_STRING

# Use EVENT_HUB_CONNECTION_STRING to initialize your Event Hub / Service Bus consumer client

def process_telemetry_event(raw_event_body: str):
    """
    Core consumer function triggered by incoming stream.
    Routes data to Primary DB, DLQ, or drops duplicates.
    """
    try:
        data = json.loads(raw_event_body)
    except json.JSONDecodeError:
        print("❌ [POISON PILL] Non-JSON payload received -> Route to Dead Letter Queue")
        return

    # 1. Check for Duplicate Messages
    msg_id = data.get("message_id")
    if is_duplicate_message(msg_id):
        print(f"⚠️ [DUPLICATE DROPPED] Message ID '{msg_id}' already processed.")
        return

    # 2. Validate Schema Contract
    is_valid, reason = validate_payload(data)
    if not is_valid:
        print(f"❌ [SCHEMA CORRUPTED] Device {data.get('device_id', 'UNKNOWN')} -> Reason: {reason} -> Route to Dead Letter Queue")
        return

    # 3. Valid & Unique Payload
    print(f"✅ [VALID STORED] Device {data['device_id']} | Msg {msg_id} -> Route to Primary Database")


# Local test run
if __name__ == "__main__":
    print("--- Testing Consumer Processing Pipeline Locally ---\n")
    
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

    process_telemetry_event(valid_payload)      # Expected: VALID STORED
    process_telemetry_event(valid_payload)      # Expected: DUPLICATE DROPPED
    process_telemetry_event(corrupted_payload)  # Expected: SCHEMA CORRUPTED