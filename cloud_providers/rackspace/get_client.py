from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client



def get_client(auth_info):
    # Get the rackspace cloud provider configurations, these configs should be in the
    # main configuration file.
    #provider_configs = config_file_dict['provider']
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=auth_info['auth_url'],
                                    username=auth_info['username'],
                                    password=auth_info['password'],
                                    project_id=auth_info['project_id'])

    sess = session.Session(auth=auth)
    nova = client.Client('2', session=sess)

    return nova
