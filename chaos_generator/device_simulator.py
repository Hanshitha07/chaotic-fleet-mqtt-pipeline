import asyncio
import json
import random
import uuid
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from chaos_injector import ChaosInjector

class DeviceSimulator:
    def __init__(self, device_id, broker_host="broker.hivemq.com", broker_port=1883, chaos_config=None):
        self.device_id = device_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.chaos = chaos_config or ChaosInjector()
        self.seq_num = 0

    async def run(self):
        client = mqtt.Client(client_id=f"sim_device_{self.device_id}_{uuid.uuid4().hex[:4]}")
        try:
            client.connect(self.broker_host, self.broker_port, 60)
            client.loop_start()
            print(f"[{self.device_id}] Connected to MQTT broker at {self.broker_host}")
        except Exception as e:
            print(f"[{self.device_id}] Failed to connect to MQTT broker: {e}")
            return

        while True:
            self.seq_num += 1
            raw_payload = {
                "message_id": f"msg_{uuid.uuid4().hex[:8]}",
                "device_id": self.device_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "sequence_number": self.seq_num,
                "telemetry": {
                    "temperature_c": round(random.uniform(20.0, 35.0), 2),
                    "vibration_hz": round(random.uniform(5.0, 15.0), 2)
                },
                "chaos_metadata": {
                    "is_corrupted": False,
                    "is_duplicate": False
                }
            }

            # Apply chaos rules
            final_payloads = self.chaos.process_payload(raw_payload)

            for p in final_payloads:
                client.publish("iot/telemetry", json.dumps(p))
                print(f"[{self.device_id}] Published seq {self.seq_num}")

            await asyncio.sleep(1.0) # Send every 1 second