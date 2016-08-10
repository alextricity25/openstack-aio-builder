import yaml

from args import get_args_parser
from config import get_conf
import pprint


def main():

    #args = get_args()

    # Build the initial configuration dictonary
    config_dict = get_conf()

    # Create options based off of that configuration
    parser = get_args_parser(config_dict)
    args = parser.parse_args()

    # import the right cloud provider
    provider = config_dict['provider']['name']
    InstanceMaker = __import__("cloud_providers.{}.instance_maker".format(provider), fromlist=["blah"]).InstanceMaker
    instance_maker = InstanceMaker("testing", "- run_cmd: echo hi", config_dict['provider']['auth_info'],
                                   config_dict['provider']['instance_info'])


    # Create the instance



if __name__ == "__main__":
    main()