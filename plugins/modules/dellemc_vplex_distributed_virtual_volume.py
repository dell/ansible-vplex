#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Distributed virtual volume module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_distributed_virtual_volume
version_added: '1.2.0'
short_description: Manage Distributed Virtual Volumes on VPLEX Storage Object
description:
- Provisioning the distributed virtual volume on VPLEX Storage System includes
  Create a distributed virtual volume,
  Get existing distributed virtual volume details,
  Rename an existing distributed virtual volume,
  Delete an existing distributed virtual volume,
  Expand a distributed virtual volume
extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex
author:
- Mohana Priya Sivalingam (@mohanapriya-dell) <vplex.ansible@dell.com>

options:
  distributed_virtual_volume_name:
    description:
    - Name of the distributed virtual volume
      Mutually exclusive with distributed_virtual_volume_id
    type: str

  distributed_device_name:
    description:
    - Name of the distributed device on top of which a distributed
      virtual volume should be created
    type: str

  distributed_virtual_volume_id:
    description:
    - Unique ID of the distributed virtual volume or it's system_id
      Mutually exclusive with distributed_virtual_volume_name
    type: str

  thin_enable:
    description:
    - Defines to have thin value
    default: true
    type: bool

  wait_for_rebuild:
    description:
    - Defines whether creation of distributed virtual volume can
      proceed on rebuilding device or not
    default: true
    type: bool

  new_distributed_virtual_volume_name:
    description:
    - New name of the distributed virtual volume to be renamed
    type: str

  expand:
    description:
    - Defines to perform expand operation for distributed virtual volume
    type: bool

  state:
    description:
    - Defines whether the distributed virtual volume should exist or not
    type: str
    required: True
    choices: ["present", "absent"]

notes:
- distributed_virtual_volume_name or distributed_virtual_volume_id is required
- distributed_virtual_volume_name and distributed_virtual_volume_id are
  mutually exclusive
'''

EXAMPLES = r'''
    - name: Create a distributed virtual volume
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd_dev"
        thin_enable: true
        distributed_virtual_volume_name: "ansible_test_vol"
        state: "present"

    - name: Create a distributed virtual volume with wait_for_rebuild=false
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd_dev"
        thin_enable: true
        distributed_virtual_volume_name: "ansible_test_vol"
        wait_for_rebuild: false
        state: "present"

    - name: Get details of distributed virtual volume using name
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_name: "ansible_test_vol"
        state: "present"

    - name: Get details of distributed virtual volume using virtual volume ID
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_id: "ansible_dist_dev_vol"
        state: "present"

    - name: Rename distributed virtual volume using virtual volume name
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_name: "ansible_test_vol"
        new_distributed_virtual_volume_name: "ansible_test_vol_new"
        state: "present"

    - name: Rename distributed virtual volume using virtual volume ID
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_id: "ansible_dist_dev_vol"
        new_distributed_virtual_volume_name: "ansible_dist_dev_vol_new"
        state: "present"

    - name: Expand distributed virtual volume using virtual volume name
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_name: "ansible_test_vol"
        expand: true
        state: "present"

    - name: Expand distributed virtual volume using virtual volume id
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_id: "ansible_dist_dev_vol"
        expand: true
        state: "present"

    - name: Delete distributed virtual volume using virtual volume name
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_name: "ansible_test_vol"
        state: "absent"

    - name: Delete distributed virtual volume using virtual volume id
      dellemc_vplex_distributed_virtual_volume:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_virtual_volume_id: "ansible_dist_dev_vol"
        state: "absent"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Distributed Virtual Volume Details:
    description: Details of the distributed virtual volume
    returned: When distributed virtual volume exists in VPLEX
    type: complex
    contains:
        block_count:
            description: Number of blocks
            type: int
        block_size:
            description: Block size
            type: int
        capacity:
            description: Size of volume
            type: int
        consistency_group:
            description: Identifies the VPLEX distributed consistency
                         group to which this distribute virtual volume belongs
            type: str
        expandable:
            description: Whether the virtual volume is expandable or not
            type: bool
        expandable_capacity:
            description: The amount of space that is available for volume
                         expansion.
            type: int
        expansion_method:
            description: The expansion method available for this volume
                -concatenation - The volume can be expanded using Concatenation
                    or RAID-C expansion.
                -storage-volume - The volume can be expanded to the Expandable
                    capacity using storage volume expansion.
                -not-supported - The volume does not support expansion.
                    This could be because the volume is being used in
                    RecoverPoint.
            type: str
        expansion_status:
            description: The expansion status of the volume.
                -dash - This volume can be expanded.
                -failed - The last volume expansion on this volume failed.
                -unknown - The volume expansion status is unknown.
                -in-progress - The volume cannot be expanded because it has a
                    volume expansion in progress.
            type: str
        health_indications:
            description: If health-state is not ok, additional information
            type: list
        health_state:
            description: Health state of volume
            type: str
        initialization_status:
            description: initialization_status
            type: str
        locality:
            description: Displays the virtual volume is distributed.
            type: str
        name:
            description: Distributed Virtual Volume name
            type: str
        operational_status:
            description: The functional status
            type: str
        recoverpoint_protection_at:
            description: Lists the VPLEX clusters at which the RecoverPoint
                         splitter is attached to the volume.
            type: list
        recoverpoint_usage:
            description: Values might be the following.
                -Local Replica - A copy created at the local site using
                    RecoverPoint CDP.
                -Remote Replica - The replica at the remote site that is
                    being replicated using CRR or CLR configurations.
                -Journal - A volume dedicated on the storage at each
                    copy in a RecoverPoint configuration. Journals are defined
                    per copy, and can consist of multiple journal volumes.
                -Repository - A special volume that must be dedicated on the
                    SAN-attached storage at each site,
                    for each RecoverPoint cluster. It stores configuration
                     information about the RecoverPoint appliances (RPAs) and
                -Production Source - This is the volume being replicated by
                    RecoverPoint.
            type: str
        service_status:
            description: whether service is running or not
            type: str
        storage_array_family:
            description: The storage array family name
            type: str
        supporting_device:
            description: The supporting distributed device on top of which the
                         corresponding distributed virtual volume is created
            type: str
        system_id:
            description: Unique volume id
            type: str
        thin_enabled:
            description: Thin provisioning support
            type: str
        visibility:
            description: To display the global access
            type: str
        vpd_id:
            description: vpd_id
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_distributed_virtual_volume')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexDistributedVirtualVolume():    # pylint:disable=R0902
    """Class with distributed virtual volume operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_distributed_virtual_volume_parameters())

        mutually_exclusive = [
            ['distributed_virtual_volume_name',
             'distributed_virtual_volume_id']
        ]

        required_one_of = [
            ['distributed_virtual_volume_name',
             'distributed_virtual_volume_id']
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
        # Create an instance to DistributedStorageApi to communicate with
        # vplexapi
        self.distvv = utils.DistributedStorageApi(api_client=self.client)
        self.cluster = utils.ClustersApi(api_client=self.client)
        self.vvol = utils.VirtualVolumeApi(api_client=self.client)

        # result is a dictionary that contains changed status and
        # distributed virtual volume details
        self.result = {"changed": False, "dist_vv_details": {}}

    def get_distributed_vv(self, dist_vv_name):
        """
        Get distributed virtual volume details
        """
        try:
            dist_vv_details = self.distvv.get_distributed_virtual_volume(
                dist_vv_name)
            LOG.info("Got distributed virtual volume details %s",
                     dist_vv_name)
            LOG.debug("Distributed Virtual Volume Details:\n%s",
                      dist_vv_details)
            return dist_vv_details
        except utils.ApiException as err:
            err_msg = ("Could not get distributed virtual volume {0} due to"
                       " error: {1}".format(dist_vv_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get distributed virtual volume {0} due to"
            err_msg = err_msg.format(dist_vv_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def rename_distributed_vv(self, dist_vv_name, new_dist_vv_name):
        """
        Rename the distributed virtual volume
        """
        try:
            dist_vv_patch_payload = [{'op': 'replace',
                                      'path': '/name',
                                      'value': new_dist_vv_name}]
            dist_vv_details = self.distvv.patch_distributed_virtual_volume(
                dist_vv_name, dist_vv_patch_payload)
            LOG.info("Renamed the distributed virtual volume %s to %s",
                     dist_vv_name, new_dist_vv_name)
            LOG.debug("Distributed Virtual Volume Details:\n%s",
                      dist_vv_details)
            return dist_vv_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not rename distributed virtual volume {0} to {1}"
            err_msg = err_msg.format(
                dist_vv_name, new_dist_vv_name) + " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def expand_distributed_vv(self, dist_vv_name, dist_vv_expand_payload):
        """
        Expand the distributed virtual volume
        """
        try:
            dist_vv_details = self.distvv.expand_distributed_virtual_volume(
                dist_vv_name, dist_vv_expand_payload)
            LOG.info("Expanded the distributed virtual volume %s",
                     dist_vv_name)
            LOG.debug("Distributed Virtual Volume Details:\n%s",
                      dist_vv_details)
            return dist_vv_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not expand distributed virtual volume {0} due"
            err_msg = err_msg.format(dist_vv_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def delete_distributed_vv(self, dist_vv_name):
        """
        Delete the distributed virtual volume
        """
        try:
            self.distvv.delete_distributed_virtual_volume(
                dist_vv_name)
            LOG.info("Deleted distributed virtual volume %s", dist_vv_name)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not delete distributed virtual volume {0} due"
            err_msg = err_msg.format(dist_vv_name) + " to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def create_distributed_vv(self, dist_vv_payload):
        """
        Create a distributed virtual volume
        """
        try:
            dist_vv_details = self.distvv.create_distributed_virtual_volume(
                dist_vv_payload)
            LOG.info("Created distributed virtual volume %s",
                     dist_vv_details.name)
            LOG.debug("Distributed Virtual Volume Details:\n%s",
                      dist_vv_details)
            return dist_vv_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not create distributed virtual volume due to"
            err_msg = err_msg + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_dist_vv_by_id(self, dist_vv_id):
        """
        Get distributed virtual volume details by using distributed virtual
        volume id
        """
        LOG.info("Trying to get distributed virtual volume by ID %s",
                 dist_vv_id)
        data = [vol for vol in self.get_distributed_virtual_volumes()
                if vol.system_id == dist_vv_id]
        if len(data) > 0:
            LOG.info("Found Distributed Virtual Volume details for %s from"
                     " ID %s", data[0].name, dist_vv_id)
            LOG.debug("Distributed Virtual Volume Details: %s", data)
            return data[0]
        return None

    def get_distributed_virtual_volumes(self):
        """
        Get all distributed virtual volumes
        """
        LOG.info("Get all distributed virtual volumes")
        try:
            res = self.distvv.get_distributed_virtual_volumes()
            LOG.debug("Distributed Virtual Volumes Details: %s", res)
            return res
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get the distributed virtual volumes due to"
            err_msg = err_msg + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_distributed_device(self, dev_name):
        """
        Get distributed device details
        """
        try:
            dev = self.distvv.get_distributed_device(dev_name)
            LOG.info("Got Distributed Device details %s", dev_name)
            LOG.debug("Distributed Device Details: %s", dev)
            return dev
        except utils.ApiException as err:
            err_msg = ("Could not get the distributed device {0} due to"
                       " error: {1}".format(dev_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get the distributed device {0} due to"
            err_msg = err_msg + " error: {1}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def check_name_existence(self, name):
        """
        Check for the existence of distributed virtual volume name across
        clusters in Vplex setup
        """
        LOG.info("Check for the distributed virtual volume name existence"
                 " across clusters")
        cluster_details = self.cluster.get_clusters()
        cl_name = [clus.name for clus in cluster_details
                   for vol in self.vvol.get_virtual_volumes(clus.name)
                   if vol.name == name]
        if len(cl_name) > 0:
            return cl_name[0]
        return None

    def validate_name(self, name, field):    # pylint: disable=R0201
        """This method validates the name length and non-presence of
        special characters"""
        char_len = '63'
        status, msg = utils.validate_name(name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def perform_module_operation(self):    # pylint: disable=R0912,R0914,R0915
        """
        Perform different actions on the distributed virtual volume  based on
        user parameters specified in the playbook
        """
        state = self.module.params['state']
        dist_vv_name = self.module.params['distributed_virtual_volume_name']
        thin_enable = self.module.params['thin_enable']
        wait_for_rebuild = self.module.params['wait_for_rebuild']
        dist_dev_name = self.module.params['distributed_device_name']
        dist_vv_id = self.module.params['distributed_virtual_volume_id']
        newvv_name = self.module.params['new_distributed_virtual_volume_name']
        expand = self.module.params['expand']
        dist_vv_details = None
        new_vv_details = None
        dev_details = None
        check_flag = False
        changed = False

        def exit_module(changed, dist_vv_details):
            self.result["changed"] = changed
            if dist_vv_details:
                dist_vv_details = utils.serialize_content(dist_vv_details)
            self.result["dist_vv_details"] = dist_vv_details
            self.module.exit_json(**self.result)

        # Check status of the cluster, whether cluster link is disabled
        degraded_cluster = utils.check_status_of_cluster(self.client)

        # Get distributed virtual volume details
        if dist_vv_id:
            dist_vv_details = self.get_dist_vv_by_id(dist_vv_id)
            if dist_vv_details is not None:
                dist_vv_name = dist_vv_details.name
        elif dist_vv_name:
            dist_vv_details = self.get_distributed_vv(dist_vv_name)

        # Common check for distributed virtual volume
        if state == "present" and not dist_dev_name and \
                dist_vv_details is None:
            if dist_vv_id:
                err_msg = ("Could not find distributed virtual volume with"
                           " distributed_virtual_volume_id {0}".format(
                               dist_vv_id))
            else:
                err_msg = ("Could not find distributed virtual volume"
                           " {0}".format(dist_vv_name))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Delete the distributed virtual volume
        if state == "absent":
            if dist_vv_details is None:
                if dist_vv_id:
                    LOG.info("Distributed virtual volume with distributed_"
                             "virtual_volume_id %s is not present to"
                             " delete", dist_vv_id)
                else:
                    LOG.info("Distributed virtual volume %s is not present"
                             " to delete", dist_vv_name)
                exit_module(changed, dist_vv_details)
            else:
                if degraded_cluster:
                    err_msg = ("Could not delete the distributed virtual"
                               " volume {0} since the cluster {1} is"
                               " degraded".format(
                                   dist_vv_name, degraded_cluster))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                elif dist_vv_details.service_status != 'unexported':
                    err_msg = ("Could not delete the distributed virtual"
                               " volume {0} since it is exported to storage"
                               " view".format(dist_vv_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                elif dist_vv_details.consistency_group is not None:
                    err_msg = ("Could not delete the distributed virtual"
                               " volume {0} since it is added to the"
                               " distributed consistency group {1}".format(
                                   dist_vv_name,
                                   dist_vv_details.consistency_group))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                # Perform delete operation
                changed = self.delete_distributed_vv(dist_vv_name)
                dist_vv_details = None

        # Create a distributed virtual volume
        if state == "present" and dist_dev_name:
            if newvv_name:
                err_msg = ("Could not perform create and rename in a single"
                           " task. Please specify each operation in"
                           " individual task")
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if dist_vv_id:
                err_msg = ("Could not perform create operation with"
                           " distributed_virtual_volume_id parameter. Instead"
                           ", please specify distributed_virtual_volume_name")
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            # Check for the existence of distributed virtual volume
            # name in other clusters
            cls_name = self.check_name_existence(dist_vv_name)
            if cls_name:
                err_msg = ("Could not create distributed virtual volume"
                           " with name {0} as it is already used in {1}."
                           " Please specify a different distributed"
                           " virtual volume name".format(
                               dist_vv_name, cls_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            dev_details = self.get_distributed_device(dist_dev_name)
            if dev_details is None:
                err_msg = ("Could not find the distributed device {0} to"
                           " create distributed virtual volume on top of it."
                           " Please provide valid distributed device"
                           " name".format(dist_dev_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            elif not dev_details.virtual_volume and dist_vv_details:
                err_msg = ("Could not create distributed virtual volume with"
                           " name {0} as it is already created on top of"
                           " another distributed device {1}. Please specify"
                           " a different distributed virtual volume"
                           " name".format(
                               dist_vv_name,
                               dist_vv_details.supporting_device))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if dev_details.virtual_volume is not None:
                vol_name = dev_details.virtual_volume.split('/')[-1]
                if vol_name == dist_vv_name:
                    dist_vv_details = self.get_distributed_vv(vol_name)
                    LOG.info("Distributed virtual volume %s is already"
                             " created on distributed device %s",
                             vol_name, dist_dev_name)
                    check_flag = True
                else:
                    err_msg = ("Could not create distributed virtual volume"
                               " with name {0} on top of distributed device"
                               " {1} as it already contains a distributed"
                               " virtual volume with name {2}".format(
                                   dist_vv_name,
                                   dev_details.name,
                                   vol_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            # Check for both create/rename should not happen during cluster
            # in degraded state
            if not check_flag and degraded_cluster:
                err_msg = ("Could not create the distributed virtual"
                           " volume since the cluster {0} is"
                           " degraded".format(degraded_cluster))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if dev_details.virtual_volume is None:
                if dev_details.rebuild_status in ['rebuilding', 'queued'] and \
                        wait_for_rebuild:
                    err_msg = ("Could not create the distributed virtual"
                               " volume as distributed device {0} is"
                               " rebuilding. Please try again later".format(
                                   dist_dev_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                # Check for the existence of volume in other clusters
                cls_name = self.check_name_existence(dist_dev_name + "_vol")
                if cls_name:
                    err_msg = ("Could not create distributed virtual volume"
                               " with name {0} as it is already used in {1}."
                               " Please rename the distributed device"
                               " {2}".format(
                                   dist_dev_name + "_vol", cls_name,
                                   dist_dev_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                # Validate the distributed virtual volume name
                self.validate_name(dist_vv_name,
                                   'distributed_virtual_volume_name')
                # Perform create operation
                uri = "/vplex/v2/distributed_storage/distributed_devices/"
                dist_vv_payload = {'device': uri + dist_dev_name,
                                   'thin': thin_enable}
                dist_vv_details = self.create_distributed_vv(dist_vv_payload)
                if dist_vv_details.name != dist_vv_name:
                    # Perform rename operation
                    dist_vv_details = self.rename_distributed_vv(
                        dist_vv_details.name, dist_vv_name)
                changed = True

        # Rename the distributed virtual volume
        if state == "present" and dist_vv_details and newvv_name:
            if newvv_name:
                if dist_vv_details.name == newvv_name:
                    LOG.info("Distributed virtual volume name and new"
                             " distributed virtual volume name are same")
                else:
                    # Check for the existence of new name in other
                    # clusters
                    cls_name = self.check_name_existence(newvv_name)
                    if cls_name:
                        err_msg = ("Could not rename distributed virtual"
                                   " volume {0} with name {1} as it is"
                                   " already used in {2}. Please"
                                   " specify a different name".format(
                                       dist_vv_details.name, newvv_name,
                                       cls_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
                    new_vv_details = self.get_distributed_vv(newvv_name)
                    if new_vv_details:
                        err_msg = ("Could not rename distributed virtual"
                                   " volume {0} with new_distributed_virtual"
                                   "_volume_name {1} as it is already"
                                   " present".format(dist_vv_details.name,
                                                     newvv_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
                    else:
                        if degraded_cluster:
                            err_msg = ("Could not rename the distributed"
                                       " virtual volume {0} since the cluster"
                                       " {1} is degraded".format(
                                           dist_vv_details.name,
                                           degraded_cluster))
                            LOG.error(err_msg)
                            self.module.fail_json(msg=err_msg)
                        # Validate the new distributed virtual volume name
                        temp = "new_distributed_virtual_volume_name"
                        self.validate_name(newvv_name, temp)
                        # Perform rename operation
                        dist_vv_details = self.rename_distributed_vv(
                            dist_vv_details.name, newvv_name)
                        changed = True

        # Expand the distributed virtual volume
        if state == "present" and dist_vv_details and expand:
            if dist_vv_details.expansion_method == "not-supported":
                err_msg = ("Could not expand the distributed virtual volume"
                           " {0} since expansion is not supported in this"
                           " volume".format(dist_vv_details.name))
            elif dist_vv_details.expandable_capacity == 0:
                LOG.info("Distributed virtual volume %s is already expanded"
                         " to its maximum size", dist_vv_details.name)
            else:
                if degraded_cluster:
                    err_msg = ("Could not expand the distributed"
                               " virtual volume {0} since the cluster"
                               " {1} is degraded".format(
                                   dist_vv_details.name, degraded_cluster))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                dist_vv_expand_payload = {'skip_init': expand}
                capacity = dist_vv_details.capacity
                LOG.info("Capacity before expansion: %s", capacity)
                dist_vv_details = self.expand_distributed_vv(
                    dist_vv_details.name, dist_vv_expand_payload)
                if capacity < dist_vv_details.capacity:
                    msg = "After expansion, "
                    msg = msg + "capacity increased from {0} to {1}.".format(
                        capacity, dist_vv_details.capacity)
                    LOG.info(msg)
                    changed = True

        # Finally call the exit module
        exit_module(changed, dist_vv_details)


def get_distributed_virtual_volume_parameters():
    """This method provide parameter required for the ansible distributed
    virtual volume module on VPLEX"""
    return dict(
        distributed_virtual_volume_name=dict(required=False, type='str'),
        distributed_device_name=dict(required=False, type='str'),
        thin_enable=dict(type='bool', required=False, default=True),
        wait_for_rebuild=dict(type='bool', required=False, default=True),
        distributed_virtual_volume_id=dict(required=False, type='str'),
        new_distributed_virtual_volume_name=dict(required=False, type='str'),
        expand=dict(required=False, type='bool'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """Create VplexDistributedVirtualVolume object and perform action on it
        based on user input from playbook"""
    obj = VplexDistributedVirtualVolume()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
