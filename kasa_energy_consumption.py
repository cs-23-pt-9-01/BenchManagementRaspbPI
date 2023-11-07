import asyncio
from kasa import Discover
from datetime import datetime
import csv
import time

async def main():
    # Discover Kasa devices on the local network
    devices = await Discover.discover()

    # Filter out devices that don't support energy monitoring
    energy_devices = {addr: dev for addr, dev in devices.items() if dev.has_emeter}

    # If no energy monitoring devices are found, exit
    if not energy_devices:
        print("No energy monitoring devices found.")
        return

    # Create or open a CSV file for writing
    with open("energy_measurements.csv", "w", newline='') as csvfile:
        fieldnames = ["timestamp", "device_alias", "address", "power_W", "voltage_V", "current_A"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header to the CSV
        writer.writeheader()

        while True:
            for addr, device in energy_devices.items():
                # Update device state (this also fetches the latest energy readings)
                await device.update()

                # Retrieve energy metrics
                energy_info = device.emeter_realtime

                # Get current timestamp with milliseconds
                #current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                current_time = time.time()
                # Write energy metrics along with the timestamp to CSV
                writer.writerow({
                    "timestamp": current_time,
                    "device_alias": device.alias,
                    "address": addr,
                    "power_W": energy_info['power'],
                    "voltage_V": energy_info['voltage'],
                    "current_A": energy_info['current']
                })

                # Optional: print to console
                print(f"[{current_time}] {device.alias} at {addr} - Power: {energy_info['power']} W, Voltage: {energy_info['voltage']} V, Current: {energy_info['current']} A")

            # Wait for a few seconds before fetching again
            await asyncio.sleep(1)


# Finds monitoring devices
async def find_devices():
    devices = await Discover.discover()

    # Filter out devices that don't support energy monitoring
    energy_devices = {addr: dev for addr, dev in devices.items() if dev.has_emeter}

    # If no energy monitoring devices are found, exit
    if not energy_devices:
        raise Exception("No monitoring devices found.")
    
    return energy_devices
    
async def measure(energy_devices, filename):
    """
    function for taking a single measurement

    :param energy_devices are the devices from find_devices
    :param filename is the name of the file written to
    """
    with open(filename, "a", newline='') as csvfile:
        fieldnames = ["timestamp", "device_alias", "address", "power_W", "voltage_V", "current_A"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            # Write the header to the CSV
            writer.writeheader()

        for addr, device in energy_devices.items():
                # Update device state (this also fetches the latest energy readings)
                await device.update()

                # Retrieve energy metrics
                energy_info = device.emeter_realtime

                # Get current timestamp with milliseconds
                current_time = time.time()
                
                # Write energy metrics along with the timestamp to CSV
                writer.writerow({
                    "timestamp": current_time,
                    "device_alias": device.alias,
                    "address": addr,
                    "power_W": energy_info['power'],
                    "voltage_V": energy_info['voltage'],
                    "current_A": energy_info['current']
                })

                # Optional: print to console
                print(f"[{current_time}] {device.alias} at {addr} - Power: {energy_info['power']} W, Voltage: {energy_info['voltage']} V, Current: {energy_info['current']} A")


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
