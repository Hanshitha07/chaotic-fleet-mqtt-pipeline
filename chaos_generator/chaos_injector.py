import random
import json

class ChaosInjector:
    def __init__(self, corrupt_rate=0.1, duplicate_rate=0.1, latency_ms=0):
        self.corrupt_rate = corrupt_rate
        self.duplicate_rate = duplicate_rate
        self.latency_ms = latency_ms

    def apply_chaos(self, payload: dict) -> list[dict]:
        messages_to_send = []
        
        # 1. Handle Payload Corruption
        if random.random() < self.corrupt_rate:
            payload["chaos_metadata"]["is_corrupted"] = True
            corruption_type = random.choice(["break_type", "remove_key"])
            if corruption_type == "break_type":
                payload["telemetry"]["temperature_c"] = "INVALID_STRING_VALUE"
            elif corruption_type == "remove_key":
                payload.pop("message_id", None)
        else:
            payload["chaos_metadata"]["is_corrupted"] = False

        messages_to_send.append(payload)

        # 2. Handle Message Duplication
        if random.random() < self.duplicate_rate and not payload.get("chaos_metadata", {}).get("is_corrupted"):
            duplicate_payload = payload.copy()
            duplicate_payload["chaos_metadata"]["is_duplicate"] = True
            messages_to_send.append(duplicate_payload)

        return messages_to_send