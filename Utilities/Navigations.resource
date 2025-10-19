*** Settings ***
Library    Browser


*** Keywords ***
Wait For Navigation
    [Documentation]    Waits for page navigation to complete. When a URL changes, waits until the page is fully loaded.
    ...    This keyword supports waiting for multiple navigations by providing a timeout parameter.
    ...
    ...    *Arguments:*
    ...    - ``timeout`` (optional): Time to wait for all navigations in seconds. Default is 30 seconds.
    ...    - ``wait_until`` (optional): When to consider navigation complete. Options are: load|domcontentloaded|networkidle. Default is "load".
    ...
    ...    *Examples:*
    ...    | Wait For Navigation |
    ...    | Wait For Navigation | timeout=60 |
    ...    | Wait For Navigation | wait_until=networkidle |
    [Arguments]    ${timeout}=30    ${wait_until}=load
    ${current_url}=    Get Url
    Wait For Navigation To Start    ${current_url}    ${timeout}
    Wait For Condition    url != "${current_url}"    timeout=${timeout}
    Wait For Load State    ${wait_until}    timeout=${timeout}

Wait For Navigation To Start
    [Documentation]    Internal keyword to wait for navigation to start by checking when the URL begins to change.
    [Arguments]    ${original_url}    ${timeout}=30
    ${url_changed}=    Set Variable    ${FALSE}
    FOR    ${i}    IN RANGE    ${timeout}
        ${current_url}=    Get Url
        IF    "${current_url}" != "${original_url}"
            ${url_changed}=    Set Variable    ${TRUE}
            BREAK
        END
        Sleep    0.1s
    END
    IF    ${url_changed} == ${FALSE}
        Fail    Navigation did not start within timeout
    END

Wait For Multiple Navigations
    [Documentation]    Waits for multiple page navigations to complete sequentially.
    ...
    ...    *Arguments:*
    ...    - ``count``: Number of navigations to wait for.
    ...    - ``timeout`` (optional): Time to wait for each navigation in seconds. Default is 30 seconds.
    ...    - ``wait_until`` (optional): When to consider navigation complete. Options are: load|domcontentloaded|networkidle. Default is "load".
    ...
    ...    *Examples:*
    ...    | Wait For Multiple Navigations | 2 |
    ...    | Wait For Multiple Navigations | 3 | timeout=60 | wait_until=networkidle |
    [Arguments]    ${count}    ${timeout}=30    ${wait_until}=load
    FOR    ${i}    IN RANGE    ${count}
        Wait For Navigation    timeout=${timeout}    wait_until=${wait_until}
    END

Wait For Payment Navigation Cycle
    [Documentation]    Waits for a complete payment navigation cycle: from your site to payment checkout and back to your site.
    ...    Can handle variable wait times during checkout processing.
    ...
    ...    *Arguments:*
    ...    - ``original_url``: The URL of your site to verify return to after payment
    ...    - ``checkout_timeout`` (optional): Maximum time to wait for checkout process in seconds. Default is 120 seconds.
    ...    - ``return_timeout`` (optional): Maximum time to wait for return to original site in seconds. Default is 60 seconds.
    ...    - ``wait_until`` (optional): When to consider navigation complete. Options are: load|domcontentloaded|networkidle. Default is "networkidle".
    [Arguments]    ${original_url}=${EMPTY}    
        ...    ${checkout_timeout}=120    
        ...    ${return_timeout}=60    
        ...    ${wait_until}=networkidle

    # Store the starting URL if original_url wasn't provided
    ${starting_url}=    Run Keyword If    "${original_url}" == "${EMPTY}"    Get Url    ELSE    Set Variable    ${original_url}

    # Wait for navigation to checkout page
    ${current_url}=    Get Url
    Wait For Condition    url != "${current_url}"    timeout=${checkout_timeout}
    Wait For Load State    ${wait_until}    timeout=${checkout_timeout}

    # Wait for navigation back to original site
    Wait For Condition    url == "${starting_url}" or url.startswith("${starting_url}")    timeout=${return_timeout}
    Wait For Load State    ${wait_until}    timeout=${return_timeout}
