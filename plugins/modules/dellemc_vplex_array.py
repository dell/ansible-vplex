#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Rediscover Array module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_array
version_added: '1.2.0'
short_description:  Rediscover Array on VPLEX Storage System
description:
- Provisioning the Rediscover Array on VPLEX Storage System

extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex
author:
- Venkatesh Mariyappan (@unknown) <vplex.ansible@dell.com>

options:
  cluster_name:
    description:
    - The name of the VPLEX cluster
    required: true
    type: str

  array_name:
    description:
    - Name of the StorageArray
    required: true
    type: str

  rediscover:
    description:
    - To determine whether rediscover should happen or not
    choices: [true, false]
    default: false
    type: bool

  '''
EXAMPLES = r'''
    - name: Rediscover StorageArray
      dellemc_vplex_array:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        array_name: "EMC-SYMMETRIX-197200581"
        rediscover: true

    - name: Get StorageArray
      dellemc_vplex_array:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        array_name: "EMC-SYMMETRIX-197200581"

'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: End of all the operations
    type: bool
array_details:
    description: Properties of the storage array
    returned: When StorageArray exist in VPLEX
    type: complex
    contains:
        auto_switch:
            description:
                - Whether or not the StorageArray supports auto_switch
            type: bool
        connectivity_status:
            description:
                - StorageArray's connectivity status
            type: str
        controllers:
            description:
                - Name of the controllers
            type: list
        logical_unit_count:
            description:
                - No of Logical units present in the StorageArray
            type: int
        name:
            description:
                - Name of the StorageArray
            type: str
        ports:
            description:
                - Ports present in the StorageArray
            type: list
        storage_array_family:
            description:
                - StorageArray's family
            type: str
        storage_groups:
            description:
                - storage_groups URI of StorageArray
            type: str
        storage_pools:
            description:
                - storage_pools URI of the StorageArray
            type: str

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_array')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexRediscoverArray():
    """Class with VPLEX Rediscover Array operation"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_rediscover_array_parameters())

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
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
        # Create the configuration instance to communicate
        # with vplexapi
        self.client = utils.config_vplexapi(self.module.params)

        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        # Checking if the cluster is reachable
        (err_code, msg) = utils.verify_cluster_name(self.client, self.cl_name)
        if err_code != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource {0}".format(self.cl_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Create an instance to StorageArrayApi to communicate with
        # vplexapi
        self.rediscoverarray = utils.StorageArrayApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_array(self, cluster_name, array_name):
        """
        Get the details of StorageArray
        """
        try:
            obj_array = self.rediscoverarray.get_storage_array(
                cluster_name, array_name)
            LOG.info("Got Array details %s from %s", array_name,
                     cluster_name)
            LOG.debug("StorageArray details:\n%s", obj_array)
            return obj_array
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get StorageArray {0} of {1} due to"
            err_msg = err_msg.format(array_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def rediscover_array(self, cluster_name, array_name):
        """
        Rediscover StorageArray on VPLEX
        """
        try:
            obj_array = self.rediscoverarray.rediscover_storage_array(
                cluster_name, array_name)
            LOG.info("Rediscovered StorageArray in %s", cluster_name)
            LOG.debug("StorageArray details:\n%s", obj_array)
            return obj_array
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not Rediscover array {0} in {1} due to"
            err_msg = err_msg.format(array_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def perform_module_operation(self):
        """
        Perform Rediscover StorageArray operation based on user parameters
        chosen in playbook
        """
        cluster_name = self.module.params['cluster_name']
        array_name = self.module.params['array_name']
        rediscover = self.module.params['rediscover']
        array_present = self.get_array(cluster_name, array_name)

        changed = False
        result = dict(
            changed=False,
            array_details=None
        )
        array_details = utils.serialize_content(array_present)
        if rediscover:
            LOG.info("Rediscover Array %s", array_name)
            obj_array = self.rediscover_array(cluster_name, array_name)
            array_details = utils.serialize_content(obj_array)
            changed = True

        result['changed'] = changed
        result['array_details'] = array_details
        self.module.exit_json(**result)


def get_vplex_rediscover_array_parameters():
    """This method provide the parameters required for the ansible
    rediscover array module on VPLEX"""
    return dict(
        cluster_name=dict(type='str', required=True),
        array_name=dict(type='str', required=True),
        rediscover=dict(type='bool', required=False, default='False',
                        choices=[True, False])
    )


def main():
    """Create VplexRediscoverArray object and perform action on it
        based on user inputs from playbook """
    obj = VplexRediscoverArray()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
