import zmq
port = "7777"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)
data = [{
    "name":"test",
    "freq":123,
    "atten":456
    }]
socket.send_json(data)
print(socket.recv_string())