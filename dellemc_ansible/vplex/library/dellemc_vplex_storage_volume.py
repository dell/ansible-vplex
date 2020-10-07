""" Storage Volume module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
    dellemc_ansible_vplex_utils as utils
from vplexapi.api import StorageVolumeApi
from vplexapi.rest import ApiException
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type  # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_storage_volume
short_description: Manage VPLEX storage volume
description:
- Based on the user inputs performs claim, unclaim, update
  operations on storage volume
extends_documentation_fragment: dellemc_vplex.dellemc_vplex
author: Amit Uniyal (amit_u@dellteam.com) vplex.ansible@dell.com

options:
  cluster_name:
    description:
    - Name of the cluster
    required: True

  storage_volume_name:
    description:
    - Name of the storage volume
      storage_volume_id is mutually exclusive with storage_volume_name

  storage_volume_id:
    description:
    - ID of the storage volume or volume system_id

  new_storage_volume_name:
    description:
    - Defines to rename storage volume name

  thin_rebuild:
    description:
    - Defines to update thin_rebuild
    choices: [True, False]
    default: True

  get_itls:
    description:
    - Defines to retrieve itls list
    choices: [True, False]

  claimed_state:
    description:
    - Defines to claim unclaimed storage volume
    choices: ['claimed', 'unclaimed']

  state:
    description:
    - Defines whether the volume should exist or not.
    required: True
    choices: ['present', 'absent']
'''

EXAMPLES = r'''
- name: Claim Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    storage_volume_name: "{{ storage_volume_1 }}"
    claimed_state: "claimed"
    state: "present"

- name: Unclaim Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    storage_volume_name: "{{ storage_volume_1 }}"
    claimed_state: "unclaimed"
    state: "present"

- name: Get itls list of Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    storage_volume_name: "{{ storage_volume_1 }}"
    get_itls: true
    claimed_state: "claimed"
    state: "present"

- name: Update Storage Volume
  dellemc_vplex_storage_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    storage_volume_name: "{{ storage_volume_1 }}"
    new_storage_volume_name: "{{ storage_volume_2 }}"
    thin_rebuild: true
    claimed_state: "claimed"
    state: "present"

'''

RETURN = r'''
output:
   changed: state changed status
   volume_details: storage volume details

changed:
    description: Whether or not the storage volume has changed
    required: always
    type: bool

volume_details:
    description: Details of the storage volume
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

LOG = utils.get_logger('dellemc_vplex_storage_volume', log_devel=logging.INFO)
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
        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")
        self.cluster_name = self.module.params['cluster_name']
        self.vol_name = self.module.params['storage_volume_name']
        self.vol_id = self.module.params['storage_volume_id']
        # Create the configuration instance to communicate with
        # vplexapi
        self.client = utils.config_vplexapi(self.module.params)
        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # Checking if the cluster is reachable
        (err_code, msg) = utils.verify_cluster_name(
            self.client, self.cluster_name)
        if err_code != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource %s" % self.cluster_name
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        self.storage_client = StorageVolumeApi(api_client=self.client)

    def get_volume(self):
        """Retrieve storage volume object by volume name"""
        try:
            res = self.storage_client.get_storage_volume(
                cluster_name=self.cluster_name,
                name=self.vol_name)
            LOG.info("Got storage volume details %s from %s", self.vol_name,
                     self.cluster_name)
            LOG.debug("Volume details: %s", res)
            return res
        except ApiException as ex:
            err_msg = ("Could not get storage volume {0} from {1} due to"
                       " error: {2}".format(self.vol_name, self.cluster_name,
                                            utils.error_msg(ex)))
            LOG.error("%s\n%s", err_msg, ex)
            self.module.fail_json(msg=err_msg)

    def get_vol_by_id(self):
        """Retrieve storage volume object by volume id"""
        try:
            res = self.storage_client.get_storage_volumes(
                cluster_name=self.cluster_name)
            LOG.debug("Obtained Volume details: %s", res)
            data = [e for e in res if e.system_id == self.vol_id]
            if len(data) > 0:
                LOG.info("Got storage volume details %s by volume ID from %s",
                         data[0].name, self.cluster_name)
                LOG.debug("Volume details: %s", data)
                return data[0]
            return None
        except ApiException as ex:
            err_msg = ("Could not get storage volume {0} from {1} due to"
                       " error: {2}".format(
                           self.vol_name, self.cluster_name,
                           utils.error_msg(ex)))
            LOG.error("%s\n%s", err_msg, ex)
            self.module.fail_json(msg=err_msg)

    def claim_storage_volume(self):
        """Claim storage volume"""
        try:
            res = self.storage_client.claim_storage_volume(
                cluster_name=self.cluster_name,
                name=self.vol_name, claim_payload={})
            LOG.info("Claimed storage volume %s of %s",
                     self.vol_name, self.cluster_name)
            LOG.debug("Claimed storage volume details: %s", res)
            return res, True
        except ApiException as ex:
            err_msg = ("Could not claim storage volume {0} from {1} due to"
                       " error: {2}".format(
                           self.vol_name, self.cluster_name,
                           utils.error_msg(ex)))
            LOG.error("%s\n%s", err_msg, ex)
            return err_msg, False

    def unclaim_storage_volume(self):
        """Unclaim storage volume"""
        try:
            res = self.storage_client.unclaim_storage_volume(
                cluster_name=self.cluster_name,
                name=self.vol_name, unclaim_payload={})
            LOG.info("Unclaimed storage volume %s of %s",
                     self.vol_name, self.cluster_name)
            LOG.debug("Unclaimed storage volume details: %s", res)
            return res, True
        except ApiException as ex:
            err_msg = ("Could not unclaim storage volume {0} from {1} due to"
                       " error: {2}".format(
                           self.vol_name, self.cluster_name,
                           utils.error_msg(ex)))
            LOG.error("%s\n%s", err_msg, ex)
            return err_msg, False

    def update_storage_volume(self, volume_payload):
        """Update storage volume"""
        try:
            LOG.debug("Update Details \n%s:\n\n%s",
                      self.vol_name, volume_payload)
            res = self.storage_client.patch_storage_volume(
                cluster_name=self.cluster_name,
                name=self.vol_name,
                storage_volume_patch_payload=volume_payload)
            LOG.info("Updated storage volume %s of %s",
                     self.vol_name, self.cluster_name)
            LOG.debug("Updated storage volume details: %s", res)
            return res, True
        except ApiException as ex:
            err_msg = ("Could not update storage volume {0} in {1} due to"
                       " error: {2}".format(
                           self.vol_name, self.cluster_name,
                           utils.error_msg(ex)))
            LOG.error("%s\n%s", err_msg, ex)
            return err_msg, False

    def perform_module_operation(self):  # pylint: disable=R0912, R0915
        """perform module operations"""
        def exit_module(data, change_flag):
            """module exit function"""
            LOG.info("Exiting module")
            data = utils.serialize_content(data)
            if 'itls' in data and get_itls is False:
                data.pop('itls')
            result = {
                "changed": change_flag,
                "storage_details": data['itls'] if get_itls else data
            }
            LOG.debug("Module result %s\n", result)
            self.module.exit_json(**result)
        claimed_state = self.module.params['claimed_state']
        new_storage_volume_name = self.module.params['new_storage_volume_name']
        thin_rebuild = self.module.params['thin_rebuild']
        get_itls = self.module.params['get_itls']
        vol_obj = None
        # Validate the new storage volume name
        if new_storage_volume_name:
            char_len = '63'
            status, msg = utils.validate_name(new_storage_volume_name,
                                              char_len,
                                              'new_storage_volume_name')
            if not status:
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            else:
                LOG.info(msg)

        if self.vol_id:
            vol_obj = self.get_vol_by_id()
            if not vol_obj:
                err_msg = ("Could not get storage volume {0} from {1}."
                           " Requested volume id does not exists".format(
                               self.vol_id, self.cluster_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            self.vol_name = vol_obj.name
        else:
            vol_obj = self.get_volume()
            self.vol_name = vol_obj.name

        changed = False
        # verify if name is correct
        if self.vol_name == '' or self.vol_name is None:
            self.module.fail_json(msg="Storage volume name is not correct")

        # form update payload
        payload = []
        if new_storage_volume_name:
            payload.append(
                {'op': 'replace', 'path': '/name',
                 'value': new_storage_volume_name}
            )
        if thin_rebuild is not None:
            if thin_rebuild != vol_obj.thin_rebuild:
                payload.append(
                    {'op': 'replace', 'path': '/thin_rebuild',
                     'value': thin_rebuild}
                )
        # Update storage volume
        if len(payload) > 0:
            if claimed_state == 'claimed':
                # update storage volume field
                LOG.info("Verify if storage volume is claimed or not")
                if vol_obj.use != 'claimed':
                    # volume must be claimed to be update
                    self.claim_storage_volume()
                vol_obj, changed = self.update_storage_volume(payload)
                if not changed:
                    self.module.fail_json(msg=vol_obj)
            else:
                msg = ("Could not update storage volume. "
                       "It must be claimed volume, claimed_state: claimed")
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # claim storage volume
        if claimed_state == 'claimed':
            # if already claimed, return with changed=False
            if vol_obj.use == 'unclaimed':
                vol_obj, changed = self.claim_storage_volume()
                # if claim fails, update user
                if not changed:
                    self.module.fail_json(msg=vol_obj)

        # unclaim storage volume
        if claimed_state == 'unclaimed':
            if vol_obj.use != 'unclaimed':
                vol_obj, changed = self.unclaim_storage_volume()
                # if unclaim fails, update user
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
