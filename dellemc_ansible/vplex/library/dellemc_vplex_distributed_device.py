""" Distributed Device module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
    dellemc_ansible_vplex_utils as utils

__metaclass__ = type  # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_distributed_device
version_added: '2.7'
short_description:  Manage storage distributed device on VPLEX Storage System
description:
- Provisioning the storage distributed device on VPLEX Storage System includes
  Create a new Distributed device,
  Delete an existing Distributed device,
  Get information about existing Distributed device,
  Rename existing Distributed device,
  Update Rule set name of the Distributed device.

extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex

author:
- Hema Sasank Marepalli (@hemasasank-dell) <vplex.ansible@dell.com>

options:
  distributed_device_name:
    description:
    - The name of the distributed device
    required: true
    type: str

  source_device:
    description:
    - The name of the source device for creating distributed device
    type: str

  source_cluster:
    description:
    - Name of the VPLEX cluster
    type: str

  target_device:
    description:
    - The name of the target device for creating distributed device
    type: str

  target_cluster:
    description:
    - Name of the VPLEX cluster
    type: str

  rule_set:
    description:
    - The name of the Rule Set applied to the distributed device
    choices: ['cluster-1-detaches', 'cluster-2-detaches']
    type: str

  sync:
    description:
    - To synchronize data from the source device to the target device
    type: bool

  new_distributed_device_name:
    description:
    - New name of the distributed device
    type: str

  state:
    description:
    - Define whether the device should exist or not
    required: true
    choices: ['absent', 'present']
    type: str

NOTE:
- distributed_device_name is optional for creating distributed device
- rule_set and sync are optional parameters for creating distributed device
'''

EXAMPLES = r'''
    - name: Create a distributed device
      dellemc_vplex_distributed_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd"
        target_cluster: "cluster-2"
        target_device: "ansible_target_dev_1"
        source_cluster: "cluster-1"
        source_device: "ansible_source_dev_1"
        rule_set: "cluster-1-detaches"
        sync: true
        state: "present"

    - name: Get details of distributed device
      dellemc_vplex_distributed_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd"
        state: "present"

    - name: Update rule set name of the distributed device
      dellemc_vplex_distributed_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd"
        rule_set: "cluster-2-detaches"
        state: "present"

    - name: Rename distributed device
      dellemc_vplex_distributed_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd"
        new_distributed_device_name: "new_ansible_test_dd"
        state: "present"

    - name: Delete a distributed device
      dellemc_vplex_distributed_device:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser}}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        distributed_device_name: "ansible_test_dd"
        state: "absent"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

dist_device_details:
    description: Details of the Distributed device
    returned: For Create, Get and Update operations
    type: complex
    contains:
        capacity:
            description: The size of the distributed device
            type: int
        geometry:
            description: RAID level applied to the distributed device
            type: str
        health_indications:
            description:
                - If health-state is not ok return additional information
            type: list
        health_state:
            description: The health state of the distributed device
            type: str
        operational_status:
            description: The functional status of the distributed device
            type: str
        rule_set_name:
            description:
                - The name of the Rule Set applied to the distributed device
            type: str
        rebuild_allowed:
            description:
                - Whether or not the distributed device is allowed to rebuild
            type: bool
        rebuild_eta:
            description:
                - If a rebuild is in progress, the estimated time
                  remaining for the current rebuild to complete
            type: str
        rebuild_progress:
            description:
                - The percentage of the distributed device that has been
                  rebuild
            type: str
        rebuild_status:
            description: The rebuild status of the distributed device
            type: str
        rebuild_type:
            description: The rebuild type
            type: str
        service_status:
            description: The distributed device running status
            type: str
        storage_array_family:
            description: The storage array family name
            type: str
        thin_capable:
            description: Thin provisioning support
            type: bool
        virtual_volume:
            description: Name of the distributed virtual volume
            type: str
        name:
            description: The name of the distributed device
            type: str
'''

LOG = utils.get_logger('dellemc_vplex_distributed_device')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexDistributedDevice():
    """Class with distributed device operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_distributed_device_parameters())
        # initialize the ansible module
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
        # Create the configuration instance to communicate with vplexapi
        self.client = utils.config_vplexapi(self.module.params)
        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client
            LOG.error(msg)
            LOG.error(err_code)
            self.module.fail_json(msg=msg)

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        api_obj = utils.VplexapiModules()
        # Create an instance to required API's to communicate with vplexapi
        self.distdevice = api_obj.DistributedStorageApi(
            api_client=self.client)
        self.device = api_obj.DevicesApi(api_client=self.client)
        self.cluster = api_obj.ClustersApi(api_client=self.client)
        self.maps_client = api_obj.MapsApi(api_client=self.client)

    def get_distributed_device(self, distributed_device_name):
        """ get distributed device """
        try:
            msg = "Trying to obtain the distributed device {0}".format(
                distributed_device_name)
            LOG.info(msg)
            dist_device_obj = self.distdevice.get_distributed_device(
                distributed_device_name)
            LOG.info(
                "Obtained the distributed device details of %s ",
                distributed_device_name)
            LOG.debug("Distributed device Details:\n%s", dist_device_obj)
            return dist_device_obj, None
        except utils.ApiException as ex:
            err_msg = 'Could not get the distributed device {0}'.format(
                distributed_device_name)
            err_msg += ' due to error: {0}'.format(utils.error_msg(ex))
            LOG.error("%s\n%s\n", err_msg, ex)
            return None, err_msg

    def create_distributed_device(self, dist_device_create_payload,
                                  distributed_device_name):
        """creating distributed device """
        try:
            msg = "Trying to create the distributed device {0}".format(
                distributed_device_name)
            LOG.info(msg)
            dist_device_obj = self.distdevice.create_distributed_device(
                dist_device_create_payload)
            LOG.info("Successfully created the distributed device")
            LOG.debug("Device details:\n%s", dist_device_obj)
            return dist_device_obj
        except utils.ApiException as ex:
            err_msg = 'Could not create the distributed device {0}'.format(
                dist_device_create_payload['name'])
            err_msg += ' due to error: {0}'.format(utils.error_msg(ex))
            LOG.error("%s\n%s\n", err_msg, ex)
            self.module.fail_json(msg=err_msg)

    def update_distributed_device(
            self,
            distributed_device_name,
            dist_device_patch_payload):
        """update disributed device """
        try:
            msg = "Trying to update the distributed device {0}".format(
                distributed_device_name)
            LOG.info(msg)
            dist_device_obj = self.distdevice.patch_distributed_device(
                distributed_device_name, dist_device_patch_payload)
            LOG.info("Successfully updated the Distributed device")
            LOG.debug("Device details:\n%s", dist_device_obj)
            return dist_device_obj
        except utils.ApiException as ex:
            err_msg = 'Could not update the distributed device {0}'.format(
                distributed_device_name)
            err_msg += ' due to error: {0}'.format(utils.error_msg(ex))
            LOG.error("%s\n%s\n", err_msg, ex)
            self.module.fail_json(msg=err_msg)

    def delete_distributed_device(self, distributed_device_name):
        """delete distributed device """
        try:
            msg = "Trying to delete the distributed device {0}".format(
                distributed_device_name)
            LOG.info(msg)
            dist_device_obj = self.distdevice.delete_distributed_device(
                distributed_device_name)
            LOG.info("Successfully deleted the distributed device")
            return dist_device_obj
        except utils.ApiException as ex:
            err_msg = 'Could not delete the distributed device {0}'.format(
                distributed_device_name)
            err_msg += ' due to error: {0}'.format(utils.error_msg(ex))
            LOG.error("%s\n%s\n", err_msg, ex)
            self.module.fail_json(msg=err_msg)

    def is_device_present(self, cluster_name, device_name):
        """ checking if device present or not """
        try:
            LOG.info("Trying to check whether given device is present")
            obj_device = self.device.get_device(cluster_name, device_name)
            LOG.info("Found the device %s in %s", device_name, cluster_name)
            return obj_device
        except utils.ApiException as ex:
            err_msg = 'Could not find the device {0}'.format(device_name)
            err_msg += ' in {0} due to error: {1}'.format(
                cluster_name, utils.error_msg(ex))
            LOG.error("%s\n%s\n", err_msg, ex)
            return None

    def check_for_dcg(self, dist_dev_details, distributed_device_name,
                      flag):
        """ Checks if distributed device is a part of distributed cg """
        if dist_dev_details.virtual_volume is not None:
            dist_cgs = self.distdevice.get_distributed_consistency_groups()
            for dist_cg in dist_cgs:
                dist_cg_det = \
                    self.distdevice.get_distributed_consistency_group(
                        dist_cg.name)
                if dist_dev_details.virtual_volume in dist_cg.virtual_volumes:
                    msg = "Could not {0} the distributed device {1} "\
                        "because its virtual volume {2} is in consistency "\
                        "group {3}".format(
                            flag,
                            distributed_device_name,
                            dist_dev_details.virtual_volume.split('/')[-1],
                            dist_cg_det.name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)

    def check_for_dvv(self, dist_dev_details, distributed_device_name):
        """ Checks if distributed device is a part of distributed \
            virtual volume """
        if dist_dev_details.virtual_volume is not None:
            dvv = dist_dev_details.virtual_volume.split('/')[-1]
            LOG.info("%s has a virtual volume %s", distributed_device_name,
                     dvv)
            dvv_details = self.distdevice.get_distributed_virtual_volume(
                dvv)
            LOG.info(dvv_details.service_status)
            if dvv_details.service_status != 'unexported':
                msg = "Could not delete the distributed device {0} because "\
                    "it has an exported virtual volume {1}".format(
                        distributed_device_name, dvv)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

    def check_rebuilding_status(self, dist_dev_details):
        """ Checks the rebuilding status of distributed device """
        LOG.info('Verifying rebuilding status')
        LOG.info(dist_dev_details)
        LOG.info('Rebuilding status is %s',
                 dist_dev_details.rebuild_status)
        if dist_dev_details.rebuild_status != 'done':
            msg = "Could not delete the distributed device {0} because "\
                "it is in rebuilding state".format(dist_dev_details.name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def name_check_in_clusters(self, dev_name):
        """ Checks if distributed device name is present in \
            any of the clusters """
        clus_det = self.cluster.get_clusters()
        for clus in clus_det:
            devices = self.is_device_present(clus.name, dev_name)
            if devices:
                return True, clus.name
        return False, None

    def check_cluster_validity(self, cluster_name):
        """ Checks if given cluster is valid or not """
        (err_code, msg) = utils.verify_cluster_name(
            self.client, cluster_name)
        if err_code != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource %s" % cluster_name
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def check_dist_device_name(self, distributed_device_name, field):
        """ Checks whether given distributed device name is valid or not """
        flag, msg = utils.validate_name(distributed_device_name, 63, field)
        if not flag:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def create_dd_checks(self, distributed_device_name, source_device,
                         source_cluster, target_device, target_cluster):
        # pylint: disable=R0913, R0915
        """ Checks all conditions to be met before creating \
            distributed device """
        LOG.info("Verifying checks for creating distributed device")
        # check for the given name in all clusters
        flag, clus = self.name_check_in_clusters(distributed_device_name)
        if flag and clus is not None:
            msg = "Could not create the distributed device {0} because "\
                "a device already exists with same name in {1}". format(
                    distributed_device_name, clus)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check validity of cluster names
        self.check_cluster_validity(source_cluster)
        self.check_cluster_validity(target_cluster)
        # check if both clusters are same or not
        if source_cluster == target_cluster:
            msg = "Could not create the distributed device {0} because "\
                "source cluster and target cluster should not be "\
                "same".format(distributed_device_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check name validity of given source_device and target_device
        self.check_dist_device_name(source_device, "source_device")
        self.check_dist_device_name(target_device, "target_device")
        source_dev_det = self.is_device_present(source_cluster, source_device)
        target_dev_det = self.is_device_present(target_cluster, target_device)
        # checking for source_device presence
        if source_dev_det is None:
            msg = "Could not create the distributed device {0} because "\
                "the source device {1} is not found in {2}".format(
                    distributed_device_name, source_device, source_cluster)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # checking for target_device presence
        if target_dev_det is None:
            msg = "Could not create the distributed device {0} because "\
                "the target device {1} is not found in {2}".format(
                    distributed_device_name, target_device, target_cluster)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if source_device and target_device are same
        if source_device == target_device:
            msg = "Could not create the distributed device {0} because "\
                "source device and target device should not be "\
                "same".format(distributed_device_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if source_device is top_level device
        if not source_dev_det.top_level:
            msg = "Could not create the distributed device {0} because "\
                "source device {1} is not top level "\
                "device".format(distributed_device_name, source_device)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if target_device is top_level device
        if not target_dev_det.top_level:
            msg = "Could not create the distributed device {0} because "\
                "target device {1} is not top level "\
                "device".format(distributed_device_name, target_device)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if capacity of target is greater or equal to source
        if source_dev_det.capacity > target_dev_det.capacity:
            msg = "Could not create the distributed device {0} because "\
                "source device capacity is greater than target "\
                "device capacity".format(distributed_device_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if source_device has any virtual volume on it
        if source_dev_det.virtual_volume is not None:
            vv_name = source_dev_det.virtual_volume.split('/')[-1]
            msg = "Could not create the distributed device {0} because "\
                "source device {1} has a virtual volume {2} "\
                "in {3}".format(distributed_device_name, source_device,
                                vv_name, source_cluster)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        # check if source_device has any virtual volume on it
        if target_dev_det.virtual_volume is not None:
            vv_name = target_dev_det.virtual_volume.split('/')[-1]
            msg = "Could not create the distributed device {0} because "\
                "target device {1} has a virtual volume {2} "\
                "in {3}".format(distributed_device_name, target_device,
                                vv_name, target_cluster)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    @classmethod
    def form_create_payload(cls, distributed_device_name, source_device,
                            source_cluster, target_device, target_cluster,
                            rule_set, sync):
        # pylint: disable=R0913
        """ Returns payload for creating distributed device """
        payload = {}
        if rule_set is None and sync is None:
            payload['name'] = distributed_device_name
            payload['primary_leg'] = '/vplex/v2/clusters/' + \
                source_cluster + '/devices/' + source_device
            payload['secondary_leg'] = '/vplex/v2/clusters/' + \
                target_cluster + '/devices/' + target_device
        elif rule_set is None and sync is not None:
            payload['name'] = distributed_device_name
            payload['primary_leg'] = '/vplex/v2/clusters/' + \
                source_cluster + '/devices/' + source_device
            payload['secondary_leg'] = '/vplex/v2/clusters/' + \
                target_cluster + '/devices/' + target_device
            payload['sync'] = sync
        elif rule_set is not None and sync is None:
            payload['name'] = distributed_device_name
            payload['primary_leg'] = '/vplex/v2/clusters/' + \
                source_cluster + '/devices/' + source_device
            payload['secondary_leg'] = '/vplex/v2/clusters/' + \
                target_cluster + '/devices/' + target_device
            payload['rule_set'] = \
                '/vplex/v2/distributed_storage/rule_sets/' + rule_set
        else:
            payload['name'] = distributed_device_name
            payload['primary_leg'] = '/vplex/v2/clusters/' + \
                source_cluster + '/devices/' + source_device
            payload['secondary_leg'] = '/vplex/v2/clusters/' + \
                target_cluster + '/devices/' + target_device
            payload['rule_set'] = \
                '/vplex/v2/distributed_storage/rule_sets/' + rule_set
            payload['sync'] = sync
        LOG.info(payload)
        return payload

    def check_dev_in_dd(self, distributed_device_name, target_device):
        """ Check for target device in distributed device """
        LOG.info("Checking if given device is a part of distributed device")
        dd_uri = '/vplex/v2/distributed_storage/distributed_devices/'\
            + distributed_device_name
        children = self.maps_client.get_map(dd_uri).children
        LOG.info(children)
        childs = []
        for child in children:
            childs.append(child.split('/')[-1])
        if target_device not in childs:
            msg = "Could not create the distributed device {0} because "\
                "a distributed device already exists with different "\
                "source target combination".format(distributed_device_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def check_rule_set_validity(self):
        """ Check for validity of rule_set """
        rule_sets = self.distdevice.get_rule_sets()
        LOG.info(rule_sets)
        rules = [rule.name for rule in rule_sets]
        return rules

    def perform_module_operation(self):
        # pylint: disable=R0912, R0914, R0915
        """
        Perform different actions on the extent based on user parameters\
        specified in the playbook
        """
        state = self.module.params['state']
        distributed_device_name = self.module.params[
            'distributed_device_name']
        new_distributed_device_name = self.module.params[
            'new_distributed_device_name']
        source_cluster = self.module.params['source_cluster']
        source_device = self.module.params['source_device']
        target_cluster = self.module.params['target_cluster']
        target_device = self.module.params['target_device']
        rule_set = self.module.params['rule_set']
        sync = self.module.params['sync']
        dist_device_details = None
        dist_device_patch_payload = []
        # chack name validity
        dist_dev_details = None
        self.check_dist_device_name(distributed_device_name,
                                    "distributed_device_name")
        dist_dev_details, msg = self.get_distributed_device(
            distributed_device_name)
        changed = False
        result = dict(
            changed=False,
            dist_device_details=None
        )
        # check status of cluster to check WAN-COM connection
        de_clus = utils.check_status_of_cluster(self.client)
        if de_clus:
            if state == 'absent' and not dist_dev_details:
                self.module.exit_json(**result)
            if state == 'absent' and dist_dev_details:
                msg = "Could not delete the distributed device {0} because "\
                    "{1} is in degraded state".format(distributed_device_name,
                                                      de_clus)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            if state == 'present' and dist_dev_details:
                if (source_device and target_device) or rule_set or \
                        new_distributed_device_name:
                    msg = "Could not perform the operation because {0} "\
                        "is in degraded state".format(de_clus)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                dist_device_details = utils.serialize_content(
                    dist_dev_details)
                result['dist_device_details'] = dist_device_details
                self.module.exit_json(**result)
            if state == 'present' and not dist_dev_details:
                if distributed_device_name is None:
                    msg = "Could not perform the operation because {0} "\
                        "is in degraded state".format(de_clus)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                self.module.fail_json(msg=msg)
        # delete distributed device
        if state == 'absent' and dist_dev_details:
            # check if distributed device attached to distributed cg
            self.check_for_dcg(dist_dev_details, distributed_device_name,
                               "delete")
            # check if distributed device attached to distributed vv
            self.check_for_dvv(dist_dev_details, distributed_device_name)
            # check for rebuilding state
            self.check_rebuilding_status(dist_dev_details)
            self.delete_distributed_device(distributed_device_name)
            dist_device_details = None
            changed = True
        # Get Distributed device details
        if (state == 'present' and dist_dev_details):
            if source_device is not None:
                self.check_dev_in_dd(distributed_device_name, source_device)
            if target_device is not None:
                self.check_dev_in_dd(distributed_device_name, target_device)
                LOG.info("Distributed device %s is already created "
                         "with same combination of source device and "
                         "target device", distributed_device_name)
            dist_device_details = utils.serialize_content(dist_dev_details)
        # Create distributed device
        if state == 'present' and not dist_dev_details:
            if source_cluster is not None and source_device is not None and \
                    target_cluster is not None and target_device is not None:
                if new_distributed_device_name:
                    msg = "Could not perform create and rename in a "\
                        "single task. Please specify each operation in "\
                        "individual task."
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                self.create_dd_checks(
                    distributed_device_name,
                    source_device,
                    source_cluster,
                    target_device,
                    target_cluster)
                # check validity of rule_set
                rule_sets = self.check_rule_set_validity()
                if rule_set is not None and rule_set not in rule_sets:
                    msg = "Could not create the distributed device {0} "\
                        "because rule_set should be one of {1}".format(
                            distributed_device_name, rule_sets)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                # form create Payload
                payload = self.form_create_payload(
                    distributed_device_name,
                    source_device,
                    source_cluster,
                    target_device,
                    target_cluster,
                    rule_set,
                    sync)
                dist_dev_details = self.create_distributed_device(
                    payload, distributed_device_name)
                dist_device_details = utils.serialize_content(
                    dist_dev_details)
                changed = True
            else:
                LOG.info(dist_dev_details)
                self.module.fail_json(msg=msg)
        # update rule_set_name
        if state == 'present' and rule_set is not None and dist_dev_details:
            # checking if it is a part of distributed cg
            self.check_for_dcg(dist_dev_details, distributed_device_name,
                               "update")
            # checking validity of rule_set
            rule_sets = self.check_rule_set_validity()
            LOG.info(rule_sets)
            if rule_set not in rule_sets:
                msg = "Could not update the distributed device {0} because "\
                    "rule_set should be one of {1}".format(
                        distributed_device_name, rule_sets)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            # idempotency
            if dist_dev_details.rule_set_name == rule_set:
                LOG.info("Provided rule_set is same compared to the "
                         "device rule_set. No need to update")
            else:
                dist_device_patch_payload.append(
                    {'op': 'replace',
                     'path': '/rule_set_name',
                     'value': rule_set})
                LOG.info("Updating Rule set name of distributed device %s",
                         distributed_device_name)
        # rename distributed device
        if state == 'present' and new_distributed_device_name is not None:
            # check for validation of new name
            self.check_dist_device_name(new_distributed_device_name,
                                        "new_distributed_device_name")
            # check for the new name existance in all clusters
            flag, clus = self.name_check_in_clusters(
                new_distributed_device_name)
            if flag and clus is not None:
                msg = "Could not rename the distributed device {0} "\
                    "because {1} already exists in {2}". format(
                        distributed_device_name, new_distributed_device_name,
                        clus)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            # check if new name is same as old name
            if dist_dev_details.name == new_distributed_device_name:
                LOG.info("New distributed device name and existing "
                         "distributed device name are same")
            # check for the new name in distributed devices
            else:
                dd_det, msg = self.get_distributed_device(
                    new_distributed_device_name)
                if dd_det:
                    msg = "Could not rename the disributed device {0} "\
                        "because new distributed device name {1} "\
                        "already exists".format(distributed_device_name,
                                                new_distributed_device_name)
                    LOG.error(msg)
                    self.module.fail_json(msg=msg)
                # form payload
                dist_device_patch_payload.append(
                    {'op': 'replace',
                     'path': '/name',
                     'value': new_distributed_device_name})
                LOG.info(
                    "Renaming distributed device %s to %s ",
                    distributed_device_name, new_distributed_device_name)
        if len(dist_device_patch_payload) > 0:
            LOG.info(dist_device_patch_payload)
            update_dist_obj = self.update_distributed_device(
                distributed_device_name, dist_device_patch_payload)
            dist_device_details = utils.serialize_content(update_dist_obj)
            changed = True
        if dist_device_details:
            dd_uri = '/vplex/v2/distributed_storage/distributed_devices/'\
                + dist_device_details['name']
            children = self.maps_client.get_map(dd_uri).children
            LOG.info(children)
            dist_device_details['devices'] = children
        result['changed'] = changed
        result['dist_device_details'] = dist_device_details
        self.module.exit_json(**result)


def get_distributed_device_parameters():  # pylint:disable=C0103
    """This method provides parameters required for this module on Vplex"""
    return dict(
        state=dict(required=True, type='str', choices=['present', 'absent']),
        distributed_device_name=dict(required=True, type='str'),
        new_distributed_device_name=dict(required=False, type='str'),
        source_cluster=dict(required=False, type='str'),
        source_device=dict(required=False, type='str'),
        target_cluster=dict(required=False, type='str'),
        target_device=dict(required=False, type='str'),
        rule_set=dict(required=False, type='str'),
        sync=dict(required=False, type='bool'),
    )


def main():
    """ Create distributed devices object and perform action on it
        based on user input from playbook"""
    obj = VplexDistributedDevice()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
