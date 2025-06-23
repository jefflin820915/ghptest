"""Page object for handling Tuya UI automation."""
import time
import uiautomator2

from typing import Optional, Set, Any
from time import sleep

from ui_automator.ui_automator import UIAutomator
from uiautomator2.xpath import XPathSelector
from common import timout
from common import constants
from common.constants import DeviceState
from common.device_base import DeviceBasic
from page_objects import gms_ui
from utils import config_manager
from utils import logging_utils

class TuyaObject:
    """Class for handling Tuya UI automation operations."""

    def __init__(self, device) -> None:
        """Initialize GHAUIPage with device and logger instances.

        Args:
            device (uiautomator2.Device): The device instance
        """
        self.device = device
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("tuya-smart.json")
        self.gms_ui = gms_ui.GMSUIPage(self.device)
        log_folder_path = DeviceBasic.create_log_folder("Object")
        self._logger = logging_utils.get_logger(__name__, log_folder_path)

    def _is_tuya_running(self) -> bool:
        """Checks if the Tuya application is currently running on the device.

        Returns:
            bool: True if the Tuya application is running, False otherwise.
    """
        return self.device.app_current().get("page_objects") == constants.TUYA_PACKAGE

    def start_tuya(self, timeout=3.0) -> bool:
        """Start the Tuya home app and ensures it's in the foreground.

        1. Force-closes any existing Google Home App.
        2. Start Tuya home app.
        3. Retry until Google Home App is successfully brought to the foreground.

        Args:
            timeout (float): Maximum time in seconds to wait for tuya to launch.
              Default is 3.0 seconds.
        """
        if self._is_tuya_running():
            return True
        self.device.shell(f"monkey -p {constants.TUYA_PACKAGE} 1")
        self._logger.info("Start Tuya Smart App")
        while True:
            if self.device.app_wait(constants.TUYA_PACKAGE, timeout=timeout, front=True) == 0:
                self.device.shell(f"monkey -p {constants.TUYA_PACKAGE} 1")
                self._logger.info("Start Tuya Smart App again")
            else:
                self._logger.info("Tuya Smart App launched")
                break
            self._logger.info("Try restarting the Tuya Smart App...")

    def stop_tuya(self) -> bool:
        """Stop the tuya app.

        Returns:
            bool: True if app stopped successfully, False otherwise
        """
        try:
            if (
                    self.device.app_current().get("package")
                    == constants.TUYA_PACKAGE
            ):
                self.device.app_stop(constants.TUYA_PACKAGE)
                self._logger.info("Tuya app stopped successfully.")
                return True
            else:
                self._logger.info("Tuya app is not running.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self._logger.error(f"Failed to stop Tuya app : {str(e)}")
            return False
        except RuntimeError as e:
            self._logger.error(f"Failed to stop Tuya app: {str(e)}")
            return False

    def _get_add_btn_index(self) -> uiautomator2.UiObject:
        """Waits for and returns the add button UiObject located within the top toolbar.

        Returns:
            uiautomator2.UiObject: The UiObject representing the add button.
        """
        self.device(resourceId=f"{constants.TUYA_TOOL_BAR_TOP_VIEW_ID}").child(index=constants.TUYA_ADD_BUTTON_INDEX).wait()
        return self.device(resourceId=f"{constants.TUYA_TOOL_BAR_TOP_VIEW_ID}").child(index=constants.TUYA_ADD_BUTTON_INDEX)

    def _get_add_device_btn(self) -> XPathSelector:
        """Waits for a specified duration and then returns the XPathSelector for the add device button.

            Returns:
                XPathSelector: The XPathSelector object representing the add device button.
        """
        sleep(constants.TWO_SECONDS)
        return self.device.xpath(f"{constants.TUYA_ADD_DEVICE_BUTTON_CLASS_AND_TEXT}")

    def _get_scan_btn(self) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the scan button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the scan button.
        """
        sleep(constants.TWO_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_SCAN_BUTTON_ID}")

    def _get_pairing_code_btn(self) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the pairing code button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the pairing code button.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(text=f"{constants.TUYA_ENTER_SETUP_CODE_TEXT}")

    def _get_pairing_code_edit_text(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the pairing code edit text field.

            Returns:
                uiautomator2.UiObject: The UiObject representing the pairing code edit text field.
        """
        return self.device(resourceId=f"{constants.TUYA_PAIRING_CODE_EDIT_TEXT_ID}")

    def _get_pairing_code_view_next_btn(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the 'Next' button on the pairing code view.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Next' button on the pairing code view.
        """
        return self.device(resourceId=f"{constants.TUYA_PAIRING_CODE_VIEW_NEXT_BUTTON_ID}")

    def _get_enter_wifi_ssid_edit_text(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the Wi-Fi SSID edit text field.

            Returns:
                uiautomator2.UiObject: The UiObject representing the Wi-Fi SSID edit text field.
        """
        return self.device(resourceId=f"{constants.TUYA_SSID_EDIT_TEXT_ID}")

    def _get_enter_wifi_pwd_edit_text(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the Wi-Fi password edit text field.

            Returns:
                uiautomator2.UiObject: The UiObject representing the Wi-Fi password edit text field.
        """
        return self.device(resourceId=f"{constants.TUYA_WIFI_PWD_EDIT_TEXT_ID}")

    def _get_enter_wifi_view_next_btn(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the 'Next' button on the enter Wi-Fi details view.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Next' button on the enter Wi-Fi details view.
        """
        return self.device(resourceId=f"{constants.TUYA_ENTER_WIFI_VIEW_NEXT_BUTTON_ID}")

    def _get_enter_wifi_view_title(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the title on the enter Wi-Fi details view.

            Returns:
                uiautomator2.UiObject: The UiObject representing the title on the enter Wi-Fi details view.
        """
        return self.device(resourceId=f"{constants.TUYA_ENTER_WIFI_VIEW_TITLE_ID}")

    def _get_uncertified_device_add_btn(self) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the add button on the uncertified device connection success screen.

            Returns:
                uiautomator2.UiObject: The UiObject representing the add button on the uncertified device connection success screen.
        """
        sleep(2)
        return self.device(resourceId=f"{constants.TUYA_CONNECT_SUCCESS_ADD_BUTTON_ID}")

    def _get_edit_device_name_done_btn(self) -> XPathSelector:
        """Waits for a specified duration and then returns the XPathSelector for the 'Done' button on the edit device name screen.

            Returns:
                XPathSelector: The XPathSelector object representing the 'Done' button on the edit device name screen.
        """
        sleep(constants.ONE_SECONDS)
        return self.device.xpath(f"{constants.TUYA_EDIT_DEVICE_NAME_DON_BUTTON_CLASS_AND_TEXT}")

    def _get_add_device_view_edit_btn(self) -> uiautomator2.UiObject:
        """Returns the UiObject for the edit button on the add device view.

            Returns:
                uiautomator2.UiObject: The UiObject representing the edit button on the add device view.
        """
        return self.device(resourceId=f"{constants.TUYA_ADD_DEVICE_VIEW_EDIT_BUTTON_ID}")

    def _get_add_device_view_edit_view(self) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the edit view on the add device screen.

            Returns:
                uiautomator2.UiObject: The UiObject representing the edit view on the add device screen.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_ADD_DEVICE_VIEW_EDIT_VIEW_ID}")

    def _get_add_device_view_done_btn(self) -> uiautomator2.UiObject:
        """
            Waits for a specified duration and then returns the UiObject for the 'Done' button on the add device view.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Done' button on the add device view.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_ADD_DEVICE_VIEW_DONE_BUTTON_ID}")

    def _get_device_detail_view(self)-> uiautomator2.UiObject:
        """Returns the UiObject for the device detail view container.

            Returns:
                uiautomator2.UiObject: The UiObject representing the device detail view container.
        """
        return self.device(resourceId=f"{constants.TUYA_DEVICE_DETAIL_VIEW_CONTAINER_ID}")

    def _get_home_tab_device_name(self) -> XPathSelector:
        """Returns the XPathSelector for the device name displayed on the home tab.

            Returns:
                XPathSelector: The XPathSelector object representing the device name on the home tab.
        """
        return self.device.xpath(f"{constants.TUYA_HOME_TAB_DEVICES_NAME}")

    def _get_device_detail_switch_btn(self):
        """Returns the UiObject for the switch button on the device detail view.

            Note: This implementation directly accesses a character in a string literal,
            which might not be the intended way to locate the element.
            Consider using a more robust selector like resource-id, text, or XPath.

            Returns:
                uiautomator2.UiObject: The UiObject representing the switch button on the device detail view.
        """
        return self.device.xpath("TUYA_DEVICE_DETAIL_VIEW_NEXT_CLASS"[13])

    def _click_home_tab_device_name(self, device_name: str) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject of a device on the home tab with the given name.

            Args:
                device_name (str): The name of the device to locate.

            Returns:
                uiautomator2.UiObject: The UiObject representing the device with the specified name on the home tab.
        """
        sleep(constants.FIVE_SECONDS)
        return self.device(text=device_name)

    def _get_try_connect_again_btn(self)-> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the 'Try Again' button on a connection error screen.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Try Again' button.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_TRY_CONNECT_AGAIN_BUTTON}")

    def _get_add_device_name_edit_view(self)-> XPathSelector:
        """Waits for a specified duration and then returns the XPathSelector for the edit view where the device name is entered during the add device process.

            Returns:
                XPathSelector: The XPathSelector object representing the device name edit view.
        """
        sleep(constants.ONE_SECONDS)
        return self.device.xpath(f"{constants.TUYA_ADD_DEVICE_NAME_EDIT_VIEW_CLASS}")

    def _get_add_device_view_clear_btn(self)-> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the clear button in the add device view's edit field.

            Returns:
                uiautomator2.UiObject: The UiObject representing the clear button in the add device view's edit field.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_ADD_DEVICE_VIEW_EDIT_CLEAR_BUTTON}")

    def _get_device_name_view(self, device_name: str) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject of a view displaying the given device name.

            Args:
                device_name (str): The name of the device to locate.

            Returns:
                uiautomator2.UiObject: The UiObject representing the view with the specified device name.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(text=device_name)

    def _get_remove_device_btn(self)-> uiautomator2.UiObject:
        """Returns the UiObject for the remove device button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the remove device button.
        """
        return self.device(resourceId=f"{constants.TUYA_REMOVE_DEVICE_BUTTON_ID}")

    def _click_confirm_remove_device(self):
        """
            Clicks the confirmation button to remove a device, waits, clicks the 'Done' button on the all devices screen, and then presses the back key.
        """
        sleep(constants.ONE_SECONDS)
        self.device(resourceId=f"{constants.TUYA_CONFIRM_BUTTON_ID}").click()
        sleep(constants.ONE_SECONDS)
        self.device(resourceId=f"{constants.TUYA_DONE_BUTTON_ON_ALL_DEVICE_ID}").click()
        self.device.press(f"{constants.KEY_BACK}")


    def _set_device_on_add_device_view(self, device_name: str) -> None:
        """Sets the name of a device on the add device view and completes the process.

            Args:
                device_name (str): The desired name for the device.
            Returns:
                None
        """
        self._get_add_device_view_edit_view().click()
        self._get_add_device_view_clear_btn().click()
        self._get_add_device_name_edit_view().set_text(device_name)
        self._get_edit_device_name_done_btn().click()
        self._get_add_device_view_done_btn().click()
        sleep(constants.THREE_SECONDS)
        self.device.press(f"{constants.KEY_BACK}")

    def _is_show_enter_wifi_view(self, password: str) -> None:
        """Checks if the enter Wi-Fi view is displayed, enters the provided password, hides the keyboard, and clicks the 'Next' button if the view is present.

            Args:
                password (str): The Wi-Fi password to enter.

            Returns:
                None
        """
        if self._get_enter_wifi_view_title():
            self._get_enter_wifi_pwd_edit_text().set_text(password)
            self.device.press(f"{constants.KEY_BACK}")
            sleep(constants.ONE_SECONDS)
            self._get_enter_wifi_view_next_btn().click()

    def _is_device_exist_home_page(self, device_name: str) -> bool:
        """Checks if a device with the given name exists on the home page by scrolling through the device list.

            Args:
                device_name (str): The name of the device to check for.

            Returns:
                bool: True if the device is found, False otherwise.
        """
        self.get_home_device_item_card().wait()
        device_name_list = []
        while True:
            if not self._get_home_tab_device_name().exists:
                self.device(resourceId=f"{constants.TUYA_HOME_CONTENT_ROOT_ID}").scroll.vert(distance='small')
            get_device_list_name = self._get_home_tab_device_name().all()
            temp_text_list = []
            for get_all_device_name in get_device_list_name:
                get_all_device_name_text = get_all_device_name.elem.get(f"{constants.ELEM_GET_TEXT}")
                if get_all_device_name_text not in device_name_list:
                    device_name_list.append(get_all_device_name_text)
                    temp_text_list.append(get_all_device_name_text)
                    self._logger.info("Found device: "f'{temp_text_list}')
                if device_name == get_all_device_name_text:
                    self._logger.info(f"Device: {device_name}  found ")
                    return True
                else:
                    self._logger.info(f"Device: {device_name} not found")
            if not temp_text_list :
                self._logger.info("swipe end")
            self.device(resourceId=f"{constants.TUYA_HOME_CONTENT_ROOT_ID}").scroll.vert(distance='small')
            time.sleep(constants.ONE_SECONDS)

    @timout.timeout(constants.THREE_MINUTES)
    def _try_connect_device_timeout(self, pairing_code: str, password: str) -> None:
        """Attempts to connect a device, handling potential timeout errors and retrying the connection process.

            Args:
                pairing_code (str): The pairing code for the device.
                password (str): The Wi-Fi password.

            Returns:
                None
        """
        try_connect_title = self.device(resourceId=f"{constants.TUYA_TRY_CONNECT_ERROR_TITLE}")
        device_connected = self.device(resourceId=f"{constants.TUYA_CONNECT_SUCCESS_TITLE_ID}")
        wifi_view_title = self._get_enter_wifi_view_title()
        try:
            while True:
                try:
                    connecting_status = self.device(resourceId=f"{constants.TUYA_CONNECTING_STATUS_ID}")
                except:
                    connecting_status = self.device(resourceId=f"{constants.TUYA_CONNECTING_STATUS_ID}")

                if connecting_status.exists() is True:
                    self._logger.info("Device is connecting")
                elif try_connect_title:
                    try_connect_title.wait()
                    self._logger.info(try_connect_title)
                    sleep(constants.TWO_SECONDS)
                    self._get_try_connect_again_btn().click()
                    self._get_pairing_code_btn().click()
                    self._get_pairing_code_edit_text().set_text(pairing_code)
                    self._get_pairing_code_view_next_btn().click()
                elif device_connected:
                    device_connected.wait()
                    self._logger.info(device_connected.get_text())
                    break
                elif wifi_view_title:
                    wifi_view_title.wait()
                    self._is_show_enter_wifi_view(password)
                    if try_connect_title:
                        try_connect_title.wait()
                        sleep(constants.TWO_SECONDS)
                        self._get_try_connect_again_btn().click()
                        self._get_pairing_code_btn().click()
                        self._get_pairing_code_edit_text().set_text(pairing_code)
                        self._get_pairing_code_view_next_btn().click()
        except TimeoutError as e:
            self._logger.info('FAIL', 'Connecting device failed due to timeout ' + repr(e).split('Exception: ')[1].split('\\n')[0])

    def _click_add_device_and_pairing_code_btn(self) -> None:
        """
            Clicks the sequence of buttons to navigate to the pairing code entry screen.
            This includes clicking the add button, the add device button, the scan button,
            and finally the enter pairing code button.

            Returns:
                None
        """
        self._get_add_btn_index().click()
        self._get_add_device_btn().click()
        self._get_scan_btn().click()
        self._get_pairing_code_btn().click()

    def _get_me_tab(self) -> XPathSelector:
        """Waits for a specified duration and then returns the XPathSelector for the 'Me' tab.

            Returns:
                XPathSelector: The XPathSelector object representing the 'Me' tab.
        """
        sleep(constants.ONE_SECONDS)
        return self.device.xpath(f"{constants.TUYA_ME_TAB_CLASS_AND_TEXT}")

    def _get_home_tab(self) -> XPathSelector:
        """Returns the XPathSelector for the 'Home' tab.

            Returns:
                XPathSelector: The XPathSelector object representing the 'Home' tab.
        """
        return self.device.xpath(f"{constants.TUYA_HOME_TAB_CLASS_AND_TEXT}")

    def _get_google_home_devices(self) -> XPathSelector:
        """Returns the XPathSelector for the Google Home devices section.

            Returns:
                XPathSelector: The XPathSelector object representing the Google Home devices section.
        """
        return self.device.xpath(f"{constants.TUYA_GOOGLE_HOME_DEVICES_CLASS_AND_TEXT}")

    def _get_connect_btn(self) -> uiautomator2.UiObject:
        """Waits for a specified duration and then returns the UiObject for the connect button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the connect button.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=f"{constants.TUYA_CONNECT_BUTTON_ID}")

    def _get_manage_btn(self)-> uiautomator2.UiObject:
        """Returns the UiObject for the manage button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the manage button.
        """
        return self.device(resourceId=f"{constants.TUYA_MANAGE_BUTTON_ID}")

    def _select_user(self) -> bool:
        """Selects a user account from a list if it exists.

            Args:
                account (str): The name or part of the name of the account to select.

            Returns:
                Optional[bool]: True if the account was found and clicked, None otherwise.
        """
        try:
            account = self.get_google_test_account()
            button = self.gms_ui.get_gms_account_element(account)
            if button.wait(timeout=constants.FIVE_SECONDS):
                self.gms_ui.wait_gms_account_list_picker()
                button.click()
                self._logger.info(f"Selected {account}.")
                return True
            else:
                self._logger.error(
                    f"Failed to click Google test account: {account} not found."
                )
                self.gms_ui.click_gms_google_account_first()
                self._logger.info(
                    "Clicked first Google account, due to {account} not found."
                )
                return True
        except uiautomator2.exceptions.RPCError as e:
            self._logger.error(f"Failed to click Google test account: {str(e)}")
            return False
        except RuntimeError as e:
            self._logger.error(f"Failed to click Google test account: {str(e)}")
            return False

    def get_google_test_account(self) -> str:
        """Get the Google test account.

        Returns:
            str: The Google test account
        """
        try:
            account = self.config_manager.get_login_account()
            self._logger.info(f"{account} loaded from config file.")
            return account
        except RuntimeError as e:
            self._logger.error(f"Failed to get Google test account: {str(e)}")
            return ""

    def _get_home_item_bar(self) -> uiautomator2.UiObject:
        """Waits for and returns the UiObject representing the home item bar.

            Returns:
                uiautomator2.UiObject: The UiObject representing the home item bar.
        """
        self.device(resourceId=f"{constants.TUYA_HOME_ITEM_ID}").wait()
        return self.device(resourceId=f"{constants.TUYA_HOME_ITEM_ID}")

    def _get_all_device_home_page(self) -> XPathSelector:
        """Returns the XPathSelector for the element representing all devices on the home page.

            Returns:
                XPathSelector: The XPathSelector object for all devices on the home page.
        """
        return self.device.xpath(constants.TUYA_ALL_DEVICE_HOME_PAGE_CLASS_AND_TEXT)

    def _select_home(self, home: str) -> Optional[bool]:
        """Selects a home from the list of homes if it exists.

            Args:
                home (str): The name or part of the name of the home to select.

            Returns:
                Optional[bool]: True if the home was found and clicked, None otherwise.
        """
        if self.device.xpath(f"{constants.TUYA_HOME_ITEM_VIEW_ID}").wait():
            get_home_name = self.device.xpath(f"{constants.TUYA_HOME_ITEM_VIEW_ID}").child(f"{constants.TUYA_HOME_ITEM_CLASS}").all()
            for get_all_home_name in get_home_name:
                get_all_google_home_text = get_all_home_name.elem.get(f"{constants.ELEM_GET_TEXT}")
                self._logger.info(get_all_google_home_text)
                if home in get_all_google_home_text:
                    return self.device(text=home).click()

    def _scroll_ghp_view_to_end(self) -> uiautomator2.UiObject:
        """Scrolls a vertical view containing the text 'Google Home Platform' until the text 'Allow' is visible.

            Returns:
                uiautomator2.UiObject: The UiObject representing the element with the text 'Allow'.
        """
        self._logger.info('starting scroll')
        return self.device(text='Google Home Platform').scroll.vert.to(text='Allow')

    def _get_allow_btn(self) -> uiautomator2.UiObject:
        """Scrolls to the end of the Google Home Platform view and then waits for and returns the 'Allow' button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Allow' button.
        """
        self._scroll_ghp_view_to_end()
        if self.device(resourceId=f"{constants.TUYA_GHP_VIEW_ALLOW_BUTTON_ID}").wait():
            return self.device(resourceId=f"{constants.TUYA_GHP_VIEW_ALLOW_BUTTON_ID}")

    def _get_cancel_btn(self) -> uiautomator2.UiObject:
        """Scrolls to the end of the Google Home Platform view and then waits for and returns the 'Allow' button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Allow' button.
        """
        self._scroll_ghp_view_to_end()
        if self.device(resourceId=f"{constants.RESOURCE_ID_GHP_CANCEL_LINK_BUTTON}").wait():
            return self.device(resourceId=f"{constants.RESOURCE_ID_GHP_CANCEL_LINK_BUTTON}")

    def _get_link_device_list(self) -> set[Any]:
        """Retrieves a list of linked device names by scrolling through the device list on the linked devices page.

            Returns:
                list[Optional[str]]: A list of the names of the linked devices. Each name is an optional string,
                             as the text retrieval might fail for some elements.
        """
        self._logger.info("start swipe link list")
        self.device(resourceId=f"{constants.TUYA_DEVICE_LIST_LINK_PAGE_ID}").child(index=f"{self._get_link_device_page_index()}").wait()
        device_name_list = []
        seen_devices = set()
        while True:
            get_device_list_name = self.device.xpath(f"{constants.TUYA_DEVICE_LIST_NAME_ID}").all()
            temp_text_list = []
            for get_all_device_name in get_device_list_name:
                get_all_device_name_text = get_all_device_name.elem.get(f"{constants.ELEM_GET_TEXT}")
                if get_all_device_name_text not in device_name_list:
                    device_name_list.append(get_all_device_name_text)
                    temp_text_list.append(get_all_device_name_text)
                    seen_devices.add(get_all_device_name_text)
                    self._logger.info(seen_devices)
            if not temp_text_list:
                self._logger.info("swipe end")
                return seen_devices
            self.device(resourceId=f"{constants.TUYA_DEVICE_LIST_LINK_PAGE_ID}").scroll.vert(percent=0.7)
            time.sleep(constants.ONE_SECONDS)

    def _get_home_device_list(self) -> set[Any]:
        """Retrieves a list of device names visible on the home tab by scrolling through the list.

            Returns:
                List[Optional[str]]: A list of the names of the devices on the home tab. Each name
                             is an optional string, as the text retrieval might fail for some elements.
        """
        self._get_home_tab_device_name().wait()
        device_name_list = []
        seen_devices = set()
        while True:
            get_device_list_name = self._get_home_tab_device_name().all()
            temp_text_list = []
            for get_all_device_name in get_device_list_name:
                get_all_device_name_text = get_all_device_name.elem.get(f"{constants.ELEM_GET_TEXT}")
                if get_all_device_name_text not in seen_devices:
                    device_name_list.append(get_all_device_name_text)
                    temp_text_list.append(get_all_device_name_text)
                    seen_devices.add(get_all_device_name_text)
                    self._logger.info(seen_devices)
            if not temp_text_list :
                self._logger.info("swipe end")
                return seen_devices
            self.device(resourceId="com.tuya.smart:id/content_root").scroll.vert(percent=0.7)
            time.sleep(constants.ONE_SECONDS)

    def _get_link_device_page_index(self) -> Optional[int]:
        """Waits for a specified duration and then retrieves the index of the last
            RelativeLayout element within the RecyclerView on the linked devices page.

            Returns:
                Optional[int]: The index of the last RelativeLayout element as an integer,
                            or None if no such elements are found.
        """
        sleep(constants.THREE_SECONDS)
        get_all_link_device_list = self.device.xpath("com.tuya.smart:id/recyclerView").child(_xpath="android.widget.RelativeLayout").all()
        all_device_list_index_list = []
        for get_all_device_name in get_all_link_device_list:
            get_all_device_name_text = get_all_device_name.elem.get(f"{constants.ELEM_GET_INDEX}")
            all_device_list_index_list.append(get_all_device_name_text)
        return all_device_list_index_list[-1]

    def get_device_state_on_tuya(self):
        sleep(constants.THREE_SECONDS)
        is_disable_bounds = (73, 682, 144, 756)
        is_enable_bounds = (141, 682, 212, 756)
        current_bound = self.device(text="Switch", className="android.widget.TextView").sibling(className="android.view.View").child().child().bounds()
        self._logger.info(f"current_bound: {current_bound}")

        if self.get_device_offline_view():
            return DeviceState.OFFLINE
        elif current_bound >= is_enable_bounds:
            return DeviceState.ON
        elif current_bound <= is_disable_bounds:
            return DeviceState.OFF
        else:
            return DeviceState.UNKNOWN

    def toggle_device_on_off(self) -> uiautomator2.UiObject:
        return self.device(text="Switch", className="android.widget.TextView").sibling(className="android.view.View").child().click()

    def get_home_device_item_card(self) -> uiautomator2.UiObject:
        return self.device(resourceId=constants.TUYA_HOME_DEVICE_ITEM_CARD_ID)
    def get_device_offline_view(self) -> bool:
        sleep(constants.ONE_SECONDS)
        return self.device.xpath("//android.widget.TextView[@text='Device is offline']").exists
