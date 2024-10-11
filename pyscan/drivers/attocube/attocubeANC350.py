# -*- coding:utf-8 -*-
from pylablib.devices.Attocube.anc350 import ANC350
from ..instrument_driver import InstrumentDriver


class AttocubeANC350(InstrumentDriver):

    def __init__(self, instrument):

        super().__init__(instrument)

        self._version = "0.1.0"

        self.inst = ANC350()
        # self.debug = False
        # self.initialize_properties()

    def get_x(self):
        self._x = self.inst.get_position(0)
        return self._x

    def set_x(self, new_value):
        xmin = 1e-3
        xmax = 4.8e-3
        if (new_value < xmax) & (new_value > xmin):
            self.inst.move_to(0, new_value)
            self._x = 0
        else:
            print('x out of range')

    def get_y(self):
        self._y = self.inst.get_position(1)
        return self._y

    def set_y(self, new_value):
        ymin = 1e-3
        ymax = 4.8e-3
        if (new_value < ymax) & (new_value > ymin):
            self.inst.move_to(1, new_value)
            self._y = 0
        else:
            print('y out of range')

    def get_z(self):
        self._z = self.inst.get_position(2)
        return self._z

    def set_z(self, new_value):
        zmin = 0.6e-3
        zmax = 1e-3
        if (new_value < zmax) & (new_value > zmin):
            self.inst.move_to(2, new_value)
            self._z = 0
        else:
            print('z out of range')

    @property
    def x(self):
        return self.get_x()

    @x.setter
    def x(self, new_value):
        return self.set_x(new_value)

    @property
    def y(self):
        return self.get_y()

    @y.setter
    def y(self, new_value):
        return self.set_y(new_value)

    @property
    def z(self):
        return self.get_z()

    @z.setter
    def z(self, new_value):
        return self.set_z(new_value)

    @property
    def xyz(self):
        return [self.get_x(), self.get_y(), self.get_z()]

    @xyz.setter
    def xyz(self, new_value):
        return self.set_x(new_value[0]), self.set_y(new_value[1]), self.set_z(new_value[2])
