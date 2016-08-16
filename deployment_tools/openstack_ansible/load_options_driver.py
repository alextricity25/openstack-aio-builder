import requests
import re


def load_options(config_file_dict):

    meta_info = _find_osa_meta_info(config_file_dict)
    deployment_scripts_links = meta_info['deployment_scripts_links']
    options_list = list()

    # Read in each file, parsing out each variable that starts with "export".
    # This is my rule: any bash variable exported to the environment is a configurable option for osa AIO,
    # with defaults set to the bash variable's value defined in the deployment script.
    for deployment_scripts_link in deployment_scripts_links:
        response = requests.get(deployment_scripts_link)
        lines_of_file = response.text.split('\n')
        for line in lines_of_file:
            option_info = list()
            result = re.search("^export ([_A-Z]+)=[\$\{\}_A-Z]+:-[\"\']([=\w\.\/-]*)[\"\']\}", line)
            if result:
                option_info.append("--{}".format(result.group(1).lower()))
                option_info.append(result.group(2))
                option_info.append("For a description, see OSA README")
                options_list.append(option_info)

    # Adding some extra options that are not in the deployment files for convenience.
    options_list.append(["--branch", "master", "The branch of openstack-ansible to checkout"])
    return options_list


def _find_osa_meta_info(config_file_dict):
    """
    return a dictionary representing the meta info of the osa deployment tool
    :param config_file_dict:
    :return:
    """

    for deployment_tool in config_file_dict['deployment_tools']:
        meta_info = deployment_tool['meta']
        if meta_info['shorthand_name'] == "osa":
            return meta_info
