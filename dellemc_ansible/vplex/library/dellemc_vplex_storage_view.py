""" Storageview module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
import json
import urllib3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
        dellemc_ansible_vplex_utils as utils
from vplexapi.api import ExportsApi
from vplexapi.rest import ApiException
from vplexapi.api import VirtualVolumeApi
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_storage_view
version_added: '2.7'
short_description: Manage storage views on VPLEX Storage System
description:
- Provisioning the storage views on VPLEX Storage System includes
  Create a storage view
  Delete an existing storage view,
  Get information about existing storage view,
  Rename existing storage view,
  Add port to the storage view,
  Remove port from the storage view,
  Add initiator to the storage view,
  Remove initiator from the storage view,
  Add virtual volume to the storage view,
  Remove virtual volume from the storage view.

extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex
author: Sherene Jean Prathiba (sherene_jean_pratibh@dellteam.com)
        vplex.ansible@dell.com

options:
  cluster_name:
    description:
    - Name of the cluster
    required: true
    type: str

  storage_view_name:
    description:
    - Name of the storage view
    required: true
    type: str

  ports:
    description:
    - Name of the ports
    type: list

  port_state:
    description:
    - To determine whether to add/remove port
    choices: ['absent-in-view', 'present-in-view']
    type: str

  initiators:
    description:
    - Name of the initiators
    type: list

  initiator_state:
    description:
    - To determine whether to add/remove initiator
    choices: ['absent-in-view', 'present-in-view']
    type: str

  virtual volumes:
    description:
    - Name of the virtual volumes
    type: list

  virtual_volume_state:
    description:
    - To determine whether to add/remove virtual volume
    choices: ['absent-in-view', 'present-in-view']
    type: str

  new_storage_view_name:
    description:
    - New name of the storage view
    type: str

  state:
    description:
    - Define whether the storage view should exist or not
    required: true
    choices: ['absent', 'present']
    type: str

Note:
- At least one port is required to create a storage view
'''

EXAMPLES = r'''
    - name: Create a storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        ports: "{{ports}}"
        state: "present"

    - name: Delete a storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        state: "absent"

    - name: Get a storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        state: "present"

    - name: Rename a storage_view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        storage_view_name: "{{ storage_view_name }}"
        new_storage_view_name: "{{ new_storage_view_name }}"
        state: "present"

    - name: Add ports to the storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        ports: "{{ ports_list }}"
        port_state: "present-in-view"
        state: "present"

    - name: Remove ports from storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        ports: "{{ ports_list }}"
        port_state: "absent-in-view"
        state: "present"

    - name: Add initiators to the storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        initiators: "{{ initiators_list }}"
        initiator_state: "present-in-view"
        state: "present"

    - name: Remove initiators from storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        initiators: "{{ initiators_list }}"
        initiator_state: "absent-in-view"
        state: "present"

    - name: Add virtualvolumes to the storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        virtual_volumes: "{{ virtualvolume_list }}"
        virtual_volume_state: "present-in-view"
        state: "present"

    - name: Remove virtualvolumes from storage view
      dellemc_vplex_storage_view:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        storage_view_name: "{{ storage_view_name }}"
        virtual_volumes: "{{ virtualvolume_list }}"
        virtual_volume_state: "absent-in-view"
        state: "present"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Storage View Details:
    description: Details of the storage view
    returned: For Create, Get, Rename, Delete and Update operations
    type: complex
    contains:
        operational_status:
            description: The functional status of the storage view
            type: str

        name:
            description: Name of the storage view
            type: str

        virtual_volumes:
            description: List of virtual volumes attached to the storage view
            type: list

        initiators:
            description: List of initiators attached to the storage view
            type: list

        ports:
            description: List of ports attached to the storage view
            type: list
'''

LOG = utils.get_logger('dellemc_vplex_storage_view', log_devel=logging.INFO)
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexStorageview():  # pylint:disable=R0902
    ''' class with storage view operations '''

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_storageview_parameters())
        self.resource_fail_msg = "Failed to collect resources"
        self.fail_msg = "Could not collect resources in {0}"

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
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

        # Create an instance to communicate with storageview VPLEX api
        self.storageview = ExportsApi(api_client=self.client)
        self.virtualvolume = VirtualVolumeApi(api_client=self.client)

        # Module parameters
        self.st_name = self.module.params['storage_view_name']
        self.new_st_name = self.module.params['new_storage_view_name']
        self.ports = self.module.params['ports']
        self.pt_state = self.module.params['port_state']
        self.initiators = self.module.params['initiators']
        self.ini_state = self.module.params['initiator_state']
        self.virvols = self.module.params['virtual_volumes']
        self.virvol_state = self.module.params['virtual_volume_state']

        # result is a dictionary that contains changed status and
        # storage view details
        self.result = {"changed": False, "storageview_details": {}}

    def create_storageview(self):
        """
        Create a storageview
        """
        try:
            # Construct the payload for creating a storage view
            pts = self.ports
            (ports,
             initiators,  # pylint:disable=W0612
             virvols) = self.get_obj_uri(ports=pts)  # pylint:disable=W0612
            storageview_payload = dict(
                name=self.st_name,
                ports=ports
            )

            storage_view_details = self.storageview.create_storage_view(
                self.cl_name, storageview_payload)
            LOG.info("Successfully created the storageview %s in %s",
                     self.st_name, self.cl_name)
            LOG.debug("Storageview details:\n%s", storage_view_details)
            return storage_view_details
        except ApiException as err:
            err_msg = ("Could not create storageview {0} in {1} due to error:"
                       " {3}".format(
                           self.st_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def get_storageview_details(self, name):
        """
        Get the storageview details
        """
        try:
            storageview_details = self.storageview.get_storage_view(
                self.cl_name, name)
            msg = ("Successfully obtained the storageview {0} details "
                   "from {1}".format(name, self.cl_name))
            LOG.info(msg)
            LOG.debug("Storageview details: %s", storageview_details)
            return storageview_details
        except ApiException as err:
            err_msg = ("Could not get storageview {0} in {1} due to error:"
                       " {2}".format(
                           name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            body = json.loads(err.body)
            if self.resource_fail_msg in body['message']:
                self.module.fail_json(msg=self.fail_msg.format(self.cl_name))
            return None

    def delete_storageview(self):
        """
        Delete a storageview
        """
        try:
            self.storageview.delete_storage_view(self.cl_name, self.st_name)
            LOG.info("Successfully deleted storageview %s from %s",
                     self.st_name, self.cl_name)
        except ApiException as err:
            err_msg = ("Could not delete storageview {0} from {1} due to "
                       "error: {3}".format(
                           self.st_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def update_storageview(self,  # pylint:disable=R0915, R0912, R0914
                           storageview_details, changed):
        """
        Update the storageview
        """
        storageview_details = utils.serialize_content(storageview_details)
        patch_payload = []

        # Check the validity and the presence of the new_storage_view_name
        if self.new_st_name == self.st_name:
            msg = "The storage_view_name and new_storage_view_name are same"
            LOG.info(msg)

        elif self.new_st_name:
            self.check_name(self.new_st_name)
            new_st_details = self.get_storageview_details(self.new_st_name)
            # Add the new name to the payload
            if not new_st_details:
                LOG.info("Renaming the storageview %s to %s in %s",
                         self.st_name, self.new_st_name, self.cl_name)
                patch_payload.append(self.payload(
                    'replace', '/name', self.new_st_name))
            else:
                msg = ("Could not rename storageview {0} in {1}."
                       " The new_storage_name {2}"
                       " is present already".format(
                           self.st_name, self.cl_name, self.new_st_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Construct the payload for ports
        if self.ports and self.pt_state == 'present-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(ports=self.ports)
            for port in ports:
                LOG.info("Adding port %s to storageview %s in %s",
                         port, self.st_name, self.cl_name)
                if port not in storageview_details['ports']:
                    patch_payload.append(self.payload(
                        'add', '/ports', port))
                else:
                    LOG.info("The port %s is already present in %s in %s",
                             port, self.st_name, self.cl_name)

        elif self.ports and self.pt_state == 'absent-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(ports=self.ports)
            for port in ports:
                LOG.info("Removing port %s from storageview %s in %s",
                         port, self.st_name, self.cl_name)
                if port in storageview_details['ports']:
                    patch_payload.append(self.payload(
                        'remove', '/ports', port))
                else:
                    LOG.info("The port %s is not present in %s in %s",
                             port, self.st_name, self.cl_name)

        # Construct the payload for initiators
        if self.initiators and self.ini_state == 'present-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(
                initiators=self.initiators)
            for initiator in initiators:
                LOG.info("Adding initiator %s to storageview %s in %s",
                         initiator, self.st_name, self.cl_name)
                if initiator not in storageview_details['initiators']:
                    patch_payload.append(self.payload(
                        'add', '/initiators', initiator))
                else:
                    LOG.info("The initiator %s is already present in %s in %s",
                             initiator, self.st_name, self.cl_name)

        elif self.initiators and self.ini_state == 'absent-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(
                initiators=self.initiators)
            for initiator in initiators:
                LOG.info("Removing initiator %s from storageview %s in %s",
                         initiator, self.st_name, self.cl_name)
                if initiator in storageview_details['initiators']:
                    patch_payload.append(self.payload(
                        'remove', '/initiators', initiator))
                else:
                    LOG.info("The initiator %s is not present in %s in %s",
                             initiator, self.st_name, self.cl_name)

        # Construct the payload for virtual volumes
        virtual_volumes = []
        for obj in storageview_details['virtual_volumes']:
            virtual_volumes.append(obj['uri'])

        # Get the list of virtual volumes from the storageview list
        if self.virvols and self.virvol_state == 'present-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(
                virtual_vols=self.virvols)
            for virtualvol in virvols:
                LOG.info("Adding virtual volume %s to storageview %s in %s",
                         virtualvol, self.st_name, self.cl_name)
                if virtualvol not in virtual_volumes:
                    # Check if the virtual volume is used by any storage view
                    status = self.is_virtual_vol_in_use(virtualvol)
                    if status:
                        msg = "In {0} you are adding a Virtual Volume {1} "
                        msg = msg + "which is already exported to another "
                        msg = msg + "Storage View. This may expose data "
                        msg = msg + "already in use to this Storage View {2}"
                        msg = msg.format(self.cl_name, virtualvol,
                                         self.st_name)
                        LOG.warning(msg)
                    patch_payload.append(self.payload(
                        'add', '/virtual_volumes', virtualvol))
                else:
                    LOG.info("The virtual volume %s is already present in %s"
                             " in %s", virtualvol, self.st_name, self.cl_name)

        elif self.virvols and self.virvol_state == 'absent-in-view':
            (ports, initiators, virvols) = self.get_obj_uri(
                virtual_vols=self.virvols)
            for virtualvol in virvols:
                LOG.info("Removing virtualvolume %s from storageview %s in %s",
                         virtualvol, self.st_name, self.cl_name)
                if virtualvol in virtual_volumes:
                    patch_payload.append(self.payload(
                        'remove', '/virtual_volumes', virtualvol))
                else:
                    LOG.info("The virtual volume %s is absent in %s in %s",
                             virtualvol, self.st_name, self.cl_name)

        if not patch_payload:
            return storageview_details, changed

        try:
            storageview_details = self.storageview.patch_storage_view(
                self.cl_name, self.st_name, patch_payload)
            LOG.info("Successfully updated the storageview %s in %s",
                     self.st_name, self.cl_name)
            LOG.debug("Storageview details: %s", storageview_details)
            return storageview_details, True
        except ApiException as err:
            err_msg = ("Could not update the storageview {0} in {1}"
                       " due to error: {2}".format(
                           self.st_name, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def check_port_validity(self):
        """
        Checks if the ports provided are present in the VPLEX
        """
        # Check if ports provided are already present in VPLEX
        if self.ports:
            LOG.info("Validating the ports")
            for port in self.ports:
                obj = None
                try:
                    obj = self.storageview.get_port(self.cl_name, port)
                except ApiException as err:
                    msg = ("Could not get port {0} details in {1} due to"
                           " error {2}".format(
                               port, self.cl_name, utils.error_msg(err)))
                    LOG.error("%s\n%s\n", msg, err)
                    self.module.fail_json(msg=msg)
                if obj is None:
                    msg = ("Could not get port {0} details in {1}"
                           .format(port, self.cl_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

    def check_storageobj_validity(self,  # pylint:disable=R0912, R0915
                                  stor_details):
        """
        Checks if the storage objects provided are present in the VPLEX
        """
        ports = []
        initiators = []

        if stor_details:
            stor_details = utils.serialize_content(stor_details)

        # Check if initiators provided are already present in VPLEX
        if self.initiators:
            LOG.info("Validating the initiators")
            for ini in self.initiators:
                obj = None
                try:
                    obj = self.storageview.get_initiator_port(
                        self.cl_name, ini)
                except ApiException as err:
                    msg = ("Could not get initiator {0} details in {1} due to"
                           " error {2}".format(
                               ini, self.cl_name, utils.error_msg(err)))
                    LOG.error("%s\n%s\n", msg, err)
                    self.module.fail_json(msg=msg)
                if obj:
                    obj = utils.serialize_content(obj)
                    # Add the initiator only if it is registered
                    if "type" not in obj.keys():
                        msg = ("The initiator {0} is unregistered in "
                               "{1}".format(ini, self.cl_name))
                        LOG.error(msg)
                        self.module.fail_json(msg=msg)
                else:
                    msg = ("Could not get initiator {0} details in {1}"
                           .format(ini, self.cl_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                initiators.append(ini)

        # Check if virtual volumes provided are already present in VPLEX
        if self.virvols:
            LOG.info("Validating the virtual volumes")
            for virvol in self.virvols:
                obj = None
                try:
                    obj = self.virtualvolume.get_virtual_volume(
                        self.cl_name, virvol)
                except ApiException as err:
                    msg = ("Could not get virtual volume {0} details in {1}"
                           " due to error {2}".format(
                               virvol, self.cl_name, utils.error_msg(err)))
                    LOG.error("%s\n%s\n", msg, err)
                    self.module.fail_json(msg=msg)
                if obj is None:
                    msg = ("Could not get virtual volume {0} details in {1}"
                           .format(virvol, self.cl_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

        # Get the complete URI of the storage objects in storageview_details
        (ports,
         initiators,  # pylint:disable=W0612
         virvol) = self.get_obj_uri(ports=ports, initiators=initiators)

        # Add the existing ports in the storageview to the list
        if stor_details:
            ports.extend(stor_details["ports"])

        # Add the existing initiators in the storageview to the list
        if stor_details:
            initiators.extend(stor_details["initiators"])

        # Check if the initiator-port combination is used in any of the
        # storage views already present in VPLEX
        storageview_list = self.storageview.get_storage_views(self.cl_name)
        if storageview_list is None:
            return
        storageview_list = utils.serialize_content(storageview_list)

        # Check if the initiator-port combination provided by the user is used
        # by other storage views in the cluster and fail if they are present
        ini = ""
        port = ""
        for obj in storageview_list:
            if obj['name'] == self.st_name:
                continue
            ini_flag = 0
            port_flag = 0
            for ini in obj['initiators']:
                if ini in initiators and self.ini_state != "absent-in-view":
                    ini_flag = 1
                    break
            for port in obj['ports']:
                if port in ports and self.pt_state != "absent-in-view":
                    port_flag = 1
                    break
            if port_flag == 1 and ini_flag == 1:
                msg = ("The view contains a target-port that is also in "
                       "another view, which contains the specified "
                       "initiator-port")
                LOG.error(msg)
                ini = ini.split("/")[-1]
                port = port.split("/")[-1]
                msg = ("Could not update storage view {0}. The "
                       "initiator {1} and port {2} combination "
                       "is already present in the storage view "
                       "{3}".format(self.st_name, ini, port, obj['name']))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

    def is_virtual_vol_in_use(self, virtualvol):
        """
        Checks if virtual volume is used by any other storage view
        """
        virtualvol_list = []
        try:
            storageview_list = self.storageview.get_storage_views(self.cl_name)
        except ApiException as err:
            msg = ("Could not get the list of storage views in {0} due to "
                   "error {1}".format(self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", msg, err)
            self.module.fail_json(msg=msg)

        if storageview_list is None:
            return False
        storageview_list = utils.serialize_content(storageview_list)

        # Collect the virtual volumes used by the storage views in the cluster
        for obj in storageview_list:
            for vol in obj['virtual_volumes']:
                virtualvol_list.append(vol['uri'])

        # Check if the given virtual volume is present in the list
        if virtualvol in virtualvol_list:
            return True
        return False

    def payload(self, operation, path, value):  # pylint:disable=R0201
        """
        Forms the patch payload for update operation
        """
        patch_payload = dict(
            op=operation,
            path=path,
            value=value
        )
        return patch_payload

    def get_obj_uri(self, ports=None, initiators=None, virtual_vols=None):
        """
        Forms the complete URI of the object given
        """
        ports_uri = []
        initiators_uri = []
        virtualvolume_uri = []

        if ports:
            ports_uri = ["/vplex/v2/clusters/{}/exports/ports/{}".format(
                self.cl_name, port) for port in ports]
        if initiators:
            uri = "/vplex/v2/clusters/{}/exports/initiator_ports/{}"
            initiators_uri = [uri.format(
                self.cl_name, initiator) for initiator in initiators]
        if virtual_vols:
            uri = "/vplex/v2/clusters/{}/virtual_volumes/{}"
            virtualvolume_uri = [uri.format(
                self.cl_name, vir_volume) for vir_volume in self.virvols]
        return (ports_uri, initiators_uri, virtualvolume_uri)

    def check_flag(self):
        """
        Checks whether an update operation is required
        """
        flag = 0
        if self.new_st_name:
            flag = 1
        elif self.ports and self.pt_state is not None:
            flag = 1
        elif self.initiators and self.ini_state is not None:
            flag = 1
        elif self.virvols and self.virvol_state is not None:
            flag = 1
        return flag

    def check_name(self, name):
        """
        Validates the storageview name
        """
        status, msg = utils.validate_name(name, "36", "storageview name")
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def perform_module_operation(self):   # pylint: disable=R0915,R0914,R0912
        """
        Performs different actions on storageview based on user parameters
        given in playbook
        """
        state = self.module.params['state']
        storageview_details = None
        changed = False

        # Check the validity and the presence of the storage_view_name
        if self.st_name:
            storageview_details = self.get_storageview_details(self.st_name)

        # Delete a storage view if state is 'absent'
        if state == 'absent' and self.st_name:
            if storageview_details:
                self.delete_storageview()
                changed = True
            else:
                LOG.info("The storageview %s is absent in %s",
                         self.st_name, self.cl_name)

            self.result["changed"] = changed
            self.module.exit_json(**self.result)

        # Checks if the ports provided are valid
        self.check_port_validity()

        # Flag is set to '1' when there is a patch operation required
        flag = self.check_flag()

        if state == 'present' and not storageview_details:
            if self.ports:
                if self.pt_state == 'absent-in-view':
                    msg = "Could not remove ports {0} from {1} in {2}"
                    msg = msg.format(self.ports, self.st_name, self.cl_name)
                    LOG.error(msg)
                    LOG.error("Storage view %s not present", self.st_name)
                    self.module.fail_json(msg=msg)
                else:
                    self.check_name(self.st_name)
                    # Create a storage view
                    storageview_details = self.create_storageview()
                    changed = True
            # If the give storageview_name is not present and ports is empty
            elif self.ports is None:
                msg = "Storage view {0} not present in {1}"
                msg = msg.format(self.st_name, self.cl_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Fail if the already existing storage view does not contain
        # the ports given for create operation
        elif (state == 'present' and storageview_details and
              self.pt_state is None):
            storageview_details = utils.serialize_content(storageview_details)
            if self.ports:
                ports = self.ports
                (ports,
                 initiators,  # pylint:disable=W0612
                 vvols) = self.get_obj_uri(ports=ports)  # pylint:disable=W0612
                if set(ports) != set(storageview_details['ports']):
                    msg = ("Could not create the storage view {0} in {1}. "
                           "The storageview is already present with different"
                           " ports".format(self.st_name, self.cl_name))
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

        # Checks if the storage object provided are valid
        self.check_storageobj_validity(storageview_details)

        # Update a storage view
        if state == 'present' and storageview_details and flag:
            (storageview_details, changed) = self.update_storageview(
                storageview_details, changed)
        # Cannot update a storage view if it is not present
        elif state == 'present' and not storageview_details and flag:
            msg = ("Could not update storage view {0} in {1}."
                   "Storage view is absent".format(self.st_name, self.cl_name))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        self.result['changed'] = changed
        if storageview_details:
            storageview_details = utils.serialize_content(storageview_details)
        self.result["storageview_details"] = storageview_details
        self.module.exit_json(**self.result)


def get_vplex_storageview_parameters():
    """
    This method provide the parameters required for the ansible
    storage view module on VPLEX
    """
    return dict(
        cluster_name=dict(type='str', required=True),
        storage_view_name=dict(type='str', required=True),
        new_storage_view_name=dict(type='str', required=False),
        ports=dict(type='list', required=False),
        port_state=dict(
            type='str',
            required=False,
            choices=['present-in-view', 'absent-in-view']),
        initiators=dict(type='list', required=False),
        initiator_state=dict(
            type='str',
            required=False,
            choices=['present-in-view', 'absent-in-view']),
        virtual_volumes=dict(type='list', required=False),
        virtual_volume_state=dict(
            type='str',
            required=False,
            choices=['present-in-view', 'absent-in-view']),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )


def main():
    """
    Create VplexStorageview object and perform action on it
    based on user input from playbook
    """
    obj = VplexStorageview()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
