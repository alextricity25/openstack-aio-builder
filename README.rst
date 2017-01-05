OpenStack-AIO- Builder is a plugable, easy-to-use python command line utility that builds all-in-one
OpenStack development boxes deployed by your tool of choice, on your cloud service provider of choice.

A deployment tool may include, but not limited to:

* OpenStack-Ansible (https://github.com/openstack/openstack-ansible)
* Rackspace Private Cloud - OpenStack (https://github.com/rcbops/rpc-openstack)
* DevStack (https://github.com/openstack-dev/devstack)

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

###########
Quick Start
###########

~~~~~~~~~~~~~~~~~~~~~~~~~
Make a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~

OpenStack-AIO-Builder (OAB), requires a configuration file in one of these directores to work:

* /etc/openstack_aio_builder/config.yml
* ~/.config/openstack_aio_builder.yml

A sample config file has been provided in the Github repo. It's named "sample_config.yml"

Another example:

.. code-block::

  provider:
    name: "rackspace"
    auth_info:
      auth_url: "https://identity.api.rackspacecloud.com/v2.0/"
      username: "your.user.name"
      password: "yourpassword"
      tenant_id: "accountnumber"
      project_id: "accountnumber"
      region_name: "IAD"
      auth_system: "rackspace"
    instance_info:
      # Any nova-supported attribute may be put here
      image: "8e7bdecd-380a-43d7-af9a-ec4f4df51dbd"
      flavor: "performance2-30"
      files: ""
      key_name: "alex_pub_iad"
      admin_pass: ""
  pre_deployment_commands:
    - touch /tmp/test_pre_deploy.txt
  post_deployment_commands:
    - git config --global user.name "Your name"
    - git config --global user.email "your.email@blah.com"

Once the config file is in place, you're ready to rock!

To build an Rackspace Private Cloud-OpenStack all-in-one, simply run:

.. code-block::

  ./openstack_aio_builder.py --instance-name test-rpco rpco

To build an OpenStack-Ansible all-in-one:

.. code-block::

  ./openstack_aio_builder.py --instance-name test-osa osa

To build a DevStack all-in-one:

.. code-block::

  ./openstack_aio_builder.py --instance-name test-devstack devstack

To build an OpenStack-Ansible all-in-one from a specific branch:

.. code-block::

  ./openstack_aio_builder.py --branch stable/newton --instance-name test-osa-newton osa

Branches can be specified for any deployment tool.

~~~~~~~~~~~~
Getting Help
~~~~~~~~~~~~

To see usage information, run the script with '-h' after the deployment tool. For example:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Usage for Rackspace Private Cloud-OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

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
                                     [--bootstrap_opts BOOTSTRAP_OPTS]
                                     [--unauthenticated_apt UNAUTHENTICATED_APT]

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
    --bootstrap_opts BOOTSTRAP_OPTS
                          For a description, see RPCO README (default: )
    --unauthenticated_apt UNAUTHENTICATED_APT
                          For a description, see RPCO README (default: no)

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Usage for OpenStack-Ansible
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

  usage: openstack_aio_builder.py osa [-h] [--http_proxy HTTP_PROXY]
                                    [--https_proxy HTTPS_PROXY]
                                    [--ansible_package ANSIBLE_PACKAGE]
                                    [--ansible_role_file ANSIBLE_ROLE_FILE]
                                    [--ssh_dir SSH_DIR]
                                    [--debian_frontend DEBIAN_FRONTEND]
                                    [--ansible_role_fetch_mode ANSIBLE_ROLE_FETCH_MODE]
                                    [--bootstrap_opts BOOTSTRAP_OPTS]

  optional arguments:
    -h, --help            show this help message and exit
    --http_proxy HTTP_PROXY
                          For a description, see OSA README (default: )
    --https_proxy HTTPS_PROXY
                          For a description, see OSA README (default: )
    --ansible_package ANSIBLE_PACKAGE
                          For a description, see OSA README (default:
                          ansible==2.2.0.0)
    --ansible_role_file ANSIBLE_ROLE_FILE
                          For a description, see OSA README (default: ansible-
                          role-requirements.yml)
    --ssh_dir SSH_DIR     For a description, see OSA README (default:
                          /root/.ssh)
    --debian_frontend DEBIAN_FRONTEND
                          For a description, see OSA README (default:
                          noninteractive)
    --ansible_role_fetch_mode ANSIBLE_ROLE_FETCH_MODE
                          For a description, see OSA README (default: galaxy)
    --bootstrap_opts BOOTSTRAP_OPTS
                          For a description, see OSA README (default: )
