from ..cloud_init_generator import BaseCloudInitGenerator
import yaml
import subprocess


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
        # TODO: add _verify_branch to make sure branch exists in devstack repo.
        branch = self.config_dict.get('branch', 'master')
        self._verify_branch(branch, self.meta_info)

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
                    'content': ("#!/bin/sh\n"
                                "DEBIAN_FRONTEND=noninteractive sudo apt-get -qqy update || sudo yum update -qy\n"
                                "DEBAIN_FRONTEND=noninteractive sudo apt-get install -qqy git || sudo yum install -qy git\n"
                                "sudo chown stack:stack /home/stack\n"
                                "cd /home/stack\n"
                                "git clone -b {} https://git.openstack.org/openstack-dev/devstack\n"
                                "cd devstack\n"
                                "{}"
                                "./stack.sh"
                                ).format(branch, self._get_localrc_conf()),
                    'path': "/home/stack/start.sh",
                    'permissions': '0755'
                }
            ],
            "package_upgrade": "true",
            "runcmd": ['su -l stack ./start.sh'],
            "output": { 'all': '| tee -a /var/log/cloud-init-output.log' }
        }

        return "#cloud-config\n{}".format(yaml.dump(cloud_init_skeleton))

    def _get_localrc_conf(self):
        # self.args['devstack_config'] should be the absolute path to the user-defined devstack
        # configuration file.
        devstack_config = self.args.devstack_config
        devstack_config_string = ''
        if devstack_config:
            with open(devstack_config) as f:
                for line in f:
                    devstack_config_string += self._prepare_line(line)
        # if devstack_config is not specified in args, then go with the vanilla install
        else:
            devstack_config_string = (
                "echo '[[local|localrc]]' > local.conf\n"
                "echo ADMIN_PASSWORD=password >> local.conf\n"
                "echo DATABASE_PASSWORD=password >> local.conf\n"
                "echo RABBIT_PASSWORD=password >> local.conf\n"
                "echo SERVICE_PASSWORD=password >> local.conf\n"
            )

        return devstack_config_string

    def _prepare_line(self, line):
        """
        Prepend "echo" in front of the line, and append ">> local.conf" to the end of line
        This is so we can appriopriatly generate the localrc file inside the VM using
        cloud init's writefiles directive.
        :param line:
        :return:
        """
        line = line.rstrip()
        return "{} \'{}\' {}".format("echo", line, ">> local.conf\n")

    def _verify_branch(self, branch, meta_info):
        github_repo = meta_info.get('github_repo', '')
        git_ls_remote_p = subprocess.Popen(['git','ls-remote', github_repo, '|', 'grep', branch],
                                           stdout=subprocess.PIPE)
        stdout, stderr = git_ls_remote_p.communicate()
        git_ls_remote_p.wait()
        if not stdout:
            print "Branch {} does not exist in the devstack repo. Exiting..".format(branch)
            exit()

