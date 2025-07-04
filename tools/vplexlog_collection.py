
""" Python script to collect the VPlex logs """
from __future__ import (absolute_import, division, print_function)
import os
import subprocess
import platform
import datetime
import sys
import re
import urllib3


__metaclass__ = type
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Check if Vplexapi is installed
try:
    import vplexapi  # pylint: disable=W0611
    HAS_VPLEXAPI_SDK = True
except ImportError:
    HAS_VPLEXAPI_SDK = False

if HAS_VPLEXAPI_SDK:
    from vplexapi import Configuration
    from vplexapi import ApiClient
    from vplexapi.api import version_api
else:
    print("Vplexapi is not installed. Exiting...")
    sys.exit(1)

# Constants
ANSIBLE_LOG = "dellemc_ansible_vplex.log"
PATH = "/var/log/VPlex/cli/"


def create_logdir():
    """
    Function to create log directory
    """
    # Create Logs directory if it is not present
    if not os.path.isdir("logs"):
        output = os.system("mkdir logs")
        if output != 0:
            print("Could not create a directory logs")
            return None
        print("Created the directory logs")

    # Create a Log folder with the current time stamp
    time = datetime.datetime.now()
    log = "logs/log_" + time.strftime("%Y_%m_%d_%H_%M_%S")
    if not os.path.isdir(log):
        output = os.system("mkdir " + log)
        if output != 0:
            print("Could not create directory {0}".format(log))
            return None
        print("Created a directory {0} for logs".format(log))
    return log


def collect_logs(log):  # pylint:disable=R0915,R0914,R0912
    """
    Function to collect the different logs and place them in the log
    directory
    """
    # Copy the ansible module logs to the log directory
    print("Collecting Ansible module logs...")
    if os.path.isfile(ANSIBLE_LOG):
        os.system("cp " + ANSIBLE_LOG + " " + log)
    else:
        print("Could not collect the Ansible module logs...")

    print("Collecting System logs...")
    # Collect system logs
    uname = platform.uname()  # pylint:disable=W0612
    details = ['machine', 'node', 'processor', 'release', 'system', 'version']
    line = sys.version
    version = []

    # Create a VPlex configuration object
    config = Configuration()
    config.host = 'https://' + sys.argv[1] + '/vplex/v2'
    config.username = sys.argv[2]
    config.password = sys.argv[3]
    config.verify_ssl = False
    config.ssl_ca_cert = False
    config.assert_hostname = False
    client = ApiClient(configuration=config)
    api_obj = version_api.VersionApi(client)

    # Get the VPlexapi version
    try:
        version = api_obj.get_versions()
    except Exception as err:  # pylint:disable=W0703
        print("Could not get the collect the VPlexapi version due to {0}".
              format(err))
        return 1
    if version != []:
        version = version[0]['version']

    # Open a log file and write the collected details to it
    with open(log + "/system_info.log", 'w') as logfile:
        logfile.write("Host System Information\n")
        logfile.write("***********************\n")
        if re.search(r"^3\.", line.split(" ", maxsplit=1)[0]):
            stdout = subprocess.check_output(["ansible", "--version"])
            logfile.write("Ansible Details:\n----------------\n{0}\n"
                          .format(stdout.decode('utf-8')))
            stdout = subprocess.check_output(["python", "--version"])
            logfile.write("Python Version: {0}\n".
                          format(stdout.decode('utf-8')))
            logfile.write("System Details:\n")
            logfile.write("---------------\n")
            # Log details based on the python version
            for attr in details:
                logfile.write("{0} : {1}\n"
                              .format(attr, eval(  # pylint:disable=W0123
                                  "uname.%s" % (attr))))
        elif re.search(r"^2\.", line.split(" ", maxsplit=1)[0]):
            stdout = subprocess.check_output(["ansible", "--version"])
            logfile.write("Ansible Details:\n----------------\n{0}\n"
                          .format(stdout))
            obj = subprocess.Popen("python --version", shell=True,
                                   stderr=subprocess.STDOUT,
                                   stdout=subprocess.PIPE)
            (stdout, stderr) = obj.communicate()  # pylint:disable=W0612
            logfile.write("Python Version: {0}\n".format(stdout))
            logfile.write("System Details:\n")
            logfile.write("---------------\n")
            # Log details based on the python version
            for attr in details:
                logfile.write("{0} : {1}\n"
                              .format(attr, eval(  # pylint:disable=W0123
                                  "platform.%s()" % (attr))))

        logfile.write("\nVplexapi Version:\n-----------------\n{0}\n"
                      .format(version))

    # Collect the VPlex server details
    log_file = []

    print("Collecting VPlex CLI logs...")
    # Get the list of log files in the VPlex server
    cmd = "sshpass -p \"" + sys.argv[3] + "\" ssh " + sys.argv[2] + "@" + \
          sys.argv[1] + " \"ls " + PATH + "restful.log_* \""
    try:
        obj = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE)
        (stdout, stderr) = obj.communicate()  # pylint:disable=W0612
        stdout = stdout.decode('utf-8').splitlines()
    except Exception as err:  # pylint:disable=W0703
        print("Could not collect the VPlex CLI Logs due to {0}".
              format(err))
        return 1
    for line in stdout:
        tmp = line.split("/")[-1]
        match = re.search(r"restful.log_(\d+)$", tmp)
        if match:
            log_file.append(match.group(1))

    # Copy the latest log file from the VPlex server to the
    # current Log directory
    if log_file == []:
        print("Could not collect the VPlex CLI Logs")
        return 1

    # Get the latest log file
    log_file = PATH + "restful.log_" + sorted(log_file)[-1]
    cmd = "sshpass -p \"" + sys.argv[3] + "\" scp " + sys.argv[2] + "@" + \
          sys.argv[1] + ":" + log_file + " " + log
    line = os.system(cmd)
    if line != 0:
        print("Could not copy the logs from the VPlex server")
        return 1

    print("The logs are in the path {0}".format(log))
    return 0


# Main function to collect logs and store it in a folder
if __name__ == "__main__":
    logpath = create_logdir()
    if not logpath:
        sys.exit(1)
    STATUS = collect_logs(logpath)
    sys.exit(STATUS)
