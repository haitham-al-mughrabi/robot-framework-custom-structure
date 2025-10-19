*** Settings ***
Library    Collections
Library    Libraries/Utilities/Generators.py


*** Keywords ***
Generate Random Number With Specified Range
    [Documentation]    Generate Random Number. It can be in specified range,
        ...            selected returned type, and prefixed on demand.
    [Arguments]  
        ...    ${range_min}=${0}
        ...    ${range_max}=${100000}
        ...    ${number_of_digits}=${None}
        ...    ${output_type}=int
        ...    ${prefix}=${None}
    ${number}    Generate Random PyNumber
        ...    range_min=${range_min}
        ...    range_max=${range_max}
        ...    number_of_digits=${number_of_digits}
        ...    output_type=${output_type}
        ...    prefix=${prefix}
    RETURN    ${number}
    
Get Random Item From List
    [Documentation]    Returns a random item from the given list. If the list is empty, returns ${EMPTY}.
    [Arguments]    ${my_list}
    ${list_length}=    Get Length    ${my_list}
    IF    ${list_length} == 0
        RETURN    ${EMPTY}
    ELSE
        ${random_index}=    Evaluate    random.randint(0, len($my_list)-1)
        ${random_item}=    Set Variable    ${my_list}[${random_index}]
        RETURN    ${random_item}
    END

Get Random Item From List & Remove The Item From List
    [Documentation]    Get Random Item From List and remove it from the list
    [Arguments]    ${my_list}
    ${random_index}=    Evaluate    random.randint(0, len(${my_list})-1)    random
    ${random_item}=    Evaluate    ${my_list}.pop(${random_index})
    RETURN    ${random_item}

Generate Random Boolean Value
    [Documentation]    Generate Random Boolean Value
    ${random_boolean_value}    Evaluate
        ...    random.choice([True, False])
        ...    modules=random
    RETURN    ${random_boolean_value}

Select Random Element From Dictionary
    [Documentation]    Returns a random key from the provided dictionary
    [Arguments]
        ...    ${dictionary}
    ${random_key}    Evaluate    
        ...    random.choice(list(dictionary.keys()))
        ...    random
    RETURN    ${random_key}

Generate Random Number Less Than Max Value
    [Documentation]    Generate Random Number Less Than Max Value
    [Arguments]    
        ...    ${min_value}
        ...    ${max_value}
    ${random_number}    Evaluate    random.randint(${min_value}, ${max_value}-1)    random
    RETURN    ${random_number}
