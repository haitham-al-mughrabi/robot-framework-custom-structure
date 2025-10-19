import json
import requests
from typing import Dict, Any, Optional, Union
from robot.api import logger
from ResponseWrapper import ResponseWrapper
from robot.api.deco import keyword, library


@library(doc_format = 'ROBOT', auto_keywords=True)
class ResponseHandler:
    """
    Handles response processing, validation, and data extraction.
    """

    def __init__(self, auto_json: bool = True, detailed_response: bool = True, return_json: bool = True):
        """
        Initialize response handler.

        :param auto_json: Automatically parse JSON responses
        :param detailed_response: Return detailed ResponseWrapper objects
        :param return_json: Return JSON for JSON responses
        """
        self.auto_json = auto_json
        self.detailed_response = detailed_response
        self.return_json = return_json
        self._response_cache = {}

    def wrap_response(self, response: Optional[ requests.Response ]) -> Union[
        ResponseWrapper, requests.Response, Dict, None ]:
        """
        Process a response according to settings.

        :param response: Original response object or None
        :return: Processed response based on settings
        """
        if response is None:
            logger.debug("Received None response, returning None")
            return None

        try:
            # Generate a unique identifier for the response object
            response_id = id(response)

            # Store the original response in the cache
            self._response_cache[ response_id ] = response

            # Always keep the original status code
            original_status_code = None
            if hasattr(response, 'status_code'):
                original_status_code = response.status_code

            # Try to parse JSON if return_json is enabled and the response appears to be JSON
            if self.return_json and hasattr(response, 'headers'):
                content_type = response.headers.get('Content-Type', '')
                if content_type and isinstance(content_type, str) and content_type.startswith('application/json'):
                    try:
                        json_data = response.json()

                        # Check if json_data is a dictionary before attempting to modify it
                        if isinstance(json_data, dict):
                            # Safely add status_code directly
                            json_data[ 'status_code' ] = original_status_code

                            # Add metadata
                            json_data[ '__response_metadata' ] = {
                                'id': response_id,
                                'status_code': original_status_code
                            }
                            return json_data
                        elif isinstance(json_data, list):
                            # For lists, wrap in a dict with metadata
                            return {
                                'data': json_data,
                                'status_code': original_status_code,
                                '__response_metadata': {
                                    'id': response_id,
                                    'status_code': original_status_code
                                }
                            }
                        else:
                            # For other types (like strings), wrap similarly
                            return {
                                'data': json_data,
                                'status_code': original_status_code,
                                '__response_metadata': {
                                    'id': response_id,
                                    'status_code': original_status_code
                                }
                            }
                    except (ValueError, json.JSONDecodeError) as e:
                        logger.debug(f"Failed to parse JSON response: {e}")
                        # Continue to ResponseWrapper if JSON parsing fails

            # Fall back to ResponseWrapper if detailed_response is enabled
            if self.detailed_response:
                try:
                    wrapper = ResponseWrapper(response, self.auto_json)
                    wrapper._response_id = response_id  # Add the ID to the wrapper
                    return wrapper
                except Exception as e:
                    logger.warn(f"Failed to create ResponseWrapper: {e}")
                    # Return original response if wrapper creation fails
                    return response
            else:
                return response
        except Exception as e:
            logger.error(f"Error in wrap_response: {e}")
            # In case of any error, return the original response
            return response

    def extract_json(self, response: Any, json_path: Optional[str] = None, default: Any = None) -> Any:
        """
        Extract JSON data or a specific value from a response.

        :param response: Response object or ResponseWrapper
        :param json_path: Optional dot-notation path to extract
        :param default: Default value to return if path not found
        :return: The JSON data or extracted value
        """
        # Convert to ResponseWrapper if it's a regular response
        if hasattr(response, 'json') and callable(response.json) and not isinstance(response, ResponseWrapper):
            wrapped_response = ResponseWrapper(response, self.auto_json)
        elif isinstance(response, ResponseWrapper):
            wrapped_response = response
        else:
            logger.warn("Cannot extract JSON from invalid response object")
            return default

        # Extract JSON data
        if json_path:
            return wrapped_response.get_json_value(json_path, default)
        else:
            return wrapped_response.json() or default

    def get_status_code(self, response: Any) -> Optional[ int ]:
        """
        Get the status code from a response object safely.

        :param response: Response object, ResponseWrapper, processed response, or JSON
        :return: Status code or None if not available
        """
        # Handle None responses
        if response is None:
            return None

        try:
            # Case 1: Direct status_code attribute
            if hasattr(response, 'status_code'):
                return response.status_code

            # Case 2: JSON dictionary with status_code as direct property
            if isinstance(response, dict) and 'status_code' in response:
                return response[ 'status_code' ]

            # Case 3: Dictionary with metadata (from JSON response)
            if isinstance(response, dict) and '__response_metadata' in response:
                return response[ '__response_metadata' ].get('status_code')

            # Case 4: ResponseWrapper or object with _response_id
            if hasattr(response, '_response_id') and response._response_id in self._response_cache:
                original_response = self._response_cache[ response._response_id ]
                if hasattr(original_response, 'status_code'):
                    return original_response.status_code

            # Case 5: Try to find the response in the cache by id
            if isinstance(response, (dict, list)) and id(response) in self._response_cache:
                original_response = self._response_cache[ id(response) ]
                if hasattr(original_response, 'status_code'):
                    return original_response.status_code

            # If none of the above work, log a warning and return None
            logger.debug(f"Cannot get status code from response object type: {type(response)}")
            return None

        except Exception as e:
            # Catch any exceptions to ensure the method never fails
            logger.error(f"Error getting status code: {e}")
            return None

    def get_headers(self, response: Any, header_name: Optional[str] = None) -> Optional[Union[Dict, str]]:
        """
        Get headers from a response object.

        :param response: Response object or ResponseWrapper
        :param header_name: Optional header name to filter
        :return: Headers dictionary, specific header value, or None
        """
        # Get headers from the response
        if isinstance(response, ResponseWrapper):
            headers = response.headers
        elif hasattr(response, 'headers'):
            headers = response.headers
        else:
            logger.warn("Cannot get headers from invalid response object")
            return None

        # Return specific header if requested
        if header_name and headers:
            # Case-insensitive header lookup
            for key, value in headers.items():
                if key.lower() == header_name.lower():
                    return value
            return None

        return headers

    def check_success(self, response: Any) -> bool:
        """
        Check if a response indicates success (status code < 400).

        :param response: Response object or ResponseWrapper
        :return: True if successful, False otherwise
        """
        if isinstance(response, ResponseWrapper):
            return response.ok
        elif hasattr(response, 'status_code'):
            return response.status_code < 400
        else:
            logger.warn("Cannot check success for invalid response object")
            return False

    def get_cookies(self, response: Any, cookie_name: Optional[str] = None) -> Optional[Union[Dict, str]]:
        """
        Get cookies from a response object.

        :param response: Response object or ResponseWrapper
        :param cookie_name: Optional cookie name to filter
        :return: Cookies dictionary, specific cookie value, or None
        """
        # Get cookies from the response
        if isinstance(response, ResponseWrapper):
            cookies = response.cookies
        elif hasattr(response, 'cookies') and hasattr(response.cookies, 'get_dict'):
            cookies = response.cookies.get_dict()
        else:
            logger.warn("Cannot get cookies from invalid response object")
            return None

        # Return specific cookie if requested
        if cookie_name and cookies:
            return cookies.get(cookie_name)

        return cookies

    def validate_response(self, response: Any, schema: Dict) -> bool:
        """
        Simple validation that checks if response is valid JSON.

        :param response: Response object or ResponseWrapper
        :param schema: JSON schema to validate against (not used)
        :return: True if valid JSON response, False otherwise
        """
        try:
            # Extract JSON from response
            if isinstance(response, ResponseWrapper):
                response_json = response.json()
            elif hasattr(response, 'json') and callable(response.json):
                response_json = response.json()
            elif isinstance(response, dict):
                response_json = response  # Assume response is already parsed JSON
            else:
                logger.error("Invalid response object for validation")
                return False

            # If we successfully got JSON data, return True
            return True
        except (ValueError, json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Could not parse response as JSON: {e}")
            return False

    def get_content_type(self, response: Any) -> Optional[str]:
        """
        Get the Content-Type header from a response.

        :param response: Response object or ResponseWrapper
        :return: Content-Type string or None if not available
        """
        return self.get_headers(response, 'content-type')

    def get_content(self, response: Any, as_text: bool = True) -> Optional[Union[str, bytes]]:
        """
        Get the content from a response.

        :param response: Response object or ResponseWrapper
        :param as_text: If True, decode content as text
        :return: Response content as text or bytes, or None
        """
        if isinstance(response, ResponseWrapper):
            if as_text:
                return response.text
            return response.content
        elif hasattr(response, 'content'):
            if as_text and hasattr(response, 'text'):
                return response.text
            return response.content
        else:
            logger.warn("Cannot get content from invalid response object")
            return None

    def get_elapsed_time(self, response: Any) -> Optional[float]:
        """
        Get the elapsed time of a request in seconds.

        :param response: Response object or ResponseWrapper
        :return: Elapsed time in seconds or None
        """
        if isinstance(response, ResponseWrapper):
            return response.elapsed
        elif hasattr(response, 'elapsed') and hasattr(response.elapsed, 'total_seconds'):
            return response.elapsed.total_seconds()
        else:
            logger.warn("Cannot get elapsed time from invalid response object")
            return None
