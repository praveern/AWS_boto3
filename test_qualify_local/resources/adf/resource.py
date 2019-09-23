from test_qualify_local.resources.resource import DemoResource
from resources.azure_request import DemoAzureRequest


class DemoAzureDataFactory(DemoResource):

    def __init__(self):
        self.azr_req = DemoAzureRequest()
        super().__init__()

    @staticmethod
    def get_type():
        return "azure_sql"
