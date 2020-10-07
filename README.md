# Ansible Modules for Dell EMC VPLEX

The Ansible Modules for Dell EMC VPLEX allow to provision the storage volume.

The capabilities of Ansible modules are managing storage views, initiators, ports, consistency groups, virtual volumes, devices, extents and storage volumes and to get information of recently configured resources through gather facts. The options available for each capability are list, show, create, delete and modify. These tasks can be executed by running simple playbooks written in yaml syntax.

## Supported Platforms
  * Dell VPLEX GeoSynchrony 6.2

## Prerequisites
  * Ansible 2.7 or higher
  * Python >= 2.7.18
  * Red Hat Enterprise Linux 7.5, 7.6
  * VPLEX Python SDK 1.0

## Idempotency
The modules are written in such a way that all requests are idempotent. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell VPLEX
  * Storage View module
  * Initiator module
  * Port module
  * Consistency Group module
  * Virtual Volume module
  * Device module
  * Extent module
  * Storage Volume module
  * Rediscover Array module
  * Gather facts module

## Installation of SDK

  * Clone the latest development repository that contains VPLEX Python SDK
  * Export the python path with vplexapi
      export PYTHONPATH="{$PYTHONPATH}:<complete path of vplexapi>”
  * The above command works only on the current execution terminal. In order to make it persistent, we need to update the same export command in $HOME/.bashrc file followed by system reboot

## Installation of Ansible Modules

  * Clone the latest development repository that contains the ansible modules
  * Make ansible-vplex as the current working directory
    * cd ansible-vplex

  * Determine the current ansible and python versions by executing the command
      "ansible --version"

  * Based on the listed python version along with location displayed in the above command, configure the ansible modules with the below steps

    For e.g: 
    * [root@<user>~]# mkdir -p /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc
    * [root@<user>~]# mkdir -p /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc/__init__.py
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/module_utils/storage/__init__.py
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell/__init__.py
    * [root@<user>~]# cp -rf dellemc_ansible/utils/dellemc_ansible_vplex_utils.py /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell/dellemc_ansible_vplex_utils.py
    * [root@<user>~]# cp -rf dellemc_ansible/vplex/library/* /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc/
    * For ansible 2.7 version,
      [root@<user>~]# cp -rf dellemc_ansible/doc_fragments/dellemc_vplex.py /usr/lib/python2.7/site-packages/ansible/utils/module_docs_fragments/dellemc_vplex.py
    * For ansible 2.8 or higher,
      [root@<user>~]# cp -rf dellemc_ansible/doc_fragments/dellemc_vplex.py /usr/lib/python2.7/site-packages/ansible/plugins/doc_fragments/dellemc_vplex.py
