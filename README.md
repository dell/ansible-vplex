# Ansible Modules for Dell EMC VPLEX
The Ansible Modules for Dell EMC VPLEX allow to provision the storage volume.

The capabilities of Ansible modules are managing storage views, initiators, ports, consistency groups, virtual volumes, devices, extents, data migration jobs and storage volumes and to get information of recently configured resources through gather facts. The options available for each capability are list, show, create, delete and modify. These tasks can be executed by running simple playbooks written in yaml syntax.

## Support
Ansible modules for VPLEX are supported by Dell EMC and are provided under the terms of the license attached to the source code. Dell EMC does not provide support for any source code modifications. For any Ansible module issues, questions or feedback, join the [Dell EMC Automation community](https://www.dell.com/community/Automation/bd-p/Automation).

## Supported Platforms
  * Dell VPLEX GeoSynchrony 6.2
  * Metro Node 7.0
  * Metro Node 9.0

## Prerequisites
  * Ansible 2.18
  * Python 3.13
  * VPLEX Python SDK 6.2, 7.0, 8.0, 8.0.1, 9.0
  * Red Hat Enterprise Linux 7.5, 7.6, 8.1, 9.4
  * Cent OS 7.6
  * SLES (SUSE Linux Enterprise Server) SLES 15 SP1 (For Metro node - VPLEX Management server)

## Idempotency
The modules are written in such a way that all requests are idempotent. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell VPLEX
  * Storage View module
  * Initiator module
  * Port module
  * Consistency Group module
  * Distributed Consistency Group module
  * Virtual Volume module
  * Distributed Virtual Volume module
  * Device module
  * Distributed Device module
  * Extent module
  * Storage Volume module
  * Rediscover Array module
  * Gather facts module
  * Data migration module
  * Maps module

## Installation of SDK
  * git clone https://github.com/dell/python-vplex.git  
  
  * Export the python path with vplexapi
      export PYTHONPATH='{$PYTHONPATH}:<complete path of vplexapi>'
  * The above command works only on the current execution terminal. In order to make it persistent, we need to update the same export command in $HOME/.bashrc file followed by system reboot

## Installing Collections
  * Download the tar build and follow the below command to install the collection anywhere in your system:
        ansible-galaxy collection install dellemc-vplex-1.3.0.tar.gz -p ./collections

  * Set the environment variable:
        export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>/collections

## Using Collections
  * In order to use any Ansible module, ensure that the importing of proper FQCN(Fully Qualified Collection Name) must be embedded in the playbook. Below example can be referred.
        collections:
        - dellemc.vplex

  * For generating Ansible documentaion for a specific module, embed the FQCN before the module name. Below example can be referred.
        ansible-doc dellemc.vplex.dellemc_vplex_gatherfacts

## Running Ansible Modules
The Ansible server must be configured with Python library for VPLEX to run the Ansible playbooks. The [Documents]( https://github.com/dell/ansible-vplex/tree/1.2.0/dellemc_ansible/docs ) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which needs to be configured before running the modules.

## SSL Certificate Validation
  * Copy the CA certificate to this "/etc/pki/ca-trust/source/anchors" path of the host by any external means.
  * Set the "REQUESTS_CA_BUNDLE" environment variable to the path of the SSL certificate using the command "export REQUESTS_CA_BUNDLE=/etc/pki/ca-trust/source/anchors/<<Certificate_Name>>"
  * Import the SSL certificate to host using the command "update-ca-trust".

## Results
Each module returns the updated state and details of the entity.
For example, if you are using the device module, all calls will return the updated details of the device.
Sample result is shown in each module's documentation.

## VPlex log collection script
Whenever a task fails the script vplexlog_collection.py collects the vplexapi logs, ansible module logs, the system logs and saves them in a folder Logs/Logs_ in the current execution path.

## Prerequisites
 * Copy tools/vplexlog_collection.py to the path of the playbook
 * Add a block for rescue in the playbook like shown in tools/log_collection.yml
 * Install sshpass
 * Add the Vplex server IP to the file ~/.ssh/known_hosts in the test system
 * Set the python path for vplexapi
 * export PYTHONPATH="{$PYTHONPATH}:/<vplexapi_PATH>"
