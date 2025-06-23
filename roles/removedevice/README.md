Role Name
=========

Performs the teardown of local device from specific cluster in VPLEX

Requirements
------------

  * Ansible 2.16
  * Python 3.10
  * VPLEX Python SDK 6.2, 7.0
  * Red Hat Enterprise Linux 7.5, 7.6, 8.1
  * Cent OS 7.6
  * SLES (SUSE Linux Enterprise Server) SLES 15 SP1 (For Metro node - VPLEX Management server)

Role Variables
--------------

  * cluster_name: "{{ cluster_name }}"
  * devices: "{{ list_of_local_devices_in_specific_cluster }}"

Dependencies
------------

Not Applicable

Example Playbook
----------------

Including an example of how to use your role

    - hosts: servers
      tasks:
        - name: Remove local device from VPLEX setup
          include_role:
            name: removedevice

          vars:
            cluster_name: "{{ cluster_name_1 }}"
            devices: "{{ list_of_device_names }}"


License
-------

Apache License 2.0

Author Information
------------------

Dell EMC VPLEX Ansible team <vplex.ansible@dell.com>
