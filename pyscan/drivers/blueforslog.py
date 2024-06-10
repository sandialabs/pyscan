# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd


def last_line(path):
    '''
    Reads the last line of the text file provided

    Args:
        path - path to text file

    returns str
    '''
    with open(path) as f:
        for line in f:
            pass
        ll = line

    return ll


def get_last_value(path):
    '''
    Returns the last value in CSV file

    Args:
        path - path to csv file


    returns float
    '''

    data = last_line(path)

    data = last_line(path).strip('\n')
    data = data.split(',')

    return float(data[-1])


def get_df(path, name):
    '''
    Returns dataframe from path

    Args:
        path - path to file
        name - name of parameter to be read

    returns pd.DataFrame
    '''

    df = pd.read_csv(path, names=['date', 'time', name])

    return df


def get_all_temperature_values(path, name):
    '''
    Returns all temperatue values from path

    Args:
        path - path to BF log file
        name - name of the temperature property

    returns pd.DataFrame
    '''

    df = get_df(path, name)
    df['date'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.drop(['time'], axis=1)

    return df


class BlueForsLog(object):
    '''
    Class ulitily to read BlueForc log files

    Parameters
    ----------
    path : str
        The path to the  log
    date : str
        Need to remember format

    Attributes
    ----------
    (Properties)
    TChX (X = 1, 2, 3, 5, 6, 9) - gets temperature of channel X
        returns float
    temperatures - gets all temperatures
        returns array (float)
    all_TCHX (X = 1, 2, 3, 5, 6, 9) - returns all temperature values for
        channel X in log file
        returns np.DataFrame
    all_temperatures - returns all temperature values in the log file
        returns np.DataFrame
    '''

    def __init__(self, path, date='now'):
        self.path = Path(path)
        self.date = date
        self._version = "0.1.0"

    def get_path(self, file):

        if self.date == 'now':
            pass
        else:
            path = str(self.path / self.date / file.format(self.date))

        return path

    @property
    def TCH1(self):
        path = self.get_path('CH1 T {}.log')
        return get_last_value(path)

    @property
    def TCH2(self):
        path = self.get_path('CH2 T {}.log')
        return get_last_value(path)

    @property
    def TCH3(self):
        path = self.get_path('CH3 T {}.log')
        return get_last_value(path)

    @property
    def TCH5(self):
        path = self.get_path('CH5 T {}.log')
        return get_last_value(path)

    @property
    def TCH6(self):
        path = self.get_path('CH6 T {}.log')
        return get_last_value(path)

    @property
    def TCH9(self):
        path = self.get_path('CH9 T {}.log')
        return get_last_value(path)

    @property
    def temperatures(self):
        return self.TCH1, self.TCH2, self.TCH3, self.TCH5, self.TCH6, self.TCH9

    @property
    def all_TCH1(self):
        path = self.get_path('CH1 T {}.log')
        return get_all_temperature_values(path, 't1')

    @property
    def all_TCH2(self):
        path = self.get_path('CH2 T {}.log')
        return get_all_temperature_values(path, 't2')

    @property
    def all_TCH3(self):
        path = self.get_path('CH3 T {}.log')
        return get_all_temperature_values(path, 't3')

    @property
    def all_TCH5(self):
        path = self.get_path('CH5 T {}.log')
        return get_all_temperature_values(path, 't5')

    @property
    def all_TCH6(self):
        path = self.get_path('CH6 T {}.log')
        return get_all_temperature_values(path, 't6')

    @property
    def all_TCH9(self):
        path = self.get_path('CH9 T {}.log')
        return get_all_temperature_values(path, 't9')

    @property
    def all_temperatures(self):

        path = self.get_path('CH1 T {}.log')
        df = get_all_temperature_values(path, 't1')

        path = self.get_path('CH2 T {}.log')
        new_df = get_df(path, 't2')
        df['t2'] = new_df['t2']

        path = self.get_path('CH3 T {}.log')
        new_df = get_df(path, 't3')
        df['t3'] = new_df['t3']

        path = self.get_path('CH5 T {}.log')
        new_df = get_df(path, 't5')
        df['t5'] = new_df['t5']

        path = self.get_path('CH6 T {}.log')
        new_df = get_df(path, 't6')
        df['t6'] = new_df['t6']

        path = self.get_path('CH9 T {}.log')
        new_df = get_df(path, 't9')
        df['t9'] = new_df['t9']

        return df
