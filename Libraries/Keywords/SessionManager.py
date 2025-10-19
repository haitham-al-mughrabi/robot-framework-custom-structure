import uuid
from typing import Dict, Any, Optional
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword, library


@library(doc_format = 'ROBOT', auto_keywords=True)
class SessionManager:
    """
    Manages API session lifecycle including creation, deletion, and updates.
    """

    def __init__(self):
        """Initialize session manager with RequestsLibrary."""
        BuiltIn().import_library('RequestsLibrary')
        self.requests_lib = BuiltIn().get_library_instance("RequestsLibrary")
        self.sessions = { }

    def create_session(self, alias: str, url: str, headers: Optional[ Dict ] = None, **kwargs) -> str:
        """
        Creates a new API session and stores it for tracking.

        :param alias: The session alias
        :param url: The base URL for the session
        :param headers: Optional dictionary of headers
        :param kwargs: Additional parameters for RequestsLibrary
        :return: The session alias
        """
        headers = headers or { }
        # Filter session-specific parameters
        session_params = { }
        for key, value in kwargs.items():
            if key in ('auth', 'verify', 'cert', 'proxies', 'timeout'):
                session_params[ key ] = value

        self.requests_lib.create_session(alias, url, headers = headers, **session_params)
        self.sessions[ alias ] = { "url": url, "headers": headers, "kwargs": session_params }
        logger.info(f"Session '{alias}' created with URL: {url}")
        return alias

    def create_random_session(self, url: str, headers: Optional[ Dict ] = None, **kwargs) -> str:
        """
        Creates a session with a randomly generated alias.

        :param url: The base URL for the session
        :param headers: Optional dictionary of headers
        :param kwargs: Additional parameters for RequestsLibrary
        :return: The random alias used for the session
        """
        random_alias = f"session_{uuid.uuid4().hex[ :8 ]}"
        return self.create_session(random_alias, url, headers = headers, **kwargs)

    def delete_session(self, alias: str) -> bool:
        """
        Deletes a specific API session.

        :param alias: The alias of the session to delete
        :return: True if session was deleted, False if not found
        """
        if alias in self.sessions:
            del self.sessions[ alias ]
            logger.info(f"Session '{alias}' deleted successfully")
            return True
        else:
            logger.warn(f"Session '{alias}' not found!")
            return False

    def delete_all_sessions(self) -> None:
        """Deletes all stored API sessions."""
        self.sessions.clear()
        logger.info("All API sessions have been deleted.")

    def update_session_headers(self, alias: str, new_headers: Dict) -> bool:
        """
        Updates session headers dynamically.

        :param alias: The alias of the session
        :param new_headers: Dictionary of new headers
        :return: True if successful, False if session not found
        """
        if alias not in self.sessions:
            logger.warn(f"Session '{alias}' not found!")
            return False

        # Validate that new_headers is a dictionary
        if not isinstance(new_headers, dict):
            logger.error(f"new_headers must be a dictionary, got {type(new_headers)}")
            return False

        # Remove the session from RequestsLibrary's internal cache
        if hasattr(self.requests_lib, "_cache") and alias in self.requests_lib._cache:
            del self.requests_lib._cache[ alias ]

        # Retrieve session details
        url = self.sessions[ alias ][ "url" ]
        kwargs = self.sessions[ alias ][ "kwargs" ].copy() if isinstance(self.sessions[ alias ][ "kwargs" ],
                                                                         dict) else { }

        try:
            # Recreate the session with the new headers
            self.requests_lib.create_session(alias, url, headers = new_headers, **kwargs)

            # Update our internal tracking
            self.sessions[ alias ] = {
                "url": url,
                "headers": new_headers.copy() if isinstance(new_headers, dict) else { },
                "kwargs": kwargs
            }
            logger.info(f"Replaced headers for session '{alias}'")
            return True
        except Exception as e:
            logger.error(f"Error updating session headers: {e}")
            return False

    def get_session_details(self, alias: str) -> Optional[ Dict ]:
        """
        Retrieves the full details of a session.

        :param alias: The alias of the session
        :return: A dictionary containing session details or None if not found
        """
        if alias not in self.sessions:
            logger.warn(f"Session '{alias}' not found!")
            return None

        try:
            # Retrieve session object from RequestsLibrary internal cache
            if hasattr(self.requests_lib, "_cache") and alias in self.requests_lib._cache:
                session_object = self.requests_lib._cache[ alias ]
            else:
                logger.warn(f"Session '{alias}' not found in RequestsLibrary cache!")
                return None

            # Extract session details
            session_details = {
                "url": self.sessions[ alias ][ "url" ],
                "headers": getattr(session_object, 'headers', None),
                "cookies": getattr(session_object, 'cookies', None).get_dict() if getattr(session_object, 'cookies',
                                                                                          None) is not None else None,
                "timeout": getattr(session_object, 'timeout', None),
                "proxies": getattr(session_object, 'proxies', None),
                "auth": getattr(session_object, 'auth', None)
            }

            return session_details
        except (KeyError, AttributeError) as e:
            logger.warn(f"Error getting session details: {e}")
            return None

    def get_session_headers(self, alias: str) -> Optional[ Dict ]:
        """
        Get headers for a specific session.

        :param alias: The session alias
        :return: Headers dictionary or None if not found
        """
        details = self.get_session_details(alias)
        return details.get('headers') if details else None

    def session_exists(self, alias: str) -> bool:
        """
        Check if a session exists.

        :param alias: The session alias
        :return: True if session exists, False otherwise
        """
        return alias in self.sessions

    def get_session_url(self, alias: str) -> Optional[ str ]:
        """
        Get the base URL for a session.

        :param alias: The session alias
        :return: The base URL or None if not found
        """
        return self.sessions.get(alias, { }).get("url")
