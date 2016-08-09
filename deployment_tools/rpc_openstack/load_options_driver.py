import requests
import re

# how should options be discovered in RPCO?????
# Can I just take the lines that start with "export VARIABLE"?
def load_options(config_file_dict):

    meta_info = _find_rpco_meta_info(config_file_dict)
    deployment_scripts_links = meta_info['deployment_scripts_links']
    options_list = list()

    # Read in each file, parsing out each variable preceeded with "export".
    # This is my rule: any bash variable exported to the environment is a configurable option for rpc,
    # with defaults set to their value
    for deployment_scripts_link in deployment_scripts_links:
        response = requests.get(deployment_scripts_link)
        lines_of_file = response.text.split('\n')
        for line in lines_of_file:
            option_info = list()
            result = re.search("^export ([_A-Z]+)=[\$\{\}_A-Z]+:-\"([a-z]+)\"\}", line)
            if result:
                option_info.append("--{}".format(result.group(1).lower()))
                option_info.append(result.group(2))
                option_info.append("For a description, see RPCO README")
                options_list.append(option_info)
    return options_list




def _find_rpco_meta_info(config_file_dict):
    """
    return a dictionary representing the meta info of the rpco deployment tool
    :param config_file_dict:
    :return:
    """

    for deployment_tool in config_file_dict['deployment_tools']:
        meta_info = deployment_tool['meta']
        if meta_info['shorthand_name'] == "rpco":
            return meta_info
