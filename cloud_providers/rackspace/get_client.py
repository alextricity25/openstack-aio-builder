from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options()