"""
MailSac is a disposable email service that allows users to receive emails via API.

This class provides keywords to interact with the MailSac API, enabling functionalities such as:
- Creating random email addresses.
- Checking inbox for received emails.
- Retrieving email metadata and content.
- Deleting emails from the inbox.
- Validating email deletion.

Dependencies:
- `requests`: For making HTTP requests to the MailSac API.
- `robot.libraries.BuiltIn`: For logging and assertions in Robot Framework.
"""

from robot.libraries.BuiltIn import BuiltIn
import requests
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class MailSac:
    """
    A utility class for interacting with the MailSac API to manage disposable email addresses.

    This class provides keywords to create email addresses, check inboxes, retrieve email content,
    and delete emails. It is designed to be used in Robot Framework for automated testing.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the MailSac class with the provided API key.

        Parameters:
        - api_key (str): The API key for authenticating requests to the MailSac API.
        """
        self.base_url = 'https://mailsac.com/api'
        self.headers = {
            'Mailsac-Key': api_key
        }
        self.mail_domain = "@mailsac.com"
        self.builtin_instance = BuiltIn()

    @keyword("Create New Random MailSac Email")
    def create_email(self, mail_box: str) -> str:
        """
        Create a new random email address using the provided mailbox name.

        Parameters:
        - mail_box (str): The mailbox name (e.g., "testuser").

        Returns:
        - str: The full email address (e.g., "testuser@mailsac.com").

        Example:
        | ${email}= | Create New Random MailSac Email | testuser |
        | Log       | ${email}                        |          |
        | # Output: | testuser@mailsac.com            |          |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.builtin_instance.log(
                message=f"Email address {mail_box} created successfully."
            )
            return email
        elif response.status_code == 401:
            self.builtin_instance.log(
                message=f"Provided email is owned by another account. Email: {email}."
            )
        else:
            self.builtin_instance.fail(
                msg=f"Failed to create email address {email}. Status code: {response.status_code}"
            )

    def _concatenate_email(self, mail_box: str) -> str:
        """
        Helper method to concatenate the mailbox name with the MailSac domain.

        Parameters:
        - mail_box (str): The mailbox name.

        Returns:
        - str: The full email address.
        """
        return f"{mail_box}{self.mail_domain}"

    @keyword("Get All Mail Box Emails")
    def check_inbox(self, mail_box: str) -> list:
        """
        Retrieve a list of all emails in the specified mailbox.

        Parameters:
        - mail_box (str): The mailbox name.

        Returns:
        - list: A list of email objects, each containing metadata (e.g., sender, subject, ID).

        Example:
        | ${emails}= | Get All Mail Box Emails | testuser |
        | Log        | ${emails}               |          |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}/messages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            emails = response.json()
            self.builtin_instance.log(
                message=f"Emails received for {email}:"
            )
            for email in emails:
                self.builtin_instance.log(
                    message=f"From: {email['from']}, Subject: {email['subject']}, ID: {email['_id']}"
                )
            return emails
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 403:
            self.builtin_instance.log(
                message=f"Provided email is owned by another account. Email: {email}."
            )
        else:
            self.builtin_instance.fail(
                msg=f"Failed to check inbox for {email}. Status code: {response.status_code}"
            )

    @keyword("Get Email ID By Index")
    def get_email_id_by_index(self, inbox: list, email_index: int = 0) -> str:
        """
        Retrieve the email ID for a specific email in the inbox by its index.

        Parameters:
        - inbox (list): The list of emails returned by `Get All Mail Box Emails`.
        - email_index (int): The index of the email in the list. Default is 0 (first email).

        Returns:
        - str: The email ID.

        Example:
        | ${email_id}= | Get Email ID By Index | ${emails} | 0 |
        | Log          | ${email_id}           |           |   |
        """
        return inbox[email_index]['_id']

    @keyword("Get Email Meta Data")
    def get_email_meta_data(self, mail_box: str, email_id: str) -> dict:
        """
        Retrieve metadata for a specific email by its ID.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Returns:
        - dict: Metadata for the email (e.g., sender, subject, attachments).

        Example:
        | ${metadata}= | Get Email Meta Data | testuser | ${email_id} |
        | Log          | ${metadata}         |          |             |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}/messages/{email_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            email_content = response.json()
            self.builtin_instance.log_many(email_content)
            return email_content
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 404:
            self.builtin_instance.fail(
                msg=f"Message not found by id. Email ID: {email_id}"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Email ID: {email_id}. Respond_body: {response.json()}"
            )

    @keyword("Get Email Content")
    def get_email_content(self, mail_box: str, email_id: str = None, content_type: str = 'text') -> str:
        """
        Retrieve the content of a specific email by its ID.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID. If not provided, the first email in the inbox is used.
        - content_type (str): The type of content to retrieve. Options: 'text', 'body', 'dirty'.

        Returns:
        - str: The email content in the specified format.

        Example:
        | ${content}= | Get Email Content | testuser | ${email_id} | text |
        | Log         | ${content}        |          |             |      |
        """
        if email_id is None:
            inbox = self.check_inbox(mail_box=mail_box)
            email_id = self.get_email_id_by_index(inbox=inbox)
        if content_type == "text":
            return self._plaintext_email_content(mail_box=mail_box, email_id=email_id)
        elif content_type == "body":
            return self._sanitized_email_content(mail_box=mail_box, email_id=email_id)
        elif content_type == "dirty":
            return self._dirty_email_content(mail_box=mail_box, email_id=email_id)
        else:
            self.builtin_instance.fail(
                msg=f"Requested Content Type Not Declared. Provided type: {content_type}"
            )

    def _dirty_email_content(self, mail_box: str, email_id: str) -> str:
        """
        Retrieve the raw HTML content of an email, including images and scripts.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Returns:
        - str: The raw HTML content.
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/dirty/{email}/{email_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.builtin_instance.log(
                message=f"Email address {mail_box} created successfully."
            )
            return response.text
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 404:
            self.builtin_instance.fail(
                msg=f"Message not found by id. Email ID: {email_id}"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Email ID: {email_id}. Respond_body: {response.json()}"
            )

    def _sanitized_email_content(self, mail_box: str, email_id: str) -> str:
        """
        Retrieve the sanitized HTML content of an email, with scripts, images, and links removed.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Returns:
        - str: The sanitized HTML content.
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/body/{email}/{email_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.builtin_instance.log(
                message=f"Email address {mail_box} created successfully."
            )
            return response.text
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 404:
            self.builtin_instance.fail(
                msg=f"Message not found by id. Email ID: {email_id}"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Email ID: {email_id}. Respond_body: {response.json()}"
            )

    def _plaintext_email_content(self, mail_box: str, email_id: str) -> str:
        """
        Retrieve the plaintext content of an email.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Returns:
        - str: The plaintext content.
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/text/{email}/{email_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.builtin_instance.log(
                message=f"Email address {mail_box} created successfully."
            )
            return response.text
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 404:
            self.builtin_instance.fail(
                msg=f"Message not found by id. Email ID: {email_id}"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Email ID: {email_id}. Respond_body: {response.json()}"
            )

    @keyword("Delete Email From Mail Box By Its ID")
    def delete_mail_from_mail_box(self, mail_box: str, email_id: str) -> None:
        """
        Delete a specific email from the mailbox by its ID.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Example:
        | Delete Email From Mail Box By Its ID | testuser | ${email_id} |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}/messages/{email_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            response_body = response.json()
            self.builtin_instance.should_be_equal_as_strings(
                response_body['_id'],
                email_id
            )
            self.builtin_instance.should_be_equal_as_strings(
                response_body['inbox'],
                email
            )
            self.builtin_instance.should_be_equal_as_strings(
                response_body['message'],
                "Message was deleted."
            )
            self.builtin_instance.log(
                message=f"Message Got Successfully Deleted From Mail Box {mail_box}."
            )
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 404:
            self.builtin_instance.fail(
                msg=f"Message not found by id. Email ID: {email_id}."
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Mailbox: {mail_box}. Respond_body: {response.json()}"
            )

    @keyword("Delete All Messages From Mail Box")
    def delete_all_messages_from_mail_box(self, mail_box: str) -> None:
        """
        Delete all emails from the specified mailbox.

        Parameters:
        - mail_box (str): The mailbox name.

        Example:
        | Delete All Messages From Mail Box | testuser |
        """
        mails = self.check_inbox(mail_box=mail_box)
        if len(mails) > 0:
            for mail in mails:
                email_id = mail['_id']
                self.delete_mail_from_mail_box(mail_box=mail_box, email_id=email_id)
        else:
            self.builtin_instance.log(
                message=f" Mail Box {mail_box} is empty."
            )

    @keyword("Check Mail Box Is Totally Empty")
    def validate_all_messages_got_deleted_from_mail_box(self, mail_box: str) -> None:
        """
        Validate that the mailbox is empty.

        Parameters:
        - mail_box (str): The mailbox name.

        Example:
        | Check Mail Box Is Totally Empty | testuser |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}/message-count"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response_body = response.json()
            self.builtin_instance.should_be_equal_as_numbers(
                response_body['count'],
                0,
                msg=f"Mailbox is not empty. Current Messages Count: {response_body['count']}"
            )
            self.builtin_instance.log(
                message=f"Emails Got Successfully Deleted. Mail Box Inbox Is Empty!"
            )
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 403:
            self.builtin_instance.fail(
                msg=f"Requested email address is owned by another user. Mailbox: {mail_box}!"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Mailbox: {mail_box}. Respond_body: {response.json()}"
            )

    @keyword("Check Email Message Got Successfully Deleted")
    def validate_mail_got_deleted_from_mail_box(self, mail_box: str, email_id: str) -> None:
        """
        Validate that a specific email has been deleted from the mailbox.

        Parameters:
        - mail_box (str): The mailbox name.
        - email_id (str): The email ID.

        Example:
        | Check Email Message Got Successfully Deleted | testuser | ${email_id} |
        """
        email = self._concatenate_email(mail_box)
        url = f"{self.base_url}/addresses/{email}/messages/{email_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            self.builtin_instance.log(
                message=f"Message not found by id. Email ID: {email_id}. Mail got successfully deleted"
            )
        elif response.status_code == 401:
            self.builtin_instance.fail(
                msg="Check Access Token Then Try Again!"
            )
        elif response.status_code == 200:
            self.builtin_instance.fail(
                msg=f"Mail {email_id} got found in mailbox {mail_box}!"
            )
        else:
            self.builtin_instance.fail(
                msg=f"Undefined Error. Email ID: {email_id}. Respond_body: {response.json()}"
            )
