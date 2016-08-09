OpenStackAIOBuilder is a plugable, easy-to-use python command line utility that builds all-in-one
OpenStack development boxes deployed by your tool of choice, on your cloud service provider of choice.

A deployment tool may include, but not limited to:
* OpenStack-Ansible (https://github.com/openstack/openstack-ansible) [WIP]
* Rackspace Private Cloud - OpenStack (https://github.com/rcbops/rpc-openstack) [WIP]
* DevStack (https://github.com/openstack-dev/devstack) [WIP]

So long as the plugin exists, this tool can use it.

Cloud service providers include, but are not limited to:
* Rackspace Public Cloud [WIP]

The deployment tools and cloud service providers that are available for this tool is dependent on whether or not someone
has made a plugin for it. Right now there is only plans to integrate the above deployment tools and cloud service
providers.

The tool works by taking in the github repo and deployment script path(s), then dynamically creating a cloud_init config
for deploying an AIO with the configured deployment tool. Once the cloud_init config has been created, it launches
a VM on the configured cloud service provider and runs it; leaving the user with a fully built OpenStack AIO development
server.

.. note::

  The cloud service provider VMs **must** support cloud_init for this tool to work.


Features that it will include are:
* Support for multiple deployment tools
* Support for multiple cloud service providers(and maybe bare metal?)
* Ability to integrate a gerrit patch set, or github pull request by defining it before deployment.
* Dynamically build out python options based on the deployment script's configurable variables. For example,
  OpenStack-Ansible has a "bootstrap-aio.sh" script with many options that are configured through bash [environment]
  variables. These variables will be mapped to python options that can be consumed by the users of this tool. Options
  that are not specified should take on the defualt value of the original deployment script(i.e the bootstrap-aio.sh).
* Subcommands for this tool should be the deployment tools that are avialable to use. For example:

.. code-block::

  openstack-aio-builder <osa | rpc | devstack>

* Options for these subcommands should be dynamically generated based off the configurable values of the deployment
  tools. For example:

.. code-block::

  openstack-aio-builder osa -h
  HTTP_PROXY
  HTTPS_PROXY
  ANSIBLE_PACKAGE
  ANSIBLE_ROLE_FILE
  SSH_DIR
  DEBIAN_FRONTEND
  ANSIBLE_ROLE_FETCH_MODE
  BOOTSTRAP_OPTS
  DEPLOY_AIO
  COMMAND_LOGS

It would be cool if this displayed the README of the deployment tool on how to deploy an AIO with it.

Example usage:

.. code-block::

  usage: openstack_aio_builder.py [-h] [--cloud-provider CLOUD_PROVIDER]
                                {rpco,devstack,osa} ...

  OpenStack AIO Builder

  positional arguments:
    {rpco,devstack,osa}   sub-command-help
      rpco                The rpc-openstack repo includes add-ons for the
                          Rackspace Private Cloud product that integrate with
                          the openstack-ansible set of Ansible playbooks and
                          roles
      devstack            DevStack is a set of scripts and utilities to quickly
                          deploy an OpenStack cloud.
      osa                 OpenStack-Ansible is an official OpenStack project
                          which aims to deploy production environments from
                          source in a way that makes it scalable while also
                          being simple to operate, upgrade, and grow.

  optional arguments:
    -h, --help            show this help message and exit
    --cloud-provider CLOUD_PROVIDER
                          The cloud provider you are going to use (default:
                          rackspace)

  usage: openstack_aio_builder.py rpco [-h] [--admin_password ADMIN_PASSWORD]
                                     [--deploy_aio DEPLOY_AIO]
                                     [--deploy_haproxy DEPLOY_HAPROXY]
                                     [--deploy_oa DEPLOY_OA]
                                     [--deploy_elk DEPLOY_ELK]
                                     [--deploy_maas DEPLOY_MAAS]
                                     [--deploy_tempest DEPLOY_TEMPEST]
                                     [--deploy_ceph DEPLOY_CEPH]
                                     [--deploy_swift DEPLOY_SWIFT]
                                     [--deploy_hardening DEPLOY_HARDENING]
                                     [--ansible_force_color ANSIBLE_FORCE_COLOR]

  optional arguments:
    -h, --help            show this help message and exit
    --admin_password ADMIN_PASSWORD
                          For a description, see RPCO README (default: secrete)
    --deploy_aio DEPLOY_AIO
                          For a description, see RPCO README (default: no)
    --deploy_haproxy DEPLOY_HAPROXY
                          For a description, see RPCO README (default: no)
    --deploy_oa DEPLOY_OA
                          For a description, see RPCO README (default: yes)
    --deploy_elk DEPLOY_ELK
                          For a description, see RPCO README (default: yes)
    --deploy_maas DEPLOY_MAAS
                          For a description, see RPCO README (default: no)
    --deploy_tempest DEPLOY_TEMPEST
                          For a description, see RPCO README (default: no)
    --deploy_ceph DEPLOY_CEPH
                          For a description, see RPCO README (default: no)
    --deploy_swift DEPLOY_SWIFT
                          For a description, see RPCO README (default: yes)
    --deploy_hardening DEPLOY_HARDENING
                          For a description, see RPCO README (default: yes)
    --ansible_force_color ANSIBLE_FORCE_COLOR
                          For a description, see RPCO README (default: true)
