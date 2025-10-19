from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library(doc_format='ROBOT')
class EnhancedScreenshot:
    def __init__(self):
        self.builtin = BuiltIn()
        BuiltIn().import_library('Browser')
        self.browser = BuiltIn().get_library_instance('Browser')

    @keyword("Enhanced Element Screenshot")
    def enhanced_element_screenshot(self, element_locator: str, outline_configurations="pass"):
        """
        Wrap element that you want to take a screenshot of with a wrapper to appear clearly on the screenshot
        """
        if outline_configurations == "pass":
            outline_configurations = {"outlineColor": "green",
                                      "outlineThickness": "6px",
                                      "outlineOffset": "10px"}
        elif outline_configurations == "fail" or outline_configurations == "failed":
            outline_configurations = {"outlineColor": "red",
                                      "outlineThickness": "6px",
                                      "outlineOffset": "10px"}
        configurations = [element_locator, outline_configurations]
        js_code = """(elements,arg)=>{
        let element = document.evaluate(arg[0],document ,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue;
        element.style.outlineOffset = arg[1].outlineOffset;
        element.style.outline = arg[1].outlineThickness+ ' solid ' + arg[1].outlineColor;
        };
        """
        self.browser.evaluate_javascript('html', js_code, arg=configurations, all_elements=False)
        self.browser.take_screenshot(fullPage=True, log_screenshot=True)
        js_code = """(elements,arg)=>{
        let element = document.evaluate(arg[0],document ,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue;
        element.style.outlineOffset = '';
        element.style.outline = '';
        };
        """
        self.browser.evaluate_javascript('html', js_code, arg=configurations, all_elements=False)
