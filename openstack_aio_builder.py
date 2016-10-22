#!/usr/bin/python

import yaml

from args import get_args_parser
from args import load_subparsers
from config import get_conf
import sys
import pprint


def main():

    # Load base options, initialize parser object
    print "Getting args parser"
    parser = get_args_parser()

    # Build the initial configuration dictonary.
    # Pass the parser because the load_options_driver might need some of it's information
    config_dict = get_conf(sys.argv)

    # Load the subparsers
    parser = load_subparsers(config_dict, parser)

    args = parser.parse_args()

    # Import the right cloud provider
    provider = config_dict['provider']['name']
    if args.smoke:
        print "Initializing {} provider instance maker object..".format(provider)
    InstanceMaker = __import__("cloud_providers.{}.instance_maker".format(provider), fromlist=["blah"]).InstanceMaker

    # Get the meta information for the subcommand being run
    print vars(args)
    deployment_tool_name = vars(args)['deployment_tool_name']
    deployment_tool_meta_info = _get_meta_info(config_dict['deployment_tools'], deployment_tool_name)

    # import the right cloud_init_generator plugin
    if args.smoke:
        print "Initialzing the {} cloud init config generator".format(
            vars(args)['deployment_tool_name'])
    CloudInitGenerator = __import__("deployment_tools.{}.cloud_init_generator".format(
        vars(args)['deployment_tool_name']), fromlist=["blah"]).CloudInitGenerator

    # Instantiating a CloudInitGenerator object
    cloud_init_generator = CloudInitGenerator(config_dict, args, deployment_tool_meta_info)

    # Generate the cloud_init config string representation
    cloud_init_config_string = cloud_init_generator.generate_cloud_init()

    if args.smoke:
        print "----CLOUD INIT CONFIG-----"
        print cloud_init_config_string
        print "--------------------------"

    instance_maker = InstanceMaker(args.instance_name, cloud_init_config_string,
                                   config_dict['provider']['auth_info'],
                                   **config_dict['provider']['instance_info']
                                   )
    # Create the instance
    if not args.smoke:
        instance_maker.create_instance()


def _get_meta_info(deployment_tools, deployment_tool_name):
    """
    Returns the dictionary in the deployment_tools list that contains
    the key value pair 'name':deployment_tool_name
    TODO: Change the structure of how deployment_tools are loaded into the config.
    List of dictionaries isn't very practical.

    :param deployment_tools: list of dictionaries representing a deployment_tool
    :param deployment_tool_name: the name of the deployment_tool whose meta info the function is returning
    :return: a dictionary representing a deployment_tool's meta info
    """

    for deployment_tool in deployment_tools:
        if deployment_tool_name in deployment_tool['meta'].values():
            return deployment_tool['meta']

if __name__ == "__main__":
    main()
