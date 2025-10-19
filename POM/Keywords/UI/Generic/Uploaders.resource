*** Settings ***
Library      Browser
Resource     Utilities/PageSupport.resource
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py


*** Keywords ***
Generic Upload File
    [Documentation]    Generic Upload File
    [Arguments]
        ...    ${element_locator}
        ...    ${file_path}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/..
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}/parent::*
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    Upload File By Selector    
        ...    ${element_locator}
        ...    path=${file_path}
    