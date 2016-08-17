OpenStackAIOBuilder is a plugable, easy-to-use python command line utility that builds all-in-one
OpenStack development boxes deployed by your tool of choice, on your cloud service provider of choice.

A deployment tool may include, but not limited to:

* OpenStack-Ansible (https://github.com/openstack/openstack-ansible)
* Rackspace Private Cloud - OpenStack (https://github.com/rcbops/rpc-openstack)
* DevStack (https://github.com/openstack-dev/devstack) [WIP]

So long as the plugin exists, this tool can use it.

Cloud service providers include, but are not limited to:

* Rackspace Public Cloud

The deployment tools and cloud service providers that are available for this tool is dependent on whether or not someone
has made a plugin for it. Right now there is only plans to integrate the above deployment tools and cloud service
providers.

The tool works by taking in the github repo and deployment script path(s), then dynamically creating a cloud_init config
for deploying an AIO with the configured deployment tool. Once the cloud_init config has been created, it launches
a VM on the configured cloud service provider and runs it; leaving the user with a fully built OpenStack AIO development
server.

.. note::

  The cloud service provider VMs **must** support cloud_init for this tool to work.



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

Example usage for openstack-ansible plugin:

.. code-block::

  alex:openstack-aio-builder$ python openstack_aio_builder.py --instance-name cantu-08-17-osa osa -h
  Reading /etc/openstack_aio_builder/config.yml...
  Config file /etc/openstack_aio_builder/config.yml not found
  Reading ~/.config/openstack_aio_builder.yml...
  usage: openstack_aio_builder.py osa [-h] [--http_proxy HTTP_PROXY]
                                      [--https_proxy HTTPS_PROXY]
                                      [--ansible_package ANSIBLE_PACKAGE]
                                      [--ansible_role_file ANSIBLE_ROLE_FILE]
                                      [--ssh_dir SSH_DIR]
                                      [--debian_frontend DEBIAN_FRONTEND]
                                      [--bootstrap_opts BOOTSTRAP_OPTS]
                                      [--branch BRANCH]

  optional arguments:
    -h, --help            show this help message and exit
    --http_proxy HTTP_PROXY
                          For a description, see OSA README (default: )
    --https_proxy HTTPS_PROXY
                          For a description, see OSA README (default: )
    --ansible_package ANSIBLE_PACKAGE
                          For a description, see OSA README (default:
                          ansible==2.1.1.0)
    --ansible_role_file ANSIBLE_ROLE_FILE
                          For a description, see OSA README (default: ansible-
                          role-requirements.yml)
    --ssh_dir SSH_DIR     For a description, see OSA README (default:
                          /root/.ssh)
    --debian_frontend DEBIAN_FRONTEND
                          For a description, see OSA README (default:
                          noninteractive)
    --bootstrap_opts BOOTSTRAP_OPTS
                          For a description, see OSA README (default: )
    --branch BRANCH       The branch of openstack-ansible to checkout (default:
                          master)

Example usage for rpc-openstack plugin:

.. code-block::

  alex:openstack-aio-builder$ python openstack_aio_builder.py --instance-name cantu-08-17-osa rpco -h
  Reading /etc/openstack_aio_builder/config.yml...
  Config file /etc/openstack_aio_builder/config.yml not found
  Reading ~/.config/openstack_aio_builder.yml...
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
                                       [--ansible_parameters ANSIBLE_PARAMETERS]
                                       [--ansible_force_color ANSIBLE_FORCE_COLOR]
                                       [--bootstrap_opts BOOTSTRAP_OPTS]
                                       [--branch BRANCH]

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
    --ansible_parameters ANSIBLE_PARAMETERS
                          For a description, see RPCO README (default: )
    --ansible_force_color ANSIBLE_FORCE_COLOR
                          For a description, see RPCO README (default: true)
    --bootstrap_opts BOOTSTRAP_OPTS
                          For a description, see RPCO README (default: )
    --branch BRANCH       The branch of rpc-openstack to checkout (default:
                          master)

Features that it will include are:

* Support for multiple deployment tools
* Support for multiple cloud service providers(and maybe bare metal?)
* Ability to integrate a gerrit patch set, or github pull request by defining it before deployment.
* Dynamically build out python options based on the deployment script's configurable variables. For example,
  OpenStack-Ansible has a "bootstrap-aio.sh" script with many options that are configured through bash [environment]
  variables. These variables will be mapped to python options that can be consumed by the users of this tool. Options
  that are not specified should take on the defualt value of the original deployment script(i.e the bootstrap-aio.sh).
* Subcommands for this tool should be the deployment tools that are avialable to use. For example:
