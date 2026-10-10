from typing import Dict, Any, Tuple

def validate_payload(raw_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates incoming raw telemetry against schema contract using standard Python.
    Returns (True, "OK") if valid, or (False, error_reason) if malformed.
    """
    # 1. Required top-level keys
    required_keys = ["message_id", "device_id", "timestamp", "sequence_number", "telemetry", "chaos_metadata"]
    for key in required_keys:
        if key not in raw_data:
            return False, f"Missing required top-level key: '{key}'"
            
    # 2. Type checks for top-level metadata
    if not isinstance(raw_data["message_id"], str) or not raw_data["message_id"].strip():
        return False, "Field 'message_id' must be a non-empty string"
        
    if not isinstance(raw_data["device_id"], str) or not raw_data["device_id"].strip():
        return False, "Field 'device_id' must be a non-empty string"

    if not isinstance(raw_data["sequence_number"], int):
        return False, "Field 'sequence_number' must be an integer"

    # 3. Telemetry payload validation
    telemetry = raw_data.get("telemetry")
    if not isinstance(telemetry, dict):
        return False, "Field 'telemetry' must be a dictionary object"

    for metric_key in ["temperature_c", "vibration_hz"]:
        if metric_key not in telemetry:
            return False, f"Missing telemetry metric: '{metric_key}'"
            
        value = telemetry[metric_key]
        # Ensure temperature and vibration are valid numbers (float or int)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False, f"Telemetry metric '{metric_key}' must be a number, got {type(value).__name__}"

    return True, "Valid Payload"