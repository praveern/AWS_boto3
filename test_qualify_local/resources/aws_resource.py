from test_qualify_local.resources.resource import DemoResource


class DemoAWSResource(DemoResource):
    """
    A demo AWS resource. Simply wrote this for testing some logic.
    """
    def __init__(self):
        super().__init__()
