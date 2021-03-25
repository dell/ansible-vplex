#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Initiator module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_initiator
version_added: '1.2.0'
short_description: Manage Initiators on VPLEX Storage Object
description:
- Provisoning the initiator on VPLEX Storage System includes
  Register an initiator,
  Unregister an initiator,
  Get information about initiator (either registered/unregistered),
  Rename a registered initiator name,
  Rediscover Initiators
extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex
author:
- Mohana Priya Sivalingam (@mohanapriya-dell) <vplex.ansible@dell.com>
options:
  cluster_name:
    description:
    - Name of the cluster
    type: str
    required: True

  initiator_name:
    description:
    - Name of the initiator (Registered/Unregistered)
    type: str

  new_initiator_name:
    description:
    - Name of the initiator to be registered or renamed
    type: str

  iscsi_name:
    description:
    - ISCSI name of the port required for registering an initiator
      Mutually exclusive with port_wwn
    type: str

  port_wwn:
    description:
    - Port WWN of FC port required for registering an initiator
      Mutually exclusive with iscsi_name
    type: str

  host_type:
    description:
    - Host type for registering the port
    type: str
    choices: ["default", "hpux", "sun-vcs", "aix", "recoverpoint"]
    default: "default"

  registered:
    description:
    - State of the initiator used for Register/Unregister
    type: bool

  rediscover_timeout:
    description:
    - Allowed time for rediscovery process
    type: int
    default: 1

  state:
    description:
    - The presence of initiator
    type: str
    required: True
    choices: ["present", "absent"]

notes:
- iscsi_name or port_wwn is required to register an initiator
- iscsi_name and port_wwn are mutually exclusive
'''

EXAMPLES = r'''
    - name: Register Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        initiator_name: "ansible_init"
        port_wwn: " 0x10000000c9b82e34"
        host_type: "hpux"
        registered: true
        state: "present"

    - name: Get details of an Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        port_wwn: "0x10000000c9b82e34"
        state: "present"

    - name: Get details of an Initiator with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        initiator_name: "ansible_init"
        state: "present"

    - name: Rename a registered Initiator name with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        port_wwn: "0x10000000c9b82e34"
        new_initiator_name: "ansibe_new_init"
        state: "present"

    - name: Rename a registered Initiator name with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        initiator_name: "ansible_init"
        new_initiator_name: "ansible_init_new"
        state: "present"

    - name: Unregister Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        port_wwn: "0x10000000c9b82e34"
        registered: false
        state: "present"

    - name: Unregister Initiator with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        initiator_name: "ansible_init"
        registered: false
        state: "present"

    - name: Rediscover Initiators
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        state: "present"

    - name: Rediscover Initiators with timeout value set
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        rediscover_timeout: "5"
        state: "present"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Initiator Details:
    description: Details of the initiator
    returned: When initiator exist in VPLEX
    type: complex
    contains:
        bandwidth_limit:
            description: Bandwidth limit of the initiator port
            type: str
        iops_limit:
            description: IOPS limit of the initiator port
            type: int
        iscsi_name:
            description: iscsi_name of the port
            type: str
        name:
            description: Name of the initiator
            type: str
        node_wwn:
            description: Unique network identifier for the HBA's interface card
            type: str
        port_wwn:
            description: Unique network identifier for the port
            type: str
        target_ports:
            description: List of VPLEX ports visible to initiator
            type: list
        type:
            description: Host operating system
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_initiator')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexInitiator():    # pylint:disable=R0902
    """Class with initiator operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_initiator_parameters())

        mutually_exclusive = [
            ['iscsi_name', 'port_wwn']
        ]

        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive
        )

        # Check for external libraries
        lib_status, message = utils.external_library_check()
        if not lib_status:
            LOG.error(message)
            self.module.fail_json(msg=message)

        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        self.cl_name = self.module.params['cluster_name']
        if not self.cl_name:
            msg = "Following is required: cluster_name"
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # Create the configuration instance to communicate with
        # vplexapi
        self.client = utils.config_vplexapi(self.module.params)

        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client  # pylint: disable=W0612
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        # Checking if the cluster is reachable
        (status, msg) = utils.verify_cluster_name(self.client, self.cl_name)
        if status != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource {0}".format(self.cl_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Create an instance to InitiatorApi to communicate with
        # vplexapi
        self.initr = utils.ExportsApi(api_client=self.client)

        # Module parameters
        self.init_name = self.module.params['initiator_name']
        self.new_init_name = self.module.params['new_initiator_name']
        self.port_wwn = self.module.params['port_wwn']
        self.iscsi_name = self.module.params['iscsi_name']
        self.registered = self.module.params['registered']
        self.temp_initiator = None
        self.flag = 0
        self.reg_flag = 0
        self.unreg_flag = 0
        self.rename_flag = 0

        # result is a dictionary that contains changed status and
        # initiator details
        self.result = {"changed": False, "initiator_details": {}}

    def get_initiator(self, initiator_name):
        """
        Get initiator port details
        """
        try:
            initiator_details = self.initr.get_initiator_port(
                self.cl_name, initiator_name)
            LOG.info("Got initiator details %s from %s", initiator_name,
                     self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except utils.ApiException as err:
            err_msg = ("Could not get initiator {0} from {1} due to"
                       " error: {2}".format(initiator_name, self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get initiator {0} from {1} due to"
            err_msg = err_msg.format(initiator_name,
                                     self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def rename_initiator(self, initiator_name, new_initiator_name):
        """
        Rename the initiator port
        """
        try:
            initiator_patch_payload = [{'op': 'replace',
                                        'path': '/name',
                                        'value': new_initiator_name}]
            initiator_details = self.initr.patch_initiator_port(
                self.cl_name, initiator_name, initiator_patch_payload)
            LOG.info("Renamed the initiator %s to %s in %s", initiator_name,
                     new_initiator_name, self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not rename initiator {0} to {1} in {2} due to"
            err_msg = err_msg.format(initiator_name,
                                     new_initiator_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def rediscover_initiator(self, timeout):
        """
        Rediscover initiator ports
        """
        payload = {
            "timeout": timeout,
            "wait": timeout * 5
        }
        try:
            initiator_details = self.initr.rediscover_initiator_ports(
                self.cl_name, rediscover_payload=payload)
            LOG.info("Rediscovered initiators from %s", self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not discover initiators from {0} due to"
            err_msg = err_msg.format(self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def unregister_initiator(self, initiator_name):
        """
        Unregister an initiator port
        """
        try:
            self.initr.unregister_initiator_port(
                self.cl_name, initiator_name)
            LOG.info("Unregistered initiator %s from %s", initiator_name,
                     self.cl_name)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not unregister initiator {0} from {1} due to"
            err_msg = err_msg.format(initiator_name,
                                     self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def register_initiator(self, initiator_payload):
        """
        Register an initiator port either with iscsi_name or port_wwn
        """
        try:
            det = self.initr.register_initiator_port(  # pylint: disable=E1121
                self.cl_name, initiator_payload)
            LOG.info("Registered initiator %s in %s", det.name, self.cl_name)
            LOG.debug("Initiator Details:\n%s", det)
            return det
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not register initiator in {0} due to"
            err_msg = err_msg.format(self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_initiator_payload(self, iscsi_name,  # pylint: disable=R0913, R0201
                              port_wwn, host_type,
                              initiator_name):
        """
        Initiator payload required for registering an initiator
        """
        initiator_payload = dict()
        initiator_payload['iscsi_name'] = iscsi_name
        initiator_payload['port_wwn'] = port_wwn
        initiator_payload['port_name'] = initiator_name
        initiator_payload['type'] = host_type
        LOG.info("Final initiator payload: %s", initiator_payload)
        return initiator_payload

    def check_initiator_flag(self):    # pylint: disable=R0201
        """This method checks for the operation to be performed and sets the
        corresponding flag"""
        if not self.init_name and not self.port_wwn and not self.iscsi_name \
                and not self.new_init_name:
            self.flag = 1
        if self.init_name and self.port_wwn and self.registered:
            self.reg_flag = 1
        elif self.init_name and self.iscsi_name and self.registered:
            self.reg_flag = 1
        if self.init_name and self.new_init_name:
            self.rename_flag = 1
        if self.new_init_name and self.port_wwn:
            self.rename_flag = 1
        elif self.new_init_name and self.iscsi_name:
            self.rename_flag = 1
        if self.init_name and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        if self.port_wwn and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        elif self.iscsi_name and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        return (self.flag, self.reg_flag, self.rename_flag, self.unreg_flag)

    def parse_data(self, object_data):    # pylint: disable=R0201
        """This method parses the fields in the object data and
        returns as a list"""
        parsed_list = []
        for initiator in object_data:
            init_list = []
            dic = {}
            if 'name' in initiator.keys():
                init_list.append('name')
            if 'type' in initiator.keys():
                init_list.append('type')
            if 'port_wwn' in initiator.keys():
                init_list.append('port_wwn')
            if 'iscsi_name' in initiator.keys():
                init_list.append('iscsi_name')
            dic = {init_list[i]: initiator[init_list[i]]
                   for i in range(len(init_list))}
            parsed_list.append(dic)
        return parsed_list

    def validate_name(self, name, field):    # pylint: disable=R0201
        """This method validates the name length and non-presence of
        special characters"""
        char_len = '36'
        status, msg = utils.validate_name(name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def check_name(self, name, search_data):
        """This method checks for port_wwn/iscsi_name from initiators list"""
        for data in search_data:
            for dummy, val in data.items():
                if name == val:
                    self.temp_initiator = data['name']
                    msg = ("Actual initiator name for {0} is {1}".format(
                        name, self.temp_initiator))
                    LOG.info(msg)
                    return True
        return False

    def perform_module_operation(self):    # pylint: disable=R0912,R0914,R0915
        """
        Perform different actions on the initiator based on user parameters
        specified in the playbook
        """
        state = self.module.params['state']
        host_type = self.module.params['host_type']
        rediscover_timeout = self.module.params['rediscover_timeout']
        init_details = None
        initiator_details = None
        new_init_details = None
        temp_details = None
        init_dict = None
        changed = False

        def exit_module(changed, initiator_details):
            self.result["changed"] = changed
            if initiator_details:
                initiator_details = utils.serialize_content(initiator_details)
            self.result["initiator_details"] = initiator_details
            self.module.exit_json(**self.result)

        if not (0 < rediscover_timeout < 3601):
            msg = "Invalid timeout value. The valid range is from 1 to 3600."
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Perform rediscover initiators and keep it for idempotency
        details = self.rediscover_initiator(rediscover_timeout)

        # Check for initiator relevant operation flag
        (self.flag, self.reg_flag, self.rename_flag, self.unreg_flag) = \
            self.check_initiator_flag()

        # Rediscover initiators if initiator_name is not present
        if self.flag and self.registered is None:
            changed = True
            exit_module(changed, details)

        # Collect the list of dictionaries with initiator names, port_wwn
        # and iscsi_name
        obj = utils.serialize_content(details)
        init_dict = self.parse_data(obj)

        # Validate the initiator_name
        if self.init_name:
            self.validate_name(self.init_name, 'initiator_name')

        # Check for initiator/port_wwn/iscsi_name presence
        if self.flag:
            err_msg = ("Could not find initiator_name, port_wwn/iscsi_name"
                       " in user parameters. Required one of the options")
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Check for port_wwn is valid
        if self.port_wwn and not self.reg_flag \
                and not self.check_name(self.port_wwn, init_dict):
            err_msg = ("Could not match port_wwn {0} in {1}. Re-enter the"
                       " correct port_wwn".format(self.port_wwn,
                                                  self.cl_name))
            LOG.error(err_msg)
            if state == "present":
                self.module.fail_json(msg=err_msg)
            else:
                exit_module(changed, initiator_details)

        # Check for iscsi_name is valid
        if self.iscsi_name and not self.reg_flag \
                and not self.check_name(self.iscsi_name, init_dict):
            err_msg = ("Could not match iscsi_name {0} in {1}. Re-enter the"
                       " correct iscsi_name".format(self.iscsi_name,
                                                    self.cl_name))
            LOG.error(err_msg)
            if state == "present":
                self.module.fail_json(msg=err_msg)
            else:
                exit_module(changed, initiator_details)

        # Get the details of given initiator
        if self.init_name:
            init_details = self.get_initiator(self.init_name)

        # Check for initiator name is valid for operations except register
        if self.init_name and init_details is None and not self.reg_flag:
            err_msg = ("Could not find initiator_name {0} from {1}".format(
                self.init_name, self.cl_name))
            LOG.error(err_msg)
            if state == "present":
                self.module.fail_json(msg=err_msg)
            else:
                exit_module(changed, init_details)

        # Get the details of port_wwn/iscsi_name specific initiator
        if self.temp_initiator:
            temp_details = self.get_initiator(self.temp_initiator)

        # Register an initiator
        if self.reg_flag:
            if self.rename_flag:
                msg = "Could not perform register and rename in a single " \
                    "task. Please specify each operation in individual task."
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            if init_details and init_details.type is not None:
                if self.port_wwn and init_details.port_wwn != self.port_wwn:
                    err_msg = ("Could not register initiator {0} as it is"
                               " already registered with different port_wwn"
                               " {1} in {2}. Please specify different"
                               " initiator_name".format(
                                   self.init_name, init_details.port_wwn,
                                   self.cl_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                elif self.iscsi_name and \
                        init_details.iscsi_name != self.iscsi_name:
                    err_msg = ("Could not register initiator {0} as it is"
                               " already registered with different iscsi_name"
                               " {1} in {2}. Please specify different"
                               " initiator_name".format(
                                   self.init_name, init_details.iscsi_name,
                                   self.cl_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            elif init_details and init_details.type is None:
                err_msg = ("Could not register with initiator_name {0} in {1}"
                           " as it is already in use. Plese specify different"
                           " initiator_name".format(
                               self.init_name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            # Check register operation with respect to port_wwn
            if self.check_name(self.port_wwn, init_dict):
                temp_details = self.get_initiator(self.temp_initiator)
                init_id = self.port_wwn
                name_id = 'port_wwn'
            # Check register operation with respect to iscsi_name
            elif self.check_name(self.iscsi_name, init_dict):
                temp_details = self.get_initiator(self.temp_initiator)
                init_id = self.iscsi_name
                name_id = 'iscsi_name'
            if temp_details is not None and temp_details.type is not None:
                if host_type == temp_details.type and \
                        temp_details.name != self.init_name:
                    err_msg = ("Could not register initiator of {0} {1} with"
                               " initiator_name {2} in {3} as it is already"
                               " registered with different name {4}".format(
                                   name_id, init_id, self.init_name,
                                   self.cl_name, temp_details.name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                elif host_type == temp_details.type and \
                        temp_details.name == self.init_name:
                    msg = ("Initiator {0} with {1} {2} in {3} is"
                           " already registered".format(
                               self.init_name, name_id, init_id,
                               self.cl_name))
                    initiator_details = temp_details
                    LOG.info(msg)
                elif host_type != temp_details.type:
                    err_msg = ("Could not register initiator of {0} {1} with"
                               " initiator_name {2} in {3} as it is already"
                               " registered with different host_type"
                               " {4}".format(
                                   name_id, init_id, self.init_name,
                                   self.cl_name, temp_details.type))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)

            # Perform registering the initiator
            else:
                initiator_payload = self.get_initiator_payload(
                    self.iscsi_name, self.port_wwn, host_type, self.init_name)
                initiator_details = self.register_initiator(
                    initiator_payload)
                init_details = initiator_details
                changed = True
                self.temp_initiator = self.init_name
                temp_details = initiator_details

        # Renaming an initiator
        if self.rename_flag:
            if self.port_wwn or self.iscsi_name and self.new_init_name:
                self.init_name = self.temp_initiator
                init_details = temp_details
            if self.new_init_name:
                if self.init_name == self.new_init_name:
                    msg = ("initiator_name and new_initiator_name are"
                           " same")
                    initiator_details = init_details
                    LOG.info(msg)
                else:
                    # Get the details of given new initiator
                    new_init_details = self.get_initiator(self.new_init_name)
                    if new_init_details is not None:
                        err_msg = ("Could not rename initiator {0} in {1}."
                                   " new_initiator_name {2} is already present"
                                   ". Specify a different name".format(
                                       self.init_name, self.cl_name,
                                       self.new_init_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
                    # Perform renaming the initiator
                    else:
                        # Validate the new initiator_name
                        self.validate_name(self.new_init_name,
                                           'new_initiator_name')
                        initiator_details = self.rename_initiator(
                            self.init_name, self.new_init_name)
                        init_details = initiator_details
                        changed = True

        # Unregister an initiator
        if self.unreg_flag:
            if self.init_name:
                if init_details.type is None:
                    msg = ("Initiator {0} in {1} is already"
                           " unregistered".format(self.init_name,
                                                  self.cl_name))
                    LOG.info(msg)
                    exit_module(changed, initiator_details)
                else:
                    self.temp_initiator = self.init_name
            elif self.port_wwn or self.iscsi_name:
                if temp_details.type is None:
                    msg = ("Initiator {0} in {1} is already"
                           " unregistered".format(self.temp_initiator,
                                                  self.cl_name))
                    LOG.info(msg)
                    exit_module(changed, initiator_details)
            # Perform unregister initiator
            self.unregister_initiator(self.temp_initiator)
            changed = True
            initiator_details = None

        # Get initiator
        if not self.reg_flag and not self.unreg_flag \
                and not self.rename_flag:
            if self.port_wwn or self.iscsi_name and not self.init_name:
                init_details = temp_details
            initiator_details = init_details

        # Finally call the exit module
        exit_module(changed, initiator_details)


def get_vplex_initiator_parameters():
    """This method provide parameter required for the ansible initiator
    module on VPLEX"""
    return dict(
        cluster_name=dict(required=True, type='str'),
        initiator_name=dict(required=False, type='str'),
        new_initiator_name=dict(required=False, type='str'),
        iscsi_name=dict(required=False, type='str'),
        port_wwn=dict(required=False, type='str'),
        host_type=dict(required=False, type='str', default='default',
                       choices=['default', 'hpux', 'sun-vcs', 'aix',
                                'recoverpoint']),
        registered=dict(required=False, type='bool'),
        rediscover_timeout=dict(required=False, type='int', default=1),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """Create VplexInitiator object and perform action on it
        based on user input from playbook"""
    obj = VplexInitiator()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
