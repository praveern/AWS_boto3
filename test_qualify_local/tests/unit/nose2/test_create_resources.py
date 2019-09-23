import os
import unittest
from test_qualify_local.resources.resource_factory import ALL_RESOURCE_CLASSES, ResourceFactory


def _current_path():
    return os.path.dirname(os.path.realpath(__file__))


# print(__file__)
# print(_current_path())
# print((os.path.dirname(os.path.dirname(_current_path()))))


class TestResourceCreation(unittest.TestCase):
    """
    This is the main test class.
    """
    def setUp(self):
        self._demo_to_flatten = {"DemoRDS": ["aws_db_instance", "AWS::RDS::DBInstance"],
                                 "DemoAzureSQL": ["Microsoft.Sql/servers/databases", "azurerm_sql_database"]}
        self._base_resource_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(_current_path()))),
                                                "resources")
        self._aws_resource = "AWS::RDS::DBInstance"
        self._azure_sql_resource = "azurerm_sql_database"
        self._resource_factory = ResourceFactory()
        self._new_keys = list(self._resource_factory.CLASS_MAPPING.keys())

    def test_if_resource_files_exist_and_match(self):
        resource_files = list()
        for current_open_path, dirs, files in os.walk(self._base_resource_path):
            for file in files:
                if os.path.basename(file) == 'resource.py':
                    if os.path.join(self._base_resource_path, file) != os.path.join(
                        current_open_path, file
                    ):
                        resource_files.append(os.path.join(current_open_path, file))
        self.assertEqual(len(ALL_RESOURCE_CLASSES), len(resource_files),
                         "Mismatch in the resource classes")

    def test_detect_resources(self):
        self.assertEqual(len(ALL_RESOURCE_CLASSES), len(self._new_keys),
                         "Need the same number of elements on both sides for zip")
        for k, v in zip(ALL_RESOURCE_CLASSES, self._new_keys):
            self.assertEqual(k.__name__, v)

    ## Any further additions to the resources would be added below as new tests.
    def test_aws_create_function(self):
        _new_resource = self._resource_factory.create(self._aws_resource)
        self.assertEqual(_new_resource.get_type(), "rds")

    def test_azure_sql_create_function(self):
        _new_resource = self._resource_factory.create(self._azure_sql_resource)
        self.assertEqual(_new_resource.get_type(), "azure_sql")
