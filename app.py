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
    
    try:
        await start_runner()
        return "<p>Started</p>"
    except Exception as e:
        print(e)
        return "<p>Failed to start check log</p>", 500
    

# endpoint for stopping measurement
@app.route("/stop")
def stop():
    global running
    if not running:
        return "<p>Not started, nothing to stop</p>"
    
    stop_runner()
    return "<p>Stopped</p>"

# starting measurement on a thread
async def start_runner():
    global running
    global stop_flag

    if running:
        raise Exception("start_runner called twice")
    
    running = True
    stop_flag = threading.Event()
    
    # finding devices
    devices = await kec.find_devices()

    # starting asyncio loop be used by measurement_loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # filename for measurement
    timestamp = time.time()
    filename = f"power_plug_{timestamp}.csv"

    # starting measurement
    measurement_loop(filename, loop, stop_flag, devices, 1)

def measurement_loop(filename, loop,stop_flag, devices, sec):
    """
    function for running a measurement periodically
    inpsired by https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval

    :param filename is the name of the file where the measurements are saved
    :param loop is an asyncio event loop, which is used for enabling threading and async io.
    :param stop_flag is a threading event, which is used to stop
    :param devices are devices from kasa_energy_consumption.find_devices()
    :param  sec is the time between measurements in seconds (only seconds since powerplug measuring interval is 1 second)
    """

    # function wrapper to be called by timer
    def func_wrapper():
        # stopping if flag is set
        if stop_flag.is_set():
            loop.close()
            return
        
        # starting timer for next measurement
        measurement_loop(filename, loop, stop_flag, devices, sec)

        # running measurement
        loop.run_until_complete(kec.measure(devices,filename))
    
    # starting timer, that calls func_wrapper for measurement
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# stopping measurement by setting stopper event
def stop_runner():
    global running
    global stop_flag
    stop_flag.set()
    running = False

if __name__ == '__main__':
    app.run(debug=False, host="192.168.0.5") # change ip to device ip