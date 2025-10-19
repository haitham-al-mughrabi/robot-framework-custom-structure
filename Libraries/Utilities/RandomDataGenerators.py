import random
from robot.api.deco import keyword, library
from Libraries.Utilities.Generators import Generators


@library(doc_format='ROBOT')
class RandomDataGenerators:
    """
    Keywords for generating random data to support test automation.
    """

    def __init__(self):
        self.generators = Generators()

    @keyword("Generate Random Number With Specified Range")
    def generate_random_number_with_specified_range(self, range_min=0, range_max=100000,
                                                    number_of_digits=None, output_type="int", prefix=None):
        """Generate Random Number. It can be in specified range,
        selected returned type, and prefixed on demand.
        """
        number = self.generators.generate_random_py_number(
            range_min=range_min,
            range_max=range_max,
            number_of_digits=number_of_digits,
            output_type=output_type,
            prefix=prefix
        )
        return number

    @keyword("Get Random Item From List")
    def get_random_item_from_list(self, my_list):
        """Returns a random item from the given list. If the list is empty, returns ${EMPTY}."""
        if not my_list or len(my_list) == 0:
            return ""
        else:
            return random.choice(my_list)

    @keyword("Get Random Item From List & Remove The Item From List")
    def get_random_item_from_list_and_remove_the_item_from_list(self, my_list):
        """Get Random Item From List and remove it from the list"""
        random_index = random.randint(0, len(my_list) - 1)
        random_item = my_list.pop(random_index)
        return random_item

    @keyword("Generate Random Boolean Value")
    def generate_random_boolean_value(self):
        """Generate Random Boolean Value"""
        random_boolean_value = random.choice([True, False])
        return random_boolean_value

    @keyword("Select Random Element From Dictionary")
    def select_random_element_from_dictionary(self, dictionary):
        """Returns a random key from the provided dictionary"""
        random_key = random.choice(list(dictionary.keys()))
        return random_key

    @keyword("Generate Random Number Less Than Max Value")
    def generate_random_number_less_than_max_value(self, min_value, max_value):
        """Generate Random Number Less Than Max Value"""
        random_number = random.randint(int(min_value), int(max_value) - 1)
        return random_number

    @keyword("Get Multiple Random Items From List")
    def get_multiple_random_items_from_list(self, my_list, count=1):
        """Returns multiple random items from the given list.

        If count is greater than list length, returns the entire list shuffled.
        If the list is empty, returns an empty list.
        """
        if len(my_list) == 0:
            return []

        count = min(int(count), len(my_list))
        # Create a copy to avoid modifying the original list
        list_copy = my_list.copy()
        random.shuffle(list_copy)
        return list_copy[:count]

    @keyword("Get Random Value From Dictionary")
    def get_random_value_from_dictionary(self, dictionary):
        """Returns a random value from the provided dictionary.

        If the dictionary is empty, returns an empty string.
        """
        if not dictionary:
            return ""

        random_key = random.choice(list(dictionary.keys()))
        return dictionary[random_key]

    @keyword("Get Random Key Value Pair From Dictionary")
    def get_random_key_value_pair_from_dictionary(self, dictionary):
        """Returns a random key-value pair from the provided dictionary.

        Returns a list containing [key, value]
        If the dictionary is empty, returns an empty list.
        """
        if not dictionary:
            return []

        random_key = random.choice(list(dictionary.keys()))
        return [random_key, dictionary[random_key]]

    @keyword("Shuffle List")
    def shuffle_list(self, my_list):
        """Returns a shuffled copy of the given list.

        The original list remains unchanged.
        """
        shuffled_list = my_list.copy()
        random.shuffle(shuffled_list)
        return shuffled_list

    @keyword("Get Random Subset Of Dictionary")
    def get_random_subset_of_dictionary(self, dictionary, count=1):
        """Returns a random subset of the provided dictionary.

        If count is greater than dictionary size, returns entire dictionary.
        If the dictionary is empty, returns an empty dictionary.
        """
        if not dictionary:
            return {}

        count = min(int(count), len(dictionary))
        keys = random.sample(list(dictionary.keys()), count)
        return {k: dictionary[k] for k in keys}
