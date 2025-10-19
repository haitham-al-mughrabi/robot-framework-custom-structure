*** Settings ***
Library         Collections
Library         Libraries/Utilities/RandomDataGenerators.py
Library         Libraries/Utilities/VariableUtils.py

Resource        Utilities/Assertions.resource

Variables       Resources/Variables/Constants/CitiesGroups.py
Variables       Resources/Variables/Constants/Regions.py
Variables       Resources/Variables/Assertions/Utilities.py


*** Keywords ***
Get Random City From Random Saudi Arabia Region
    [Documentation]    Get Random City From Random Saudi Arabia Region
    ${region_dict}    Get Random Saudi Arabia Region
        ...    name_only=${False}
    ${city_dict}    Get Random Region City
        ...    region_name=${region_dict}
    ${region_and_city}    Create Dictionary
        ...    ar_region=${region_dict['ar_name']}
        ...    en_region=${region_dict['en_name']}
        ...    region_id=${region_dict['id']}
        ...    ar_city=${city_dict['ar_name']}
        ...    en_city=${city_dict['en_name']}
        ...    city_id=${city_dict['id']}
    RETURN    ${region_and_city}

Get Random Cities For The Same Region
    [Documentation]    Get Random Cities For The Same Region
    [Arguments]
        ...    ${region_dict}=${None}
        ...    ${number_of_cities}=${2}
    ${cities}    Create List

    ${is_data_provided}    Is Not None    ${region_dict}
    
    IF    not ${is_data_provided}
        ${region_dict}    Get Random Saudi Arabia Region
            ...    name_only=${False}
    END

    FOR    ${loop_index}    IN RANGE    ${number_of_cities}
        ${city_dict}    Get Random Region City
            ...    region_name=${region_dict}
        ${city_information}    Create Dictionary    
            ...    ar_city=${city_dict['ar_name']}
            ...    en_city=${city_dict['en_name']}
            ...    city_id=${city_dict['id']}
        Append To List    ${cities}    ${city_dict}
    END
    
    ${region_and_city}    Create Dictionary
        ...    ar_region=${region_dict['ar_name']}
        ...    en_region=${region_dict['en_name']}
        ...    region_id=${region_dict['id']}
        ...    cities=${cities}
    
    RETURN    ${region_and_city}
        
Get Random Saudi Arabia Region
    [Documentation]    Get Random Saudi Arabia Region
    [Arguments]    
        ...    ${name_only}=${True}
    ${selected_region_dict}    Get Random Item From List
        ...    my_list=${REGIONS}
    IF    ${name_only}
        RETURN    ${selected_region_dict['en_name']}
    END
    RETURN    ${selected_region_dict}

Get Random Region City
    [Documentation]    Get Random Region City
    [Arguments]    
        ...    ${region_name}
    ${value_type}    Retrieve Variable Type
        ...    variable=${region_name}
    IF    '$value_type' == 'str'
        No Operation
    ELSE IF    '$value_type = dict'
        ${region_name}    Set Variable    ${region_name['en_name']}
    ELSE
        Fail    ${NEGATIVE_VARIABLE_TYPE_ERROR('${value_type}')}
    END
    ${cities_group}    Get From Dictionary    
            ...    ${REGION_MAP}
            ...    ${region_name}
            ...    ${None}
    ${is_cities_group_none}    Is Not None    ${cities_group}
    IF    not ${is_cities_group_none}
        Fail    ${CITY_NOT_FOUND_IN_ENUM}
    END
    ${random_city_dict}    Get Random Item From List
        ...    my_list=${cities_group}
    RETURN    ${random_city_dict}
    