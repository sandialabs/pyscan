# -*- coding: utf-8 -*-
import ctypes
from ctypes import byref
from ...general.item_attribute import ItemAttribute
from time import sleep
from pathlib import Path
from time import strftime

TTREADMAX = 131072
FLAG_OVERFLOW = 0x0040
FLAG_FIFOFULL = 0x0003
HISTCHAN = 65536
syncDivider = 1

phlib = ctypes.CDLL("phlib64.dll")
counts = (ctypes.c_uint * HISTCHAN)()
libVersion = ctypes.create_string_buffer(b"", 8)
hwSerial = ctypes.create_string_buffer(b"", 8)
hwPartno = ctypes.create_string_buffer(b"", 8)
hwVersion = ctypes.create_string_buffer(b"", 8)
hwModel = ctypes.create_string_buffer(b"", 16)
errorString = ctypes.create_string_buffer(b"", 40)
resolution = ctypes.c_double()
count_rate_0 = ctypes.c_int()
count_rate_1 = ctypes.c_int()
flags = ctypes.c_int()
nactual = ctypes.c_int()
ctcDone = ctypes.c_int()
buffer = (ctypes.c_uint * TTREADMAX)()

# def t2_data_to_times(data):

#    n31 = 0
#    n30 = 0

#    chan0 = []
#    n0 = 0
#    chan1 = []
#    n1 = 0
#    for i in range(len(data)):
#        bdata = bin(data[i])
#        if len(bdata) == 31:
#            chan1.append(int('0b' + bdata[3:], 2))
#            if len(chan1) > 1:
#                if chan1[-1] < chan1[-2]:
#                    n1+= 1
#                    chan1[-1] += n1*2**28

#        elif len(bdata) < 31:
#            chan0.append(int(bdata, 2))
#            if len(chan0) > 1:
#                if chan0[-1] < chan0[-2]:
#                    n0+= 1
#                    chan0[-1] += n0*2**28

#    return chan0, chan1


def t2_data_to_times(data):

    offset = 0
    wrap_around = 210698240
    chan0 = []
    chan1 = []

    for i, d in enumerate(data):
        if len(bin(d)) == 34:
            if bin(d)[2:6] == '1111':
                offset += wrap_around
        else:
            bdata = bin(d)
            if len(bdata) == 31:
                chan1.append(int(bdata[3::], 2) + offset)
            else:
                chan0.append(int(bdata[2::], 2) + offset)

    return chan0, chan1


def tryfunc(retcode, funcName):
    if retcode < 0:
        phlib.PH_GetErrorString(errorString, ctypes.c_int(retcode))
        print("PH_%s error %d (%s). Aborted." % (funcName, retcode,
              errorString.value.decode("utf-8")))
        # closeDevices()


class PicoHarp300(ItemAttribute):
    '''Class to control PicoQuant PicoHarp 300 - Stand-alone TCSP Module with USB Interface

    Parameters
    ----------
    dev : int
        Device index, default 0

    '''

    def __init__(self, dev=0):

        self._version = "0.1.0"

        retcode = phlib.PH_OpenDevice(ctypes.c_int(dev), hwSerial)
        if retcode == 0:
            print("{}S/N {}".format(dev, hwSerial.value.decode("utf-8")))
            self.dev = dev
        else:
            if retcode == -1:
                print("{} no device".format(dev))
            else:
                phlib.PH_GetErrorString(errorString, ctypes.c_int(retcode))
                print("{} {}".format(dev, errorString.value.decode("utf8")))

        sleep(0.2)

    # @property
    # def binning(self):
    #     tryfunc(phlib.PH_GetBinning(ctypes.c_int(self.dev), ctypes.c_int(binning)), "GetBinning")
    #     self._binning = binning.value
    #     return self._binning

    # @binning.setter
    # def binning(self, new_value):
    #     binning = new_value
    #     tryfunc(phlib.PH_SetBinning(ctypes.c_int(self.dev), ctypes.c_int(binning)), "SetBinning")

    # @property
    # def offset(self):
    #     tryfunc(phlib.PH_GetOffset(ctypes.c_int(self.dev), ctypes.c_int(offset)), "GetOffset")
    #     self._offset = offset.value
    #     return self._offset

    # @offset.setter
    # def offset(self, new_value):
    #     offset = new_value
    #     tryfunc(phlib.PH_Setoffset(ctypes.c_int(self.dev), ctypes.c_int(offset)), "SetOffset")

    @property
    def resolution(self):
        tryfunc(phlib.PH_GetResolution(ctypes.c_int(self.dev), byref(resolution)), "GetResolution")
        self._resolution = resolution.value
        return self._resolution

    @resolution.setter
    def resolution(self, new_value):
        resolution = new_value
        tryfunc(phlib.PH_SetResolution(ctypes.c_int(self.dev), byref(resolution)), "SetResolution")

    def set_channel_0_voltage(self, zero_cross=10, discriminator=100):
        print(self.dev, zero_cross, discriminator)

        tryfunc(
            phlib.PH_SetInputCFD(
                ctypes.c_int(self.dev), ctypes.c_int(0),
                ctypes.c_int(discriminator), ctypes.c_int(zero_cross)),
            "SetInputCFD")
        sleep(0.2)

    def set_channel_1_voltage(self, zero_cross=10, discriminator=100):
        print(self.dev, zero_cross, discriminator)

        tryfunc(
            phlib.PH_SetInputCFD(
                ctypes.c_int(self.dev), ctypes.c_int(1),
                ctypes.c_int(discriminator), ctypes.c_int(zero_cross)),
            "SetInputCFD"
        )
        sleep(0.2)

    def set_sync_divider(self):
        tryfunc(phlib.PH_SetSyncDiv(ctypes.c_int(self.dev), ctypes.c_int(syncDivider)), "SetSyncDiv")

    def calibrate(self):
        tryfunc(phlib.PH_Calibrate(ctypes.c_int(self.dev)), "Calibrate")

    def set_histgram_mode(self):
        tryfunc(phlib.PH_Initialize(ctypes.c_int(self.dev), ctypes.c_int(0)), "Initialize")

    def set_corrleation_mode(self):
        tryfunc(phlib.PH_Initialize(ctypes.c_int(self.dev), ctypes.c_int(2)), "Initialize")

    def clear_histogram_memory(self):
        tryfunc(phlib.PH_ClearHistMem(ctypes.c_int(self.dev), ctypes.c_int(0)), "ClearHistMeM")

    def get_count_rate_0(self):
        tryfunc(
            phlib.PH_GetCountRate(ctypes.c_int(self.dev), ctypes.c_int(0), byref(count_rate_0)),
            "GetCountRate")
        return count_rate_0.value

    def get_count_rate_1(self):
        tryfunc(
            phlib.PH_GetCountRate(ctypes.c_int(self.dev), ctypes.c_int(1), byref(count_rate_1)),
            "GetCountRate")
        return count_rate_1.value

    def start_measurement(self, time):
        tryfunc(phlib.PH_StartMeas(ctypes.c_int(self.dev), ctypes.c_int(time)), "StartMeas")

    def stop_measurement(self):
        tryfunc(phlib.PH_StopMeas(ctypes.c_int(self.dev)), "StopMeas")

    def get_histogram(self):
        tryfunc(phlib.PH_GetHistogram(ctypes.c_int(self.dev), byref(counts), ctypes.c_int(0)),
                "GetHistogram")

    def get_flags(self):
        tryfunc(phlib.PH_GetFlags(ctypes.c_int(self.dev), byref(flags)), "GetFlags")
        return flags.value

    def get_ctc_status(self):
        tryfunc(phlib.PH_CTCStatus(ctypes.c_int(self.dev), byref(ctcDone)),
                "CTCStatus")
        return ctcDone.value

    def read_fifo(self):
        tryfunc(
            phlib.PH_ReadFiFo(ctypes.c_int(self.dev), byref(buffer), TTREADMAX,
                              byref(nactual)),
            "ReadFiFo")

    def offset(self, new_value):
        offset = new_value
        tryfunc(phlib.PH_SetOffset(ctypes.c_int(self.dev), ctypes.c_int(offset)), "SetOffset")

    def resolution(self):
        tryfunc(phlib.PH_GetResolution(ctypes.c_int(self.dev), byref(resolution)), "GetResolution")
        self._resolution = resolution.value
        return self._resolution

    def init_histogram_mode(self):
        self.set_histgram_mode()
        self.calibrate()
        self.set_sync_divider()
        sleep(0.2)

    def init_correlation_mode(self):
        self.set_corrleation_mode()
        self.calibrate()
        self.set_sync_divider()
        sleep(0.2)

    def run_correlation(self, time, file_name=None):

        self.start_measurement(time)

        if file_name is None:
            if not Path('./g2').is_dir():
                Path('./g2').mkdir()

            file_name = './g2/{}'.format(strftime("%Y%m%dT%H%M%S"))

        outputfile = open(file_name, "wb+")

        while True:
            flags = self.get_flags()

            if flags & FLAG_FIFOFULL > 0:
                print("\nFiFo Overrun!")
                break
            self.read_fifo()

            if nactual.value > 0:
                outputfile.write((ctypes.c_uint * nactual.value)(*buffer[0:nactual.value]))
            else:
                ctc_status = self.get_ctc_status()
                if ctc_status > 0:
                    self.stop_measurement()
                    outputfile.close()
                    break

        return file_name
