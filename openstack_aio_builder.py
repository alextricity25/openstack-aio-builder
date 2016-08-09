import yaml

from args import get_args_parser
from config import get_conf
import pprint








def main():

    #args = get_args()

    # For testing puposes
    config_dict = get_conf()
    #pprint.pprint(config_dict)
    parser = get_args_parser(config_dict)
    args = parser.parse_args()

    # update the config and parser depending on what the subparser commands are



if __name__ == "__main__":
    main()