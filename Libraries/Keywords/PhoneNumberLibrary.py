import random
import requests
from datetime import datetime, timedelta
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from Libraries.Keywords.SupabaseLibrary import *


@library(doc_format='ROBOT')
class PhoneNumberLibrary:
    def __init__(self, supabase_url, supabase_key):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase_lib = SupabaseLibrary(supabase_url, supabase_key)
        self.builtin = BuiltIn()
        # No need to init DB here, assuming table exists in Supabase

    @keyword("Generate Unique Phone Number")
    def generate_unique_phone_number(self, country_key=None, starts_with='05', store=True, env='uat'):
        """
        Generates a unique phone number that starts with '05' and is 10 digits long and stores in Supabase.
        """
        while True:
            if country_key is not None:
                number = country_key + starts_with + ''.join(random.choices('0123456789', k=8))
            else:
                number = starts_with + ''.join(random.choices('0123456789', k=8))

            if self._validate_number(number, env):
                if store:
                    self._store_number_in_db(number)
                return number

    def _validate_number(self, number, env):
        """
        Validates the phone number by sending a POST request to the API.
        """
        url = f"https://donation-platform-api.donations.{env}.devops.takamol.support/sessions/login"
        payload = {
            "user": {
                "login": number,
                "otp_attempt": "0000",
                "user_role": 0
            }
        }
        response = requests.post(url, json=payload)
        if response.status_code == 422 and "رمز التحقق غير صحيح" in response.json().get("error", ""):
            self.builtin.log(f"Number {number} is not registered and is usable.", level="INFO")
            return True
        elif response.status_code == 200 and "id" in response.json():
            self.builtin.log(f"Number {number} is already registered.", level="INFO")
            self._store_number_in_db(number)  # Store even if registered, as per original logic
            return False
        else:
            self.builtin.log(f"Unexpected response for number {number}: {response.text}", level="WARN")
            return False

    def _store_number_in_db(self, number):
        """
        Stores the phone number in the Supabase database.
        """
        table_name = "phone_numbers"
        data_to_insert = {"number": str(number)}
        try:
            self.supabase_lib.insert_data(table_name, data_to_insert)
            self.builtin.log(f"Number {number} added to Supabase database.", level="INFO")
        except Exception as e:  # Catch SupabaseLibrary exceptions
            if "23505" in str(
                    e):  # Error code for unique violation - IntegrityError equivalent in Supabase? Check Supabase error codes. For Postgres unique constraint violation is 23505
                self.builtin.log(f"Number {number} already exists in the Supabase database.", level="DEBUG")
            else:
                self.builtin.log(f"Error storing number {number} in Supabase: {e}", level="ERROR")
                raise e  # Re-raise to signal failure

    @keyword("Mark Number As Deleted")
    def mark_number_as_deleted(self, number):
        """Mark the phone number as deleted in Supabase."""
        table_name = "phone_numbers"
        filters = self.supabase_lib.build_filter_query([{"key": "number", "op": "equals", "value": number}])
        delete_time = (datetime.now() + timedelta(days=10)).isoformat()  # Full timestamp
        data_to_update = {"is_deleted": True, "delete_time": delete_time}
        try:
            self.supabase_lib.update_data(table_name, filters, data_to_update)
            self.builtin.log(f"Number {number} marked as deleted in Supabase.", level="INFO")
        except Exception as e:
            self.builtin.log(f"Error marking number {number} as deleted in Supabase: {e}", level="ERROR")
            raise e

    @keyword("Cleanup Deleted Numbers")
    def cleanup_deleted_numbers(self):
        """Remove numbers that have been marked as deleted for more than 10 days from Supabase."""
        table_name = "phone_numbers"
        ten_days_ago = (datetime.now() - timedelta(days=10)).isoformat()  # Format datetime to ISO string for Supabase
        filters = self.supabase_lib.build_filter_query([
            {"key": "is_deleted", "op": "equals", "value": True},
            # is_deleted should be boolean in Supabase, changed to True
            {"key": "delete_time", "op": "lte", "value": ten_days_ago}
        ])
        try:
            response = self.supabase_lib.select_data(table_name, filters)
            if isinstance(response, list):
                deleted_numbers_count = 0
                for record in response:
                    number_to_delete = record.get('number')
                    if number_to_delete:
                        delete_filter = self.supabase_lib.build_filter_query(
                            [{"key": "number", "op": "equals", "value": number_to_delete}])
                        self.supabase_lib.delete_data(table_name,
                                                      delete_filter)  # Use delete_data to actually remove from Supabase
                        deleted_numbers_count += 1
                self.builtin.log(f"Successfully removed {deleted_numbers_count} deleted numbers from Supabase.",
                                 level="INFO")
            else:
                self.builtin.log("No deleted numbers found for cleanup in Supabase.", level="INFO")


        except Exception as e:
            self.builtin.log(f"Error cleaning up deleted numbers from Supabase: {e}", level="ERROR")
            raise e
