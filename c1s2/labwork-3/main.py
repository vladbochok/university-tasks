"""Vladyslav Bochok"""
import sys
import load
from error import *


def print_name_and_variant():
    print("Variant 31", "Vladyslav Bochok", sep="\n")


def print_info():
    print("Process semester journal data class attendance checks.")
    print("Print only information about students who missed only 4 lessons.")
    print("Sort the data by specified criteria:")
    print("Students are sorted by: number of passes, name, surname")
    print("Sorting within one student: week, day, lessons")


def main(path_config_file: str):
    """
    Function for data processing "on a turn-key basis".

    Opens and retrieves data from the configuration file
    Loads data files and processes them, make outputs
    In case of incorrect data, it displays an error message and terminates with code 0.

    :param path_config_file: path to json file with configurations
    """
    try:
        print(f"ini {path_config_file} :", end=' ')
        # create an instance of the class that will load the data
        builder = load.create_builder(path_config_file, "utf-8")
        print("OK")

        csv_name = builder.get_name_cvs()
        json_name = builder.get_name_json()
        out_name = builder.get_name_outpath()
        out_enc = builder.get_enc_outpath()

        print(f"input-csv {csv_name} :", end=' ')
        builder.load_data()  # download basic data
        print("OK")

        print(f"input-json {json_name} :", end=' ')
        builder.load_stat()  # download auxiliary statistics data
        print("OK")

        info = builder.get_product_information()  # get an instance of the class that stores the processed data

        print("json?=csv:", end=' ')
        if not info.fit():
            raise ConformityInformationError()
        print("OK")

        print(f"output {out_name} :", end=' ')
        info.output(out_name, out_enc)
        print("OK")

    except Error as e:
        print('\n***** program aborted *****')
        print(e)


print_name_and_variant()
print_info()
print("*****")
if len(sys.argv) == 2:  # check if user started the program with one argument
    main(sys.argv[1])
else:
    print("***** program aborted *****")
    print("***** command line error *****")
