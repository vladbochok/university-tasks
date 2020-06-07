"""Vladyslav Bochok"""


class Error(BaseException):
    def __str__(self):
        return ''


class InitError(Error):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '***** init file error *****\n' + self.data


class LoadError(Error):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class ReadCvsError(Error):
    def __str__(self):
        return '***** can not read input csv-file *****'


class InputCvsError(Error):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '***** incorrect input csv-file *****\n' + self.data


class ReadJsonError(Error):
    def __str__(self):
        return '***** can not read input json-file *****'


class InputJsonError(Error):
    def __str__(self):
        return '***** incorrect input json-file *****'


class ConformityInformationError(Error):
    def __str__(self):
        return '***** inconsistent information *****'


class WriteError(Error):
    def __str__(self):
        return '***** can not write output file *****'
