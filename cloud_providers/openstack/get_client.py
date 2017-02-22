import os_client_config

def get_client(auth_info):
    # Get the rackspace cloud provider configurations, these configs should be in the
    # main configuration file.
    nova = os_client_config.make_client('compute', **auth_info)
    return nova
