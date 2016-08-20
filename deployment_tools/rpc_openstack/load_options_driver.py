import re
import subprocess
import os

# how should options be discovered in RPCO?????
# Can I just take the lines that start with "export VARIABLE"?
def load_options(config_file_dict):


    # The directory to temporarily clone the repo to.
    RPCO_TEMP_DIR = "/tmp/rpc-openstack"
    # Write output to devnull
    FNULL = open(os.devnull, 'w')

    meta_info = _find_rpco_meta_info(config_file_dict)
    options_list = list()

    # If the repo already exists, print out a warning informing the user that it
    # might be outdated
    if os.path.isdir(RPCO_TEMP_DIR):
        #print ("WARNING: {} already exists, and could be outdated. If you want to pull in the latest"
               #" codebase, delete the directory").format(RPCO_TEMP_DIR)
        pass
        # TODO: Make an option that will force delete RPCO_TEMP_DIR
        # shutil.rmtree(RPCO_TEMP_DIR)
    else:
        git_clone_command = ['git',
                             'clone',
                             '--recursive',
                             meta_info['github_repo'],
                             RPCO_TEMP_DIR]
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
                                      cwd=RPCO_TEMP_DIR)

    # I need to figure out a better way of loading options so I don't have
    # to load all of the plugins, but just the one being used.
#    git_checkout_p.wait()
#    if git_checkout_p.returncode:
#        print "'{}' failed with return code {}".format(
#            " ".join(git_checkout_command),
#            git_checkout_p.returncode
#        )

    # Update the submodule, just in case it might be old.
    git_submodule_update_command = ['git',
                                    'submodule',
                                    'update']
    git_submodule_update_p = subprocess.Popen(git_submodule_update_command,
                                              stdout=FNULL,
                                              cwd=RPCO_TEMP_DIR)
    git_submodule_update_p.wait()
    if git_submodule_update_p.returncode:
        print "'{}' failed with return code {}".format(
            " ".join(git_submodule_update_command),
            git_submodule_update_p.returncode
        )

    FNULL.close()

    # Read in each file, parsing out each variable that starts with "export".
    # This is my rule: any bash variable exported to the environment is a configurable option for rpco AIO,
    # with defaults set to the bash variable's value defined in the deployment script.
    for deployment_script in meta_info['deployment_scripts']:
        with open("{}{}".format(RPCO_TEMP_DIR, deployment_script)) as f:
            for line in f:
                option_info = list()
                result = re.search("^export ([_A-Z]+)=[\$\{\}_A-Z]+:-[\"\']([=\w\.\/-]*)[\"\']\}", line)
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
