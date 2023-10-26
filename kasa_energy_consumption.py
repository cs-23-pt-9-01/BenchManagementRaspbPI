import asyncio
from kasa import Discover
from datetime import datetime
import time
import pandas as pd
import threading
import _thread
import os


temp_list = [] #Bad practise to use globals, i know, dont @ me (MADS!!!!)

async def main(path):

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
            energy_info = device.emeter_realtime

            # Get current timestamp with milliseconds
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            temp_list.append((current_time, device.alias, addr, energy_info['power'], energy_info['voltage'], energy_info['current']))
            # Print energy metrics along with the timestamp
            print(f"[{current_time}] {device.alias} at {addr} - Power: {energy_info['power']} W, Voltage: {energy_info['voltage']} V, Current: {energy_info['current']} A")

        # Wait for a few seconds before fetching again
        await asyncio.sleep(0.1)


def socket_func():
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("starting socket")

    while True:
        message = socket.recv() #Wait for request
        print("Received request for review: %s" % message)

        socket.send(b"Denne kaffe er daarlig")

        _thread.interrupt_main()
        return

        
def exit_func():
    
    print("Saving data and exiting")
    csv_df = pd.DataFrame(data=temp_list, columns=['Date','device','address','watt','voltage','current'])
    csv_df.to_csv(path, index=False)
    exit()


def get_data_filepath():
    #Get current working dir, and split to get parent dir (to avoid saving data to the git local repo).
    cwd = os.getcwd().split("\\")
    parent_dir = os.path.join(*cwd[:-1])

    #Get current time and convert to unix format, then create filename with unix time
    timestamp = datetime.now().timetuple()
    unix_timestamp = int(time.mktime(timestamp))
    file = f"power_plug_{unix_timestamp}.csv"

    #return full path for file
    return os.path.join(cwd, file)


    
# Run the event loop
if __name__ == "__main__":
    
    path = get_data_filepath()
    
    try:
        x = threading.Thread(target=socket_func, daemon=True)
        x.start()

        asyncio.run(main(path))

    except KeyboardInterrupt:
        exit_func()
    
