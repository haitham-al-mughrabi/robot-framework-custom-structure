import requests
import json
from typing import Optional, Dict
from robot.api import logger
from robot.api.deco import keyword, library


@library(doc_format = 'ROBOT', auto_keywords=True)
class TokenManager:
    """
    Manages token validation and refresh operations.
    """

    def __init__(self, token_endpoint: Optional[str] = None):
        """
        Initialize token manager.

        :param token_endpoint: Endpoint for token validation/refresh
        """
        self.token_endpoint = token_endpoint or "https://donation-platform-api.donations.uat.devops.takamol.support/sessions/refresh_token_check"

    def validate_token(self, headers: Dict) -> bool:
        """
        Validate if a token is still valid by calling the token check endpoint.

        :param headers: Request headers containing the authorization token
        :return: True if token is valid, False otherwise
        """
        try:
            if not headers or 'Authorization' not in headers:
                return False

            auth_token = headers['Authorization']
            if auth_token.startswith('Bearer '):
                auth_token = auth_token[7:]  # Remove 'Bearer ' prefix

            # Prepare headers for token validation request
            validation_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'RefreshToken': auth_token
            }

            # Make a request to the token validation endpoint
            response = requests.post(
                self.token_endpoint,
                headers=validation_headers,
                timeout=10
            )

            # Check if response is successful and contains valid token data
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    # Verify the response contains the expected data
                    return 'auth_token' in response_data and 'auth_expires_at' in response_data
                except (ValueError, json.JSONDecodeError):
                    pass

            return False
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False

    def refresh_token(self, headers: Dict) -> Optional[str]:
        """
        Attempts to refresh the token by calling the refresh token endpoint.

        :param headers: Request headers containing the current token
        :return: New token if refresh was successful, None otherwise
        """
        try:
            if not headers or 'Authorization' not in headers:
                return None

            auth_header = headers['Authorization']
            if auth_header.startswith('Bearer '):
                auth_token = auth_header[7:]  # Remove 'Bearer ' prefix
            else:
                auth_token = auth_header

            # Prepare headers for token refresh request
            refresh_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'RefreshToken': auth_token
            }

            # Call refresh token endpoint
            response = requests.post(
                self.token_endpoint,
                headers=refresh_headers,
                timeout=10
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if 'auth_token' in response_data:
                        return response_data['auth_token']
                except (ValueError, json.JSONDecodeError):
                    pass

            logger.warn("Failed to refresh token")
            return None
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return None

    def extract_token_from_headers(self, headers: Dict) -> Optional[str]:
        """
        Extract the authentication token from headers.

        :param headers: Request headers
        :return: The token string or None if not found
        """
        if not headers or 'Authorization' not in headers:
            return None

        auth_header = headers['Authorization']
        if auth_header.startswith('Bearer '):
            return auth_header[7:]  # Remove 'Bearer ' prefix
        return auth_header
