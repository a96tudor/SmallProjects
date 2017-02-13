"""
                Website blocker

    MIT Standard Licence -- © Tudor Avram -- 13/02/17
"""
import platform
from dateutil import parser as p
from datetime import datetime as dt
import time

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

def startup_checks():
    """
        Function that does the initial checks (such as if it is running on a supported OS)
    :return:    - the path to the hosts file
                - the redirect IP address
    """
    hosts_paths = {
        "windows": r"C:\Windows\System32\drivers\etc\hosts",
        "linux": r"/etc/hosts",
        "darwin": r"/etc/hosts"
    }

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
        print("ERROR: We are sorry, but this application is not available for this operating system")
        exit()  # terminating the current application

    hosts_path = hosts_paths[_platform]
    redirect = "127.0.0.1"

    return hosts_path, redirect

def get_websites_list(f):
    """
        Reads the list of websites from the config files
    :param f:       The file pointer to read from
    :return:        The list of websites
    """
    websites = list()
    # creating the websites list
    line = f.readline()
    print(line == "#")
    while not (line == "#\n"):
        websites.append(line.replace("\n", ""))
        line = f.readline()

    return websites

def get_start_and_end_times(f):
    """
        Reads the start and end times from the config file
    :param f:       The file pointer to read from
    :return:        two datetime.datetime objects, representing the
                start and end times
    """
    str_start = f.readline()
    start = p.parse(str_start)
    str_end = f.readline()
    end = p.parse(str_end)

    return start, end

def solve_configs(cnf_file, redirect, host_path):
    """
        Reads the configuration file and collects the necessary data
        Also writes the website
    :param cnf_file:     The path to the configuration file
    :param redirect:     The IP address to redirect to
    :param host_path:    The path to the hosts file
    :return:     -  Two datetime.datetime objects, representing
    """

    print("Solving config\n")
    with open(cnf_file, "r") as f:
        _ = f.readline()  # ignoring the 1st line of the file

        websites = get_websites_list(f)
        start, end = get_start_and_end_times(f)

    with open(host_path, "r+") as f:
        content = f.read()
        # we have to write all the websites
        for website in websites:
            if website in content:
                pass
            else:
                f.write(redirect + " " + website + "\n")
    print("Written config\n")

    return websites, start, end

def reset_hosts_file(path, websites):
    """
        Resets the hosts file, by removing every change made by this program
    :param path:        The path to the hosts file
    :param websites:    The websites list
    :return:            -
    """
    with open(path, "r+") as f:
        contents = f.readlines()
        f.seek(0) #setting the file pointer
        for line in contents:
            if not any(website in line for website in websites):
                f.write(line)
        f.truncate()
def main():
    """
        The main function of the program
    :return: -
    """
    hosts, redirect = startup_checks()

    websites, start, end = solve_configs(
        cnf_file="config.cnf",
        redirect=redirect,
        host_path=hosts
    )

    while True:
        if start < dt.now() < end:
            #still work hours
            print("Still working hours... :(")
        else:
            # free time
            print("Yay!! Working hours are over! :D")
            reset_hosts_file(websites=websites, path=hosts)
            #let's reset the hosts file
        time.sleep(5)

main()