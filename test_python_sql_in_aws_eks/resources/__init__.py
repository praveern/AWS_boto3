from test_qualify_local.resources.resource import DemoResource
from test_qualify_local.resources.resource_factory import ResourceFactory
from test_qualify_local.resources.aws_resource import DemoAWSResource
from test_qualify_local.resources.azure_request import DemoAzureRequest
from test_qualify_local.resources.rds import DemoRDS
from test_qualify_local.resources.azure_sql import DemoAzureSQL
from test_qualify_local.resources.ec2 import DemoEC2

__all__ = [DemoResource, DemoAWSResource, DemoRDS, DemoAzureRequest, DemoAzureSQL, ResourceFactory]
