from time import sleep

from pyvisa import ResourceManager


rm = ResourceManager()
class AnalogDAQ:
    def __init__(self, port):
        self.port = port
        self.dev = None

    def initialize(self):
        self.dev = rm.open_resource(self.port)
        self.dev.write_termination = '\n'
        self.dev.read_termination = '\r\n'
        sleep(1)

    def idn(self):
        return self.dev.query('*IDN?')

    def set_value(self, channel, value):
        if channel not in (0, 1):
            raise ValueError('Channel should be 0 or 1')
        if value > 4095:
            raise ValueError('Value should be < 4095')

        command = f'OUT:CH{channel} {value}'
        return self.dev.query(command)

    def read_value(self, channel):
        command = f'MEAS:CH{channel}?'
        return self.dev.query(command)

    def finalize(self):
        self.dev.close()


if __name__ == "__main__":
    dev = AnalogDAQ('ASRL/dev/cu.usbmodem11101::INSTR')
    dev.initialize()
    print(dev.idn())
    dev.set_value(0, 4095)
    print(dev.read_value(0))
    dev.set_value(0, 0)
    print(dev.read_value(0))
    dev.finalize()

