import asyncio
import click
from device_simulator import DeviceSimulator

@click.command()
@click.option('--devices', default=3, help='Number of virtual devices to simulate.')
@click.option('--corrupt', default=0.2, help='Probability of payload corruption.')
@click.option('--duplicate', default=0.1, help='Probability of duplication.')
@click.option('--latency', default=0, help='Artificial latency in ms.')
@click.option('--broker', default='broker.hivemq.com', help='MQTT broker host.')
@click.option('--port', default=1883, help='MQTT broker port.')
def main(devices, corrupt, duplicate, latency, broker, port):
    print("=" * 50)
    print(">>> CHAOTIC FLEET: EDGE SIMULATOR INITIALIZED")
    print(f">>> Devices: {devices} | Corrupt Rate: {corrupt*100}% | Duplicate Rate: {duplicate*100}%")
    print("=" * 50)

    chaos_config = {
        "corrupt_rate": corrupt,
        "duplicate_rate": duplicate,
        "latency_ms": latency
    }

    async def run_fleet():
        simulators = [
            DeviceSimulator(
                device_id=f"VAN_UNIT_{i:03d}",
                broker_host=broker,
                broker_port=port,
                chaos_config=chaos_config
            ) for i in range(1, devices + 1)
        ]
        await asyncio.gather(*(sim.run(interval_seconds=2.0) for sim in simulators))

    try:
        asyncio.run(run_fleet())
    except KeyboardInterrupt:
        print("\nSimulator stopped safely by user.")

if __name__ == '__main__':
    main()