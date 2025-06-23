# Overview

# Set up a test environment

This guide lists the basic requirement for the environment and provides
instructions on how to download and set up the environment on your machine.

## The Prerequisite

Learn about the hardware and software required for setting up an environment.

### Required Equipment

1. Ubuntu 14.04+ or macOS Ventura 13+

1. Nest products supporting Matter (ex: Nest Hub 2nd, Nest Hub Max... etc)
   being a Matter controller. The supported devices are listed [Google Developer Center](https://developers.home.google.com/matter/supported-devices#hubs)

1. Android Phone (ex: Pixel phone) being a commissioner.

1. DUT being a commissionee.

1. A third app from partner. (ex: Tuya Home App, Aqara Home app... etc)

### Prerequisite Software Installation

#### Ubuntu/macOS host

1. adb (1.0.40+ recommended)
1. python3.11+
1. pip3

#### Android Phone

1. Install Google Home App in Google Play Store
1. Install Partner app in Google Play/Apple Store
1. Set up Nest hubs or speakers with a gmail account
1. Sign in to the Google Home app and the partner app
1. Enable USB debugging in Developer options.
1. Enable Stay awake in Developer options.

#### DUT

1.  Install the partner's third app:
    - [Tuya Home App](https://play.google.com/store/apps/details?id=com.tuya.smart&hl=en)
      , run `adb install $APK PATH ` or  `Install from play/apple store`.
    - [Aqara Home App](https://play.google.com/store/apps/details?id=com.lumiunited.aqarahome.play&hl=en)
      , run `adb install $APK PATH ` or  `Install from play/apple store`.

1. Run the testcase you would like to test with Partner App. Currently, the automation
   testing only support TOP 5 partner.

#### Other

1. Phone and hub / speaker have to be logged in with the same gmail account.
1. To get the latest versions of Google Play Services and Google Home App,
   test accounts must join the Trusted Tester program. Please follow the
   instructions on [Google Play Services](https://developers.home.google.com/matter/eap/setup/play-services)
   and [Google Home App](https://developers.home.google.com/matter/eap/setup/home-app) to opt in.
1. Please log in to the test account you want to test beforehand.

#### Known Limitation

1. ONE PC struct supports ONE phone. Multiple phone have not be supported yet.

## Install and set up automation testing

1. Run or copy the latest official automated test release from code search.
   ```
   google3/experimental/HHPE_TPE_QA/Home_API_e2e_Auto/
   
   https://source.corp.google.com/piper///depot/google3/experimental/HHPE_TPE_QA/Home_API_e2e_Auto/;l=1?q=experimental%2FHHPE_TPE_QA%2FHome_API_e2e_Auto
   experimental/HHPE_TPE_QA/Home_API_e2e_Auto/
   
   blaze run //experimental/HHPE_TPE_QA/Home_API_e2e_Auto:main

   ```

1. Create a virtual environment for the project.
   ```
   cd Home_API_e2e_Auto
   python3 -m venv env
   ```

1. Activate the virtual environment
   ```
   source env/bin/activate
   ```

1. Install Python Packages on your host by requirements file. Please execute the following command.
   ```
   pip3 install -r requirements.txt
   ```

1. Connect phone to host by USB cable. Make sure host has adb permission to
   access phone.

1. Install 3rd APP to Android phone.
   ```
   adb install Partner APP .
   ```

1. Power on DUT. Make sure the PC has connection with DUT.

# Run tests

Perform a series of test cases by executing the following command.
## Command:
```
Execute 1 time per testcase
pytest

Execute the specified test case
pytest ./testcase/test_aqara_testcase.py::TestAqaraTestCase::test_aqara_to_ghp_link_allow_process

Execute the test cases a given number of times.
pytest --count
```

## Arguments:
*  `-s`: Disable all output capturing. This means that any output printed to the console during the test execution (e.g., using Python's print() function) will be directly shown in your terminal in real-time. Without this flag, pytest captures this output and only shows it if a test fails
*  `/testcase`: This specifies the directory that pytest should look into to discover and run tests. Pytest will recursively search for test files (typically Python files starting with test_ or ending with _test.py) and test functions within this directory.
*  `--capture=sys`: This explicitly sets the capture method for standard output (stdout) and standard error (stderr) to sys. This is essentially the same as using -s. It ensures that any output sent to sys.stdout or sys.stderr is not captured by pytest and is instead passed directly to the terminal.
*  `-v`: Increase verbosity. This makes pytest print the name of each test function as it is executed, providing more detailed information about the test run

## Exmaple:
```
pytest
```
This command runs the test cases once using the pytest command".

```
pytest --count=1000
```
This command runs the specified times (using `--count=1000`) using the count command".

```
pytest ./testcase/test_aqara_testcase.py::TestAqaraTestCase::test_aqara_to_ghp_link_allow_process
```
This command runs the specified testcase (using `./[testcase_path]/[testcase.py]::[ClassName]::[funcName]`) using the pytest command".

Supported test cases are
* test_aqara_testcase
* test_tuya_testcase
* test_lg_testcase

# Read Result

All test result are placed in the path you set in `[PROJECT ROOT]/reports/`,`[PROJECT ROOT]/log/LOG_xxxx-xxxx_Device&Conftest/conftest.log`
or the log path `[PROJECT ROOT]/log/`.

1. test_log.INFO & test_log.DEBUG : Record the log on host side
1. [LOG_xxxxxxx_Device&Conftest]: Record `device_base` and `conftest` log on host side.
1. [LOG_xxxxxxx_Device&Conftest]/conftest.log, output the simple report and execution count.
1. [LOG_xxxxxxx_Object]: Record ui object log per app on host side.
1. [LOG_xxxxxxx_testcase]: Record testcase per app log on host side.
1. [reports]: An HTML report of test results. This report provides a clear and easily shareable summary of your test run.
1. [TEST_CASE_NAME]/logcat,adb_logcat_xxxxxxxx-yyyyyy.log : The log from the controller.
1. [TEST_CASE_NAME]/screenrecord, xxxxxx-xxxx_[funcName].mp4: The screen recording per test case.

The changes to the config.yml file will be reflected in the test flow.

# Folder Structure
```
Project
├── common : The folder contains the common codes and constants for all test cases.
├── config : The configuration file for the partner app.
├── env(venv) : The target directory for the virtual Python environment. It will be
│         created after following the previous instructions.
├── log : The default location for storing logs. It will be created after
│         following the previous instructions to execute tests.
├── page_objects : The object for the partner app. 
├── pytest_log : The log from pytest output.
├── reports : The log from pytest output.
├── testcase : The directory to store all supporting test cases.
├── utils : The required tool for the test.
├── conftest.py : This file serves as a local plugin for pytest. It is automatically discovered
│             by pytest and provides a way to define fixtures, hooks, and other test-related
│             configurations that are specific to the current test directory and its subdirectories.
├── main.py: The `pytest.main()` function is the primary entry point for running pytest
│             from within a Python script. It essentially mimics the behavior of invoking
│             the `pytest` command-line tool.
├── pytest.ini : The file is a configuration file used by the pytest testing
│               framework to customize its behavior for a specific test project or directory.
│               It is typically placed at the root of your test project or within a subdirectory
│               to apply configurations to tests within that scope.
├── README.md
└── requirements.txt : The list of required packages to run tests.
```
