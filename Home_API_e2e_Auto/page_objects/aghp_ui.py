"""Page object for handling GHA UI automation."""
import time
from time import sleep
from typing import Any, Optional

import uiautomator2

from utils import logging_utils
from utils import config_manager
from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector
from common import constants
from common.device_base import DeviceBasic
from common.constants import DeviceState
from page_objects import gms_ui

class AGHPUIPage:
    """Class for handling GHA UI automation operations."""
    def __init__(self, device) -> None:
        """Initialize GHAUIPage with device and logger instances.

        Args:
            device (uiautomator2.Device): The device instance
        """
        self.device = device
        log_folder_path = DeviceBasic.create_log_folder("Object")
        self._logger = logging_utils.get_logger(__name__, log_folder_path)
        self.gms_ui = gms_ui.GMSUIPage(self.device)
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("android-sample-app.json")

    def stop_aghp(self) -> bool:
        """Stop the gha app.

        Returns:
            bool: True if app stopped successfully, False otherwise
        """
        try:
            if (
                    self.device.app_current().get("package")
                    == constants.AGHP_PACKAGE
            ):
                self.device.app_stop(constants.AGHP_PACKAGE)
                self._logger.info("Android Sample App stopped successfully.")
                return True
            else:
                self._logger.info("Android Sample App is not running.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self._logger.error(f"Failed to stop Android Sample App : {str(e)}")
            return False
        except RuntimeError as e:
            self._logger.error(f"Failed to stop Android Sample App: {str(e)}")
            return False

    def start_aghp(self, timeout=3.0) -> bool:
        """Start the Google Home App (GHA) and ensures it's in the foreground.

        1. Force-closes any existing Google Home App.
        2. Start Google Home App.
        3. Retry until Google Home App is successfully brought to the foreground.

        Args:
            timeout (float): Maximum time in seconds to wait for GHA to launch.
              Default is 3.0 seconds.
        """
        if self._is_aghp_running():
            return True
        self.device.shell(f"monkey -p {constants.AGHP_PACKAGE} 1")
        self._logger.info("Start Android Sample App")
        while True:
            if self.device.app_wait(constants.AGHP_PACKAGE, timeout=timeout, front=True) == 0:
                self.device.shell(f"am start -a {constants.ANDROID_INTENT_VIEW_ACTIVITY} {constants.AGHP_PACKAGE}")
                self._logger.info("Start Android Sample App again")
            else:
                self._logger.info("Android Sample App launched")
                break
            self._logger.info("Try restarting the Android Sample App...")
    def _is_aghp_running(self) -> bool:
        """Checks if the Google Home app is running in the foreground.

        Returns:
            True if the Google Home app is running in the foreground, False
            otherwise.
        """
        return self.device.app_current().get("page_objects") == constants.AGHP_PACKAGE

    def get_ghp_session_structure_name(self) -> XPathSelector:
        return self.device.xpath(constants.AGHP_GHP_SESSION_TITLE_BUTTON_CLASS_AND_TEXT)

    def get_unverified_view(self) -> uiautomator2.UiObject:
        sleep(constants.TWO_SECONDS)
        return self.device(text=constants.GHP_UNVERIFIED_VIEW_TEXT)

    def get_understand_button(self) -> XPathSelector:
        sleep(constants.ONE_SECONDS)
        return self.device.xpath(constants.UNVERIFIED_VIEW_UNDERSTAND_BUTTON_CLASS_AND_TEXT)

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

    def get_unverified_view_back_button(self) -> uiautomator2.UiObject:
        sleep(constants.ONE_SECONDS)
        self.device(className=constants.RESOURCE_CLASS_GMS_WEBKIT_CONTAINER).scroll.vert.to(description=constants.RESOURCE_CLASS_GO_BACK_BUTTON_DESCRIPTION)
        return self.device(description=constants.RESOURCE_CLASS_GO_BACK_BUTTON_DESCRIPTION)

    def _scroll_ghp_view_to_end(self) -> uiautomator2.UiObject:
        """Scrolls a vertical view containing the text 'Google Home Platform' until the text 'Allow' is visible.

            Returns:
                uiautomator2.UiObject: The UiObject representing the element with the text 'Allow'.
        """
        self._logger.info('starting scroll')
        return self.device(text='Google Home Platform').scroll.vert.to(text='Allow')

    def _get_cancel_btn(self) -> uiautomator2.UiObject:
        """Scrolls to the end of the Google Home Platform view and then waits for and returns the 'Allow' button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Allow' button.
        """
        self._scroll_ghp_view_to_end()
        if self.device(resourceId=f"{constants.RESOURCE_ID_GHP_CANCEL_LINK_BUTTON}").wait():
            return self.device(resourceId=f"{constants.RESOURCE_ID_GHP_CANCEL_LINK_BUTTON}")

    def _get_home_item_bar(self) -> uiautomator2.UiObject:
        self.device(resourceId=f"{constants.AGHP_HOME_ITEM_ID}").wait()
        return self.device(resourceId=f"{constants.AGHP_HOME_ITEM_ID}")

    def is_home_linked_devices_page(self, home):
        self.device(text=home).wait()
        return self.device(text=home)


    def _get_allow_btn(self) -> uiautomator2.UiObject:
        """Scrolls to the end of the Google Home Platform view and then waits for and returns the 'Allow' button.

            Returns:
                uiautomator2.UiObject: The UiObject representing the 'Allow' button.
        """
        self._scroll_ghp_view_to_end()
        if self.device(resourceId=f"{constants.TUYA_GHP_VIEW_ALLOW_BUTTON_ID}").wait():
            return self.device(resourceId=f"{constants.TUYA_GHP_VIEW_ALLOW_BUTTON_ID}")

    def _select_user(self) -> bool:
        """Selects a user account from a list if it exists.

            Args:
                account (str): The name or part of the name of the account to select.

            Returns:
                Optional[bool]: True if the account was found and clicked, None otherwise.
        """
        try:
            sleep(constants.THREE_SECONDS)
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
