*** Keywords ***
Add Numbers
    [Documentation]    Add Numbers
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) + float($num2)
    IF    ${get_fixed_number}
        ${result}    Format Decimal To Fixed Integer
            ...    num_as_string=${result}
    END
    ${result}    Convert To Integer    ${result}
    RETURN    ${result}

Subtract Numbers
    [Documentation]    Subtract Numbers
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) - float($num2)
    IF    ${get_fixed_number}
        ${result}    Format Decimal To Fixed Integer
            ...    num_as_string=${result}
    END
    RETURN    ${result}

Multiply Numbers
    [Documentation]    Multiply Numbers
    [Arguments]    
        ...    ${num1}    
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}    Evaluate    float($num1) * float($num2)
    IF    ${get_fixed_number}
        ${result}    Format Decimal To Fixed Integer
            ...    num_as_string=${result}
    END
    RETURN    ${result}

Divide Numbers
    [Documentation]    Divide Numbers
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    Run Keyword If    $num2 == 0
    ...    Fail    Cannot divide by zero.
    ${result}=    Evaluate    float($num1) / float($num2)
    IF    ${get_fixed_number}
        ${result}    Format Decimal To Fixed Integer
            ...    num_as_string=${result}
    END
    RETURN    ${result}

Toggle Sign
    [Documentation]    Toggle Sign
    [Arguments]    ${num}
    ${result}=    Evaluate    -float($num)
    RETURN    ${result}

Format Decimal To Fixed Integer
    [Documentation]    Format Decimal To Fixed Integer
    [Arguments]    ${num_as_string}
    ${formatted_string}    Evaluate    f"{${num_as_string}:.0f}"
    RETURN    ${formatted_string}

Division Remainder
    [Documentation]    Finds Division Remainder
    [Arguments]    
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    Run Keyword If    $num2 == 0
    ...    Fail    Cannot divide by zero.
    ${result}=    Evaluate    float($num1) // float($num2)
    IF    ${get_fixed_number}
        ${result}    Format Decimal To Fixed Integer
            ...    num_as_string=${result}
    END
    RETURN    ${result}

Less Than
    [Documentation]    Check If num1 is less than num2
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) < float($num2)
    RETURN    ${result}

Less Than Or Equal To
    [Documentation]    Check If num1 is less than num2 or equal to it
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) = float($num2)
    RETURN    ${result}

Bigger Than
    [Documentation]    Check If num1 is bigger than num2
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) > float($num2)
    RETURN    ${result}

Bigger Than Or Equal To
    [Documentation]    Check If num1 is bigger than num2 or equal to it
    [Arguments]
        ...    ${num1}
        ...    ${num2}
        ...    ${get_fixed_number}=${True}
    ${result}=    Evaluate    float($num1) >= float($num2)
    RETURN    ${result}
