*** Settings ***
Library        Browser
Library        Collections
Library        Libraries/Utilities/StringOperations.py

*** Keywords ***
Check Page Scrollability
    [Documentation]    Checks if the page is scrollable or not using Java Script
    @{args}    Create List    
    ${isPageScrollable}    Evaluate Javascript    body    (elements,arg)=>{
        ...    const docElement = document.documentElement;
        ...    const isPageScrollable = docElement.scrollHeight > docElement.clientHeight;
        ...    return isPageScrollable;
        ...    }
        ...    arg=@{args}
    RETURN    ${isPageScrollable}

Add Attribute To Element Using Javascript
    [Documentation]    Add Attribute To Element Using Javascript
    [Arguments]    
        ...    ${element_locator}
        ...    ${attribute_name}
        ...    ${attribute_value}
    @{args}    Create List    
        ...    ${element_locator}
        ...    ${attribute_name}
        ...    ${attribute_value}
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    evaluated_element.setAttribute(arg[1], arg[2]);
        ...    }
        ...    arg=@{args}

Remove Attribute To Element Using Javascript
    [Documentation]    Remove Attribute To Element Using Javascript
    [Arguments]
        ...    ${element_locator}
        ...    ${attribute_name}
    @{args}    Create List
        ...    ${element_locator}
        ...    ${attribute_name}
    Evaluate Javascript    body    (elements,arg)=>{
        ...    let xpath_query = document.evaluate(
        ...        arg[0],
        ...        document,
        ...        null,
        ...        XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...        null
        ...    );
        ...    let evaluated_element = xpath_query.singleNodeValue;
        ...    evaluated_element.removeAttribute(arg[1]);
        ...    }
        ...    arg=@{args}

Element Has Attribute
    [Documentation]    Checks if an element has a specific attribute with robust null safety
    [Arguments]    ${xpath}    ${attribute_name}

    # Clean the XPath by removing newlines
    ${xpath}=    Replace In String    ${xpath}    \n    ${EMPTY}

    Log    Checking XPath: "${xpath}" for attribute: "${attribute_name}"    level=INFO

    @{args}=    Create List    ${xpath}    ${attribute_name}

    # First check if element exists to avoid JavaScript errors
    ${element_exists}=    Run Keyword And Return Status    Get Element Count    xpath=${xpath}    assertion_operator=>=    assertion_expected=1    message=XPath element not found

    IF    not ${element_exists}
        Log    Element with XPath '${xpath}' not found    level=WARN
        RETURN    ${FALSE}
    END

    # Now execute JavaScript with null safety
    ${result}=    Evaluate Javascript    body    (elements, arg) => {
        ...    try {
        ...        // Create XPath query
        ...        const xpath = arg[0];
        ...        const attributeName = arg[1];
        ...        console.log(`Checking XPath: "${xpath}" for attribute: "${attributeName}"`);
        ...
        ...        let xpath_query = document.evaluate(
        ...            xpath,
        ...            document,
        ...            null,
        ...            XPathResult.FIRST_ORDERED_NODE_TYPE,
        ...            null
        ...        );
        ...
        ...        // Get the element
        ...        let evaluated_element = xpath_query.singleNodeValue;
        ...
        ...        // Null safety check
        ...        if (!evaluated_element) {
        ...            console.warn(`No element found with XPath: ${xpath}`);
        ...            return { found: false, error: "Element not found" };
        ...        }
        ...
        ...        // Log element details
        ...        console.log("Found element:", evaluated_element);
        ...        console.log("Element tag:", evaluated_element.tagName);
        ...
        ...        // Check if element has attributes property
        ...        if (!evaluated_element.attributes) {
        ...            console.warn(`Element does not have attributes property`);
        ...            return { found: true, hasAttributes: false, attributes: {} };
        ...        }
        ...
        ...        // Gather attributes safely
        ...        const attributeMap = {};
        ...        Array.from(evaluated_element.attributes || []).forEach(attr => {
        ...            attributeMap[attr.name] = attr.value;
        ...        });
        ...
        ...        // Check for specific attribute
        ...        const hasAttribute = attributeName in attributeMap;
        ...
        ...        return {
        ...            found: true,
        ...            hasAttributes: true,
        ...            attributes: attributeMap,
        ...            hasRequestedAttribute: hasAttribute
        ...        };
        ...    } catch (error) {
        ...        console.error("Error in XPath evaluation:", error);
        ...        return {
        ...            found: false,
        ...            error: error.toString()
        ...        };
        ...    }
        ...    }
        ...    arg=@{args}
        ...    all_elements=${True}

    # Log the complete result for debugging
    Log    JavaScript result: ${result}    level=INFO

    # Handle different result scenarios
    IF    $result.get('error', None) != None
        Log    Error checking attributes: ${result}[error]    level=WARN
        RETURN    ${FALSE}
    END

    IF    not $result.get('found', False)
        Log    Element not found by JavaScript    level=WARN
        RETURN    ${FALSE}
    END

    IF    not $result.get('hasAttributes', False)
        Log    Element has no attributes    level=INFO
        RETURN    ${FALSE}
    END

    # Direct access to the pre-computed result
    ${has_attribute}=    Set Variable    ${result}[hasRequestedAttribute]

    # Additional logging for clarity
    IF    ${has_attribute}
        Log    Found attribute '${attribute_name}' with value '${result}[attributes][${attribute_name}]'    level=INFO
    ELSE
        Log    Attribute '${attribute_name}' not found in available attributes: ${result}[attributes]    level=INFO
    END

    RETURN    ${has_attribute}
