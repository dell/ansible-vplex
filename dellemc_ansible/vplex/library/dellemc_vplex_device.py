""" Device module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
import urllib3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
         dellemc_ansible_vplex_utils as utils
from vplexapi.api import DevicesApi
from vplexapi.api import ExtentApi
from vplexapi.rest import ApiException
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_device
version_added: '2.7'
short_description:  Manage storage device on VPLEX Storage System
description:
- Provisioning the storage device on VPLEX Storage System includes
  Create a new Device,
  Delete an existing Device,
  Get information about existing Device,
  Rename existing Device,
  Add extent to the Device,
  Remove extent from the Device.

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
  '''
EXAMPLES = r'''

    - name: Create a new raid-1 device
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        geometry: "{{ geometry }}"
        device_name: "{{ device_name }}"
        extents: "{{ extents }}"
        extent_state: "present-in-device"
        state: "present"

    - name: Create a new raid-0 device
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        geometry: "{{ geometry }}"
        stripe_depth: "{{ stripe_depth }}"
        device_name: "{{ device_name }}"
        extents: "{{ extents }}"
        extent_state: "present-in-device"
        state: "present"

    - name: Get device from cluster
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        device_name: "{{ device_name }}"
        state: "present"

    - name: Delete device from cluster
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        device_name: "{{ device_name }}"
        state: "absent"

    - name: Rename a local device
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        device_name: "{{ device_name }}"
        new_device_name: "{{ new_device_name }}"
        state: "present"

    - name: Add extent to device
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        device_name: "{{ device_name }}"
        extents: "{{ extents }}"
        extent_state: "present-in-device"
        state: "present"

    - name: Remove extent from Device
      dellemc_vplex_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        device_name: "{{ device_name }}"
        extents: "{{ extents }}"
        extent_state: "absent-in-device"
        state: "present"

'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

device_details:
    description: Properties of the device
    returned: When device exist in VPLEX
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

LOG = utils.get_logger('dellemc_vplex_device', log_devel=logging.INFO)

HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexDevice():
    """Class with VPLEX Device operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_device_parameters())

        required_together = [['extents', 'extent_state']]

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

        # Create an instance to DeviceApi to communicate with
        # vplexapi

        self.device = DevicesApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for provisioning')

    def get_device(self, cluster_name, device_name):
        """
        Get the details of a device.
        """
        try:
            obj_device = self.device.get_device(cluster_name, device_name)
            LOG.info("Got device details %s from %s", device_name,
                     cluster_name)
            LOG.debug("Device Details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except ApiException as err:
            err_msg = ("Could not get device {0} of {1} due to"
                       " error: {2}".format(device_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def create_device(self, cluster_name, device_payload):
        """
        Create device on VPLEX
        """

        try:
            obj_device = self.device.create_device(
                cluster_name, device_payload)
            LOG.info("Created device in %s", cluster_name)
            LOG.debug("Device details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except ApiException as err:
            err_msg = ("Could not create device {0} in {1} due to"
                       " error: {2}".format(device_payload['name'],
                                            cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def delete_device(self, cluster_name, device_name):
        """
        Delete device on VPLEX
        """

        try:
            obj_device = self.device.delete_device(cluster_name, device_name)
            LOG.info("Deleted device %s from %s", device_name, cluster_name)
            LOG.debug("Device details:\n%s", obj_device)
            return True
        except ApiException as err:
            err_msg = ("Could not delete device {0} from {1} due to"
                       " error: {2}".format(device_name,
                                            cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def update_local_device(self, cluster_name,
                            device_name, device_patch_payload):
        """
        Update device attributes
        """

        try:
            LOG.info("Final payload: %s", device_patch_payload)
            obj_device = self.device.patch_local_device(
                cluster_name, device_name, device_patch_payload)
            LOG.info("Updated device %s in %s", device_name, cluster_name)
            LOG.debug("Device details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except ApiException as err:
            err_msg = ("Could not update the device {0} in {1} due to"
                       " error: {2}".format(device_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def is_extent_inuse(self, cluster_name, extent_name):
        """
        Check if the extent is used by any Device
        """

        try:
            extent_details = None
            use = None
            used_device_name = None
            obj_extent = ExtentApi(api_client=self.client)
            extent_details = obj_extent.get_extent(cluster_name, extent_name)
            if extent_details:
                LOG.debug("Extent details:\n%s", str(extent_details))
                if extent_details.use == "used":
                    used_device_name = extent_details.used_by[0].split('/')[-1]
            use = extent_details.use
            return (use, used_device_name)

        except ApiException as err:
            err_msg = ("Could not get extent details {0} of {1} due to"
                       " error: {2}".format(extent_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

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

        extents_uri = ["/vplex/v2/clusters/{}/extents/{}".format(
            cluster_name, extent) for extent in extents]
        LOG.info("extents_uri: %s", extents_uri)
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

    def check_task_validity(self, device_name):
        """
        Check if the device_name is valid string
        """
        char_len = "60"
        status, msg = utils.validate_name(device_name, char_len, 'device_name')
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

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

        changed = False
        result = dict(
            changed=False,
            device_details=None
        )
        device_details = None
        device_patch_payload = []

        self.check_task_validity(device_name)
        device_details = self.get_device(cluster_name, device_name)

        if (state == 'present' and not device_details):
            if (extents and extent_state == 'present-in-device'):
                if geometry is None:
                    geometry = 'raid-1'
                if stripe_depth:
                    if geometry in ('raid-1', 'raid-c'):
                        msg = "stripe_depth not required \
                        for '{0}'".format(geometry)
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
            else:
                err_msg = ("Could not get device {0} in {1}".format(
                    device_name, cluster_name))
                LOG.error("%s\n", err_msg)
                self.module.fail_json(msg=err_msg)

        elif (state == 'absent' and device_details):
            if "rebuilding" in device_details["health_indications"]:
                msg = ("Could not delete device {0} since device is"
                       " rebuilding".format(device_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            self.delete_device(cluster_name, device_name)
            device_details = None
            changed = True

        elif (state == 'present' and new_device_name and device_details):
            self.check_task_validity(new_device_name)
            if new_device_name != device_details["name"]:
                get_new_dev = self.get_device(cluster_name, new_device_name)
                if get_new_dev:
                    err_msg = ("New Device name {0} already exist"
                               " in {1}".format(new_device_name, cluster_name))
                    self.module.fail_json(msg=err_msg)
                operation = 'replace'
                path = '/name'
                value = new_device_name
                patch_payload = self.get_device_patch_payload(
                    operation, path, value)
                device_patch_payload.append(patch_payload)
                device_details = self.update_local_device(
                    cluster_name, device_name, device_patch_payload)
                changed = True

        elif (state == 'present' and extents and extent_state and
              device_details):
            if device_details["geometry"] == "raid-1":
                for extent in extents:
                    (extent_use, used_device_name) = self.is_extent_inuse(
                        cluster_name, extent)
                    if extent_use == 'used':
                        if used_device_name != device_name:
                            msg = "Extent used by another device'{0}'".format(
                                used_device_name)
                            LOG.error(msg)
                            self.module.fail_json(msg=msg)

                    if (extent_state == 'present-in-device' and
                            extent_use == 'claimed'):
                        operation = 'add'
                        path = '/legs'
                        value = "/vplex/v2/clusters/{}/extents/{}".format(
                            cluster_name, extent)
                        patch_payload = self.get_device_patch_payload(
                            operation, path, value)
                        device_patch_payload.append(patch_payload)

                    if (extent_state == 'absent-in-device' and
                            extent_use == 'used'):
                        if ("rebuilding" in
                                device_details["health_indications"]):
                            msg = ("Could not remove extent {0}"
                                   " since the device is in rebuild"
                                   " state".format(str(extents)))
                            LOG.error(msg)
                            self.module.fail_json(msg=msg)
                        operation = 'remove'
                        path = '/legs'
                        value = "/vplex/v2/clusters/{}/extents/{}".format(
                            cluster_name, extent)
                        patch_payload = self.get_device_patch_payload(
                            operation, path, value)
                        device_patch_payload.append(patch_payload)

                if len(device_patch_payload) > 0:
                    device_details = self.update_local_device(
                        cluster_name, device_name, device_patch_payload)
                    changed = True

            else:
                msg = "Add/Remove extent is supported only on raid-1 device"
                LOG.info(msg)

        result['changed'] = changed
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
        extents=dict(type='list', required=False),
        extent_state=dict(type='str', required=False, choices=[
            'present-in-device', 'absent-in-device']),
        new_device_name=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )


def main():
    """Create VplexDevice object and perform action on it
        based on user inputs from playbook"""
    obj = VplexDevice()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
