from robot.api.deco import keyword, library
from Libraries.Utilities.Generators import *
from Libraries.Variables.Payments import *
from Libraries.Variables.Cities import *
from Resources.Variables.Constants.Cards import AVAILABLE_CARD_TYPES


@library(doc_format='ROBOT')
class PaymentCard:
    def __init__(self):
        self.mada_bins = MADA_BINS
        self.cities = CITIES
        self.card = ''
        self.expiry_date = ''
        self.cvv = ''
        self.city = ''
        self.address = ''
        self.postal_code = ''
        self.generators_instance = Generators()
        self.card_type = ''
        self.last_four_digits= ''

    @staticmethod
    def luhn_checksum(card_number):
        """
        Calculate the Luhn checksum of a card number.
        :param card_number:
        :return:
        """
        digits_of = lambda n: [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def generate_luhn_valid_card(self, bin_prefix: str, length: int) -> str:
        """
        Generate a valid card number using the Luhn algorithm, keeping the BIN unchanged.
        :param bin_prefix:
        :param length:
        :return:
        """
        # Ensure the BIN is not altered
        number = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(bin_prefix) - 1)])
        # Calculate the check digit
        checksum_digit = str((10 - self.luhn_checksum(number + '0')) % 10)
        return number + checksum_digit

    @keyword("Generate ${card_name} Card Information")
    def generate_card(self, card_name, card_type: str) -> dict:
        """
        Generate a valid card number based on the card type (Mada, Visa, MasterCard).
        :param card_name:
        :param card_type:
        :return:
        """
        if card_type == "random_card":
            card_type = random.choice(AVAILABLE_CARD_TYPES)

        if card_type.capitalize() == "Mada":
            bin_prefix = random.choice(self.mada_bins)
        elif card_type.capitalize() == "Visa":
            bin_prefix = "4" + ''.join(random.choices("0123456789", k=5))
        elif card_type.capitalize() == "Mastercard":
            # MasterCard can start with 51-55 or 2221-2720
            if random.choice([True, False]):
                bin_prefix = str(random.randint(51, 55)) + ''.join(random.choices("0123456789", k=4))
            else:
                bin_prefix = str(random.randint(2221, 2720))
        else:
            raise ValueError("Unsupported card type. Choose 'mada', 'visa', or 'mastercard'.")

        # Generate and return the card number
        self.card_type = card_type.lower()
        self.card = self.generate_luhn_valid_card(bin_prefix, 16)
        self.last_four_digits = self.card[-4:]
        self.city, self.address, self.postal_code = self.generators_instance.generate_random_address()
        self.expiry_date = self.generators_instance.generate_expiry_date()
        self.cvv = self.generators_instance.generate_cvv()
        card_data = {
            'card_number': self.card,
            'expiry_date': self.expiry_date,
            'cvv': self.cvv,
            'name': 'AQA Tester',
            'city': self.city,
            'address': self.address,
            'postal_code': self.postal_code,
            'card_type': self.card_type,
            'last_four_digits': self.last_four_digits
        }
        return card_data
