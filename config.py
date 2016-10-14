
import os
import yaml
import pprint

CONFIG_FILES = [
    "/etc/openstack_aio_builder/config.yml",
    "~/.config/openstack_aio_builder.yml",
    "{}/sample_config.yml".format(os.getcwd())
]

SUPPORTED_PROVIDERS = [
    "rackspace"
]

# This is going to have to be shared across the whole project
config_file_dict = {
    "provider": dict(),
    "deployment_tools": list(),
    "post_deployment_commands": list(),
    "pre_deployment_commands": list()
}

# Gets what's in the openstack_aio_builder, and the deployment tool's meta.yml file
def get_conf(branch, argv):
    """
    Get the configuration file
    :return: a dictionary representing all of the configs
    """

    # Set variable to true if smoke flag is detected
    is_smoke = '--smoke' in argv

    # Find args so they can be passed to the load_options_driver
    for config_file in CONFIG_FILES:
        # If file is not found, try next one
        config_file_path = os.path.expanduser(config_file)
        if is_smoke:
            print "Attempting to read config file {}".format(config_file_path)
        if not os.path.isfile(config_file_path):
            continue
        else:
            if is_smoke:
                print "Config file {} found. Using that one".format(config_file_path)
            with open(config_file_path, 'r') as f:
                loaded_config = yaml.safe_load(f)

                # Loading cloud provider
                try:
                    config_file_dict["provider"] = loaded_config["provider"]
                    if is_smoke:
                        print "Using {} provider".format(config_file_dict['provider'])
                except KeyError:
                    # TODO: I should raise the proper exceptions here.
                    print "Cloud provider must be defined in the global configuration file!"
                    exit()

                # Set branch to value provider in args. If no value was provided
                # in args, then check the config. If no value is still to be found,
                # default to master.
                if branch:
                    config_file_dict['branch'] = branch
                else:
                    config_file_dict['branch'] = loaded_config.get('branch', 'master')

                # Print branch name if smoke flag is given
                if is_smoke:
                    print "Using branch: {}".format(config_file_dict['branch'])

                # Check to see if the provider is supported
                if config_file_dict["provider"]["name"] not in SUPPORTED_PROVIDERS:
                    print "The provider {} is not supported".format(config_file_dict["provider"])
                    exit()

                # Gather pre-deployment commands
                if loaded_config.get('pre_deployment_commands', ''):
                    config_file_dict['pre_deployment_commands'] = loaded_config['pre_deployment_commands']

                # Gather post-deployment commands
                if loaded_config.get('post_deployment_commands', ''):
                    config_file_dict['post_deployment_commands'] = loaded_config['post_deployment_commands']

            # Find DP shorthand name from command line
            # Iterate through the list, starting from the end
            # Find first argument without "--" in front of it.
            for argument in argv[::-1]:
                if "--" in argument:
                    continue
                else:
                    dp_shorthand_name = argument
                    break

            if not dp_shorthand_name:
                print "ERROR: Unable to find shorthand name of deployment tool on command line!"
                exit()
            elif is_smoke:
                print "Shorthand name found: {}".format(dp_shorthand_name)

            # Load the deployment tools' meta.yml file into the config dictionary.
            _load_deployment_tools_meta(config_file_dict,
                                        shorthand_name_filter=dp_shorthand_name)
            _load_options_for_deployment_tool(config_file_dict)

            if is_smoke:
                print "Loaded config:"
                pprint.pprint(config_file_dict)

            return config_file_dict

def _load_deployment_tools_meta(config_file, shorthand_name_filter=None):
    """
    Loads the meta information for all deployment tools

    :param config_file: dict() - the configuration dictionary
    :return:
    """

    for file in _find_meta_files(shorthand_name_filter=shorthand_name_filter):
        deployment_tool = {
            "meta": file,
            "options": list()
        }

        config_file["deployment_tools"].append(deployment_tool)

def _load_options_for_deployment_tool(config_file_dict):
    """
    This function runs the load_options_driver for the respective deployment tool,
    and loads it into the configuration file dictionary.

    :param config_file_dict: the dictionary representing the configuration
    :return: config_file_dict
    """
    try:
        deployment_tools = config_file_dict['deployment_tools']
    except KeyError:
        print "Could not find deployment tools in the config file!"

    for deployment_tool in deployment_tools:
        try:
            meta_info = deployment_tool['meta']
        except KeyError:
            print "Cloud not find meta information for deployment tool"

        load_options_driver = meta_info['load_options_driver']
        load_options = __import__(load_options_driver, fromlist=["blah"]).load_options
        deployment_tool['options'] = load_options(config_file_dict)

def _find_meta_files(directory=os.path.dirname(__file__), shorthand_name_filter=None):
    """
    Recursivly walk the directory, finding all meta.yml files, reading them, and safe_loading them.
    We need to read the meta files to find the deployment tool's name so we can map it to a subparser.

    :param directory: String to absolute or relative path of the directory to walk
    :param shorthand_name_filter: String of a deployment tool's shorthand name to filter by.
                                  This will cause the code to check to see if the shorthand
                                  name defined in a DT's meta.yml file matches the filter
                                  specified here.
    :return: list() of the loaded yaml meta files of the deployment tools
    """

    meta_files = list()
    for root, dir, files in os.walk(directory):
        for file in files:
            if file == "meta.yml":
                full_file_path = "{}/{}".format(root, file)
                # In order to filter this file by shorthand_name, we
                # have to read it in and check the value
                with open(full_file_path, 'r') as f:
                    loaded_meta_file = yaml.safe_load(f)
                if shorthand_name_filter:
                    if loaded_meta_file['shorthand_name'] == shorthand_name_filter:
                        meta_files.append(loaded_meta_file)
                        break
                else:
                    meta_files.append(loaded_meta_file)

    return meta_files
