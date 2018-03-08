import zmq
import spidev
from pllboard import PllEvalBoard


port = "7777"

channel_dict = dict()

class Channel():
    def __init__(self, name, pll, spi_dev_pll, spi_cs_pll, amplitute_control=False, atten=None, 
                 spi_dev_atten=None, spi_cs_atten=None ):
        assert isinstance(pll, PllEvalBoard)
        self.name = name
        self.pll = pll
        self.amplitute_control = amplitute_control

        self.spi_pll = spidev.SpiDev()
        self.spi_pll.open(spi_dev_pll, spi_cs_pll)
        self.spi_pll.spi_pllspi.cshigh = False 
        self.spi_pll.max_speed_hz = 100000

        if amplitute_control:
            self.spi_atten = spidev.SpiDev()
            self.spi_atten.open(spi_dev_atten, spi_cs_atten)
            self.spi_atten.spi_pllspi.cshigh = False 
            self.spi_atten.max_speed_hz = 100000
        else:
            self.spi_atten = None

        self.atten = atten

    def channel_init(self):
        self.pll.program_init()
        
    def set_channel(self,data):
        assert isinstance(data, dict)
        print("setting channel: {0}".format(self.name))
        if "freq" in data.keys():
            freq = data["freq"]
            print( "frequency:", freq)
            self.pll.set_freq(freq)
            self.pll.program_freq(self.spi_pll)

        if "atten" in data.keys():
            print( "attenuation", data["atten"])
            
    def register_to_channel_dict(self):
        channel_dict[self.name] = self
    


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

Channel("test",None,None, None).register_to_channel_dict()

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


