#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Device module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_device
version_added: '1.2.0'
short_description:  Manage storage device on VPLEX Storage System
description:
- Provisioning the storage device on VPLEX Storage System includes
  Create a new Device,
  Delete an existing Device,
  Get information about existing Device,
  Rename existing Device,
  Add extent to the Device,
  Remove extent from the Device.
  Add remote/local mirror to the Device
  Remove remote/local mirror from the Device

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

  target_cluster:
    description:
    - The name of the target cluster where the mirror is present
    type: str

  device_name:
    description:
    - Name of the device
    required: true
    type: str

  geometry:
    description:
    - RAID volume type
    choices: ['raid-0', 'raid-1', 'raid-c']
    default: 'raid-1'
    type: str

  stripe_depth:
    description:
    - stripe_depth to create raid-0 device
    type: str

  extents:
    description:
    - Name of the extents
    type: list
    elements: str

  extent_state:
    description:
    - To determine whether add/remove extent
    choices: ['absent-in-device', 'present-in-device']
    type: str

  new_device_name:
    description:
    - New name of the device
    type: str

  state:
    description:
    - Define whether the device should exist or not
    required: true
    choices: ['absent', 'present']
    type: str

  transfer_size:
    description:
    - Size of the region in cache used to service the migration
    type: int

  mirror_name:
    description:
    - Name of the mirror
    type: str

  mirror_state:
    description:
    - To determine whether add/remove mirror
    choices: ['absent-in-device', 'present-in-device']
    type: str

  '''
EXAMPLES = r'''

- name: Create a new raid-1 device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    geometry: "raid-1"
    device_name: "ansible_device_1"
    extents: ["extent_1", "extent_2"]
    extent_state: "present-in-device"
    state: "present"

- name: Create a new raid-0 device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    geometry: "raid-0"
    stripe_depth: "4KB"
    device_name: "ansible_device_1"
    extents: ["extent_1", "extent_2"]
    extent_state: "present-in-device"
    state: "present"

- name: Get device from cluster
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    state: "present"

- name: Delete device from cluster
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    state: "absent"

- name: Rename a local device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    new_device_name: "new_device_name"
    state: "present"

- name: Update transfer_size of a local device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    transfer_size: "40960"
    state: "present"

- name: Add extent to device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    extents: ["extent_1", "extent_2"]
    extent_state: "present-in-device"
    state: "present"

- name: Remove extent from Device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    extents: ["extent_1", "extent_2"]
    extent_state: "absent-in-device"
    state: "present"

- name: Add mirror to device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    target_cluster: "cluster-2"
    mirror_name: "mirror_dev_1"
    mirror_state: "present-in-device"
    state: "present"

- name: Remove mirror from device
  dellemc_vplex_device:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    device_name: "ansible_device_1"
    target_cluster: "cluster-2"
    mirror_name: "mirror_dev_1"
    mirror_state: "absent-in-device"
    state: "present"
'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: End of all operations
    type: bool

device_details:
    description: Properties of the device
    returned: When local device exists in VPLEX
    type: complex
    contains:
        application_consistent:
            description:
                - Whether or not this Device is application-consistent
            type: bool
        auto_resume:
            description:
                - Whether or not this Device is support auto_resume
            type: bool
        block_count:
            description:
                - The number of blocks in the device
            type: int
        block_size:
            description:
                - The block size of the device
            type: int
        capacity:
            description:
                - The size of the device
            type: int
        geometry:
            description:
                - RAID level applied to the device
            type: str
        health_indications:
            description:
                - If health-state is not ok return additional information
            type: list
        health_state:
            description:
                - The health state of the device
            type: str
        locality:
            description:
                - Locality of the supporting device
            type: str
        name:
            description:
                - The name of the device
            type: str
        operational_status:
            description:
                - The functional status of the device
            type: str
        rebuild_allowed:
            description:
                - Whether or not this device is allowed to rebuild
            type: bool
        rebuild_eta:
            description:
                - If a rebuild is in progress, the estimated time
                  remaining for the current rebuild to complete
            type: str
        rebuild_progress:
            description:
                - The percentage of this device that has been rebuild
            type: str
        rebuild_status:
            description:
                - The rebuild status of this device
            type: str
        rebuild_type:
            description:
                - The rebuild type
            type: str
        service_status:
            description:
                - The device running status
            type: str
        storage_array_family:
            description:
                - The storage array family name
            type: str
        stripe_depth:
            description:
                - The stripe depth of the raid-0 device
            type: str
        system_id:
            description:
                - The device system id
            type: str
        thin_capable:
            description:
                - Whether or not the device is thin capable
            type: bool
        top_level:
            description:
                - Whether or not the device is top level
            type: bool
        transfer_size:
            description:
                - Size of the region in cache used to service the migration
            type: int
        virtual_volume:
            description:
                - Name of the virtual volume
            type: str
        visibility:
            description:
                - The cluster visibility of the device
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_device')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexDevice():  # pylint: disable=R0902
    """Class with VPLEX Device operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_device_parameters())

        required_together = [['extents', 'extent_state'],
                             ['mirror_name', 'mirror_state']]

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            required_together=required_together,
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

        self.tgcl_name = self.module.params['target_cluster']
        cluster_list = []

        cluster_list.append(self.cl_name)
        if (self.tgcl_name is not None and self.tgcl_name != self.cl_name):
            cluster_list.append(self.tgcl_name)

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
        for cls in cluster_list:
            (err_code, msg) = utils.verify_cluster_name(self.client, cls)
            if err_code != 200:
                if "Resource not found" in msg:
                    msg = "Could not find resource {0}".format(cls)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Create an instance to DeviceApi to communicate with
        # vplexapi
        self.ext = utils.ExtentApi(api_client=self.client)
        self.device = utils.DevicesApi(api_client=self.client)
        self.obj_extent = utils.ExtentApi(api_client=self.client)
        self.distdevice = utils.DistributedStorageApi(api_client=self.client)
        self.maps = utils.MapsApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_device(self, cluster_name, device_name):
        """
        Get the details of a device.
        """
        try:
            all_devices = self.device.get_devices(self.cl_name)
            flag = False
            if all_devices:
                for device in all_devices:
                    if device.name == device_name:
                        flag = True
                        break
            if flag:
                obj_device = self.device.get_device(cluster_name, device_name)
                LOG.info("Got device details %s from %s", device_name, cluster_name)
                LOG.debug("Device Details:\n%s", obj_device)
                device_details = utils.serialize_content(obj_device)
                return device_details
        except utils.ApiException as err:
            err_msg = ("Could not get device {0} of {1} due to"
                       " error: {2}".format(device_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get device {0} of {1} due to"
            err_msg = err_msg.format(device_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def create_device(self, cluster_name, device_payload):
        """
        Create device on VPLEX
        """

        try:
            obj_device = self.device.create_device(
                cluster_name, device_payload)
            LOG.info("Created device %s in %s", device_payload['name'],
                     cluster_name)
            LOG.debug("Device details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not create device {0} in {1} due to"
            err_msg = err_msg.format(device_payload['name'],
                                     cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def delete_device(self, cluster_name, device_name):
        """
        Delete device on VPLEX
        """

        try:
            self.device.delete_device(cluster_name, device_name)
            LOG.info("Deleted device %s from %s", device_name, cluster_name)
            return True
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not delete device {0} from {1} due to"
            err_msg = err_msg.format(device_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_local_device(self, cluster_name,
                            device_name, device_patch_payload):
        """
        Update device attributes
        """

        try:
            LOG.error("Updating the local device")
            LOG.info("Final payload: %s", device_patch_payload)
            obj_device = self.device.patch_local_device(
                cluster_name, device_name, device_patch_payload)
            LOG.info("Updated device %s in %s", device_name, cluster_name)
            LOG.debug("Device details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not update the device {0} in {1} due to"
            err_msg = err_msg.format(device_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def update_dist_device(self, device_name, device_patch_payload):
        """
        Add/Remove mirror to the distributed devices
        """

        try:
            LOG.info("Final payload distributed device: %s",
                     device_patch_payload)
            obj_device = self.distdevice.patch_distributed_device(
                device_name, device_patch_payload)
            LOG.info("Updated the distributed device %s", device_name)
            LOG.debug("Distributed Device details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not update the distributed device {0} due to"
            err_msg = err_msg.format(device_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def is_extent_inuse(self, cluster_name, extent_name):
        """
        Check if the extent is used by any Device
        """

        try:
            extent_details = None
            use = None
            extent_details = self.obj_extent.get_extent(cluster_name,
                                                        extent_name)
            if extent_details:
                LOG.debug("Extent details:\n%s", str(extent_details))
            use = extent_details.use
            extent_details = utils.serialize_content(extent_details)
            return (use, extent_details)

        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get extent details {0} of {1} due to"
            err_msg = err_msg.format(extent_name, cluster_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_device_payload(self,      # pylint: disable=R0913
                           cluster_name, device_name, geometry,
                           stripe_depth, extents):
        """
        Prepare device_payload
        """

        extents = self.get_device_uri(cluster_name, extents)
        device_payload = dict()
        device_payload['name'] = device_name
        device_payload['geometry'] = geometry
        device_payload['primary_leg'] = extents[0]
        if stripe_depth and geometry == 'raid-0':
            device_payload['stripe_depth'] = stripe_depth
        if len(extents) > 1:
            device_payload['secondary_legs'] = extents[1:]
        LOG.info("Create device_payload: %s", device_payload)
        return device_payload

    @classmethod
    def get_device_uri(cls, cluster_name, extents):
        """
        Get the device uri from VPLEX IP
        """

        extents_uri = ["/vplex/v2/clusters/{0}/extents/{1}".format(
            cluster_name, extent) for extent in extents]
        return extents_uri

    @classmethod
    def get_device_patch_payload(cls, operation, path, value):
        """
        Prepare get_device_patch_payload
        """

        patch_payload = {
            'op': operation,
            'path': path,
            'value': value
        }
        return patch_payload

    def get_sd_map(self, stripe_depth):
        """
        Convert the stripe_depth w.r.t vplexapi standard
        """

        mapping = {
            '4KB': '1',
            '8KB': '2',
            '16KB': '4',
            '32KB': '8',
            '64KB': '16',
            '128KB': '32',
            '256KB': '64',
            '512KB': '128',
            '1MB': '256'
        }
        if stripe_depth not in mapping:
            msg = "Unsupported stripe_depth:'{0}'.".format(stripe_depth)
            msg = msg + "Supported values are 4KB, 8KB, 16KB, 32KB, " \
                "64KB, 128KB, 256KB, 512KB, 1MB"
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        return mapping[stripe_depth]

    def validate_device(self, mirror, target_cluster, device_details):
        """
        Check if the mirror device is valid
        """
        mirror_details = self.get_device(target_cluster, mirror)
        # Checking the presence of the mirror device
        if mirror_details is None:
            msg = ("Could not add mirror {0} to device {1}. Mirror not "
                   "present".format(mirror, device_details['name']))
            LOG.error(msg)
            self.module.fail_json(msg=msg)
            return None
        return mirror_details

    def check_task_validity(self, device_name, name):
        """
        Check if the device_name is valid string
        """
        char_len = "63"
        status, msg = utils.validate_name(device_name, char_len, name)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def getdistdev(self, device_name):
        """
        Get the distributed device details
        """
        try:
            list_of_dis_devices = self.distdevice.get_distributed_devices()
            flag = False
            if list_of_dis_devices:
                for dd in list_of_dis_devices:
                    if dd.name == device_name:
                        flag = True
                        break
            if flag:

                details = self.distdevice.get_distributed_device(device_name)
                LOG.info("Got distributed device details %s", device_name)
                LOG.debug("Distributed Device Details:\n%s", details)
                dist_dev_details = utils.serialize_content(details)
                return dist_dev_details
        except utils.ApiException as err:
            err_msg = ("Could not get distributed device {0} due to"
                       " error: {1}".format(device_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None
        except (ValueError, TypeError) as err:
            err_msg = "Could not get distributed device {0} due to"
            err_msg = err_msg.format(device_name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def updatemirror(self, mirror_name, mirror_state,  # pylint: disable=R0913
                     uri, device_details, target_cluster):
        """
        Add/Remove local/remote mirror to the device
        """
        # Form the mirror_uri
        dev_children = []
        children = self.maps.get_map(uri).children
        for child in children:
            if child.split("/")[-2] == "devices":
                dev_children.append(child)

        # Form uri for the mirror device
        mirror_uri = ("/vplex/v2/clusters/{0}/devices/{1}"
                      .format(target_cluster, mirror_name))

        # Form the device patch payload
        if mirror_state == "present-in-device":
            # Form uri for the mirror device
            mirror_details = self.validate_device(mirror_name,
                                                  target_cluster,
                                                  device_details)
            if mirror_uri not in dev_children:
                # The mirror capacity should not be lesser than the
                # device capacity
                if device_details['capacity'] > mirror_details['capacity']:
                    msg = ("The mirror device capacity should not be "
                           "lesser than the device {0} capacity"
                           .format(device_details['name']))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                patch_payload = self.get_device_patch_payload(
                    "add", "/legs", mirror_uri)
                return patch_payload

            msg = ("Mirror {0} is already attached to device {1}"
                   .format(mirror_name, device_details['name']))
            LOG.info(msg)

        elif mirror_state == "absent-in-device":
            if mirror_uri in dev_children:
                patch_payload = self.get_device_patch_payload(
                    "remove", "/legs", mirror_uri)
                return patch_payload

            msg = ("Mirror {0} is not present in device {1}"
                   .format(mirror_name, device_details['name']))
            LOG.info(msg)

        return None

    def perform_module_operation(self):   # pylint: disable=R0915,R0914,R0912
        """
        Perform different actions on Device based on user parameters
        chosen in playbook
        """
        cluster_name = self.module.params['cluster_name']
        geometry = self.module.params['geometry']
        stripe_depth = self.module.params['stripe_depth']
        device_name = self.module.params['device_name']
        extents = self.module.params['extents']
        extent_state = self.module.params['extent_state']
        new_device_name = self.module.params['new_device_name']
        state = self.module.params['state']
        mirror_name = self.module.params['mirror_name']
        mirror_state = self.module.params['mirror_state']
        target_cluster = self.module.params['target_cluster']
        transfer_size = self.module.params['transfer_size']
        changed = False
        result = dict(
            changed=False,
            device_details=None
        )
        device_details = None
        dist_dev_details = None
        device_patch_payload = []
        distdev_patch_payload = []
        create_flag = False
        # Checking the validity of the device name
        self.check_task_validity(device_name, "device name")
        device_details = self.get_device(cluster_name, device_name)
        if device_details is None:
            dist_dev_details = self.getdistdev(device_name)

        # If the target cluster is None it is a local mirror
        if target_cluster is None:
            target_cluster = cluster_name

        if (state == 'present' and not device_details):
            if (extents and extent_state == 'present-in-device'):
                if geometry is None:
                    geometry = 'raid-1'
                if stripe_depth:
                    if geometry in ('raid-1', 'raid-c'):
                        msg = ("stripe_depth not required for '{0}'"
                               .format(geometry))
                        LOG.error(msg)
                        self.module.fail_json(msg=msg)
                    stripe_depth = self.get_sd_map(stripe_depth)
                if geometry == 'raid-0' and not stripe_depth:
                    msg = "stripe_depth required for '{0}'".format(geometry)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                device_payload = self.get_device_payload(
                    cluster_name, device_name, geometry,
                    stripe_depth, extents)
                create_obj = self.create_device(cluster_name, device_payload)
                device_details = utils.serialize_content(create_obj)
                changed = True
                create_flag = True

        # Delete a device
        elif (state == 'absent' and device_details):
            # Cannot delete device if it is in rebuilding state
            if "rebuilding" in device_details["health_indications"]:
                msg = ("Could not delete device {0} since device is"
                       " rebuilding".format(device_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            # Cannot delete device if there is a virtual volume on it
            if ('virtual_volume' in device_details.keys() and
                    device_details['virtual_volume'] is not None):
                msg = ("Could not delete device {0} in {1}, it is in use"
                       .format(device_name, cluster_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            self.delete_device(cluster_name, device_name)
            device_details = None
            changed = True

        # Rename a device
        elif (state == 'present' and new_device_name and device_details):
            self.check_task_validity(new_device_name, "new device name")
            if new_device_name != device_details["name"]:
                get_new_dev = self.get_device(cluster_name, new_device_name)
                if get_new_dev:
                    err_msg = ("New Device name {0} already exists"
                               " in {1}".format(new_device_name, cluster_name))
                    self.module.fail_json(msg=err_msg)
                operation = 'replace'
                path = '/name'
                value = new_device_name
                patch_payload = self.get_device_patch_payload(
                    operation, path, value)
                device_patch_payload.append(patch_payload)
            else:
                LOG.info("The device name and the new device name are the"
                         " same")

        # Update transfer size if given
        if (state == 'present' and transfer_size and device_details):
            if device_details['geometry'] != "raid-1":
                msg = ("Failed to replace property transfer_size, {0} in {1}"
                       " is not a raid-1".format(device_name, cluster_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

            # Validate the transfer size
            if transfer_size != device_details['transfer_size']:
                if transfer_size < 40960:
                    msg = ("Transfer size cannot be less than 40960 bytes. "
                           "Valid range for transfer size is [40960-"
                           "134217728] and should be multiples of 4K(4096)")
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                elif transfer_size > 134217728:
                    msg = ("Transfer size cannot be more than 134217728 "
                           "bytes. Valid range for transfer size is [40960-"
                           "134217728] and should be multiples of 4K(4096)")
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                elif transfer_size % 4096 != 0:
                    msg = ("The transfer size {0} should be in multiples "
                           "of 4K(4096). Valid range for transfer size "
                           "is [40960-134217728]".format(transfer_size))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

                operation = 'replace'
                path = '/transfer_size'
                value = transfer_size
                patch_payload = self.get_device_patch_payload(
                    operation, path, value)
                device_patch_payload.append(patch_payload)

            # Idempotency check for transfer size
            else:
                msg = ("The device {0} on {1} already has the same transfer"
                       " size {2}".format(device_name, cluster_name,
                                          transfer_size))
                LOG.info(msg)

        # Add/Remove extents
        if (state == 'present' and extents and  # pylint: disable=R1702
                extent_state and device_details):
            if device_details["geometry"] == "raid-1":
                for extent in extents:
                    (extent_use, extdetails) = self.is_extent_inuse(
                        cluster_name, extent)
                    if extent_use == "used":
                        used_device_name = extdetails["used_by"][0]
                        used_device_name = used_device_name.split('/')[-1]

                    if extent_state == 'present-in-device':
                        if extent_use == 'claimed':
                            # Checking if the capacity of the extent is
                            # greater than or equal to the device capacity
                            if (device_details["capacity"]
                                    > extdetails["capacity"]):
                                msg = ("Could not attach extent {0} to device"
                                       " {1} in {2}. The size of the device is"
                                       " greater than the extent"
                                       .format(extent, device_name,
                                               cluster_name))
                                LOG.error(msg)
                                self.module.fail_json(msg=msg)

                            operation = 'add'
                            path = '/legs'
                            value = "/vplex/v2/clusters/{}/extents/{}"
                            value = value.format(cluster_name, extent)
                            patch_payload = self.get_device_patch_payload(
                                operation, path, value)
                            device_patch_payload.append(patch_payload)
                        elif (extent_use == 'used' and
                              used_device_name == device_name):
                            msg = ("Extent {0} is already added to device {1}"
                                   " in {2}".format(extent, device_name,
                                                    cluster_name))
                            LOG.info(msg)
                        elif (extent_use == 'used' and
                              used_device_name != device_name):
                            msg = ("Extent {0} is used by another device {1}"
                                   " in {2}".format(extent, used_device_name,
                                                    cluster_name))
                            LOG.error(msg)
                            self.module.fail_json(msg=msg)

                    elif extent_state == 'absent-in-device':
                        if extent_use == 'claimed':
                            msg = ("Extent {0} is not present in the device "
                                   "{1} in {2}"
                                   .format(extent, device_name, cluster_name))
                            LOG.info(msg)
                        elif (extent_use == 'used' and
                              used_device_name != device_name):
                            msg = ("Extent {0} is not present in the device "
                                   "{1} in {2}"
                                   .format(extent, device_name, cluster_name))
                            LOG.info(msg)
                        elif (extent_use == 'used' and
                              used_device_name == device_name):
                            if ("rebuilding" in
                                    device_details["health_indications"]):
                                msg = ("Could not remove extent {0}"
                                       " since the device is in rebuild"
                                       " state".format(str(extents)))
                                LOG.error(msg)
                                self.module.fail_json(msg=msg)
                            operation = 'remove'
                            path = '/legs'
                            value = "/vplex/v2/clusters/{}/extents/{}"
                            value = value.format(cluster_name, extent)
                            patch_payload = self.get_device_patch_payload(
                                operation, path, value)
                            device_patch_payload.append(patch_payload)

            elif (device_details["geometry"] != 'raid-1' and not create_flag):
                exts = []
                flag = False
                uri = ("/vplex/v2/clusters/{0}/devices/{1}".format(
                    cluster_name, device_name))
                children = self.maps.get_map(uri).children
                for child in children:
                    exts.append(child.split("/")[-1])
                if extent_state == "present-in-device":
                    for extent in extents:
                        if extent not in exts:
                            flag = True
                elif extent_state == "absent-in-device":
                    for extent in extents:
                        if extent in exts:
                            flag = True
                        else:
                            msg = ("The extent {0} is not present in {1} "
                                   "in {2}".format(extent, device_name,
                                                   cluster_name))
                            LOG.info(msg)
                if flag:
                    msg = ("Add/Remove extent is supported only on raid-1 "
                           "device")
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                else:
                    if extent_state == "present-in-device":
                        msg = ("The device {0} is already present in "
                               "{1}".format(device_name, cluster_name))
                        LOG.info(msg)

        # Patch operation to add local/remote and remove local mirror
        if (state == 'present' and mirror_name and mirror_state and
                device_details):
            # Get the children of the existing device
            uri = ("/vplex/v2/clusters/{0}/devices/{1}".format(
                cluster_name, device_name))
            patch_payload = self.updatemirror(mirror_name, mirror_state, uri,
                                              device_details, target_cluster)
            if patch_payload is not None:
                device_patch_payload.append(patch_payload)

        elif (state == 'present' and mirror_name and
              mirror_state and device_details is None):
            # Check if the device provided is a distributed device
            if dist_dev_details is not None:
                # Get the children of the existing device
                uri = ("/vplex/v2/distributed_storage/distributed_devices/{0}"
                       .format(device_name))
                patch_payload = self.updatemirror(mirror_name, mirror_state,
                                                  uri, dist_dev_details,
                                                  target_cluster)
                if patch_payload is not None:
                    distdev_patch_payload.append(patch_payload)

        if len(device_patch_payload) > 0:
            device_details = self.update_local_device(
                cluster_name, device_name, device_patch_payload)
            changed = True

        if len(distdev_patch_payload) > 0:
            device_details = self.update_dist_device(
                device_name, distdev_patch_payload)
            changed = True

        if (device_details is None and state == "present"
                and dist_dev_details is None):
            err_msg = ("Could not get device {0} in {1}".format(
                device_name, cluster_name))
            LOG.error("%s\n", err_msg)
            self.module.fail_json(msg=err_msg)

        result['changed'] = changed
        if dist_dev_details:
            dist_dev_details = utils.serialize_content(dist_dev_details)
            result['device_details'] = dist_dev_details
        else:
            result['device_details'] = device_details
        self.module.exit_json(**result)


def get_vplex_device_parameters():
    """This method provide the parameters required for the ansible
    device module on VPLEX
    """
    return dict(
        cluster_name=dict(type='str', required=True),
        geometry=dict(type='str', required=False, default='raid-1',
                      choices=['raid-0', 'raid-1', 'raid-c']),
        stripe_depth=dict(type='str', required=False),
        device_name=dict(type='str', required=True),
        extents=dict(type='list', required=False, elements='str'),
        extent_state=dict(type='str', required=False, choices=[
            'present-in-device', 'absent-in-device']),
        new_device_name=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        mirror_name=dict(type='str', required=False),
        mirror_state=dict(type='str', required=False, choices=[
            'present-in-device', 'absent-in-device']),
        target_cluster=dict(type='str', required=False),
        transfer_size=dict(type='int', required=False)
    )


def main():
    """Create VplexDevice object and perform action on it
        based on user inputs from playbook"""
    obj = VplexDevice()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
