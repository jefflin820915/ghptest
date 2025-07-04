"""Conftest module for Home API e2e automation.

This module provides fixtures, hooks, and configurations for pytest,
including device setup, logging, screenshot capture, and test reporting.
"""
import base64
import os
import subprocess
import time
import allure
import pytest
import uiautomator2

from datetime import datetime
from typing import Any, Optional
from webbrowser import Error
from _pytest.runner import CallInfo
from common import constants
from common.constants import DeviceState
from common.device_base import DeviceBasic
from page_objects.tuya_ui import TuyaObject
from page_objects.gha_ui import GHAObject
from page_objects.aqara_ui import AqaraUIPage
from page_objects.gms_ui import GMSUIPage
from page_objects.aghp_ui import AGHPUIPage
from utils import logging_utils

log_folder_path = DeviceBasic.create_log_folder("Device&Conftest")
logger = logging_utils.get_logger(__name__, log_folder_path)
count = 0
items_list = []

@pytest.fixture(scope="session")
def device(request) -> uiautomator2.Device:
    global driver
    """create uiautomator2 device connect。"""
    try:
        driver = uiautomator2.connect()
        driver.implicitly_wait(constants.THIRTY_SECONDS)
        logger.info(f"Device connected: {driver.serial}")

        def teardown() -> None:
            yield driver
            logger.info("Fixture 'device' teardown: No specific action needed for uiautomator2 connection.")
        request.addfinalizer(teardown)
        return driver
    except uiautomator2.exceptions.ConnectError as e:
        logger.info(f"can't connect device: {e}")
        pytest.fail(f"can't connect device: {e}")

@pytest.fixture(scope="session", autouse=True)
def configure_allure_environment(request):
    """配置 Allure 環境資訊，顯示在報告的 Environment 頁面"""
    alluredir = request.config.getoption("--alluredir")
    if alluredir:
        environment = {
            "OS": os.name,
            "Python version": pytest.__version__,
            "Test Frame": "pytest",
        }
        with open(os.path.join(alluredir, "environment.properties"), "w", encoding="utf-8") as f:
            for key, value in environment.items():
                f.write(f"{key}={value}\n")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ('call', 'setup'):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            if file_name:
                allure.attach(
                    driver.screenshot(),
                    name=file_name,
                    attachment_type=allure.attachment_type.PNG
                )
    report.description = str(item.function.__doc__)



def pytest_collection_modifyitems(items) -> None:
    """
    Pytest hook that is called after collection has been performed and modifies the collected items in-place.

    Args:
        session: The pytest session object.
        config: The pytest config object.
        items (list of pytest.Item): List of collected test items.
    """
    global count
    global items_list
    count = len(items)
    items_list = items

def pytest_runtest_logstart(nodeid : str) -> None:
    """Pytest hook called at the very beginning of running a single test item.

  Args:
      nodeid (str): The node ID of the test item about to be run.
    """
    try:
        current_item = next(item for item in items_list if item.nodeid == nodeid)
        current_index = items_list.index(current_item) + 1
        print(f"\nStarting to run test case: {nodeid} (Current times: {current_index}/ Total times: {count})")
        logger.info(f"\nStarting to run test case: {nodeid} (Current times: {current_index}/ Total times: {count})")
    except StopIteration:
        print(f"\nStarting to run test case: {nodeid} (Unable to determine execution count)")
        logger.info(f"\nStarting to run test case: {nodeid} (Unable to determine execution count)")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: CallInfo) -> Optional[pytest.TestReport]:
    """
    Pytest hook function that is called to create test reports.
    It captures screenshots on test failure or skip (if not an expected failure)
    and embeds them into the HTML report. It also adds the docstring of the
    test function as the test description in the report.

    Args:
        item: The pytest Item object representing the test function.
        call: The CallInfo object containing the result of the test execution phase.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screenshot = adb_screen_shot()
            if file_name:
                pytst_html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:258;height:512px;" ' \
                             'onclick="window.open(this.src)" align="right"/></div>' % screenshot
                extra.append(pytest_html.extras.html(pytst_html))
        report.extras = extra
        report.description = str(item.function.__doc__)

def pytest_runtest_logreport(report) -> None:
    """This hook function is called after each test case is executed.

    It receives a 'report' object containing information about the test outcome.

    Args:
        report: A _pytest.reports.TestReport object containing test results.
                It includes attributes like 'nodeid' (test identifier),
                'outcome' ('passed', 'failed', 'skipped'), 'duration',
                'longrepr' (traceback for failures), and more.
  """
    print(f"======={report}")
    outcome = report.outcome
    if report.when == "call":
        logger.info("Starting test execution: %s", report.nodeid)
        if outcome == "passed":
            logger.info("Test passed: %s", report.nodeid)
        elif outcome == "failed":
            logger.info("Test failed: %s", report.nodeid)

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells) -> list:
    """Add parameters and annotations to the pytest HTML results table header.

  Args:
      cells (list): A list of th (table header) elements (strings) representing
        the existing header.

  Returns:
      list: A modified list of th elements (strings) with added headers for
      parameters and annotations.
  """
    cells.insert(1, "<th>Test_Case_Name<th>")
    cells.insert(2, '<th class="sortable time" data-column-type="time">Time</th>')
    cells.pop(2)

@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report) -> Any:
    """Modify the title of the HTML report.

  Args:
      report: The pytest-html report object.
  """
    report.title = "Home API post launch monitoring"

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not os.path.exists('./reports'):
        os.makedirs('./reports')
    config.option.htmlpath = './reports/'+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+".html"

def adb_screen_shot() -> None:
    """
    Captures a screenshot from the connected ADB device, saves it temporarily,
    reads it, encodes it in Base64, and returns the encoded string.
    Returns None if any step fails.
    """
    device_tmp_path = f'/data/local/tmp/screenshot_{constants.TIMESTAMP}.png'
    local_folder_name = 'screenshot_' + constants.TIMESTAMP
    log_path_base = constants.LOG_PATH.rstrip('/') + '/'
    local_folder_path = os.path.join(f"{log_path_base}{local_folder_name}")
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
        logging_utils.get_logger(__name__).info("Log directory created: %s", local_folder_path)
    local_tmp_file_path = os.path.join(local_folder_path, f'screenshot_{constants.TIMESTAMP}.png')
    screenshot_b64 = None
    try:
        cmd_capture = ['adb', 'shell', 'screencap', device_tmp_path]
        result_capture = subprocess.run(cmd_capture, capture_output=True, text=True, check=False, timeout=15)
        if result_capture.returncode != 0:
            logger.info(f"ADB Error (screencap): {result_capture.stderr or result_capture.stdout}")
            return None
        cmd_pull = ['adb', 'pull', device_tmp_path, local_tmp_file_path]
        result_pull = subprocess.run(cmd_pull, capture_output=True, text=True, check=False, timeout=15)
        if result_pull.returncode != 0:
            logger.info(f"ADB Error (pull): {result_pull.stderr or result_pull.stdout}")
            subprocess.run(['adb', 'shell', 'rm', device_tmp_path], check=False, timeout=5)
            return None
        if os.path.exists(local_tmp_file_path):
            with open(local_tmp_file_path, 'rb') as image_file:
                file_info_bytes = image_file.read()
            screenshot_b64 = base64.b64encode(file_info_bytes).decode('utf-8')
        else:
            logger.info(f"Error: Pulled screenshot file not found at {local_tmp_file_path}")
            return None
    except (subprocess.CalledProcessError, OSError, IOError) as e:
        logger.info(f"An error occurred during screenshot process: {e}")
        return None
    finally:
        try:
            logger.debug(f"Cleaning up device screenshot: {device_tmp_path}")
            cmd_rm = f'adb shell rm "{device_tmp_path}"'
            subprocess.run(cmd_rm, shell=True, check=False)
            logger.info(f"delete: {cmd_rm}")
            logger.debug(f"Cleaning up device screenshot: {device_tmp_path}")
            cmd_local_rm = f'rm -rf "{local_folder_path}"'
            subprocess.run(cmd_local_rm, shell=True, check=False)
            logger.info(f"delete: {cmd_local_rm}")
        except Error as e:
            logger.warning(f"Failed to remove screenshot from device: {e}")
        if os.path.exists(local_tmp_file_path):
            try:
                logger.debug(f"Cleaning up local screenshot: {local_tmp_file_path}")
                os.remove(local_tmp_file_path)
            except OSError as e:
                logger.warning(f"Failed to remove local screenshot file: {e}")
    return screenshot_b64

def adb_bugreport(log_path):
    """
    Capture adb bugreport and save it to the specified log path.

    Args:
        log_path (str): The full path where the bugreport will be saved.

    Returns:
        bool: True if the bugreport was captured successfully, False otherwise.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bugreport_filename = f"bugreport_{timestamp}.zip"
    bugreport_path = os.path.join(log_path, bugreport_filename)
    try:
        logger.info(f"Capturing adb bugreport to: {bugreport_path}")
        subprocess.run(['adb', 'bugreport', bugreport_path], check=True)
        logger.info("Adb bugreport captured successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error capturing adb bugreport: {e}")
    except FileNotFoundError:
        logger.error("adb command not found. Make sure ADB is in your system's PATH.")

def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    """
    A pytest hook that adds a detailed test execution summary to the terminal output.

    Args:
        terminalreporter: The pytest TerminalReporter instance.
        exitstatus: The exit status code of the pytest run.
        config: The pytest Config object.
    """
    total_tests = terminalreporter._numcollected
    passed_tests = len([item for item in terminalreporter.stats.get('passed', []) if item.when != 'teardown'])
    failed_tests = len([item for item in terminalreporter.stats.get('failed', []) if item.when != 'teardown'])
    error_tests = len([item for item in terminalreporter.stats.get('error', []) if item.when != 'teardown'])
    skipped_tests = len([item for item in terminalreporter.stats.get('skipped', []) if item.when != 'teardown'])
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    duration = time.time() - terminalreporter._sessionstarttime
    all_reports = [item for category in terminalreporter.stats if isinstance(terminalreporter.stats[category], list) for item in terminalreporter.stats[category]]
    logger.info("\n" + "=" * 30 + " Test Execution Summary " + "=" * 30)
    logger.info(f"⏱️ Total Execution Time: {duration:.2f} seconds")
    logger.info(f"🚦 Exit Status Code: {exitstatus}")
    logger.info(f"📊 Total Tests: {total_tests}, ✅ Passed: {passed_tests}, ❌ Failed: {failed_tests}, 💥 Error: {error_tests}, ⏭️ Skipped: {skipped_tests}")
    logger.info(f"💯 Test Success Rate: {success_rate:.2f}%")
    logger.info("-" * 80)
    logger.info("\n" + "=" * 30 + " Detailed Test Case Results " + "=" * 29)

    for report in all_reports:
        logger.info(f"📂 Test Case: {report.nodeid}")
        if hasattr(report, 'when'):
            logger.info(f"   ➡️ Stage: {report.when.upper()}")
        logger.info(f"   ✅ Result: {report.outcome.upper()}")
        logger.info("-" * 60)
    logger.info("\n" + "=" * 25 + " Setup/Teardown Phase Results " + "=" * 25)
    for report in all_reports:
        if hasattr(report, 'when') and report.when != 'call':
            logger.info(f"📂 Test Case: {report.nodeid}, Stage: {report.when.upper()}, Result: {report.outcome.upper()}")
    logger.info("-" * 80)

    logger.info("\n" + "=" * 28 + " Test Case Execution Results " + "=" * 27)
    for report in all_reports:
        if hasattr(report, 'when') and report.when == 'call':
            logger.info(f"📂 Test Case: {report.nodeid}, Result: {report.outcome.upper()}")
    logger.info("-" * 80)
    logger.info("\n" + "=" * 33 + " Passed Test Cases " + "=" * 32)
    if terminalreporter.stats.get('passed'):
        for report in terminalreporter.stats['passed']:
            logger.info(f"✅ Test Case: {report.nodeid}")
    else:
        logger.info("🎉 No test cases passed.")
    logger.info("-" * 80)

    if exitstatus != 0 and failed_tests > 0:
        logger.error("\n" + "🔥" * 20 + " FAILURE SUMMARY " + "🔥" * 20)
        logger.error("⚠️ Failures found in test cases.") # Using a bit of Russian for 'failures detected' for visual interest
        for report in terminalreporter.stats.get('failed', []):
            logger.error(f"❌ Failed Test Case: {report.nodeid}")
        logger.error("🔥" * 63)
        #adb_bugreport(log_folder_path)


@pytest.fixture
def tuya_ui(device: uiautomator2.Device) -> TuyaObject:
    """
    Create an instance of the TuyaObject.

    Args:
        device: The connected uiautomator2 device object.

    Returns:
        TuyaObject: An instance of the TuyaObject.
    """
    return TuyaObject(device)

@pytest.fixture
def gha_ui(device: uiautomator2.Device) -> GHAObject:
    """
    Create an instance of the GHAObject.

    Args:
        device: The connected uiautomator2 device object.

    Returns:
        GHAObject: An instance of the GHAObject.
    """
    return GHAObject(device)

@pytest.fixture
def gms_ui(device: uiautomator2.Device) -> GMSUIPage:
    """
    Create an instance of the GMSUIPage.

    Args:
        device: The connected uiautomator2 device object.

    Returns:
        GMSUIPage: An instance of the GMSUIPage.
    """
    return GMSUIPage(device)

@pytest.fixture
def aqara_ui(device: uiautomator2.Device) -> AqaraUIPage:
    """
    Create an instance of the AqaraUIPage.

    Args:
        device: The connected uiautomator2 device object.

    Returns:
        AqaraUIPage: An instance of the AqaraUIPage.
    """
    return AqaraUIPage(device)

@pytest.fixture
def aghp_ui(device: uiautomator2.Device) -> AGHPUIPage:
    """
    Create an instance of the AqaraUIPage.

    Args:
        device: The connected uiautomator2 device object.

    Returns:
        AqaraUIPage: An instance of the AqaraUIPage.
    """
    return AGHPUIPage(device)