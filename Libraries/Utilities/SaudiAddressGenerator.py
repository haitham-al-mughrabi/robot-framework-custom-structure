import random
from robot.api.deco import keyword, library
from Libraries.Variables.Address import *


@library(doc_format = 'ROBOT')
class SaudiAddressGenerator:
    """
    A class to generate realistic Arabic addresses across Saudi Arabia.
    Includes methods for generating addresses organized by administrative areas (provinces),
    cities, neighborhoods, street names, building numbers and postal codes.
    """

    def __init__(self):
        """
        Initialize the data for Saudi Arabian administrative areas, cities,
        neighborhoods, streets, and postal codes in Arabic.
        """
        # Administrative areas (provinces) in Saudi Arabia with Arabic names
        self.administrative_areas = administrative_areas

        # Major cities by administrative area - UPDATED with new data
        self.cities_by_area = cities_by_area

        # General neighborhoods for cities not explicitly listed
        self.general_neighborhoods = general_neighborhoods

        # Postal code information by region
        self.postal_code_by_region = postal_code_by_region

        # Default postal code range for regions not explicitly listed
        self.default_postal_range = default_postal_range

        # Arabic building number formats
        self.building_formats = building_formats

        self.neighborhoods_by_city = neighborhoods_by_city

        self.general_streets = general_streets

        self.streets_by_city = streets_by_city

    @keyword('Get Administrative Areas')
    def get_administrative_areas(self):
        """
        Get the list of available administrative areas in Saudi Arabia.

        Returns:
            list: List of Saudi administrative areas
        """
        return list(self.administrative_areas.keys())

    @keyword('Select Random Administrative Area')
    def select_random_administrative_area(self):
        """
        Select a random administrative area.

        Returns:
            str: An administrative area name in Arabic
        """
        return random.choice(list(self.administrative_areas.keys()))

    @keyword('Get Cities In Area')
    def get_cities_in_area(self, area = None):
        """
        Get cities in a specific administrative area.

        Args:
            area (str, optional): The administrative area name in Arabic

        Returns:
            list: List of cities in the specified area
        """
        if area is None:
            area = self.select_random_administrative_area()

        return self.cities_by_area.get(area, [ ])

    @keyword('Select Random City')
    def select_random_city(self, area = None):
        """
        Select a random city from an administrative area, or from all cities if area is None.

        Args:
            area (str, optional): The administrative area name in Arabic

        Returns:
            str: A city name in Arabic
        """
        if area is None:
            area = self.select_random_administrative_area()

        cities = self.get_cities_in_area(area)
        if not cities:
            # Default to a major city if no cities found in the area
            cities = self.cities_by_area[ "منطقة الرياض" ]

        return random.choice(cities)

    @keyword('Generate Street Name')
    def generate_street_name(self, city = None, area = None):
        """
        Generate a random street name for a given city, or a random city if none specified.

        Args:
            city (str, optional): The city in Arabic to generate a street name for
            area (str, optional): The administrative area in Arabic (used if city is None)

        Returns:
            str: A street name in Arabic
        """
        if city is None:
            city = self.select_random_city(area)

        if city in self.streets_by_city:
            return random.choice(self.streets_by_city[ city ])
        else:
            # For cities without specific street lists, use general streets
            return random.choice(self.general_streets)

    @keyword('Generate Neighborhood Name')
    def generate_neighborhood_name(self, city = None, area = None):
        """
        Generate a random neighborhood name for a given city, or a random city if none specified.

        Args:
            city (str, optional): The city in Arabic to generate a neighborhood name for
            area (str, optional): The administrative area in Arabic (used if city is None)

        Returns:
            str: A neighborhood name in Arabic
        """
        if city is None:
            city = self.select_random_city(area)

        if city in self.neighborhoods_by_city:
            return random.choice(self.neighborhoods_by_city[ city ])
        else:
            # For cities without specific neighborhood lists, use general neighborhoods
            return random.choice(self.general_neighborhoods)

    @keyword('Generate Building Number')
    def generate_building_number(self):
        """
        Generate a realistic building number in Arabic format.

        Returns:
            str: A building number in Arabic format
        """
        number = random.randint(1, 9999)

        # Different formats of building numbers
        format_type = random.choice(self.building_formats)

        if "{letter}" in format_type:
            letter = random.choice([ 'أ', 'ب', 'ج', 'د' ])
            return format_type.format(number = number, letter = letter)
        elif "{unit}" in format_type:
            unit = random.randint(1, 20)
            return format_type.format(number = number, unit = unit)
        else:
            return format_type.format(number = number)

    @keyword('Generate Postal Code')
    def generate_postal_code(self, area = None):
        """
        Generate a realistic postal code for a given administrative area, or a random area if none specified.

        Args:
            area (str, optional): The administrative area in Arabic to generate a postal code for

        Returns:
            str: A 5-digit postal code
        """
        if area is None:
            area = self.select_random_administrative_area()

        if area in self.postal_code_by_region:
            min_code, max_code = self.postal_code_by_region[ area ]
            return str(random.randint(min_code, max_code))
        else:
            min_code, max_code = self.default_postal_range
            return str(random.randint(min_code, max_code))

    @keyword('Get Area For City')
    def get_area_for_city(self, city):
        """
        Find which administrative area a city belongs to.

        Args:
            city (str): City name in Arabic

        Returns:
            str: Administrative area name in Arabic, or None if not found
        """
        for area, cities in self.cities_by_area.items():
            if city in cities:
                return area
        return None

    @keyword('Generate Complete Address')
    def generate_complete_address(self, city = None, area = None):
        """
        Generate a complete address in Saudi Arabia.

        Args:
            city (str, optional): The city for the address in Arabic
            area (str, optional): The administrative area in Arabic (used if city is None)

        Returns:
            dict: A dictionary containing all address components in Arabic
        """
        if area is None and city is not None:
            area = self.get_area_for_city(city)

        if area is None:
            area = self.select_random_administrative_area()

        if city is None:
            city = self.select_random_city(area)

        address = {
            "building_number": self.generate_building_number(),
            "street_name": self.generate_street_name(city, area),
            "neighborhood_name": self.generate_neighborhood_name(city, area),
            "postal_code": self.generate_postal_code(area),
            "city": city,
            "area": area,
            "country": "المملكة العربية السعودية"
        }

        return address

    @keyword('Format Address')
    def format_address(self, address_dict = None, city = None, area = None):
        """
        Format an address dictionary as a readable string in Arabic.

        Args:
            address_dict (dict, optional): Address dictionary. If None, generates a new address.
            city (str, optional): City for the new address (in Arabic) if address_dict is None
            area (str, optional): Administrative area (in Arabic) if address_dict is None

        Returns:
            str: Formatted address string in Arabic
        """
        if address_dict is None:
            address_dict = self.generate_complete_address(city, area)

        formatted_address = (
            f"{address_dict[ 'building_number' ]}، "
            f"{address_dict[ 'street_name' ]}، "
            f"حي {address_dict[ 'neighborhood_name' ]}، "
            f"{address_dict[ 'city' ]} {address_dict[ 'postal_code' ]}، "
            f"{address_dict[ 'area' ]}، "
            f"{address_dict[ 'country' ]}"
        )

        return formatted_address

    @keyword('Generate Addresses')
    def generate_addresses(self, count = 1, city = None, area = None):
        """
        Generate multiple addresses.

        Args:
            count (int): Number of addresses to generate
            city (str, optional): City for all addresses in Arabic, or random if None
            area (str, optional): Administrative area in Arabic, or random if None

        Returns:
            list: List of formatted address strings in Arabic
        """
        addresses = [ ]
        for _ in range(count):
            address = self.generate_complete_address(city, area)
            formatted = self.format_address(address)
            addresses.append(formatted)

        return addresses

    @keyword('Get Random Area With Details')
    def get_random_area_with_details(self):
        """
        Generate information about a random neighborhood area with all associated details.

        Returns:
            dict: A dictionary containing all details about a random neighborhood area including:
                - administrative_area: The province/region in Arabic
                - administrative_area_en: The province/region in English
                - city: The city in Arabic
                - neighborhood: The neighborhood name in Arabic
                - street: A random street in the neighborhood
                - postal_code: The postal code for the area
                - sample_building: A sample building number in the area
                - sample_address: A complete formatted address
        """
        # Select a random administrative area
        admin_area = self.select_random_administrative_area()
        admin_area_en = self.administrative_areas[ admin_area ]

        # Select a random city in that area
        city = self.select_random_city(admin_area)

        # Get a random neighborhood in that city
        neighborhood = self.generate_neighborhood_name(city, admin_area)

        # Get a random street in that city
        street = self.generate_street_name(city, admin_area)

        # Get the postal code for the area
        postal_code = self.generate_postal_code(admin_area)

        # Generate a sample building number
        building = self.generate_building_number()

        # Generate a sample complete address
        address_dict = {
            "building_number": building,
            "street_name": street,
            "neighborhood_name": neighborhood,
            "postal_code": postal_code,
            "city": city,
            "area": admin_area,
            "country": "المملكة العربية السعودية"
        }

        formatted_address = self.format_address(address_dict)

        # Compile all details into a comprehensive dictionary
        details = {
            "administrative_area": admin_area,
            "administrative_area_en": admin_area_en,
            "city": city,
            "neighborhood": neighborhood,
            "street": street,
            "postal_code": postal_code,
            "sample_building": building,
            "sample_address": formatted_address
        }

        return details
