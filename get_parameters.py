import os
import argparse
import logging
from logger import Logger

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def get_user_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("ftp_website", help="Full FTP Website(username,password,directory) ", type=str)
    parser.add_argument("local_directory", help="Directory we want to synchronize", type=str)
    parser.add_argument("max_depth", help="Maximal depth to synchronize starting from the root directory", type=int)
    parser.add_argument("refresh_frequency", help="Refresh frequency to synchronize with FTP server (in seconds)", type=int)
    parser.add_argument("nb_multi", nargs='?', help="The number of thread (optional)",  default="1")
    parser.add_argument("excluded_extensions", nargs='*', help="List of the extensions to excluded when synchronizing (optional)",
                        type=str, default=[])
    # nargs = '*' : the last argument take zero or more parameter
    args = parser.parse_args()

    wrong_input = False

    # get the ftp website
    ftp_website = args.ftp_website

    # get the local directory to synchronize
    local_directory = args.local_directory
    if os.path.exists(local_directory) is False:
        Logger.log_error("Invalid FTP website")
        wrong_input = True

    # get the maximal depth
    try:
        max_depth = int(args.max_depth)
    except ValueError:
        Logger.log_error("Invalid input for the maximal depth : must be an integer")
        wrong_input = True
    else:
        if max_depth <= 0:
            Logger.log_error("Invalid value for the maximal depth : it can not be inferior or equal to 0")
            wrong_input = True

    # get the refresh frequency
    try:
        refresh_frequency = int(args.refresh_frequency)
    except ValueError:
        Logger.log_error("Invalid input for the refresh frequency : must be an integer")
        wrong_input = True
    else:
        if refresh_frequency <= 0:
            Logger.log_error("Invalid value for the refresh frequency : it can not be inferior or equal to 0")
            wrong_input = True

    # judge and get the number of thread
    if args.nb_multi.isdigit():
        try:
            nb_multi = int(args.nb_multi)
        except ValueError:
            Logger.log_error("Invalid input for the number of thread : must be an integer")
            wrong_input = True
        else:
            if nb_multi <= 0:
                Logger.log_error("Invalid value for the number of thread : it can not be inferior or equal to 0")
                wrong_input = True
    else:
        args.excluded_extensions.append(args.nb_multi)
        nb_multi = 1

    # get a list of the excluded extensions
    excluded_extensions = args.excluded_extensions

    if wrong_input is False:
        Logger.log_info("Valid parameters")
        return ftp_website, local_directory, max_depth, refresh_frequency, nb_multi, excluded_extensions
    else:
        return 0
