*** Settings ***
Library    Browser
Variables    POM/Locators/Registration.py


*** Keywords ***
Registration Fill First Name
    [Documentation]    Fill First Name In Registration Form under Perfonal Info
    [Arguments]    ${user_first_name}    ${clear_previous_data}=${True}
    Wait For Elements State    
        ...    ${REGISTRATION_FIRST_NAME}    
        ...    timeout=60s    
        ...    message=Failed to wait for first name input field
    Type Text
        ...    txt=${user_first_name}
        ...    selector=${REGISTRATION_FIRST_NAME}
        ...    clear=${clear_previous_data}Open Browser
    ...    url=${url}
    ...    browser=${browser}
