*** Settings ***
Documentation       Set setup, teardown and global variables values.
Library             Collections
Library             Browser
Library             String

Resource            Resources/Configurations/Execution.resource
Resource            Resources/Variables/FilePaths/Extensions.resource

Variables           Resources/DataSources/Setup/BrowserConfigurations.py
Variables           Resources/Configurations/Baselines/DefaultBaseValues.py
Variables           Resources/Configurations/Baselines/DefaultTestsMessages.py


*** Keywords ***
Configure Browser Arguments
    [Documentation]    Configure Browser Arguments Values.
        ...            This option is automatically configured based on the ${EXECUTION_ENV} value.
        ...            ⚠️ Do not change the value from `NONE` unless you are testing something specific.
        ...            For normal execution, please ensure the value remains set to `NONE`.

    @{shared_browser_configuration}     Copy List
        ...    ${browser_arguments["shared"]}
        ...    deepcopy=${True}
    IF    ${WINDOW_FULL}
        Append To List
            ...    ${shared_browser_configuration}
            ...    --start-fullscreen
    END

    IF    ${WINDOW_MAXIMIZED}
        Append To List
            ...    ${shared_browser_configuration}
            ...    --start-maximized
    END

    IF    ${CAPTCHA_SOLVER}
        Append To List    ${shared_browser_configuration}
            ...    --disable-extensions-except=${NOPE_CAPTCHA_SOLVER_PATH}
            ...    --load-extension=${NOPE_CAPTCHA_SOLVER_PATH}
    END
    Append To List    ${shared_browser_configuration}
        ...    --window-size=${WINDOW_WIDTH},${WINDOW_HEIGHT}

    IF    '$EXECUTION_ENV == local' and ${HEADLESS}
        Append To List    ${shared_browser_configuration}
            ...    --headless=new
        Log    Headless has been set for local execution
    END

    Set Global Variable
        ...    @{BROWSER_ARGS}
        ...    @{shared_browser_configuration}

    RETURN    @{shared_browser_configuration}

Convert Browser Details
    [Documentation]    Converts Browser library details (tuple, dict, or string) into a structured dictionary format
    [Arguments]    ${details}
    ${result_dict}=    Create Dictionary

    # Check input type
    ${is_tuple}=    Evaluate    isinstance($details, tuple)
    ${is_dict}=    Evaluate    isinstance($details, dict)
    ${is_string}=    Evaluate    isinstance($details, str)

    # Process string input
    IF    ${is_string}
        ${matches}=    Run Keyword And Return Status    Should Match Regexp    ${details}    ^[^=]+=.+$
        IF    ${matches}
            ${type_and_id}=    Split String    ${details}    =
            ${type}=    Set Variable    ${type_and_id}[0]
            ${id}=    Set Variable    ${type_and_id}[1]
            Set To Dictionary    ${result_dict}    ${type}=${id}
        ELSE
            Log    Non-matching string format: ${details}
        END
    # Process tuple
    ELSE IF    ${is_tuple}
        FOR    ${item}    IN    @{details}
            ${is_string}=    Evaluate    isinstance($item, str)
            ${is_dict}=    Evaluate    isinstance($item, dict)

            # Process string items with format 'type=uuid'
            IF    ${is_string}
                ${matches}=    Run Keyword And Return Status    Should Match Regexp    ${item}    ^[^=]+=.+$
                IF    ${matches}
                    ${type_and_id}=    Split String    ${item}    =
                    ${type}=    Set Variable    ${type_and_id}[0]
                    ${id}=    Set Variable    ${type_and_id}[1]
                    Set To Dictionary    ${result_dict}    ${type}=${id}
                ELSE
                    # Handle other string formats if needed
                    Log    Non-matching string format: ${item}
                END
            # Process nested dictionary
            ELSE IF    ${is_dict}
                FOR    ${key}    ${value}    IN    &{item}
                    ${is_str_value}=    Evaluate    isinstance($value, str)
                    IF    ${is_str_value}
                        ${matches}=    Run Keyword And Return Status    Should Match Regexp    ${value}    ^[^=]+=.+$
                        IF    ${matches} and '${key}' == 'page_id'
                            ${type_and_id}=    Split String    ${value}    =
                            ${type}=    Set Variable    ${type_and_id}[0]
                            ${id}=    Set Variable    ${type_and_id}[1]
                            Set To Dictionary    ${result_dict}    ${type}=${id}
                        ELSE
                            Set To Dictionary    ${result_dict}    ${key}=${value}
                        END
                    ELSE
                        Set To Dictionary    ${result_dict}    ${key}=${value}
                    END
                END
            END
        END
    # Process dictionary
    ELSE IF    ${is_dict}
        FOR    ${key}    ${value}    IN    &{details}
            ${is_str_value}=    Evaluate    isinstance($value, str)
            IF    ${is_str_value}
                ${matches}=    Run Keyword And Return Status    Should Match Regexp    ${value}    ^[^=]+=.+$
                IF    ${matches}
                    ${type_and_id}=    Split String    ${value}    =
                    ${type}=    Set Variable    ${type_and_id}[0]
                    ${id}=    Set Variable    ${type_and_id}[1]
                    Set To Dictionary    ${result_dict}    ${type}=${id}
                ELSE
                    Set To Dictionary    ${result_dict}    ${key}=${value}
                END
            ELSE
                Set To Dictionary    ${result_dict}    ${key}=${value}
            END
        END
    ELSE
        Log    Unsupported input type: ${details}
    END

    RETURN    ${result_dict}

Convert Multiple Browser Details
    [Documentation]    Converts multiple Browser library details into a single consolidated dictionary
    [Arguments]    @{details_list}
    ${result_dict}=    Create Dictionary

    # Process each item passed as an argument
    FOR    ${details_item}    IN    @{details_list}
        # Convert the current item to a dictionary
        ${converted_dict}=    Convert Browser Details    ${details_item}

        # Merge the converted dictionary into our result dictionary
        FOR    ${key}    ${value}    IN    &{converted_dict}
            Set To Dictionary    ${result_dict}    ${key}=${value}
        END
    END

    RETURN    ${result_dict}
    
Globalize Browser Variables
    [Documentation]    Set Browser Variables as Test Level Variables
    [Arguments]    
        ...    ${browser_session_info}
    Set Test Variable    ${BROWSER_ID}    ${browser_session_info['browser']}    
    Set Test Variable    ${CONTEXT_ID}    ${browser_session_info['context']}    
    Set Test Variable    ${PAGE_ID}    ${browser_session_info['page']}    
    Set Test Variable    ${VIDEO_PATH}    ${browser_session_info['video_path']}    
    