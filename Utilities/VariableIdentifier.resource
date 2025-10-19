*** Keywords ***
Get Variable Type
    [Documentation]    Determine what the variable type is
    [Arguments]    
        ...    ${variable_under_examination}
    ${variable_type}
          ...    Evaluate    type($variable_under_examination).__name__
    RETURN    ${variable_type}
