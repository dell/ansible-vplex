"""vplexapi connection establishment module"""

import logging
import re
from json import loads

try:
    import vplexapi  # pylint: disable=W0611
    HAS_VPLEXAPI_SDK = True
except ImportError:
    HAS_VPLEXAPI_SDK = False

try:
    import urllib3
    HAS_URLLIB3 = True
except ImportError:
    HAS_URLLIB3 = False

try:
    import certifi  # pylint: disable=W0611
    HAS_CERTIFI = True
except ImportError:
    HAS_CERTIFI = False


class VplexapiModules():    # pylint:disable=R0903
    """Class with vplexapi python sdk import statements"""
    if HAS_VPLEXAPI_SDK:
        from vplexapi.api import AmpApi  # pylint:disable=C0415
        from vplexapi.api import ClustersApi  # pylint:disable=C0415
        from vplexapi.api import ConsistencyGroupApi  # pylint:disable=C0415
        from vplexapi.api import DevicesApi  # pylint:disable=C0415
        from vplexapi.api import DistributedStorageApi  # pylint:disable=C0415
        from vplexapi.api import ExportsApi  # pylint:disable=C0415
        from vplexapi.api import ExtentApi  # pylint:disable=C0415
        from vplexapi.api import StorageArrayApi  # pylint:disable=C0415
        from vplexapi.api import StorageVolumeApi  # pylint:disable=C0415
        from vplexapi.api import VirtualVolumeApi  # pylint:disable=C0415
        from vplexapi.api import HardwarePortsApi  # pylint:disable=C0415
        from vplexapi.api import MapsApi  # pylint:disable=C0415
        from vplexapi.api import DataMigrationApi  # pylint:disable=C0415


if HAS_VPLEXAPI_SDK:
    from vplexapi import Configuration
    from vplexapi import ApiClient
    from vplexapi.api import ClustersApi, VersionApi
    from vplexapi.rest import ApiException

if HAS_URLLIB3:
    from urllib3.exceptions import MaxRetryError
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOCUMENTATION = r'''
---

Check required libraries
'''


def has_vplexapi_sdk():
    """This method checks for Python SDK library"""
    return HAS_VPLEXAPI_SDK


def external_library_check():
    """This method checks for external libraries"""
    module_dict = {'urllib3': HAS_URLLIB3, 'certifi': HAS_CERTIFI}
    for key, value in module_dict.items():
        if not value:
            err_msg = ("Ansible modules for VPLEX require {0}"
                       " library to be installed. Please install the"
                       " library before using these modules.".format(
                           key))
            return (False, err_msg)
    return (True, None)


DOCUMENTATION = r'''
---

This method is to initialize the configuration for VPLEX API
parameters:
  module_params - Ansible module parameters which contain below VPLEX
                  host details required for connection establishment
     - vplexhost: VPLEX host IP
     - vplexuser: Username of VPLEX host
     - vplexpassword: Password of VPLEX host
     - verifycert: To verify SSL certificate
     - ssl_ca_cert: CA certificate file to be specified when verifycert is
                    set to True
returns ApiClient object
'''


def config_vplexapi(module_params):
    """This method provide the vplexapi connection establishment"""
    exit_code, msg = None, None
    host = module_params['vplexhost']
    user = module_params['vplexuser']
    password = module_params['vplexpassword']
    cert = module_params['verifycert']
    ssl_cert = module_params['ssl_ca_cert']

    if not (all([host, user, password]) and cert in [True, False]):
        msg = ('vplexhost, vplexuser, vplexpassword, verifycert '
               'can not be empty')
        exit_code = 403
    if cert and not ssl_cert:
        msg = ('ssl_ca_cert file(CA Certificate in .pem format) is required'
               ' when verifycert(verify_ssl) is set to True')
        exit_code = 495
    if exit_code and msg:
        return exit_code, msg

    config = Configuration()
    config.host = 'https://' + host + '/vplex/v2'
    config.username = user
    config.password = password
    config.verify_ssl = cert
    config.ssl_ca_cert = ssl_cert
    config.assert_hostname = False
    # Enable VPlex api to collect the logs
    config.debug = True

    client = ApiClient(configuration=config)
    try:
        cluster_client = ClustersApi(client)
        cluster_client.get_clusters_with_http_info(_request_timeout=5)
    except (ApiException, MaxRetryError) as ex:
        if config.verify_ssl:
            msg = ('Could not establish connection with Host %s. Please'
                   ' check the host or CA certificate if provided, is'
                   ' valid' % (host))
        else:
            msg = 'Could not establish connection with Host %s' % (host)
        if isinstance(ex, MaxRetryError):
            return 504, msg
        if isinstance(ex, ApiException):
            if ex.status == 401:
                return 401, 'Could not authenticate user in %s' % (host)
            try:
                body = loads(ex.body)
                return ex.status, body['message']
            except Exception as ex:  # pylint: disable=W0703
                # if user provided server where
                # non VPLEX service is running
                return 503, msg
    return client


DOCUMENTATION = r'''
---
This function verify if given cluster name is correct or not
It accepts vplexapi-client and cluster_name
'''


def verify_cluster_name(vplexclient, cluster_name):
    """Verify if given cluster is valid or not"""
    cluster_client = ClustersApi(vplexclient)
    try:
        cluster_client.get_cluster(cluster_name)
    except ApiException as ex:
        body = loads(ex.body)
        return body['error_code'], body['message']
    return 200, 'Cluster Found: %s' % cluster_name


DOCUMENTATION = r'''
---

Common function to serialize the output
'''


def serialize_content(vplex_data):
    """This method will serialize the VPLEX output to JSON"""
    serialize_obj = ApiClient()
    return serialize_obj.sanitize_for_serialization(vplex_data)


DOCUMENTATION = r'''
---

This method provide parameter required for the ansible modules on VPLEX
options:
  vplexhost:
    description:
    - IP/FQDN of VPLEX host
    required: true
  vplexuser:
    description:
    - User name to access on to vplexhost
  vplexpassword:
    description:
    - password to access on to vplexhost
  verifycert:
    description:
    - To verify SSL certificate
  ssl_ca_cert:
    description:
    - SSL CA certificate file (.pem format) provided by the user to verify SSL
'''


def get_vplex_management_host_parameters():
    """This method gets the common host parameters of VPLEX"""
    return dict(
        vplexhost=dict(type='str', required=True),
        vplexuser=dict(type='str', required=True),
        vplexpassword=dict(type='str', required=True, no_log=True),
        verifycert=dict(type='bool', required=True),
        ssl_ca_cert=dict(type='str', required=False)
    )


DOCUMENTATION = r'''
---

This method is to initialize logger and return the logger object

parameters:
     - module_name: Name of module to be part of log message.
     - log_file_name: name of the file in which the log messages get appended.
     - log_devel: log level.
returns logger object
'''


def get_logger(module_name, log_file_name='dellemc_ansible_vplex.log',
               log_devel=logging.INFO):
    """This method initializes the logger module"""
    format_string = '%(asctime)-15s %(filename)s %(levelname)s : %(message)s'
    logging.basicConfig(filename=log_file_name, format=format_string)
    log = logging.getLogger(module_name)
    log.setLevel(log_devel)
    return log


DOCUMENTATION = r'''
---

This method is to get vplex setup version in use
It accepts vplexclient.

returns vplex setup version
'''


def get_vplex_setup(vplexclient):
    """Gets VPLEX setup version"""
    ver = VersionApi(vplexclient).get_versions()
    return 'VPLEX setup in use ' + ver[0]['version']


DOCUMENTATION = r'''
---

This method is to validate the name provided by the user
name should not be more than certain number of characters
name should not have special characters except -_
name should start with an alphabet

parameters:
     - name: The name to be validated
     - char_len: Maximum length of the name
     - field: The parameter of the specific module

returns Boolean value and message
'''


def validate_name(name, char_len, field):
    """This method validates the argument for special characters"""
    valid_msg = "Validated the {0} '{1}'".format(field, name)
    if len(name) > int(char_len):
        msg = "The length of {0} should not be".format(field)
        msg = msg + " more than {0} characters".format(char_len)
        return False, msg
    grp = re.search(r"(^[a-zA-Z_][\w\-\_]*$)", name)
    if not grp:
        msg = "{0} should start with an alphabet or '_'".format(field)
        msg = msg + " and only alphanumeric characters and -_ are"
        msg = msg + " allowed"
        return False, msg
    return True, valid_msg


DOCUMENTATION = r'''
---

This method takes the error messages and returns the valid message

parameters:
     - err_input: Represents the entire error statement

returns Valid error message based on the error_code
'''


def error_msg(err_input):
    """This method parses the error code and returns the error message"""
    codes = [400, 404, 409, 500, 501]    # list of error_codes
    content = loads(err_input.body)
    if content['error_code'] in codes:
        content['message'] = re.sub('[^A-Za-z:.,0-9/_-]+', ' ',
                                    content['message'])
        return content['message']
    return err_input


DOCUMENTATION = r'''
---

This method is used to check wether the status of the cluster is degraded.
This occurs if cluster link is disabled.

returns degraded cluster name
'''


def check_status_of_cluster(vplexclient):
    """
    Check the operational status of cluster
    """
    cluster_client = ClustersApi(vplexclient)
    clus_details = cluster_client.get_clusters()
    for cluster in clus_details:
        cluster_info = cluster_client.get_cluster(cluster.name)
        if cluster_info.operational_status == "degraded":
            return cluster.name
    return None
