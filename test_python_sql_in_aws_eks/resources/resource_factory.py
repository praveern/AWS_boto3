import inspect
import os
import pkgutil
from test_qualify_local.helpers.extractor import Extractor


def _current_path():
    return os.path.dirname(os.path.realpath(__file__))


def __search_for_all_resources(path):
    all_resources = list()
    """
    Simply searches for all "resource.py" files and lists out all available
    resource classes, but only the ones INSIDE PLUGIN FOLDERS. They are the
    true resource classes.

    Args:
        path: Path where to look for resources. If it is a multi-level package,
              then a recursive search is performed.

    :return: Nothing. Stored in the variable defined globally.
    """

    def is_it_really_a_class_member(object_name, moduleName):
        """
        What this function performs is a simple comparison between the currently opened module's name and the selected
        object's name, that is whether or not they are the same; AFTER confirming that the selected object is indeed, a class.

        This basically allows us to differentiate between the module defined classes and module imported classes.
        In turn, it makes the resource selection more accurate. Only the resources defined inside "resource.py" are
        selected at the end of the main function in file.

        :param object_name: Currently selected object name.
        :param moduleName: Currently selected module's name.
        :return:
        """
        ## This is the test part that gives a verbose explanation for the tests. Just uncomment if needed for debugging.
        # print("Object name: ", object_name)
        # print("Object module name: ", object_name.__module__)
        # print("Is it class?", inspect.isclass(object_name))
        # print("Name", moduleName)
        # print("Is object.module == module.name?", object_name.__module__ == moduleName)
        # print("\n\n")
        return inspect.isclass(object_name) and object_name.__module__ == moduleName

    def remove_duplicates_from_list(input_list):
        """
        This sub-function is to remove the duplicates inside the list.
        NOTE: This is a temporary workaround for a strange occurrence which
              is causing some levels of duplication in a tested code.

        :param input_list: A list which can potentially contain duplicates.
        :return: De-duplicated list.
        """
        out_list = []
        newly_added = set()
        for val in input_list:
            if val not in newly_added:
                out_list.append(val)
                newly_added.add(val)
        return out_list

    current_path = _current_path()

    for importer, module_name, is_it_a_pkg in pkgutil.walk_packages(path):

        # If it is a package
        if is_it_a_pkg:
            all_resources = __search_for_all_resources([os.path.join(path[0], module_name)])

        # If it is having the name "resource" (and it is NOT a package)
        if module_name == 'resource':
            module = importer.find_module('resource').load_module('resource')

            # Need to check for whether is it the base resource class (which defines all resources as "resource")
            is_it_base_resource_file = \
                module.__file__ in [os.path.join(current_path, i)
                                    for i in os.listdir(current_path)
                                    if os.path.isfile(os.path.join(current_path, i))]

            if os.path.dirname(module.__file__) != os.path.dirname(__file__) \
                    and not is_it_base_resource_file:

                # Now loop for checking all possible class names - BUT they can
                # only be treated as resources if ACTUALLY defined in that
                # particular resource.py file. That is why I'm using the above
                # internal function.

                for possible_class_name in dir(module):

                    # Classes starting with " _ " / " __ " - that is not a valid start
                    if possible_class_name.startswith('_') or \
                            possible_class_name.startswith('__'):
                        continue

                    possible_class = getattr(module, possible_class_name)

                    if not inspect.isclass(possible_class):
                        continue

                    if not is_it_really_a_class_member(possible_class, module.__name__):
                        continue

                    if possible_class not in all_resources:
                        all_resources.append(possible_class)

    return remove_duplicates_from_list(all_resources)


ALL_RESOURCE_CLASSES = __search_for_all_resources([_current_path()])


# def load_config(config_file_name=''):
#     """
#     Loads up the correct config. If none is given then use local config.
#
#     Args:
#         config_file_name: Config file name. Must always be located in
#                           app_config folder.
#
#     :return: The JSON config.
#     """
#     _data = None
#     if config_file_name == '':
#         try:
#             local_config_path = os.path.join(os.getcwd(), "app_configuration", "app_config-local.json")
#             if os.path.isfile(local_config_path):
#                 with open(local_config_path, 'r') as fr:
#                     _data = json.load(fr)
#                     # print(_data)
#             else:
#                 raise FileNotFoundError("cannot find the file {} with the specified".format(local_config_path))
#         except Exception:
#             logger.error("Error occurred during loading settings.")
#             raise
#     else:
#         pass
#     return _data


class ResourceFactory(object):
    """
    This class is used as the interface between the resource classes and the various resource types (which are
    defined differently in different specification templates).
    """

    ## This reference mapping connects resource types to the correct classes. Then the actual one-key-one-value
    ## dictionary will be created from which the correct "{resource_type: resource_class_type}" map is returned.
    REFERENCE_MAPPING = {"DemoRDS": ["aws_db_instance", "AWS::RDS::DBInstance"],
                         "DemoAzureSQL": ["Microsoft.Sql/servers/databases", "azurerm_sql_database"],
                         "DemoEC2": ["aws_instance", "AWS::EC2::Instance"],
                         "DemoAzureDataFactory": ["Microsoft.DataFactory/factories", "azurerm_data_factory"]}

    CURRENT_RESOURCES = Extractor.flatten_to_list(REFERENCE_MAPPING)

    CLASS_MAPPING = {ALL_RESOURCE_CLASSES[i].__name__: ALL_RESOURCE_CLASSES[i]
                     for i in range(0, len(ALL_RESOURCE_CLASSES))}

    ALL_RESOURCES_AVAILABLE = dict()

    @staticmethod
    def create(resource_type):
        if len(ResourceFactory.ALL_RESOURCES_AVAILABLE.keys()) == 0:

            # Get a resource class object
            for resource_class_type in ALL_RESOURCE_CLASSES:

                # Check if its maps to the list containing the resource type value
                for resource_current in ResourceFactory.CURRENT_RESOURCES:

                    if resource_current in \
                            ResourceFactory.REFERENCE_MAPPING[resource_class_type.__name__]:

                        # Map that class as a call to the resource type
                        # print(resource_class_type, "---", resource_current)

                        ResourceFactory.ALL_RESOURCES_AVAILABLE[resource_current] = \
                            ResourceFactory.CLASS_MAPPING[resource_class_type.__name__]

        return ResourceFactory.ALL_RESOURCES_AVAILABLE.get(resource_type, None)

    # @staticmethod
    # def get_ci_class(resource_type):
    #     pass


if __name__ == '__main__':
    print(ALL_RESOURCE_CLASSES)
    get_resource = ResourceFactory()
    new_resource = get_resource.create("azurerm_sql_database")
    print(new_resource.get_type(), "is created!")
    print("======================================")
    new_resource_2 = get_resource.create("AWS::RDS::DBInstance")
    print(new_resource_2.get_type(), "is created!")
