from ..cloud_init_generator import BaseCloudInitGenerator

class CloudInitGenerator(BaseCloudInitGenerator):

    def __init__(self, config_dict, args, meta_info, **kwargs):
        """
        Needs to inherit attributes from BaseCloudInitGenerator
        """
        BaseCloudInitGenerator.__init__(self, config_dict, args)

        self.meta_info = meta_info

    def generate_cloud_init(self):
        """
        This function is required. You must implement it.
        """
        pass
