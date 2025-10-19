*** Settings ***
Library     Collections
Library     Libraries/Utilities/Loggers.py
Resource    Resources/Configurations/Execution.resource


*** Keywords ***
Execution Variables Table
    [Documentation]    Logs a formatted table displaying execution-time values of key configuration variables.

        ${variables}    Create Dictionary

    ### Browser Setup ###
    Set To Dictionary    ${variables}
    ...    Context Type=${CONTEXT_TYPE}
    ...    Execution Environment=${EXECUTION_ENV}
    ...    Browser Family=${BROWSER_FAMILY}
    ...    Browser Channel=${BROWSER_CHANNEL}
    ...    Headless Mode=${HEADLESS}
    ...    Browser Arguments=${BROWSER_ARGS}
    ...    Viewport Size=${BROWSER_VIEW_PORT}
    ...    Offline Mode=${RUN_OFFLINE}
    ...    DevTools Enabled=${DEV_TOOLS}
    ...    Security Sandbox=${CHROME_SECURITY_SANDBOX}
    ...    Playwright Tracing=${PLAYWRIGHT_TRACING}
    ...    Development Mode=${DEVELOPMENT_ENVIRONMENT}
    ...    Video Recording=${RECORD_VIDEO}
    ...    CAPTCHA Solver=${CAPTCHA_SOLVER}

    ### HAR Capture ###
    Set To Dictionary    ${variables}
    ...    HAR Omit Content=${OMITCONTENT}
    ...    HAR Enabled=${ENABLE_HAR}
    ...    Platform Language=${PLATFORM_LANGUAGE}

    ### Window Settings ###
    Set To Dictionary    ${variables}
    ...    Window Width=${WINDOW_WIDTH}
    ...    Window Height=${WINDOW_HEIGHT}
    ...    Fullscreen Mode=${WINDOW_FULL}
    ...    Maximized Window=${WINDOW_MAXIMIZED}

    ### Timeouts ###
    Set To Dictionary    ${variables}
    ...    Browser Timeout=${BROWSER_TIMEOUT}

    ### Video Settings ###
    Set To Dictionary    ${variables}
    ...    Video Height=${VIDEO_HEIGHT}
    ...    Video Width=${VIDEO_WIDTH}

    Table Logger    table_contents=${variables}    table_title=Execution Configuration
