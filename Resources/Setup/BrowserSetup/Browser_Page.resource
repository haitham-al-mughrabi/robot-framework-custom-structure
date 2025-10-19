*** Settings ***
Documentation       Set setup, teardown and global variables values.
Library             Collections
Library             Browser
Library             Libraries/Utilities/VariableUtils.py

Resource            Utilities/FileDirOperations.resource

Variables           Resources/DataSources/Setup/BrowserConfigurations.py
Variables           Resources/Configurations/Baselines/DefaultBaseValues.py
Variables           Resources/Configurations/Baselines/DefaultTestsMessages.py


*** Keywords ***
Add New Page
    [Documentation]    Opens New Page & Stores Page Information In Global List For Page Switching
    [Arguments]
        ...    ${init_url}
        ...    ${destination_url}=${None}
        ...    ${wait_until}=${DEFAULT_WAIT_PAGE_COMMIT_BEHAVIOR}
    ${page_data}    New Page
        ...    url=${init_url}
        ...    wait_until=${wait_until}
    ${is_destination_url_provided}    Is Not None    ${destination_url}
    IF    ${is_destination_url_provided}
        Go To
            ...    url=${destination_url}
            ...    wait_until=${wait_until}
        ${current_url}    Set Variable    ${destination_url}
    ELSE
        ${current_url}    Set Variable    ${init_url}
    END
    RETURN    ${page_data}

Switch Between Tabs
    [Documentation]    Uses stored Page IDs To Switch Between Tabs
    [Arguments]
        ...    ${page_id}=${None}
        ...    ${context}=ALL
        ...    ${browser}=ALL
    ${is_id_provided}    Check Nullability    ${page_id}
    IF    not ${is_id_provided}
        Fail    Page Object Is Not Provided. Aborting!
    END
    Switch Page
        ...    ${page_id}
        ...    context=${context}
        ...    browser=${browser}
    Log    Tab got switched to page with id: ${page_id}

Get All Active Pages
    [Documentation]    Get List Of All Active Pages
    [Arguments]
        ...    ${context}=ACTIVE
        ...    ${browser}=ACTIVE
    ${pages}    Get Page Ids
        ...    page=ALL
        ...    context=${context}
        ...    browser=${browser}
    RETURN    ${pages}

Get Tab ID By Page Index
    [Documentation]    Get the desired page ID by its index
    [Arguments]
        ...    ${page_index}
        ...    ${context}=ACTIVE
        ...    ${browser}=ACTIVE
    ${pages}    Get All Active Pages
        ...    context=${context}
        ...    browser=${browser}
    ${desired_page_id}    Get From List    ${pages}    ${page_index}
    RETURN    ${desired_page_id}

Get Active Page ID
    [Documentation]    Get Active Page ID
    ${page_id}    Get Page Ids    page=ACTIVE
    RETURN    ${page_id[0]}

Close Desired Page
    [Documentation]    Closes The Desired Page & Remove It From Session Pages List
    [Arguments]
        ...    ${page_index}
    ${page_id}    Get Tab ID By Page Index
        ...    page_index=${page_index}
    Close Page    page=${page_id}

Close Current Page
    [Documentation]    Closes Current Page, and Head To The Desired Page. In case
        ...            desired page did not get defined, preceding page will be
        ...            automatically be selected. In case the page was the only
        ...            page opened, the browser, including context will be closed
    [Arguments]
        ...    ${desired_page}=${None}
    ${is_desired_page_provided}    Check Nullability    ${desired_page}
    ${current_page_id}    Get Active Page ID
    IF    ${is_desired_page_provided}
        Switch Between Tabs
            ...   page_id=${desired_page}
    END
    Sleep    1s

    Close Page    ${current_page_id}