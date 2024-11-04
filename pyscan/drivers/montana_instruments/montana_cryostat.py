from ..instrument_driver import InstrumentDriver
import socket


class MontanaCryostat(InstrumentDriver):

    def __init__(self, ip, port=7773):

        self.ip = ip
        self.port = port

        try:
            self.instrument = socket.create_connection((ip, port), timeout=10)
        except Exception as err:
            print("CryoComm:Connection error - {}".format(err))
            raise err

        self.instrument.settimeout(5)

    def __send(self, message):
        "CryoComm - Send a message to the Cryostation"

        total_sent = 0

        # Prepend the message length to the message.
        message = str(len(message)).zfill(2) + message

        while total_sent < len(message):
            try:
                sent = self.instrument.send(message[total_sent:].encode())
            except Exception as err:
                print("CryoComm:Send communication error - {}".format(err))
                raise err

            # If sent is zero, there is a communication issue
            if sent == 0:
                raise RuntimeError("CryoComm:Cryostation connection lost on send")
            total_sent = total_sent + sent

    def __receive(self):
        "CryoComm - Receive a message from the Cryostation"

        chunks = []
        received = 0

        try:
            message_length = int(self.instrument.recv(2).decode('UTF8'))
        except Exception as err:
            print("CryoComm:Receive message length communication error - {}".format(err))
            raise err

        # Read the message
        while received < message_length:
            try:
                chunk = self.instrument.recv(message_length - received)
            except Exception as err:
                print("CryoComm:Receive communication error - {}".format(err))
                raise err

            # If an empty chunk is read, there is a communication issue
            if chunk == '':
                raise RuntimeError("CryoComm:Cryostation connection lost on receive")
            chunks.append(chunk)
            received += len(chunk)

        return ''.join([x.decode('UTF8') for x in chunks])

    def query(self, message):

        self.__send(message)
        return self.__receive()

    @property
    def platform_temperature(self):
        self._platform_temperature = float(self.query('GPT'))
        return self._platform_temperature

    @platform_temperature.setter
    def platform_temperature(self, new_value):
        response = self.query("STSP" + str(new_value))
        if response.startswith('OK'):
            self._platform_temperature = new_value
        else:
            raise Exception('Failed to set target temperature')
