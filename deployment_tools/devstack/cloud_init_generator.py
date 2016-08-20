from ..cloud_init_generator import BaseCloudInitGenerator
import yaml


class CloudInitGenerator(BaseCloudInitGenerator):

    def __init__(self, config_dict, args, meta_info, **kwargs):
        """
        Generate a cloud_init config file for deploying a rpc-openstack AIO.

        :param args: arguments from argparse
        :param kwargs: Any arbitrary kwargs that can extend this plugin's functionality.
        """
        BaseCloudInitGenerator.__init__(self, config_dict, args)

        self.meta_info = meta_info

    def generate_cloud_init(self):
        """
        """
        # cloud init example is from:
        # http://docs.openstack.org/developer/devstack/guides/single-vm.html
        cloud_init_skeleton = {
            "users": ['default',
                      {
                          'name': 'stack',
                          'lock_passwd': 'Flase',
                          'sudo': ["ALL=(ALL) NOPASSWD:ALL\nDefaults:stack !requiretty"],
                          'shell': "/bin/bash"
                      }],
            "write_files": [
                {
                    'content': ("#!/bin/sh"
                                "DEBIAN_FRONTEND=noninteractive sudo apt-get -qqy update || sudo yum update -qy\n"
                                "DEBAIN_FRONTEND=noninteractive sudo apt-get install -qqy git || sudo yum install -qy git\n"
                                "sudo chown stack:stack /home/stack\n"
                                "cd /home/stack\n"
                                "git clone https://git.openstack.org/openstack-dev/devstack\n"
                                "cd devstack\n"
                                "echo '[[local|localrc]]' > local.conf\n"
                                "echo ADMIN_PASSWORD=password >> local.conf\n"
                                "echo DATABASE_PASSWORD=password >> local.conf\n"
                                "echo RABBIT_PASSWORD=password >> local.conf\n"
                                "echo SERVICE_PASSWORD=password >> local.conf\n"
                                "./stack.sh"
                                ),
                    'path': "/home/stack/start.sh",
                    'permissions': '0755'
                }
            ],
            "package_upgrade": "true",
            "runcmd": ['su -l stack ./start.sh'],
            "output": { 'all': '| tee -a /var/log/cloud-init-output.log' }
        }

        return "#cloud-config\n{}".format(yaml.dump(cloud_init_skeleton))
