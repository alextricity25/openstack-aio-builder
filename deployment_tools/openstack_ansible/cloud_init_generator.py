from ..cloud_init_generator import BaseCloudInitGenerator
import yaml


class CloudInitGenerator(BaseCloudInitGenerator):

    def __init__(self, args, meta_info, **kwargs):
        """
        :param args:
        :param kwargs:
        TODO: support these kwargs:
        kwargs['extra_packages']: list() - list of extra pacakges to be installed
        kwargs['extra_options']: dict() - dictionary with extra options
        kwargs['extra_pre_commands']: list() - list of commands to run before deploying rpc-openstack

        """
        BaseCloudInitGenerator.__init__(self, args)

        self.meta_info = meta_info
        print "Initialized CloudInitGenerator"

    def generate_cloud_init(self):
        """
        How should this plugin generate the cloud_init file?
        Maybe the cloud_init file for openstack-ansible should look like:

        package_upgrade: true
        packages:
          - git-core
          - screen
          - vim
          {% for package in kwargs['extra_packages'] %}
          - {{ package }}
          {% endfor %}

        runcmd:
          {% for option in args.subparser['osa'].get_options() %}
          - export {{ option.key }}={{ option.value }}
          {% endfor %}
          {% for extra_option in kwargs['extra_options'] %}
          - export {{ extra_option.key }}={{ extra_option.value }}
          {% endfor %}
          {% for extra_pre_command in kwargs['extra_pre_commands'] %}
          - extra_pre_command
          {% endfor %}
          - git clone -b ${args.TAG} ${meta.github_repo} /opt/openstack-ansible
          {% for deployment_script in meta.deployment_scripts %}
          - cd /opt/openstack-ansible && {{ deployment_script }}
          {% endfor %}
        output: { all: '| tee -a /var/log/cloud-init-output.log' }
        :return:
        """
        cloud_init_skeleton = {
            "package_upgrade": "true",
            "pacakges": list(),
            "runcmd": list(),
            "output": { 'all': '| tee -a /var/log/cloud-init-output.log' }
        }

        commands = list()

        # Adding required packages
        cloud_init_skeleton['packages'] = ['git', 'screen']

        # Create export commands out of the options given
        for option, value in vars(self.args).iteritems():
            commands.append(self._prepare_option(option, value))

        # Make sure we are ALWAYS deploying an AIO
        commands.append(self._prepare_option("DEPLOY_AIO", "yes"))

        # Set ansible_role_fetch_mode
        commands.append(self._prepare_option("ANSIBLE_ROLE_FETCH_MODE", "git-clone"))

        # Export HOME variable, because some tasks in the openstack-ansible
        # project require it, and the system hasn't set the variable this early
        # into the boot process.
        commands.append(self._prepare_option("HOME", "/root/"))

        # Clone the openstack-ansible repository
        # The branch value is loaded as an argparse argument in load_options_driver
        commands.append("git clone -b $BRANCH {} /opt/openstack-ansible".format(
            self.meta_info['github_repo']))

        # Grabing AIO deployment scripts from metadata file
        for deployment_script in self.meta_info['deployment_scripts']:
            commands.append("cd /opt/openstack-ansible && {}".format(deployment_script))

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