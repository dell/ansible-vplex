""" Virtual Volume module """

# !/usr/bin/python  # pylint: disable=C0302
# Copyright: (c) 2020, DellEMC

import logging
from datetime import datetime, timedelta
from collections import OrderedDict
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
    dellemc_ansible_vplex_utils as utils
from vplexapi.api import VirtualVolumeApi, ExportsApi, \
    DevicesApi, ExtentApi, MapsApi
from vplexapi.rest import ApiException
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type   # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_virtual_volume
version_added: '2.7'
short_description: Manage VPLEX virtual volume
description:
- Managing virtual volume on VPLEX System includes
  Get Virtual Volume,
  Create Virtual Volume,
  Update Virtual Volume,
  Delete Virtual Volume,
  Enable/Disable remote access,
  Add/Remove local mirror,
  Expand Virtual Volume

extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex

author: Amit Uniyal (amit_u@dellteam.com)
        vplex.ansible@dell.com

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

  new_virtual_volume_name:
    description:
    - Defines to rename virtual volume name
    type: str

  thin_enable:
    description:
    - Defines to have thin value
    default: true
    type: bool

  mirroring_device_name:
    description:
    - Defines to add/remove mirroring device to existing volume
    type: str

  mirroring_flag:
    description:
    - Defines to add/remove mirroring device
    type: bool

  additional_devices:
    description:
    - Defines to add/remove virtual volume to expand
    type: list

  remote_access:
    description:
    - Defines remote access to virtual volume
    type: str
    choices: ['enable', 'disable']

  state:
    description:
    - Defines whether the volume should exist or not
    required: True
    choices: ['absent', 'present']
'''

EXAMPLES = r'''
- name: Get virtual Volume by volume id
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_id: "{{ virtual_vol_id }}"
    state: "present"

- name: Get virtual Volume by volume name
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_vol_name}}"
    state: "present"

- name: Create Virtual volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    supporting_device_name: "{{ device_name }}"
    thin_enable: true
    state: "present"

- name: Rename Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_id: "{{ virtual_volume_id }}"
    new_virtual_volume_name: "{{ new_virtual_volume_name }}"
    state: "present"

- name: Delete Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    state: "absent"

- name: Enable remote access of Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    remote_access: "enable"
    state: "present"

- name: Disable Remote Access of Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    remote_access: "disable"
    state: "present"

- name: Expand virtual volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    additional_devices: "{{ additional_devices }}"
    state: "present"

- name: Add local mirror device to Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    mirroring_device_name: "{{ mirroring_device_name }}"
    mirroring_flag: true
    state: "present"

- name: Remove local mirror device from Virtual Volume
  dellemc_vplex_virtual_volume:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "{{ cluster_name }}"
    virtual_volume_name: "{{ virtual_volume_name }}"
    mirroring_device_name: "{{ mirroring_device_name }}"
    mirroring_flag: false
    state: "present"

'''

RETURN = r'''
output:
changed: state changed status
volume_details: virtual volume details

changed:
    description: Whether or not the virtual volume has changed
    required: always
    type: bool

volume_details:
    description: Details of the virtual volume
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
                Possible values:
                concatenation - The volume can be expanded using Concatenation
                    or RAID-C expansion.
                storage-volume - The volume can be expanded to the Expandable
                    capacity using storage volume expansion.
                not-supported - The volume does not support expansion.
                    This could be because the volume is being used in
                    RecoverPoint.
            type: str
        expansion_status:
            description: The expansion status of the volume. The volume can be:
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
            description: Values might be:
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
            descrition: added device list for mirroring
            type: list
'''


LOG = utils.get_logger('dellemc_vplex_virtual_volume', log_devel=logging.INFO)
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
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            mutually_exclusive=mutually_exclusive,
            supports_check_mode=False)
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

        self.virtual_client = VirtualVolumeApi(api_client=self.client)
        self.export_client = ExportsApi(api_client=self.client)
        self.device_client = DevicesApi(api_client=self.client)
        self.extent_client = ExtentApi(api_client=self.client)
        self.maps_client = MapsApi(api_client=self.client)
        self.cluster_name = self.module.params['cluster_name']
        self.vol_obj = None

        # Verify if required cluster is reachable
        (err_code, msg) = utils.verify_cluster_name(
            self.client, self.cluster_name)
        if err_code != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource %s" % self.cluster_name
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_volume(self, vol_name=None):
        """Get virtual volume object by volume name or id"""
        # As volume id is as same as volume name,
        # we can use any one to get volume object
        if vol_name is None:
            vol_name = self.vol_obj.name
        LOG.info('Trying to get virtual volume by name')
        LOG.info('Get virtual volume %s from %s',
                 vol_name, self.cluster_name)
        try:
            res = self.virtual_client.get_virtual_volume(
                cluster_name=self.cluster_name,
                name=vol_name)
            LOG.info('Found Volume details for %s', res.name)
            LOG.debug('Virtual volume details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not get the virtual volume {0} in {1} due to"
                       " error: {2}".format(
                           vol_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)

    def get_volume_by_id(self, vol_id):
        """Get virtual volume object by volume id"""
        LOG.info('Trying to get virtual volume by ID')
        LOG.info('Get virtual volume %s from %s',
                 vol_id, self.cluster_name)
        err_msg = ("Could not get the virtual volume {0} in {1}".format(
            vol_id, self.cluster_name))
        vols = self.get_volumes()
        data = [e for e in vols if e.system_id == vol_id]
        if len(data) > 0:
            LOG.info('Found Volume details for %s', data[0].name)
            LOG.debug('Virtual volume details: %s', data)
            return data[0]
        return str(err_msg)

    def get_volumes(self):
        """Get all virtual volumes"""
        LOG.info('Get all virtual volumes')
        try:
            res = self.virtual_client.get_virtual_volumes(
                cluster_name=self.cluster_name)
            LOG.debug('Virtual Volumes details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not get the virtual volumes in {0} due to"
                       " error: {1}".format(
                           self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def create_volume(self, payload):
        """Create virtual volume"""
        LOG.info('Creating virtual volume')
        LOG.debug('Details \n%s:\n\n', payload)
        try:
            res = self.virtual_client.create_virtual_volume(
                cluster_name=self.cluster_name,
                virtual_volume_payload=payload)
            LOG.info('Created volume %s', res.name)
            LOG.debug('New virtual volume details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not create virtual volume in {0} due to"
                       " error: {1}".format(
                           self.cluster_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def update_volume(self, volume_payload):
        """Update virtual volume"""
        LOG.info('Updating virtual volume %s', self.vol_obj.name)
        LOG.debug('Details \n%s:\n\n%s', self.vol_obj.name, volume_payload)
        try:
            res = self.virtual_client.patch_virtual_volume(
                cluster_name=self.cluster_name,
                name=self.vol_obj.name,
                virtual_volume_patch_payload=volume_payload)
            LOG.info('Updated %s', self.vol_obj.name)
            LOG.debug('Updated virtual volume details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not update virtual volume {0} in {1} due to"
                       " error: {2}".format(
                           self.vol_obj.name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def expand_volume(self, payload):
        """Expanding virtual volume"""
        LOG.info('Expanding virtual volume %s', self.vol_obj.name)
        LOG.debug('Details: \n%s', payload)
        try:
            res = self.virtual_client.expand_virtual_volume(
                cluster_name=self.cluster_name,
                name=self.vol_obj.name,
                virtual_volume_expand_payload=payload)
            LOG.info('Expanded %s', self.vol_obj.name)
            LOG.debug('Expanded virtual volume details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not expand virtual volume {0} in {1} due to"
                       " error: {2}".format(
                           self.vol_obj.name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def delete_volume(self, vol_name=None):
        """Delete virtual volume"""
        LOG.info('Deleting virtual volume')
        if not vol_name:
            vol_name = self.vol_obj.name
        try:
            self.virtual_client.delete_virtual_volume(
                cluster_name=self.cluster_name,
                name=vol_name)
            msg = 'Deleted volume '+vol_name
            LOG.info(msg)
            return True
        except ApiException as err:
            err_msg = ("Could not delete virtual volume {0} in {1} due to"
                       " error: {2}".format(
                           vol_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def get_device(self, dev_name):
        """Get Device"""
        LOG.info('Get device %s from VPLEX', dev_name)
        try:
            res = self.device_client.get_device(
                cluster_name=self.cluster_name,
                name=dev_name)
            LOG.info('Found %s', res.name)
            LOG.debug('Device details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not get device {0} in {1} due to"
                       " error: {2}".format(
                           dev_name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)

    def update_device(self, dev_name, payload):
        """Updating local device"""
        LOG.info('Trying to update device %s', dev_name)
        LOG.debug('Payload details \n\n%s\n', payload)
        try:
            res = self.device_client.patch_local_device(
                cluster_name=self.cluster_name,
                name=dev_name,
                local_device_patch_payload=payload)
            LOG.info('Updated device %s', dev_name)
            LOG.debug("Device details\n%s", res)
            return res, True
        except ApiException as err:
            err_msg = ("Could not update device {0} in virtual volume {1}"
                       " in {2} due to error: {3}".format(
                           dev_name, self.vol_obj.name, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg), False

    def get_map(self, uri):
        """Get object map from VPLEX"""
        obj = uri.split('/')[-1]
        LOG.info('Get map for %s', obj)
        try:
            res = self.maps_client.get_map(uri)
            LOG.info('Map Found')
            LOG.debug('Map details: %s', res)
            return res
        except ApiException as err:
            err_msg = ("Could not get map for {0} in {1} due to"
                       " error: {2}".format(
                           obj, self.cluster_name,
                           utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return str(err_msg)

    def perform_module_operation(self):  # pylint: disable=R0914, R0912, R0915
        """perform module operations"""
        def exit_module(details, change_flag):
            """module exit function"""
            details = utils.serialize_content(details)
            # add mirror and expand info in details
            if vol_type:
                if vol_type == 'mirrored':
                    details['mirrors'] = list(children.values())
                    details['additional_devs'] = []
                elif vol_type == 'expanded':
                    details['mirrors'] = []
                    details['additional_devs'] = list(children.values())
            elif details != {}:
                details['mirrors'] = []
                details['additional_devs'] = []
            result = {
                "changed": change_flag,
                "virtual_volume_details": details
            }
            LOG.debug('Result %s', result)
            LOG.info('Exiting module')
            self.module.exit_json(**result)

        def is_device_rebuilding(dev):
            """Verify if device is rebuilding or not"""
            LOG.info('Verify if device is rebuilding for %s', dev.name)
            LOG.info('Device current rebuilding status is %s',
                     dev.rebuild_status)
            if dev.rebuild_status in ['rebuilding', 'queued']:
                msg = 'Device {0} rebuilding is in progress in  '\
                    '{1}, Please try again later.'.format(
                        dev.name, self.cluster_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        def dev_checks(device_name, chk_vol=None, chk_top_level=None,
                       chk_rebuild=None, chk_size=None):
            """Validate device for different tasks"""
            dev = self.get_device(device_name)
            if isinstance(dev, str):
                self.module.fail_json(msg=dev)
            if chk_vol and dev.virtual_volume is not None:
                msg = 'Device {0} is already used in {1} virtual ' \
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
            if chk_size:
                _dev = self.get_device(vol_dev_name)
                msg = 'Verify mirror device size, if its greater or ' \
                    'less than supporting device size'
                LOG.info(msg)
                msg = 'Device sizes:'
                msg += '\n\tSupporting device size ' + str(_dev.capacity)
                msg += '\n\tMirror device size ' + str(dev.capacity)
                LOG.info(msg)
                if _dev.capacity > dev.capacity:
                    msg = 'Size of mirror device {0} is lesser than '\
                        'supporting device {1} in {2}'.format(
                            dev.name, _dev.name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
            return dev

        def get_volume_type(children):
            """Get volume type, if its mirrored or expanded"""
            def get_dates():
                dates = ["2000-01-01", "9999-01-01"]
                start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
                dates = OrderedDict(((start + timedelta(_)).strftime(r"%Y%b"),
                                     None)
                                    for _ in range((end - start).days)).keys()
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

        state = self.module.params['state']
        virt_vol_name = self.module.params['virtual_volume_name']
        virt_vol_id = self.module.params['virtual_volume_id']
        new_vol_name = self.module.params['new_virtual_volume_name']
        support_dev_name = self.module.params['supporting_device_name']
        mirror_dev_name = self.module.params['mirroring_device_name']
        mirroring_flag = self.module.params['mirroring_flag']
        additional_devs = self.module.params['additional_devices']
        remote_access = self.module.params['remote_access']
        thin_enabled = self.module.params['thin_enable']

        changed = False
        vol_type = None

        # Get volume details
        # all update operations can be performed by self.vol_obj
        if virt_vol_name:
            self.vol_obj = self.get_volume(virt_vol_name)
        elif virt_vol_id:
            self.vol_obj = self.get_volume_by_id(virt_vol_id)
        if isinstance(self.vol_obj, str):
            self.vol_obj = None

        # delete volume
        if state == 'absent':
            if self.vol_obj:
                LOG.info('Trying to delete virtual volume %s',
                         self.vol_obj.name)
                if self.vol_obj.service_status != 'unexported':
                    msg = 'Could not delete the virtual volume {0} from {1},' \
                        ' since virtual volume is exported to storage'\
                        ' view'.format(self.vol_obj.name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                changed = self.delete_volume()
            else:
                msg = 'Volume is not present to delete'
                LOG.info(msg)
            exit_module({}, changed)

        # create volume
        if not self.vol_obj and state == 'present' and support_dev_name and \
                thin_enabled in [True, False]:
            LOG.info('Trying to create virtual volume from %s',
                     support_dev_name)
            dev = dev_checks(support_dev_name)
            if dev.virtual_volume is None:
                if dev.top_level:
                    uri = '/vplex/v2/clusters/{0}/devices/{1}'.format(
                        self.cluster_name, support_dev_name)
                    payload = {
                        "thin": thin_enabled,
                        "device": uri
                    }
                    is_device_rebuilding(dev)
                    self.vol_obj = self.create_volume(payload)
                    changed = True
                else:
                    msg = 'Device {0} is already used in some other ' \
                        'virtual volume in {1}'.format(
                            support_dev_name, self.cluster_name)
                    LOG.info(msg)
                    self.module.fail_json(msg=msg)
            else:
                vol_name = dev.virtual_volume.split('/')[-1]
                msg = 'Device {0} is already attached to volume {1} ' \
                    'in {2}'.format(dev.name, vol_name,
                                    self.cluster_name)
                LOG.info(msg)
                self.vol_obj = self.get_volume(vol_name)

        # remaining all operations required state and vol_obj to be present,
        # we can skip further operation validation
        if not self.vol_obj:
            volume = virt_vol_name if virt_vol_name else virt_vol_id
            msg = 'Could not get \'{0}\' volume details in {1}.'.format(
                volume, self.cluster_name)
            logmsg = msg + '\nAll below operations required correct volume' \
                ' details:\n\tRename virtual volume' \
                '\n\tEnable/Disable remote access' \
                '\n\tExpand virtual volume' \
                '\n\tAdd mirror device'
            LOG.error(logmsg)
            self.module.fail_json(msg=msg)

        # As control with state as 'absent' won't go any futher
        # and only state as present will be available,
        # we may not need to check for state == 'persent' anymore
        vol_dev_name = self.vol_obj.supporting_device.split('/')[-1]

        # rename volume
        if new_vol_name:
            LOG.info('Trying to rename volume from %s to %s',
                     self.vol_obj.name, new_vol_name)

            def validate_name(name):
                """Name validation"""
                LOG.info('Valdating new name')
                status, msg = utils.validate_name(
                    name, 63, 'new_virtual_volume_name')
                if not status:
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                LOG.info(msg)

            if new_vol_name == self.vol_obj.name:
                msg = 'New name is same as old name, '\
                    'No need to rename volume.'
                LOG.info(msg)
            else:
                validate_name(new_vol_name)
                vol = self.get_volume(new_vol_name)
                if isinstance(vol, str):
                    payload = [{
                        "op": "replace",
                        "path": "/name",
                        "value": new_vol_name}]
                    self.vol_obj = self.update_volume(payload)
                    changed = True
                    LOG.info('Volume name updated to %s',
                             self.vol_obj.name)
                else:
                    msg = 'Virtual volume {0} with same name already exists' \
                        ' in {1}'.format(new_vol_name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

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
                if self.vol_obj.service_status != 'unexported':
                    msg = 'Virtual volume {0} in {1} is not ' \
                        '\'unexported\' to disable remote access'.format(
                            self.vol_obj.name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                payload = [{
                    "op": "replace",
                    "path": "/visibility",
                    "value": "local"
                }]
            if payload:
                dev, changed = self.update_device(vol_dev_name, payload)
                if not changed:
                    self.module.fail_json(msg=dev)
                self.vol_obj = self.get_volume()

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
        if len(additional_devs) > 0:
            LOG.info('Trying to expand volume')
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
                    LOG.debug('Payload: %s', payload)
                    self.vol_obj = self.expand_volume(payload)
                if capacity < self.vol_obj.capacity:
                    msg = 'Capacity increased from {0} to {1}.'.format(
                        capacity, self.vol_obj.capacity)
                    LOG.info(msg)
                    changed = True
            else:
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

        # mirroring volume
        elif mirror_dev_name:
            payload = None
            uri = '/vplex/v2/clusters/{0}/devices/{1}'.format(
                self.cluster_name, mirror_dev_name)

            if mirroring_flag:
                LOG.info('Trying to add mirror %s to virtual volume  '
                         '%s', mirror_dev_name, self.vol_obj.name)
                if vol_type == 'expanded':
                    msg = 'Could not add mirror to virtual volume {0} ' \
                        'in {1}, volume is expanded already, ' \
                        'can not be mirrored.'.format(
                            self.vol_obj.name, self.cluster_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                if mirror_dev_name in children:
                    LOG.info('%s is already attached to volume',
                             mirror_dev_name)
                    exit_module(self.vol_obj, changed)

                dev_checks(mirror_dev_name, chk_vol=True, chk_top_level=True,
                           chk_rebuild=True, chk_size=True)

                payload = [{
                    "op": "add",
                    "path": "/legs",
                    "value": uri
                }]
            elif mirroring_flag is False:
                LOG.info('Trying to remove mirror %s from virtual volume  '
                         '%s', mirror_dev_name, self.vol_obj.name)
                if mirror_dev_name not in children:
                    LOG.info('%s is not attached to volume',
                             mirror_dev_name)
                    exit_module(self.vol_obj, changed)
                dev_checks(mirror_dev_name, chk_rebuild=True)
                payload = [{
                    "op": "remove",
                    "path": "/legs",
                    "value": uri
                }]
            if payload:
                dev, changed = self.update_device(vol_dev_name, payload)
                if not changed:
                    self.module.fail_json(msg=dev)
                # get upgraded virtual volume object
                self.vol_obj = self.get_volume()
            if mirroring_flag is False:
                # Defect: VPLEX-29038
                # removed mirror device formed a new virtual volume
                # remove virtual volume created itself
                dev = self.get_device(mirror_dev_name)
                if dev.virtual_volume:
                    vol = dev.virtual_volume.split('/')[-1]
                    self.delete_volume(vol)
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
        thin_enable=dict(type='bool', required=False, default=True),

        mirroring_device_name=dict(type='str', required=False),
        mirroring_flag=dict(type='bool', required=False),

        additional_devices=dict(type='list', required=False, default=[]),

        remote_access=dict(type='str', required=False, choices=[
            'enable', 'disable']))


def main():
    """Create VPLEX VirtualVolumeModule object and perform action on it
        based on user input from playbook"""
    virt_vm = VirtualVolumeModule()
    virt_vm.perform_module_operation()


if __name__ == '__main__':
    main()
