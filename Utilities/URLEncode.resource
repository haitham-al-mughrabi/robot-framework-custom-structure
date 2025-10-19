*** Keywords ***
Encode URL
    [Documentation]    Encode URL
    [Arguments]    ${decoded_url}
    ${encoded_url}=    Evaluate    urllib.parse.quote_plus('${decoded_url}')
    RETURN    ${encoded_url}

Decode URL
    [Documentation]    Decode URL
    [Arguments]    ${encoded_url}
    ${decoded_url}=    Evaluate    urllib.parse.unquote_plus('${encoded_url}')
    RETURN    ${decoded_url}
    