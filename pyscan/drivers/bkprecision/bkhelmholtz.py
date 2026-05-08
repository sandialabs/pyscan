from .bkprecision9130b import BKPrecision9130B
import numpy as np


class BKHelmholtz(BKPrecision9130B):

    def __init__(self, instrument, current_to_field=5):

        super().__init__(instrument)

        self.current_to_field = current_to_field

    @property
    def ix(self):
        self._ix = self.i1
        return self._ix

    @ix.setter
    def ix(self, new_value):
        self.i1 = new_value
        self._ix = new_value

    @property
    def iy(self):
        self._iy = self.i2
        return self._iy

    @iy.setter
    def iy(self, new_value):
        self.i2 = new_value
        self._iy = new_value

    @property
    def iz(self):
        self._iz = self.i3
        return self._iz

    @iz.setter
    def iz(self, new_value):
        self.i3 = new_value
        self._iz = new_value

    @property
    def bx(self):
        self._bx = self.ix * self.current_to_field
        return self._bx

    @bx.setter
    def bx(self, new_value):

        if (0 <= new_value) and (new_value < 20):
            self.ix = new_value / self.current_to_field
            # sleep(1)
            self._bx = new_value
        else:
            print('Current out of range 0 <= bx <= 20 Gauss')

    @property
    def by(self):
        self._by = self.iy * self.current_to_field
        return self._by

    @by.setter
    def by(self, new_value):

        if (new_value >= 0) and (new_value <= 20):
            self.iy = new_value / self.current_to_field
            # sleep(1)
            self._by = new_value
        else:
            print('Current out of range 0 <= by <= 20 Gauss')

    @property
    def bz(self):
        self._bz = self.iz * self.current_to_field
        return self._bz

    @bz.setter
    def bz(self, new_value):

        if (new_value >= 0) and (new_value <= 20):
            self.iz = new_value / self.current_to_field
            # sleep(1)
            self._bz = new_value
        else:
            print('Current out of range 0 <= bz <= 20 Gauss')

    @property
    def bmag(self):
        self._bmag = np.sqrt(self.bx**2 + self.by**2 + self.bz**2)
        return self._bmag

    @bmag.setter
    def bmag(self, new_value):

        if (new_value < 20) and (new_value > 0):

            theta = self.btheta * np.pi / 180
            phi = self.bphi * np.pi / 180

            bz = new_value * np.cos(theta)
            bx = new_value * np.sin(theta) * np.cos(phi)
            by = new_value * np.sin(theta) * np.sin(phi)

            self.bx = bx
            # sleep(1)
            self.by = by
            # sleep(1)
            self.bz = bz
            # sleep(1)

        else:
            print('B magnetude out of range 0 <= Bmag <= 20 Gauss')

    @property
    def btheta(self):
        self._btheta = np.arctan2(np.sqrt(self.bx**2 + self.by**2), self.bz) * 180 / np.pi

        return self._btheta

    @btheta.setter
    def btheta(self, new_value):

        if (new_value >= 0) and (new_value <= 90):

            phi = self.bphi * np.pi / 180
            theta = new_value * np.pi / 180
            bmag = self.bmag

            bz = bmag * np.cos(theta)
            bx = bmag * np.sin(theta) * np.cos(phi)
            by = bmag * np.sin(theta) * np.sin(phi)

            self.bx = bx
            # sleep(1)
            self.by = by
            # sleep(1)
            self.bz = bz
            # sleep(1)

        else:
            print('B theta out of range 0 <= Bmag <= 90 degrees')

    @property
    def bphi(self):
        self._bphi = np.arctan2(self.by, self.bx) * 180 / np.pi
        return self._bphi

    @bphi.setter
    def bphi(self, new_value):

        if (new_value >= 0) and (new_value <= 90):

            phi = new_value * np.pi / 180
            theta = self.btheta * np.pi / 180
            bmag = self.bmag

            bz = bmag * np.cos(theta)
            bx = bmag * np.sin(theta) * np.cos(phi)
            by = bmag * np.sin(theta) * np.sin(phi)

            self.bx = bx
            # sleep(1)
            self.by = by
            # sleep(1)
            self.bz = bz
            # sleep(1)

        else:
            print('B phi out of range 0 <= Bmag <= 90 degrees')
