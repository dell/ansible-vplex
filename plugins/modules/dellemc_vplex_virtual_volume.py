#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Virtual Volume module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_virtual_volume
version_added: '1.2.0'
short_description: Manage VPLEX virtual volume
description:
- Managing virtual volume on VPLEX System includes
  Get Virtual Volume,
  Create Virtual Volume,
  Update Virtual Volume,
  Delete Virtual Volume,
  Enable/Disable remote access,
  Expand Virtual Volume,
  Cache invalidate

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

  virtual_volume_name:
    description:
    - Unique name of the virtual volume
      virtual_volume_id is mutually exclusive with virtual_volume_name
    type: str

  virtual_volume_id:
    description:
    - Unique ID of the virtual volume or volume system_id
      virtual_volume_name is mutually exclusive with virtual_volume_id
    type: str

  supporting_device_name:
    description:
    - Unique name of the supporting device.
      Over which Virtual volume should be created
    type: str

  new_virtual_volume_name:
    description:
    - Defines to rename virtual volume name
    type: str

  thin_enable:
    description:
    - Defines to have thin value
    default: true
    type: bool
    choices: ['True','False']

  wait_for_rebuild:
    description:
    - Defines whether creation of virtual volume can
      proceed on rebuilding device or not
    default: true
    type: bool

  expand:
    description:
    - Defines to perform expand operation for virtual volume
    type: bool

  additional_devices:
    description:
    - Defines to add/remove virtual volume to expand
    type: list
    elements: str

  remote_access:
    description:
    - Defines remote access to virtual volume
    type: str
    choices: ['enable', 'disable']

  state:
    description:
    - Defines whether the volume should exist or not
    type: str
    required: True
    choices: ['absent', 'present']

  cache_invalidate:
    description:
    - To perform cache invalidate on the virtual volume
    type: bool
    default: false
    choices: ['True','False']
'''

EXAMPLES = r'''
- name: Get virtual Volume by volume id
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_id: "ansible_dev_vol"
    state: "present"

- name: Get virtual Volume by volume name
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    state: "present"

- name: Create Virtual volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    supporting_device_name: "ansible_dev"
    thin_enable: true
    state: "present"

- name: Create Virtual volume with wait_for_rebuild set to 'false'
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    supporting_device_name: "ansible_dev"
    thin_enable: true
    wait_for_rebuild: false
    state: "present"

- name: Rename Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_id: "ansible_dev_vol"
    new_virtual_volume_name: "ansible_dev_vol_new_name"
    state: "present"

- name: Delete Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    state: "absent"

- name: Enable remote access of Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    remote_access: "enable"
    state: "present"

- name: Disable Remote Access of Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    remote_access: "disable"
    state: "present"

- name: Expand virtual volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    expand: true
    state: "present"

- name: Expand virtual volume with 'additional_devices'
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    expand: true
    additional_devices: ["ansible_dev_1"]
    state: "present"

- name: Perform Cache Invalidate
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    virtual_volume_name: "ansible_dev_vol"
    cache_invalidate: true
    state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the virtual volume has changed
    returned: End of all the operations
    type: bool

volume_details:
    description: Details of the virtual volume
    returned: When local virtual volume exist in VPLEX
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
            description: Identifies the VPLEX consistency group to which this
                         virtual volume belogs
            type: int
        expandable:
            description: Whether the virtual volume is expandable or not
            type: bool
        expandable_capacity:
            description: The amount of space that is available for volume
                         expansion.
            type: int
        expansion_method:
            description: The expansion method available for this volume
                concatenation - The volume can be expanded using Concatenation
                    or RAID-C expansion.
                storage-volume - The volume can be expanded to the Expandable
                    capacity using storage volume expansion.
                not-supported - The volume does not support expansion.
                    This could be because the volume is being used in
                    RecoverPoint.
            type: str
        expansion_status:
            description: The expansion status of the volume.
                - (dash) - This volume can be expanded.
                failed - The last volume expansion on this volume failed
                unknown - The volume expansion status is unknown.
                in-progress - The volume cannot be expanded because it has a
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
            description: Designates where the virtual volume is located.
                Values can be cluster 1, cluster 2 or distributed
            type: str
        name:
            description: Virtual volume name
            type: str
        operational_status:
            description: The functional status
            type: str
        recoverpoint_protection_at:
            description: Lists the VPLEX clusters at which the RecoverPoint
                splitter is attached to the volume.
            type: list
        recoverpoint_usage:
            description:
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
            description: The supporting device of virtual volume
            type: str
        system_id:
            description: Unique volume id
            type: str
        thin_enabled:
            description: Thin provisioning support
            type: bool
        visibility:
            description: To enable remote access global or local
            type: str
        vpd_id:
            description: vpd_id
            type: str
        additional_devs:
            description: added device list to expand virtual volume
            type: list
        mirrors:
            description: added device list for mirroring
            type: list
'''

from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils
from ansible.module_utils.basic import AnsibleModule
from datetime import datetime, timedelta
from collections import OrderedDict


LOG = utils.get_logger('dellemc_vplex_virtual_volume')

HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VirtualVolumeModule:  # pylint: disable=R0902
    """Class with virtual Volume operations"""

    def __init__(self):
        """Define all parameters required by the module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_user_parameters())
        mutually_exclusive = [
            ['virtual_volume_name', 'virtual_volume_id']
        ]
        required_one_of = [
            ['virtual_volume_name', 'virtual_volume_id']
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

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        # Create an instance to communicate with storageview VPLEX api
        self.virt_cl = utils.VirtualVolumeApi(api_client=self.client)
        self.dev_cl = utils.DevicesApi(api_client=self.client)
        self.maps_cl = utils.MapsApi(api_client=self.client)
        self.dist_virt_cl = utils.DistributedStorageApi(
            api_client=self.client)
        self.cluster_cl = utils.ClustersApi(api_client=self.client)
        self.dir_cl = utils.DirectorApi(api_client=self.client)
        self.cluster_name = self.module.params['cluster_name']
        self.vol_obj = None
        LOG.info("Got VPLEX instance to access common lib methods "
                 "on VPLEX")

    def get_all_volumes(self, cluster_name):
        """Get all virtual volume from VPLEX"""
        LOG.info('Get all virtual volumes from %s', cluster_name)
        try:
            all_vols = self.virt_cl.get_virtual_volumes(
                cluster_name=cluster_name)
            LOG.debug("Obtained Volume details: %s", all_vols)
            return all_vols
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get all virtual volumes from {0}"
            err_msg = err_msg.format(cluster_name) + " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_volume_by_id(self, vol_id):
        """Get virtual volume object by volume id"""
        LOG.info('Get virtual volume by ID')
        all_vols = self.get_all_volumes(self.cluster_name)
        data = [e for e in all_vols if e.system_id == vol_id]
        if len(data) > 0:
            LOG.info("Got virtual volume details %s by volume ID "
                     "from %s", data[0].name, self.cluster_name)
            LOG.debug("Volume details: %s", data)
            if data[0].locality == "local":
                return data[0], None
        err_msg = ("Could not get virtual volume {0} from "
                   "{1}".format(vol_id, self.cluster_name))
        return None, err_msg

    def get_volume_by_name(self, vol_name):
        """Get virtual volume object by volume name"""
        LOG.info('Get virtual volume by name')
        err_msg = ("Could not get virtual volume {0} from {1} due to"
                   " error: ".format(vol_name, self.cluster_name))
        try:
            res = self.virt_cl.get_virtual_volume(
                cluster_name=self.cluster_name,
                name=vol_name)
            LOG.info("Got virtual volume details %s from %s", vol_name,
                     self.cluster_name)
            LOG.debug("Volume details: %s", res)
            if res.locality == "local":
                return res, None
            err_msg += "{0} is not a local virtual volume".format(vol_name)
            LOG.error("%s\n", err_msg)
        except utils.ApiException as err:
            err_msg += "{0}".format(utils.error_msg(err))
            LOG.error("%s\n%s", err_msg, err)
        except (ValueError, TypeError) as err:
            err_msg += "{0}"
            err_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)
        return None, err_msg

    def create_volume(self, payload):
        """Create virtual volume"""
        LOG.info('Creating virtual volume')
        LOG.debug('Details \n%s:\n\n', payload)
        try:
            res = self.virt_cl.create_virtual_volume(
                cluster_name=self.cluster_name,
                virtual_volume_payload=payload)
            LOG.info('Created volume %s', res.name)
            LOG.debug('New virtual volume details: %s', res)
            return res
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not create virtual volume in {0} due to"
            err_msg = err_msg.format(self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_volume(self, volume_payload):
        """Update virtual volume"""
        LOG.info('Updating virtual volume %s', self.vol_obj.name)
        LOG.debug('Details \n%s:\n\n%s', self.vol_obj.name, volume_payload)
        try:
            res = self.virt_cl.patch_virtual_volume(
                cluster_name=self.cluster_name,
                name=self.vol_obj.name,
                virtual_volume_patch_payload=volume_payload)
            LOG.info('Updated %s', self.vol_obj.name)
            LOG.debug('Updated virtual volume details: %s', res)
            return res
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not update virtual volume {0} in {1} due to"
            err_msg = err_msg.format(self.vol_obj.name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def expand_volume(self, payload):
        """Expand virtual volume"""
        LOG.info('Expanding virtual volume %s', self.vol_obj.name)
        LOG.debug('Details: \n%s', payload)
        try:
            res = self.virt_cl.expand_virtual_volume(
                cluster_name=self.cluster_name,
                name=self.vol_obj.name,
                virtual_volume_expand_payload=payload)
            LOG.info('Expanded %s', self.vol_obj.name)
            LOG.debug('Expanded virtual volume details: %s', res)
            return res
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not expand virtual volume {0} in {1} due to"
            err_msg = err_msg.format(self.vol_obj.name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def delete_volume(self, vol_name=None):
        """Delete virtual volume"""
        LOG.info('Deleting virtual volume')
        if not vol_name:
            vol_name = self.vol_obj.name
        try:
            self.virt_cl.delete_virtual_volume(
                cluster_name=self.cluster_name,
                name=vol_name)
            msg = 'Deleted volume ' + vol_name
            LOG.info(msg)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not delete virtual volume {0} in {1} due to"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_all_devices(self, cluster_name):
        """Get all devices from VPLEX"""
        LOG.info('Get all devices from %s', cluster_name)
        try:
            all_devs = self.dev_cl.get_devices(
                cluster_name=cluster_name)
            LOG.debug("Obtained devices details: %s", all_devs)
            return all_devs
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get all devices from {0} due to "
            err_msg = err_msg.format(cluster_name) + "error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_device(self, dev_name):
        """Get device object by volume name"""
        LOG.info('Get device %s from VPLEX', dev_name)
        try:
            res = self.dev_cl.get_device(
                cluster_name=self.cluster_name,
                name=dev_name)
            LOG.info('Found %s', res.name)
            LOG.debug('Device details: %s', res)
            return res
        except utils.ApiException as err:
            err_msg = ("Could not get device {0} in {1} due to"
                       " error: {2}".format(
                           dev_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)
        except (ValueError, TypeError) as err:
            err_msg = "Could not get device {0} in {1} due to"
            err_msg = err_msg.format(dev_name,
                                     self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_device(self, dev_name, payload):
        """Updating local device"""
        LOG.info('Trying to update device %s', dev_name)
        LOG.debug('Payload details \n\n%s\n', payload)
        try:
            res = self.dev_cl.patch_local_device(
                cluster_name=self.cluster_name,
                name=dev_name,
                local_device_patch_payload=payload)
            LOG.info('Updated device %s', dev_name)
            LOG.debug("Device details\n%s", res)
            return res, True
        except utils.ApiException as err:
            err_msg = ("Could not update device {0} in virtual volume {1}"
                       " in {2} due to error: {3}".format(
                           dev_name, self.vol_obj.name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg), False
        except (ValueError, TypeError) as err:
            msg = "Could not update device {0} in virtual volume {1} in {2}"
            err_msg = msg.format(dev_name, self.vol_obj.name,
                                 self.cluster_name) + " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_map(self, uri):
        """Get map object from VPLEX"""
        obj = uri.split('/')[-1]
        LOG.info('Get map for %s', obj)
        try:
            res = self.maps_cl.get_map(uri)
            LOG.info('Map Found')
            LOG.debug('Map details: %s', res)
            return res
        except utils.ApiException as err:
            err_msg = ("Could not get map for {0} in {1} due to"
                       " error: {2}".format(
                           obj, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)
        except (ValueError, TypeError) as err:
            err_msg = "Could not get map for {0} in {1} due to"
            err_msg = err_msg.format(obj, self.cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_distributed_virtual_volume(self, vol_name):
        """Get distributed virtual volume object by volume name"""
        LOG.info('Get distributed virtual volume by name')
        try:
            res = self.dist_virt_cl.get_distributed_virtual_volume(vol_name)
            LOG.info("Got distributed virtual volume details %s", vol_name)
            LOG.debug("Volume details: %s", res)
            return res, None
        except utils.ApiException as err:
            err_msg = ("Could not get distributed virtual volume {0} from"
                       " {1} due to error: {2}".format(
                           vol_name, self.cluster_name, utils.error_msg(err)))
            LOG.error("%s\n%s", err_msg, err)
            return None, err_msg
        except (ValueError, TypeError) as err:
            err_msg = "Could not get distributed virtual volume {0} from {1}"
            err_msg = err_msg.format(vol_name,
                                     self.cluster_name) + " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_clusters(self):
        """Get all clusters object from VPLEX"""
        LOG.info('Get all clusters')
        try:
            res = self.cluster_cl.get_clusters()
            LOG.debug('Clusters details: %s', res)
            return [each.name for each in res]
        except utils.ApiException as err:
            err_msg = ("Could not get all clusters due to "
                       "error: {0}".format(utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)
        except (ValueError, TypeError) as err:
            err_msg = "Could not get all clusters due to "
            err_msg = err_msg + "error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def volume_exists_in_other_clusters(self, vol_name):
        """Verify if same volume name exists in other clusters"""
        clusters = self.get_clusters()
        clusters = list(set(clusters).difference([self.cluster_name]))
        for cluster in clusters:
            all_vols = self.get_all_volumes(cluster)
            for vol in all_vols:
                if vol_name == vol.name:
                    return True
        return False

    def device_exists_in_other_clusters(self, dev_name):
        """Verify if same volume name exists in other clusters"""
        clusters = self.get_clusters()
        clusters = list(set(clusters).difference([self.cluster_name]))
        LOG.info(dev_name)
        for cluster in clusters:
            all_devs = self.get_all_devices(cluster)
            for dev in all_devs:
                if dev_name in dev.name:
                    return True
        return False

    def director_status(self):
        """ check the director status """
        dir_details = self.dir_cl.get_directors()
        for dir_det in dir_details:
            dir_info = self.dir_cl.get_director(dir_det.name)
            if dir_info.communication_status != "ok":
                return dir_det.name
        return None

    def cache_invalidate(self, vol_name):
        """ Perform cache invalidate on the virtual volume """
        msg = ("Performing cache invalidate on {0} in {1}".
               format(self.vol_obj.name, self.cluster_name))
        LOG.info(msg)
        try:
            res = self.virt_cl.virtual_volume_cache_invalidate(
                cluster_name=self.cluster_name,
                name=vol_name)
            LOG.info("Performed cache invalidate on virtual volume %s in %s",
                     vol_name, self.cluster_name)
            LOG.debug("Volume details: %s", res)
            return res, None
        except (utils.ApiException, ValueError, TypeError) as err:
            msg = "Could not perform cache invalidate on virtual volume"
            msg = msg + " {0} in {1} due to error: ".format(vol_name,
                                                            self.cluster_name)
            err_msg = msg + "{0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def perform_module_operation(self):  # pylint: disable=R0912, R0914, R0915
        """perform module operations"""
        def exit_module(volume, change_flag):
            """module exit function"""
            volume = utils.serialize_content(volume)
            if vol_type:
                if vol_type == 'mirrored':
                    volume['mirrors'] = list(children.values())
                    volume['additional_devs'] = []
                elif vol_type == 'expanded':
                    volume['mirrors'] = []
                    volume['additional_devs'] = list(children.values())
            elif volume != {}:
                volume['mirrors'] = []
                volume['additional_devs'] = []
            result = {
                "changed": change_flag,
                "storage_details": volume
            }
            LOG.debug("Result %s\n", result)
            self.module.exit_json(**result)

        def is_device_rebuilding(dev):
            """Verify if device is in rebuilding state"""
            LOG.info('Verify if device is rebuilding for %s', dev.name)
            LOG.info('Device current rebuilding status is %s',
                     dev.rebuild_status)
            if dev.rebuild_status in ['rebuilding', 'queued']:
                msg = 'Device {0} rebuilding is in progress in '\
                    '{1}, Please try again later.'.format(
                        dev.name, self.cluster_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        def dev_checks(device_name, chk_vol=None, chk_top_level=None,
                       chk_rebuild=None):
            """Validate device for different tasks"""
            dev = self.get_device(device_name)
            if isinstance(dev, str):
                self.module.fail_json(msg=dev)
            if chk_vol and dev.virtual_volume is not None:
                msg = 'Device {0} is already used in {1} virtual '\
                    'volume in {2}'.format(
                        device_name, dev.virtual_volume, self.cluster_name)
                LOG.info(msg)
                self.module.fail_json(msg=msg)
            if chk_top_level and not dev.top_level:
                msg = 'Device {0} is already in use in {1}'.format(
                    device_name, self.cluster_name)
                LOG.info(msg)
                self.module.fail_json(msg=msg)
            if chk_rebuild:
                is_device_rebuilding(dev)
            return dev

        def verify_new_volume_name(name, field='new_virtual_volume_name'):
            def exit_fail(msg):
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            # if name is valid
            LOG.info('Valdating %s', field)
            status, msg = utils.validate_name(
                name, 63, field)
            if not status:
                exit_fail(msg)

            msg = "Virtual volume {0} with same name already exists" \
                " in ".format(name)
            # if name is already assigned to dist virtual volume
            vol, dummy = self.get_distributed_virtual_volume(name)
            if vol and vol.locality == 'distributed':
                msg += 'distributed virtual volume'
                exit_fail(msg)
            # if name is already assigned to virtual volume in same cluster
            vol, dummy = self.get_volume_by_name(name)
            if vol:
                msg += self.cluster_name
                exit_fail(msg)

        def get_volume_type(children):
            """Get volume type, if its mirrored or expanded"""
            def get_dates():
                dates = ["2000-01-01", "9999-01-01"]
                start, end = [datetime.strptime(
                    dummy, "%Y-%m-%d") for dummy in dates]
                dates = OrderedDict(((start + timedelta(
                    dummy)).strftime(r"%Y%b"), None)
                    for dummy in range((end - start).days)).keys()
                return dates
            # verify if volume is mirrored or expanded
            dates = get_dates()
            if len(children) == 0:
                return None
            expanded = False
            for child in list(children.keys()):
                if child.split(vol_dev_name)[-1][:7] in dates:
                    children.pop(child)
                    expanded = True
            if not expanded:
                return 'mirrored'
            return 'expanded'

        def rename(new_vol_name):
            payload = [{
                "op": "replace",
                "path": "/name",
                "value": new_vol_name}]
            self.vol_obj = self.update_volume(payload)

        state = self.module.params['state']
        vol_name = self.module.params['virtual_volume_name']
        vol_id = self.module.params['virtual_volume_id']
        new_vol_name = self.module.params['new_virtual_volume_name']
        support_dev_name = self.module.params['supporting_device_name']
        thin_enabled = self.module.params['thin_enable']
        chk_rebuild = self.module.params['wait_for_rebuild']
        expand = self.module.params['expand']
        remote_access = self.module.params['remote_access']
        additional_devs = self.module.params['additional_devices']
        cache_invalidate = self.module.params['cache_invalidate']

        changed = False
        vol_type = None

        if vol_name:
            self.vol_obj, err_msg = self.get_volume_by_name(vol_name)
        if not self.vol_obj and vol_id:
            self.vol_obj, err_msg = self.get_volume_by_id(vol_id)
        if not any([vol_name, vol_id]):
            err_msg = "Both volume name and volume id can not be None"
        if err_msg:
            LOG.error(err_msg)

        # delete virtual volume
        if state == 'absent':
            if self.vol_obj:
                LOG.info('Trying to delete virtual volume %s',
                         self.vol_obj.name)
                msg = 'Could not delete the virtual volume {0} in {1}, ' \
                    'since '.format(self.vol_obj.name, self.cluster_name)
                if self.vol_obj.consistency_group:
                    msg += 'virtual volume is a part of Consistency Group'
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                if self.vol_obj.service_status != 'unexported':
                    msg += 'virtual volume is not uexported'
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                changed = self.delete_volume()
            else:
                msg = 'Volume is not present to delete'
                LOG.info(msg)
            exit_module({}, changed)

        # create virtual volume
        if state == 'present' and support_dev_name and not self.vol_obj:
            if new_vol_name:
                msg = "Could not perform create and rename in a single " \
                    "task. Please specify each operation in individual task."
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            if vol_name:
                LOG.info('Trying to create virtual volume from %s',
                         support_dev_name)
                verify_new_volume_name(vol_name, 'virtual_volume_name')
                dev = dev_checks(support_dev_name, chk_top_level=True,
                                 chk_rebuild=chk_rebuild)
                if dev.virtual_volume is None:
                    uri = '/vplex/v2/clusters/{0}/devices/{1}'.format(
                        self.cluster_name, support_dev_name)
                    payload = {
                        "thin": thin_enabled,
                        "device": uri
                    }
                    self.vol_obj = self.create_volume(payload)
                    changed = True
                    if vol_name != self.vol_obj.name:
                        rename(vol_name)
                else:
                    vol_name = dev.virtual_volume.split('/')[-1]
                    msg = 'Device {0} is already attached to volume {1} ' \
                        'in {2}'.format(dev.name, vol_name,
                                        self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
            else:
                msg = 'Supporting device and volume name must be given to ' \
                    'create virtual volume'
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Perform cache invalidate
        version = utils.get_vplex_setup(self.client)
        if '6.2' in version:
            vplex_version = 6
        else:
            vplex_version = 7

        if state == 'present' and self.vol_obj and cache_invalidate and \
                self.vol_obj.service_status != 'unexported':
            dir_status = self.director_status()
            if dir_status is not None:
                msg = ("For cache invalidate operation, directors "
                       "communication status must be 'ok'")
                self.module.fail_json(msg=msg)
            if vplex_version > 6:
                msg = ("To perform cache invalidate the VPLEX version "
                       "should be 6.2 or lesser")
                self.module.fail_json(msg=msg)
            else:
                self.vol_obj, msg = self.cache_invalidate(vol_name)
                if self.vol_obj is None:
                    self.module.fail_json(msg=msg)
                changed = True

        # remaining all operations required state and vol_obj to be present,
        # exit if vol_obj is not avilable in this stage
        if not self.vol_obj:
            volume = vol_name if vol_name else vol_id
            msg = 'Could not get \'{0}\' volume details in {1}.'.format(
                volume, self.cluster_name)
            logmsg = msg + '\nAll below operations required correct volume' \
                ' details:\n\tRename virtual volume' \
                '\n\tEnable/Disable remote access' \
                '\n\tExpand virtual volume'
            LOG.error(logmsg)
            self.module.fail_json(msg=msg)

        # rename virtual volume
        if new_vol_name:
            LOG.info('Trying to rename volume from %s to %s',
                     self.vol_obj.name, new_vol_name)
            if new_vol_name == self.vol_obj.name:
                msg = 'New name is same as old name, '\
                    'No need to rename volume.'
                LOG.info(msg)
            else:
                verify_new_volume_name(new_vol_name)
                rename(new_vol_name)
                changed = True
                LOG.info('Volume name updated to %s',
                         self.vol_obj.name)

        vol_dev_name = self.vol_obj.supporting_device.split('/')[-1]

        # enable/disable remote access
        if remote_access:
            LOG.info('Trying to %sing remote access ', remote_access[:-1])
            # enable/disable remote access can be updated
            # in rebuilding state as well
            payload = None

            if self.vol_obj.visibility == 'local' and \
                    remote_access == 'enable':
                payload = [{
                    "op": "replace",
                    "path": "/visibility",
                    "value": "global"
                }]
            elif self.vol_obj.visibility == 'global' and \
                    remote_access == 'disable':
                payload = [{
                    "op": "replace",
                    "path": "/visibility",
                    "value": "local"
                }]
            if payload:
                if self.volume_exists_in_other_clusters(self.vol_obj.name):
                    msg = "Could not update remote access of virtual volume "\
                        "{0} in {1}, since virtual volume with same name "\
                        "exists in another clusters".format(
                            self.vol_obj.name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                if self.device_exists_in_other_clusters(vol_dev_name):
                    msg = "Could not update remote access of virtual volume "\
                        "{0} in {1}, since device with same name exists "\
                        "in another clusters".format(
                            vol_dev_name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                dev, changed = self.update_device(vol_dev_name, payload)
                if not changed:
                    self.module.fail_json(msg=dev)
                self.vol_obj, dummy = self.get_volume_by_name(
                    self.vol_obj.name)

        # If a virtual_volume has a mirror device,
        # we should not allow additional devices to be added to it.
        dev_uri = '/vplex/v2/clusters/{0}/devices/{1}'.format(
            self.cluster_name, vol_dev_name)
        children = self.get_map(dev_uri).children
        # create dict of dev_name and uri
        children = {child.split(
            '/')[-1]: child for child in children if '/extents/' not in child}
        vol_type = get_volume_type(children)

        # expand volume
        if vplex_version > 6 and len(additional_devs) > 0:
            msg = ("To perform expand with additional device(s) the VPLEX "
                   "version should be 6.2 or lesser")
            self.module.fail_json(msg=msg)
        if additional_devs and not expand:
            msg = 'Could not expand virtual volume {0} in ' \
                '{1}, expand parameter should be set true to ' \
                'expand.'.format(self.vol_obj.name, self.cluster_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        if len(additional_devs) > 0 and expand:
            LOG.info('Trying to expand volume using additional devices')
            if vol_type == 'mirrored':
                LOG.info('Children: %s', children)
                msg = 'Could not expand virtual volume {0} in ' \
                    '{1}, volume is mirrored already, can not be ' \
                    'expanded.'.format(self.vol_obj.name, self.cluster_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            err_msg = 'Could not expand virtual volume {0} in ' \
                '{1}, additional_devices must has all the devices in an ' \
                'ordered list.'.format(self.vol_obj.name, self.cluster_name)
            err_msg += ' Current list: %s' % list(children.keys())

            if len(children) <= len(additional_devs):
                for child, new_child in zip(children, additional_devs):
                    if child != new_child:
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)

                if len(children) == len(additional_devs):
                    msg = 'All devices are already added'
                    LOG.info(msg)
                    LOG.debug(additional_devs)
                    exit_module(self.vol_obj, changed)
                else:
                    additional_devs = additional_devs[len(children):]

                # check if devices is used by another volume
                for dev in additional_devs:
                    dev_checks(dev, chk_vol=True, chk_top_level=True)

                capacity = self.vol_obj.capacity
                LOG.info('Capacity: %s', capacity)

                for dev in additional_devs:
                    dev_uri = '/vplex/v2/clusters/{0}/devices/{1}'.format(
                        self.cluster_name, dev)
                    payload = {
                        "skip_init": "False",
                        "spare_storage": dev_uri
                    }
                    LOG.debug('Expand Payload: %s', payload)
                    self.vol_obj = self.expand_volume(payload)
                if capacity < self.vol_obj.capacity:
                    msg = 'Capacity increased from {0} to {1}.'.format(
                        capacity, self.vol_obj.capacity)
                    LOG.info(msg)
                    changed = True
            else:
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
        elif self.vol_obj.expandable_capacity > 0 and expand:
            LOG.info('Trying to expand volume from backend array')
            capacity = self.vol_obj.capacity
            LOG.info('Capacity: %s', capacity)
            payload = {"skip_init": "False"}
            LOG.debug('Expand Payload: %s', payload)
            self.vol_obj = self.expand_volume(payload)
            if capacity < self.vol_obj.capacity:
                msg = 'Capacity increased from {0} to {1}.'.format(
                    capacity, self.vol_obj.capacity)
                LOG.info(msg)
                changed = True

        exit_module(self.vol_obj, changed)


def get_user_parameters():
    """This method provide the parameters required for the ansible
    virtual volume module on VPLEX"""
    return dict(
        state=dict(type='str', required=True,
                   choices=['present', 'absent']),
        cluster_name=dict(type='str', required=True),
        virtual_volume_name=dict(type='str', required=False),
        virtual_volume_id=dict(type='str', required=False),
        new_virtual_volume_name=dict(type='str', required=False),
        supporting_device_name=dict(type='str', required=False),
        thin_enable=dict(type='bool', required=False, default=True,
                         choices=[True, False]),
        wait_for_rebuild=dict(type='bool', required=False, default=True),
        expand=dict(required=False, type='bool'),
        remote_access=dict(type='str', required=False,
                           choices=['enable', 'disable']),
        additional_devices=dict(type='list', required=False, default=[],
                                elements='str'),
        cache_invalidate=dict(type='bool', required=False, default=False,
                              choices=[True, False])
    )


def main():
    """Create VPLEX StorageVolumeModule object and perform action on it
        based on user input from playbook"""
    svm = VirtualVolumeModule()
    svm.perform_module_operation()


if __name__ == '__main__':
    main()
