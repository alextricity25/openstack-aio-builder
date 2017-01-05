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
                                 server.addresses['public'][1]['addr']])
                server_list.append(server.name)

        print self.pt

