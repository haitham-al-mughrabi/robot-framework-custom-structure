from bs4 import BeautifulSoup
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class HtmlParser:
    """
    A utility class for parsing HTML content and extracting text using BeautifulSoup.

    This class provides keywords to extract text from HTML content based on specific HTML tags.
    It is designed to be used in Robot Framework for automated testing and data extraction tasks.
    """

    @keyword("Extract Text From HTML Using Tag")
    def extract_text_from_html(self, html, tag):
        """
        Extracts text from HTML content based on the specified HTML tag.

        This keyword parses the provided HTML content and retrieves all occurrences of the specified tag.
        It then extracts and returns the text content of each matching tag as a list.

        Parameters:
        - html (str): The HTML content from which text will be extracted.
        - tag (str): The HTML tag to search for (e.g., 'div', 'p', 'h1').

        Returns:
        - list: A list of strings, where each string is the text content of a matching tag.

        Example:
        | ${html}=       | <html><div>Hello</div><div>World</div></html> |
        | ${text_list}=  | Extract Text From HTML Using Tag              | ${html} | div |
        | Log            | ${text_list}                                  |
        | # Output:      | ['Hello', 'World']                            |
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all elements with the specified tag
        elements = soup.find_all(tag)

        # Extract and return the text content of each element
        return [element.get_text() for element in elements]
