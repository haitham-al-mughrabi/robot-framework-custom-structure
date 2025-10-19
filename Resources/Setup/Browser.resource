*** Settings ***
Documentation       Set setup, teardown and global variables values.
Library             Collections
Library             Browser
    ...             auto_closing_level=MANUAL
Library             Libraries/Utilities/CustomConditioning.py
Library             Libraries/Utilities/VariableUtils.py
Resource            Resources/Setup/BrowserSetup/Browser_Context.resource
Resource            Resources/Setup/BrowserSetup/Browser_Page.resource
Resource            Resources/Setup/BrowserSetup/Browser_Configurations.resource
Resource            Utilities/ExecutionConfiguration.resource
Resource            Resources/Configurations/Execution.resource
Resource            Resources/Variables/FilePaths/Configurations.resource
Resource            root_path.resource


*** Keywords ***
Initialize New Browser
    [Documentation]    Configure Browser Options, including browser type, browser args and more
    [Arguments]
        ...    ${base_page}=${None}
    Load Project Path
    Execution Variables Table
    Configure Browser Arguments
    ${context_options}    Setup Browser Context
    ${is_normal_context}    Compare Strings    
        ...    string1=${CONTEXT_TYPE}    
        ...    string2=NORMAL
        ...    case_transform1=lower
        ...    case_transform2=lower
    IF    ${is_normal_context}
        ${browser_session_info}    Use Normal Context
            ...    base_page=${base_page}
            ...    context_options=${context_options}
    ELSE
        ${browser_session_info}    Use Persistent Context
            ...    base_page=${base_page}
            ...    context_options=${context_options}
    END
    Set Browser Timeout    timeout=${BROWSER_TIMEOUT}
    Globalize Browser Variables
        ...    browser_session_info=${browser_session_info}

Use Persistent Context
    [Documentation]    Use Persistent Context
    [Arguments]    
        ...    ${base_page}
        ...    ${context_options}
    ${browser_session_details}    New Persistent Context
        ...    browser=${BROWSER_FAMILY}
        ...    headless=${HEADLESS}
        ...    channel=${BROWSER_CHANNEL}
        ...    args=${BROWSER_ARGS}
        ...    downloadsPath=${DOWNLOADS_DIRECTORY_PATH}
        ...    devtools=${DEV_TOOLS}
        ...    chromiumSandbox=${CHROME_SECURITY_SANDBOX}
        ...    viewport=${BROWSER_VIEW_PORT}
        ...    offline=${RUN_OFFLINE}
        ...    recordVideo=${context_options['video_proprieties']}
        ...    recordHar=${context_options['har_proprieties']}
        ...    screen=${context_options['screen_dimensions']}
        ...    userAgent=${BROWSER_AGENT}
        ...    tracing=${context_options['tracing']}
        ...    url=${base_page}
    ${browser_session_info}    Convert Browser Details    ${browser_session_details}
    RETURN    ${browser_session_info}
    
Use Normal Context
    [Documentation]    Use the default context initializer
    [Arguments]    
        ...    ${context_options}
        ...    ${base_page}=${None}
    ${browser_details}    New Browser
        ...    browser=${BROWSER_FAMILY}
        ...    headless=${HEADLESS}
        ...    channel=${BROWSER_CHANNEL}
        ...    args=${BROWSER_ARGS}
        ...    downloadsPath=${DOWNLOADS_DIRECTORY_PATH}
        ...    devtools=${DEV_TOOLS}
        ...    chromiumSandbox=${CHROME_SECURITY_SANDBOX}

    ${context_details}    New Context
        ...    viewport=${BROWSER_VIEW_PORT}
        ...    offline=${RUN_OFFLINE}
        ...    recordVideo=${context_options['video_proprieties']}
        ...    recordHar=${context_options['har_proprieties']}
        ...    screen=${context_options['screen_dimensions']}
        ...    userAgent=${BROWSER_AGENT}
        ...    tracing=${context_options['tracing']}
    
    ${url_provided}    Is Not None    ${base_page}
    
    IF    ${url_provided}
        ${page_details}    Add New Page
            ...    init_url=${base_page}
            ...    wait_until=${DEFAULT_WAIT_PAGE_COMMIT_BEHAVIOR}
    END
    
    ${browser_session_info}    Convert Multiple Browser Details
        ...    ${browser_details}    
        ...    ${context_details}    
        ...    ${page_details}
        
    RETURN    ${browser_session_info}

Load Project Path
    [Documentation]    Read and Set The Project Root Path
    Set Global Variable    ${ROOT_PATH}    ${ROOT_PATH}
