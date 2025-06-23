Role Name
=========

Creates storage view in a specific cluster in VPLEX

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
  * virtual_volume: "{{ list_of_virtual_volumes_to_add_in_view }}"

Dependencies
------------

Not Applicable

Example Playbook
----------------

Including an example of how to use your role

    - hosts: servers
      tasks:
        - name: Create storage view on VPLEX setup
          include_role:
            name: createstorageview

          vars:
            cluster_name: "{{ cluster_name_1 }}"
            virtual_volume: "{{ virtual_volume_list }}"


License
-------

Apache License 2.0

Author Information
------------------

Dell EMC VPLEX Ansible team <vplex.ansible@dell.com>
