# -*- coding: utf-8 -*-
import numpy as np
from ...general.item_attribute import ItemAttribute
from thorlabs_kinesis import benchtop_stepper_motor as bsm
from ctypes import c_char_p, c_int, c_double, c_ushort, c_ulong, c_short
from time import sleep

c_word = c_ushort
c_dword = c_ulong


class ThorlabsBSC203(ItemAttribute):
    '''
    Driver for ThorLabs BSC203 - Three-Channel Benchtop
    Stepper Motor Controller.

    Parameters
    ----------
    serial : str
        Unit serial number. Defaults to "70878515".
    '''

    def __init__(self, serial="70878515"):
        self._version = "0.1.0"
        self.serial = c_char_p(bytes(serial, "utf-8"))
        if self.build_device_list() != 0:
            assert 0, 'Could not build device list'
        if self.open() != 0:
            print(self.open())
        sleep(1.5)

        for i in range(1, 4):
            self.set_channel_velocity_parameters(c_short(i), 4, 2)
            self.start_polling_channel(i)

            sleep(0.25)
            j = 0
            while True:
                try:
                    self.load_channel_settings(c_short(i))
                    break
                except:
                    j += 1
                    pass
                if j == 10:
                    break
            sleep(0.25)

    def build_device_list(self):
        return bsm.TLI_BuildDeviceList()

    def open(self):
        return bsm.SBC_Open(self.serial)

    def close(self):
        bsm.SBC_Close(self.serial)

    def get_number_channels(self):
        return bsm.SBC_GetNumChannels(self.serial)

    def home_channel(self, channel, wait=True):
        bsm.SBC_Home(self.serial, c_short(channel))
        target = 0
        bsm.SBC_RequestPosition(self.serial, channel)
        sleep(0.05)
        pos = bsm.SBC_GetPosition(self.serial, channel)
        i = 0
        while target != pos:
            bsm.SBC_RequestPosition(self.serial, channel)
            sleep(0.05)
            pos = bsm.SBC_GetPosition(self.serial, channel)
            i += 1
            if i > 20:
                break

        print('done')

    def home_all(self, wait=True):
        for i in range(1, 4):
            self.home_channel(i)
        self.x, self.y, self.z

    def to_device_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [4 / 3276800, 2 / 87960930, 4 / 36048]
        return int(round(val / conversions[pva]))

    def to_real_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [4 / 3276800, 2 / 87960930, 4 / 36048]
        return val * conversions[pva]

    def load_channel_settings(self, channel):
        bsm.SBC_LoadSettings(self.serial, channel)
        print(channel)

    def characterize_channel(self, channel):
        max_vel, max_accel = self.get_channel_velocity_parameters(channel)
        min_pos, max_pos = self.get_channel_travel_limits(channel)
        homing_vel = self.get_channel_homing_velocity(channel)
        pos = self.get_channel_position(channel)
        js = self.get_channel_job_step(channel)
        bl = self.get_channel_backlash(channel)
        # 'limits_vel':[self.toRealUnits(q,1) for q in self.motor.get_motor_velocity_limits(self.chan)],
        return {'homing_vel': homing_vel,
                'max_pos': max_pos,
                'min_pos': min_pos,
                'max_vel': max_vel,
                'value_acc': max_accel,
                'value_pos': pos,
                'backlash': bl,
                'jog_step': js}

    def set_channel_velocity_parameters(self, channel, max_vel, max_acc):

        max_acc = self.to_device_units(max_acc, 2)
        max_vel = self.to_device_units(max_vel, 1)
        bsm.SBC_SetVelParams(self.serial, channel, max_acc, max_vel)

    def get_channel_velocity_parameters(self, channel):
        acceleration = c_int()
        max_velocity = c_int()

        bsm.SBC_GetVelParams(self.serial, channel, acceleration, max_velocity)

        acc = self.to_real_units(acceleration.value, 2)
        vel = self.to_real_units(max_velocity.value, 1)

        return vel, acc

    def get_channel_travel_limits(self, channel):
        min_position = c_double()
        max_position = c_double()
        bsm.SBC_GetMotorTravelLimits(self.serial, channel, min_position, max_position)
        min_pos = self.to_real_units(min_position.value, 2)
        max_pos = self.to_real_units(max_position.value, 1)
        return min_pos, max_pos

    def get_channel_homing_velocity(self, channel):
        params = bsm.MOT_HomingParameters()
        bsm.SBC_GetHomingParamsBlock(self.serial, channel, params)
        velocity = self.to_real_units(params.velocity, 1)
        return velocity

    def get_channel_position(self, channel):

        pos = bsm.SBC_GetPosition(self.serial, c_short(channel))
        pos = self.to_real_units(pos)

        return pos

    def get_channel_backlash(self, channel):

        bl = bsm.SBC_GetBacklash(self.serial, channel)
        bl = self.to_real_units(bl)

        return bl

    def get_channel_job_step(self, channel):

        js = bsm.SBC_GetJogStepSize(self.serial, channel)
        js = self.to_real_units(js)

        return js

    def move_channel_to(self, channel, location, wait=True):
        index = self.to_device_units(location, 0)
        bsm.SBC_MoveToPosition(self.serial, channel, index)

        if wait:
            bsm.SBC_RequestPosition(self.serial, channel)
            sleep(0.15)
            pos = bsm.SBC_GetPosition(self.serial, channel)
            i = 0
            while index != pos:
                bsm.SBC_RequestPosition(self.serial, channel)
                sleep(0.15)
                pos = bsm.SBC_GetPosition(self.serial, channel)
                i += 0
                if i > 10:
                    break

    def move_channel_fast(self, channel, location):
        index = self.to_device_units(location, 0)
        bsm.SBC_MoveToPosition(self.serial, channel, index)
        # if channel == 1:
        #     x0 = self._x
        # elif channel == 2:
        #     x0 = self._y
        # elif channel == 3:
        #     x0 = self._z
        # sleep(np.abs(location-x0))

    def start_polling_channel(self, channel, interval=100):
        bsm.SBC_StartPolling(self.serial, channel, interval)

    def stop_polling_channel(self, channel):
        bsm.SBC_StopPolling(self.serial, channel)

    def can_move_without_home_first(self, channel):
        return bsm.SBC_CanMoveWithoutHomingFirst(self.serial)

    @property
    def x(self):
        self._x = self.get_channel_position(1)
        return self._x

    @x.setter
    def x(self, value):
        self.move_channel_to(1, value)
        self._x = value

    @property
    def xfast(self):
        self._x = self.get_channel_position(1)
        return self._x

    @xfast.setter
    def xfast(self, value):
        self.move_channel_fast(1, value)
        self._x = value

    @property
    def y(self):
        self._y = self.get_channel_position(2)
        return self._y

    @property
    def yfast(self):
        self._y = self.get_channel_position(2)
        return self._y

    @y.setter
    def y(self, value):
        self.move_channel_to(2, value)
        self._y = value

    @yfast.setter
    def yfast(self, value):
        self.move_channel_fast(2, value)
        self._y = value

    @property
    def z(self):
        self._z = self.get_channel_position(3)
        return self._z

    @z.setter
    def z(self, value):
        self.move_channel_to(3, value)
        self._z = value

    @property
    def zfast(self):
        self._z = self.get_channel_position(3)
        return self._z

    @zfast.setter
    def zfast(self, value):
        self.move_channel_fast(3, value)
        self._z = value

    @property
    def xyz(self):
        self._xyz = [self.get_channel_position(i) for i in range(1, 4)]
        return self._xyz

    @xyz.setter
    def xyz(self, posns):
        for i, posn in zip(range(1, 4), posns):
            self.move_channel_to(i, posn)

    def __del__(self):
        [self.stop_polling_channel(q) for q in range(1, 4)]
        self.close()

    # def wait(self,value):
    #     channels=np.arange(1, 4)
    #     [self.clear_channel_message_queue(q) for q in channels]
    #     chanready=np.zeros(3)
    #     starttime=time.time()
    #     while not all(chanready) and time.time()-starttime<10: # device sometimes doesn't respond
    #         info=np.array([self.wait_for_channel_message(q)[:2] if
    #         chanready[q-1]==0 else [2,value] for q in channels])
    #         chanready=np.all(info==[2,value],axis=1)
    #         print(info,chanready)
    # sys.stdout.flush()

    def clear_channel_message_queue(self, channel):
        bsm.SBC_ClearMessageQueue(self.serial, channel)

    # def wait_for_channel_message(self, channel):
    #     msg_type = c_word()
    #     msg_id = c_word()
    #     msg_data = c_dword()
    #     bsm.SBC_WaitForMessage(self.serial, channel, msg_type, msg_id,msg_data)
    #     return msg_type.value, msg_id.value, msg_data.value

    # def focus(self,expt,measure_function,zmin=2,zmax=3,zstep=.1):
    #     zs=[];data=[]
    #     for z in np.arange(zmin,zmax+zstep/2,zstep):
    #         self.moveto(z)
    #         zs.append(z)
    #         data.append(measure_function(expt).counts)
    #     zfocus=np.dot(data,zs)/np.sum(data)

    #     return zfocus,zs,data

    def calcWaitTime(self, dx, vmax=2, amax=4):
        """In units of mm[/s[/s]], returns in seconds"""
        if dx < vmax ** 2 / amax:
            return 2 * np.sqrt(dx / amax)
        else:
            return vmax / amax + dx / vmax

    def reset_speed(self):

        for chan in range(1, 4):
            self.set_channel_velocity_parameters(chan, 2, 4)
