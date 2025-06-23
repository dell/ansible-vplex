#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Consistency Group module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_consistency_group
version_added: '1.2.0'
short_description:  Manage consistency group on VPLEX Storage System
description:
- Managing consistency group on VPLEX Storage System includes
  Create Consistency Group,
  Add virtual volumes to the Consistency Group,
  Remove virtual volumes from the Consistency Group,
  Rename Consistency Group,
  Delete Consistency Group,
  Get Consistency Group.

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

  cg_name:
    description:
    - Name of the consistency group
    required: true
    type: str

  virtual_volumes:
    description:
    - List of virtual volumes
    type: list
    elements: str

  virtual_volume_state:
    description:
    - describes the state of volumes inside consistency group
    choices: ['absent-in-cg', 'present-in-cg']
    type: str

  new_cg_name:
    description:
    - New name of the consistency group
    type: str

  state:
    description:
    - Define whether the consistency group should exist or not
    required: true
    choices: ['absent', 'present']
    type: str
'''

EXAMPLES = r'''
- name: Create consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  state: "present"

- name: Add virtual volumes to consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  virtual_volumes: ["ansible_vv_1", "ansible_vv_2"]
  virtual_volume_state: "present-in-cg"
  state: "present"

- name: Get consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  state: "present"

- name: Rename consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  new_cg_name: "ansible_new_cg"
  state: "present"

- name: Remove virtual volumes from consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  virtual_volumes: ["ansible_vv_1", "ansible_vv_2"]
  virtual_volume_state: "absent-in-cg"
  state: "present"

- name: Delete consistency group
  dellemc_vplex_consistency_group:
  vplexhost: "{{ vplexhost }}"
  vplexuser: "{{ vplexuser }}"
  vplexpassword: "{{ vplexpassword }}"
  verifycert: "{{ verifycert }}"
  cluster_name: "cluster-1"
  cg_name: "ansible_cg"
  state: "absent"
'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: End of all the operations
    type: bool

consistency_group_details:
    description: Properties of the consistency group
    returned: When local consistency group exists in VPLEX
    type: complex
    contains:
        active_clusters:
            description:
                - Active clusters of consistency group
            type: list
        auto_resume_at_loser:
            description:
                - Whether or not this consistency group supports auto_resume
            type: bool
        cache_mode:
            description:
                - Active cache mode of the consistency group
            type: str
        detach_rule:
            description:
                - Active detach rule of consistency group
            type: str
        name:
            description:
                - Name of the consistency group.
            type: str
        operational_status:
            description:
                - Operational status of the consistency group
            type: list
        passive_clusters:
            description:
                - Alternative cluster of the consistency group
            type: list
        read_only:
            description:
                - Whether or not this consistency group is read only
            type: bool
        recoverpoint:
            description:
                - Recovery point of the consistency group
            type: str
        recoverpoint_enabled:
            description:
                - Whether or not recoverpoint is enabled
            type: bool
        storage_at_clusters:
            description:
                - Consistency group storage clusters
            type: list
        virtual_volumes:
            description:
                - URI of virtual volumes belongs to consistency group
            type: list
        visibility:
            description:
                - Cluster visibility of consistency group
            type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils


LOG = utils.get_logger('dellemc_vplex_consistency_group')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class ConsistencyGroup():
    """Class with VPLEX Consistency group operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_cg_parameters())

        required_together = [['virtual_volumes', 'virtual_volume_state']]

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            required_together=required_together
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

        # Create an instance to ConsistencyGroupApi to communicate with
        # vplexapi
        self.cgrp = utils.ConsistencyGroupApi(api_client=self.client)
        self.vvol = utils.VirtualVolumeApi(api_client=self.client)
        self.dcgroup = utils.DistributedStorageApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_cgrp(self, cluster_name, cg_name):
        """
        Get the details of a consistency group.
        """
        try:
            all_cgrp = self.cgrp.get_consistency_groups(cluster_name)
            flag = False
            for cg in all_cgrp:
                if cg.name == cg_name:
                    flag = True
                    break
            if flag:
                obj_cgrp = self.cgrp.get_consistency_group(cluster_name, cg_name)
                LOG.info("Got consistency group details %s from %s", cg_name, cluster_name)
                LOG.debug("Consistency group Details:\n%s", obj_cgrp)
                cg_details = utils.serialize_content(obj_cgrp)
                return cg_details
            else:
                return None
        except utils.ApiException as err:
            err_msg = ("Could not get consistency group {0} of {1} due to"
                       " error: {2}".format(cg_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get consistency group {0} of {1} due to"
            err_msg = err_msg.format(cg_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def create_cgrp(self, cluster_name, cg_payload):
        """
        Create consistency group on VPLEX
        """
        try:
            obj_cgrp = self.cgrp.create_consistency_group(
                cluster_name, cg_payload)
            LOG.info("Created consistency group %s in %s", cg_payload['name'],
                     cluster_name)
            LOG.debug("Consistency group details:\n%s", obj_cgrp)
            cg_details = utils.serialize_content(obj_cgrp)
            return cg_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not create consistency group {0} in {1} due to"
            err_msg = err_msg.format(cg_payload['name'],
                                     cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def delete_cgrp(self, cluster_name, cg_name):
        """
        Delete consistency group on VPLEX
        """

        try:
            obj_cgrp = self.cgrp.delete_consistency_group(
                cluster_name, cg_name)
            LOG.info("Deleted the consistency group %s from %s", cg_name,
                     cluster_name)
            LOG.debug("Consistency group details:\n%s", obj_cgrp)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not delete consistency group {0} from {1} due"
            err_msg = err_msg.format(cg_name, cluster_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_cgrp(self, cluster_name, cg_name, cg_patch_payload):
        """
        Update consistency group attributes
        """

        try:
            obj_cgrp = self.cgrp.patch_consistency_group(
                cluster_name, cg_name, cg_patch_payload)
            LOG.info("Final payload: %s", cg_patch_payload)
            LOG.info("Updated consistency group %s in %s", cg_name,
                     cluster_name)
            LOG.debug("Consistency group details:\n%s", obj_cgrp)
            cg_details = utils.serialize_content(obj_cgrp)
            return cg_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not update the consistency group {0} in {1} due"
            err_msg = err_msg.format(cg_name, cluster_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def is_vir_vol_inuse(self, cluster_name, vir_vol_name):
        """
        Check if the virtual volume is used by any consistency group
        """
        try:
            vir_vol_details = None
            visibility = None
            used_cg_name = None
            vir_vol_details = self.vvol.get_virtual_volume(
                cluster_name, vir_vol_name)
            if vir_vol_details:
                LOG.debug("Virtual volume details:\n%s", str(vir_vol_details))
                if vir_vol_details.consistency_group is not None:
                    used_cg_name = \
                        vir_vol_details.consistency_group.split('/')[-1]
                visibility = vir_vol_details.visibility
            return (visibility, used_cg_name)

        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get virtual volume {0} in {1} due"
            err_msg = err_msg.format(vir_vol_name,
                                     cluster_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    @classmethod
    def get_v_vol_uri(cls, cluster_name, v_vol):
        """
        Prepare the proper virtual volume uri
        """
        v_vol_uri = "/vplex/v2/clusters/{0}/virtual_volumes/{1}".format(
            cluster_name, v_vol)
        return v_vol_uri

    @classmethod
    def get_cgrp_patch_payload(cls, operation, path, value):
        """
        Prepare consistency group patch payload
        """
        patch_payload = {
            'op': operation,
            'path': path,
            'value': value
        }
        return patch_payload

    def check_task_validity(self, name, field):
        """
        Check if the consistency group name is valid string
        """
        char_len = "63"
        status, msg = utils.validate_name(name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def check_name_in_distributed_cg(self, cg_name):
        """
        check whether same cg name is present in
        distributed storage consistency groups
        """

        distributed_details = self.dcgroup.get_distributed_consistency_groups()
        for distributed_storage in distributed_details:
            if distributed_storage.name == cg_name:
                return cg_name

        return None

    def perform_module_operation(self):  # pylint: disable=R0915,R0914,R0912
        """
        Perform different actions on Consistency group based on user
        parameters chosen in playbook
        """

        cluster_name = self.module.params['cluster_name']
        cg_name = self.module.params['cg_name']
        vir_vols = self.module.params['virtual_volumes']
        vir_vol_state = self.module.params['virtual_volume_state']
        new_cg_name = self.module.params['new_cg_name']
        state = self.module.params['state']

        changed = False
        result = dict(
            changed=False,
            cg_details=None
        )
        cg_details = None
        cg_patch_payload = []

        self.check_task_validity(cg_name, "cg_name")
        cg_details = self.get_cgrp(cluster_name, cg_name)

        if (state == 'absent' and cg_details):
            self.delete_cgrp(cluster_name, cg_name)
            cg_details = None
            changed = True

        if (state == 'present' and not cg_details):
            distributed_storage = self.check_name_in_distributed_cg(cg_name)
            if distributed_storage:
                msg = "Could not create consistency group {0} already " \
                      "exists with same name in distributed cg.".format(
                          cg_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if new_cg_name:
                msg = "Could not perform create and rename in a single " \
                      "task. Please specify each operation in single task."
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            cg_payload = {"name": cg_name}
            cg_details = self.create_cgrp(cluster_name, cg_payload)
            changed = True

        if (state == 'present' and vir_vols and vir_vol_state):
            for v_vol in vir_vols:
                (visibility, used_cg_name) = self.is_vir_vol_inuse(
                    cluster_name, v_vol)

                if used_cg_name not in (cg_name, None):
                    msg = ("Virtual volume '{0}' is used by another "
                           "Consistency group '{1}' in {2}"
                           .format(v_vol, used_cg_name, cluster_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if visibility != "local":
                    msg = "Virtual volume '{0}' visibility is '{1}'." \
                          "It should be local".format(v_vol, visibility)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if used_cg_name is None and vir_vol_state == 'present-in-cg':
                    operation = 'add'
                    path = '/virtual_volumes'
                    value = self.get_v_vol_uri(cluster_name, v_vol)
                    patch_payload = self.get_cgrp_patch_payload(
                        operation, path, value)
                    cg_patch_payload.append(patch_payload)

                if used_cg_name == cg_name and vir_vol_state == 'absent-in-cg':
                    operation = 'remove'
                    path = '/virtual_volumes'
                    value = self.get_v_vol_uri(cluster_name, v_vol)
                    patch_payload = self.get_cgrp_patch_payload(
                        operation, path, value)
                    cg_patch_payload.append(patch_payload)

        if (state == 'present' and new_cg_name and cg_details):
            self.check_task_validity(new_cg_name, 'new_cg_name')
            if new_cg_name == cg_details["name"]:
                msg = "The cg name and new cg" \
                      " are same"
                LOG.info(msg)

            else:
                get_new_cg = self.get_cgrp(cluster_name, new_cg_name)
                if get_new_cg:
                    msg = ("New Consistency group name {0} already exists"
                           " in {1}".format(new_cg_name, cluster_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                # check the new cg name is present in distributed storage
                distributed_storage = self.check_name_in_distributed_cg(
                    new_cg_name)
                if distributed_storage:
                    msg = "Could not rename consistency " \
                        "group {0}, already exists with " \
                        "same name in distributed_storage" \
                        "".format(new_cg_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                operation = 'replace'
                path = '/name'
                value = new_cg_name
                patch_payload = self.get_cgrp_patch_payload(
                    operation, path, value)
                cg_patch_payload.append(patch_payload)

        if len(cg_patch_payload) > 0:
            cg_details = self.update_cgrp(
                cluster_name, cg_name, cg_patch_payload)
            changed = True

        result['changed'] = changed
        result['cg_details'] = cg_details
        self.module.exit_json(**result)


def get_vplex_cg_parameters():
    """
    This method provide the parameters required for the ansible
    consistency group module on VPLEX
    """
    return dict(
        cluster_name=dict(type='str', required=True),
        cg_name=dict(type='str', required=True),
        virtual_volumes=dict(type='list', required=False, elements='str'),
        virtual_volume_state=dict(type='str', required=False, choices=[
            'present-in-cg', 'absent-in-cg']),
        new_cg_name=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )


def main():
    """
    Create ConsistenctGroup object and perform action on it
    based on user inputs from playbook
    """
    obj = ConsistencyGroup()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
