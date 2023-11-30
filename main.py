"""  ---PyTest Framework---
Add-on Features:
- uses PyTest framework - has the ability to run on the system (without IDE)
- has loggers,
- descriptive test case string replaces default node id values,
- upon completion of terminal test runs, json reports is exported and is parsed into readable, customized HTML,
which can be sent as email,
- able to read browser console logs, and passed to reports in HTML format,
- Selenium can be safely used for browser-based automated inputs.

How:
- There are modules in this project whose name should start with "test_". These are the files that should contain
test functions whose name should also start with "test_". PyTest will automatically detect these test functions
to run when the command is called.
- There are a couple of ways to run them:
    1. Via the PyCharm IDE. It has PyTest functionalities integrated with the IDE after the PyTest package is
    downloaded. Simply click the run buttons accordingly.
    2. Via the terminal. This is the suggested way. You would skip the step of launching the IDE this way.
    However, the "venv" environment has to be activated first in the terminal before running it.

"""
