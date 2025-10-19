import time
import requests
import json
from typing import Dict, Any, Optional, Union, Callable, List
from robot.api import logger
from robot.api.deco import keyword, library
from SessionManager import SessionManager
from TokenManager import TokenManager
from ResponseHandler import ResponseHandler
from RequestUtils import RequestUtils


@library(doc_format = 'ROBOT', auto_keywords=True)
class RequestSender:
    """
    Handles all request sending operations including retries, token management, and waiting strategies.
    """

    def __init__(self, session_manager: SessionManager, token_manager: TokenManager,
                 response_handler: ResponseHandler, auto_log: bool = True, global_timeout: int = 30):
        """
        Initialize request sender.

        :param session_manager: SessionManager instance
        :param token_manager: TokenManager instance
        :param response_handler: ResponseHandler instance
        :param auto_log: Whether to automatically log requests
        :param global_timeout: Default timeout for requests
        """
        self.session_manager = session_manager
        self.token_manager = token_manager
        self.response_handler = response_handler
        self.utils = RequestUtils()
        self.auto_log = auto_log
        self.global_timeout = global_timeout

    def send_request(self, method: Optional[ str ] = None, alias: Optional[ str ] = None,
                     endpoint: Optional[ str ] = None, url: Optional[ str ] = None, **kwargs) -> Any:
        """
        Unified method for sending API requests with comprehensive options.

        :param method: HTTP method (GET, POST, etc.)
        :param alias: The session alias (optional)
        :param endpoint: API endpoint (relative to base URL)
        :param url: Full URL for the request (when not using session)
        :param kwargs: Additional request parameters including:
            - max_retries: Maximum number of retries
            - delay: Time between retries
            - token: Authentication token
            - token_type: Type of token (default: Bearer)
            - token_check_on_failure: Whether to check/refresh token on failure
            - custom_headers: Headers for this request only
            - random_session: Create a random session if alias not provided
            - expected_status: Expected HTTP status code(s)
        :return: Response object or None if failed
        """
        # Extract parameters
        method, alias, endpoint, url, control_params, request_kwargs = self.utils.extract_request_params(
            method, alias, endpoint, url, **kwargs)

        # Handle session creation if needed
        if not alias and not url:
            logger.error("Either alias or URL must be provided")
            return self.response_handler.wrap_response(None)

        # Create random session if requested
        if not alias and control_params.get('random_session', False):
            if not url:
                logger.error("URL is required for random session creation")
                return self.response_handler.wrap_response(None)

            # Parse URL to get base URL
            base_url, path = self.utils.parse_url(url)
            headers = request_kwargs.get('headers', { })

            # Add token to headers if provided
            if control_params.get('token'):
                token_type = control_params.get('token_type', 'Bearer')
                headers[ 'Authorization' ] = f"{token_type} {control_params[ 'token' ]}"
                request_kwargs[ 'headers' ] = headers

            alias = self.session_manager.create_random_session(base_url, headers)
            endpoint = path

        # Handle custom headers without creating a new session
        elif alias and control_params.get('custom_headers'):
            return self._send_with_custom_headers(method, alias, endpoint,
                                                  control_params[ 'custom_headers' ], **request_kwargs)

        # Handle retry strategy
        max_retries = control_params.get('max_retries', 1)
        delay = control_params.get('delay', 2)

        if max_retries > 1:
            return self._send_with_retries(method, alias, endpoint, url, max_retries, delay,
                                           control_params, request_kwargs)

        # Simple single request
        if alias:
            # Check token validity if configured
            if control_params.get('token_check_on_failure', False):
                return self._send_with_token_check(method, alias, endpoint, control_params, request_kwargs)
            return self._send_session_request(method, alias, endpoint, **request_kwargs)
        else:
            return self._send_direct_request(method, url, **request_kwargs)

    def _send_session_request(self, method: str, alias: str, endpoint: str, **kwargs) -> Any:
        """Send a request through an existing session."""
        if not self.session_manager.session_exists(alias):
            logger.warn(f"Session '{alias}' not found!")
            return self.response_handler.wrap_response(None)

        # Apply global timeout if not specified
        if 'timeout' not in kwargs:
            kwargs[ 'timeout' ] = self.global_timeout

        try:
            # Get the method function from RequestsLibrary
            requests_lib = self.session_manager.requests_lib
            method_func = getattr(requests_lib, f"{method.lower()}_request")
            response = method_func(alias, endpoint, **kwargs)

            if self.auto_log:
                self._log_api_request(alias, method, endpoint, response)

            return self.response_handler.wrap_response(response)
        except Exception as e:
            logger.error(f"❌ REQUEST FAILED: {e}")
            logger.error(f"   - Session: {alias}")
            logger.error(f"   - Method: {method}")
            logger.error(f"   - Endpoint: {endpoint}")
            return self.response_handler.wrap_response(None)

    def _send_direct_request(self, method: str, url: str, **kwargs) -> Any:
        """Send a request directly without a session."""
        try:
            # Apply global timeout if not specified
            if 'timeout' not in kwargs:
                kwargs[ 'timeout' ] = self.global_timeout

            response = requests.request(method.upper(), url, **kwargs)

            if self.auto_log:
                self._log_api_request("DIRECT", method, url, response)

            return self.response_handler.wrap_response(response)
        except Exception as e:
            logger.error(f"❌ DIRECT REQUEST FAILED: {e}")
            logger.error(f"   - Method: {method}")
            logger.error(f"   - URL: {url}")
            return self.response_handler.wrap_response(None)

    def _send_with_retries(self, method: str, alias: Optional[ str ], endpoint: Optional[ str ],
                           url: Optional[ str ], max_retries: int, delay: float,
                           control_params: Dict, request_kwargs: Dict) -> Any:
        """Send a request with retry logic."""
        expected_status = control_params.get('expected_status')
        request_url = url if url else f"{self.session_manager.get_session_url(alias)}{endpoint}"
        last_response = None

        for attempt in range(max_retries):
            # Send the request
            if alias:
                response = self._send_session_request(method, alias, endpoint, **request_kwargs)
            else:
                response = self._send_direct_request(method, url, **request_kwargs)

            # Store the response for later use (even if None)
            last_response = response

            # Check if we got a valid response
            status_code = None
            if response is not None:
                status_code = self.response_handler.get_status_code(response)

            # If no response or no status code, log and retry
            if response is None or status_code is None:
                logger.warn(f"Retry {attempt + 1}/{max_retries} - No valid response received")
                logger.warn(f"  - URL: {request_url}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                continue

            # If no expected status specified, any valid response is successful
            if expected_status is None:
                return response

            # Check if status matches expected
            is_success = False
            if isinstance(expected_status, list):
                is_success = status_code in expected_status
            else:
                is_success = status_code == expected_status

            if is_success:
                return response

            # Status didn't match expected
            logger.warn(f"Retry {attempt + 1}/{max_retries} - Status check failed")
            logger.warn(f"  - Expected status: {expected_status}")
            logger.warn(f"  - Received status: {status_code}")
            logger.warn(f"  - URL: {request_url}")

            # Wait before next retry (if not the last attempt)
            if attempt < max_retries - 1:
                time.sleep(delay)

        # All retries failed - check if token refresh might help
        if alias and control_params.get('token_check_on_failure', False) and last_response is not None:
            status_code = self.response_handler.get_status_code(last_response)
            # Only attempt token refresh if we have a status code and it's 401 or 403
            if status_code in (401, 403):
                logger.info("Attempting token refresh after failed retries")
                if self._handle_token_refresh(alias, control_params):
                    # One final attempt with refreshed token
                    logger.info("Token refreshed, making final attempt")
                    return self._send_session_request(method, alias, endpoint, **request_kwargs)

        logger.error(f"❌ REQUEST FAILED after {max_retries} retries")
        logger.error(f"   - Method: {method}")
        logger.error(f"   - URL: {request_url}")

        # Return the last response we got, even if it didn't meet expectations
        return last_response

    def _send_with_token_check(self, method: str, alias: str, endpoint: str,
                               control_params: Dict, request_kwargs: Dict) -> Any:
        """Send a request with token validation."""
        # Check token validity
        headers = self.session_manager.get_session_headers(alias)
        token_valid = self.token_manager.validate_token(headers)

        if not token_valid:
            if not self._handle_token_refresh(alias, control_params):
                logger.warn(f"Token is expired for session '{alias}' and refresh failed")
                return self.response_handler.wrap_response(None)

        return self._send_session_request(method, alias, endpoint, **request_kwargs)

    def _send_with_custom_headers(self, method: str, alias: str, endpoint: str,
                                  custom_headers: Dict, **kwargs) -> Any:
        """Send a request with custom headers without modifying the original session."""
        # Create a temporary session with custom headers
        temp_alias = f"temp_{alias}_{self.utils.generate_id()}"
        original_details = self.session_manager.get_session_details(alias)

        if not original_details:
            return self.response_handler.wrap_response(None)

        self.session_manager.create_session(
            temp_alias,
            original_details[ "url" ],
            headers = custom_headers,
            **original_details.get("kwargs", { })
        )

        # Send the request using the temporary session
        response = self._send_session_request(method, temp_alias, endpoint, **kwargs)

        # Clean up the temporary session
        self.session_manager.delete_session(temp_alias)

        return response

    def _handle_token_refresh(self, alias: str, control_params: Dict) -> bool:
        """Handle token refresh logic."""
        if control_params.get('token'):
            # Use provided token
            self.session_manager.update_session_headers(alias, {
                "Authorization": f"{control_params.get('token_type', 'Bearer')} {control_params[ 'token' ]}"
            })
            return True
        elif control_params.get('auto_refresh', True):
            # Try to refresh token
            headers = self.session_manager.get_session_headers(alias)
            new_token = self.token_manager.refresh_token(headers)
            if new_token:
                # Update session with new token
                headers[ "Authorization" ] = f"Bearer {new_token}"
                self.session_manager.update_session_headers(alias, headers)
                return True

        return False

    def _check_expected_status(self, response: Any, expected_status: Any) -> bool:
        """
        Check if response status matches expected status.
        IMPORTANT: This has been replaced with direct status checking in _send_with_retries,
        but is kept for backward compatibility with other methods.
        """
        # Early exit for None response
        if response is None:
            logger.debug("Cannot check expected status: response is None")
            return False

        # If no expected status is provided, consider it a pass
        if expected_status is None:
            return True

        # Safely get status code
        try:
            status_code = self.response_handler.get_status_code(response)
        except Exception as e:
            logger.warn(f"Error getting status code in _check_expected_status: {e}")
            return False

        # If we couldn't get a status code, the check fails
        if status_code is None:
            logger.debug("Cannot check expected status: status code is None")
            return False

        # Check against expected status
        if isinstance(expected_status, list):
            return status_code in expected_status
        else:
            return status_code == expected_status

    def _log_api_request(self, alias: str, method: str, endpoint: str, response: Any) -> None:
        """Log API request and response details."""
        status_code = self.response_handler.get_status_code(response)
        content = "No Content"

        if response:
            try:
                if self.response_handler.get_content_type(response).startswith('application/json'):
                    content = self.response_handler.extract_json(response)
                else:
                    content = self.response_handler.get_content(response, as_text = True)
            except Exception as e:
                content = f"Could not parse response content: {str(e)}"

        # Format content for logging
        if isinstance(content, (dict, list)):
            try:
                content_str = json.dumps(content, indent = 2)
            except:
                content_str = str(content)
        else:
            content_str = str(content)

        # Log differently based on response status
        if response is None:
            logger.error(f"❌ API REQUEST FAILED:")
            logger.error(f"   - Session: {alias}")
            logger.error(f"   - Method: {method.upper()}")
            logger.error(f"   - Endpoint: {endpoint}")
            logger.error(f"   - Response: None (Request failed completely)")
        elif status_code and status_code >= 400:
            logger.error(f"❌ API REQUEST ERROR:")
            logger.error(f"   - Session: {alias}")
            logger.error(f"   - Method: {method.upper()}")
            logger.error(f"   - Endpoint: {endpoint}")
            logger.error(f"   - Response Code: {status_code}")
            logger.error(f"   - Response Body: {content_str}")
        else:
            log_message = f"""
            ✅ API REQUEST SUCCESS:
            - Session: {alias}
            - Method: {method.upper()}
            - Endpoint: {endpoint}
            - Response Code: {status_code}
            - Response Body: {content_str}
            """
            logger.info(log_message)

    def send_batch_requests(self, requests_list: List[ Dict ], **kwargs) -> List[ Any ]:
        """
        Send multiple API requests.

        :param requests_list: List of request dictionaries
        :param kwargs: Common parameters for all requests
        :return: List of response objects
        """
        responses = [ ]

        for i, request_data in enumerate(requests_list):
            try:
                # Merge common kwargs with individual request data
                merged_kwargs = kwargs.copy()
                merged_kwargs.update(request_data.get('kwargs', { }))

                # Send individual request
                response = self.send_request(
                    method = request_data.get('method'),
                    alias = request_data.get('alias'),
                    endpoint = request_data.get('endpoint'),
                    url = request_data.get('url'),
                    **merged_kwargs
                )
                responses.append(response)
            except Exception as e:
                logger.error(f"Error processing request at index {i}: {e}")
                responses.append(self.response_handler.wrap_response(None))

        return responses

    def wait_until_status(self, method: str, alias: str, endpoint: str, expected_status: Union[ int, List[ int ] ],
                          timeout: int = 60, interval: int = 5, **kwargs) -> Any:
        """Wait until an API endpoint returns an expected status code."""
        start_time = time.time()
        end_time = start_time + timeout

        if not isinstance(expected_status, (list, tuple)):
            expected_status = [ expected_status ]

        while time.time() < end_time:
            try:
                response = self.send_request(method, alias, endpoint = endpoint, **kwargs)
                status_code = self.response_handler.get_status_code(response)

                if status_code in expected_status:
                    return response

                logger.info(f"Waiting for API status {expected_status}, got {status_code}")
            except Exception as e:
                logger.warn(f"Error while waiting for API status: {e}")

            time.sleep(interval)

        logger.error(f"Timeout after {timeout} seconds waiting for API status {expected_status}")
        return self.response_handler.wrap_response(None)

    def wait_until_response(self, method: str, alias: str, endpoint: str, condition_func: Callable,
                            timeout: int = 60, interval: int = 5, **kwargs) -> Any:
        """Wait until an API endpoint returns a response that satisfies a condition."""
        start_time = time.time()
        end_time = start_time + timeout

        while time.time() < end_time:
            try:
                response = self.send_request(method, alias, endpoint = endpoint, **kwargs)

                if condition_func(response):
                    return response

                logger.info("Waiting for API response to satisfy condition")
            except Exception as e:
                logger.warn(f"Error while waiting for API response: {e}")

            time.sleep(interval)

        logger.error(f"Timeout after {timeout} seconds waiting for API response condition")
        return self.response_handler.wrap_response(None)
