*** Settings ***
Library      OperatingSystem
Library      String
Library      Libraries/Utilities/VariableUtils.py
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Utilities.py


*** Keywords ***
Check & Create Directory
    [Documentation]    Check & Create Directory
    [Arguments]    
        ...    ${directory_path}
    ${is_created}    Run Keyword And Return Status
        ...    Directory Should Exist
            ...    path=${directory_path}
    IF    not ${is_created}
        Create Directory
            ...    ${directory_path}
    ELSE
        Log    ${DIRECTORY_FOUND_PATH_MESSAGE('$directory_path')}
    END

Check & Create File
    [Documentation]    Check & Create File
    [Arguments]
        ...    ${file_path}
        ...    ${content}=${None}
        ...    ${encoding}=${DEFAULT_FILE_ENCODING}
    ${is_created}    Run Keyword And Return Status
        ...    File Should Exist
            ...    path=${file_path}
    IF    not ${is_created}
        Create File
            ...    ${file_path}
            ...    content=${content}
            ...    encoding=${encoding}
    ELSE
        ${log_message}    Set Variable    ${FILE_FOUND_PATH_MESSAGE('$file_path')}
        Log    ${log_message}
    END

Check & Delete Directory
    [Documentation]    Check & Delete Directory
    [Arguments]
        ...    ${directory_path}
        ...    ${remove_sub_directories}=${False}
    ${is_created}    Run Keyword And Return Status
        ...    Directory Should Exist
            ...    path=${directory_path}
    IF    ${is_created}
        Remove Directory
            ...    ${directory_path}
            ...    recursive=${remove_sub_directories}
    ELSE
        Log    ${DIRECTORY_ALREADY_DELETED_MESSAGE}
    END

Check & Delete File
    [Documentation]    Check File Existence & Delete File
    [Arguments]
        ...    ${file_path}
    ${is_exists}    Run Keyword And Return Status
        ...    File Should Exist
            ...    path=${file_path}
    IF    ${is_exists}
        Remove File
            ...    ${file_path}
    ELSE
        Log    ${FILE_ALREADY_DELETED_MESSAGE}
    END

Check & Remove All Directory Files
    [Documentation]    Check & Remove All Directory Files
    [Arguments]
        ...    ${directory_path}
    ${is_created}    Run Keyword And Return Status
        ...    Directory Should Exist
            ...    path=${directory_path}
    IF    ${is_created}
        Empty Directory
            ...    ${directory_path}
    ELSE
        Log    ${DIRECTORY_ALREADY_DELETED_MESSAGE}
    END

Check & Move Single File
    [Documentation]    Check & Move Single File
    [Arguments]    
        ...    ${source_file_path}
        ...    ${destination_folder_path}
    ${is_file_exists}    Run Keyword And Return Status
        ...    File Should Exist
            ...    path=${source_file_path}
    ${is_destination_created}    Run Keyword And Return Status
        ...    Directory Should Exist
            ...    path=${destination_folder_path}
    IF    ${is_file_exists} and ${is_destination_created}
        Move File    
            ...    source=${source_file_path}
            ...    destination=${destination_folder_path}
    ELSE IF    not ${is_file_exists}
         Fail    ${FILE_NOT_EXISTS_MESSAGE('$source_file_path')}
    ELSE IF    not ${is_destination_created}
        Fail    ${DIRECTORY_NOT_EXISTS_MESSAGE('$destination_folder_path')}
    END

Check & Rename A Single File
    [Documentation]    Check & Rename A Single File
    [Arguments]    
        ...    ${directory_path}
        ...    ${new_file_name}
        ...    ${file_extension}
        ...    ${cur_file_name}=${None}
   
    ${is_current_name_provided}    Is Not None
        ...    passed_variable=${cur_file_name}
    IF    not ${is_current_name_provided}
        ${cur_file_name}    Check & Get Single File Name
            ...    directory_path=${directory_path}
            ...    file_extension=${file_extension}
    END
    ${original_file_path}    Set Variable
        ...    ${directory_path}${/}${cur_file_name}${file_extension}
    ${new_file_path}    Set Variable    
        ...    ${directory_path}${/}${new_file_name}${file_extension}
    Sleep    1min
    Move File    
        ...    ${original_file_path}
        ...    ${new_file_path}
    RETURN    ${new_file_path}

Check & Get Single File Name
    [Documentation]    Check & Get Single File Name
    [Arguments]    
        ...    ${directory_path}
        ...    ${file_extension}=${DEFAULT_FILE_EXTENSION}
        ...    ${return_with_extension}=${False}
    ${is_directory_created}    Run Keyword And Return Status
        ...    Directory Should Exist
            ...    path=${directory_path}
    IF    ${is_directory_created}
        ${pattern}    Set Variable
            ...    *${file_extension}
            
        @{matches}    List Directory
            ...    path=${directory_path}
            ...    pattern=${pattern}
        ${file_name}    Set Variable    ${matches[0]}
        IF    not ${return_with_extension}
            @{file_name_with_extension}    Split String
                ...    ${file_name}
                ...    ${DEFAULT_FILE_SEPERATOR}
            ${file_name}    Set Variable
                ...    ${file_name_with_extension[0]}
        END
        
        RETURN    ${file_name}
    ELSE
        Fail    ${DIRECTORY_NOT_EXISTS_MESSAGE('$directory_path')}
    END

Get File Name & Extension From Path
    [Documentation]    Get File Name & Extension From Path
    [Arguments]    
        ...    ${file_path}
        ...    ${splitter}=${DEFAULT_PATH_SEPERATOR}
    @{split_path}    Split String
        ...    ${file_path}
        ...    ${splitter}
    @{file_name_with_extension}    Split String    
        ...    ${split_path[-1]}
        ...    ${DEFAULT_FILE_SEPERATOR}
    &{file_info}    Create Dictionary
        ...    file_name=${file_name_with_extension[0]}
        ...    file_extension=${file_name_with_extension[-1]}
    RETURN    &{file_info}

Get Directory Files Names
    [Documentation]    Get Directory Files Names
    [Arguments]    
        ...    ${directory_path}
    ${directory_files}    List Files In Directory    ${directory_path}
    RETURN    ${directory_files}
    