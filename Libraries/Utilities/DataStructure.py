from robot.api.deco import keyword, library
from collections import defaultdict
from json import dumps, loads


@library(doc_format='ROBOT')
class DataStructure:
    @keyword("Update Or Create Dictionary")
    def update_or_create_dict(self, base_dict=None, reference_dict=None, *args, **kwargs):
        """
        Creates or updates a dictionary based on a reference dictionary.

        Arguments:
        - base_dict (dict, optional): A dictionary that serves as the base.
        - reference_dict (dict, optional): A dictionary whose keys will be used as a template for updating.
        - *args (dict): Additional dictionaries to merge into base_dict.
        - **kwargs: Key-value pairs to be added or updated.

        Returns:
        - A merged dictionary with updated values.
        """

        # Validate or initialize base dictionary
        if base_dict is None:
            base_dict = {}
        elif not isinstance(base_dict, dict):
            raise ValueError("First argument (base_dict) must be a dictionary or None.")
        else:
            base_dict = base_dict.copy()  # Prevent modification of original dictionary

        # Merge reference dictionary into base_dict (if provided)
        if reference_dict:
            if not isinstance(reference_dict, dict):
                raise ValueError("Reference dictionary must be a valid dictionary.")
            base_dict = self._deep_merge(base_dict, reference_dict)

        # Merge dictionaries from *args
        for arg in args:
            if not isinstance(arg, dict):
                raise ValueError("All arguments in *args must be dictionaries.")
            base_dict = self._deep_merge(base_dict, arg)

        # Merge keyword arguments into dictionary
        base_dict.update(kwargs)

        return base_dict

    def _deep_merge(self, dict1, dict2):
        """Recursively merges two dictionaries, preserving nested structures."""
        for key, value in dict2.items():
            # Convert numeric values properly
            if key in dict1:
                dict1[key] = self._convert_type(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def _convert_type(self, existing_value, new_value):
        """Ensures type consistency between old and new values."""
        if isinstance(existing_value, int) and isinstance(new_value, str):
            try:
                return int(new_value)  # Convert string numbers to int
            except ValueError:
                return new_value  # Keep as is if conversion fails
        return new_value

    @keyword("Create New Tuple")
    def py_tuple(self, *args):
        """
        Create a python tuple
        :param args:
        :return:
        """
        return tuple(args)

    @keyword("Check Item In Tuple")
    def check_item_in_tuple(self, pytuple: tuple, item: any) -> bool:
        """
        Check if the passed item in the provided pytuple
        :param pytuple:
        :param item:
        :return:
        """
        if item in pytuple:
            return True
        else:
            return False

    @keyword("Update Item In Tuple")
    def update_tuple(self, pytuple: tuple, item_index: int, new_value: any) -> tuple:
        """
        Change Value In An Exists Tuple
        :param pytuple:
        :param item_index:
        :param new_value:
        :return:
        """
        converted_tuple = list(pytuple)
        converted_tuple[item_index] = new_value
        pytuple = self.py_tuple(*converted_tuple)
        return pytuple

    @keyword("Append To Tuple")
    def append_to_tuple(self, pytuple: tuple, new_value: any) -> tuple:
        """
        Add New Item To An Existing Tuple
        :param pytuple:
        :param new_value:
        :return:
        """
        converted_tuple = list(pytuple)
        converted_tuple.append(new_value)
        pytuple = self.py_tuple(*converted_tuple)
        return pytuple

    @keyword("Count Item Occurrence In Tuple")
    def count_items_in_tuple(self, pytuple: tuple, item: any) -> int:
        """
        Count Item Occurrence In Tuple
        :param pytuple:
        :param item:
        :return:
        """
        return pytuple.count(item)

    @keyword("Remove Item From Tuple")
    def remove_item_from_tuple(self, pytuple: tuple, item: any):
        """
        Remove Item From Tuple
        :param pytuple:
        :param item:
        :return:
        """
        converted_tuple = list(pytuple)
        converted_tuple.remove(item)
        pytuple = self.py_tuple(*converted_tuple)
        return pytuple

    @keyword("Create New Set")
    def py_set(self, *args):
        """
        Create a Python set
        :param args:
        :return:
        """
        return set(args)

    @keyword("Check Item In Set")
    def check_item_in_set(self, pyset: set, item: any) -> bool:
        """
        Check if the passed item is in the provided pyset
        :param pyset:
        :param item:
        :return:
        """
        return item in pyset

    @keyword("Update Item In Set")
    def update_set(self, pyset: set, old_value: any, new_value: any) -> set:
        """
        Change value in an existing set
        :param pyset:
        :param old_value:
        :param new_value:
        :return:
        """
        pyset.discard(old_value)
        pyset.add(new_value)
        return pyset

    @keyword("Add To Set")
    def add_to_set(self, pyset: set, new_value: any) -> set:
        """
        Add new item to an existing set
        :param pyset:
        :param new_value:
        :return:
        """
        pyset.add(new_value)
        return pyset

    @keyword("Remove Item From Set")
    def remove_item_from_set(self, pyset: set, item: any) -> set:
        """
        Remove item from set
        :param pyset:
        :param item:
        :return:
        """
        pyset.discard(item)
        return pyset

    @keyword(name="Create New PyList")
    def create_new_pylist(self, *args):
        """
        Create a Python list from the given arguments.

        :param args: Any number of arguments to be included in the list.
        :return: A Python list containing the provided arguments.
        """
        return list(args)

    @keyword(name="Add To PyList")
    def add_to_pylist(self, pylist_instance: list, *args):
        """
            Adds the provided arguments to a base list or creates a new list if none is provided.

            :param pylist_instance: An existing list to which items will be added (optional).
            :param args: Additional items to be added to the list.
            :return: The updated list with the added items.
            """
        # If no base list is provided, initialize an empty list
        if pylist_instance is None:
            pylist_instance = []

        # Add the provided arguments to the list
        pylist_instance.extend(args)

    @keyword("Clean List")
    def clean_pylist(self, list_instance):
        list_instance.clear()
        return list_instance

    @keyword("Clean Dictionary")
    def clean_pydict(self, dictionary_instance):
        dictionary_instance.clear()
        return dictionary_instance

    @keyword("Convert PyDict To JSON Object")
    def convert_dict_to_json(self, dict_object: dict) -> str:
        json_object = dumps(dict_object)
        return json_object

    @keyword("Convert JSON String Object To PyDict")
    def convert_json_to_dict(self, json_string_object: str) -> dict:
        dict_object = loads(json_string_object)
        return dict_object

    @keyword("Remove Key From Dict List")
    def remove_key_from_dict_list(self, dict_list, key_name):
        """
        Removes a specific key from each dictionary in a list.

        Args:
            dict_list (list): List of dictionaries to process
            key_name (str): Key to remove from each dictionary

        Returns:
            list: New list with dictionaries where the specified key has been removed
        """
        result_list = [ ]

        for item in dict_list:
            # Create a copy to avoid modifying the original dictionary
            item_copy = item.copy()

            # Remove the key if it exists
            if key_name in item_copy:
                item_copy.pop(key_name)

            result_list.append(item_copy)

        return result_list
