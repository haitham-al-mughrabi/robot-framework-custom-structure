*** Settings ***
Resource    Utilities/AlertIntegration.resource


*** Keywords ***
Generic Custom Automation Alertion
    [Documentation]    Displays a customizable alert on the screen.
        ...    Arguments:
        ...    alert_title (str): The title of the alert.
        ...    alert_context (str): The main content or body of the alert.
        ...    timeout (int): Duration in milliseconds before the alert disappears. Default is 5000.
        ...    status_index (int): Alert type index (0: Success, 1: Error, 2: Info,
        ...        3: Warning, 4: Critical, 5: Debug). Default is 0.
        ...    context_direction (str): Text direction ("ltr" or "rtl"). Default is "rtl".
        ...    alert_position (int): Screen position index (0: Top-Left, 1: Top-Middle, 2: Top-Right,
        ...        3: Bottom-Left, 4: Bottom-Middle, 5: Bottom-Right). Default is 5.
    [Arguments]
        ...    ${alert_title}
        ...    ${alert_context}
        ...    ${timeout}=5000
        ...    ${status_index}=${0}
        ...    ${context_direction}=rtl
        ...    ${alert_position}=${5}
        ...    ${add_sleep}=${False}
        ...    ${sleep_duration}=1s
    Load Alert System Resources
    Add Custom Automation Alert
        ...    alert_title=${alert_title}
        ...    alert_context=${alert_context}
        ...    timeout=${timeout}
        ...    status_index=${status_index}
        ...    context_direction=${context_direction}
        ...    alert_position=${alert_position}
    IF    ${add_sleep}
       Sleep    ${sleep_duration}    ${alert_context}
    END
