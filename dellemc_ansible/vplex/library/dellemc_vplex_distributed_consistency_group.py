""" Distributed Consistency Group module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
    dellemc_ansible_vplex_utils as utils

__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_distributed_consistency_group
version_added: '2.7'
short_description: Manage VPLEX distributed consistency group
description:
- Managing distributed consistency group on VPLEX Storage System includes
  Create a distributed consistency group,
  Get a distributed consistency group,
  Add a distributed virtual volume to a distributed consistency group,
  Remove a distributed virtual volume from a distributed consistency group,
  Update the detach rule for a distributed consistency group,
  Enable/Disable the auto resume at loser of distributed consistency group,
  Resume distributed consistency group,
  Rename the distributed consistency group,
  Delete a distributed consistency group.

extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex

author:
- Chandra Prakash Boinapally (@chandra-dell) <vplex.ansible@dell.com>

options:
  distributed_cg_name:
    description:
    - The name of the distributed consistency group
    required: true
    type: str

  new_distributed_cg_name:
    description:
    - The new name of the distributed consistency group
    type: str

  distributed_virtual_volumes:
    description:
    - List of distributed virtual volumes
    type: list

  distributed_virtual_volume_state:
    description:
    - Describes the state of distributed virtual volumes
    choices: ['absent-in-cg', 'present-in-cg']
    type: str

  detach_rule:
    description:
    - Describes detach rule no_automatic_winner or winner for distributed cg
    choices: ['no_automatic_winner', 'cluster-1', 'cluster-2']
    type: str

  auto_resume_at_loser:
    description:
    - Enable/disable auto_resume_at_loser
    type: bool

  resume_at:
    description:
    - Describes which cluster to resume I/O, if cluster link is disabled
    type: str

  state:
    description:
    - Define whether the distributed consistency group should exist or not
    required: true
    choices: ['absent', 'present']
    type: str
'''

EXAMPLES = r'''
    - name: Create a distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        state: "present"

    - name: Get a distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        state: "present"

    - name: Rename a distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        new_distributed_cg_name: "ansible_dr_cg_name"
        state: "present"

    - name: Add distributed volumes to distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        distributed_virtual_volumes: ["ansible_dr_vv_1","ansible_dr_vv_2"]
        distributed_virtual_volume_state: "present-in-cg"
        state: "present"

    - name: Remove distributed volumes from distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        distributed_virtual_volumes: ["ansible_dr_vv_1","ansible_dr_vv_2"]
        distributed_virtual_volume_state: "absent-in-cg"
        state: "present"

    - name: Disable auto_resume_at_loser in distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        auto_resume_at_loser: false
        state: "present"

    - name: Enable auto_resume_at_loser in distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        auto_resume_at_loser: true
        state: "present"

    - name: Update the detach rule of distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        detach_rule: "cluster-1"
        state: "present"

    - name: Resume I/O on virtual volumes in distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_re_cg"
        resume_at: "cluster-1"
        state: "present"

    - name: Delete a distributed cg
      dellemc_vplex_distributed_consistency_group:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_cg_name: "ansible_dr_cg"
        state: "absent"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Distributed consistency group Details:
    description: Details of the distributed consistency group
    returned: For Create, Get, Delete and update operations
    type: complex
    contains:
        detach_rule:
             description: The detch_rule type of distributed consistency group
             typr: str
        operational status:
             description: The functional status clusters in distributed cg
             type: str
        read_only:
             description: Whether or not this distributed cg read only
             type: bool
        recoverypoint_enabled:
             description: Whether or not recoverpoint is enabled
             type: bool
        storage_at_clusters:
             description: Distributed cg use storage from both clusters
             type: List
        virtual_volumes:
             description: List of distributed virtual volumes
             type: list
        visibility:
             description: Lists the visibility distributed consistency group
             type: List
        auto_resume_at_loser:
             description: enable or disable auto_resume_at_loser
             type: bool
        recoverpoint:
             description: The recovery point of distributed consistency group
             type: str
        name:
             description: The name of the distributed consistency group
             type:  str
'''

LOG = utils.get_logger('dellemc_vplex_distributed_consistency_group')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class DistributedConsistencyGroup():
    """Class with VPLEX Distributed consistency group operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_dcg_parameters())

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

        # Create the configuration instance to communicate
        # with vplexapi
        self.client = utils.config_vplexapi(self.module.params)

        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client   # pylint: disable=W0612
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        # Create an instance to ConsistencyGroupApi to communicate with
        # vplexapi
        api_obj = utils.VplexapiModules()
        self.clus = api_obj.ClustersApi(api_client=self.client)
        self.cgrp = api_obj.ConsistencyGroupApi(api_client=self.client)
        self.dcgrp = api_obj.DistributedStorageApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_d_cgrp(self, dr_cg_name):
        """
        Get the details of a distributed consistency group.
        """
        try:
            obj_dcgrp = self.dcgrp.get_distributed_consistency_group(
                dr_cg_name)
            LOG.info("Got distributed consistency group details %s",
                     dr_cg_name)
            LOG.debug("Distributed consistency group Details:\n%s", obj_dcgrp)
            d_cg_details = utils.serialize_content(obj_dcgrp)
            return d_cg_details
        except utils.ApiException as err:
            err_msg = ("Could not get distributed consistency group {0} due to"
                       " error: {1}".format(dr_cg_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def create_d_cgrp(self, d_cg_payload):
        """
        Create Distributed consistency group on VPLEX
        """
        try:
            obj_d_cgrp = self.dcgrp.create_distributed_consistency_group(
                d_cg_payload)
            LOG.info("Created distributed consistency group %s",
                     d_cg_payload['name'])
            LOG.debug("Consistency group details:\n%s", obj_d_cgrp)
            d_cg_details = utils.serialize_content(obj_d_cgrp)
            return d_cg_details
        except utils.ApiException as err:
            err_msg = ("Could not create distributed consistency group {0}"
                       " due to error: {1}".format(
                           d_cg_payload['name'], utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def delete_d_cgrp(self, dr_cg_name):
        """
        Delete distributed consistency group on VPLEX
        """
        try:
            self.dcgrp.delete_distributed_consistency_group(dr_cg_name)
            LOG.info("Deleted the distributed consistency group %s",
                     dr_cg_name)
            return True
        except utils.ApiException as err:
            err_msg = ("Could not delete distributed consistency group {0} due"
                       " to error: {1}".format(
                           dr_cg_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def update_d_cgrp(self, dr_cg_name, d_cg_patch_payload):
        """
        Update distributed consistency group attributes
        """
        try:
            obj_dcgrp = self.dcgrp.patch_distributed_consistency_group(
                dr_cg_name, d_cg_patch_payload)
            LOG.info("Final payload: %s", d_cg_patch_payload)
            LOG.info("Updated distributed consistency group %s", dr_cg_name)
            LOG.debug("Distributed consistency group details:\n%s", obj_dcgrp)
            d_cg_details = utils.serialize_content(obj_dcgrp)
            return d_cg_details
        except utils.ApiException as err:
            err_msg = ("Could not update the consistency group {0} due"
                       " to error: {1}".format(
                           dr_cg_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def d_resume(self, dr_cg_name, d_cg_resume_payload):
        """
        resume Distributed consistency group
        """

        try:
            obj_dcgrp = self.dcgrp.resume(dr_cg_name, d_cg_resume_payload)
            LOG.info("Resume on the distributed consistency group %s",
                     dr_cg_name)
            LOG.debug("Distributed consistency group details:\n%s", obj_dcgrp)
            d_cg_details = utils.serialize_content(obj_dcgrp)
            return d_cg_details
        except utils.ApiException as err:
            err_msg = ("Could not resume distributed consistency group {0} due"
                       " to error: {1}".format(
                           dr_cg_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def is_distributed_volume_inuse(self, dr_vol_name):
        """
        Check if the distributed volume is used by any distributed cg
        """
        try:
            dr_vol_details = None
            used_dr_cg_name = None
            dr_vol_details = self.dcgrp.get_distributed_virtual_volume(
                dr_vol_name)
            if dr_vol_details:
                LOG.debug("Distributed virtual volume details:\n%s",
                          str(dr_vol_details))
                if dr_vol_details.consistency_group is not None:
                    used_dr_cg_name = \
                        dr_vol_details.consistency_group.split('/')[-1]
                locality = dr_vol_details.locality
            return (locality, used_dr_cg_name)

        except utils.ApiException as err:
            err_msg = ("Could not get distributed virtual volume {0} due"
                       " to error: {1}".format(
                           dr_vol_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def list_clusters(self):
        """
        return the list of clusters
        """
        cluster_list = []
        cluster_details = self.clus.get_clusters()
        for cluster in cluster_details:
            cluster_list.append(cluster.name)
        LOG.info("cluster details are %s", cluster_list)
        return cluster_list

    def check_name_in_clusters(self, dr_cg_name):
        """
        check whether same distributed cg name present in another cluster
        """
        cluster_details = self.clus.get_clusters()
        data = [clust.name for clust in cluster_details
                for cgrp in self.cgrp.get_consistency_groups(clust.name)
                if cgrp.name == dr_cg_name]
        if len(data) > 0:
            LOG.info("Consistency group with name %s is already"
                     " present in the cluster %s", dr_cg_name,
                     data[0])
            return data[0]
        return None

    def check_task_validity(self, name, field):
        """
        Check if the distributed consistency group name is valid string
        """
        char_len = "63"
        status, msg = utils.validate_name(name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def perform_module_operation(self):    # pylint: disable=R0915,R0914,R0912
        """
        Perform different actions on Distributed consistency group based on
        user parameters chosen in playbook
        """
        dr_cg_name = self.module.params['distributed_cg_name']
        new_dr_cg_name = self.module.params['new_distributed_cg_name']
        dr_vir_vol_state = self.module.params[
            'distributed_virtual_volume_state']
        dr_vir_vols = self.module.params['distributed_virtual_volumes']
        detach_rule = self.module.params['detach_rule']
        state = self.module.params['state']
        auto_resume_at_loser = self.module.params['auto_resume_at_loser']
        resume_at = self.module.params['resume_at']
        changed = False
        result = dict(
            changed=False,
            d_cg_details=None
        )

        d_cg_details = None
        d_cg_patch_payload = []

        self.check_task_validity(dr_cg_name, 'distributed_cg_name')
        d_cg_details = self.get_d_cgrp(dr_cg_name)

        # check status of the cluster, whether cluster link is disabled
        degraded_cluster = utils.check_status_of_cluster(self.client)
        if state == 'absent':
            if degraded_cluster and d_cg_details:
                msg = "Could not delete as {0} is degraded".format(
                    degraded_cluster)
                LOG.error(msg=msg)
                self.module.fail_json(msg=msg)

            if degraded_cluster or not d_cg_details:
                self.module.exit_json(**result)

            self.delete_d_cgrp(dr_cg_name)
            d_cg_details = None
            changed = True

        if (state == 'present' and degraded_cluster):
            if resume_at and not d_cg_details:
                msg = "Could not perform resume as consistency group {0}" \
                    " not found".format(dr_cg_name)
                LOG.error(msg=msg)
                self.module.fail_json(msg=msg)

            if not d_cg_details or new_dr_cg_name or detach_rule \
                    or dr_vir_vols or (auto_resume_at_loser is not None):
                msg = "Could not perform the operation as {0}" \
                    " is degraded".format(degraded_cluster)
                LOG.error(msg=msg)
                self.module.fail_json(msg=msg)

        if (state == 'present' and d_cg_details and resume_at):
            # get the list of clusters to resume I/O
            clusters = self.list_clusters()
            if resume_at not in clusters:
                msg = "Provided resume_at cluster '{0}' is invalid".format(
                    resume_at)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if len(d_cg_details['virtual_volumes']) == 0:
                msg = "Could not resume the distributed consistency {0}," \
                    " since no virtual volume is present".format(dr_cg_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if len(d_cg_details['virtual_volumes']) > 0:
                status_c1 = d_cg_details["operational_status"][0]["summary"]
                status_c2 = d_cg_details["operational_status"][1]["summary"]

                if (status_c1 == "suspended" and status_c2 == "suspended"):
                    resume_payload = {
                        "resume_at": "/vplex/v2/clusters/" + resume_at}
                    changed = True
                    d_cg_details = self.d_resume(dr_cg_name, resume_payload)

        if (state == 'present' and not d_cg_details):
            # check the name of distributed_cg is present in clusters
            cluster_name = self.check_name_in_clusters(dr_cg_name)

            if new_dr_cg_name:
                msg = "Could not perform create and rename in a single " \
                    "task. Please specify each operation in individual task."
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if resume_at:
                msg = "Could not resume distributed consistency group" \
                    " {0}, as it does not exists".format(dr_cg_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if cluster_name:
                msg = "Could not create the distributed consistency group" \
                    " {0}, already exists with same name in {1}".format(
                        dr_cg_name, cluster_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            d_cg_payload = {"name": dr_cg_name}
            d_cg_details = self.create_d_cgrp(d_cg_payload)
            changed = True

        if (state == 'present' and dr_vir_vols and dr_vir_vol_state):
            for dr_vols in dr_vir_vols:
                (locality, used_dr_cg_name) = \
                    self.is_distributed_volume_inuse(dr_vols)

                if locality != 'distributed':
                    msg = "Virtual volume '{0}' locality is '{1}'." \
                        "It should be distributed".format(dr_vols, locality)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if used_dr_cg_name not in (dr_cg_name, None):
                    msg = "Distributed virtual volume '{0}' used by another" \
                        " distributed consistency group {1}".format(
                            dr_vols, used_dr_cg_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if used_dr_cg_name is None and \
                        dr_vir_vol_state == 'present-in-cg':
                    uri = '/vplex/v2/distributed_storage/' + \
                        'distributed_virtual_volumes/' + dr_vols
                    d_cg_patch_payload.append(
                        {
                            'op': 'add',
                            'path': '/virtual_volumes',
                            'value': uri
                        }
                    )

                if used_dr_cg_name == dr_cg_name and \
                        dr_vir_vol_state == 'absent-in-cg':
                    uri = '/vplex/v2/distributed_storage/' + \
                        'distributed_virtual_volumes/' + dr_vols
                    d_cg_patch_payload.append(
                        {
                            'op': 'remove',
                            'path': '/virtual_volumes',
                            'value': uri
                        }
                    )

        if (state == 'present' and auto_resume_at_loser is not None):
            if auto_resume_at_loser == d_cg_details['auto_resume_at_loser']:
                LOG.info("Distributed consistency group has same auto resume"
                         " at loser as provided")

            else:
                d_cg_patch_payload.append(
                    {
                        'op': 'replace',
                        'path': '/auto_resume_at_loser',
                        'value': auto_resume_at_loser
                    }
                )

        if (state == 'present' and detach_rule):
            # get the list of clusters
            clusters = self.list_clusters()
            detach = ['no_automatic_winner']
            detach.extend(clusters)
            if detach_rule not in detach:
                msg = "Provided detach_rule is invalid '{0}'".format(
                    detach_rule)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            if detach_rule == d_cg_details['detach_rule']['type']:
                LOG.info("detach_rule and distributed consistency"
                         " detach rule are same")

            else:
                detach = {}
                if detach_rule == 'no_automatic_winner':
                    detach['type'] = detach_rule
                    d_cg_patch_payload.append(
                        {
                            'op': 'replace',
                            'path': '/detach_rule',
                            'value': detach
                        }
                    )

                elif d_cg_details['detach_rule']['type'] == 'winner' and \
                        detach_rule == \
                        d_cg_details['detach_rule']['cluster'].split('/')[-1]:
                    LOG.info("detach_rule and distributed consistency"
                             " detach rule are same")

                else:
                    detach['type'] = 'winner'
                    detach['cluster'] = '/vplex/v2/clusters/' + detach_rule
                    detach['delay'] = 5
                    d_cg_patch_payload.append(
                        {
                            'op': 'replace',
                            'path': '/detach_rule',
                            'value': detach
                        }
                    )

        if (state == 'present' and new_dr_cg_name and d_cg_details):
            self.check_task_validity(new_dr_cg_name, 'new_distributed_cg_name')
            if new_dr_cg_name == d_cg_details["name"]:
                msg = "The distributed cg name and new distributed cg" \
                    " are same"
                LOG.info(msg)

            else:
                get_new_d_cg = self.get_d_cgrp(new_dr_cg_name)
                if get_new_d_cg:
                    err_msg = "New distributed consistency group name {0}," \
                        " already exists".format(new_dr_cg_name)
                    self.module.fail_json(msg=err_msg)

                # check the new distributed cg name is present in clusters
                cluster_name = self.check_name_in_clusters(new_dr_cg_name)
                if cluster_name:
                    msg = "Could not rename distributed consistency" \
                        " group {0}, already exists with same name in" \
                        " {1}".format(new_dr_cg_name, cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                d_cg_patch_payload.append(
                    {
                        'op': 'replace',
                        'path': '/name',
                        'value': new_dr_cg_name
                    }
                )
        if len(d_cg_patch_payload) > 0:
            d_cg_details = self.update_d_cgrp(dr_cg_name, d_cg_patch_payload)
            changed = True

        result['changed'] = changed
        result['d_cg_details'] = d_cg_details
        self.module.exit_json(**result)


def get_vplex_dcg_parameters():
    """
    This method provide the parameters required for the ansible
    distributed consistency group module on VPLEX
    """
    return dict(
        distributed_cg_name=dict(type='str', required=True),
        distributed_virtual_volumes=dict(type='list', required=False),
        distributed_virtual_volume_state=dict(type='str',
                                              required=False,
                                              choices=['present-in-cg',
                                                       'absent-in-cg']),
        new_distributed_cg_name=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        detach_rule=dict(type='str', required=False),
        auto_resume_at_loser=dict(type='bool', required=False),
        resume_at=dict(type='str', required=False)
    )


def main():
    """
    Create DistributedconsistenctGroup object and perform action on it
    based on user inputs from playbook
    """
    obj = DistributedConsistencyGroup()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
