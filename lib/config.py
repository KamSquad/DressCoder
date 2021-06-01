import os
from collections import namedtuple
from dotenv import load_dotenv
from pprint import pprint


class EnvConfig:
    def __init__(self):
        """
        Get environment variables
        """
        try:
            load_dotenv('.env')
        except:
            load_dotenv('../.env')

        self.m_ports = namedtuple('m_ports', 'auth')
        self.m_ports.auth = int(os.environ.get("M_PORT_AUTH", default=2289))

    @staticmethod
    def get(name: str) -> str:
        return os.environ.get(name)

    def print_params(self) -> pprint:
        params = [self.m_ports]
        for param in params:
            new_param = {}
            param_dict = dict(vars(param))
            for value in param_dict:
                # print()
                if not value.startswith('_'):
                    new_param[value] = param_dict[value]
            pprint(new_param)
