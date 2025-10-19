import json
import requests
from typing import Dict, Any, Optional, Union, List
from robot.api import logger
from robot.api.deco import library, keyword


@library(doc_format = 'ROBOT', auto_keywords=True)
class ResponseWrapper:
    """
    A wrapper for response objects with enhanced functionality.
    Provides easy access to common response properties and attributes.
    """

    def __init__(self, response: Optional[requests.Response], auto_json: bool = False):
        """
        Initialize the ResponseWrapper with a requests.Response object.

        :param response: The original requests.Response object or None if request failed
        :param auto_json: Whether to automatically parse JSON response
        """
        self.response = response
        self._json_data = None
        self._auto_json = auto_json

        # Auto-parse JSON if enabled
        if auto_json and response is not None and hasattr(response, 'content') and response.content:
            try:
                self._json_data = response.json()
            except (ValueError, json.JSONDecodeError):
                # Not JSON content, ignore
                pass

    @property
    def status_code(self) -> Optional[int]:
        """Get the HTTP status code of the response."""
        return self.response.status_code if self.response and hasattr(self.response, 'status_code') else None

    @property
    def ok(self) -> bool:
        """Return True if status_code is less than 400, False otherwise."""
        return bool(self.response and hasattr(self.response, 'ok') and self.response.ok)

    @property
    def content(self) -> Optional[bytes]:
        """Get the raw content of the response."""
        return self.response.content if self.response and hasattr(self.response, 'content') else None

    @property
    def text(self) -> Optional[str]:
        """Get the text content of the response."""
        return self.response.text if self.response and hasattr(self.response, 'text') else None

    @property
    def headers(self) -> Optional[Dict]:
        """Get the headers of the response."""
        return self.response.headers if self.response and hasattr(self.response, 'headers') else None

    @property
    def url(self) -> Optional[str]:
        """Get the URL of the response."""
        return self.response.url if self.response and hasattr(self.response, 'url') else None

    @property
    def elapsed(self) -> Optional[float]:
        """Get the elapsed time of the request in seconds."""
        if not self.response or not hasattr(self.response, 'elapsed'):
            return None
        if hasattr(self.response.elapsed, 'total_seconds'):
            return self.response.elapsed.total_seconds()
        return None

    @property
    def cookies(self) -> Optional[Dict]:
        """Get the cookies from the response."""
        if not self.response or not hasattr(self.response, 'cookies'):
            return None
        if hasattr(self.response.cookies, 'get_dict'):
            return self.response.cookies.get_dict()
        return None

    def json(self) -> Optional[Any]:
        """
        Parse the response content as JSON.
        If auto_json is enabled, returns cached result.
        """
        if self._auto_json and self._json_data is not None:
            return self._json_data

        if not self.response or not hasattr(self.response, 'content') or not self.response.content:
            return None

        try:
            if not self._json_data:
                self._json_data = self.response.json()
            return self._json_data
        except (ValueError, json.JSONDecodeError):
            logger.warn("Response content is not valid JSON")
            return None

    def get_json_value(self, key_path: str, default: Any = None) -> Any:
        """
        Extract a value from the JSON response using a dot-notation path.

        :param key_path: Path to the value (e.g., "data.user.id")
        :param default: Default value to return if path not found
        :return: The extracted value or default
        """
        if not self.response:
            return default

        json_data = self.json()
        if not json_data:
            return default

        keys = key_path.split('.')
        current = json_data

        try:
            for key in keys:
                if isinstance(current, list) and key.isdigit():
                    # Handle array indices in the path
                    index = int(key)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return default
                elif isinstance(current, dict):
                    if key in current:
                        current = current[key]
                    else:
                        return default
                else:
                    # Current is neither a list nor a dict
                    return default

            # Return the extracted value
            return current
        except (KeyError, IndexError, TypeError):
            return default

    def __bool__(self) -> bool:
        """Make the wrapper evaluate to True if response exists and status is ok."""
        return self.ok

    def __str__(self) -> str:
        """String representation of the response wrapper."""
        if not self.response:
            return "ResponseWrapper(No Response)"

        status = self.status_code if self.status_code is not None else "unknown"
        url = self.url if self.url is not None else "unknown"
        elapsed = f"{self.elapsed}s" if self.elapsed is not None else "unknown"

        return f"ResponseWrapper(status={status}, url={url}, elapsed={elapsed})"

    def get_original(self) -> Optional[requests.Response]:
        """Get the original response object."""
        return self.response
