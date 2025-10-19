import uuid
from urllib.parse import urlparse, urlunparse
from typing import Dict, Any, Optional, Union, Tuple, List
from robot.api import logger
from robot.api.deco import keyword, library


@library(doc_format = 'ROBOT', auto_keywords=True)
class RequestUtils:
    """
    Utility functions for request processing.
    """

    def extract_request_params(self, method: Optional[ str ] = None, alias: Optional[ str ] = None,
                               endpoint: Optional[ str ] = None, url: Optional[ str ] = None,
                               **kwargs) -> Tuple:
        """
        Extract and normalize request parameters from kwargs.

        :return: Tuple of (method, alias, endpoint, url, control_params, request_kwargs)
        """
        # Copy kwargs to avoid modifying the original
        control_params = { }
        request_kwargs = { }

        # Safely copy kwargs to request_kwargs
        for key, value in kwargs.items():
            request_kwargs[ key ] = value

        # Extract method
        if method is None:
            for key in [ 'method', 'Method', 'METHOD' ]:
                if key in request_kwargs:
                    method = request_kwargs.pop(key)
                    break

        # Extract alias
        if alias is None and 'alias' in request_kwargs:
            alias = request_kwargs.pop('alias')

        # Extract endpoint
        if endpoint is None and 'endpoint' in request_kwargs:
            endpoint = request_kwargs.pop('endpoint')

        # Extract URL
        if url is None:
            for key in [ 'url', 'Url', 'URL', 'uri', 'Uri', 'URI' ]:
                if key in request_kwargs:
                    url = request_kwargs.pop(key)
                    break

        # Extract token safely
        token = None
        for key in [ 'token', 'Token', 'TOKEN', 'auth_token', 'access_token', 'bearerToken' ]:
            if key in request_kwargs:
                token = request_kwargs.pop(key)
                break

        # Extract control parameters safely (not for HTTP request)
        control_params[ 'max_retries' ] = request_kwargs.pop('max_retries', 3)
        control_params[ 'delay' ] = request_kwargs.pop('delay', 2)
        control_params[ 'token_check_on_failure' ] = request_kwargs.pop('token_check_on_failure', True)
        control_params[ 'auto_refresh' ] = request_kwargs.pop('auto_refresh', True)
        control_params[ 'random_session' ] = request_kwargs.pop('random_session', False)

        # Safely handle custom_headers
        custom_headers = request_kwargs.pop('custom_headers', None)
        if custom_headers is not None and isinstance(custom_headers, dict):
            control_params[ 'custom_headers' ] = custom_headers
        else:
            control_params[ 'custom_headers' ] = None

        control_params[ 'token_type' ] = request_kwargs.pop('token_type', 'Bearer')

        # Store token in control_params if found
        if token:
            control_params[ 'token' ] = token

        # Handle expected_status separately and safely
        if 'expected_status' in request_kwargs:
            try:
                control_params[ 'expected_status' ] = self.extract_expected_status(request_kwargs)
            except Exception as e:
                logger.error(f"Error extracting expected_status: {e}")
                control_params[ 'expected_status' ] = None

        return method, alias, endpoint, url, control_params, request_kwargs

    def extract_expected_status(self, kwargs: Dict) -> Union[ int, List[ int ], None ]:
        """
        Extract and process expected_status parameter from kwargs.

        :param kwargs: Keyword arguments dict
        :return: Processed expected_status value or None
        """
        expected_status = kwargs.pop('expected_status', None)

        # Convert to int or list of ints if needed
        if isinstance(expected_status, str):
            if ',' in expected_status:
                expected_status = [ int(s.strip()) for s in expected_status.split(',') ]
            else:
                try:
                    expected_status = int(expected_status)
                except ValueError:
                    logger.warn(f"Could not convert expected_status '{expected_status}' to integer")

        return expected_status

    def parse_url(self, url: str) -> Tuple[ str, str ]:
        """
        Parse a URL to extract base URL and endpoint.

        :param url: Full URL
        :return: Tuple of (base_url, endpoint)
        """
        try:
            # Special case for URLs without protocol
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            parsed = urlparse(url)

            # Construct the base URL (scheme + netloc)
            base_url = urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))

            # Get the path component for the endpoint
            endpoint = parsed.path or '/'

            # Include query string in endpoint if present
            if parsed.query:
                endpoint = f"{endpoint}?{parsed.query}"

            # Include fragment in endpoint if present
            if parsed.fragment:
                endpoint = f"{endpoint}#{parsed.fragment}"

            return base_url, endpoint
        except Exception as e:
            logger.error(f"Error parsing URL '{url}': {e}")
            # Fallback URL parsing
            if '//' in url:
                parts = url.split('//')
                if '/' in parts[ 1 ]:
                    base_domain = parts[ 1 ].split('/', 1)[ 0 ]
                    base_url = f"{parts[ 0 ]}//{base_domain}"
                    endpoint = url[ len(base_url): ] or '/'
                    return base_url, endpoint

            return url, "/"

    def generate_id(self) -> str:
        """
        Generate a random ID for temporary sessions.

        :return: A short random ID string
        """
        return uuid.uuid4().hex[ :8 ]

    def merge_headers(self, *headers_dicts: Dict) -> Dict:
        """
        Merge multiple header dictionaries into one.

        :param headers_dicts: Variable number of header dictionaries
        :return: Merged headers dictionary
        """
        merged = { }
        for headers in headers_dicts:
            if headers:
                merged.update(headers)
        return merged

    def filter_session_params(self, kwargs: Dict) -> Dict:
        """
        Filter parameters that are specific to session creation.

        :param kwargs: All keyword arguments
        :return: Dictionary with only session-specific parameters
        """
        session_params = { }
        session_keys = ('auth', 'verify', 'cert', 'proxies', 'timeout')

        for key, value in kwargs.items():
            if key in session_keys:
                session_params[ key ] = value

        return session_params

    def is_json_content_type(self, content_type: str) -> bool:
        """
        Check if the content type indicates JSON.

        :param content_type: Content-Type header value
        :return: True if JSON content type, False otherwise
        """
        if not content_type:
            return False
        return content_type.lower().startswith('application/json')

    def normalize_method(self, method: str) -> str:
        """
        Normalize HTTP method to uppercase.

        :param method: HTTP method string
        :return: Normalized method string
        """
        return method.upper() if method else None

    def validate_required_params(self, **params) -> List[ str ]:
        """
        Validate that required parameters are present.

        :param params: Dictionary of parameters to check
        :return: List of missing parameter names
        """
        missing = [ ]
        for name, value in params.items():
            if value is None:
                missing.append(name)
        return missing
