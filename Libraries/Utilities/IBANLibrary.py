import random
from robot.api.deco import keyword, library
from Libraries.Variables.Bank import SAUDI_BANK_CODES


@library(doc_format='ROBOT')
class IBANLibrary:

    def __init__(self):
        self.saudi_bank_codes = SAUDI_BANK_CODES

    @keyword("Generate Saudi IBAN")
    def generate_saudi_iban(self, bank_code, prefix=None):
        """
        Generate a valid Saudi IBAN for the given bank code.

        Args:
            bank_code (str): A 2-digit string representing the Saudi bank code.
            prefix (str): A 2 English Characters string representing the Saudi Code.
        Returns:
            str: A valid Saudi IBAN.
        """
        if bank_code not in self.saudi_bank_codes:
            raise ValueError("Invalid bank code. Please provide a valid 2-digit Saudi bank code.")

        # Generate a random 18-digit account number
        account_number = ''.join(random.choices('0123456789', k=18))

        # Construct the initial IBAN without check digits
        initial_iban = f'SA00{bank_code}{account_number}'

        # Move the first four characters to the end
        rearranged_iban = initial_iban[4:] + initial_iban[:4]

        # Replace each letter with two digits (A=10, B=11, ..., Z=35)
        numeric_iban = ''.join(str(ord(char) - 55) if char.isalpha() else char for char in rearranged_iban)

        # Convert to an integer
        iban_int = int(numeric_iban)

        # Calculate the remainder of the division of iban_int by 97
        remainder = iban_int % 97

        # Calculate the check digits
        check_digits = 98 - remainder

        # Format check digits to be two digits (e.g., '03', '27')
        check_digits_str = f'{check_digits:02}'

        # Construct the final IBAN
        iban = prefix if prefix is not None else '' + f'{check_digits_str}{bank_code}{account_number}'

        return iban
