*** Settings ***
Library      Browser
Library      Libraries/Utilities/CustomConditioning.py
Library      Libraries/Utilities/VariableUtils.py
Resource     POM/Keywords/UI/Generic/Captures.resource
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py


*** Keywords ***
Assert Text
    [Documentation]    
    [Arguments]    
        ...    ${provided_text}
        ...    ${expected_text}=${None}
        ...    ${strip_spaces}=${True}
        ...    ${fail_on_error}=${True}
        ...    ${use_regex}=${False}
        ...    ${regex_pattern}=${None}
    ${provided_text}    Strip String    
        ...    ${provided_text}
        ...    characters=${SPACE}
    ${provided_text}    Replace String    
        ...    ${provided_text}
        ...    \n
        ...    ${EMPTY}
    IF    ${use_regex}
        ${assertion_result}    Run Keyword And Return Status
            ...    Should Match Regexp
                ...    ${provided_text}
                ...    ${regex_pattern}
    ELSE
        ${expected_text}    Strip String
            ...    ${expected_text}
            ...    characters=${SPACE}
        ${expected_text}    Replace String
            ...    ${expected_text}
            ...    \n
            ...    ${EMPTY}
        ${assertion_result}    Run Keyword And Return Status
            ...    Should Be Equal As Strings
                ...    ${provided_text}
                ...    ${expected_text}
                ...    strip_spaces=${strip_spaces}
    END
    IF    ${fail_on_error}
        IF    not ${assertion_result}
            Log    ${TEXT_ASSERTION_NOT_MATCHING_ERROR_MESSAGE('${provided_text}','${expected_text}')}
        END
    END
    RETURN    ${assertion_result}
    
Capture & Assert Text
    [Documentation]    Capture & Assert Text
    [Arguments]
        ...    ${element_locator}
        ...    ${expected_text}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${take_screenshot}=${True}
        ...    ${strip_spaces}=${True}
        ...    ${fail_on_error}=${True}
    ${captured_text}    Generic Capture Element Text
        ...    element_locator=${element_locator}
        ...    scroll_to_element=${scroll_to_element}
        ...    wait_for_element_state=${wait_for_element_state}
    
    ${assertion_result}    Assert Text
        ...    provided_text=${captured_text}
        ...    expected_text=${expected_text}
        ...    strip_spaces=${strip_spaces}
        ...    fail_on_error=${fail_on_error}
    IF    ${take_screenshot}
        Take Screenshot
            ...    selector=${element_locator}
            ...    timeout=${DEFAULT_SCREENSHOT_TIMEOUT}

        Take Screenshot
    END

    IF    not ${assertion_result}
        Fail    ${CAPTURED_TEXT_ASSERTION_NOT_MATCHING_ERROR_MESSAGE}

    END

    RETURN    ${assertion_result}


Capture & Assert Text By Regex
    [Documentation]    Capture & Assert Text By Regex
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${take_screenshot}=${True}
        ...    ${regex_pattern}=${None}
        ...    ${fail_on_error}=${True}
    ${captured_text}    Generic Capture Element Text
        ...    element_locator=${element_locator}
        ...    scroll_to_element=${scroll_to_element}
        ...    wait_for_element_state=${wait_for_element_state}

    ${assertion_result}    Assert Text
        ...    provided_text=${captured_text}
        ...    fail_on_error=${fail_on_error}
        ...    use_regex=${True}
        ...    regex_pattern=${regex_pattern}
    IF    ${take_screenshot}
        Take Screenshot
            ...    selector=${element_locator}
            ...    timeout=${DEFAULT_SCREENSHOT_TIMEOUT}
    END
    RETURN    ${assertion_result}

Verify Expected Element State
    [Documentation]    Verify Expected Element State
    [Arguments]    
        ...    ${element_locator}
        ...    ${expected_element_status}
        ...    ${take_screenshot}=${True}
        ...    ${timeout}=3s
        ...    ${error_message}=${NONE}
        ...    ${fail_on_error}=${True}
    ${verification_status}    Run Keyword And Return Status    
            ...    Wait For Elements State
                ...    selector=${element_locator}
                ...    state=${expected_element_status}
                ...    timeout=${timeout}
                ...    message=${error_message}
    Take Screenshot    
        ...    log_screenshot=${True}
        ...    fullPage=${True}
    IF    ${verification_status} == ${True} and ${take_screenshot} == ${True}
        Take Screenshot
            ...    selector=${element_locator}
            ...    log_screenshot=${True}
    ELSE IF    ${verification_status} == ${False} and ${fail_on_error}==${True}
        ${is_message_empty}    Is None    ${error_message}
        ${message}    Inline IF    
            ...    condition=${is_message_empty}    
            ...    condition_satisfied=Verification Failed
            ...    condition_failed=${error_message}
        Fail    ${message}
    END

Capture & Assert Attribute
    [Documentation]    Capture and assert a single attribute value of an element.
    [Arguments]
    ...    ${element_locator}
    ...    ${attribute_name}
    ...    ${expected_value}
    ...    ${scroll_to_element}=${True}
    ...    ${wait_for_element_state}=${True}
    ...    ${take_screenshot}=${True}
    ...    ${strip_spaces}=${True}
    ...    ${fail_on_error}=${True}

    ${captured_value}    Generic Capture Element Attribute
    ...    element_locator=${element_locator}
    ...    attribute_name=${attribute_name}
    ...    scroll_to_element=${scroll_to_element}
    ...    wait_for_element_state=${wait_for_element_state}

    ${assertion_result}    Assert Text
    ...    provided_text=${captured_value}
    ...    expected_text=${expected_value}
    ...    strip_spaces=${strip_spaces}
    ...    fail_on_error=${fail_on_error}

    IF    ${take_screenshot}
        Take Screenshot
        ...    selector=${element_locator}
        ...    timeout=${DEFAULT_SCREENSHOT_TIMEOUT}
    END

    IF    not ${assertion_result}
        Fail    ${CAPTURED_ATTRIBUTE_ASSERTION_NOT_MATCHING_ERROR_MESSAGE}
    END

    RETURN    ${assertion_result}

Capture & Assert Attributes
    [Documentation]    Capture and assert multiple attributes of an element.
    [Arguments]
    ...    ${element_locator}
    ...    ${expected_attributes}    # Dictionary of attribute_name=expected_value
    ...    ${scroll_to_element}=${True}
    ...    ${wait_for_element_state}=${True}
    ...    ${take_screenshot}=${True}
    ...    ${strip_spaces}=${True}
    ...    ${fail_on_error}=${True}

    ${assertion_result}    Set Variable    ${True}
    FOR    ${name}    ${expected}    IN    &{expected_attributes}
        ${captured}    Generic Capture Element Attribute
        ...    element_locator=${element_locator}
        ...    attribute_name=${name}
        ...    scroll_to_element=${scroll_to_element}
        ...    wait_for_element_state=${wait_for_element_state}

        ${match}    Assert Text
        ...    provided_text=${captured}
        ...    expected_text=${expected}
        ...    strip_spaces=${strip_spaces}
        ...    fail_on_error=${fail_on_error}

        IF    not ${match}
            ${assertion_result}    Set Variable    ${False}
        END
    END

    IF    ${take_screenshot}
        Take Screenshot
        ...    selector=${element_locator}
        ...    timeout=${DEFAULT_SCREENSHOT_TIMEOUT}
    END

    IF    not ${assertion_result}
        Fail    ${CAPTURED_ATTRIBUTES_ASSERTION_NOT_MATCHING_ERROR_MESSAGE}
    END

    RETURN    ${assertion_result}

Capture & Assert CSS Style Attribute
    [Documentation]    Capture and assert a specific CSS property from an element's inline style attribute.
    [Arguments]
    ...    ${element_locator}
    ...    ${css_property}
    ...    ${expected_value}
    ...    ${scroll_to_element}=${True}
    ...    ${wait_for_element_state}=${True}
    ...    ${strip_value}=${True}
    ...    ${take_screenshot}=${True}
    ...    ${fail_on_error}=${True}

    ${style_attr}    Generic Capture Element Attribute
    ...    element_locator=${element_locator}
    ...    attribute_name=style
    ...    scroll_to_element=${scroll_to_element}
    ...    wait_for_element_state=${wait_for_element_state}
    ...    strip_value=${strip_value}
    ...    take_screen_shot=${take_screenshot}

    TRY
        ${actual_value}    Evaluate
        ...    [v.strip() for v in '''${style_attr}'''.split(';') if v.strip().startswith('${css_property}:')][0].split(':', 1)[1].strip()
        ...    modules=BuiltIn
    EXCEPT
        Fail    CSS property '${css_property}' not found in element style: ${style_attr}
    END

    ${assertion_result}    Assert Text
    ...    provided_text=${actual_value}
    ...    expected_text=${expected_value}
    ...    strip_spaces=${strip_value}
    ...    fail_on_error=${fail_on_error}

    IF    not ${assertion_result}
        Fail    CSS style value for '${css_property}' did not match expected value. Found: '${actual_value}', Expected: '${expected_value}'
    END

    RETURN    ${assertion_result}
