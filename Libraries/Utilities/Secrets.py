import random
import string
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from Libraries.Variables.Names import *


@library(doc_format='ROBOT')
class Secrets:
    def __init__(self):
        self.builtin = BuiltIn()
        self.matched_index = -1
        self.arabic_first_names = arabic_first_names
        self.english_first_names = english_first_names
        self.arabic_last_names = arabic_last_names
        self.english_last_names = english_last_names

        # Organization name components
        self.arabic_org_prefixes = arabic_org_prefixes

        self.english_org_prefixes = english_org_prefixes

        self.arabic_org_domains = arabic_org_domains

        self.english_org_domains = english_org_domains

        # Generate organization full names lists
        self.english_charity_names = self._generate_english_org_names()
        self.arabic_charity_names = self._generate_arabic_org_names()

    def _generate_english_org_names(self):
        """Generate a list of English organization names"""
        names = []
        # Base pattern with first names
        for prefix in self.english_org_prefixes:
            for domain in self.english_org_domains:
                for first_name in self.english_first_names[:10]:  # Using first 10 names to limit list size
                    names.append(f"{first_name} {prefix} for {domain}")
                    names.append(f"{first_name} {domain} {prefix}")
                    names.append(f"The {first_name} {prefix} of {domain}")
                    names.append(f"{first_name} {domain} {prefix}")
                    names.append(f"International {first_name} {prefix} for {domain}")

        # Add variations with last names
        for prefix in self.english_org_prefixes[:8]:  # Using subset to limit size
            for domain in self.english_org_domains[:8]:
                for last_name in self.english_last_names[:8]:
                    names.append(f"{last_name} {prefix} for {domain}")
                    names.append(f"{prefix} {last_name} {domain}")
                    names.append(f"The {last_name} {domain} {prefix}")
                    names.append(f"{last_name} & Partners {domain} {prefix}")
                    names.append(f"Global {last_name} {prefix} for {domain}")

        # Add generic patterns without names
        for prefix in self.english_org_prefixes:
            for domain in self.english_org_domains:
                names.append(f"Global {domain} {prefix}")
                names.append(f"International {prefix} for {domain}")
                names.append(f"United {domain} {prefix}")
                names.append(f"Advanced {domain} {prefix}")
                names.append(f"{domain} {prefix} International")
                names.append(f"Premier {domain} {prefix}")
                names.append(f"{domain} {prefix} World")
                names.append(f"The {domain} {prefix}")

        # Add combined domains
        domain_pairs = []
        for i in range(min(10, len(self.english_org_domains))):
            for j in range(i + 1, min(10, len(self.english_org_domains))):
                domain_pairs.append((self.english_org_domains[i], self.english_org_domains[j]))

        for prefix in self.english_org_prefixes[:5]:
            for domain1, domain2 in domain_pairs[:10]:
                names.append(f"{domain1} & {domain2} {prefix}")
                names.append(f"{prefix} for {domain1} and {domain2}")

        return names

    def _generate_arabic_org_names(self):
        """Generate a list of Arabic organization names"""
        names = []
        # Base pattern with first names
        for prefix in self.arabic_org_prefixes:
            for domain in self.arabic_org_domains:
                for first_name in self.arabic_first_names[:10]:  # Using first 10 names to limit list size
                    names.append(f"{prefix} {first_name} {domain}")
                    names.append(f"{prefix} {domain} {first_name}")
                    names.append(f"{prefix} {first_name} {domain} الدولية")
                    names.append(f"{prefix} {first_name} العالمية {domain}")

        # Add variations with last names
        for prefix in self.arabic_org_prefixes[:8]:  # Using subset to limit size
            for domain in self.arabic_org_domains[:8]:
                for last_name in self.arabic_last_names[:8]:
                    names.append(f"{prefix} {last_name} {domain}")
                    names.append(f"{prefix} {domain} {last_name}")
                    names.append(f"{prefix} {last_name} وشركاه {domain}")
                    names.append(f"{prefix} آل {last_name} {domain}")
                    names.append(f"{prefix} {last_name} المتحدة {domain}")

        # Add generic patterns without names
        for prefix in self.arabic_org_prefixes:
            for domain in self.arabic_org_domains:
                names.append(f"{prefix} الدولية {domain}")
                names.append(f"{prefix} العالمية {domain}")
                names.append(f"{prefix} المتحدة {domain}")
                names.append(f"{prefix} المتطورة {domain}")
                names.append(f"{prefix} الرائدة {domain}")
                names.append(f"{prefix} الأولى {domain}")
                names.append(f"{prefix} الخليج {domain}")
                names.append(f"{prefix} العربية {domain}")
                names.append(f"{prefix} الشرق الأوسط {domain}")
                names.append(f"{prefix} الوطنية {domain}")

        # Add combined domains
        domain_pairs = []
        for i in range(min(10, len(self.arabic_org_domains))):
            for j in range(i + 1, min(10, len(self.arabic_org_domains))):
                domain_pairs.append((self.arabic_org_domains[i], self.arabic_org_domains[j]))

        for prefix in self.arabic_org_prefixes[:5]:
            for domain1, domain2 in domain_pairs[:10]:
                names.append(f"{prefix} {domain1} و{domain2}")
                names.append(f"{prefix} المتكاملة {domain1} و{domain2}")

        return names

    @keyword("Generate A Conditional Random Word")
    def generate_word(self, **kwargs):
        length = kwargs.get('length', 8)
        prefix = kwargs.get('prefix', '')

        use_upper = kwargs.get('use_upper', False)
        use_lower = kwargs.get('use_lower', True)
        use_digits = kwargs.get('use_digits', False)
        use_arabic = kwargs.get('use_arabic', False)
        use_special = kwargs.get('use_special', False)
        use_spaces = kwargs.get('use_spaces', False)

        lower = string.ascii_lowercase if use_lower else ''
        upper = string.ascii_uppercase if use_upper else ''
        digits = string.digits if use_digits else ''
        arabic = 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي' if use_arabic else ''
        special = '!@#$%^&*()_+-=[]{}|;:,.<>/?' if use_special else ''
        spaces = ' ' if use_spaces else ''

        all_chars = f"{lower}{upper}{digits}{arabic}{special}{spaces}"

        if not all_chars:
            self.builtin.fail("At least one character set must be enabled")

        required_chars = ''
        if use_lower:
            required_chars += random.choice(lower)
        if use_upper:
            required_chars += random.choice(upper)
        if use_digits:
            required_chars += random.choice(digits)
        if use_arabic:
            required_chars += random.choice(arabic)
        if use_special:
            required_chars += random.choice(special)
        if use_spaces:
            required_chars += random.choice(spaces)

        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            self.builtin.fail("Length is too short to include all required character sets")

        result = ''.join(random.choice(all_chars) for _ in range(remaining_length))
        result += required_chars
        result = ''.join(random.sample(result, len(result)))  # Shuffle the result to randomize positions
        return prefix + result if prefix else result

    @keyword("Generate A Conditional Random Password")
    def generate_password(self, **kwargs):
        length = kwargs.get('length', 8)
        correct_password = kwargs.get('correct_password', False)

        if correct_password:
            if length < 8:
                raise ValueError("Length must be at least 8 to meet the condition requirements")
            # Start with a guaranteed uppercase letter
            password = [random.choice(string.ascii_uppercase)]
            # Ensure the inclusion of at least one of each required character type
            password.extend([
                random.choice(string.ascii_lowercase),
                random.choice(string.digits),
                random.choice('!@#$%^&*()_+-=[]{}|;:,.<>/?')
            ])
            # Generate the remaining characters
            remaining_length = length - len(password)
            password.extend(self.generate_word(length=remaining_length, **kwargs))
            random.shuffle(password[1:])  # Shuffle only the part after the first character
            password = ''.join(password)
        else:
            password = self.generate_word(length=length, **kwargs)

        return password

    @keyword("Generate Random Number")
    def generate_random_number(self, min_value: int = 0, max_value: int = 10):
        """
        Generates a random number between the specified minimum and maximum values.

        Args:
            min_value: The minimum value (inclusive) for the random number.
            max_value: The maximum value (inclusive) for the random number.

        Returns:
            The generated random number.
        """
        try:
            if min_value >= max_value:
                self.builtin.log("Minimum value must be less than the maximum value. Please try again.")
            else:
                random_number = random.randint(min_value, max_value)
                self.builtin.log(f"The generated random number is: {random_number}")
                return random_number  # Return the generated number

        except ValueError:
            self.builtin.fail("Invalid input. Please enter integers only.")

    def _pick(self, name_list, indexed=False):
        """
        Helper method to pick an item from a list based on the class-stored index.
        """
        if indexed and self.matched_index is not None:
            # If indexed is True and a class-stored index exists, use it
            if 0 <= self.matched_index < len(name_list):
                return name_list[self.matched_index]
            else:
                raise ValueError("Stored index is invalid.")
        else:
            # Otherwise, pick a random item and store the index
            self.matched_index = random.randint(0, len(name_list) - 1)
            return name_list[self.matched_index]

    @keyword("Pick English Charity Names")
    def pick_english_charity_names(self, indexed=False):
        return self._pick(self.english_charity_names, indexed)

    @keyword("Pick Arabic Charity Names")
    def pick_arabic_charity_names(self, indexed=False):
        return self._pick(self.arabic_charity_names, indexed)

    @keyword("Pick English Last Names")
    def pick_english_last_names(self, indexed=False):
        return self._pick(self.english_last_names, indexed)

    @keyword("Pick English First Names")
    def pick_english_first_names(self, indexed=False):
        return self._pick(self.english_first_names, indexed)

    @keyword("Pick Arabic Last Names")
    def pick_arabic_last_names(self, indexed=False):
        return self._pick(self.arabic_last_names, indexed)

    @keyword("Pick Arabic First Names")
    def pick_arabic_first_names(self, indexed=False):
        return self._pick(self.arabic_first_names, indexed)
