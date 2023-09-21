import asyncio
from kasa import Discover
from datetime import datetime

async def main():
    # Discover Kasa devices on the local network
    devices = await Discover.discover()

    # Filter out devices that don't support energy monitoring
    energy_devices = {addr: dev for addr, dev in devices.items() if dev.has_emeter}

    # If no energy monitoring devices are found, exit
    if not energy_devices:
        print("No energy monitoring devices found.")
        return

    while True:
        for addr, device in energy_devices.items():
            # Update device state (this also fetches the latest energy readings)
            await device.update()

            # Retrieve energy metrics
            energy_info = await device.emeter_realtime()

            # Get current timestamp with milliseconds
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            # Print energy metrics along with the timestamp
            print(f"[{current_time}] Device at {addr} (Alias: {device.alias}) - Power: {energy_info['power']} W, Voltage: {energy_info['voltage']} V, Current: {energy_info['current']} A")

        # Wait for a few seconds before fetching again
        await asyncio.sleep(0.5)

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
