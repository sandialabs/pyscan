# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
import re
import time


class Stanford900(InstrumentDriver):
    '''
    Driver to control Stanford Research Systems SIM900 - 8 Slot Small
    Instrumentation Modules (SIM) System Mainframe.

    SIM modules can subclass from this class to directly connect
    to a single sim module.


    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument
    port : str or int
        port to connnect driver.  If no port is identified, the
        driver will communicate with the mainframe.

    Methods
    -------
    flush_buffers()
        Flush both output and input buffers of all SIM ports
    flush_buffer(port):
        Flush the buffer of a single port `port`
    ports_message_available()
        List porst with a message available
    port_message_available(port)
        Query whether port `port` has a message
    message_available_status()
        Returns the status bit of message available
    flush_output_queue()
        Flushes the output queue
    sim_reset()
        Resets the SIM modules
    recover()
        Flush all buffers and resets port, or all sims
    setup_port(port)
    '''

    def __init__(self, instrument, port=None):

        self.instrument = instrument
        self.port = port
        self.module_id_string = None
        self._version = "0.1.0"

        # reset mainframe to default configuration (prevents conflicts between Matlab and Python)
        self.write('*RST')

        if self.port is None:
            # driver for sim900 mainframe device

            # transmit device clear to all ports
            self.sim_reset()
            # clear status bits for SIM928
            self.write('*CLS')

        else:
            # driver for sim port device

            # setup status communications and events
            self.write('FLOW {}, 0'.format(port))

            # use status byte to determine if a message is available
            # mask status bit 0 to show message available summary
            self.write('*STE 0,1')

            # mask port data pending status to determine if port has a message
            self.write('pdpe {},1'.format(self.port))

            # clear port input and output buffers
            self.flush_buffer()

            idn = self.query_port('*idn?')
            self.module_id_string = idn

        self.flush_output_queue()

    def flush_buffers(self):
        '''
        Flush both output and input buffers of all SIM ports
        '''

        self.write('FLSH')

    def flush_buffer(self, port=None):
        '''
        flush self.port buffer only

        Parameters
        ----------
        port : str or int
            Port number to use (self.port if port=None). Defaults to None.
        '''

        port = self.setup_port(port)
        self.write('FLSH {}'.format(port))

    def ports_message_available(self):
        '''
        List porst with a message available

        Returns
        -------
        list
            List of ports
        '''

        port_list = []

        # check if any messages are available
        if self.msg_avail_status():
            pdpr_status = int(self.query('pdpr?'))
            for i in range(9):
                if 2**i & pdpr_status:
                    port_list.append(i)

        return port_list

    def port_message_available(self, port=None):
        '''
        Parameters
        ----------
        port : str or int
            Port number to use (self.port if port=None). Defaults to None.

        Returns
        -------
        bool
            True or False representing whether a message is available at port or self.port
        '''

        port = self.setup_port(port)

        # read *stb? to clear the message available bit
        # if self.msg_avail_status():
        #     if int(self.query('pdpr? {}'.format(port))):
        #         return True

        # skip status byte check, and just check if there is a port msg
        if int(self.query('pdpr? {}'.format(port))):
            return True

        return False

    def message_available_status(self):
        '''
        Returns the status bit of message available

        Returns
        -------
        bool
            True or False if the message_avail bit (0) of the status byte is set.
        '''

        if int(self.query('*stb? 0')):
            return True

        return False

    def flush_output_queue(self):
        '''
        Flushes the output queue
        '''

        self.write('FLOQ')

    def sim_reset(self):
        '''
        Resets the SIM modules
        '''
        self.write('SRST')

    def recover(self):
        '''
        Flush input and output buffers for a single port self.port
        if self.port != None, otherwise flushes a single port
            '''

        # port = self.setup_port(port)

        if self.port:
            # flush port buffer
            self.flush_buffer()
            # reset port
            self.write('SRST {}'.format(self.port))
        else:
            self.sim_reset()
            self.flush_buffers()

    def setup_port(self, port):
        '''
        Port communications can be to default port (self.port) or to the
        specified port.

        Returns
        -------
        port number
        '''

        if port is None and self.port is None:
            raise Exception('no port identified')
        if port is None:
            port = self.port

        return port

    def write_port(self, command, port=None):
        '''
        Write a command to self.port.

        Parameters
        ----------
        command : str
            Command to execute
        port : str or int
            Port to write command to. Defaults to None.
        '''

        # writing numerous commands rapidly can overload the buffer - add a bit of time
        delay = 0.003

        port = self.setup_port(port)
        port_command = 'SNDT {}, "{}"'.format(port, command)
        self.write(port_command)
        time.sleep(delay)
        self.logger.debug('write_port: {}'.format(repr(port_command)))

    def wait_port_msg(self, port=None, timeout=3):
        '''Wait for a message from port until data is available or the timeout
        occurs

        Returns
        -------
        bool
            True when message is available, False otherwise
        '''

        port = self.setup_port(port)

        # wait until message is available or timeout
        delay = 0.005
        dt = 0
        done = False
        ts = time.time()
        if self.port_msg_avail(port):
            done = True
        while not done:
            time.sleep(delay)
            dt = time.time() - ts
            if self.port_msg_avail(port):
                done = True
            elif dt > timeout:
                self.logger.info('wait_port_msg: message timeout on port {}'.format(port))
                return False

        return True

    def read_port(self, port=None):
        '''Read message directly from the port input queue (input to SIM900).
        Port message is terminated with \r\n, and main queue with \n.  Message
        is complete when both terminators are sent.

        Parameters
        ----------
        port : str or int
            Port number to use (self.port if port=None). Defaults to None.

        '''

        port = self.setup_port(port)

        if not self.wait_port_msg(port):
            # timeout occurred - no message
            self.logger.warning('read_port, timeout waiting for '
                                'start message (port {})'.format(port))
            return False

        full_message = ''
        done = False
        while not done:
            # nbytes = int(self.query('NINP? {}'.format(port)))
            response = self.query('GETN? {}, {}'.format(port, 128))
            self.logger.debug('read_port: response={}'.format(repr(response)))
            message, message_complete = self.extract_message(response)
            full_message += message
            if message_complete:
                done = True
            else:
                if not self.wait_port_msg(port):
                    # timeout
                    done = True
                    self.logger.warning('read_port: timeout waiting to '
                                        'complete message (port {}'.format(port))

        self.logger.debug('read_port: port={} msg={}'.format(port, full_message))

        # with the complete response from the port, determine if multiple
        # messages were waiting
        message_list = full_message.split('\r\n')

        if message_list[0] == '':
            # this should not occur since a message was available
            self.logger.warning('port {}, no message available'.format(port))

        if len(message_list) == 1:
            return message_list[0]
        else:
            return message_list

    def query_port(self, command, port=None):
        '''Write a command to the port, and then read the response directly from
        the port.

        Parameters
        ----------
        command : str
            Command to write to the port
        port : str or int
            Port number to use (self.port if port=None). Defaults to None.

        Returns
        -------
        str
            Response
        '''

        port = self.setup_port(port)

        # flush buffer to prevent <LOG ... info from corrupting result (be sure to complete long tasks first)
        self.flush_buffer()

        self.write_port(command, port=port)

        return self.read_port(port=port)

    def extract_message(self, response):
        '''Message based communications are either message packets or
        definite-length arb blocks. Separate the message from the response.
        Note: SIM900 responses are ascii strings.

        Parameters
        ----------
        response :
            SIM900 instrument response

        Returns
        -------
        (message, message_complete)
            message is the extracted message from
            the port, and message_complete is true when it ends with "\r\n".
        '''

        # separate header (if it exists) and the message packet
        msg_match = re.match(r'MSG (\d),#3(\d\d\d)(.*)\n', response, re.DOTALL)
        arb_match = re.match(r'#3(\d\d\d)(.*)\n', response, re.DOTALL)
        if msg_match:
            # port_origin = int(msg_match[1])
            packet = msg_match[2]
            packet = msg_match[3]
        elif arb_match:
            # message_bytes = arb_match[1]
            packet = arb_match[2]
        else:
            self.logger.error('extract, unexpected response format: '
                              '{}'.format(repr(response)))
            raise Exception('unexpected response format')

        # message is complete when it ends with a terminator
        # note: this can fail if multiple msgs happend to break at \r\n
        packet_match = re.match(r'(.*)\r\n$', packet, re.DOTALL)
        if packet_match:
            message_complete = True
            message = packet_match[1]
        else:
            message_complete = False
            message = packet
            # edge case: message splits between \r\n (ideally handle with regex, but MPL adds this)
            if packet == '\n':
                message_complete = True
                message = ''

        self.logger.debug('extract: complete={}, {}'.format(message_complete, repr(packet)))

        return (message, message_complete)
