"""Vladyslav Bochok"""
import csv
import json
from information import Information
from error import *


class Builder:
    """
    Reads and processes data to construct the Information object.
    Stores and returns configuration and processed information.
    """

    def __init__(self, in_cvs: str, in_json: str, in_enc: str, out_enc: str, out_name: str):
        self._information = Information()
        self._in_cvs = in_cvs
        self._in_json = in_json
        self._in_enc = in_enc
        self._out_enc = out_enc
        self._out_name = out_name
        self._is_load_stat_done = False
        self._is_load_data_done = False

    def load_data(self):
        """
        Reads information from the main CVS file about each of the students
        Transmits collected information to the Information class the class Information.

        In case of impossibility to read data - raise ReadCvsError
        In case of incorrect data - raise InputCvsError
        """
        try:
            with open(self._in_cvs, 'r', encoding=self._in_enc) as read_file:
                reader = csv.DictReader(read_file, delimiter=';')
                for row in reader:
                    self._information.load(row['name1'], row['name2'], row['group'], row['whom'],
                                           row['course'], row['data'], row['when'], row['num'], row['kind'], row['aud'])
                self._is_load_data_done = True
        except OSError:
            self._information.clear_data()
            raise ReadCvsError()
        except LoadError as e:
            self._information.clear_data()
            raise InputCvsError(str(e))

    def load_stat(self):
        """
        Reads additional statistical information from the json file to verify the data.

        In case of impossibility to read data - raise ReadJsonError
        In case of incorrect data - raise InputJsonError
        """
        try:
            with open(self._in_json, encoding=self._in_enc) as read_file:
                data = json.load(read_file)

            cnt_missed_4_lessons = data["кількість пропусків на четвертих парах"]
            cnt_missed_lectures = data["кількість пропусків лекцій"]

            self._information.set_stat(cnt_missed_4_lessons, cnt_missed_lectures)
            self._is_load_stat_done = True
        except OSError:
            self._information.clear_stat()
            raise ReadJsonError()
        except BaseException:
            self._information.clear_stat()
            raise InputJsonError()

    def is_product_done(self) -> bool:
        """returns the logical value of checking the complete correctness of the data"""
        return self._is_load_data_done and self._is_load_stat_done

    def get_product_information(self) -> Information:
        """
        Returns the constructed instance of the information class.
        In case the Information class is not yet constructed, it returns None
        """
        if self.is_product_done():
            return self._information

    def get_name_cvs(self):
        return self._in_cvs

    def get_name_json(self):
        return self._in_json

    def get_name_outpath(self):
        return self._out_name

    def get_enc_outpath(self):
        return self._out_enc


def create_builder(input_name: str, encoding: str) -> Builder:
    """
    Reads a file with the main fields, constructs an object of type Builder.
    In case of impossibility to read data or their incorrectness - raise InitError

    :param input_name: path to json file with settings
    :return: Builder
    """
    try:
        with open(input_name, encoding=encoding) as read_file:  #
            data = json.load(read_file)

        in_cvs = data['input']['csv']
        in_json = data['input']['json']
        in_enc = data['input']['encoding']
        out_enc = data['output']['encoding']
        out_name = data['output']['fname']

        # If the term is empty then conclusion needs to be made in stdout
        if not out_name:
            out_name = "stdout"

        return Builder(in_cvs, in_json, in_enc, out_enc, out_name)
    except OSError:
        raise InitError('***** file can not opened *****')
    except BaseException:
        raise InitError('***** incorrect file data *****')
