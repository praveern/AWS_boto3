import unittest
import os
from test_qualify_local.helpers.extractor import Extractor


def _current_path():
    return os.path.dirname(os.path.realpath(__file__))


class TestExtractorFunctions(unittest.TestCase):
    def setUp(self):
        self.val_dict = {
            'azurerm_sql_database': {
                'kind': 'v12.0',
                'properties': {
                    'administratorLogin': 'testsqluser',
                    'version': '12.0'
                }
            },
            'type': 'azure_sql'
        }
        self._demo_to_flatten = {"DemoRDS": ["aws_db_instance", "AWS::RDS::DBInstance"],
                                 "DemoAzureSQL": ["Microsoft.Sql/servers/databases", "azurerm_sql_database"]}

    def test_walk(self):
        key1 = "azurerm_sql_database.properties.version"
        extract_walk = Extractor.walk(key1, self.val_dict)
        self.assertEqual(extract_walk, "12.0")

    def test_flatten(self):
        key1 = "azurerm_sql_database.properties.version"
        flat_dict = Extractor.flatten(self.val_dict)
        self.assertEqual(flat_dict[key1], '12.0')

    def test_flatten_dict_of_lists(self):
        """ Specifically for the resource_factory class usage function. """
        self.assertEqual(Extractor.flatten_to_list(self._demo_to_flatten),
                         ["aws_db_instance", "AWS::RDS::DBInstance",
                          "Microsoft.Sql/servers/databases", "azurerm_sql_database"])
