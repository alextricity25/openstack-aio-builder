import argparse
import os

from utils import get_meta_file
from config import get_conf


# Really, these arguments are built based on what we find in the config,
# so the config dict needs to be built as part of this.
def get_args_parser(config_file_dict):
    # At this point, the provider, and deployment tools' meta.yml file has been loaded into the config.

    parser = argparse.ArgumentParser(description="OpenStack AIO Builder",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Global options

    # Cloud provider, default is rackspace.
    parser.add_argument('--cloud-provider',
                        default="rackspace",
                        help="The cloud provider you are going to use")


    # build subparses based off what plugins are available (this information should be in config_dict at this point.)
    # it should be in the deployment_tools list of dictionaries.


    _load_subparsers(config_file_dict, parser)

    return parser

# This should probably move to config.py
def _load_subparsers(config_file_dict, parser):
    """
    Create a list of subparsers, each one corresponding to a deployment tool. i.e OpenStack-Ansible, rpc-openstack

    :param parser: argparse.ArgumentParser
    :return: list()
    """

    # Initialize he subparsers
    subparsers_object = parser.add_subparsers(help='sub-command-help')

    # Get a list of the shorthand names of all deployment tools, and make the subparsers
    for deployment_tool in config_file_dict['deployment_tools']:
        try:
            meta_info = deployment_tool['meta']
        except KeyError:
            print "ERROR! Could not load deployment tool's meta file!"
            exit()
        subparser = subparsers_object.add_parser(meta_info['shorthand_name'],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 help=meta_info['description'])
        for option in deployment_tool['options']:
            subparser.add_argument(option[0], default=option[1], help=option[2])
#        for key, value in deployment_tool['meta'].items():
#            if key == 'shorthand_name':
#                subparser = subparsers_object.add_parser(value, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#                subparsers.append(subparser)
#                # load options for subparser


