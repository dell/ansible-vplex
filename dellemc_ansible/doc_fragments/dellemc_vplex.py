# -*- coding: utf-8 -*-    # pylint: disable=C0114

# Copyright: (c) 2020, Dell EMC.


class ModuleDocFragment(object):    # pylint: disable=C0115,R0205,R0903

    DOCUMENTATION = r'''
options:
  - See respective platform section for more details
requirements:
  - See respective platform section for more details
notes:
  - Ansible modules are available for EMC VPLEX Storage Platform
'''

    # Documentation fragment for VPLEX (dellemc_vplex)
    DELLEMC_VPLEX = r'''
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
        choices: [ True, False]

requirements:
  - A DellEMC VPLEX Storage device.
  - Ansible 2.7.
notes:
  - The modules prefixed with dellemc_vplex are built to support the
    DellEMC VPLEX storage platform.
'''
