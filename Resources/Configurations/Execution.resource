*** Settings ***
Documentation     Define execution properties such as Browser Type, HEADLESS, and other configurations.
...               ⚠️ Important Notes:
...               - All default `None` values must remain unchanged in the script.
...               - These values should ONLY be modified using command-line arguments.
...               - Use the following format to set values during execution:
...                 `--variable variable_name:variable_value`
...               - For the complete list of configurable values and their descriptions, refer to the README file.


*** Variables ***
# Browser Setup
${CONTEXT_TYPE}                                  ${NONE}
${EXECUTION_ENV}                                 ${None}
${BROWSER_FAMILY}                                chromium
${BROWSER_CHANNEL}                               chromium
${HEADLESS}                                      ${None}
@{BROWSER_ARGS}                                  ${None}
${BROWSER_VIEW_PORT}                             ${None}
${RUN_OFFLINE}                                   ${None}
${DEV_TOOLS}                                     ${None}
${CHROME_SECURITY_SANDBOX}                       ${None}
${PLAYWRIGHT_TRACING}                            ${None}
${DEVELOPMENT_ENVIRONMENT}                       ${None}
${RECORD_VIDEO}                                  ${None}
${CAPTCHA_SOLVER}                                ${None}

# HAR
${OMITCONTENT}                                   ${None}    
${ENABLE_HAR}                                    ${None}
${PLATFORM_LANGUAGE}                              عربي

# Window resolution
${WINDOW_WIDTH}                                  ${None}
${WINDOW_HEIGHT}                                 ${None}
${WINDOW_FULL}                                   ${None}
${WINDOW_MAXIMIZED}                              ${None}

# Timeouts
${BROWSER_TIMEOUT}                               60s

# Video Dimensions
${VIDEO_HEIGHT}                                  1080
${VIDEO_WIDTH}                                   1920
