
import os
import yaml
'''
what should the master config look like? Maybe something like...

{
    # this value can be gotten from
    # Hopefull the povider configs are part of the main programs configuration
    provider:
    {
        name: "rackspace",
        auth_url: "blah.blah.com:5000/v3.0",
        username: "someuser",
        password: "password",
        project_id: "some_project_id"
    },

    # These configs are loaded from the deployment tool's load_options_driver
    deployment_tools: [
    {
        name: "rpc_openstack"
        configs in meta.yml go here...
        Also, options that have been loaded by the load_opitons_driver go here.
'''

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
    "deployment_tools": list()
}

# Gets what's in the openstack_aio_builder, and the deployment tool's meta.yml file
def get_conf():
    """
    Get the configuration file
    :return: a dictionary representing all of the configs
    """

    for config_file in CONFIG_FILES:
        # If file is not found, try next one
        if not os.path.isfile(config_file):
            continue
        else:
            with open(config_file, 'r') as f:
                loaded_config = yaml.safe_load(f)

                # Loading cloud provider
                try:
                    config_file_dict["provider"] = loaded_config["provider"]
                except KeyError:
                    # TODO: I should raise the proper exceptions here.
                    print "Cloud provider must be defined in the global configuration file!"
                    exit()

                # Check to see if the provider is supported
                if config_file_dict["provider"]["name"] not in SUPPORTED_PROVIDERS:
                    print "The provider {} is not supported".format(config_file_dict["provider"])
                    exit()


            # Load the deployment tools' meta.yml file into the config dictionary.
            _load_deployment_tools_meta(config_file_dict)
            _load_options_for_deployment_tool(config_file_dict)
            return config_file_dict




def _load_deployment_tools_meta(config_file):
    """
    Loads the meta information for all deployment tools

    :param config_file: dict() - the configuration dictionary
    :return:
    """

    for file in _find_meta_files():
        deployment_tool = {
            "meta": dict(),
            "options": list()
        }

        with open(file, 'r') as f:
            loaded_meta_file = yaml.safe_load(f)

        deployment_tool['meta'] = loaded_meta_file
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

def _find_meta_files(directory=os.getcwd()):
    """
    Recursivly walk the directory, finding all meta.yml files.
    We need to read the meta files to find the deployment tool's name so we can map it to a subparser.

    :param directory: String to absolute or relative path of the directory to walk
    :return: list() of absolute path names of all meta.yml files in the project
    """
    meta_files = list()
    for root, dir, files in os.walk(directory):
        for file in files:
            if file == "meta.yml":
                meta_files.append("{}/{}".format(root, file))
    return meta_files
