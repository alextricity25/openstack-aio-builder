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
        # Verify the user is using a supported flavor
        self._verify_supported_flavors()
        # Verify the user is using a supported image
        self._verify_supported_image()

    def generate_cloud_init(self):
        cloud_init_skeleton = {
            # This was commented out on 06-12-2017 because updating any pacakges
            # before running bootstrap-ansible.yml with an artifacted AIO deployment
            # caused package dependency conflicts
            #"package_upgrade": "true",
            # Kind of looks like "pancakes" when you're tired
            "pacakges": list(),
            "runcmd": list(),
            "output": { 'all': '| tee -a /var/log/cloud-init-output.log' }
        }

        commands = list()

        # Adding required packages
        cloud_init_skeleton['packages'] = ['git', 'screen', 'tmux', 'python']

        # Create the tmux session
        commands.append("tmux new-session -d -s deploy")
        commands.append("tmux select-pane -t 0")

        # Create export commands out of the options given
        for option, value in vars(self.args).iteritems():
            commands.append(self._prepare_option(option, value))

        # Make sure we are ALWAYS deploying an AIO
        commands.append(self._prepare_option("DEPLOY_AIO", "yes"))

        # Set the HOME variable, because cloud-init in 16.04 is stupid
        commands.append(self._prepare_option("HOME", "/root"))

        # Make sure we are using git to get the OpenStack-Ansible roles
        commands.append(self._prepare_option("ANSIBLE_ROLE_FETCH_MODE", "git-clone"))

        # Export the branch name
        branch = self.config_dict['branch']
        commands.append(self._prepare_option("BRANCH", branch))

        # Cloning the repo, running the pre-deployment commands, the deployment scripts,
        # finally the post-deployment commands
        deploy_string = "tmux send-keys 'git clone -b $BRANCH --recursive {} /opt/rpc-openstack".format(
            self.meta_info['github_repo']
        )
        deploy_string += " && cd /opt/rpc-openstack"
        # Adding the pre-deployment commands if they are specified
        if self.config_dict.get('pre_deployment_commands'):
            deploy_string += " && " + ' && '.join(self.config_dict.get('pre_deployment_commands'))
        # Adding the deployment scripts
        deploy_string += " && ." + ' && .'.join(self.meta_info['deployment_scripts'])
        # Adding the post-deployment commands if they are specified
        if self.config_dict.get('post_deployment_commands'):
            deploy_string += ' && ' + ' && '.join(self.config_dict.get('post_deployment_commands'))
        deploy_string += "' C-m"

        # Adding the deploy_string as a command to the cloud_init cloud-config file.
        commands.append(deploy_string)
        cloud_init_skeleton['runcmd'] = commands

        return "#cloud-config\n{}".format(yaml.dump(cloud_init_skeleton))

    def _prepare_option(self, option_name, option_value):
        """
        Prepends "export" to the option name, and inserts "=" between the name and value

        :param option_name: The name of the option
        :param option_value: The value of the option
        :return: A string representation of how the options will be exported the the system environment
        """
        return "tmux send-keys 'export {}={}' C-m".format(option_name.upper(), option_value)

    def _verify_supported_flavors(self):
        """
        """
        flavor = self.config_dict['provider']['instance_info']['flavor']
        supported_flavors = self.meta_info['supported_flavors']
        if self.args.smoke:
            print "The flavor configured is: {}".format(
                flavor
            )
        for key, value in supported_flavors.items():
            if type(value) is list:
                for _flavor in value:
                    if _flavor == flavor:
                        return True

        # Flavor given is not a supported flavor, using the first
        # flavor defined as a supported flavor for this particular
        # cloud provider
        new_flavor = self.meta_info['supported_flavors'] \
                               [self.config_dict['provider']['name']][0]

        print "{} is not a supported flavor for this deployment tool!".format(
            flavor
        )
        print "The supported flavors are {}".format(supported_flavors.values())
        print "Using {} flavor instead.".format(new_flavor)

    def _verify_supported_image(self):
        """"""
        image = self.config_dict['provider']['instance_info']['image']
        supported_images = self.meta_info['supported_images']
        if self.args.smoke:
            print "The image conifgured is: {}".format(
                image
            )
        for key, value in supported_images.items():
            if type(value) is list:
                for _image in value:
                    if _image == image:
                        return True

        print "{} is not a supported image for this deployment tool!".format(
            image
        )
        print "The supported images are {}".format(supported_images.values())
        exit()
