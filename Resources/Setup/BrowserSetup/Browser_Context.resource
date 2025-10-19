*** Settings ***
Documentation       Set setup, teardown and global variables values.
Library             Collections
Library             Browser

Resource            Utilities/FileDirOperations.resource
Resource            Resources/Configurations/Execution.resource
Resource            Resources/Variables/FilePaths/Configurations.resource

Variables           Resources/DataSources/Setup/BrowserConfigurations.py
Variables           Resources/Configurations/Baselines/DefaultBaseValues.py
Variables           Resources/Configurations/Baselines/DefaultTestsMessages.py


*** Keywords ***
Setup Browser Context
    [Documentation]    Setup Browser Context
    # Creates Debug Directory
    Check & Create Directory    directory_path=${DEBUGGING_DIRECTORY_PATH}

    # Define Data Wrappers
    ${context_options}=    Prepare Context Options
    RETURN    ${context_options}

Prepare Context Options
    [Documentation]    Prepares browser context options by configuring video recording, HAR recording, 
        ...    Playwright tracing and screen dimensions. This keyword initializes necessary properties to configure
        ...    the Browser context with appropriate recording settings.
        ...    Returns a dictionary containing all the configured options for the browser context.
    # Initialize Basic Values
    ${tracing_file_path}=    Set Variable    ${None}
    ${video_proprieties}=    Set Variable    ${None}
    ${har_proprieties}=      Set Variable    ${None}

    # Configure Optional Recording Features
    ${video_proprieties}=    Configure Video Recording    ${RECORD_VIDEO}
    ${har_proprieties}=      Configure HAR Recording      ${ENABLE_HAR}
    ${tracing_file_path}=    Configure Playwright Tracing    ${PLAYWRIGHT_TRACING}

    # Set Screen Dimensions
    ${screen_dimensions}=    Create Dictionary
    ...    height=${WINDOW_HEIGHT}
    ...    width=${WINDOW_WIDTH}

    ${context_options}=    Create Dictionary
    ...    video_proprieties=${video_proprieties}
    ...    screen_dimensions=${screen_dimensions}
    ...    har_proprieties=${har_proprieties}
    ...    tracing=${tracing_file_path}

    RETURN    ${context_options}

Configure Video Recording
    [Arguments]    ${record_video}
    ${video_proprieties}=    Set Variable    ${None}

    IF    ${record_video}
        ${test_video_path}=    Prepare Video Directory Path
        ${video_dimensions}=    Create Dictionary
        ...    width=${VIDEO_WIDTH}
        ...    height=${VIDEO_HEIGHT}

        ${video_proprieties}=    Create Dictionary
        ...    dir=${test_video_path}
        ...    size=${video_dimensions}

        Set Global Variable    ${RECORDED_TEST_EXECUTION_VIDEO_PATH}    ${test_video_path}
    END

    RETURN    ${video_proprieties}

Define video Directory Path
    [Documentation]    Define video Directory Path

Prepare Video Directory Path
    Check & Create Directory    directory_path=${VIDEO_RECORDING_DIRECTORY_PATH}

    ${optimized_suite_name}=    Replace String    ${SUITE_NAME}    ${SPACE}    ${EMPTY}
    ${optimized_suite_name}=    Replace String    ${optimized_suite_name}    -    ${EMPTY}

    @{sub_directories}=    Split String    ${optimized_suite_name}    separator=.
    @{sub_directories}=    Set Variable    ${sub_directories[2:]}

    ${test_video_path}=    Set Variable    ${VIDEO_RECORDING_DIRECTORY_PATH}

    FOR    ${sub_directory}    IN    @{sub_directories}
        ${test_video_path}=    Catenate    SEPARATOR=${/}    ${test_video_path}    ${sub_directory}
        Check & Create Directory    directory_path=${test_video_path}
    END

    ${split_test_name}=    Split String    ${TEST NAME}    ${SPACE}    ${1}
    ${optimized_test_name}=    Set Variable    ${split_test_name[0]}
    ${test_video_path}=    Set Variable    ${test_video_path}${/}${optimized_test_name}

    Check & Create Directory    directory_path=${test_video_path}

    RETURN    ${test_video_path}

Configure HAR Recording
    [Arguments]    ${enable_har}
    ${har_proprieties}=    Set Variable    ${None}

    IF    ${enable_har}
        Check & Create Directory    directory_path=${HAR_RECORDING_DIRECTORY_PATH}
        Check & Delete File    file_path=${HAR_RECORDING_FILE_PATH}

        ${har_proprieties}=    Create Dictionary
        ...    omitContent=${OMITCONTENT}
        ...    path=${HAR_RECORDING_FILE_PATH}
    END

    RETURN    ${har_proprieties}

Configure Playwright Tracing
    [Arguments]    ${playwright_tracing}
    ${tracing_file_path}=    Set Variable    ${None}

    IF    ${playwright_tracing}
        Check & Delete File    file_path=${PLAYWRIGHT_TRACING_FILE_PATH}
        Check & Create File    file_path=${PLAYWRIGHT_TRACING_FILE_PATH}    content=${EMPTY}
        ${tracing_file_path}=    Set Variable    ${PLAYWRIGHT_TRACING_FILE_PATH}
    END

    RETURN    ${tracing_file_path}
