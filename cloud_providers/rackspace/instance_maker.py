from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client
from ..instance_maker import InstanceMaker
from get_client import get_client

# This InstanceMaker class can be shared across all cloud providers
class InstanceMaker():

    def __init__(self, name, cloud_init_config, auth_info, instance_info):

        self.name = name
        self.cloud_init_config = cloud_init_config
        self.auth_info = auth_info
        self.image = instance_info['image']
        self.flavor = instance_info['flavor']
        self.files = instance_info['files']
        self.key_name = instance_info['key_name']
        self.admin_pass = instance_info['admin_pass']
        self.client = get_client(auth_info)

        print "Initializing RaxInstanceMaker"

    def create_instance(self):

        # Because I like the name nova better
        nova = self.client
        nova.servers.create(self.name, self.image, self.flavor, files=self.files,
                            userdata=self.cloud_init_config, key_name=self.key_name,
                            admin_pass=self.admin_pass)
