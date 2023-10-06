import zmq

context = zmq.Context()


print("Connecting to KaffeReviewer")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


print("Sending request for review")
socket.send(b"Hvad synes du om denne kaffe?")


message = socket.recv()
print("Received reply: " + str(message))