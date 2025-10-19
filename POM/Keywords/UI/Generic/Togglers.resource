*** Settings ***
Library      Browser
Resource     Utilities/pyString.resource
Resource     Utilities/PageSupport.resource
Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py

*** Keywords ***
Toggle An Toggler
    [Documentation]    Switch On Or Off A Toggler [Checkbox, Radio Button (Only On), Other 
        ...            Types That acts as a toggler as long as its type is checkbox or radio]
    [Arguments]    
        ...    ${element_locator}
        ...    ${checked}
        ...    ${take_screen_shot}=${False}
        ...    ${scroll_to_element}=${True}
    ${element_locator}    Strip Locator Text    ${element_locator}
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
            ...    selector=${element_locator}
    END
    @{args}    Create List      ${element_locator}    ${checked}
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    let checked_status = evaluated_element.checked;
        ...    if (arg[1] != checked_status){
        ...        evaluated_element.checked=arg[1]
        ...        evaluated_element.dispatchEvent(new Event("change"))
        ...        }
        ...    }
        ...    arg=@{args}
            
Generic Check Element
    [Documentation]    Generic Check Element
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
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
            ...    selector=${element_locator}
    END
    
    Check Checkbox    
        ...    ${element_locator}

Generic Check Element Using Javascript
    [Documentation]    Generic Check Element Using Javascript
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${check_action}=change
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
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
    
    @{args}    Create List      ${element_locator}    ${check_action}
    
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    evaluated_element.checked=true
        ...    evaluated_element.dispatchEvent(new Event(arg[1]))
        ...    }
        ...    arg=@{args}

Generic Uncheck Element
    [Documentation]    Generic Uncheck Element
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
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
    
    Uncheck Checkbox
        ...    ${element_locator}

Generic Uncheck Element Using Javascript
    [Documentation]    Generic Uncheck Element Using Javascript
    [Arguments]
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${uncheck_action}=change
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}/parent::*
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
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

    @{args}    Create List      ${element_locator}    ${uncheck_action}
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    evaluated_element.checked=false
        ...    evaluated_element.dispatchEvent(new Event(arg[1]))
        ...    }
        ...    arg=@{args}
