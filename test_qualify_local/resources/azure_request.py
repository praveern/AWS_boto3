import os
import requests


class DemoAzureRequest:
    """
    A demo fake "Azure" Request. Doesn't really request anything to Azure other
    than "Hey, Google!"
    """
    def __init__(self):
        self._this_req = "https://www.google.com/"
