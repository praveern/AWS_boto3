from test_qualify_local.resources.aws_resource import DemoAWSResource


class DemoEC2(DemoAWSResource):

    @staticmethod
    def get_type():
        return "ec2"
