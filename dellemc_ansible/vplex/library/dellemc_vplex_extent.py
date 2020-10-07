""" Extent module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import json
import logging
import urllib3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
        dellemc_ansible_vplex_utils as utils
from vplexapi.api import ExtentApi
from vplexapi.api import StorageVolumeApi
from vplexapi.rest import ApiException
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_extent
version_added: '2.7'
short_description: Manage Extents on VPLEX Storage Object
description:
- Provisioning the storage extent on VPLEX Storage System includes
  Create a new extent,
  Delete an existing extent,
  Get information about existing extent,
  Rename existing extent,
extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex
author: Sherene Jean Prathiba (sherene_jean_pratibh@dellteam.com)
        vplex.ansible@dell.com

options:
  cluster_name:
    description:
    - Name of the cluster
    type: str
    required: True

  storage_volume_name:
    description:
    - Name of the storage volume on which the extent will be created
      Mutually exclusive with storage_volume_id and extent_name
    type: str

  storage_volume_id:
    description:
    - ID of the storage volume on which the extent will be created
      Mutually exclusive with storage_volume_name and extent_name
    type: str

  extent_name:
    description:
    - Name of the extent
      Mutually exclusive with storage_volume_name and storage_volume_id
    type: str

  new_extent_name:
    description:
    - New name of the extent for rename operation
    type: str

  state:
    description:
    - Defines whether the extent should exist or not
    type: str
    choices: ["absent", "present"]
    required: True

Notes:
- storage_volume_name or storage_volume_id or extent_name is required
- storage_volume_name or storage_volume_id is required to create extent
- storage_volume_name, storage_volume_id and extent_name are
  mutually exclusive
'''

EXAMPLES = r'''
    - name: Create Extent using storage volume name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        storage_volume_name: "{{ storage_volume_name }}"
        state: "present"

    - name: Get Extent using extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        extent_name: "{{ extent_name }}"
        state: "present"

    - name: Delete Extent using extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        extent_name: "{{ extent_name }}"
        state: "absent"

    - name: Rename Extent using the extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        new_extent_name: "{{ new_extent_name }}"
        extent_name: "{{ extent_name }}"
        state: "present"

    - name: Rename Extent using the storage volume name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        new_extent_name: "{{ new_extent_name }}"
        storage_volume_name: "{{ storage_volume_name }}"
        state: "present"

    - name: Rename Extent using the storage volume id
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        new_extent_name: "{{ new_extent_name }}"
        storage_volume_id: "{{ storage_volume_id }}"
        state: "present"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Extent Details:
    description: Details of the extent
    returned: For Create, Get and Rename operations
    type: complex
    contains:
        name:
            description: Name of the extent
            type: str
        block_count:
            description: Number of blocks in the extent
            type: int
        block_offset:
            description: The block_offset on the underlying storage volume
            type: int
        block_size:
            description: Block_size of the extent
            type: str
        capacity:
            description: Size of the extent
            type: str
        health_indications:
            description: If health-state is not ok, additional information
            type: list
        health_state:
            description: Health state of the extent
            type: enum
        io_status:
            description: The device is alive or not
            type: str
        locality:
            description: Placement of the extent. Either Local or distributed
                         or remote
            type: enum
        operational_status:
            description: The functional status of the extent
            type: enum
        storage_array_family:
            description: The storage array family name
            type: str
        storage_volume:
            description: Name of the storage volume over which the extent is
                         created
            type: str
        storage_volumeType:
            description: The storage volume type
            type: str
        system_id:
            description: Unique ID of the extent
            type: str
        thin_capable:
            description: Thin provisioning support
            type: bool
        underlying_storage_block_size:
            description: Size of the storage volume block
            type: int
        use:
            description: Status of the extent
            type: str
        used_by:
            description: Device list which use the extent
            type: list
        vendor_specific_name:
            description: Vendor specific name
            type: str

'''

LOG = utils.get_logger('dellemc_vplex_extent', log_devel=logging.INFO)
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexExtent():  # pylint:disable=R0902
    """Class with extent operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_extent_parameters())
        self.resource_fail_msg = "Failed to collect resources"
        self.fail_msg = "Could not collect resources in {0}"

        mutually_exclusive = [
            ['storage_volume_name', 'storage_volume_id',
             'extent_name']
        ]

        required_one_of = [
            ['storage_volume_name', 'storage_volume_id',
             'extent_name']
        ]
        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of
        )

        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        self.cl_name = self.module.params['cluster_name']

        # Create the configuration instance to communicate with
        # vplexapi
        self.client = utils.config_vplexapi(self.module.params)

        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Checking if the cluster is reachable
        (err_code, msg) = utils.verify_cluster_name(self.client, self.cl_name)
        if err_code != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource {0}".format(self.cl_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Create an instance to ExtentApi to communicate with
        # vplexapi
        self.extent = ExtentApi(api_client=self.client)

        # result is a dictionary that contains changed status and
        # extent details
        self.result = {"changed": False, "extent_details": {}}

    def get_extent(self, extent_name):
        """
        Get extent details
        """
        try:
            extent_details = self.extent.get_extent(self.cl_name, extent_name)
            LOG.info("Got extent details %s from %s", extent_name,
                     self.cl_name)
            LOG.debug("Extent Details:\n%s", extent_details)
            return extent_details
        except ApiException as err:
            err_msg = ("Could not get extent {0} from {1} due to"
                       " error: {2}".format(
                           extent_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            body = json.loads(err.body)
            if self.resource_fail_msg in body['message']:
                self.module.fail_json(msg=self.fail_msg.format(self.cl_name))

    def rename_extent(self, extent_name, new_extent_name):
        """
        Rename the extent
        """
        try:
            ext_payload = [{'op': 'replace',
                            'path': '/name',
                            'value': new_extent_name}]
            extent_details = self.extent.patch_extent(self.cl_name,
                                                      extent_name, ext_payload)
            LOG.info("Renamed the extent %s to %s in %s", extent_name,
                     new_extent_name, self.cl_name)
            LOG.debug("Extent Details:\n%s", extent_details)
            return extent_details
        except ApiException as err:
            err_msg = ("Could not rename extent {0} to name {1} in {2} due to"
                       " error: {3}".format(
                           extent_name, new_extent_name, self.cl_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def delete_extent(self, extent_name):
        """
        Delete an extent
        """
        try:
            self.extent.delete_extent(self.cl_name, extent_name)
            LOG.info("Deleted extent %s from %s", extent_name, self.cl_name)
            return True
        except ApiException as err:
            err_msg = ("Could not delete extent {0} from {1} due to"
                       " error: {2}".format(
                           extent_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def create_extent(self, stor_vol, storvol_details):
        """
        Create an extent on a storage volume
        """
        if not storvol_details:
            stor = stor_vol
            (used, ext, storvol) = \
                self.is_storvol_inuse(stor)  # pylint:disable=W0612
        else:
            used = storvol_details.use

        if used == "unclaimed":
            err_msg = ("Could not create extent as the storage volume {0}"
                       " is unclaimed".format(stor_vol))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)
        elif used is None:
            err_msg = ("Could not get storage volume {0} from"
                       " {1}".format(stor_vol, self.cl_name))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        path = "/vplex/v2/clusters/" + self.cl_name + "/storage_volumes/"
        stor_vol = path + stor_vol
        ex_payload = {'storage_volume': stor_vol}
        try:
            ext_details = self.extent.create_extent(self.cl_name, ex_payload)
            LOG.info("Created extent %s on %s", ext_details.name, self.cl_name)
            LOG.debug("Extent Details:\n%s", ext_details)
            return ext_details
        except ApiException as err:
            err_msg = ("Could not create extent on {0} in {1} due to"
                       " error: {2}".format(
                           stor_vol, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def is_storvol_inuse(self, stor_vol):
        """
        Get the status of the storage volume
        """
        # Create an instance to ExtentApi to communicate with
        # vplexapi
        stor_obj = StorageVolumeApi(api_client=self.client)
        try:
            extent_details = None
            use = None
            details = None
            details = stor_obj.get_storage_volume(self.cl_name, stor_vol)
            LOG.info("Got the details of storage volume %s of %s", stor_vol,
                     self.cl_name)
            if details:
                if details.use == "used":
                    extent_name = details.used_by[0].split('/')[-1]
                    extent_details = self.get_extent(extent_name)
                use = details.use
            return (use, extent_details, details)
        except ApiException as err:
            err_msg = ("Could not get storage volume details {0} from {1} due"
                       " to error: {2}".format(
                           stor_vol, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def get_storvol_name(self, stor_id):
        """
        Get the name of the storage volume with the storage volume ID
        """
        # Create an instance to ExtentApi to communicate with
        # vplexapi
        stor_obj = StorageVolumeApi(api_client=self.client)
        stor_vol_name = None

        try:
            stor_vol_list = stor_obj.get_storage_volumes(self.cl_name)
            for stor_vol in stor_vol_list:
                if stor_vol.system_id == stor_id:
                    stor_vol_name = stor_vol.name
            LOG.info("Got storage volume name %s from storage volume ID %s",
                     stor_vol_name, stor_id)
            return stor_vol_name
        except ApiException as err:
            err_msg = ("Could not get storage volume ID {0} from {1} due to"
                       " error: {2}".format(
                           stor_id, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def perform_module_operation(self):    # pylint:disable=R0915, R0912, R0914
        """
        Perform different actions on the extent based on user parameters
        specified in the playbook
        """
        state = self.module.params['state']
        extent_name = self.module.params['extent_name']
        storage_volume_name = self.module.params['storage_volume_name']
        storage_volume_id = self.module.params['storage_volume_id']
        new_extent_name = self.module.params['new_extent_name']
        extent_details = None
        extent_info = None
        new_extent_info = None
        changed = False

        # Checking for wrong user inputs
        if new_extent_name and state == 'absent':
            msg = "When new extent name is given state can not be absent"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Validating the new_extent_name
        if new_extent_name:
            char_len = '60'
            status, msg = utils.validate_name(new_extent_name, char_len,
                                              'new_extent_name')
            if not status:
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            else:
                LOG.info(msg)

        # Get the storage volume name from ID
        if storage_volume_id:
            storage_volume_name = self.get_storvol_name(storage_volume_id)
            if not storage_volume_name:
                err_msg = ("Could not get storage volume name from ID {0} in"
                           "  {1}".format(storage_volume_id, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

        # Get the extent details if the storage volume is in use
        if storage_volume_name:
            stor = storage_volume_name
            (used, extent_info, storvol) = \
                self.is_storvol_inuse(stor)  # pylint:disable=W0612

        # Getting the details of the extent if extent_name is present
        if extent_name:
            extent_info = self.get_extent(extent_name)

        # Getting the details of the extent if new_extent_name is present
        if new_extent_name:
            new_extent_info = self.get_extent(new_extent_name)

        if extent_info and state == 'present':
            if not new_extent_name:
                extent_details = extent_info
            elif new_extent_info:
                if new_extent_info.name == extent_info.name:
                    LOG.info("Extent name and New extent name are the same")
                    extent_details = extent_info
                else:
                    err_msg = ("Could not rename extent {0} in {1}. Extent"
                               " with name {2} is already present".format(
                                   extent_name, self.cl_name, new_extent_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            elif new_extent_name and not new_extent_info:
                extent_details = self.rename_extent(extent_info.name,
                                                    new_extent_name)
                changed = True

        elif extent_info and state == 'absent':
            if extent_info.use == "used":
                name = extent_info.name
                err_msg = ("Could not delete extent {0} from {1}. Extent is"
                           " occupied".format(name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            self.delete_extent(extent_info.name)
            changed = True
            extent_details = None

        elif not extent_info and state == 'present':
            # If storage volume name is given create an extent
            if storage_volume_name:
                ext = self.create_extent(storage_volume_name, storvol)
                extent_details = ext
                changed = True
            else:
                err_msg = ("Could not get extent details {0} from {1}."
                           " Extent is not present".format(
                               extent_name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            # If storage volume name and new extent name are given
            # Create an extent and rename it  with the new extent name
            if new_extent_name:
                if new_extent_name and not new_extent_info:
                    extent_details = self.rename_extent(extent_details.name,
                                                        new_extent_name)
                    changed = True
                elif new_extent_info:
                    err_msg = ("Could not rename extent {0} in {1}. Extent"
                               " with name {2} is already present".format(
                                   extent_name, self.cl_name, new_extent_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                    extent_details = None
                    changed = False
                elif new_extent_info.name == extent_details.name:
                    LOG.info("Extent name and New extent name are the same")

        elif not extent_info and state == 'absent':
            LOG.info("Could not get extent details")

        # Finally update the module changed state details
        self.result["changed"] = changed
        if extent_details:
            ext = utils.serialize_content(extent_details)
            extent_details = ext
        self.result["extent_details"] = extent_details
        self.module.exit_json(**self.result)


def get_vplex_extent_parameters():
    """This method provide parameter required for the ansible extent
    module on VPLEX"""
    return dict(
        cluster_name=dict(required=True, type='str'),
        extent_name=dict(required=False, type='str'),
        new_extent_name=dict(required=False, type='str'),
        storage_volume_name=dict(required=False, type='str'),
        storage_volume_id=dict(required=False, type='str'),
        state=dict(required=True, type='str')
    )


def main():
    """Create VplexExtent object and perform action on it
        based on user input from playbook"""
    obj = VplexExtent()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
