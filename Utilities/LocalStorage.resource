*** Settings ***
Library      Browser
Library      Collections
Library      String
Library      JSONLibrary
Library      Libraries/Utilities/VariableUtils.py

Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Utilities.py


*** Keywords ***
Globalize Local Storage Data
    [Documentation]    Capture all local storage from the browser
    ...                then populate all data as a global variable
    ...
    Sleep    5s       # Required to wait until local storage data got stored
    ${local_storage_object}=    Evaluate Javascript    html    window.localStorage
    Set Global Variable
        ...    ${LOCAL_STORAGE}   #Global Variable Name
        ...    ${local_storage_object}    #Value
    
Get Certain Data From Global Local Storage
    [Documentation]    Get a specific data from the global local
    ...                storage data object. Note that Globalize
    ...                Local Storage Data Keyword should be 
    ...                called first.
    [Arguments]        ${data_key}
    ${data_value}   Get From Dictionary
        ...    ${LOCAL_STORAGE}    # Dictionary
        ...    ${data_key}         # Given Key
        ...    None                # Default Value
    ${check_result}=    Is Not None      variable=${data_value}
    IF   ${check_result}
        ${data_value}    Strip String
            ...    ${data_value}
            ...    mode=both
            ...    characters="'${SPACE}
        RETURN    ${data_value}
    ELSE
        Fail    ${KEY_NOT_FOUND_IN_LOCAL_STORAGE('${data_key}')}
    END

Add A Value To Local Storage
    [Documentation]    Add A Value To Local Storage  
    [Arguments]   ${key}    ${value}
    Local Storage Set Item
        ...    key=${key}
        ...    value=${value}

    Log    Loading Access Token, Hang Tight!

    Sleep    5s
    
    Log    Reloading The Page To Apply Changes, Hang Tight!

    Reload
    
    Local Storage Get Item
        ...    key=${key}
        ...    assertion_operator===
        ...    assertion_expected=${value}
        ...    message=${DEFAULT_LOCAL_STORAGE_VALUE_NOT_FOUND_ERROR_MESSAGE}

    Log    ${DEFAULT_LOCAL_STORAGE_VALUE_ADDED_SUCCESSFULLY_MESSAGE}

Load Up Local Storage Items By JS
    [Documentation]    Get All Current Local Storage Items Using Javascript
    ${current_local_storage_items}    Evaluate Javascript
        ...    html    
        ...    ()=>{return localStorage}
    RETURN    ${current_local_storage_items}

Check If Local Storage Has A Certain Key
    [Documentation]    Check If Local Storage Has A Certain Key
    [Arguments]    
        ...    ${desired_key}
    ${current_local_storage_items}
        ...    Load Up Local Storage Items By JS
    ${ls_item}    Get From Dictionary
            ...    ${current_local_storage_items}
            ...    key=${desired_key}
            ...    default=${None}
    ${check_result}    Is Not None    
        ...    ${ls_item}
    RETURN    ${check_result}

Convert Local Storage Object To Dictionary
    [Documentation]    Convert Local Storage Object To Dictionary
    [Arguments]    
        ...    ${ls_object}
    ${ls_object}    Convert To Dictionary    ${ls_object}
    RETURN    ${ls_object}
    
Convert Local Storage Sub Object To Dictionary
    [Documentation]    
    [Arguments]    
        ...    ${sub_object}
    ${type}    Retrieve Variable Type    ${sub_object}
    Log    Object Type Is: ${type}
    ${sub_object}    Convert String To Json    ${sub_object}
    RETURN    ${sub_object}
