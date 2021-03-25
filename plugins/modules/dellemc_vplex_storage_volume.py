#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Storage Volume module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_storage_volume
version_added: '1.2.0'
short_description: Manage VPLEX storage volume
description:
- Based on the user inputs performs claim, unclaim, update
  operations on storage volume
extends_documentation_fragment:
- dellemc.vplex.dellemc_vplex.vplex
author:
- Amit Uniyal (@euniami-dell) <vplex.ansible@dell.com>

options:
  cluster_name:
    description:
    - Name of the cluster
    required: True
    type: str

  storage_volume_name:
    description:
    - Name of the storage volume
      storage_volume_id is mutually exclusive with storage_volume_name
    type: str

  storage_volume_id:
    description:
    - ID of the storage volume or volume system_id
    type: str

  new_storage_volume_name:
    description:
    - Defines to rename storage volume name
    type: str

  thin_rebuild:
    description:
    - Defines to update thin_rebuild
    type: bool

  get_itls:
    description:
    - Defines to retrieve itls list
    type: bool

  claimed_state:
    description:
    - Defines to claim unclaimed storage volume
    choices: ['claimed', 'unclaimed']
    type: str

  state:
    description:
    - Defines whether the volume should exist or not.
    required: True
    choices: ['present', 'absent']
    type: str
'''

EXAMPLES = r'''
- name: Claim Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    storage_volume_name: "ansible_st_vol"
    claimed_state: "claimed"
    state: "present"

- name: Unclaim Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    storage_volume_name: "ansible_st_vol"
    claimed_state: "unclaimed"
    state: "present"

- name: Get itls list of Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    storage_volume_name: "ansible_st_vol"
    get_itls: true
    claimed_state: "claimed"
    state: "present"

- name: Update Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    storage_volume_name: "ansible_st_vol"
    new_storage_volume_name: "ansible_st_vol_new_name"
    thin_rebuild: true
    claimed_state: "claimed"
    state: "present"

'''

RETURN = r'''
changed:
    description: Whether or not the storage volume has changed
    returned: End of all the operations
    type: bool

volume_details:
    description: Details of the storage volume
    returned: When storage volume exist in VPLEX
    type: complex
    contains:
        application_consistent:
            description: Application consistent
            type: bool
        block_count:
            description: Number of blocks
            type: int
        block_size:
            description: Block size
            type: int
        capacity:
            description: Size of volume
            type: int
        health_indications:
            description: If health-state is not ok, additional information
            type: list
        health_state:
            description: Health state of volume
            type: str
        name:
            description: Storage volume name
            type: str
        operational_status:
            description: The functional status
            type: str
        io_status:
            description: Resource is alive or not
            type: str
        itls:
            description: List of initiators
            type: list
        largest_free_chunk:
            description: Largest free chunk
            type: str
        provision_type:
            description: The provision type
            type: str
        storage_array_family:
            description: The storage array family name
            type: str
        storage_array_name:
            description: The storage array name
            type: str
        storage_volumetype:
            description: The storage volume type
            type: str
        system_id:
            description: Unique volume id
            type: str
        thin_capable:
            description: Thin provisioning support
            type: bool
        thin_rebuild:
            description: Thin rebuild
            type: bool
        use:
            description: Status of the volume
            type: str
        used_by:
            description: List of extents used by
            type: bool
        vendor_specific_name:
            description: Vendor specific name
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_storage_volume')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class StorageVolumeModule:
    """Class with Storage Volume operations"""

    def __init__(self):
        """Define all parameters required by the module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_user_parameters())
        mutually_exclusive = [
            ['storage_volume_name', 'storage_volume_id']
        ]
        required_one_of = [
            ['storage_volume_name', 'storage_volume_id']
        ]
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of,
            supports_check_mode=False)

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
        if not self.module.params['cluster_name']:
            msg = "Following is required: cluster_name"
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # Checking if the cluster is reachable
        if self.module.params['cluster_name']:
            cl_name = self.module.params['cluster_name']
            (err_code, msg) = utils.verify_cluster_name(self.client, cl_name)
            if err_code != 200:
                if "Resource not found" in msg:
                    msg = "Could not find resource {0}".format(cl_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
        self.strg_client = utils.StorageVolumeApi(api_client=self.client)
        self.cluster_name = self.module.params['cluster_name']
        self.all_vols = None

        LOG.info("Got VPLEX instance to access common lib methods "
                 "on VPLEX")

    def get_volume_by_id(self, vol_id):
        """Retrieve storage volume object by volume id"""
        LOG.info('Get volume by ID')
        err_msg = ("Could not get storage volume {0} from "
                   "{1}".format(vol_id, self.cluster_name))
        try:
            self.all_vols = self.strg_client.get_storage_volumes(
                cluster_name=self.cluster_name)
            LOG.debug("Obtained Volume details: %s", self.all_vols)
            data = [e for e in self.all_vols if e.system_id == vol_id]
            if len(data) > 0:
                LOG.info("Got storage volume details %s by volume ID from %s",
                         data[0].name, self.cluster_name)
                LOG.debug("Volume details: %s", data)
                return data[0], None
            return None, err_msg
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg += " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_volume_by_name(self, vol_name):
        """Retrieve storage volume object by volume name"""
        LOG.info('Get volume by name')
        try:
            res = self.strg_client.get_storage_volume(
                cluster_name=self.cluster_name,
                name=vol_name)
            LOG.info("Got storage volume details %s from %s", vol_name,
                     self.cluster_name)
            LOG.debug("Volume details: %s", res)
            return res, None
        except utils.ApiException as err:
            err_msg = ("Could not get storage volume {0} from {1} due to"
                       " error: {2}".format(vol_name, self.cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s", err_msg, err)
            # self.module.fail_json(msg=err_msg)
            return None, err_msg
        except (ValueError, TypeError) as err:
            err_msg = "Could not get storage volume {0} from {1} due to"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def claim_storage_volume(self, vol_name):
        """Claim storage volume"""
        try:
            res = self.strg_client.claim_storage_volume(
                cluster_name=self.cluster_name,
                name=vol_name, claim_payload={})
            LOG.info("Claimed storage volume %s of %s",
                     vol_name, self.cluster_name)
            LOG.debug("Claimed storage volume details: %s", res)
            return res, True
        except utils.ApiException as err:
            err_msg = ("Could not claim storage volume {0} from {1} due to"
                       " error: {2}".format(
                           vol_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s", err_msg, err)
            return err_msg, False
        except (ValueError, TypeError) as err:
            err_msg = "Could not claim storage volume {0} from {1} due to"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def unclaim_storage_volume(self, vol_name):
        """Unclaim storage volume"""
        try:
            res = self.strg_client.unclaim_storage_volume(
                cluster_name=self.cluster_name,
                name=vol_name, unclaim_payload={})
            LOG.info("Unclaimed storage volume %s of %s",
                     vol_name, self.cluster_name)
            LOG.debug("Unclaimed storage volume details: %s", res)
            return res, True
        except utils.ApiException as err:
            err_msg = ("Could not unclaim storage volume {0} from {1} due to"
                       " error: {2}".format(
                           vol_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s", err_msg, err)
            return err_msg, False
        except (ValueError, TypeError) as err:
            err_msg = "Could not unclaim storage volume {0} from {1} due to"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_storage_volume(self, vol_name, volume_payload):
        """Update storage volume"""
        LOG.debug("Update Details \n%s:\n\n%s", vol_name, volume_payload)
        try:
            res = self.strg_client.patch_storage_volume(
                cluster_name=self.cluster_name,
                name=vol_name,
                storage_volume_patch_payload=volume_payload)
            LOG.info("Updated storage volume %s of %s",
                     vol_name, self.cluster_name)
            LOG.debug("Updated storage volume details: %s", res)
            return res, True
        except utils.ApiException as err:
            err_msg = ("Could not update storage volume {0} in {1} due to"
                       " error: {2}".format(
                           vol_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s", err_msg, err)
            return err_msg, False
        except (ValueError, TypeError) as err:
            err_msg = "Could not update storage volume {0} in {1} due to"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def perform_module_operation(self):  # pylint: disable=R0912, R0914, R0915
        """perform module operations"""
        def filter_itls(volume):
            if get_itls is not None:
                if get_itls:
                    volume = volume['itls']
                else:
                    volume.pop('itls')
            return volume

        def exit_module(volume, change_flag):
            """module exit function"""
            volume = utils.serialize_content(volume)
            if 'itls' in volume:
                volume = filter_itls(volume)
            result = {
                "changed": change_flag,
                "storage_details": volume
            }
            LOG.debug("Result %s\n", result)
            self.module.exit_json(**result)

        def get_rename_payload(payload):
            if vol_obj.use == 'unclaimed':
                err_msg = 'Unclaimed Storage volume can not be renamed'
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if vol_obj.name != new_storage_vol_name:
                err_msg = ("Could not rename storage volume {0} in {1} as "
                           "name {2} is already in use".format(
                               vol_obj.name, self.cluster_name,
                               new_storage_vol_name))
                if self.all_vols:
                    for each in self.all_vols:
                        if each.name == new_storage_vol_name:
                            LOG.error("%s", err_msg)
                            self.module.fail_json(msg=err_msg)
                # Validate the new storage volume name
                status, msg = utils.validate_name(
                    new_storage_vol_name, 63, 'new_storage_volume_name')
                if not status:
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                else:
                    LOG.info(msg)
                payload.append(
                    {'op': 'replace', 'path': '/name',
                     'value': new_storage_vol_name}
                )
            else:
                msg = 'The new storage volume and the existing '\
                    'storage volume name are same.'
                LOG.info(msg)

            return payload

        state = self.module.params['state']
        vol_name = self.module.params['storage_volume_name']
        vol_id = self.module.params['storage_volume_id']
        new_storage_vol_name = self.module.params['new_storage_volume_name']
        get_itls = self.module.params['get_itls']
        thin_rebuild = self.module.params['thin_rebuild']
        claimed_state = self.module.params['claimed_state']

        vol_obj = None
        changed = False

        if vol_name:
            vol_obj, err_msg = self.get_volume_by_name(vol_name)
        if not vol_obj and vol_id:
            vol_obj, err_msg = self.get_volume_by_id(vol_id)
        if not any([vol_name, vol_id]):
            err_msg = "Both volume name and volume id can not be None"
        if err_msg:
            LOG.error(err_msg)

        if state == 'absent':
            if vol_obj:
                # storage volume can not be deleted
                exit_module(vol_obj, changed)
            else:
                exit_module({}, changed)
        # for next all operations we must need volume object
        # if its not available at this stage, we should exit
        if not vol_obj and err_msg:
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Unclaim volume
        if claimed_state == 'unclaimed':
            if vol_obj.use == 'claimed':
                vol_obj, changed = self.unclaim_storage_volume(vol_obj.name)
                # if unclaim fails, update user
                if not changed:
                    self.module.fail_json(msg=vol_obj)
                exit_module(vol_obj, changed)

            elif vol_obj.use != 'unclaimed':
                err_msg = ("Could not unclaim storage volume {0} from "
                           "{1} as it is not claimed.".format(
                               vol_obj.name, self.cluster_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

        # Claim volume
        elif claimed_state == 'claimed' and vol_obj.use == 'unclaimed':
            vol_obj, changed = self.claim_storage_volume(vol_obj.name)
            # if claim fails, update user
            if not changed:
                self.module.fail_json(msg=vol_obj)

        # Create update payload
        payload = []
        if new_storage_vol_name:
            payload = get_rename_payload(payload)
        if thin_rebuild is not None and thin_rebuild != vol_obj.thin_rebuild:
            # if user wants update thin_rebuild
            # and claimed_state is given as 'unclaimed'
            if vol_obj.use == 'unclaimed':
                msg = ("Could not update thin rebuild for {0} in"
                       " {1} as it is unclaimed".format(
                           vol_obj.name, self.cluster_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            payload.append(
                {'op': 'replace', 'path': '/thin_rebuild',
                 'value': thin_rebuild}
            )

        # Update storage volume
        if len(payload) > 0:
            vol_obj, changed = self.update_storage_volume(
                vol_obj.name, payload)
            if not changed:
                self.module.fail_json(msg=vol_obj)

        exit_module(vol_obj, changed)


def get_user_parameters():
    """This method provide the parameters required for the ansible
    storage volume module on VPLEX"""
    return dict(
        state=dict(type='str', required=True,
                   choices=['present', 'absent']),
        cluster_name=dict(type='str', required=True),
        storage_volume_name=dict(type='str', required=False),
        storage_volume_id=dict(type='str', required=False),
        claimed_state=dict(type='str', required=False,
                           choices=['claimed', 'unclaimed']),
        new_storage_volume_name=dict(type='str', required=False),
        thin_rebuild=dict(type='bool', required=False),
        get_itls=dict(type='bool', required=False))


def main():
    """Create VPLEX StorageVolumeModule object and perform action on it
        based on user input from playbook"""
    svm = StorageVolumeModule()
    svm.perform_module_operation()


if __name__ == '__main__':
    main()
