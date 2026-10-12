import argparse
import asyncio
from chaos_injector import ChaosInjector
from device_simulator import DeviceSimulator

async def main():
    parser = argparse.ArgumentParser(description="Chaotic Fleet MQTT Simulator")
    parser.add_argument("--devices", type=int, default=10, help="Number of virtual devices")
    parser.add_argument("--corrupt-rate", type=float, default=0.0, help="Fraction of corrupted payloads (0.0 to 1.0)")
    parser.add_argument("--duplicate-rate", type=float, default=0.0, help="Fraction of duplicate payloads (0.0 to 1.0)")
    parser.add_argument("--delay", type=int, default=0, help="Simulated network latency in milliseconds")
    parser.add_argument("--broker", type=str, default="localhost", help="MQTT Broker host")
    
    args = parser.parse_args()

    print(f"Starting Chaotic Fleet with {args.devices} virtual devices...")
    print(f"Chaos Config -> Corrupt: {args.corrupt_rate*100}%, Duplicate: {args.duplicate_rate*100}%, Delay: {args.delay}ms")

    chaos = ChaosInjector(
        corrupt_rate=args.corrupt_rate,
        duplicate_rate=args.duplicate_rate,
        delay_ms=args.delay
    )

    tasks = []
    for i in range(args.devices):
        device_id = f"SENSOR_{i+1:03d}"
        simulator = DeviceSimulator(device_id=device_id, broker_host=args.broker, chaos_config=chaos)
        tasks.append(simulator.run())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Chaos Simulator gracefully.")