#!/usr/bin/python
# Copyright: (c) 2020, DellEMC
# GNU General Public License v3.0+

""" Maps module """

from __future__ import (absolute_import, division, print_function)


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_maps
version_added: '1.2.0'
short_description: Get storage entity usage hierarchy map
description:
- Get complete usage hierarchy for a storage element from
  bottom level storage-array to top level parent entity
  for VPLEX storage object.

extends_documentation_fragment:
  - dellemc.vplex.dellemc_vplex.vplex

author:
- Amit Uniyal (@euniami-dell) <vplex.ansible@dell.com>

options:
  cluster_name:
    description:
    - Name of the cluster
    type: str

  entity_type:
    description:
    - Type of the storage entity
    type: str
    required: True
    choices: [
        'virtual_volumes', 'devices', 'extents', 'storage_volumes'
    ]

  entity_name:
    description:
    - Name of the storage entity
    type: str
    required: True

'''

EXAMPLES = r'''
- name: Get virtual volumes
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    entity_type: 'virtual_volumes'
    entity_name: 'ansible_vv'

- name: Get distributed virtual volume
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    entity_type: 'virtual_volumes'
    entity_name: 'ansible_dd_vv'

- name: Get devices
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    entity_type: 'devices'
    entity_name: 'ansible_dev'

- name: Get distributed devices
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    entity_type: 'devices'
    entity_name: 'ansible_dd_dev'

- name: Get extents
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    entity_type: 'extents'
    entity_name: 'ansible_extent'

- name: Get storage volumes
  dellemc_vplex_maps:
    vplexhost: "{{ vplexhost }}"
    vplexuser: "{{ vplexuser }}"
    vplexpassword: "{{ vplexpassword }}"
    verifycert: "{{ verifycert }}"
    cluster_name: "cluster-1"
    entity_type: 'storage_volumes'
    entity_name: 'ansible_strg_vol'
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

map_details:
    description: Usage hierarchy map for storage entity
    returned: When given storage entity in valid and exists in VPLEX
    type: complex
    contains:
        storage_view:
            description: The name of storage view to which the given
                         storage entity is exported.
            type: str
        consistency_groups:
            description: The name of consistency group to which the given
                         storage entity belongs.
            type: str
        distributed_consistency_groups:
            description: The name of distributed consistency group if the given
                         storage entity is distributed entity.
            type: str
        virtual_volume:
            description: The name of virtual volume if exists over the given
                         storage entity.
            type: str
        distributed_virtual_volume:
            description: The name of distributed virtual volume if the given
                         storage entity is distributed entity.
            type: str
        device:
            description: The name of device in the map of given storage entity.
            type: str
        distributed_device:
            description: The name of distributed device if the given storage
                         entity is distributed entity.
            type: str
        extent:
            description: The name of extent under the given storage entity.
            type: str
        storage_array:
            description: The name of storage array to which the given
                         storage entity belongs.
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell\
    import dellemc_ansible_vplex_utils as utils

LOG = utils.get_logger('dellemc_vplex_maps')
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexMaps():
    """Class with maps operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_maps_parameters())

        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
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

        # Create an instance to MapsApi to communicate with
        # vplexapi
        self.maps_cl = utils.MapsApi(api_client=self.client)

        self.unsupported_entity = [
            'distributed_consistency_groups',
            'storage_views',
            'consistency_groups',
            'storage_arrays',
        ]

    def get_map(self, uri):
        """Get map object from VPLEX"""
        entity, name = uri.split('/')[-2:]
        entity = entity[:-1]
        LOG.info('Get %s map for %s', entity, name)
        try:
            res = self.maps_cl.get_map(uri)
            # LOG.info('Map Found')
            LOG.debug('Map details: %s', res)
            return res
        except (utils.ApiException, ValueError, TypeError) as err:
            err_msg = "Could not get map for {0} {1} due to"
            err_msg = err_msg.format(entity, name) + " error: {0}"
            e_msg = utils.display_error(err_msg, err)
            LOG.error("%s\n%s\n", e_msg, err)
            self.module.fail_json(msg=e_msg)

    def get_parents(self, uri, queue):
        """collect up to top level parent of entity"""
        for entity in self.unsupported_entity:
            if entity in uri:
                return queue
        obj = self.get_map(uri)
        for each in obj.parents:
            queue.insert(0, each)
            self.get_parents(each, queue)
        if uri not in queue:
            queue.append(uri)
        return queue

    def get_childrens(self, uri, queue):
        """Collect all children of entity"""
        for entity in self.unsupported_entity:
            if entity in uri:
                return queue

        if 'storage_volumes' in uri and '%3A' in uri:
            uri = uri.replace('%3A', ':')
        obj = self.get_map(uri)
        queue.update(
            {uri: tuple(obj.children)}
        )

        for each in obj.children:
            self.get_childrens(each, queue)
        return queue

    def show_use_hierarchy(self, data, entity_type):  # pylint: disable=R0201
        """
        Format/shape the use hierarchy of a storage entity down
        to storage-array level
        """
        d_dict = []
        for key, value in data.items():
            _prop, val = key.split('/')[-2:]
            if _prop == entity_type:
                d_dict.append(
                    '(* {0} ): {1}'.format(_prop, val)
                )
            else:
                d_dict.append(
                    '( {0} ): {1}'.format(_prop, val)
                )

            if 'storage_arrays' in value[0]:
                _prop, val = value[0].split('/')[-4:-2]
                d_dict.append(
                    '( {0} ): {1}'.format(_prop, val)
                )

        LOG.debug("Unformatted hierarchy: \n%s\n", d_dict)
        LOG.info("show-use-hierarchy: formatting entity usage hierarchy")

        indent = 0
        indent_cache = {}
        for each in d_dict:
            tmp = each.split('):')[0] + ')'
            if tmp not in indent_cache:
                indent_cache[tmp] = indent
                indent += 3

        for index, each in enumerate(d_dict):
            tmp = each.split('):')[0] + ')'
            for entity, indent in indent_cache.items():
                if tmp in entity:
                    d_dict[index] = " " * indent + each

        return d_dict

    def perform_module_operation(self):
        """perform module operations"""
        def exit_module(entity_map, change_flag):
            """module exit function"""
            entity_map = utils.serialize_content(entity_map)
            result = {
                "changed": change_flag,
                "map_details": entity_map
            }
            LOG.debug("Result %s\n", result)
            self.module.exit_json(**result)

        cluster_name = self.module.params['cluster_name']
        entity_type = self.module.params['entity_type']
        entity_name = self.module.params['entity_name']

        if cluster_name:
            uri = "/vplex/v2/clusters/{0}/{1}/{2}".format(
                cluster_name, entity_type, entity_name)
        elif entity_type in ['devices', 'virtual_volumes']:
            entity_type = 'distributed_' + entity_type
            uri = "/vplex/v2/distributed_storage/{0}/{1}".format(
                entity_type, entity_name)
        else:
            err_msg = ("Could not get map for {0} due to"
                       " error: Input entity_type, without cluster"
                       " is not supported".format(
                           entity_type))
            LOG.error("%s\n", err_msg)
            self.module.fail_json(msg=err_msg)

        LOG.info("Formed entity uri : %s", uri)
        parents = self.get_parents(uri, [])
        LOG.debug("Parent %s ", parents)
        for index, each in enumerate(parents):
            if not each.split('/')[-2] in self.unsupported_entity:
                toplevel_uri = each
                stack = parents[:index]
                break

        LOG.debug("Toplevel supported entity: %s ", toplevel_uri)
        stack = {each: ('toplevel_uri') for each in stack}
        stack.update(self.get_childrens(toplevel_uri, {}))
        LOG.debug("Stack %s", stack)
        the_map = self.show_use_hierarchy(stack, entity_type)
        exit_module(the_map, False)


def get_vplex_maps_parameters():
    """This method provide parameters required for the ansible maps
    module on VPLEX"""
    return dict(
        cluster_name=dict(required=False, type='str'),
        entity_type=dict(required=True, type='str', choices=[
            'virtual_volumes', 'devices', 'extents', 'storage_volumes'
        ]),
        entity_name=dict(required=True, type='str')
    )


def main():
    """Create VplexMaps object and perform action on it
        based on user input from playbook"""
    obj = VplexMaps()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
