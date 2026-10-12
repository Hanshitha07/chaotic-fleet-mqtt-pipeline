import random
import time
import json

class ChaosInjector:
    def __init__(self, corrupt_rate=0.0, duplicate_rate=0.0, delay_ms=0):
        self.corrupt_rate = corrupt_rate
        self.duplicate_rate = duplicate_rate
        self.delay_ms = delay_ms

    def process_payload(self, payload: dict):
        # 1. Inject Delay if specified
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)

        payloads_to_send = [payload]

        # 2. Inject Payload Corruption
        if random.random() < self.corrupt_rate:
            # Corrupt the payload by removing a required field or messing up data types
            if "message_id" in payload:
                del payload["message_id"] # Missing mandatory field -> triggers DLQ
            payload["telemetry"]["temperature_c"] = "INVALID_DATA"

        # 3. Inject Duplication
        if random.random() < self.duplicate_rate:
            # Append a duplicate packet to test deduplication cache
            payloads_to_send.append(payload.copy())

        return payloads_to_send