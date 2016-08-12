import yaml

from args import get_args_parser
from config import get_conf
import pprint
import os


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

    # Instantiate an InstanceMaker object
    # We are using this cloud_init config for testing purposes,
    # the real cloud_init_config will be dynamically generated
    # by the deployment tool's cloud_init_generator plugin
    with open(os.path.abspath("./tests/test_cloud_init_deploy_osa.yml")) as f:
        print "opening..{}".format(os.path.abspath("./tests/test_cloud_init_deploy_osa.yml"))
        instance_maker = InstanceMaker("cantu-testing", f, config_dict['provider']['auth_info'],
                                        **config_dict['provider']['instance_info'])
        instance_maker.create_instance()



    # Create the instance



if __name__ == "__main__":
    main()