
class BaseCloudInitGenerator():

    def __init__(self, args):
        """
        Base class for the cloud_init_generator plugins for deployment_tools

        :param args: The arguments built from the main program
        :parm writing_dest: The file the driver will write the cloud_init config file to when specified

        """
        self.args = args

    def generate_cloud_init(self):
        """
        This function's implementation should be in every class that inherits from BaseCloudInitGenerator
        It will generate a cloud_init config string, and dump it out to self.writing_dest

        :return: str() - it will return a string representation of the cloud_init config file.
        """
        pass
