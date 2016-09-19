import re
import subprocess
import os
import shutil

RPCO_TEMP_DIR = "/tmp/rpc-openstack"

# The directory to temporarily clone the repo to.
# Write output to devnull
FNULL = open(os.devnull, 'w')

def load_options(config_file_dict):



    meta_info = _find_rpco_meta_info(config_file_dict)
    options_list = list()

    if os.path.isdir(RPCO_TEMP_DIR):
        git_status_command = "git status | head -n 1 | awk '{print $3}'"
        git_status_p = subprocess.Popen(git_status_command,
                                        shell=True,
                                        stdout=FNULL,
                                        cwd=RPCO_TEMP_DIR)
        git_status_p.wait()
        if git_status_p.returncode:
            print "{} failed with return code {}".format(
                " ".join(git_status_command),
                git_status_p.returncode
            )
            exit()

        current_branch = git_status_p.stdout

        if current_branch != config_file_dict['branch']:
            git_checkout_command = ['git', 'checkout',
                                    config_file_dict['branch']]
            git_checkout_p = subprocess.Popen(git_checkout_command, stdout=FNULL,
                                              cwd=RPCO_TEMP_DIR)
            git_checkout_p.wait()
            if git_checkout_p.returncode:
                print "{} failed with return code {}".format(
                    " ".join(git_checkout_command),
                    git_checkout_p.returncode
                )
                exit()

    else:
        _get_repository(config_file_dict, meta_info)

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
                result = re.search("^export ([_A-Z]+)=[\$\{\}_A-Z]+:-[\"\']*([=\w\.\/-]*)[\"\']*\}", line)
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

def _get_repository(config_file_dict, meta_info):

    git_clone_command = ['git',
                         'clone',
                         '--recursive',
                         '-b',
                         config_file_dict['branch'],
                         meta_info['github_repo'],
                         RPCO_TEMP_DIR]
    git_clone_p = subprocess.Popen(git_clone_command, stdout=FNULL)
    git_clone_p.wait()
    if git_clone_p.returncode:
        print "'{}' failed with return code {}".format(
            " ".join(git_clone_command),
            git_clone_p.returncode
        )
        exit()

        # TODO: I need to figure out a better way of loading options so I don't have
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
