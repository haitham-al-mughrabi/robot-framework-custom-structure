*** Settings ***
Library     DateTime
Library     String
Library     Collections
Library     Libraries/Utilities/MathOperations.py
Library     Libraries/Utilities/LogicalOperations.py
Resource    Utilities/pyString.resource


*** Keywords ***
Modify Today Date
    [Documentation]    Get Today's Date Then Modify The Date By
        ...            Either Add Or Subtract Days From Today's
        ...            Date.
    [Arguments]
        ...            ${action_value}
        ...            ${action}=Increment
        ...            ${reverse_date}=${False}
    ${today_date}    Get Todays Date And Or Time

    ${modified_date}    Increment Or Reduction Given Date
        ...    given_date=${today_date}
        ...    action=${action}
        ...    action_value=${action_value}

    ${reformatted_date}    Reformat Date
        ...        ${modified_date}
    IF    ${reverse_date}
        ${reformatted_date}    Reverse Data    
            ...    original_date=${reformatted_date}
    END
    
    RETURN        ${reformatted_date}
    
Get Todays Date And Or Time
    [Documentation]    Use Get Current Date To Get Todays Date.
        ...            You can get either the date or the time
        ...            or both values.
    [Arguments]        
        ...    ${date_only}=${False}
        ...    ${time_only}=${False}
        ...    ${date_format}=%d.%m.%Y %H:%M
        ...    ${date_seperator}=-
    
    ${date_format}=     Replace String Using Regexp
        ...    ${date_format}    # String
        ...    [.-/]    # Pattern
        ...    ${date_seperator}    # Replace with
        ...    count=${2}

    ${generated_date_time}    Get Current Date    time_zone=UTC    increment=3:00:00

    IF    not ${date_only} and not ${time_only}
        RETURN    ${generated_date_time}

    ELSE IF    ${date_only} and not ${time_only}
        ${optimized_date_format}    Split String
            ...    ${date_format}
            ...    separator=${SPACE}
            ...    max_split=1

        ${optimized_date_only}    Convert Date
            ...    ${generated_date_time}
            ...    result_format=${optimized_date_format[0]}

        RETURN    ${optimized_date_only}
    ELSE IF    not ${date_only} and ${time_only}
        ${optimized_date_format}    Split String
            ...    ${date_format}
            ...    separator=${SPACE}
            ...    max_split=1

        ${optimized_date_only}    Convert Date
            ...    ${generated_date_time}
            ...    result_format=${optimized_date_format[1]}

        RETURN    ${optimized_date_only}
    END

Increment Or Reduction Given Date
    [Documentation]    Increment Or Reduction Given Date
        ...    Accepted Action Values:
        ...    days, day, d
        ...    hours, hour, h
        ...    minutes, minute, mins, min, m
        ...    seconds, second, secs, sec, s
        ...    milliseconds, millisecond, millis, ms
        ...    microseconds, microsecond, us, μs (new in RF 6.0)
        ...    nanoseconds, nanosecond, ns (new in RF 6.0)
        ...    Example: 1 d, 7 s
    [Arguments]
        ...    ${given_date}
        ...    ${action}= Increment    # Increment / Reduction
        ...    ${action_value}= 1d
        ...    ${date_format}= ${None}
    
    IF    $action == 'Reduction'
        ${number}    Extract Numbers Using Regex    ${action_value}

        ${toggled_sign_number}    Toggle Sign    ${number}
        
        ${action_value}    Replace String
            ...    ${action_value}
            ...    Convert To String    ${number}
            ...    ${toggled_sign_number}

    END
    ${new_date}    Add Time To Date
        ...    ${given_date}      # date
        ...    ${action_value}    # Time

    IF    $date_format != ${None}
        ${date_format}    Convert Date
            ...    ${date_format}    # Date
            ...    date_format=${date_format}
    END

    RETURN    ${new_date}
    
Reformat Date
    [Documentation]    Get Date From DateTime Variable
    [Arguments]  
        ...    ${date_string}
        ...    ${date_seperator}=-
    ${optimized_date_format}    Split String
            ...    ${date_string}
            ...    separator=${SPACE}
            ...    max_split=1
    RETURN    ${optimized_date_format[0]}

Get Date Or Time From DateTime String
    [Documentation]    Get Date Or Time From DateTime String
    [Arguments]
        ...    ${datetime_string}
        ...    ${date_or_time}=Date
    @{separated_date_time}    Split String
        ...    ${datetime_string}
        ...    ${SPACE}
    IF    '${date_or_time}' == 'Date'
        RETURN    ${separated_date_time[0]}
    ELSE
        RETURN    ${separated_date_time[-1]}
    END

Reverse Data
    [Documentation]    Reverse Data
    [Arguments]    
        ...    ${original_date}
        ...    ${date_seperator}=-
        
    @{date_as_list}    Split String    
        ...    string=${original_date}
        ...    separator=${date_seperator}
    Reverse List
        ...    ${date_as_list}
    ${reversed_date}    Join String    
        ...    ${date_as_list}
        ...    separator=${date_seperator}
    RETURN    ${reversed_date}
    