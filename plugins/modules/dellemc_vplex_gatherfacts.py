#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" GatherFacts module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_gatherfacts
version_added: '1.2.0'
short_description: Gathers information about VPLEX Storage details
description:
- Gathers the list of specified VPLEX Storage entities like the list
  of storage arrays, storage volumes, storage views, ports, initiators,
  virtual volumes, consistency groups, local/distributed devices, extents
  ditributed consistency groups, distributed virtual volumes, back end ports,
  device migration jobs, extent migration jobs and array management providers.
extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex
author:
- Mohana Priya Sivalingam (@mohanapriya-dell) <vplex.ansible@dell.com>
options:
  cluster_name:
    description:
    - Name of the cluster
    type: str

  gather_subset:
    description:
    - List of string variables to specify the VPLEX entities for which
      information is required.
    - stor_array - storage array
    - stor_vol - storage volumes
    - stor_view - storage views
    - port - ports
    - initiator - initiators
    - virt_vol - virtual volumes
    - cg - consistency groups
    - device - devices
    - extent - extents
    - dist_device - distributed devices
    - dist_cg - distributed consistency groups
    - dist_virt_vol - distributed virtual volumes
    - amp - array management providers
    - be_port - back end ports
    - device_mig_job - device migration jobs
    - extent_mig_job - extent migration jobs
    type: list
    elements: str
    choices: [stor_array, stor_vol, stor_view, port, initiator, virt_vol, cg,
              device, extent, dist_device, dist_cg, dist_virt_vol, amp,
              be_port, device_mig_job, extent_mig_job]

  filters:
    description:
    - List of filters to support filtered output for storage entities.
    - Each filter is a list of {filter_key, filter_operator, filter_value}.
    - Supports passing of multiple filters.
    required: False
    type: list
    elements: dict
    suboptions:
      filter_key:
        description:
        - Name identifier of the filter.
        type: str
        required: True
      filter_operator:
        description:
        - Operation to be performed on filter key.
        type: str
        choices: [equal, greater, lesser, greater-equal, lesser-equal]
        required: True
      filter_value:
        description:
        - Value of the filter key.
        type: str
        required: True
'''

EXAMPLES = r'''
- name: Get list of clusters
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"

- name: Get list of storage arrays
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - stor_array

- name: Get list of storage volumes
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - stor_vol
    filters:
      - filter_key: "capacity"
        filter_operator: "greater"
        filter_value: "4GB"
      - filter_key: "sort_by"
        filter_operator: "equal"
        filter_value: "use,name"

- name: Get list of back end ports
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - be_port

- name: Get list of ports
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - port

- name: Get list of initiators
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - initiator

- name: Get list of storage views
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - stor_view

- name: Get list of virtual volumes
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - virt_vol

- name: Get list of consistency groups
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - cg

- name: Get list of devices
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - device

- name: Get list of distributed devices
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - dist_device

- name: Get list of distributed consistency groups
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - dist_cg

- name: Get list of distributed virtual volumes
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - dist_virt_vol

- name: Get list of registered array management providers
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - amp

- name: Get list of extents
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    gather_subset:
      - extent

- name: Get list of device migration jobs
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - device_mig_job

- name: Get list of extent migration jobs
  dellemc_vplex_gatherfacts:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    gather_subset:
      - extent_mig_job

'''

RETURN = r'''
Clusters:
    description: List of clusters present in VPLEX
    returned: when cluster name is not present
    type: list
    contains:
        name:
            description: name of the cluster
            type: str

Storage Arrays:
    description: List of Storage Arrays in a cluster
    returned: When Storage Arrays exist
    type: list
    contains:
        name:
            description: Storage Array names
            type: str

Storage Volumes:
    description: List of Storage Volumes in a cluster
    returned: When Storage Volumes exist
    type: list
    contains:
        name:
            description: Storage Volume names
            type: str

Ports:
    description: List of Ports in a cluster
    returned: When Ports exist
    type: list
    contains:
        name:
            description: Port names
            type: str

Back End Ports:
    description: List of back end Ports in VPLEX
    returned: When back end ports exist
    type: complex
    contains:
        address:
            description: Addres of the back end port
            type: str
        name:
            description: Back end port name
            type: str
        director:
            description: Director the port is attached to
            type: str
        role:
            description: Type of the port
            type: str
        status:
            description: Status of the Back end port
            type: str

Initiators:
    description: List of Initiators in a cluster
    returned: When Initiators exist
    type: complex
    contains:
        name:
            description: Initiator names
            type: str
        type:
            description: Host type
            type: str

Storage Views:
    description: List of Storage Views in a cluster
    returned: When Storage Views exist
    type: list
    contains:
        name:
            description: Storage View names
            type: str

Virtual Volumes:
    description: List of Virtual Volumes in a cluster
    returned: When Virtual Volumes exist
    type: list
    contains:
        name:
            description: Virtual Volume names
            type: str

Consistency Groups:
    description: List of Consistency Groups in a cluster
    returned: When Consistency Groups exist
    type: list
    contains:
        name:
            description: Consistency Group names
            type: str

Devices:
    description: List of local Devices in a cluster
    returned: When Devices exist
    type: list
    contains:
        name:
            description: Local Device names
            type: str

Distributed Devices:
    description: List of Distributed Devices(metro) in VPLEX
    returned: When Distributed Devices exist
    type: list
    contains:
        name:
            description: Distributed Device names
            type: str

Distributed Consistency Groups:
    description: List of Distributed Consistency Groups(metro) in VPLEX
    returned: When Distributed Consistency Groups exist
    type: list
    contains:
        name:
            description: Distributed Consistency Group names
            type: str

Distributed Virtual Volumes:
    description: List of Distributed Virtual Volumes(metro) in VPLEX
    returned: When Distributed Virtual Volumes exist
    type: list
    contains:
        name:
            description: Distributed Virtual Volume names
            type: str

Array Management Providers:
    description: List of registered Array Management Providers in a cluster
    returned: When Array Management Providers exist
    type: list
    contains:
        name:
            description: Array Management Provider names
            type: str

Extents:
    description: List of Extents in a cluster
    returned: When Extent exist
    type: list
    contains:
        name:
            description: Extent names
            type: str

Device Migration Jobs:
    description: List of Device migration jobs
    returned: When Device migration jobs exist
    type: list
    contains:
        name:
            description: Device migration job names
            type: str

Extent Migration Jobs:
    description: List of Extent migration jobs
    returned: When Extent migration jobs exist
    type: list
    contains:
        name:
            description: Extent migration job names
            type: str
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_gatherfacts')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexGatherFacts():  # pylint: disable=R0904
    """Class with Gather Facts operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_gatherfacts_parameters())
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
        if self.module.params['cluster_name']:
            cl_name = self.module.params['cluster_name']
            (err_code, msg) = utils.verify_cluster_name(self.client, cl_name)
            if err_code != 200:
                if "Resource not found" in msg:
                    msg = "Could not find resource {0}".format(cl_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        LOG.info("Got VPLEX instance to access common lib methods on VPLEX")

    def logmsg(self, task, details, cluster=None):    # pylint: disable=R0201
        """This method is used to log the success message along with the
           function output details"""
        if cluster:
            msg = "Got {0}s from {1}".format(task, cluster)
        else:
            msg = "Got {0} details from VPLEX".format(task)
        LOG.info(msg)
        LOG.debug("Obtained %s details:\n%s\n", task, details)

    def get_clusters(self, filters_dict=None):
        """Get the list of clusters in VPLEX"""
        try:
            clusters = utils.ClustersApi(api_client=self.client)
            if filters_dict:
                obj = clusters.get_clusters(**filters_dict)
            else:
                obj = clusters.get_clusters(fields=utils.get_cluster_desired_fields())
            self.logmsg('cluster', obj)
            return obj
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Clusters due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_storage_array_list(self, cluster_name=None, filters_dict=None):
        """Get the list of storage arrays on a specific cluster in VPLEX"""
        try:
            storage_array = utils.StorageArrayApi(
                api_client=self.client)
            if filters_dict:
                obj = storage_array.get_storage_arrays(cluster_name,
                                                       **filters_dict)
            else:
                obj = storage_array.get_storage_arrays(cluster_name)
            self.logmsg('Storage Array', obj, cluster_name)
            array_details = utils.serialize_content(obj)
            return self.parse_data(array_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Storage Arrays from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_storage_volume_list(self, cluster_name=None, filters_dict=None):
        """Get the list of storage volumes on a specific cluster in VPLEX"""
        try:
            storage_volume = utils.StorageVolumeApi(
                api_client=self.client)
            if filters_dict:
                obj = storage_volume.get_storage_volumes(cluster_name,
                                                         **filters_dict)
            else:
                obj = storage_volume.get_storage_volumes(cluster_name)
            self.logmsg('Storage Volume', obj, cluster_name)
            volume_details = utils.serialize_content(obj)
            return self.parse_data(volume_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Storage Volumes from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_port_list(self, cluster_name=None, filters_dict=None):
        """Get the list of ports on a specific cluster in VPLEX"""
        try:
            port = utils.ExportsApi(api_client=self.client)
            if filters_dict:
                obj = port.get_ports(cluster_name, **filters_dict)
            else:
                obj = port.get_ports(cluster_name)
            self.logmsg('Port', obj, cluster_name)
            port_details = utils.serialize_content(obj)
            return self.parse_data(port_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Ports from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_be_port_list(self, filters_dict=None):
        """Get the list of back end ports on a specific cluster in VPLEX"""
        try:
            be_port = utils.HardwarePortsApi(api_client=self.client)
            if filters_dict:
                obj = be_port.get_hardware_ports(role="back-end",
                                                 **filters_dict)
            else:
                obj = be_port.get_hardware_ports(role="back-end")
            self.logmsg('Back end Port', obj)
            port_details = utils.serialize_content(obj)
            return port_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Back end Ports due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_initiator_list(self, cluster_name=None, filters_dict=None):
        """Get the list of initiators on a specific cluster in VPLEX"""
        try:
            initiator = utils.ExportsApi(api_client=self.client)
            if filters_dict:
                obj = initiator.get_initiator_ports(cluster_name,
                                                    **filters_dict)
            else:
                obj = initiator.get_initiator_ports(cluster_name)
            self.logmsg('Initiator', obj, cluster_name)
            initiator_details = utils.serialize_content(obj)
            return self.parse_data(initiator_details, initiator=True)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Initiators from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_storage_view_list(self, cluster_name=None, filters_dict=None):
        """Get the list of storage views on a specific cluster in VPLEX"""
        try:
            storage_view = utils.ExportsApi(api_client=self.client)
            if filters_dict:
                obj = storage_view.get_storage_views(cluster_name,
                                                     **filters_dict)
            else:
                obj = storage_view.get_storage_views(cluster_name)
            self.logmsg('Storage View', obj, cluster_name)
            view_details = utils.serialize_content(obj)
            return self.parse_data(view_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Storage Views from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_virtual_volume_list(self, cluster_name=None, filters_dict=None):
        """Get the list of virtual volumes on a specific cluster in VPLEX"""
        try:
            virtual_volume = utils.VirtualVolumeApi(
                api_client=self.client)
            if filters_dict:
                obj = virtual_volume.get_virtual_volumes(cluster_name,
                                                         **filters_dict)
            else:
                obj = virtual_volume.get_virtual_volumes(cluster_name)
            self.logmsg('Virtual Volume', obj, cluster_name)
            virt_vol_details = utils.serialize_content(obj)
            return self.parse_data(virt_vol_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Virtual Volumes from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_consistency_group_list(self, cluster_name=None, filters_dict=None):
        """Get the list of consistency groups on a specific cluster in VPLEX"""
        try:
            consistency_grp = utils.ConsistencyGroupApi(
                api_client=self.client)
            if filters_dict:
                obj = consistency_grp.get_consistency_groups(cluster_name,
                                                             **filters_dict)
            else:
                obj = consistency_grp.get_consistency_groups(cluster_name)
            self.logmsg('Consistency Group', obj, cluster_name)
            consistency_grp_details = utils.serialize_content(obj)
            return self.parse_data(consistency_grp_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Consistency Groups from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_device_list(self, cluster_name=None, filters_dict=None):
        """Get the list of local devices on a specific cluster in VPLEX"""
        try:
            device = utils.DevicesApi(api_client=self.client)
            if filters_dict:
                obj = device.get_devices(cluster_name, **filters_dict)
            else:
                obj = device.get_devices(cluster_name)
            self.logmsg('Device', obj, cluster_name)
            device_details = utils.serialize_content(obj)
            return self.parse_data(device_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get local Devices from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_distributed_device_list(self, filters_dict=None):
        """Get the list of (metro) distributed devices in VPLEX"""
        try:
            dist_dev = utils.DistributedStorageApi(
                api_client=self.client)
            if filters_dict:
                obj = dist_dev.get_distributed_devices(**filters_dict)
            else:
                obj = dist_dev.get_distributed_devices()
            self.logmsg('Distributed Device', obj)
            dist_device_details = utils.serialize_content(obj)
            return self.parse_data(dist_device_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Distributed Devices due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_distributed_consistency_group_list(self, filters_dict=None):
        """Get the list of distributed consistency groups in VPLEX"""
        try:
            dist_cgp = utils.DistributedStorageApi(
                api_client=self.client)
            if filters_dict:
                obj = dist_cgp.get_distributed_consistency_groups(
                    **filters_dict)
            else:
                obj = dist_cgp.get_distributed_consistency_groups()
            self.logmsg('Distributed Consistency Group', obj)
            dist_cg_details = utils.serialize_content(obj)
            return self.parse_data(dist_cg_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Distributed Consistency Groups due to"
            err_msg = err_msg + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_distributed_virtual_volume_list(self, filters_dict=None):
        """Get the list of distributed virtual volumes in VPLEX"""
        try:
            dist_virt_volume = utils.DistributedStorageApi(
                api_client=self.client)
            if filters_dict:
                obj = dist_virt_volume.get_distributed_virtual_volumes(
                    **filters_dict)
            else:
                obj = dist_virt_volume.get_distributed_virtual_volumes()
            self.logmsg('Distributed Virtual Volume', obj)
            dist_virvol_details = utils.serialize_content(obj)
            return self.parse_data(dist_virvol_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Distributed Virtual Volumes due to"
            err_msg = err_msg + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_array_management_provider_list(self, cluster_name=None,
                                           filters_dict=None):
        """Get the list of registered array management providers on a
        specific cluster in VPLEX"""
        try:
            amps = utils.AmpApi(api_client=self.client)
            if filters_dict:
                obj = amps.get_array_management_providers(cluster_name,
                                                          **filters_dict)
            else:
                obj = amps.get_array_management_providers(cluster_name)
            self.logmsg('Array Management Provider', obj, cluster_name)
            amp_details = utils.serialize_content(obj)
            return self.parse_data(amp_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Array Management Providers from {0}"
            err_msg = err_msg.format(cluster_name) + " due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_extent_list(self, cluster_name=None, filters_dict=None):
        """Get the list of extents on a specific cluster in VPLEX"""
        try:
            extent = utils.ExtentApi(api_client=self.client)
            if filters_dict:
                obj = extent.get_extents(cluster_name, **filters_dict)
            else:
                obj = extent.get_extents(cluster_name)
            self.logmsg('Extent', obj, cluster_name)
            device_details = utils.serialize_content(obj)
            return self.parse_data(device_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Extents from {0} due to"
            err_msg = err_msg.format(cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_extent_migration_list(self, filters_dict=None):
        """Get the list of extent migration jobs in VPLEX"""
        try:
            extent_mig = utils.DataMigrationApi(api_client=self.client)
            if filters_dict:
                obj = extent_mig.get_extent_migrations(**filters_dict)
            else:
                obj = extent_mig.get_extent_migrations()
            self.logmsg('Extent migration job', obj)
            extent_mig_details = utils.serialize_content(obj)
            return self.parse_data(extent_mig_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Extent migration jobs due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_device_migration_list(self, filters_dict=None):
        """Get the list of device migration jobs in VPLEX"""
        try:
            device_mig = utils.DataMigrationApi(api_client=self.client)
            if filters_dict:
                obj = device_mig.get_device_migrations(**filters_dict)
            else:
                obj = device_mig.get_device_migrations()
            self.logmsg('Device migration job', obj)
            device_mig_details = utils.serialize_content(obj)
            return self.parse_data(device_mig_details)
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get Device migration jobs due to error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_filters(self, filters=None):  # pylint: disable=R0912, R0915
        """Get the filters to be applied"""
        filters_dict = {}
        for item in filters:
            if 'filter_key' in item and 'filter_operator' in item\
                    and 'filter_value' in item:
                if item["filter_key"] is None \
                        or item["filter_operator"] is None \
                        or item["filter_value"] is None:
                    error_msg = "Please provide input for filter sub-options."
                    LOG.error(error_msg)
                    self.module.fail_json(msg=error_msg)
                else:
                    f_key = item["filter_key"]
                    if item["filter_operator"] == "equal":
                        f_operator = ""
                    elif item["filter_operator"] == "greater":
                        f_operator = "gt~"
                    elif item["filter_operator"] == "lesser":
                        f_operator = "lt~"
                    elif item["filter_operator"] == "greater-equal":
                        f_operator = "gte~"
                    elif item["filter_operator"] == "lesser-equal":
                        f_operator = "lte~"
                    else:
                        msg = "The filter operator is not supported -- only" \
                              " 'equal', 'greater-equal', 'lesser-equal'," \
                              " 'greater' and 'lesser' are supported."
                        LOG.error(msg)
                        self.module.fail_json(msg=msg)

                    val = item["filter_value"]
                    if val in ('True', 'False'):
                        f_value = val
                    elif re.match('^[0-9]+$', val):
                        if f_operator == "":
                            f_value = int(val)
                        else:
                            f_value = f_operator + val
                    else:
                        if re.match('^[0-9]+TB$', val):
                            val = int(val.split('TB')[0]) * 1024 * 1024 \
                                * 1024 * 1024
                        elif re.match('^[0-9]+GB$', val):
                            val = int(val.split('GB')[0]) * 1024 * 1024 * 1024
                        elif re.match('^[0-9]+MB$', val):
                            val = int(val.split('MB')[0]) * 1024 * 1024
                        elif re.match('^[0-9]+B$', val):
                            val = int(val.split('B')[0])
                        f_value = f_operator + str(val)

                    if f_key in filters_dict and \
                            not isinstance(filters_dict[f_key], int):
                        filters_dict[f_key] = filters_dict[f_key] + ',' + \
                            f_value
                    else:
                        filters_dict[f_key] = f_value
            else:
                msg = 'filter_key and filter_operator and filter_value is ' \
                      'expected, "%s" given.' % list(item.keys())
                LOG.error(msg)
                self.module.fail_json(msg=msg)
        # check for offset and limit are present together
        if 'limit' in filters_dict.keys() and \
                'offset' not in filters_dict.keys() or \
                'offset' in filters_dict.keys() and \
                'limit' not in filters_dict.keys():
            msg = "'limit' and 'offset' filter keys must be specified together"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        LOG.info("Query parameters: %s", filters_dict)
        return filters_dict

    def parse_data(self, obj_data, initiator=False):   # pylint: disable=R0201
        """This method parses the fields in the object data and
        returns as a list"""
        parsed_list = []
        LOG.info('Parsing the entire details to fetch a list of required data')
        for item in obj_data:
            if initiator is True:
                if 'type' in item.keys():
                    parsed_list.append(dict({'name': item['name'],
                                             'type': item['type']}))
                else:
                    parsed_list.append(dict({'name': item['name']}))
            else:
                parsed_list.append(item['name'])
        return parsed_list

    def perform_module_operation(self):    # pylint: disable=R0914,R0912,R0915
        """This method invokes the user VPLEX operation"""
        cluster_name = self.module.params['cluster_name']
        subset = self.module.params['gather_subset']
        filters = self.module.params['filters']
        nondistributed_check = False

        filters_dict = {}
        if filters:
            filters_dict = self.get_filters(filters=filters)

        cluster_obj = self.get_clusters()
        cluster_details = utils.serialize_content(cluster_obj)
        cluster_list = self.parse_data(cluster_details)

        if subset is not None:
            storage_array = []
            storage_volume = []
            port = []
            be_port = []
            initiator = []
            storage_view = []
            virtual_volume = []
            conscy_gp = []
            device = []
            dist_device = []
            dist_cg = []
            dist_virt_vol = []
            amp = []
            extent = []
            device_mig_job = []
            extent_mig_job = []

            # Local list to avoid cluster name dependency for distributed cases
            temp_list = ['stor_array', 'stor_vol', 'port', 'initiator', 'cg',
                         'stor_view', 'virt_vol', 'device', 'extent', 'amp']
            for item in temp_list:
                if item in subset:
                    nondistributed_check = True
                    break

            if ((cluster_name == '') and (nondistributed_check is True)):
                self.module.exit_json(Clusters=cluster_details)
            else:
                if 'stor_array' in subset:
                    storage_array = self.get_storage_array_list(
                        cluster_name, filters_dict=filters_dict)
                if 'stor_vol' in subset:
                    storage_volume = self.get_storage_volume_list(
                        cluster_name, filters_dict=filters_dict)
                if 'port' in subset:
                    port = self.get_port_list(
                        cluster_name, filters_dict=filters_dict)
                if 'be_port' in subset:
                    be_port = self.get_be_port_list(filters_dict=filters_dict)
                if 'initiator' in subset:
                    initiator = self.get_initiator_list(
                        cluster_name, filters_dict=filters_dict)
                if 'stor_view' in subset:
                    storage_view = self.get_storage_view_list(
                        cluster_name, filters_dict=filters_dict)
                if 'virt_vol' in subset:
                    virtual_volume = self.get_virtual_volume_list(
                        cluster_name, filters_dict=filters_dict)
                if 'cg' in subset:
                    conscy_gp = self.get_consistency_group_list(
                        cluster_name, filters_dict=filters_dict)
                if 'device' in subset:
                    device = self.get_device_list(
                        cluster_name, filters_dict=filters_dict)
                if 'dist_device' in subset:
                    dist_device = self.get_distributed_device_list(
                        filters_dict=filters_dict)
                if 'dist_cg' in subset:
                    dist_cg = self.get_distributed_consistency_group_list(
                        filters_dict=filters_dict)
                if 'dist_virt_vol' in subset:
                    dist_virt_vol = self.get_distributed_virtual_volume_list(
                        filters_dict=filters_dict)
                if 'device_mig_job' in subset:
                    device_mig_job = self.get_device_migration_list(
                        filters_dict=filters_dict)
                if 'extent_mig_job' in subset:
                    extent_mig_job = self.get_extent_migration_list(
                        filters_dict=filters_dict)
                if 'amp' in subset:
                    vplex_setup = utils.get_vplex_setup(self.client)
                    if '6.2' in vplex_setup:
                        amp = self.get_array_management_provider_list(cluster_name, filters_dict=filters_dict)
                if 'extent' in subset:
                    extent = self.get_extent_list(
                        cluster_name, filters_dict=filters_dict)
                self.module.exit_json(
                    StorageArrays=storage_array,
                    StorageVolumes=storage_volume,
                    Ports=port,
                    BackEndPorts=be_port,
                    Initiators=initiator,
                    StorageViews=storage_view,
                    VirtualVolumes=virtual_volume,
                    ConsistencyGroups=conscy_gp,
                    Devices=device,
                    Extents=extent,
                    DistributedDevices=dist_device,
                    DistributedConsistencyGroups=dist_cg,
                    DistributedVirtualVolumes=dist_virt_vol,
                    DeviceMigrationJobs=device_mig_job,
                    ExtentMigrationJobs=extent_mig_job,
                    ArrayManagementProviders=amp)

        else:
            self.module.exit_json(Clusters=cluster_list)


def get_vplex_gatherfacts_parameters():
    """This method provide the parameters required for the ansible
    gather facts module on VPLEX"""
    return dict(
        cluster_name=dict(type='str', required=False, default=''),
        gather_subset=dict(type='list', required=False, elements='str',
                           choices=['stor_array',
                                    'stor_vol',
                                    'port',
                                    'be_port',
                                    'initiator',
                                    'stor_view',
                                    'virt_vol',
                                    'cg',
                                    'device',
                                    'extent',
                                    'dist_device',
                                    'dist_cg',
                                    'dist_virt_vol',
                                    'device_mig_job',
                                    'extent_mig_job',
                                    'amp',
                                    ]),
        filters=dict(type='list', required=False, elements='dict',
                     options=dict(
                         filter_key=dict(type='str', required=True),
                         filter_operator=dict(type='str', required=True,
                                              choices=['equal', 'greater',
                                                       'lesser',
                                                       'greater-equal',
                                                       'lesser-equal']),
                         filter_value=dict(type='str', required=True))
                     )

    )


def main():
    """Create VplexGatherFacts object and perform action on it
        based on user input from playbook"""
    obj = VplexGatherFacts()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
