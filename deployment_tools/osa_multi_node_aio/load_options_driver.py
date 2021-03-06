import re
import subprocess
import os


def load_options(config_file_dict):

    # The directory to temporarily clone the repo to.
    REPO_TEMP_DIR = "/tmp/openstack-ansible-ops"

    # Write output os subprocess commands to devnull
    FNULL = open(os.devnull, 'w')

    meta_info = _find_meta_info(config_file_dict)
    options_list = list()

    # If the repo already exists, print out a warning informing the user that it
    # might be outdated
    if os.path.isdir(REPO_TEMP_DIR):
        #print ("WARNING: {} already exists, and could be outdated. If you want to pull in the latest"
                #" codebase, delete the directory").format(OSA_TEMP_DIR)
        pass
        #TODO: Make an option that will force delete TEMP_DIR
        #shutil.rmtree(OSA_TEMP_DIR)
    else:
        git_clone_command = ['git', 'clone', meta_info['github_repo'], REPO_TEMP_DIR]
        git_clone_p = subprocess.Popen(git_clone_command, stdout=FNULL)
        git_clone_p.wait()
        if git_clone_p.returncode:
            print "'{}' failed with return code {}".format(
                " ".join(git_clone_command),
                git_clone_p.returncode
            )

    # Check out the right branch specified in the config
    git_checkout_command = ['git', 'checkout', config_file_dict['branch']]
    git_checkout_p = subprocess.Popen(git_checkout_command,
                                      stdout=FNULL,
                                      stderr=FNULL,
                                      cwd=REPO_TEMP_DIR)
    git_checkout_p.wait()

    # Read in each file, parsing out each variable that starts with "export".
    # This is my rule: any bash variable exported to the environment is a configurable option for osa AIO,
    # with defaults set to the bash variable's value defined in the deployment script.
    # The tool is located in the multi-node-aio, so we open the deployment scripts
    # from that directory.
    for deployment_script in meta_info['deployment_scripts']:
        with open("{}/multi-node-aio/{}".format(REPO_TEMP_DIR, deployment_script)) as f:
            for line in f:
                option_info = list()
                result = re.search("^([_A-Z]+)=[\$\{\}_A-Z]+:-[\"\']*([=\w\.\/-]*)[\"\']*\}", line)
                if result:
                    option_info.append("--{}".format(result.group(1).lower()))
                    option_info.append(result.group(2))
                    option_info.append("For a description, see OSA README")
                    options_list.append(option_info)

    return options_list

# TODO: The meta_info dictionary is already available in the config_file_dict,
# we just need the key to use for accessing it. The key name is available as
# part of the args dataset, so it might be worth while to pass that into this
# class here.
def _find_meta_info(config_file_dict):
    """
    return a dictionary representing the meta info of the osa deployment tool
    :param config_file_dict:
    :return:
    """

    for deployment_tool in config_file_dict['deployment_tools']:
        meta_info = deployment_tool['meta']
        if meta_info['shorthand_name'] == "osa_multi_aio":
            return meta_info