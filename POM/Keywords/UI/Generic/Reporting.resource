*** Settings ***
Resource    Utilities/FileDirOperations.resource


*** Keywords ***
Add Image Source To Logs
    [Documentation]    Add Image Source To Logs
    [Arguments]    
        ...    ${image_path}
        ...    ${image_width}=600px
    Log    <img src="${image_path}" width="${image_width}">    html=True

Add Video Source To Logs
    [Documentation]    Add Video Source To Logs
    [Arguments]
        ...    ${video_path}
        ...    ${video_width}=600   
    Log    <video width="${video_width}" controls><source src="${VIDEO_PATH}" type="video/webm">Execution</video>
        ...    html=True

Add Multiple Video Sources To Logs
    [Documentation]    Add Multiple Video Sources To Logs
    [Arguments]    
        ...    ${directory_path}
    ${videos_files}    Get Directory Files Names    ${directory_path}
    FOR    ${video_file}    IN    @{videos_files}
        Add Video Source To Logs
            ...    video_path=${directory_path}${/}${video_file}
    END
