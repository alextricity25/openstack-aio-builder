from get_client import get_client
from prettytable import PrettyTable
import re

class Glimpse():

    def __init__(self, auth_info, regex_pattern):
        self.regex_pattern = regex_pattern
        self.pt = PrettyTable()
        self.client = get_client(auth_info)

    def glimpse(self):
        # Create list of servers whose name matches the regex pattern

        self.pt.field_names = ["Server Name", "IP"]
        server_list = list()

        for server in self.client.servers.list():
            if re.match(self.regex_pattern, server.name):
                self.pt.add_row([server.name,
                                 self._get_ipv4_address(server.addresses)])
                server_list.append(server.name)

        print self.pt

    def _get_ipv4_address(self, addresses):
        """
        Takes in a dictionary of addresses of the form:
        {u'private': [{u'addr': u'10.208.128.99', u'version': 4}],
         u'public': [{u'addr': u'2001:4802:7802:101:be76:4eff:fe20:e736',
                      u'version': 6},
                     {u'addr': u'162.242.251.65', u'version': 4}]}
        :return: string representing an ipv4 address
        """
        for key, value in addresses.items():
            if key == 'GATEWAY_NET_V6':
                for addr_info in value:
                    if "." in addr_info.get("addr", ""):
                        return addr_info['addr']

        return "Address not found"




