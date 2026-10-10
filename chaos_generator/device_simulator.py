import asyncio
import json
import random
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from chaos_injector import ChaosInjector

class DeviceSimulator:
    def __init__(self, device_id: str, broker_host: str, broker_port: int, chaos_config: dict):
        self.device_id = device_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=f"sim_client_{device_id}")
        self.injector = ChaosInjector(**chaos_config)
        self.seq_num = 0

    def connect(self):
        try:
            print(f"[{self.device_id}] Connecting to MQTT broker {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, keepalive=10)
            self.client.loop_start()
            print(f"[{self.device_id}] Connected successfully!")
        except Exception as e:
            print(f"[{self.device_id}] Connection error: {e}. Running simulation mode.")

    async def run(self, interval_seconds: float = 2.0):
        self.connect()
        print(f"[{self.device_id}] Started streaming telemetry loop...")
        
        try:
            while True:
                self.seq_num += 1
                raw_payload = {
                    "message_id": f"msg_{self.device_id}_{self.seq_num}_{random.randint(1000,9999)}",
                    "device_id": self.device_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "sequence_number": self.seq_num,
                    "telemetry": {
                        "temperature_c": round(random.uniform(20.0, 45.0), 2),
                        "vibration_hz": round(random.uniform(5.0, 25.0), 2)
                    },
                    "chaos_metadata": {
                        "is_corrupted": False,
                        "is_duplicate": False
                    }
                }

                processed_messages = self.injector.apply_chaos(raw_payload)

                for msg in processed_messages:
                    if self.injector.latency_ms > 0:
                        await asyncio.sleep(self.injector.latency_ms / 1000.0)
                    
                    topic = f"fleet/telemetry/{self.device_id}"
                    payload_str = json.dumps(msg)
                    try:
                        self.client.publish(topic, payload_str)
                    except:
                        pass
                    
                    print(f"[{self.device_id}] Published -> Corrupted: {msg['chaos_metadata']['is_corrupted']} | Duplicate: {msg['chaos_metadata']['is_duplicate']}")

                await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            self.client.loop_stop()
            self.client.disconnect()