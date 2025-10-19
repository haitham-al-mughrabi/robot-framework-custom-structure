*** Settings ***
Library      Browser
Resource     Utilities/pyString.resource
Resource     Utilities/PageSupport.resource
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py


*** Keywords ***
Generic Fill Input Field Element
    [Documentation]    Generic keyword to fill an input field element with the provided text.
    [Arguments]
        ...    ${element_locator}                 # The locator of the element to be filled.
        ...    ${text_to_fill}                    # The text to fill into the input field.
        ...    ${scroll_to_element}=${True}       # Boolean flag to scroll to the element before filling. Defaults to True.
        ...    ${wait_for_element_state}=${True}  # Boolean flag to wait for the element state before filling. Defaults to True.
        ...    ${secret_txt}=${False}             # Boolean flag to indicate if the text is secret (e.g., password). Defaults to False.
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}/parent::*
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}/parent::*
    END

    IF    ${secret_txt}
        Type Secret
            ...    ${element_locator}
            ...    secret=$text_to_fill
            ...    delay=${DEFAULT_SINGLE_KEY_STROKES}
            ...    clear=${DEFAULT_CLEAR_INPUT_FIELD_ACTION}
    ELSE
        Type Text
            ...    ${element_locator}
            ...    txt=${text_to_fill}
            ...    delay=${DEFAULT_SINGLE_KEY_STROKES}
            ...    clear=${DEFAULT_CLEAR_INPUT_FIELD_ACTION}
    END

Generic Unfilled Input Field Element
    [Documentation]    Generic keyword to unfilled an input field element.
    [Arguments]
        ...    ${element_locator}                 # The locator of the element to be unfilled.
        ...    ${scroll_to_element}=${True}       # Boolean flag to scroll to the element before infilling.
        ...    ${wait_for_element_state}=${True}  # Boolean flag to wait for the element state before infilling.
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}/parent::*
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    TRY
        ${input_field_type}    Get Attribute
            ...    ${element_locator}
            ...    attribute=inputmode
    EXCEPT    
        ${input_field_type}    Get Attribute
            ...    ${element_locator}
            ...    attribute=type
    END
    
    IF    $input_field_type == 'tel'
        ${place_holder_txt}    Set Variable    123
    ELSE IF    $input_field_type == 'text'
        ${place_holder_txt}    Set Variable    ABC
    END    

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}/parent::*
    END

    Type Text
        ...    selector=${element_locator}
        ...    txt=${place_holder_txt}
        ...    delay=${DEFAULT_SINGLE_KEY_STROKES}
        ...    clear=${DEFAULT_CLEAR_INPUT_FIELD_ACTION}

    Clear Text    
        ...    selector=${element_locator}

Fill Input Field Using Javascript
    [Documentation]    Fill Input Field Using Javascript
    [Arguments]
        ...    ${element_locator}                 # The locator of the element to be filled.
        ...    ${text_to_fill}                    # The text to fill into the input field.
        ...    ${scroll_to_element}=${True}       # Boolean flag to scroll to the element before filling. Defaults to True.
        ...    ${wait_for_element_state}=${True}  # Boolean flag to wait for the element state before filling. Defaults to True.
        ...    ${trigger_action}=${False}
        ...    ${action}=${None}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}/parent::*
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}/parent::*
    END

    @{args}    Create List
          ...    ${element_locator}
          ...    ${text_to_fill}
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    evaluated_element.value=arg[1];
        ...    }
        ...    arg=@{args}

    IF    ${trigger_action}
        @{args}    Set Variable
        ...    ${element_locator}
        ...    ${action}

        Evaluate Javascript    body    (elements,arg)=>{
                ...    let xpath_query = document.evaluate(
            ...        arg[0],
            ...        document,
            ...        null,
            ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
            ...        null
            ...    );
            ...    let evaluated_element = xpath_query.singleNodeValue;
            ...    evaluated_element.dispatchEvent(new Event(arg[1]))
            ...    }
            ...    arg=@{args}
    END
