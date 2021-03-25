# Copyright: (c) 2020, Dell EMC.

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type


class ModuleDocFragment(object):    # pylint: disable=R0205,R0903

    DOCUMENTATION = r'''
options:
  - See respective platform section for more details
requirements:
  - See respective platform section for more details
notes:
  - Ansible modules are available for EMC VPLEX Storage Platform
'''

    # Documentation fragment for VPLEX (dellemc_vplex)
    VPLEX = r'''
options:
    vplexhost:
        description:
            - IP or FQDN of the VPLEX host
        type: str
        required: True
    vplexuser:
        description:
            - username of the VPLEX host.
        type: str
        required: True
    vplexpassword:
        description:
            - the password of the VPLEX host.
        type: str
        required: True
    verifycert:
        description:
            - boolean variable to specify whether to validate SSL
              certificate or not.
            - True - indicates that the SSL certificate should be
                     verified.
            - False - indicates that the SSL certificate should not be
                      verified.
        type: bool
        required: True
    ssl_ca_cert:
        description:
            - SSL CA certificate file (.pem format) provided by the
              user to verify SSL
        type: str
    debug:
        description:
            - To specify whether to have debug statements from vplexapi
              in log file or not
        type: bool
    vplex_timeout:
        description:
            - the network connectivity timeout value to connect to VPLEX
              host in seconds
        type: int
        default: 30

requirements:
  - A DellEMC VPLEX Storage device.
  - Ansible 2.7.
notes:
  - The modules prefixed with dellemc_vplex are built to support the
    DellEMC VPLEX storage platform.
'''
