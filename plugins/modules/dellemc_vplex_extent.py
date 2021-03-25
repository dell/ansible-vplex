#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Extent module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_extent
version_added: '1.2.0'
short_description: Manage Extents on VPLEX Storage Object
description:
- Provisioning the storage extent on VPLEX Storage System includes
  Create a new extent,
  Delete an existing extent,
  Get information about existing extent,
  Rename existing extent,
extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex
author:
- Sherene Jean Prathiba (@sherenevinod-dell) <vplex.ansible@dell.com>

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

notes:
- storage_volume_name or storage_volume_id or extent_name is required
- storage_volume_name or storage_volume_id and extent_name is
  required to create extent
- storage_volume_name and storage_volume_id are mutually exclusive
'''

EXAMPLES = r'''
    - name: Create Extent using storage volume name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        extent_name: "ansible_extent_1"
        storage_volume_name: "ansible_st_vol"
        state: "present"

    - name: Get Extent using extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        extent_name: "ansible_extent"
        state: "present"

    - name: Delete Extent using extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        extent_name: "ansible_extent"
        state: "absent"

    - name: Rename Extent using the extent name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        new_extent_name: "ansible_extent_new_name"
        extent_name: "ansible_extent"
        state: "present"

    - name: Rename Extent using the storage volume name
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        new_extent_name: "ansible_extent_new_name"
        storage_volume_name: "ansible_st_vol"
        state: "present"

    - name: Rename Extent using the storage volume id
      dellemc_vplex_extent:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        new_extent_name: "ansible_extent_new_name"
        storage_volume_id: "VPD83T3:60000970000197200581533030353438"
        state: "present"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Extent Details:
    description: Details of the extent
    returned: When extent exists in VPLEX
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
            type: str
        io_status:
            description: The device is alive or not
            type: str
        locality:
            description: Placement of the extent. Either Local or distributed
                         or remote
            type: str
        operational_status:
            description: The functional status of the extent
            type: str
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

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_extent')
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
            ['storage_volume_name', 'storage_volume_id']
        ]
        required_one_of = [
            ['storage_volume_name', 'storage_volume_id', 'extent_name']
        ]
        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of
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
        self.state = self.module.params['state']
        if not self.cl_name:
            msg = "Following is required: cluster_name"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Create the configuration instance to communicate with
        # vplexapi
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

        # Create an instance to ExtentApi to communicate with
        # vplexapi
        self.extent = utils.ExtentApi(api_client=self.client)
        self.stor_obj = utils.StorageVolumeApi(api_client=self.client)

        # result is a dictionary that contains changed status and
        # extent details
        self.result = {"changed": False, "extent_details": {}}

    def get_extent(self, extent_name):
        """
        Get extent details
        """
        try:
            extent_details = self.extent.get_extent(self.cl_name, extent_name)
            LOG.info("Got extent %s details from %s", extent_name,
                     self.cl_name)
            LOG.debug("Extent Details:\n%s", extent_details)
            return extent_details
        except utils.ApiException as err:
            err_msg = ("Could not get extent {0} from {1} due to"
                       " error: {2}".format(
                           extent_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            body = utils.loads(err.body)
            if self.resource_fail_msg in body['message']:
                self.module.fail_json(msg=self.fail_msg.format(self.cl_name))
        except (ValueError, TypeError) as err:
            err_msg = "Could not get extent {0} from {1} due to"
            err_msg = err_msg.format(extent_name, self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

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
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not rename extent {0} to name {1} in {2} due to"
            err_msg = err_msg.format(extent_name, new_extent_name,
                                     self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def delete_extent(self, extent_name):
        """
        Delete an extent
        """
        try:
            self.extent.delete_extent(self.cl_name, extent_name)
            LOG.info("Deleted extent %s from %s", extent_name, self.cl_name)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not delete extent {0} from {1} due to"
            err_msg = err_msg.format(extent_name, self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def create_extent(self, stor_vol, storvol_details, ext_name):
        """
        Create an extent on a storage volume
        """
        if not storvol_details:
            stor = stor_vol
            (used, ext, storvol) = \
                self.is_storvol_inuse(stor, ext_name)  # pylint:disable=W0612
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
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not create extent on {0} in {1} due to"
            err_msg = err_msg.format(stor_vol, self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def is_storvol_inuse(self, stor_vol, ext_name):
        """
        Get the status of the storage volume
        """
        try:
            extent_details = None
            use = None
            details = None
            details = self.stor_obj.get_storage_volume(self.cl_name, stor_vol)
            LOG.info("Got the details of storage volume %s in %s", stor_vol,
                     self.cl_name)
            if details:
                if details.use == "used":
                    extent_name = details.used_by[0].split('/')[-1]
                    extent_details = self.get_extent(extent_name)
                    if extent_details:
                        LOG.info("The storage volume %s contains an extent"
                                 " %s in %s", stor_vol, extent_name,
                                 self.cl_name)
                else:
                    if ext_name is None and self.state != 'absent':
                        msg = "Could not get extent details from {0} "\
                            "because it has no extent on it".format(stor_vol)
                        LOG.error(msg)
                        self.module.fail_json(msg=msg)
                use = details.use
            return (use, extent_details, details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get storage volume details {0} from {1} due"
            err_msg = err_msg.format(stor_vol, self.cl_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_storvol_name(self, stor_id):
        """
        Get the name of the storage volume with the storage volume ID
        """
        stor_vol_name = None
        try:
            stor_vol_list = self.stor_obj.get_storage_volumes(self.cl_name)
            for stor_vol in stor_vol_list:
                if stor_vol.system_id == stor_id:
                    stor_vol_name = stor_vol.name
            LOG.info("Got storage volume name %s from storage volume ID %s",
                     stor_vol_name, stor_id)
            return stor_vol_name
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get storage volume ID {0} from {1} due to"
            err_msg = err_msg.format(stor_id, self.cl_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def name_check(self, extent_name, field):
        """Check the validity of extent name """
        char_len = '63'
        status, msg = utils.validate_name(extent_name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

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

        # Check validity of given extent name
        if extent_name is not None:
            self.name_check(extent_name, 'extent_name')
        # Get the storage volume name from ID
        if storage_volume_id:
            storage_volume_name = self.get_storvol_name(storage_volume_id)
            if not storage_volume_name:
                err_msg = ("Could not get storage volume name from ID {0} in"
                           " {1}".format(storage_volume_id, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

        # Get the extent details if the storage volume is in use
        if storage_volume_name:
            stor = storage_volume_name
            ext_name = extent_name
            (used, extent_info, storvol) = \
                self.is_storvol_inuse(stor, ext_name)  # pylint:disable=W0612
            if extent_name:
                ext_info = self.get_extent(extent_name)
                if extent_info is not None and ext_info is not None:
                    if ext_info.name == extent_info.name:
                        extent_info = ext_info
                        msg = "{0} is already created".format(extent_name)
                        LOG.info(msg)
                    else:
                        msg = "Could not create {0} in {1} because an extent"\
                            " already exists on given storage volume".format(
                                extent_name, self.cl_name)
                        LOG.error(msg)
                        self.module.fail_json(msg=msg)
                elif extent_info is None and ext_info is not None:
                    msg = "Could not create {0} in {1} because given extent "\
                        "name already exists".format(
                            extent_name, self.cl_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                elif ext_info is None and extent_info is not None:
                    msg = "Could not create {0} in {1} because given "\
                        "storage volume is in use".format(
                            extent_name, self.cl_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

        # Getting the details of the extent if extent_name is present
        if extent_name and not extent_info:
            extent_info = self.get_extent(extent_name)

        if extent_info and state == 'absent':
            if extent_info.use == "used":
                name = extent_info.name
                err_msg = ("Could not delete extent {0} from {1}. Extent is"
                           " occupied".format(name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            self.delete_extent(extent_info.name)
            changed = True
            extent_details = None

        elif not extent_info and state == 'absent':
            if extent_name:
                msg = ("Could not get extent details {0} from {1}."
                       " Extent is not present.".format(
                           extent_name, self.cl_name))
                LOG.info(msg)
            elif storage_volume_name:
                msg = ("Extent is not present in storage volume {0}"
                       " in {1}".format(storage_volume_name, self.cl_name))
                LOG.info(msg)

        elif not extent_info and state == 'present':
            # If storage volume name is given create an extent
            if storage_volume_name and extent_name is not None:
                if new_extent_name:
                    msg = "Could not perform create and rename in a "\
                        "single task. Please specify each operation in "\
                        "individual task."
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                ext = self.create_extent(
                    storage_volume_name, storvol, extent_name)
                if ext.name == extent_name:
                    LOG.info("Created extent {0} and extent name are same")
                else:
                    ext = self.rename_extent(ext.name, extent_name)
                    extent_details = ext
                    extent_info = ext
                changed = True
            elif storage_volume_name and extent_name is None:
                msg = "extent_name is required for creating an extent"
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            elif extent_name:
                err_msg = ("Could not get extent details {0} from {1}."
                           " Extent is not present.".format(
                               extent_name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

        if extent_info and state == 'present':
            extent_details = extent_info
            # Getting the details of the extent if new_extent_name is present
            if (new_extent_name and (new_extent_name == extent_info.name)):
                LOG.info("Extent name and New extent name are the same")
            elif new_extent_name:
                new_extent_info = self.get_extent(new_extent_name)
                if new_extent_info:
                    err_msg = ("Could not rename extent {0} in {1}. Extent"
                               " with name {2} is already present".format(
                                   extent_info.name, self.cl_name,
                                   new_extent_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)

                if not new_extent_info:
                    # Validating the new_extent_name
                    self.name_check(new_extent_name, 'new_extent_name')
                    extent_details = self.rename_extent(extent_info.name,
                                                        new_extent_name)
                    changed = True

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
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """Create VplexExtent object and perform action on it
        based on user input from playbook"""
    obj = VplexExtent()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
