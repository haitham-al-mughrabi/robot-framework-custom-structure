from robot.api import logger
from tabulate import tabulate
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
import textwrap


@library(doc_format='ROBOT')
class Loggers:
    @keyword(name="Table Logger")
    def table_logger(self, table_title: str, table_contents: dict, table_headers: list = ["Key", "Value"],
                     logging_type: str = 'html', wrap_width: int = 50) -> None:
        """
        Logs a dictionary (including nested keys) as a table, with nested fields as separate columns.
        URLs are excluded from the table.
        """
        # Initialize BuiltIn library
        builtin = BuiltIn()

        # Flatten the dictionary and extract nested fields
        flattened_data, nested_headers = self.flatten_dict_with_nested_fields(table_contents, wrap_width)

        # Prepare the table data
        table = []
        for row in flattened_data:
            table.append(row)

        # Add nested headers to the main headers
        if table_headers is None:
            table_headers = ["Key", "Value"] + nested_headers

        # Generate the console (pretty) table with row lines
        if logging_type in ('all', 'console'):
            console_table = tabulate(table, headers=table_headers, tablefmt="grid")  # Grid format adds row separators
            builtin.log(f"\n[{table_title}]\n" + console_table, console=True)  # Log to console

        # Generate the HTML table with borders
        if logging_type in ('all', 'html'):
            html_table = """
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
            <table>
            """
            html_table += "<tr>" + "".join(f"<th>{header}</th>" for header in table_headers) + "</tr>\n"
            for row in table:
                html_table += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>\n"
            html_table += "</table>"

            # Log the HTML table
            builtin.log(f"\n[{table_title}]\n" + html_table, html=True)  # Log as HTML

    def flatten_dict_with_nested_fields(self, data: dict, wrap_width: int, parent_key: str = '',
                                        sep: str = '.') -> tuple:
        """
        Recursively flattens a nested dictionary and extracts nested fields as separate columns.
        Wraps long text to improve readability.
        """
        flattened = []
        nested_headers = set()

        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key

            # Skip URLs
            if isinstance(value, str) and (value.startswith("http://") or value.startswith("https://")):
                continue

            if isinstance(value, dict):
                # Recursively flatten nested dictionaries
                nested_rows, nested_cols = self.flatten_dict_with_nested_fields(value, wrap_width, new_key, sep)
                flattened.extend(nested_rows)
                nested_headers.update(nested_cols)
            elif isinstance(value, list):
                # Handle lists of dictionaries (e.g., charity_details)
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        nested_rows, nested_cols = self.flatten_dict_with_nested_fields(item, wrap_width,
                                                                                        f"{new_key}[{index}]", sep)
                        flattened.extend(nested_rows)
                        nested_headers.update(nested_cols)
                    else:
                        # Handle non-dictionary items in the list
                        if isinstance(item, str) and (item.startswith("http://") or item.startswith("https://")):
                            continue
                        wrapped_value = self.wrap_text(str(item), wrap_width)
                        flattened.append([new_key, wrapped_value])
            else:
                # Handle non-nested fields
                formatted_key = self.format_key(new_key)
                wrapped_value = self.wrap_text(str(value), wrap_width)
                flattened.append([formatted_key, wrapped_value])

        return flattened, sorted(nested_headers)

    def format_key(self, key: str) -> str:
        """
        Helper function to format the key:
        - Replace underscores with spaces.
        - Capitalize the first letter of each word.
        """
        return ' '.join(word.capitalize() for word in key.replace('_', ' ').split())

    def wrap_text(self, text: str, width: int) -> str:
        """
        Wraps text to a specified width for better table formatting.
        """
        return '\n'.join(textwrap.wrap(text, width))
