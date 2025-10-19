*** Settings ***
Library      Browser
Library      Libraries/Utilities/VariableUtils.py

Resource     Utilities/pyString.resource
Resource     POM/Keywords/UI/Generic/Getters.resource
Resource     Utilities/PageSupport.resource

Variables    Resources/Configurations/Baselines/DefaultBaseValues.py
Variables    Resources/Configurations/Baselines/DefaultTestsMessages.py
Variables    Resources/Variables/Assertions/Generics.py


*** Keywords ***
Generic Click Element
    [Documentation]    Generic Click Element
    [Arguments]    
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State    
            ...    ${element_locator}
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}
    END

    Click With Options
        ...    ${element_locator}
        ...    button=${DEFAULT_MOUSE_CLICK_ACTION}
        ...    clickCount=${DEFAULT_NUMBER_OF_MOUSE_CLICKS}

Generic Hover On Element
    [Documentation]    Generic Hover On Element
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END
    
    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}
    END
    
    Hover
        ...    ${element_locator}

Generic Menu Element Picker
    [Documentation]    Generic Menu Element Picker
    [Arguments]    
        ...    ${menu_locator}
        ...    ${menu_item_name}=${None}
        ...    ${menu_main_action}=click
        ...    ${custom_menu_item_locator}=${None}
        ...    ${wait_for_elements}=${True}
        ...    ${scroll_to_elements}=${True}
    ${menu_locator}    Strip Locator Text    ${menu_locator}
    IF    '${menu_main_action}' == 'click'
        Generic Click Element
            ...    element_locator=${menu_locator}
            ...    wait_for_element_state=${wait_for_elements}
            ...    scroll_to_element=${scroll_to_elements}
    ELSE IF    '${menu_main_action}' == 'hover'
        Generic Hover On Element    
            ...    element_locator=${menu_locator}
            ...    scroll_to_element=${wait_for_elements}
            ...    wait_for_element_state=${scroll_to_elements}
    ELSE
        Fail    Given Action Not Declared. Aborting!
    END
    
    ${menu_item_has_custom_locator}    Is Not None
        ...    ${custom_menu_item_locator}
    IF    ${menu_item_has_custom_locator}
        Generic Click Element
            ...    element_locator=${custom_menu_item_locator}
            ...    wait_for_element_state=${wait_for_elements}
            ...    scroll_to_element=${scroll_to_elements}
    ELSE
        ${menu_item_locator}    Generic XPath Creator By Element Attribute
            ...    attribute_value=${menu_item_name}
            ...    element_attribute=${TEXT_ATTRIBUTE_WITH_NORMALIZED_SPACES}
        Generic Click Element
            ...    element_locator=${menu_item_locator}
            ...    wait_for_element_state=${wait_for_elements}
            ...    scroll_to_element=${scroll_to_elements}
    END

Generic Click Element Using Javascript
    [Documentation]    Generic Click Element Using Javascript
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${check_action}=click
        ...    ${fire_click_natively}=${False}
        ...    ${take_screen_shot}=${False}
    ${element_locator}    Strip Locator Text    ${element_locator}
    IF    ${wait_for_element_state}
        Wait For Elements State
            ...    ${element_locator}
            ...    state=${DEFAULT_ELEMENT_VISIBLE_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}

        Wait For Elements State
            ...    ${element_locator}
            ...    state=${DEFAULT_ELEMENT_STATE}
            ...    timeout=${timeout}
            ...    message=${DEFAULT_ELEMENT_DOES_NOT_EXISTS_VALIDATION_MESSAGE}
    END

    IF    ${scroll_to_element}
        ${isPageScrollable}    Check Page Scrollability
        IF    ${isPageScrollable}
            Scroll To Element
                ...    ${element_locator}
        ELSE
            Log    Page is not scrollable. Scrolling Disabled.
        END
    END

    IF    ${take_screen_shot}
        Take Screenshot
            ...    selector=${element_locator}
    END

    @{args}    Create List      
        ...    ${element_locator}
        ...    ${check_action}
        ...    ${fire_click_natively}
    
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...        );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    if(arg[2]){
        ...        evaluated_element.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        ...        }
        ...    else{
        ...        evaluated_element.dispatchEvent(new Event(arg[1]));
        ...        }
        ...    
        ...    }
        ...    arg=@{args}

Generic Click Invisible Element
    [Documentation]    Generic Click Element Wrapper for elements that are hidden from user
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${take_screen_shot}=${False}
        ...    ${parent_wrapper}=${None}
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

    Click With Options
        ...    ${element_locator}
        ...    button=${DEFAULT_MOUSE_CLICK_ACTION}
        ...    clickCount=${DEFAULT_NUMBER_OF_MOUSE_CLICKS}

Generic Click Invisible Element Using Javascript
    [Documentation]    Generic Click Invisible Element Using Javascript
    [Arguments]
        ...    ${element_locator}
        ...    ${scroll_to_element}=${True}
        ...    ${wait_for_element_state}=${True}
        ...    ${timeout}=${DEFAULT_WAIT_ELEMENT_STATE_TIMEOUT}
        ...    ${check_action}=click
        ...    ${fire_click_natively}=${False}
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

    @{args}    Create List
        ...    ${element_locator}
        ...    ${check_action}
        ...    ${fire_click_natively}

    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...        );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    if(arg[2]){
        ...        evaluated_element.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        ...        }
        ...    else{
        ...        evaluated_element.dispatchEvent(new Event(arg[1]));
        ...        }
        ...
        ...    }
        ...    arg=@{args}
