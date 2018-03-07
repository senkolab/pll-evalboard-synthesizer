import zmq
#from adf41020 import ADF41020
#from adf4355_2 import ADF4355



port = "7777"

channel_dict = dict()

class Channel():
    def __init__(self, name, pll, spi_pll, amplitute_control=False, atten=None, spi_atten=None, ):
        self.name = name
        self.pll = pll
        self.amplitute_control = amplitute_control
        self.spi_pll = spi_pll
        self.atten = atten
        self.spi_atten = spi_atten

        
    def set_channel(self,data):
        assert isinstance(data, dict)

        if "freq" in data.keys():
            print( "frequency", data["freq"])
        if "atten" in data.keys():
            print( "attenuation", data["atten"])
            
    def register_to_channel_dict(self):
        channel_dict[self.name] = self
    


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

Channel("test",None,None).register_to_channel_dict()

print("Server is running at port {0}".format(port))
while True:
    datas = socket.recv_json()
    for data in datas:
        try:
            channel = channel_dict[data["name"]]
            print("setting channel: {0}".format(data["name"]))
        except KeyError:
            print("invalid channel name: {0}".format(data["name"]))
            continue
        channel.set_channel(data)
    socket.send_string("OK")


