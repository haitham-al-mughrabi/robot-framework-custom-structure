*** Settings ***
Resource    root_path.resource

*** Variables ***
${DOWNLOADS_DIRECTORY_PATH}               ${root_path}${/}Resources${/}Downloads
${UPLOADS_DIRECTORY_PATH}                 ${root_path}${/}Resources${/}Uploads
${DEBUGGING_DIRECTORY_PATH}               ${root_path}${/}Results${/}Evidences
${VIDEO_RECORDING_DIRECTORY_PATH}         ${DEBUGGING_DIRECTORY_PATH}${/}Video
${RECORDED_TEST_EXECUTION_VIDEO_PATH}     ${None}
${HAR_RECORDING_DIRECTORY_PATH}           ${DEBUGGING_DIRECTORY_PATH}${/}HAR
${HAR_RECORDING_FILE_PATH}                ${HAR_RECORDING_DIRECTORY_PATH}${/}har_file.har
${PLAYWRIGHT_TRACING_FILE_PATH}           ${DEBUGGING_DIRECTORY_PATH}${/}PlayRightTracingFile.zip
