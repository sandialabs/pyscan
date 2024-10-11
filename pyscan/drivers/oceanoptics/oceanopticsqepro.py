# -*- coding: utf-8 -*-
import numpy as np
from seabreeze.spectrometers import Spectrometer
from ...general.item_attribute import ItemAttribute


class OceanOpticsQEPro(ItemAttribute):
    '''
    Class to control Ocean Opticss QEPro optical spectrometer

    Parameters
    ----------
    sn :
        serial number of the spectrometer. Defaults to None.

    Properties
    ----------
    intensities :
        returns an array of intensities
    wavelength :
        returns an array of measured wavelenghts
    spectrum :
        returns both intensities and wavelengths
    '''

    def __init__(self, sn=None):

        if sn is None:
            self.spec = Spectrometer.from_first_available()
        else:
            self.spec = Spectrometer.from_serial_number(sn)
        self.sn = sn
        self.set_integration_time(.25)
        self._version = "0.1.0"

    def set_integration_time(self, value):
        '''
        Sets the integration time for the spectrum

        Args:
            value - integration time in ns
        '''
        self._integration_time = value * 1e6
        return self.spec.integration_time_micros(value * 1e6)

    def get_integration_time(self):
        return self.spec.integration_time_micros()

    @property
    def intensities(self):
        return self.spec.intensities()

    @property
    def wavelength(self):
        return self.spec.wavelengths()

    @property
    def spectrum(self):
        return self.spec.spectrum()

    def counts(self):
        return np.sum(self.spec.intensities())

    def __del__(self):
        self.spec.close()
