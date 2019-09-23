from test_qualify_local.resources.aws_resource import DemoAWSResource


class DemoRDS(DemoAWSResource):

    @staticmethod
    def get_type():
        return "rds"
