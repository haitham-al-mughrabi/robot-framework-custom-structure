from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library(doc_format = 'ROBOT')
class BrowserScripting:
    def __init__(self):
        self.builtin = BuiltIn()
        BuiltIn().import_library('Browser')
        self.browser = BuiltIn().get_library_instance('Browser')

    @keyword(name = "Run Javascript Script")
    def run_js_script(self, script_string: str, args: [ list, str, int, dict, None ], element_wrapper: str = "html",
                      customized_wrapper: [ str, None ] = None, all_elements: bool = False,
                      return_values: bool = False):
        js_function = "(elements,arg)=>" + "{" + script_string + "}"
        if customized_wrapper is not None:
            js_function = customized_wrapper
        print(js_function)
        execution_result = self.browser.evaluate_javascript(element_wrapper, js_function, arg = args,
                                                            all_elements = all_elements)
        if return_values:
            return execution_result

    @keyword(name = "Add To HTML Element")
    def add_to_html_element(self, element_locator: str, args: [ None, list ], options: [ None, dict ] = None) -> None:
        """
        :param element_locator: The locator for the HTML element (e.g., XPath or CSS selector).
        :param args: A list of actions to perform on the element. Each action is a dictionary with 'attribute' and 'value'.
        :param options: Additional options like 'locator_wrapper', 'element_wrapper', etc.
        :return: None
        """
        js_string = f"""
        let element = document.evaluate(`{element_locator}`, {getattr(options, 'locator_wrapper', 'document')}, null,
XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        """
        for arg in args:
            js_string = js_string + f"element.{arg[ 'attribute' ]} = '{arg[ 'value' ]}';\n"
        self.run_js_script(script_string = js_string, args = None,
                           element_wrapper = getattr(options, 'element_wrapper', 'html'))

    @keyword(name = "Change HTML Element")
    def change_html_element(self, element_locator: str, args: [ None, list ], options: [ None, dict ] = None) -> None:
        """
        :param element_locator: The locator for the HTML element (e.g., XPath or CSS selector).
        :param args: A list of actions to perform on the element. Each action is a dictionary with 'attribute' and 'value'.
        :param options: Additional options like 'locator_wrapper', 'element_wrapper', etc.
        :return: None
        """
        self.browser.take_screenshot()
        js_string = f"""
            let element = document.evaluate(`{element_locator}`, {getattr(options, 'locator_wrapper', 'document')}, null,
    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            """
        for arg in args:
            if arg[ 'action' ] == "command":
                js_string = js_string + f"element.{arg[ 'attribute' ]} = '{arg[ 'value' ]}';"
            elif arg[ 'action' ] == "function":
                js_string = js_string + f"element.{arg[ 'function' ]};"
        self.run_js_script(script_string = js_string, args = None,
                           element_wrapper = getattr(options, 'element_wrapper', 'html'))
