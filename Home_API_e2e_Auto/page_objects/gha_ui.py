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



class GHAObject:
    """Class for handling GHA UI automation operations."""

    def __init__(self, device) -> None:
        """Initialize GHAUIPage with device and logger instances.

        Args:
            device (uiautomator2.Device): The device instance
        """
        self.device = device
        log_folder_path = DeviceBasic.create_log_folder("Object")
        self._logger = logging_utils.get_logger(__name__, log_folder_path)
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("tuya-smart.json")

    def stop_gha(self) -> bool:
        """Stop the gha app.

        Returns:
            bool: True if app stopped successfully, False otherwise
        """
        try:
            if (
                    self.device.app_current().get("package")
                    == constants.GHA_PACKAGE
            ):
                self.device.app_stop(constants.GHA_PACKAGE)
                self._logger.info("GHA stopped successfully.")
                return True
            else:
                self._logger.info("GHA is not running.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self._logger.error(f"Failed to stop GHA : {str(e)}")
            return False
        except RuntimeError as e:
            self._logger.error(f"Failed to stop GHA: {str(e)}")
            return False

    def start_gha(self, timeout=3.0) -> bool:
        """Start the Google Home App (GHA) and ensures it's in the foreground.

        1. Force-closes any existing Google Home App.
        2. Start Google Home App.
        3. Retry until Google Home App is successfully brought to the foreground.

        Args:
            timeout (float): Maximum time in seconds to wait for GHA to launch.
              Default is 3.0 seconds.
        """
        if self._is_gha_running():
            return True
        self.device.shell(f"am start -a {constants.ANDROID_INTENT_VIEW_ACTIVITY} {constants.GHA_PACKAGE}")
        self._logger.info("Start Google Home App")
        while True:
            if self.device.app_wait(constants.GHA_PACKAGE, timeout=timeout, front=True) == 0:
                self.device.shell(f"am start -a {constants.ANDROID_INTENT_VIEW_ACTIVITY} {constants.GHA_PACKAGE}")
                self._logger.info("Start Google Home App again")
            else:
                self._logger.info("Google Home app launched")
                break
            self._logger.info("Try restarting the Google Home App...")

    def _get_device_tab_on_gha(self) -> uiautomator2.UiObject:
        """Get device tab Object.

        Returns:
            Device tab UI Object.
        """
        return self.device(resourceId=f"{constants.GHA_DEVICE_TAB_ID}")

    def navigate_to_device_tab_on_gha(self) -> uiautomator2.UiObject:
        """Ensures that the 'Devices' navigation in GHA is selected.

        If the "Devices" navigation is not currently selected, clicks on it.
        """
        return self._get_device_tab_on_gha()

    def _get_device_tab_device_name(self) -> XPathSelector:
        """Constructs an XPath selector to locate the device name within a device tab.

        Returns:
            An XPathSelector object for the device name element.
        """
        return self.device.xpath(f"{constants.GHA_DEVICE_TAB_DEVICE_NAME_ID}")

    def _toggle_device_on_off(self, device_name: str) -> uiautomator2.UiObject:
        """Clicks on a device element by its displayed name to toggle its on/off state.

        Args:
            device_name: The visible name of the device to interact with.

        Returns:
            The result of the click action performed on the device element.
        """
        return self.device(text=f"{device_name}").click()

    def _long_toggle_lock_device_on_off(self) -> uiautomator2.UiObject:
        """Clicks on a device element by its displayed name to toggle its on/off state.

        Returns:
            The result of the click action performed on the device element.
        """
        return self.device(resourceIdMatches=constants.GHA_LOCKED_UNLOCKED_BUTTON_ID).long_click(constants.ONE_SECONDS, constants.THREE_SECONDS)

    def _get_save_pin_code_checkbox(self) -> uiautomator2.UiObject:
        """get on a device element by its displayed name to save pincode checkbox.

       Returns:
           The result of the get action performed on the device element.
       """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=constants.GHA_SAVE_PIN_CODE_CHECKBOX_ID)

    def _set_pin_code(self, pin_code) -> uiautomator2.UiObject:
        """Clicks on a device element by its displayed name to toggle its on/off state.

        Returns:
            The result of the click action performed on the device element.
        """
        sleep(constants.ONE_SECONDS)
        return self.device(resourceId=constants.GHA_PIN_EDIT_TEXT_ID).set_text(pin_code)

    def _click_ok_button_on_pin_edit(self) -> bool:
        """Clicks on a device element by its displayed name to toggle its on/off state.

        Returns:
            The result of the click action performed on the device element.
        """
        if self.device(resourceId=constants.TUYA_OK_BUTTON_ON_PIN_EDIT_ID).get_text() == "OK":
            self._logger.info("Found OK Button")
            sleep(constants.ONE_SECONDS)
            self.device(resourceId=constants.TUYA_OK_BUTTON_ON_PIN_EDIT_ID).click()
            self.device.press(f"{constants.KEY_BACK}")
            time.sleep(constants.FIVE_SECONDS)
        else:
            self._logger.info("Not found OK Button")
            assert False

    def _is_device_exist_device_page(self, device_name: str) -> bool:
        """Checks if a specific device exists on the current device page by its displayed name.

            It repeatedly scans the visible device names, scrolls if necessary,
            and returns True if the device name is found.

            Args:
                device_name: The visible name of the device to check for.

            Returns:
                True if the device with the given name is found on the page, False otherwise.
        """
        self._get_device_tab_device_name().wait()
        device_name_list = []
        while True:
            get_device_list_name = self._get_device_tab_device_name().all()
            temp_text_list = []
            for get_all_device_name in get_device_list_name:
                get_all_device_name_text = get_all_device_name.elem.get(f"{constants.ELEM_GET_TEXT}")
                if get_all_device_name_text not in device_name_list:
                    device_name_list.append(get_all_device_name_text)
                    temp_text_list.append(get_all_device_name_text)
                    self._logger.info(device_name_list)
                if device_name == get_all_device_name_text:
                    return True
            if not temp_text_list :
                self._logger.info("swipe end")
            self.device(resourceId=f"{constants.GHA_DEVICE_TAB_MAIN_VIEW_ID}").scroll.vert(distance='small')
            time.sleep(1)

    def _get_navigate_frame(self) -> uiautomator2.UiObject:
        """Get Navigate frame Object.

        Returns:
            Navigate frame UI Object.
        """
        return self.device(
            resourceId=(
                f"{constants.GHA_PACKAGE}:id/{constants.GHA_NAVIGATION_FRAME_ID}"
            )
        )

    def _get_refresh_spinner(self) -> XPathSelector:
        """Get Refresh Spinner Object.

        Returns:
            Refresh Spinner UI Object.
        """
        return self.device.xpath(f'//*[@resource-id="{constants.GHA_PACKAGE}:'f'id/{constants.GHA_REFRESH_SPINNER_ID}"]/android.widget.ImageView[1]')

    def refresh_gha_devices(self, timeout=5) -> None:
        """Refresh all devices in the Google Home App.

        Wait for the refresh to complete.

        Args:
            timeout: The time to wait for the refresh spinner to disappear. Default
              is 5 seconds.
        """
        self._get_navigate_frame().swipe(direction="down", steps=40)
        if self._get_refresh_spinner().wait_gone(timeout=timeout):
            self._logger.info(f"GHA has been refreshed.")
        else:
            self._logger.critical(f"Refresh too long..., timeout: {timeout}")

    def _get_gha_user_account(self) -> str:
        """Get the Google Home user account string.

        Returns:
            The text of the user account string.
        """
        account_info = self.device(
            resourceId=f"{constants.GHA_PACKAGE}:id/{constants.GHA_USER_ACCOUNT_ID}"
        )
        if account_info.exists:
            return account_info.get_text()
        else:
            return ""

    def _close_gha_account_info(self, timeout=5) -> None:
        """Closes the Google Home app user account information popup.

        Args:
            timeout: The maximum time in seconds to wait for the close button to
              appear.
        """
        gha_account_info_close_btn = self.device(
            resourceId=f"{constants.GHA_PACKAGE}:id/{constants.GHA_USER_ACCOUNT_INFO_CLOSE_BTN}"
        )
        if gha_account_info_close_btn.wait(timeout):
            gha_account_info_close_btn.click()
        time.sleep(1)  # Brief pause to allow for UI animations to complete

    def _get_add_more_detail_btn(self) -> uiautomator2.UiObject:
        """Gets add more detailed information button in the feedback page.

        Returns:
            Add more detail button UI object.
        """
        return self.device(
            resourceId=(
                f"{constants.GMS_PACKAGE}:id/{constants.GMS_ADD_MORE_DETAIL_ID}"
            )
        )

    def _get_all_devices_in_view(self) -> uiautomator2.UiObject:
        """Retrieves all device control objects in the current view of the Google Home app.

        Returns:
            A list of UI object device controls.
            What the function returns depend on how the user uses it, it can act like a list.
            e.g. for i in _get_all_devices_in_view(), _get_all_devices_in_view()[1], etc.
            See https://github.com/openatx/uiautomator2?tab=readme-ov-file#selector.
        """
        return self.device(
            resourceId=(
                f"{constants.TUYA_DEVICE_LIST_LINK_PAGE_ID}"
            )
        )

    def _launch_wifi_settings_activity(self) -> None:
        """Launches the Wi-Fi settings activity on the device."""
        self.device.shell(f"am force-stop {constants.ANDROID_SETTINGS_PACKAGE}")
        self.device.shell(f"am start -a {constants.ANDROID_WIFI_SETTINGS_PACKAGE}")
        time.sleep(1)  # Brief pause to allow for SSID UI updates

    def _get_navigate_up_button(self) -> UiObject:
        """Retrieves the 'Navigate up' button in the feedback page.

        Returns:
            Navigate up button UI Object.
        """
        return self.device(description="Navigate up")

    def _click_navigate_up_button(self, timeout=5) -> None:
        """Navigates up one page.

        Args:
            timeout: The maximum amount of time to wait for the button to appear in
              seconds.
        """
        if self._get_navigate_up_button().wait(timeout=timeout):
            self._get_navigate_up_button().click()

    def _is_gha_running(self) -> bool:
        """Checks if the Google Home app is running in the foreground.

        Returns:
            True if the Google Home app is running in the foreground, False
            otherwise.
        """
        return self.device.app_current().get("page_objects") == constants.GHA_PACKAGE

    def _get_user_account_frame_in_gha(self) -> uiautomator2.UiObject:
        """Retrieves the UI Object representing the user account frame.

        Returns:
            The UIObject representing the user account frame.
        """
        return self.device(
            resourceId=(
                f"{constants.GHA_PACKAGE}:id/{constants.GHA_USER_ACCOUNT_FRAME_ID}"
            )
        )

    def _get_account_information_element_in_gha(
            self, account
    ) -> uiautomator2.UiObject:
        """Gets the account information element.

        Args:
            account: The Account name to switch to.

        Returns:
            The UiObject representing the found account information UI element.
            An element using both the constructed resource ID and account text.
        """
        return self.device(
            resourceId=(
                f"{constants.GHA_PACKAGE}:id/{constants.GHA_ACCOUNT_INFORMATION_ID}"
            ),
            text=f"{account}",
        )

    def _get_gha_container_bottom(self) -> uiautomator2.UiObject:
        """Retrieves the UI Object representing the container bottom in Google Home App.

        Returns:
            The UIObject representing the container bottom in Google Home App.
        """
        return self.device(
            resourceId=(
                f"{constants.GHA_PACKAGE}:id/{constants.GHA_CONTAINER_BOTTOM_ID}"
            )
        )

    def _get_android_internet_ssid_layout(self) -> uiautomator2.UiObject:
        """Retrieves the UI Object representing the ssid layout.

        Returns:
            The UIObject representing the ssid layout.
        """
        return self.device(
            resourceId=f"{constants.ANDROID_SETTINGS_PACKAGE}:id/{constants.ANDROID_INTERNET_SSID_ID}"
        )

    def _get_android_3_button_navigation_bar(self) -> uiautomator2.UiObject:
        """Get Android navigation bar (3-button navigation mode).

        Returns:
            The Android navigation bar frame UI object.
        """
        return self.device(resourceId=f"{constants.ANDROID_SYSTEM_UI_PACKAGE}:id/{constants.ANDROID_NAVIGATION_BAR_FRAME}")

    def _get_android_gesture_navigation_bar(self) -> uiautomator2.UiObject:
        """Get Android bar background (Gesture navigation mode).

        Returns:
            The Android navigation bar background UI object.
        """
        return self.device(resourceId=f"{constants.ANDROID_INTENT}:id/{constants.ANDROID_NAVIGATION_BAR_BACKGROUND}")

    def get_status_and_set_to_presetting(self, gha_ui: Any, device_name: str, status_from_automation: Any, pin_code: Optional[str] = None) -> Any:
        """
        Checks a device's status in the Google Home App and sets it to a predefined state.

        This method navigates the GHA to find the specified device. It compares the
        device's current status with the desired status (`status_from_automation`).
        - If the status is different, it toggles the device to match the desired state.
        - If the device is offline, it returns the 'OFFLINE' status immediately.
        - If the status is already correct, it toggles the device twice, likely to
          force a state refresh or for testing purposes.

        Args:
            gha_ui (Any): The UI automation object or locator for Google Home App elements.
            device_name (str): The name of the target device.
            status_from_automation (Any): The desired status for the device (e.g., a 'DeviceState' enum member).
            pin_code (Optional[str], optional): The PIN code for the device if one is needed
                                                 to change its state. Defaults to None.

        Returns:
            Any: The final status of the device after all operations are complete.
        """
        self.start_gha()
        self.navigate_to_device_tab_on_gha().click()
        self.refresh_gha_devices()
        self._is_device_exist_device_page(device_name)
        current_status = DeviceBasic.get_device_state_on_gha(self, device_name, gha_ui)
        self._logger.info(f"current_status: {current_status}")
        if status_from_automation != current_status and current_status != DeviceState.OFFLINE:
            self._logger.info('device status differs from automation setting')
            self.toggle_lock_device(current_status, status_from_automation, device_name, pin_code)
            set_status_diff = DeviceBasic.get_device_state_on_gha(self, device_name, gha_ui)
            self._logger.info(f"if_status_diff: {set_status_diff}")
            self.stop_gha()
            return set_status_diff
        elif current_status == DeviceState.OFFLINE:
            self._logger.info('device status is OFFLINE')
            self.stop_gha()
            return current_status
        else:
            self._logger.info('device status sames from automation setting')
            for i in range(2):
                self.toggle_lock_device(current_status, status_from_automation, device_name, pin_code)
            set_status_same = DeviceBasic.get_device_state_on_gha(self, device_name, gha_ui)
            self._logger.info(f"if_status_same: {set_status_same}")
            self.stop_gha()
            return set_status_same

    def toggle_lock_device(self, current_status: Any, status_from_automation: Any, device_name: str, pin_code: Optional[str] = None) -> None:
        self._logger.info(f"current_state: {current_status} and automation setting: {status_from_automation}")
        self._logger.info('Toggling the device')
        self._toggle_device_on_off(device_name)
        self._long_toggle_lock_device_on_off()
        sleep(constants.THREE_SECONDS)
        if pin_code is not None:
            self._logger.info(f"pin_code: {pin_code}")
            if self._get_save_pin_code_checkbox():
                self._get_save_pin_code_checkbox().click()
            self._set_pin_code(pin_code)
            self._click_ok_button_on_pin_edit()
        else:
            self._logger.info(f"Device not set pin_code")
            self.device.press(f"{constants.KEY_BACK}")
    sleep(constants.FIVE_SECONDS)
