# Static Locators

# Assertors.resource
CAPTURED_TEXT_ASSERTION_NOT_MATCHING_ERROR_MESSAGE = """
Assertion Failed Due To not matchability. Aborting!
"""
CAPTURED_ATTRIBUTE_ASSERTION_NOT_MATCHING_ERROR_MESSAGE = """
Assertion Failed Due To not matchability. Aborting!
"""
CAPTURED_ATTRIBUTES_ASSERTION_NOT_MATCHING_ERROR_MESSAGE = """
Assertion Failed Due To not matchability. Aborting!
"""
# Dynamic Locators
TEXT_ASSERTION_NOT_MATCHING_ERROR_MESSAGE = lambda provided_text, expected_text: f"""
Provided text [${provided_text}] does not match expected text [{expected_text}]
"""
