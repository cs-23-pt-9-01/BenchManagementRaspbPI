import asyncio
from kasa import Discover
from datetime import datetime
import pandas as pd




async def main():

    temp_list = [] #Bad practise i know dont @ me

    
    # Discover Kasa devices on the local network
    devices = await Discover.discover()

    # Filter out devices that don't support energy monitoring
    energy_devices = {addr: dev for addr, dev in devices.items() if dev.has_emeter}
    

    # If no energy monitoring devices are found, exit
    if not energy_devices:
        print("No energy monitoring devices found.")
        return


    
    


    #For testing
    import time

    n_minutes = 1 #Minutes to run
    end_time = time.time() + (60 * n_minutes)
    #end_time = time.time() + 5

    try:
        while time.time() < end_time:
            for addr, device in energy_devices.items():
                # Update device state (this also fetches the latest energy readings)
                await device.update()

                # Retrieve energy metrics
                energy_info = device.emeter_realtime

                # Get current timestamp with milliseconds
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                temp_list.append((current_time, device.alias, addr, energy_info['power'], energy_info['voltage'], energy_info['current']))
                # Print energy metrics along with the timestamp
                print(f"[{current_time}] {device.alias} at {addr} - Power: {energy_info['power']} W, Voltage: {energy_info['voltage']} V, Current: {energy_info['current']} A")

            # Wait for a few seconds before fetching again
            await asyncio.sleep(0.1)

        csv_df = pd.DataFrame(data=temp_list, columns=['Date','device','address','watt','voltage','current'])
        csv_df.to_csv(r"C:\Users\Mads\Documents\GitHub\BenchManagementRaspbPI\Data\Kasa\test.csv", index=False)


    except KeyboardInterrupt:
        print("Saving data and exiting")

        csv_df = pd.DataFrame(data=temp_list, columns=['Date','device','address','watt','voltage','current'])
        csv_df.to_csv(r"C:\Users\Mads\Documents\GitHub\BenchManagementRaspbPI\Data\Kasa\test.csv", index=False)

        exit()
    


# Run the event loop
if __name__ == "__main__":
    
    asyncio.run(main())
    
