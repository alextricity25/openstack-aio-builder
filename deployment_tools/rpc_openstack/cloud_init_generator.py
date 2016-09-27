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
        How should this plugin generate the cloud_init file?
        Maybe the cloud_init file for rpc_openstack should look like:

        package_upgrade: true
        packages:
          - git-core
          - screen
          - vim
          {% for package in kwargs['extra_packages'] %}
          - {{ package }}
          {% endfor %}

        runcmd:
          {% for option in args.subparser['rpco'].get_options() %}
          - export {{ option.key }}={{ option.value }}
          {% endfor %}
          {% for extra_option in kwargs['extra_options'] %}
          - export {{ extra_option.key }}={{ extra_option.value }}
          {% endfor %}
          {% for extra_pre_command in kwargs['extra_pre_commands'] %}
          - extra_pre_command
          {% endfor %}
          - git clone -b ${args.TAG} --recursive ${meta.github_repo} /opt/rpc-openstack
          {% for deployment_script in meta.deployment_scripts %}
          - cd /opt/rpc-openstack && {{ deployment_script }}
          {% endfor %}
        output: { all: '| tee -a /var/log/cloud-init-output.log' }
        :return:
        """
        cloud_init_skeleton = {
            "package_upgrade": "true",
            # Kind of looks like "pancakes" when you're tired
            "pacakges": list(),
            "runcmd": list(),
            "output": { 'all': '| tee -a /var/log/cloud-init-output.log' }
        }

        commands = list()

        # Adding required packages
        cloud_init_skeleton['packages'] = ['git', 'screen']

        # Run pre-deployment commands
        for command in self.config_dict.get('pre_deployment_commands', ''):
            commands.append(command)

        # Create export commands out of the options given
        for option, value in vars(self.args).iteritems():
            commands.append(self._prepare_option(option, value))

        # Make sure we are ALWAYS deploying an AIO
        commands.append(self._prepare_option("DEPLOY_AIO", "yes"))

        # Make sure we are using git to get the OpenStack-Ansible roles
        commands.append(self._prepare_option("ANSIBLE_ROLE_FETCH_MODE", "git-clone"))

        # Export the branch name
        branch = self.config_dict['branch']
        commands.append(self._prepare_option("BRANCH", branch))

        # Clone the rpc-openstack repository
        # The branch value is loaded as an argparse argument in load_options_driver
        commands.append("git clone -b $BRANCH --recursive {} /opt/rpc-openstack".format(
            self.meta_info['github_repo']))
        # TODO: pull these script paths from the metadata file

        for deployment_script in self.meta_info['deployment_scripts']:
            commands.append("cd /opt/rpc-openstack && .{}".format(deployment_script))

        # Run post-deployment commands
        for command in self.config_dict.get('post_deployment_commands', ''):
            commands.append(command)

        cloud_init_skeleton['runcmd'] = commands

        return "#cloud-config\n{}".format(yaml.dump(cloud_init_skeleton))

    def _prepare_option(self, option_name, option_value):
        """
        Prepends "export" to the option name, and inserts "=" between the name and value
        i.e export KEY=VALUE

        :param option_name: The name of the option
        :param option_value: The value of the option
        :return: A string representation of how the options will be exported the the system environment
        """
        return "export {}={}".format(option_name.upper(), option_value)
