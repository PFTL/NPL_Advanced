from pftl.controller.analog_daq import AnalogDAQ


class ModelDAQ:
    def __init__(self, port):
        self.port = port
        self._driver = AnalogDAQ(port)
        self._driver.initialize()

    def set_voltage(self, channel, voltage):
        """ Voltage should be in volts.
        """
        voltage_bits = int(voltage/3.3*(2**12-1))
        self._driver.set_value(channel, voltage_bits)

    def read_voltage(self, channel):
        """ Output is in volts
        """
        voltage_bits = int(self._driver.read_value(channel))
        return voltage_bits*3.3/(2**12-1)

    def finalize(self):
        self._driver.set_value(0, 0)
        self._driver.set_value(1, 0)
        self._driver.close()

