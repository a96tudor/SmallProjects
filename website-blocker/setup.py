"""
   Setup application for the website blocker

    MIT Standard Licence -- © Tudor Avram -- 13/02/17
"""
import platform
from dateutil import parser as p
from datetime import datetime as dt

separator = "-"*60

def error_message(msg, terminate = True):
    """
        This function prints a given error message
    :param msg:             The messsage to be printed
    :param terminate:       True if we want to terminate the program
                            False if not
    :return:                -
    """
    print(msg)
    if terminate:
        exit()

def print_platform(f):
    """
        Function that gets the platform ID and prints it to the config file
    :param: f       The file pointer
    :return: -
    """

    known_platforms = [
        "windows",
        "linux",
        "darwin"  # MAC OS X
    ]

    # getting the operating system
    _platform = platform.system().lower()
    # doing the check
    if not (_platform in known_platforms):
        # error
        f.write("OS ERROR\n")  # writing the error to the config file
        error_message("ERROR: We are sorry, but this application is not available for this operating system")
    else:
        f.write(_platform + "\n")

def print_websites(f):
    """
        This function reads from the console and prints to the config file the
    websites that are going to be blocked
    :param f:       The file pointer to write to
    :return:    -
    """
    # getting websites counter
    try:
        cnt = int(input("How many websites do you want to block?\n"))
    except ValueError:
        f.write("INPUT ERROR\n")
        error_message("ERROR: You didn't write a valid number")

    # getting the websites
    for i in range(cnt):
        website = input("Enter the website number" + str(i + 1) + ": ")
        f.write(website.replace("www.", "") + "\n")
        f.write(website + "\n")
    f.write("#\n")

def check_format(input):
    """
        This function checks if a given string is in a date format. If not, it terminates the program
    :param input:       the input string
    :return:            The input as an datetime.datetime object if the string is in the right format
                        Nothing if it's not
    """
    try :
        return p.parse(input)
    except ValueError:
        print("ERROR: The specified date/time is not valid.")
        exit()

def print_start_and_end_times(f):
    """
        This function reads the start and end hours for the blocker and prints them to the config file
    :param f:   The file pointer
    :return:    -
    """
    print("Now you can set the times you want the websites to be blocked between: \n" +
          "They have to be in a readable date-time format and mention the hour and minutes"
        )
    start = check_format(input("Start time: \n"))
    end = check_format(input("End time: \n"))

    if start >= end:
        #error
        error_message("ERROR: The end time is smaller than the start time.\n")

    str_start = start.strftime("%H:%M")
    str_end = end.strftime("%H:%M")

    if str_start == "00:00" or str_end == "00:00":
        error_message("ERROR: The specified times are not valid\n")

    f.write(str_start + "\n")
    f.write(str_end + "\n")

def main():

    with open("config.cnf", "w") as f:
        print_platform(f)
        print_websites(f)
        print_start_and_end_times(f)

main()
