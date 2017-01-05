import argparse
import os
import random
import string

from utils import get_meta_file
from config import get_conf


BASE_OPTIONS = [
    {
        "name": "--branch",
        "required": False,
        "default": "master",
        "help": "The branch of the deployment tool to use",
        "action": "store_true"
    },
    {
        "name": "--instance-name",
        "required": False,
        "help": "The name of the instance being spawned"
    },
    {
        "name": "--smoke",
        "required": False,
        "default": False,
        "action": "store_true",
        "help": "Run program as if it were normally run, but with debug messages and don't actually create the instance"
    },
    {
        "name": "--glimpse",
        "required": False,
        "default": False,
        "action": "store_true",
        "help": "Get a glimpse"
    }
]

def get_args_parser():
    # At this point, the provider, and deployment tools' meta.yml file has been loaded into the config.

    # Make parser
    parser = argparse.ArgumentParser(description="OpenStack AIO Builder",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Load base options
    for base_option_dict in BASE_OPTIONS:
        parser.add_argument(base_option_dict.pop("name"), **base_option_dict)

    # Load the subparsers
    #_load_subparsers(config_file_dict, parser)

    return parser


def load_subparsers(config_file_dict, parser):
    """
    Create a subparser for each corresponding to a deployment tool. i.e OpenStack-Ansible, rpc-openstack

    :param parser: argparse.ArgumentParser
    :return: list()
    """

    # Initialize the subparsers
    subparsers_object = parser.add_subparsers(help='sub-command-help')

    # Get a list of the shorthand names of all deployment tools, and make the subparsers
    for deployment_tool in config_file_dict['deployment_tools']:
        try:
            meta_info = deployment_tool['meta']
        except KeyError:
            print "ERROR! Could not load deployment tool's meta file!"
            exit()

        # Add a parser for each deployment tool using the shorthand name
        subparser = subparsers_object.add_parser(meta_info['shorthand_name'],
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                 help=meta_info['description'])

        # Adding an attribute to the parser, so we know what subcommand is being run
        # and what plugins to load post-invocation
        subparser.set_defaults(subcommand=meta_info['shorthand_name'])
        subparser.set_defaults(deployment_tool_name=meta_info['name'])

        # Adding the arguments for each subparser.
        for option in deployment_tool['options']:
            subparser.add_argument(option[0], default=option[1], help=option[2])

    return parser
