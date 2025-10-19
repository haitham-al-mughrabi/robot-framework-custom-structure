*** Settings ***
Library      Browser
Library      String
Resource     Utilities/pyString.resource
Resource     Utilities/PageSupport.resource
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py


*** Keywords ***
Generic Capture Element Text
    [Documentation]    Generic Capture Element Text
    [Arguments]    
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${strip_text}=${False}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    xpath=${element_locator}
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}
    END

    ${captured_text}    Get Text    
        ...    ${element_locator}
        ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    IF    ${strip_text}
        ${captured_text}    Strip String    
            ...    ${captured_text}
            ...    characters=${SPACE}
        ${captured_text}    Replace String    
            ...    ${captured_text}
            ...    search_for=\n
            ...    replace_with=${EMPTY}
    END

    RETURN    ${captured_text}

Generic Capture Element Attribute
    [Documentation]    Generic Capture Element Attribute
    [Arguments]
    ...    ${element_locator}
    ...    ${attribute_name}
    ...    ${scroll_to_element}=${True}
    ...    ${wait_for_element_state}=${True}
    ...    ${strip_value}=${False}
    ...    ${take_screen_shot}=${False}

    ${element_locator}    Strip Locator Text    ${element_locator}

    IF    ${wait_for_element_state}
        Wait For Elements State
        ...    xpath=${element_locator}
        ...    state=${DEFAULT_ELEMENT_STATE}
        ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
            ...    ${element_locator}
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
        ...    selector=${element_locator}
    END

    ${captured_value}    Get Attribute
    ...    ${element_locator}
    ...    ${attribute_name}
    ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

    IF    ${strip_value}
        ${captured_value}    Strip String
        ...    ${captured_value}
        ...    characters=${SPACE}
        ${captured_value}    Replace String
        ...    ${captured_value}
        ...    search_for=\n
        ...    replace_with=${EMPTY}
    END

    RETURN    ${captured_value}
    