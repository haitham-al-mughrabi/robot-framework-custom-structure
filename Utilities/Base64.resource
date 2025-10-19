*** Keywords ***
Encode Base64
    [Documentation]    Encode Base64
    [Arguments]        ${data}
    ${encoded_string}    Evaluate
        ...    base64.b64encode('${data}'.encode('utf-8')).decode('utf-8')    
        ...    modules=base64
    RETURN    ${encoded_string}
