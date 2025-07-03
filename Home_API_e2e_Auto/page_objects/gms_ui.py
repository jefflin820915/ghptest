"""Page object for handling GMS Core UI automation."""

# Standard library imports
import json
import os
import re
import time
from typing import Optional
# Local application imports
from common import constants
from common import session_data
from common.device_base import DeviceBasic
# Third-party imports
import uiautomator2
import uiautomator2.exceptions
from utils import color_analysis
from utils import logging_utils


class GMSUIPage:
    """Class for handling GMS Core UI automation operations."""

    def __init__(self, device) -> None:
        """Initialize GMSUIPage with device and logger instances."""
        self.device = device
        log_folder_path = DeviceBasic.create_log_folder("Object")
        self.logger = logging_utils.get_logger(__name__, log_folder_path)
        self.logger.debug("GMS UI page initialized")
        self.ghp_session_device_linked_data = (
            session_data.GHP_SESSION_DEVICE_LINKED_DATA
        )

    def _create_temp_folder(self) -> str:
        """Create a temporary folder."""
        temp_folder = os.path.join(os.getcwd(), "temp")
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        return temp_folder

    def _click_element(
            self,
            element: uiautomator2.UiObject,
            timeout: int = constants.FIVE_SECONDS,
    ) -> bool:
        """Clicks the element.

        Args:
            element (uiautomator2.UiObject): The element to click
            timeout (int): Maximum time to wait in seconds

        Returns:
            True if click successful, False otherwise
        """
        try:
            if element.wait(timeout=timeout):
                element.click(timeout=timeout)
                return True
            else:
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            return False

    def _get_resource_id_element(
            self, resource_id: str, text: Optional[str] = None
    ) -> Optional[uiautomator2.UiObject]:
        """Get UI element by resource ID and optional text.

        Args:
            resource_id (str): Resource ID of the UI element
            text (Optional[str]): Text content of the UI element

        Returns:
            Optional[uiautomator2.UiObject]: UI object if found, None otherwise
        """
        try:
            if text is not None:
                return self.device(resourceId=resource_id, text=text)
            else:
                return self.device(resourceId=resource_id)

        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get UI element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get UI element: {str(e)}")
            return None

    def get_gms_account_first_element(self) -> uiautomator2.UiObject | None:
        """Get the GMS account element.

        Returns:
            uiautomator2.UiObject | None: The GMS account element if found,
                None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_GMS_ACCOUNT
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GMS account element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GMS account element: {str(e)}")
            return None

    def click_gms_google_account_first(self) -> bool:
        """Click the Google test account.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_gms_account_first_element()
            self._click_element(button)
            self.logger.info("Clicked first Google account.")
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click first Google account: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click first Google account: {str(e)}")

    def get_gms_account_list_picker(self) -> uiautomator2.UiObject | None:
        """Get the GMS account list picker element.

        Returns:
            uiautomator2.UiObject | None: The GMS account list picker element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_GMS_ACCOUNT_LIST_PICKER
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GMS account list picker: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GMS account list picker: {str(e)}")
            return None

    def get_gms_account_list_ready_bar(self) -> uiautomator2.UiObject | None:
        """Get the GMS account list ready bar element.

        Returns:
            uiautomator2.UiObject | None: The GMS account list ready bar element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_GMS_ACCOUNT_LIST_READY_BAR
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get GMS account list ready bar element: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get GMS account list ready bar element: {str(e)}"
            )
            return None

    def wait_gms_account_list_picker(self) -> bool:
        """Wait for GMS account list picker.

        Returns:
            bool: True if wait successful, False otherwise
        """
        try:
            if self.get_gms_account_list_picker().wait(
                    timeout=constants.FIVE_SECONDS
            ):
                self.logger.info("GMS account list picker ready.")
                return True
            else:
                self.logger.error("GMS account list picker not ready.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to wait GMS account list picker: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to wait GMS account list picker: {str(e)}")
            return False

    def wait_gms_account_list_ready(self) -> bool:
        """Wait for GMS account list ready.

        Returns:
            bool: True if wait successful, False otherwise
        """
        try:
            if self.get_gms_account_list_ready_bar().wait(
                    timeout=constants.FIVE_SECONDS
            ):
                self.logger.info("GMS account list ready.")
                return True
            else:
                self.logger.error("GMS account list not ready.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to wait GMS account list ready: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to wait GMS account list ready: {str(e)}")
            return False

    def get_gms_account_element(
            self, account: str = ""
    ) -> uiautomator2.UiObject | None:
        """Get the GMS account element.

        Args:
            account (str): The account name to search for

        Returns:
            uiautomator2.UiObject | None: The GMS account element if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_GMS_ACCOUNT, text=account
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GMS account: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GMS account: {str(e)}")
            return None

    def get_gms_toggle_button(self) -> uiautomator2.UiObject | None:
        """Get the GMS toggle button.

        Returns:
            uiautomator2.UiObject | None: The GMS toggle button if found,
                None otherwise
        """
        try:
            return self.device(resourceIdMatches="mat-mdc-slide-toggle-.*-button")
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GMS toggle button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GMS toggle button: {str(e)}")
            return None

    def get_ghp_loading_element(self) -> uiautomator2.UiObject | None:
        """Get the GHP loading element.

        Returns:
            uiautomator2.UiObject | None: The GHP loading element if found,
                None otherwise
        """
        try:
            return self.device(className="android.widget.ProgressBar")
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GHP loading element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GHP loading element: {str(e)}")
            return None

    def wait_ghp_loading(self) -> bool:
        """Wait for GHP loading.

        Returns:
            bool: True if wait successful, False otherwise
        """
        try:
            if self.get_ghp_loading_element().wait(timeout=constants.TEN_SECONDS):
                self.logger.info("GHP Session loading...")
                while True:
                    if self.get_ghp_loading_element().wait_gone(
                            timeout=constants.TEN_SECONDS
                    ):
                        self.logger.info("GHP Session loaded.")
                        return True
                    else:
                        self.logger.info("GHP Session loading...")
                    time.sleep(1)
            else:
                self.logger.info("GHP Session not loading.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to wait for GHP loading: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to wait for GHP loading: {str(e)}")
            return False

    def get_ghp_session_structure_name_element(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the GHP session structure name element.

        Returns:
            uiautomator2.UiObject | None: The GHP session structure name element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId="mat-select-0", className="android.widget.Spinner"
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get GHP session structure name element: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get GHP session structure name element: {str(e)}"
            )
            return None

    def get_ghp_allow_link_button(self) -> uiautomator2.UiObject | None:
        """Get the GHP allow link button element.

        Returns:
            uiautomator2.UiObject | None: The GHP allow link button element if
            found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_GHP_ALLOW_LINK_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GHP allow link button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GHP allow link button: {str(e)}")
            return None

    def get_ghp_cancel_link_button(self) -> uiautomator2.UiObject | None:
        """Get the GHP cancel link button element.

        Returns:
            uiautomator2.UiObject | None: The GHP cancel link button element if
            found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_GHP_CANCEL_LINK_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GHP cancel link button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GHP cancel link button: {str(e)}")
            return None

    def click_ghp_cancel_link_button(self) -> bool:
        """Click the GHP cancel link button.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_ghp_cancel_link_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked GHP cancel link button.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click GHP cancel link button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click GHP cancel link button: {str(e)}")
            return False

    def click_ghp_allow_link_button(self) -> bool:
        """Click the GHP allow link button.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_ghp_allow_link_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked GHP allow link button.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click GHP allow link button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click GHP allow link button: {str(e)}")
            return False

    def find_ghp_allow_link_button_and_click(self) -> bool:
        """Find the GHP allow link button and click.

        Returns:
            bool: True if found and clicked, False otherwise
        """
        while True:
            try:
                button = self.get_ghp_allow_link_button()
                if button.wait(timeout=constants.FIVE_SECONDS):
                    self.click_ghp_allow_link_button()
                    return True
                else:
                    self.device.swipe(direction=constants.DIRECTION_UP, steps=7)
                    self.logger.info("Swiping up...")
                    time.sleep(1)
            except uiautomator2.exceptions.RPCError as e:
                self.logger.error(f"Failed to find GHP allow link button: {str(e)}")
                return False
            except RuntimeError as e:
                self.logger.error(f"Failed to find GHP allow link button: {str(e)}")
                return False
            time.sleep(1)

    def find_ghp_cancel_link_button_and_click(self) -> bool:
        """Find and click the GHP cancel link button.

        Returns:
            bool: True if click successful, False otherwise
        """
        first_dump = self.device.dump_hierarchy()
        while True:
            try:
                button = self.get_ghp_cancel_link_button()
                if button.wait(timeout=constants.TWO_SECONDS):
                    self.click_ghp_cancel_link_button()
                    self.logger.info("Found GHP cancel link button and clicked.")
                    return True
                else:
                    self.device.swipe(direction=constants.DIRECTION_UP, steps=7)
                    self.logger.info("Swiping up...")
                time.sleep(1)  # wait for the hierarchy to update
                second_dump = self.device.dump_hierarchy()
                if first_dump == second_dump:
                    self.logger.info("GHP cancel link button not found.")
                    return False
                first_dump = second_dump
            except uiautomator2.exceptions.RPCError as e:
                self.logger.error(f"Failed to find GHP cancel link button: {str(e)}")
                return False
            except RuntimeError as e:
                self.logger.error(f"Failed to find GHP cancel link button: {str(e)}")
                return False
            time.sleep(1)

    def get_ghp_webkit(self) -> uiautomator2.UiObject | None:
        """Get the GHP webkit element.

        Returns:
            uiautomator2.UiObject | None: The GHP webkit element if found,
            None otherwise
        """
        try:
            return self.device(
                className="android.webkit.WebView", text="Google Home Platform"
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GHP webkit: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get GHP webkit: {str(e)}")
            return None

    def check_gms_choose_an_account_page(self, timeout: int = 2) -> bool:
        """Check if the GMS choose an account page is displayed.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if found, False otherwise
        """
        try:
            button = self.device(
                resourceId=constants.RESOURCE_ID_GMS_MAIN_TITLE,
                text="Choose an account",
            )
            if button.wait(timeout=timeout):
                self.logger.info("Found choose an account page.")
                return True
            else:
                self.logger.info("Choose an account page not found.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get choose an account page: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to get choose an account page: {str(e)}")
            return False

    def get_ghp_session_structure_name(self) -> str:
        """Get the GHP session structure name.

        Returns:
          str: The GHP session structure name
        """
        try:
            self.ghp_session_device_linked_data[
                "structure_name"
            ] = self.get_ghp_session_structure_name_element().get_text(
                timeout=constants.FIVE_SECONDS
            )
            self.logger.info(
                "GHP session structure name:"
                f" {self.ghp_session_device_linked_data['structure_name']}"
            )
            return self.ghp_session_device_linked_data["structure_name"]
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get GHP session structure name: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get GHP session structure name: {str(e)}")
            return ""

    def find_ghp_session_device_type_linked_button(self) -> bool:
        """Find the GHP session device type linked button.

        Returns:
          bool: True if found, False otherwise
        """
        first_dump = self.device.dump_hierarchy()
        while True:
            try:
                button = self.device(textMatches=".*device type.* linked").wait(
                    timeout=constants.TWO_SECONDS
                )
                if button:
                    self.logger.info("Found GHP session device type linked.")
                    return True
                else:
                    self.device.swipe(direction=constants.DIRECTION_UP, steps=7)
                    time.sleep(1)
                    second_dump = self.device.dump_hierarchy()
                    if first_dump == second_dump:
                        self.logger.info("GHP session device type linked not found.")
                        return False
                    first_dump = second_dump
            except uiautomator2.exceptions.RPCError as e:
                self.logger.error(
                    f"Failed to find GHP session device type linked: {str(e)}"
                )
                return False
            except RuntimeError as e:
                self.logger.error(
                    f"Failed to find GHP session device type linked: {str(e)}"
                )
                return False
            time.sleep(1)

    def get_ghp_session_device_type_linked_count(self) -> int:
        """Get the count of linked device types in GHP session.

        Returns:
          int: The number of linked device types, 0 if not found or error occurs
        """
        try:
            # Get the full text (e.g., "12 device types linked")
            full_text = self.device(textMatches=".*device type.* linked").get_text(
                timeout=constants.TWO_SECONDS
            )

            if not full_text:
                self.logger.warning("Device types linked text is empty")
                return 0

            # Split the text and get the first element (the number)
            parts = full_text.split()
            if len(parts) < 1:
                self.logger.warning(
                    f"Invalid format of device types linked text: {full_text}"
                )
                return 0

            # Try to convert the first element to integer
            try:
                count = int(parts[0])
                if count < 0:
                    self.logger.warning(f"Invalid device count: {count}")
                    return 0
                self.ghp_session_device_linked_data["device_type_linked_count"] = count
                self.logger.info(f"Device type linked count {count}")
                return count
            except ValueError:
                self.logger.warning(f"Cannot convert to number: {parts[0]}")
                return 0
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get device type linked count: {str(e)}")
            return 0
        except RuntimeError as e:
            self.logger.error(
                f"Unexpected error getting device type linked count: {str(e)}"
            )
            return 0

    def click_ghp_session_device_type_linked(self) -> bool:
        """Click the GHP session device type linked.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.device(textMatches=".*device type.* linked")
            self._click_element(button)
            self.logger.info("Clicked GHP session device type linked.")
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click GHP session device type linked: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click GHP session device type linked: {str(e)}"
            )
            return False

    def get_class_webkit_container(self) -> uiautomator2.UiObject:
        """Get the class webkit container.

        Returns:
            uiautomator2.UiObject: The class webkit container
        """
        return self.device(className=constants.RESOURCE_CLASS_GMS_WEBKIT_CONTAINER)

    def get_ghp_devices_linked_view_layout_container(
            self,
    ) -> uiautomator2.UiObject:
        """Get the resource id layout container.

        Returns:
            uiautomator2.UiObject: The resource id layout container
        """
        return self.device(resourceId=constants.RESOURCE_ID_GHP_DEVICES_LINKED_VIEW)

    def get_class_go_back_button(self) -> uiautomator2.UiObject:
        """Get the class go back button.

        Returns:
            uiautomator2.UiObject: The class go back button
        """
        return self.device(
            className=constants.RESOURCE_CLASS_GO_BACK_BUTTON,
            description=constants.RESOURCE_CLASS_GO_BACK_BUTTON_DESCRIPTION,
        )

    def click_class_go_back_button(self) -> bool:
        """Click the class go back button.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_class_go_back_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                button.click(offset=(0.9, 0.9))
                self.logger.info("Clicked class go back button.")
                return True
            self.logger.info("Class go back button not found.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click class go back button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click class go back button: {str(e)}")
            return False

    def back_to_ghp_session(self) -> bool:
        """Back to GHP session page.

        Returns:
            bool: True if back successful, False otherwise
        """
        try:
            first_page = self.device.dump_hierarchy()
            while True:
                self.device(className=constants.RESOURCE_CLASS_GMS_WEBKIT_CONTAINER).scroll.vert.to(description=constants.RESOURCE_CLASS_GO_BACK_BUTTON_DESCRIPTION)
                self.logger.info("Swiping down...")
                time.sleep(1)  # wait for the hierarchy to update
                second_page = self.device.dump_hierarchy()
                if first_page == second_page:
                    self.logger.info("Already at the top of the page.")
                    break
                first_page = second_page
                self.logger.info("Not yet at the top of the page.")
            time.sleep(1)
            self.click_class_go_back_button()
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to back to GHP session page: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to back to GHP session page: {str(e)}")
            return False

    def get_ghp_api_device_linked_data(self, mode=None) -> dict[str, any]:
        """Get the GHP API device linked data.

        Args:
            mode (str, optional): The mode to set the toggle button.
              If 'True', it will enable the GHP API toggle button.
              If 'False', it will disable the GHP API toggle button.
              Defaults to None.

        Returns:
            dict[str, any]: A dictionary containing the linked device data.
        """

        first = self.device.dump_hierarchy()
        temp_folder = self._create_temp_folder()
        if self.get_gms_toggle_button().wait(timeout=constants.FIVE_SECONDS):
            self.logger.info("GMS toggle button found.")
        while True:
            for index, i in enumerate(self.get_gms_toggle_button()):
                try:
                    if i.wait(timeout=constants.FIVE_SECONDS):
                        enable_status = i.screenshot()
                        enable_status.save(f"{temp_folder}/toggle_button.png")
                        enabled = color_analysis.is_mostly_blue(
                            os.path.join(temp_folder, "toggle_button.png")
                        )
                        if mode is not None:
                            enabled = self._click_toggle_button(
                                toggle_button=i, enabled=enabled, mode=mode
                            )
                        match = re.match(
                            r"^(.*?)(\d+)(.*)$", i.get_text(timeout=constants.FIVE_SECONDS)
                        )
                        if match:
                            get_text = [
                                match.group(1).strip(),
                                int(match.group(2)),
                                match.group(3).strip(),
                            ]
                        else:
                            parts = (
                                i.get_text(timeout=constants.FIVE_SECONDS)
                                .strip()
                                .split(" ", 1)
                            )
                            if len(parts) == 2:
                                get_text = [parts[0], 0, parts[1].strip()]
                            else:
                                get_text = [
                                    i.get_text(timeout=constants.FIVE_SECONDS).strip(),
                                    0,
                                    "",
                                ]
                        self.logger.info(f"[{index}]GHP devices linked data: {get_text}")
                        if (
                                get_text[0]
                                not in self.ghp_session_device_linked_data["device_linked_data"]
                        ):
                            if get_text[1] is not None:
                                self.ghp_session_device_linked_data["device_linked_data"][
                                    get_text[0]
                                ] = {
                                    "connected": get_text[1],
                                    "device_type": get_text[2],
                                    "enabled": enabled,
                                }
                except uiautomator2.exceptions.UiAutomationError as e:
                    self.logger.info(f"Failed to get GMS linked data: {i} ({str(e)})")
                    continue
            if self.get_class_webkit_container().wait(timeout=constants.FIVE_SECONDS):
                self.get_class_webkit_container().swipe(
                    constants.DIRECTION_UP, steps=0.2
                )
                self.logger.info("Webkit container swiped up")
            else:
                self.get_ghp_devices_linked_view_layout_container().wait(
                    timeout=constants.FIVE_SECONDS
                )
                (self.get_ghp_devices_linked_view_layout_container()
                 .scroll.vert.forward())
                self.logger.info("Layout container swiped up")
            time.sleep(2)  # wait for the hierarchy to update
            second = self.device.dump_hierarchy()
            if first == second:
                break
            first = second
        self.logger.info(
            "GHP devices linked data:"
            f" {json.dumps(self.ghp_session_device_linked_data, indent=4)}"
        )
        self.back_to_ghp_session()
        return self.ghp_session_device_linked_data

    def _click_toggle_button(
            self,
            toggle_button: uiautomator2.UiObject,
            enabled: bool,
            mode: bool = None,
    ) -> bool:
        """Click the toggle button.

        Args:
            toggle_button (uiautomator2.UiObject): The toggle button to click.
            enabled (bool): The mode to set the toggle button. If True, it will
              enable the toggle button. If False, it will disable the toggle button.
              Defaults to None.
            mode (bool): The desired state of the toggle button. If True, the toggle
              button should be enabled. If False, the toggle button should be
              disabled. If None, the function will return False.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            if mode is None:
                return False
            if mode:
                if not enabled:
                    toggle_button.click(timeout=constants.FIVE_SECONDS)
                    self.logger.info(
                        f"{toggle_button.get_text(timeout=constants.FIVE_SECONDS)} Enabled."
                    )
                    enabled = True
            elif not mode:
                if enabled:
                    toggle_button.click(timeout=constants.FIVE_SECONDS)
                    self.logger.info(
                        f"{toggle_button.get_text(timeout=constants.FIVE_SECONDS)} Disabled."
                    )
                    enabled = False
                else:
                    return False
            return enabled
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click toggle button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click toggle button: {str(e)}")
            return False
