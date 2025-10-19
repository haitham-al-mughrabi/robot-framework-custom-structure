*** Settings ***
Library      Collections
Library      BuiltIn
Library      Browser
Variables    Resources/Variables/Constants/Assertions.py
Variables    Resources/Variables/Assertions/Utilities.py


*** Keywords ***
Check Nullability
    [Documentation]    Check if the given variable empty or not.
        ...            Real Value -> True
        ...            None Value -> False
    [Arguments]    
        ...    ${passed_variable}
    ${variable_type}    Retrieve Variable Type
        ...    variable=${passed_variable}
    IF    '${variable_type}' == 'NoneType'
        RETURN    False
    ELSE    
        RETURN    True
    END

Nullability Assertion
    [Documentation]    Check if the variable is none(null).
        ...            Returns True if the variable is none(null).
        ...            Return False if the variable is not none(null).
    [Arguments]    
        ${examination_variable}
    ${examination_result}    Evaluate    ${examination_variable} is None
    RETURN    ${examination_result}
        

Retrieve Variable Type
    [Documentation]    Retrieve Variable Type
    [Arguments]    
        ...    ${variable}
    ${variable_type}    Evaluate
        ...    type($variable).__name__
    RETURN    ${variable_type}

Assert Element State
    [Documentation]    Check the element status if match the desired status
    [Arguments]    
        ...    ${element_locator}
        ...    ${expected_status}
    ${element_statuses}      Get Element States
            ...    ${element_locator}    
    ${assertion_status}    Run Keyword And Return Status
        ...    List Should Contain Value
            ...    ${element_statuses}
            ...    ${expected_status}
    IF    ${assertion_status}
        Log    ${POSITIVE_ELEMENT_STATE_RESULT}
    ELSE
        Fail    ${NEGATIVE_ELEMENT_STATE_RESULT('${expected_status}', @{element_statuses})}
    END
