import re
from urllib.parse import quote, unquote, urlparse, urljoin
from robot.api import logger
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class URLHandler:
    @keyword("Encode URL")
    def encode_url(self, url):
        """
        Encodes a URL by replacing special characters with their percent-encoded equivalents.

        Args:
            url (str): The URL to encode.

        Returns:
            str: The encoded URL.
        """
        encoded_url = quote(url)
        logger.info(f"Encoded URL '{url}': {encoded_url}")
        return encoded_url

    @keyword("Decode URL")
    def decode_url(self, url):
        """
        Decodes a URL by converting percent-encoded characters back to their original form.

        Args:
            url (str): The URL to decode.

        Returns:
            str: The decoded URL.
        """
        decoded_url = unquote(url)
        logger.info(f"Decoded URL '{url}': {decoded_url}")
        return decoded_url

    @keyword("Get URL Components")
    def get_url_components(self, url):
        """
        Extracts and returns the components of a URL (scheme, netloc, path, params, query, fragment).

        Args:
            url (str): The URL to parse.

        Returns:
            dict: A dictionary containing the URL components.
        """
        parsed_url = urlparse(url)
        components = {
            "scheme": parsed_url.scheme,
            "netloc": parsed_url.netloc,
            "path": parsed_url.path,
            "params": parsed_url.params,
            "query": parsed_url.query,
            "fragment": parsed_url.fragment
        }
        logger.info(f"Extracted components from URL '{url}': {components}")
        return components

    @keyword("Join URLs")
    def join_urls(self, base_url, relative_url):
        """
        Joins a base URL and a relative URL into a single absolute URL.

        Args:
            base_url (str): The base URL.
            relative_url (str): The relative URL.

        Returns:
            str: The joined absolute URL.
        """
        joined_url = urljoin(base_url, relative_url)
        logger.info(f"Joined URLs '{base_url}' and '{relative_url}': {joined_url}")
        return joined_url

    @keyword("Validate URL")
    def validate_url(self, url):
        """
        Validates if a string is a properly formatted URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, otherwise False.
        """
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # Scheme
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # Domain
            r"localhost|"  # Localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # IPv4
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # IPv6
            r"(?::\d+)?"  # Port
            r"(?:/?|[/?]\S+)$", re.IGNORECASE
        )
        is_valid = bool(regex.match(url))
        logger.info(f"Validated URL '{url}': {is_valid}")
        return is_valid
