import certifi
import requests
from robot.api.deco import keyword, library
from Libraries.Variables.Operators import OPERATORS


@library(doc_format = 'ROBOT', auto_keywords=True)
class SupabaseLibrary:
    """
    A Robot Framework library to interact with Supabase APIs.

    This library provides keywords to perform CRUD operations on Supabase,
    including inserting, selecting, updating, and deleting data using the Supabase REST API.
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initializes the SupabaseLibrary with the given URL and API key.

        :param supabase_url: The base URL of the Supabase project.
        :param supabase_key: The API key for authentication.
        """
        self.supabase_url = supabase_url.rstrip('/')
        self.supabase_key = supabase_key
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        self.operators = OPERATORS

    @keyword("Insert Data Into Supabase")
    def insert_data(self, table: str, data: dict):
        """
        Inserts data into a specified table in Supabase.

        :param table: The name of the table.
        :param data: A dictionary containing the data to be inserted.
        :return: The response from Supabase.
        """
        url = f"{self.supabase_url}/rest/v1/{table}"
        response = requests.post(url, json=data, headers=self.headers, verify=certifi.where())
        return self._handle_response(response)

    @keyword("Select Data From Supabase")
    def select_data(self, table: str, filters: str = ""):
        """
        Selects data from a specified table in Supabase.

        :param table: The name of the table.
        :param filters: A query string for filtering the results (optional).
        :return: The response from Supabase.
        """
        url = f"{self.supabase_url}/rest/v1/{table}"
        if filters:
            url += f"?{filters}"
        response = requests.get(url, headers=self.headers, verify=certifi.where())
        return self._handle_response(response)

    @keyword("Update Data In Supabase")
    def update_data(self, table: str, filters: str, data: dict):
        """
        Updates data in a specified table in Supabase.

        :param table: The name of the table.
        :param filters: A query string to filter the rows to be updated.
        :param data: A dictionary containing the updated data.
        :return: The response from Supabase.
        """
        url = f"{self.supabase_url}/rest/v1/{table}?{filters}"
        response = requests.patch(url, json=data, headers=self.headers, verify=certifi.where())
        return self._handle_response(response)

    @keyword("Delete Data From Supabase")
    def delete_data(self, table: str, filters: str):
        """
        Deletes data from a specified table in Supabase based on filters.

        :param table: The name of the table.
        :param filters: A query string to filter the rows to be deleted.
        :return: The response from Supabase.
        """
        url = f"{self.supabase_url}/rest/v1/{table}?{filters}"
        response = requests.delete(url, headers=self.headers, verify=certifi.where())
        return self._handle_response(response)

    @keyword("Acquire And Release User")
    def acquire_and_release_user(self, table: str, user_identifier: str = "id"):
        """
        Acquires an available user (where under_use is false), updates it to true,
        and releases it back to false after use.

        :param table: The table where users are stored.
        :param user_identifier: The column that uniquely identifies the user (default is "id").
        :return: The acquired user details.
        """
        # Step 1: Find an available user
        filters = [{"key": "under_use", "op": "equals", "value": False}]
        filter_query = self.build_filter_query(filters)
        users = self.select_data(table, filter_query)

        if isinstance(users, dict):
            users = [users]

        if not users:
            raise Exception("No available user found.")

        user = users[0]
        user_id = user[user_identifier]

        # Step 2: Mark user as under use (under_use = true)
        update_filters = [{"key": user_identifier, "op": "equals", "value": user_id}]
        update_query = self.build_filter_query(update_filters)
        self.update_data(table, update_query, {"under_use": True})

        return user  # Return the acquired user

    @keyword("Release User")
    def release_user(self, table: str, user_id: int, user_identifier: str = "id"):
        """
        Releases a user by setting under_use back to false.

        :param table: The table where users are stored.
        :param user_id: The unique identifier of the user.
        :param user_identifier: The column that uniquely identifies the user (default is "id").
        """
        filters = [{"key": user_identifier, "op": "equals", "value": user_id}]
        filter_query = self.build_filter_query(filters)
        self.update_data(table, filter_query, {"under_use": False})

    def _handle_response(self, response: requests.Response):
        """
        Handles the response from Supabase API.
        """
        if response.status_code in (200, 201, 204):
            try:
                json_data = response.json()
                if isinstance(json_data, list) and len(json_data) == 1 and isinstance(json_data[0], dict):
                    return json_data[0]  # Convert single-item list to dict
                return json_data if isinstance(json_data, (list, dict)) else []
            except ValueError:
                return "Success"
        else:
            raise Exception(f"Supabase API error: {response.status_code} - {response.text}")

    @keyword("Build Filter Query")
    def build_filter_query(self, filters: list) -> str:
        """
        Builds a query string for filtering Supabase data.

        :param filters: A list of dictionaries containing:
            - "key": The column name.
            - "op": The operation (e.g., "equals", "like", "in").
            - "value": The value to filter by.
        :return: A query string formatted for Supabase filtering.
        """
        query_parts = []
        for filter in filters:
            key = filter["key"]
            op = self.operators.get(filter["op"], filter["op"])  # Convert to Supabase-friendly operator
            value = filter["value"]

            # Handle list values for "in" and other set operations
            if isinstance(value, list):
                value = f"({','.join(map(str, value))})"

            # Handle boolean values explicitly
            elif isinstance(value, bool):
                value = "true" if value else "false"

            # Handle special LIKE cases
            elif op in ["like", "ilike"]:
                value = value.replace("*", "%").replace("?", "_")  # Convert wildcards if needed

            query_parts.append(f"{key}={op}.{value}")

        return "&".join(query_parts)

    @keyword("Get Available Supabase User")
    def get_available_user_procedure(self):
        """
        Calls Supabase RPC function 'get_available_user' to atomically fetch and lock an available user.
        """
        url = f"{self.supabase_url}/rest/v1/rpc/get_available_user"
        response = requests.post(url, headers = self.headers, json = { }, verify = certifi.where())
        response.raise_for_status()

        data = response.json()
        if not data:
            raise Exception("No available user found.")

        return data[ 0 ]

    @keyword("Release Supabase User By Procedure")
    def release_user_procedure(self, user_id: int):
        """
        Calls Supabase RPC function 'release_user' to reset a user's 'under_use' flag by ID.
        :param user_id: ID of the user (integer)
        """
        url = f"{self.supabase_url}/rest/v1/rpc/release_user"
        payload = { "in_user_id": user_id }
        response = requests.post(url, headers = self.headers, json = payload, verify = certifi.where())
        response.raise_for_status()

    @keyword("Release All Supabase Users")
    def release_all_users_procedure(self):
        """
        Calls Supabase RPC function 'release_all_users' to reset all users' under_use flag to false.
        """
        url = f"{self.supabase_url}/rest/v1/rpc/release_all_users"
        response = requests.post(url, headers = self.headers, json = { }, verify = certifi.where())
        response.raise_for_status()
