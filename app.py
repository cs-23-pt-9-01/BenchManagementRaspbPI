from flask import Flask
import time
import threading
import kasa_energy_consumption as kec

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

# measurement function
def kasa(flag):
    while not flag.is_set():
        print("measureing")
        time.sleep(1)

# starting measurement in thread
async def start_runner():
    global running
    global stop_flag

    if running:
        return
    running = True
    stop_flag = threading.Event()
    
    devices = await kec.find_devices()
    threading.Thread(target=kec.thread_measurement, args=(stop_flag,devices)).start()

# stopping measurement by setting stopper event
def stop_runner():
    global running
    global stop_flag
    stop_flag.set()
    running = False

if __name__ == '__main__':
    app.run(debug=False)