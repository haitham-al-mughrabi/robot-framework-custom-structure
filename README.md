# Setup Instructions

---

# Project and IDE installation

**1. Download your favorite IDE >> [Pycharm, RIDE, VSCode]**

**2. Clone the desired project using Git, then open it in your favorite IDE. If you have the option to select the
default python version, please select 3.9.x**

---

# Python - Pyenv

**1. Python 3.9.x is required in order to use poetry, if you don't have python version 3.9.x (x stands for any sub
version), please install pyenv to handle the process of installing and switching to the specified python version:**

    https://github.com/pyenv/pyenv

_For windows please follow these instructions:_

    https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#powershell

_To install python version 3.9.x, please use the following command:_

> Please note that you can use any sub version you like, 3.9.13 is just a sample for demonstrating the installation
> process.

    pyenv install 3.9.13

_To change the python version, please use the following command_

    pyenv shell 3.9.13

> Required - must run it before use poetry for the first time.

    pyenv local 3.9.13

> Optional - use it in case you need to close the terminal and want to keep using the same python version that got
> selected above.

---

# Poetry

**1. In order to use virtual environment, please install poetry using pip command**

    pip install poetry

_2. Run `pyenv which python` to get the python path_

_3. Run `poetry env use {python path that you copied}` then run `poetry shell`_

> Access poetry virtual environment

    poetry self install

> Install all specified packages. you don't need to do anything, just execute the above command and watch the magic
> happens

    exit

> This command is optional, in case you needed to quit the virtual environment.

_In order to execute the test cases, you have two options:_

1. Use `poetry run {command}` -> you should be out the poetry virtual environment.
2. Use `poetry shell` to access the virtual environment then execute your commands without using `poetry run {command}`

**All required packages will be installed using the above command, however, if you need to install any new package, use
**

    poetry add package_name

# nvm (node version manager)

> Follow this site to install nvm and the recommended (lts) version of node using it on windows.

    https://www.freecodecamp.org/news/nvm-for-windows-how-to-download-and-install-node-version-manager-in-windows-10/#:~:text=To%20install%20a%20specific%20version,0%20

> Follow this site to install nvm and the recommended (lts) version of node using it on linux/MacOS.

    https://gist.github.com/d2s/372b5943bce17b964a79

> Follow this site to install robotframework-browser library

    https://github.com/MarketSquare/robotframework-browser#robotframework-browser

---

# Plugins

**Install the following plugins:**

      1. Robotframework support
      2. Run Robotframework
      3. Intellibot patched SeleniumLibrary

Then restart you IDE after installing plugin and Libs

---

# Project Files Structure

**Test Automation Framework Project for Robot Framework which contains the following layers:**

    ├── Libraries                # This is for custom python libraries (Not built in)
    ├── POM
    │   ├── Keywords
    │   │   ├── API
    │   │   │   ├── Calls
    │   │   │   └── Actions 
    │   │   ├── UI
    │   │   │    ├── Modules          # This is for business keywords
    │   │   │    └── Pages  
    │   │   └── DB   
    │   │               
    │   └── Locators             # This is for elemets identifications(python files)
    ├── Resources
    │   ├── Configurations
    │   │   ├── Environments.resource   # This is for environment variables       
    │   │   └── Execution.resource      # This is for test execution configurations
    │   ├── DataSources          # This is for external test data files
    │   ├── Setup                # This is for any setup used for tests
    │   ├── Uploads              # This is for different files format to upload
    │   └── Variables            # This is for global variables across the whole project
    ├── Results
    │    └── Reports             # This is to store the generated reports of differed types
    ├── Tests
    │   ├── api                 # API test suites
    │   └── ui                  # UI test suites
    ├── Utilities               # Include helper functions , parsing data, and etc..
    ├── .gitignore              # List files and dirs ignored by git
    ├── .gitlab-ci.yml          # This is for gitlab ci/cd pipeline
    └── README.md               # This is for Project description

1. **POM (Page Object Model) Directory:**

Which contains Keywords for each and every element will be used in each Page for AUT (Application Under Test). Each
Keyword usually should contain of:

1. Locators Directory: Contains Web Elements Identifiers. '.py' files got used in order to write dynamic reference and
   it should be used with all locator's files.
2. Keywords Directory: contains two main directories, and they are:

    1. Pages Directory: This directory contains all Actions that would be triggered on the Element like "Click, Input,
       Select, ..etc"
    2. Modules Directory: This directory contains Keywords for each Step details needed combined in One Keyword. Guys
       coming from Java or Python this layer like Step definition to get your code organized

3. **Tests Directory**

   Which contains Test Cases calling Keywords of Keyword level which contains:

    1. Test Setup/ Suite Setup
       This is used to be executed before Test Steps executed for each Test Cases in Test Case/Suite
    2. Test /Suite Teardown
       This is used to executed once at the end of Test Case/ suite execution
    3. Test Case Title
       Which should matches Test Case Titles
    4. [Tags]: Which could contains Test Case Tags, IDs in Test Management Tools as well as Smoke-Test, Functionality,
       ..etc
    5. [Arguments]: Which contains Test Arguments as a Parameters to pass Test Data
    6. Test Steps: Which calls the pre-defined Keywords using their names from modules directory

---

# Tests Execution

**Note: If you used `poetry shell` command, no need to use `poetry run` in any commands**

**Execution use the following Command:**

    poetry run robot -d ./Results/Reports/  ./Tests/ui/SigninBuyProduct_TestSuite.robot

**You can add -T to the command to generate reports with date_time_staps**

    poetry run robot -T -d ./Results/Reports/  ./Tests/ui/SigninBuyProduct_TestSuite.robot

This command will export by default three types of Reports(log.html, report.html, output.xml). Under Results/Reports
directory, which will be used later for Test Execution on Test Tools like JIRA")
**To generate allure reports use the following command:**

    poetry run robot --listener allure_robotframework ./Tests/ui/SigninBuyProduct_TestSuite.robot

**To rerun failed tests:**

    poetry run robot --rerunfailed .\Results\Reports\output.xml --output .\Results\Reports\rerun.xml .\Tests\ui\

    poetry run rebot --merge .\Results\Reports\output.xml .\Results\Reports\rerun.xml

_Note: Please don't remove the "poetry.lock" & "pyproject.toml"_

---

# References

1. Collections library: http://robotframework.org/robotframework/latest/libraries/Collections.html
2. String
   Library: https://robotframework.org/robotframework/latest/libraries/String.html#Get%20Lines%20Containing%20String
3. Robot Framework official documentation: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.
   html#user-keyword-name-and-documentation
4. Browser library: https://robotframework-browser.org/

# Done on each pull request

_1. Run command:_

    poetry lock
