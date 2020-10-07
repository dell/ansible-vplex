""" Consistency Group module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
import urllib3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
         dellemc_ansible_vplex_utils as utils
from vplexapi.rest import ApiException
from vplexapi.api import ConsistencyGroupApi
from vplexapi.api import VirtualVolumeApi
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_consistency_group
version_added: '2.7'
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
  - dellemc_vplex.dellemc_vplex

author: Venkatesh Mariyappan (venkatesh_mariyappan@dellteam.com)
        vplex.ansible@dell.com

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
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        state: "present"

    - name: Add virtual volumes to consistency group
      dellemc_vplex_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        virtual_volumes: "{{ virtual_volumes }}"
        virtual_volume_state: "present-in-cg"
        state: "present"

    - name: Get consistency group
      dellemc_vplex_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        state: "present"

    - name: Rename consistency group
      dellemc_vplex_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        new_cg_name: "{{ new_cg_name }}"
        state: "present"

    - name: Remove virtual volumes from consistency group
      dellemc_vplex_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        virtual_volumes: "{{ virtual_volumes }}"
        virtual_volume_state: "absent-in-cg"
        state: "present"

    - name: Delete consistency group
      dellemc_vplex_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        cg_name: "{{ cg_name }}"
        state: "absent"

'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

consistency_group_details:
    description: Properties of the consistency group
    returned: When consistency group exist in VPLEX
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

LOG = utils.get_logger('dellemc_vplex_consistency_group',
                       log_devel=logging.INFO)

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
        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        self.cl_name = self.module.params['cluster_name']

        # Create the configuration instance to communicate
        # with vplexapi
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

        # Create an instance to ConsistencyGroupApi to communicate with
        # vplexapi

        self.cgrp = ConsistencyGroupApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_cgrp(self, cluster_name, cg_name):
        """
        Get the details of a consistency group.
        """
        try:
            obj_cgrp = self.cgrp.get_consistency_group(cluster_name, cg_name)
            LOG.info("Got consistency group details %s from %s", cg_name,
                     cluster_name)
            LOG.debug("Consistency group Details:\n%s", obj_cgrp)
            cg_details = utils.serialize_content(obj_cgrp)
            return cg_details
        except ApiException as err:
            err_msg = ("Could not get consistency group {0} of {1} due to"
                       " error: {2}".format(cg_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

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
        except ApiException as err:
            err_msg = ("Could not create consistency group {0} in {1} due to"
                       " error: {2}".format(cg_payload['name'],
                                            cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

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
        except ApiException as err:
            err_msg = ("Could not delete consistency group {0} from {1} due"
                       " to error: {2}".format(cg_name, cluster_name,
                                               utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

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
        except ApiException as err:
            err_msg = ("Could not update the consistency group {0} in {1} due"
                       " to error: {2}".format(cg_name, cluster_name,
                                               utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def is_vir_vol_inuse(self, cluster_name, vir_vol_name):
        """
        Check if the virtual volume is used by any consistency group
        """
        try:
            vir_vol_details = None
            visibility = None
            used_cg_name = None
            obj_vir_vol = VirtualVolumeApi(api_client=self.client)
            vir_vol_details = obj_vir_vol.get_virtual_volume(
                cluster_name, vir_vol_name)
            if vir_vol_details:
                LOG.debug("Virtual volume details:\n%s", str(vir_vol_details))
                if vir_vol_details.consistency_group is not None:
                    used_cg_name = \
                        vir_vol_details.consistency_group.split('/')[-1]
                visibility = vir_vol_details.visibility
            return (visibility, used_cg_name)

        except ApiException as err:
            err_msg = ("Could not get virtual volume {0} in {1} due"
                       " to error: {2}".format(vir_vol_name, cluster_name,
                                               utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    @classmethod
    def get_v_vol_uri(cls, cluster_name, v_vol):
        """
        Prepare the proper virtual volume uri
        """
        v_vol_uri = "/vplex/v2/clusters/{}/virtual_volumes/{}".format(
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

    def check_task_validity(self, cg_name):
        """
        Check if the consistency group name is valid string
        """
        char_len = "63"
        status, msg = utils.validate_name(cg_name, char_len, 'cg_name')
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def perform_module_operation(self):    # pylint: disable=R0915,R0914,R0912
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

        self.check_task_validity(cg_name)
        cg_details = self.get_cgrp(cluster_name, cg_name)

        if (state == 'absent' and cg_details):
            self.delete_cgrp(cluster_name, cg_name)
            cg_details = None
            changed = True

        if (state == 'present' and not cg_details):
            cg_payload = {"name": cg_name}
            cg_details = self.create_cgrp(cluster_name, cg_payload)
            changed = True

        if (state == 'present' and vir_vols and vir_vol_state):
            for v_vol in vir_vols:
                (visibility, used_cg_name) = self.is_vir_vol_inuse(
                    cluster_name, v_vol)

                if used_cg_name not in (cg_name, None):
                    msg = "Virtual volume '{0}' used by another Consistency "\
                        "group '{1}'".format(v_vol, used_cg_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if visibility != "local":
                    msg = "Virtual volume '{0}' visibility is '{1}'."\
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
            if len(cg_patch_payload) > 0:
                cg_details = self.update_cgrp(
                    cluster_name, cg_name, cg_patch_payload)
                changed = True

        if (state == 'present' and new_cg_name and cg_details):
            self.check_task_validity(new_cg_name)
            if new_cg_name != cg_details["name"]:
                get_new_cg = self.get_cgrp(cluster_name, new_cg_name)
                if get_new_cg:
                    err_msg = ("New Consistency group name {0} already exists"
                               " in {1}".format(new_cg_name, cluster_name))
                    self.module.fail_json(msg=err_msg)
                operation = 'replace'
                path = '/name'
                value = new_cg_name
                patch_payload = self.get_cgrp_patch_payload(
                    operation, path, value)
                cg_patch_payload.append(patch_payload)
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
        virtual_volumes=dict(type='list', required=False),
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
