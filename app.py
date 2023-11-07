from flask import Flask
import time
import threading
import kasa_energy_consumption as kec
import asyncio

app = Flask(__name__)

# event used to stop the measurement thread
stop_flag = None

# bool indicating measurement is running
running = False

# status endpoint
@app.route("/")
def status():
    global running
    if running:
        return "<p>Running</p>"
    else:
        return "<p>Not running</p>"

# endpoint for starting measurement
@app.route("/start")
async def start():
    global running
    if running:
        return "<p>Already started</p>"
    await start_runner()
    return "<p>Started</p>"

# endpoint for stopping measurement
@app.route("/stop")
def stop():
    stop_runner()
    return "<p>Stopped</p>"

# starting measurement on a thread
async def start_runner():
    global running
    global stop_flag

    if running:
        return
    running = True
    stop_flag = threading.Event()
    
    # finding devices and starting measurement
    devices = await kec.find_devices()
    threading.Thread(target=runMeasurement, args=(stop_flag,devices)).start()
    
# function for running measurement on a thread with asyncio
def runMeasurement(stop_flag,devices):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(kec.thread_measurement(stop_flag,devices))
    loop.close()

# stopping measurement by setting stopper event
def stop_runner():
    global running
    global stop_flag
    stop_flag.set()
    running = False

if __name__ == '__main__':
    app.run(debug=False)