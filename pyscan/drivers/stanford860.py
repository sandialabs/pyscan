# -*- coding: utf-8 -*-
from .instrumentdriver import InstrumentDriver


class Stanford860(InstrumentDriver):
    '''Class to control Stanford Research Systems SR860 - 500 kHz lock-in amplifier
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.gain = 1

        self.debug = False

    def read_output(self, source):
        values = ['x', 'y', 'r', 'theta']
        if source in values:
            index = values.index(source) + 1
            if source in ['x', 'y', 'r']:
                return (float(self.query('OUTP? {}'.format(index))))
            else:
                return (float(self.query('OUTP? {}'.format(index)))
                        * 180 / 3.14159)
        else:
            print('Value Error:')
            print('Outputs are {}, {}, {}, or {}'.format(*values))

    def snap(self, *args):
        values = ['x', 'y', 'r', 'theta', 'aux1', 'aux2', 'aux3',
                  'aux4', 'frequency', 'display1', 'display2']

        if 2 <= len(args) <= 6:
            if set(args) < set(values):
                args = [str(values.index(val) + 1) for val in args]
                query_string = 'SNAP? ' + ', '.join(args)
                outputs = self.query(query_string)
                outputs = outputs.split(',')
                outputs = [float(op) for op in outputs]
                for i in range(len(outputs)):
                    if args[i] in range(2):
                        outputs[i] *= self.input_gain
                    elif args[i] == 3:
                        outputs[i] *= 180 / 3.14159
                return outputs

            else:
                print('Value Error')
                print('Snap requires 2 to 6 of the following')
                print(', '.join(values))
        else:
            print('Value Error')
            print('Snap requires 2 to 6 of the following')
            print(', '.join(values))
