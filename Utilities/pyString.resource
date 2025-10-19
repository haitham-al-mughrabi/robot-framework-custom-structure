*** Settings ***
Library      String
Library      Browser
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py


*** Keywords ***
Contains
    [Documentation]    Check if the given sub string is in the given string
    [Arguments]    
        ...    ${given_string}
        ...    ${sub_string}
        ...    ${check_error}=True
        ...    ${returnable}=False

    ${does_it_contains}=    Evaluate    "${sub_string}" in "${given_string}"

    IF    ${check_error} == True
        IF    ${does_it_contains} == False
            Fail    ${DEFAULT_CONTINUATION_ASSERTION_FAILED_MESSAGE}
        ELSE
            Log    ${DEFAULT_CONTINUATION_ASSERTION_SUCCESS_MESSAGE}
        END
    END

    IF    ${returnable} == True
        RETURN    {does_it_contains}
    END

Extract Numbers Using Regex
    [Documentation]    Extract Numbers From A String Using Regex
    [Arguments]     ${text}
    ${numbers}=    Replace String Using Regexp
        ...    ${text}
        ...    [^0-9]
        ...    ${EMPTY}
    RETURN     ${numbers}

Join String
    [Documentation]    Join List Items Into Single String
    [Arguments]    
        ...    ${list}
        ...    ${separator}=${EMPTY}
        ${joined_string} =  Evaluate  "${separator}".join($list)
        RETURN    ${joined_string}

Strip Locator Text
    [Documentation]    Strip Locator Text
    [Arguments]    
        ...    ${locator_text}
    ${stripped_string}    Replace String    
        ...    string=${locator_text}
        ...    search_for=\n
        ...    replace_with=${EMPTY}
    RETURN    ${stripped_string}
