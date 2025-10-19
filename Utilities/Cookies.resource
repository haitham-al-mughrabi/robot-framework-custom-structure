*** Settings ***
Library        Browser
Library        Collections
Library        Libraries/Utilities/VariableUtils.py
Variables      Resources/Variables/Assertions/Utilities.py

*** Keywords ***
Globalize Cookies
    [Documentation]    Capture all cookies from the browser
    ...                then populate all cookies as a glo-
    ...                bal variable.
    ${captured_cookies}       Get Cookies
    Set Global Variable
        ...    ${COOKIES}   #Global Variable Name
        ...    ${captured_cookies[0]}    #Value
    RETURN    ${captured_cookies}

Get Certain Cookie From Cookie Jar
    [Documentation]    Get Certain Cookie From Cookie Jar
    [Arguments]    ${cookie_name}

    ${captured_cookie}=
        ...    Get Cookie    
        ...    cookie=${cookie_name}

    RETURN    ${captured_cookie}
    
Get Cookie Value From Cookie Body
    [Documentation]    Get Cookie Value From Cookie Body
    [Arguments]    ${cookie}
    
    ${check_result}    Is Not None   ${cookie}
    IF    ${check_result}
        ${cookie_value}    Get From Dictionary
        ...    ${cookie}
        ...    value
        ...    None
        RETURN    ${cookie_value}
    ELSE
        Fail    ${COOKIE_JAR_EMPTY}
    END
