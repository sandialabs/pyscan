# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep, time

import numpy as np

from ..instrument_driver import InstrumentDriver


class OxfordIPS120(InstrumentDriver):
    """Class to control Oxford Instruments Intelligent Power Supply IPS120 Superconducting Magnet Power Supply

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`.new_instrument`)

    Attributes
    ----------
    (Properties)

    field: float
        Get/set target field sweep (blocking)
    current_rate: float
        Get/set rate for changing magnet current
    current_set_point: float
        Get/set set point for magnet current
    field_set_point: float
        Get/set set point for magnet field; range defined by attribute field_limit: [-8, 8]
    field_rate: float
        Get/set rate for changing magnet field; range defined by attribute field_rate_limit: [0, 0.2]

    (Read-only properties)

    output_current: read-only
        Get current in magnet power supply
    voltage: read-only
        Get voltage across leads
    measured_current: read-only
        Get measured current in leads
    output_field: read-only
        Get field from current in magnet power supply (not actual field if persistent)
    software_voltage_limit: read-only
        Get max voltage
    persistent_current: read-only
        Get current in magnet where heater was turned off
    trip_field: read-only
        Get field where last magnet quench occurred
    persistent_field: read-only
        Get field in magnet where heater was turned off
    switch_heater_current: read-only
        Get current in switch heater
    safe_current_limit_negative: read-only
        Get max negative current
    safe_current_limit_positive: read-only
        Get max positive current
    lead_resistance: read-only
        Get resistance
    magnet_inductance: read-only
        Get inductance
    firmware_version: read-only
        Get power supply model
    status_string: read-only

    (Write-only properties)

    remote_control: str
        Set local/remote to "local_locked", "remote_locked", "local_unlocked", "remote_unlocked"
    communications_protocol: str
        Set rate and set point precision to "normal", "extended"
    heater_control: str
        Set heater to "off", "on", "force"
    activity_control: str
        Set sweep activity to "hold", "to_set_point", "to_zero", "clamp"

    Methods
    -------
    heater()
        turn heater on/off and deal correctly with persistent mode
    print_state()
        summarize state of the magnet
    print_status()
        not implemented yet
    print_properties()
        not_implemented yet
    hold()
        activity_control with checks
    to_zero()
        activity_control with checks
    to_set_point()
        activity_control with checks
    clamp()
        activity_control with checks
    """

    def __init__(
        self,
        instrument,
        *,
        field_limit,
        field_rate_limit,
        field_to_current_ratio,
        debug=False,
    ):
        """
        OxfordIPS120 initilization requires keyword arguments:
            field_limit: maximum magnetic field (T)
            field_rate_limit: maximum sweep rate (T/min)
            field_to_current_ratio: constant to switch between field and current (T/A)
        """
        super().__init__(instrument, debug)

        self._version = "0.1.0"

        self.instrument.read_termination = "\r"
        self.instrument.write_termination = "\r"
        self.remote_control = "remote_unlocked"

        # make sure the buffer is empty:
        # read status byte by performing a serial poll
        # bit 1: byte available
        # bit 4: message available
        # bit 6: requesting service (reset after read)
        stb = self.instrument.read_stb()
        if not stb:
            stb = self.instrument.read_stb()
        if stb & 16:
            message = self.instrument.read()
            print(f"Message in buffer: {message}")

        # magnet specific settings
        self._field_limit = field_limit
        self._field_rate_limit = field_rate_limit
        self._field_to_current_ratio = field_to_current_ratio

        self.debug = debug
        self.initialize_properties()
        self.update_properties()

        self.check_field_to_current_ratio()

    def query(self, string, timeout=1):
        """
        Overload query for IPS120
        Read until status indicates full message is received.
        """
        # message = self.query(string)
        self.write(string)
        stb = self.instrument.read_stb()
        # wait for message
        i = 0
        start_time = time()
        while (time() - start_time) < timeout:
            while not (stb & 16):
                if self.debug:
                    if stb & 2:
                        print("byte available but not message")
                stb = self.instrument.read_stb()
                i += 1
            if self.debug:
                # typically i=4, time = 0.01
                print(f"needed to wait {i}; {time() - start_time} seconds")
            message = self.read()
            return message

        raise IPS120Error("IPS120 query Timeout")

    def check_field_to_current_ratio(self):
        """
        Compare safe_current_limit_positive to the field_limit
        """

        calculated_current_limit = self._field_limit / self._field_to_current_ratio
        # IPS120 has 4 dig accuracy in ratio and 2 dig accuracy in safe_current limits
        # we need to check the calculated current to tolerance of +- 0.01 A
        tol = 0.01
        safe_current = self.safe_current_limit_positive
        if (calculated_current_limit > safe_current - tol) and (
            calculated_current_limit < safe_current + tol
        ):

            return

        assert (
            False
        ), "field_limit and field_to_current_ratio ({}) not consistent with IPS120 safe_current ({})".format(
            calculated_current_limit, safe_current
        )

    def initialize_properties(self):
        """
        The IPS120 does not have traditional get/set parameters.  The control
        parameters are set using command.  Getting values is accomplished with
        either "examine status", X or "read parameter" R {}.
        """

        # control commands

        self.add_device_property(
            {
                "name": "field_set_point",
                "write_string": "$J{}",
                "query_string": "R8",
                "range": [-self._field_limit, self._field_limit],
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "field_rate",
                "write_string": "$T{}",
                "query_string": "R9",
                "range": [-self._field_rate_limit, self._field_rate_limit],
                "return_type": ips120_float,
            }
        )

        # TODO: fix all rounding issues related to T->A and precision
        self.add_device_property(
            {
                "name": "current_set_point",
                "write_string": "$I{}",
                "query_string": "R5",
                "range": [
                    np.round(-self._field_limit / self._field_to_current_ratio, 2),
                    np.round(self._field_limit / self._field_to_current_ratio, 2),
                ],
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "current_rate",
                "write_string": "$S{}",
                "query_string": "R6",
                "range": [
                    np.round(-self._field_rate_limit / self._field_to_current_ratio, 2),
                    np.round(self._field_rate_limit / self._field_to_current_ratio, 2),
                ],
                "return_type": ips120_float,
            }
        )

        # read-only properties

        self.add_device_property(
            {
                "name": "output_current",
                "query_string": "R0",
                "read_only": float,
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {"name": "voltage", "query_string": "R1", "return_type": ips120_float}
        )

        self.add_device_property(
            {
                "name": "measured_current",
                "query_string": "R2",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {"name": "output_field", "query_string": "R7", "return_type": ips120_float}
        )

        self.add_device_property(
            {
                "name": "software_voltage_limit",
                "query_string": "R15",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "persistent_current",
                "query_string": "R16",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "trip_field",  # mA
                "query_string": "R17",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "persistent_field",
                "query_string": "R18",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "switch_heater_current",
                "query_string": "R20",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "safe_current_limit_negative",
                "query_string": "R21",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "safe_current_limit_positive",
                "query_string": "R22",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "lead_resistance",
                "query_string": "R23",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {
                "name": "magnet_inductance",
                "query_string": "R24",
                "return_type": ips120_float,
            }
        )

        self.add_device_property(
            {"name": "firmware_version", "query_string": "V", "return_type": str}
        )

        self.add_device_property(
            {"name": "status_string", "query_string": "X", "return_type": str}
        )

        # write-only properties

        self.add_device_property(
            {
                "name": "remote_control",
                "write_string": "$C{}",
                "dict_values": {
                    "local_locked": 0,
                    "remote_locked": 1,
                    "local_unlocked": 2,
                    "remote_unlocked": 3,
                },
                "return_type": int,
            }
        )

        self.add_device_property(
            {
                "name": "communications_protocol",
                "write_string": "Q{}",  # no echo since this command clears output buffer
                "dict_values": {
                    "normal": 0,
                    "extended": 4,
                },  # do not allow switch to <CR><LF>
                "return_type": int,
            }
        )

        self.add_device_property(
            {
                "name": "heater_control",
                "write_string": "$H{}",
                "indexed_values": ["off", "on", "force"],
                "return_type": int,
            }
        )

        self.add_device_property(
            {
                "name": "activity_control",
                "write_string": "$A{}",
                "dict_values": {"hold": 0, "to_set_point": 1, "to_zero": 2, "clamp": 4},
                "return_type": int,
            }
        )

    def print_state(self):
        """
        Print operating state of the IPS120 power supply
        """
        status = self.status()
        value = ""
        if self.quench_status:
            value += "QUENCHED"
        if self.heater_status:
            value += "Heater on"
        else:
            value += "Heater off"
        value += "\n"
        if self.sweeping_status:
            value += "Field is changing"
        else:
            value += "At rest"
        if self.persistent_status:
            value += "\n"
            value += "Magnet is persistent"
            value += "\n"
            value += f"persistent_field = {self.get_persistent_field}"
        value += "\n"
        value += f"activity: {status.A_value()}"
        value += "\n"
        value += f"output_field = {self.output_field}"
        value += "\n"
        value += f"field_set_point = {self.field_set_point}"
        value += "\n"
        value += f"field_rate = {self.field_rate}"

        return value

    # TODO: implement status message
    def print_status(self):
        """
        Print current status of the IPS120 power supply
        """
        pass

    # TODO: combine hold(), to_set_point() and to_zero() into activity property
    def hold(self):
        if not self.remote_status:
            raise IPS120Error(
                "Control commands require the power supply to be in remote mode"
            )
        self.activity_control = "hold"

    def to_set_point(self):
        if not self.remote_status:
            raise IPS120Error(
                "Control commands require the power supply to be in remote mode"
            )
        self.activity_control = "to_set_point"

    def to_zero(self):
        if not self.remote_status:
            raise IPS120Error(
                "Control commands require the power supply to be in remote mode"
            )
        self.activity_control = "to_zero"

    # TODO: should be a property
    def heater(self, state):
        """
        Set the state of the heater.  Record the time when the heater was changed
        """

        if not self.remote_status:
            raise IPS120Error(
                "Control commands require the power supply to be in remote mode"
            )

        # TODO: deal with persistent magnet
        if self.persistent_status:
            raise IPS120Error(
                "take magnet out of persistent mode before changing heater"
            )

        if state == "on":
            if not self.heater_status:
                self.time_heater_toggle = datetime.now()
                self.heater_control = "on"
                sleep(30)
        elif state == "off":
            if self.heater_status:
                self.time_heater_toggle = datetime.now()
                self.heater_control = "off"
                sleep(30)
        else:
            print("State must be 'on' or 'off'")

    def remote(self, locked=False):
        if locked:
            self.remote_control = "remote_locked"
        else:
            self.remote_control = "remote_unlocked"

    def local(self, locked=False):
        if locked:
            self.remote_control = "local_locked"
        else:
            self.remote_control = "local_unlocked"

    @property
    def field(self):
        """
        TODO add settings dictionary with range to make this consistent with pyscan property
        """
        self._field = self.output_field
        return self._field

    @field.setter
    def field(self, new_value):
        self.hold()
        self.field_set_point = new_value
        self.to_set_point()
        # TODO: check if field is sweeping or at set point (if not either, then wait until it is sweeping)
        sleep(0.1)
        while self.sweeping_status:
            sleep(0.1)

    def status(self):
        status_string = self.query("X")
        return Status(status_string)

    @property
    def quench_status(self):
        """
        True when the magnet quenched
        """

        status = self.status()
        if status.X1 == 1:
            self._quench_status = True
        else:
            self._quench_status = False
        return self._quench_status

    @property
    def heater_status(self):
        """
        heater True for on and False for off
        """

        status = self.status()
        if status.H == 0:
            self._heater_status = False
        elif status.H == 1:
            self._heater_status = True
        else:
            # magnet persistant or heater fault - may need to have a heater_status object in future
            self._heater_status = False
        return self._heater_status

    @property
    def sweeping_status(self):
        """
        True when the field is changing, False when the field is at rest
        """

        status = self.status()
        if status.M2 == 0:
            self._sweeping_status = False
        else:
            self._sweeping_status = True
        return self._sweeping_status

    @property
    def remote_status(self):
        """
        True when magnet is in remote mode, False when it is in local mode.
        """

        status = self.status()
        if (status.C == 1) or (status.C == 3):
            self._remote_status = True
        else:
            self._remote_status = False

        return self._remote_status

    @property
    def persistent_status(self):
        """
        True when the magnet is in persistent mode
        """

        status = self.status()
        if status.H == 2:
            self._persistent_status = True
        else:
            self._persistent_status = False
        return self._persistent_status


class Status:
    def __init__(self, status_string="X00A1C3H1M10P03"):
        """
        Returns:
            Tuple of dictionaries, X1, X2, A, C, H, M1 and M2
            Each dictionary has a
                'description': what status is reported
                'value': integer from status string
                'states': text explanation of the status from the integer value
        """

        # get index values
        self.X1_name = "system status (operation)"
        self.X1 = int(status_string[1])
        self.X2_name = "system status (voltage)"
        self.X2 = int(status_string[2])
        self.A_name = "Activity"
        self.A = int(status_string[4])
        self.C_name = "LOC/REM status"
        self.C = int(status_string[6])
        self.H_name = "Heater"
        self.H = int(status_string[8])
        self.M1_name = "Mode (rate)"
        self.M1 = int(status_string[10])
        self.M2_name = "Mode (sweep)"
        self.M2 = int(status_string[11])

    def __repr__(self):
        value = "\n"
        value += f"{self.X1_name} : {self.X1_value()} (X1={self.X1})"
        value += "\n"
        value += f"{self.X2_name} : {self.X2_value()} (X2={self.X2})"
        value += "\n"
        value += f"{self.A_name} ; {self.A_value()} (A={self.A})"
        value += "\n"
        value += f"{self.C_name} ; {self.C_value()} (C={self.C})"
        value += "\n"
        value += f"{self.H_name} ; {self.H_value()} (H={self.H})"
        value += "\n"
        value += f"{self.M1_name} ; {self.M1_value()} (M1={self.M1})"
        value += "\n"
        value += f"{self.M2_name} ; {self.M2_value()} (M2={self.M2})"

        return value

    def X1_value(self):
        indexed_values = {
            0: "Normal",
            1: "Quenched",
            2: "Over Heated",
            4: "Warming Up",
            8: "Fault",
        }
        return indexed_values[self.X1]

    def X2_value(self):
        indexed_values = {
            0: "Normal",
            1: "On Positive Voltage Limit",
            2: "On Negative Voltage Limit",
            4: "Outside Negative Current Limit",
            8: "Outside Positive Current Limit",
        }
        return indexed_values[self.X2]

    def A_value(self):
        indexed_values = {0: "Hold", 1: "To Set Point", 2: "To Zero", 4: "Clamped"}
        return indexed_values[self.A]

    def C_value(self):
        indexed_values = {
            0: "Local & Locked",
            1: "Remote & Locked",
            2: "Local & Unlocked",
            3: "Remote & Unlocked",
            4: "Auto-Run-Down",
            5: "Auto-Run-Down",
            6: "Auto-Run-Down",
            7: "Auto-Run-Down",
        }
        return indexed_values[self.C]

    def H_value(self):
        indexed_values = {
            0: "Off Magnet at Zero",
            1: "On",
            2: "Off Magnet at Field",
            5: "Heater Fault",
            8: "No Switch Fitted",
        }
        return indexed_values[self.H]

    def M1_value(self):
        indexed_values = {
            0: "Amps, Immediate, Fast",
            1: "Tesla, Immediate, Fast",
            2: "Amps, Sweep, Fast",
            3: "Tesla, Sweep, Fast",
            4: "Amps, Immediate, Slow",
            5: "Tesla, Immediate, Slow",
            6: "Amps, Sweep, Slow",
            7: "Tesla, Sweep, Slow",
        }
        return indexed_values[self.M1]

    def M2_value(self):
        indexed_values = {
            0: "At Rest",
            1: "Sweeping",
            2: "Sweep Limiting",
            3: "Sweeping & Sweep Limiting",
            4: "Polarity Fault",
            5: "Sweeping & Polarity Fault",
            6: "Amps, Sweep, Slow",
            7: "Tesla, Sweep, Slow",
        }
        return indexed_values[self.M2]


class IPS120Error(Exception):
    pass


def ips120_float(string):
    """
    Helper function used with return_type to drop character and convert to a float.
    """

    return float(string[1:])


def ips120_int(string):
    """
    Helper function used with return_type to drop character and convert to a float.
    """

    return int(string[1:])
