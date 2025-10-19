*** Settings ***
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py
Variables    POM/Locators/Shared/DynamicLocators.py


*** Keywords ***
Generic XPath Creator By Element Text
    [Documentation]    Creates an XPath expression based on the provided element text.
        ...            The keyword supports options to specify if the text is a substring 
        ...            and if the element should be unique or indexed.
    [Arguments]
        ...    ${element_text}              # The text used to locate the element.
        ...    ${element_type}=${DEFAULT_GENERIC_ELEMENT_TAG}
        ...    ${is_sub_string}=${False}    # Boolean flag to specify if the text should be matched as a substring.
        ...    ${is_unique}=${True}         # Boolean flag to specify if the element is unique. Defaults to True.
        ...    ${element_index}=${None}     # The index of the element if it is not unique. Defaults to None.
        ...    ${is_element_group}=${False}    # Multiple elements that shared the same locator
    IF    ${is_unique}
        IF    ${is_sub_string}
            RETURN    ${UNIQUE_ELEMENT_BY_ITS_CONTAINED_TEXT('${element_type}','${element_text}')}
        ELSE
            RETURN    ${UNIQUE_ELEMENT_BY_ITS_TEXT('${element_type}','${element_text}')}
        END
    ELSE
        IF    ${is_sub_string}
            RETURN    ${INDEXED_ELEMENT_BY_ITS_CONTAINED_TEXT('${element_type}','${element_text}',${element_index})}
        ELSE IF    ${is_element_group}
            RETURN    ${INDEXED_ELEMENT_GROUP_BY_ITS_CONTAINED_TEXT('${element_type}','${element_text}',${element_index})}
        ELSE
            RETURN    ${INDEXED_ELEMENT_BY_ITS_TEXT('${element_type}','${element_text}',${element_index})}
        END
    END

Generic XPath Creator By Element Attribute
    [Documentation]    Creates an XPath expression based on the provided element attribute.
        ...            The keyword supports options to specify if the attribute value is a 
        ...            substring and if the element should be unique or indexed.
    [Arguments]
        ...    ${attribute_value}
        ...    ${element_attribute}=${TEXT_ATTRIBUTE}
        ...    ${element_type}=${DEFAULT_GENERIC_ELEMENT_TAG}
        ...    ${is_sub_string}=${False}    # Boolean flag to specify if the text should be matched as a substring.
        ...    ${is_unique}=${True}         # Boolean flag to specify if the element is unique. Defaults to True.
        ...    ${element_index}=${None}     # The index of the element if it is not unique. Defaults to None.
        ...    ${is_element_group}=${False}    # Multiple elements that shared the same locator
    IF    ${is_unique}
        IF    ${is_sub_string}
            RETURN    ${UNIQUE_ELEMENT_BY_ITS_CONTAINED_ATTRIBUTE('${element_type}','${element_attribute}','${attribute_value}')}
                
        ELSE
            RETURN    ${UNIQUE_ELEMENT_BY_ITS_ATTRIBUTE('${element_type}','${element_attribute}','${attribute_value}')}
        END
    ELSE
        IF    ${is_sub_string}
            RETURN    ${INDEXED_ELEMENT_BY_ITS_CONTAINED_ATTRIBUTE('${element_type}','${element_attribute}','${attribute_value}','${element_index}')}
        ELSE IF    ${is_element_group} # Multiple elements that shared the same locator
            RETURN    ${INDEXED_ELEMENT_GROUP_BY_ITS_CONTAINED_ATTRIBUTE('${element_type}','${element_attribute}','${attribute_value}',${element_index})}
        ELSE
            RETURN    ${INDEXED_ELEMENT_BY_ITS_ATTRIBUTE('${element_type}','${element_attribute}','${attribute_value}','${element_index}')}
        END
    END
