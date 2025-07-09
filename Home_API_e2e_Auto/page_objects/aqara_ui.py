"""Aqara UI page."""

# Standard library imports
import time
from typing import Optional
# Local application imports
from common import constants
from common import session_data
from common.device_base import DeviceBasic
from page_objects import gms_ui
# Third-party imports
import uiautomator2
import uiautomator2.exceptions
from utils import config_manager
# Local application imports
from utils import logging_utils


class AqaraUIPage:
    """Class for handling Aqara UI automation operations."""

    def __init__(self, device) -> None:
        """Initialize AqaraUIPage with device and logger instances.

        Args:
            device (uiautomator2.Device): The device instance
        """
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("aqara-home-40727.json")
        self.device = device
        log_folder_path = DeviceBasic.create_log_folder("Object")
        self.gms_ui = gms_ui.GMSUIPage(self.device)
        self.logger = logging_utils.get_logger(__name__, log_folder_path)
        self.logger.info("Aqara UI page initialized")
        self.ghp_session_device_linked_data = (
            session_data.GHP_SESSION_DEVICE_LINKED_DATA
        )

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

    def stop_aqara_app(self) -> bool:
        """Stop the Aqara app.

        Returns:
          bool: True if app stopped successfully, False otherwise
        """
        try:
            if (
                    self.device.app_current().get("package")
                    == constants.AQARA_PACKAGE_NAME
            ):
                self.device.app_stop(constants.AQARA_PACKAGE_NAME)
                self.logger.info("Aqara app stopped successfully.")
                return True
            else:
                self.logger.info("Aqara app is not running.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to stop Aqara app: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to stop Aqara app: {str(e)}")
            return False

    def start_aqara_app(self) -> bool:
        """Start the Aqara app.

        Returns:
          bool: True if app started successfully, False otherwise
        """
        try:
            while True:
                if (
                        self.device.app_current().get("package")
                        == constants.AQARA_PACKAGE_NAME
                ):
                    self.logger.info("Aqara app is already running.")
                    return True
                else:
                    self.device.app_start(constants.AQARA_PACKAGE_NAME)
                time.sleep(1)  # wait for the app to start
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to start Aqara app: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to start Aqara app: {str(e)}")
            return False

    def get_profile_button(self) -> uiautomator2.UiObject | None:
        """Get the profile button element.

        Returns:
          uiautomator2.UiObject | None: The profile button element if found.
        """
        try:
            return self._get_resource_id_element(constants.RESOURCE_ID_PROFILE_BUTTON)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get profile button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get profile button: {str(e)}")
            return None

    def is_aqara_home_page(self) -> bool:
        """Check if current page is the Aqara home page.

        Returns:
          bool: True if current page is Aqara home page, False otherwise
        """
        try:
            result = self.get_profile_button().wait(timeout=constants.FIVE_SECONDS)
            self.logger.info(f"Is Aqara home page: {result}")
            return result
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check Aqara home page: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check Aqara home page: {str(e)}")
            return False

    def click_profile_button(self) -> bool:
        """Click the profile button.

        Returns:
          bool: True if click successful, False otherwise
        """
        try:
            self._click_element(self.get_profile_button())
            self.logger.info("Clicked profile button.")
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click profile button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click profile button: {str(e)}")
            return False

    def click_google_home_automations(self) -> bool:
        """Click the Google Home Automations button.

        Returns:
          bool: True if click successful, False otherwise
        """
        try:
            button = self._get_resource_id_element(
                constants.RESOURCE_ID_GOOGLE_HOME_AUTOMATIONS,
                constants.RESOURCE_ID_GOOGLE_HOME_AUTOMATIONS_TEXT,
            )
            if button.wait(timeout=constants.FIVE_SECONDS):
                time.sleep(constants.TWO_SECONDS)  # App Animation
                self._click_element(button)
                self.logger.info("Clicked Google Home Automations.")
                return True
            else:
                self.logger.error("Google Home Automations not found.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click Google Home Automations: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click Google Home Automations: {str(e)}")
            return False

    def get_google_test_account(self) -> str:
        """Get the Google test account.

        Returns:
          str: The Google test account
        """
        try:
            account = self.config_manager.get_login_account()
            self.logger.info(f"{account} loaded from config file.")
            return account
        except RuntimeError as e:
            self.logger.error(f"Failed to get Google test account: {str(e)}")
            return ""

    def find_gms_account_and_click(self, account: str) -> bool:
        """Find the Google test account element.

        Args:
          account (str): The Google test account

        Returns:
          bool: True if found, False otherwise
        """
        first_dump = self.device.dump_hierarchy()
        try:
            self.gms_ui.wait_gms_account_list_picker()
            while True:
                self.logger.info(f"Looking for {account}...")
                button = self.gms_ui.get_gms_account_element(account)
                if button.wait(timeout=constants.TWO_SECONDS):
                    button.click()
                    self.logger.info(f"Selected {account}.")
                    return True
                else:
                    self.device(
                        resourceId=constants.RESOURCE_ID_GMS_ACCOUNT_LIST_PICKER
                    ).swipe(constants.DIRECTION_UP, 0.7)
                    self.logger.info("Swiping up...")
                time.sleep(constants.TWO_SECONDS)  # wait for the hierarchy to update
                second_dump = self.device.dump_hierarchy()
                if first_dump == second_dump:
                    self.logger.info(f"{account} not found.")
                    return False
                first_dump = second_dump

        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to find Google test account: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to find Google test account: {str(e)}")
            return False

    def click_gms_google_test_account(self) -> bool:
        """Click the Google test account.

        Returns:
          bool: True if click successful, False otherwise
        """
        try:
            account = self.get_google_test_account()
            time.sleep(1)  # Account list animation
            if self.find_gms_account_and_click(account):
                self.logger.info(f"Clicked Google {account} account.")
                return True
            else:
                self.gms_ui.click_gms_google_account_first()
                self.logger.info("Clicked first Google account.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click Google test account: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click Google test account: {str(e)}")
            return False

    def get_ghp_session_device_type_linked(self) -> str:
        """Get the GHP session device type linked.

        Returns:
          str: The GHP session device type linked
        """
        try:
            return self.device(textMatches=".*device type.* linked").get_text(
                timeout=constants.FIVE_SECONDS
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get GHP session device type linked: {str(e)}"
            )
            return ""
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get GHP session device type linked: {str(e)}"
            )
            return ""

    def get_automation_title_element(self) -> uiautomator2.UiObject | None:
        """Get the automation title element.

        Returns:
            uiautomator2.UiObject | None: The automation title element if found,
                None otherwise
        """
        return self._get_resource_id_element(constants.RESOURCE_ID_TOOLBAR_TITLE)

    def get_automation_title_text(self) -> str:
        """Get the text content of the automation title.

        Returns:
            str: The text content of the automation title, empty string if not
            found
        """
        try:
            title = self.get_automation_title_element()
            if title:
                return title.get_text()
            else:
                return ""
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation title text: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation title text: {str(e)}")
            return ""

    def is_automation_page(self, timeout: int = constants.FIVE_SECONDS) -> bool:
        """Check if current page is the automation page.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if current page is automation page, False otherwise
        """
        try:
            button = self._get_resource_id_element(
                constants.RESOURCE_ID_TOOLBAR_TITLE
            )
            if button.wait(timeout=timeout):
                return button.get_text() == "Automation"
            else:
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check automation page: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check automation page: {str(e)}")
            return False

    def get_aqara_connect_to_ecosystems_button(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the aqara connect to ecosystems button element.

        Returns:
            uiautomator2.UiObject | None: The aqara connect to ecosystems button
            element if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_CONNECT_TO_ECOSYSTEMS_BUTTON,
                text=constants.RESOURCE_ID_CONNECT_TO_ECOSYSTEMS_BUTTON_TEXT,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get aqara connect to ecosystems button: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get aqara connect to ecosystems button: {str(e)}"
            )
            return None

    def click_aqara_connect_to_ecosystems_button(self) -> bool:
        """Click the aqara connect to ecosystems button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_aqara_connect_to_ecosystems_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked aqara connect to ecosystems button.")
                return True
            self.logger.error("Failed to click aqara connect to ecosystems button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click aqara connect to ecosystems button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click aqara connect to ecosystems button: {str(e)}"
            )
            return False

    def get_ecosystem_google_home_button(self) -> uiautomator2.UiObject | None:
        """Get the ecosystem google home button element.

        Returns:
            uiautomator2.UiObject | None: The ecosystem google home button element
            if found,
                None otherwise
        """
        try:
            return self.device(
                className=constants.CLASS_ECOSYSTEM_GOOGLE_HOME_BUTTON,
                text=constants.CLASS_ECOSYSTEM_GOOGLE_HOME_BUTTON_TEXT,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get ecosystem google home button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get ecosystem google home button: {str(e)}")
            return None

    def click_ecosystem_google_home_button(self) -> bool:
        """Click the ecosystem google home button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_ecosystem_google_home_button()
            if button.wait(timeout=constants.TEN_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked ecosystem google home button.")
                return True
            self.logger.error("Failed to click ecosystem google home button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click ecosystem google home button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click ecosystem google home button: {str(e)}"
            )
            return False

    def get_automation_management_button(self) -> uiautomator2.UiObject | None:
        """Get the automation management button element.

        Returns:
            uiautomator2.UiObject | None: The automation management button element
            if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AUTOMATION_MANAGEMENT_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation management button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation management button: {str(e)}")
            return None

    def click_automation_management_button(self) -> bool:
        """Click the automation management button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_automation_management_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked automation management button.")
                return True
            self.logger.error("Failed to click automation management button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click automation management button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click automation management button: {str(e)}"
            )
            return False

    def get_bind_google_account_button(self) -> uiautomator2.UiObject | None:
        """Get the bind google account button element.

        Returns:
            uiautomator2.UiObject | None: The bind google account button element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AQARA_BIND_GOOGLE_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get bind google account button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get bind google account button: {str(e)}")
            return None

    def click_bind_google_account_button(self) -> bool:
        """Click the bind google account button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_bind_google_account_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked bind google account button.")
                return True
            self.logger.error("Failed to click bind google account button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click bind google account button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click bind google account button: {str(e)}")
            return False

    def get_connect_to_ecosystems_button(self) -> uiautomator2.UiObject | None:
        """Get the connect to ecosystems button element.

        Returns:
            uiautomator2.UiObject | None: The connect to ecosystems button element
            if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_CONNECT_TO_ECOSYSTEMS_BUTTON,
                text=constants.RESOURCE_ID_CONNECT_TO_ECOSYSTEMS_BUTTON_TEXT,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get connect to ecosystems button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get connect to ecosystems button: {str(e)}")
            return None

    def click_connect_to_ecosystems_button(self) -> bool:
        """Click the connect to ecosystems button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_connect_to_ecosystems_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked connect to ecosystems button.")
                return True
            self.logger.error("Failed to click connect to ecosystems button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click connect to ecosystems button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click connect to ecosystems button: {str(e)}"
            )
            return False

    def get_automation_management_left_button(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the automation management left button element.

        Returns:
            uiautomator2.UiObject | None: The automation management left button
            element if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AUTOMATION_MANAGEMENT_LEFT_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get automation management left button: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get automation management left button: {str(e)}"
            )
            return None

    def click_automation_management_left_button(self) -> bool:
        """Click the automation management left button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_automation_management_left_button()
            if button.wait(timeout=constants.TEN_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked automation management left button.")
                return True
            self.logger.error("Failed to click automation management left button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click automation management left button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click automation management left button: {str(e)}"
            )
            return False

    def check_ecosystem_google_home_button(self) -> bool:
        """Check the ecosystem google home button element.

        Returns:
            bool: True if the ecosystem google home button element is found, False
            otherwise
        """
        try:
            button = self.get_ecosystem_google_home_button().wait(
                timeout=constants.TEN_SECONDS
            )
            if button:
                self.logger.info("Found ecosystem google home button.")
                return True
            self.logger.error("Failed to find ecosystem google home button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to check ecosystem google home button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to check ecosystem google home button: {str(e)}"
            )
            return False

    def ecosystem_to_google_home_process(self) -> bool:
        """The ecosystem to google home process."""
        try:
            while True:
                if self.check_ecosystem_google_home_button():
                    self.logger.info("The Aqara Server is ready.")
                    self.click_ecosystem_google_home_button()
                    break
                else:
                    self.logger.info(
                        "The Aqara Server is not ready, back to the previous page."
                    )
                    self.click_automation_management_left_button()
                    self.click_connect_to_ecosystems_button()
                self.logger.info("Retry the ecosystem to google home process.")
                time.sleep(1)
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to ecosystem to google home process: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to ecosystem to google home process: {str(e)}")
            return False

    def get_switch_google_account_button(self) -> uiautomator2.UiObject | None:
        """Get the switch google account button element.

        Returns:
            uiautomator2.UiObject | None: The switch google account button element
            if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_SWITCH_GOOGLE_ACCOUNT_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get switch google account button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get switch google account button: {str(e)}")
            return None

    def click_switch_google_account_button(self) -> bool:
        """Click the switch google account button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_switch_google_account_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked switch google account button.")
                return True
            self.logger.error("Failed to click switch google account button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click switch google account button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click switch google account button: {str(e)}"
            )
            return False

    def get_user_is_logged_in(self) -> bool:
        """Get the user is logged in element.

        Returns:
            bool: True if the user is logged in, False otherwise
        """
        try:
            button = self.get_switch_google_account_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self.logger.info("The user is logged in.")
                return True
            self.logger.info("The user is not logged in.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get user is logged in: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to get user is logged in: {str(e)}")
            return False

    def get_add_exist_automation_button(self) -> uiautomator2.UiObject | None:
        """Get the add button element.

        Returns:
            uiautomator2.UiObject | None: The add button element if found.
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_ADD_BUTTON_EXISIT_AUTOMATION
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get add button element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get add button element: {str(e)}")
            return None

    def get_add_not_exist_automation_button(self) -> uiautomator2.UiObject | None:
        """Get the add button element.

        Returns:
            uiautomator2.UiObject | None: The add button element if found.
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_ADD_BUTTON_NOT_EXISIT_AUTOMATION
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get add button element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get add button element: {str(e)}")
            return None

    def click_add_exist_automation_button(
            self, timeout: int = constants.FIVE_SECONDS
    ) -> bool:
        """Click the add button.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(
                self.get_add_exist_automation_button(), timeout
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click add button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click add button: {str(e)}")
            return False

    def click_add_not_exist_automation_button(
            self, timeout: int = constants.FIVE_SECONDS
    ) -> bool:
        """Click the add button.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(
                self.get_add_not_exist_automation_button(), timeout
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click add button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click add button: {str(e)}")
            return False

    def get_aqara_ghp_switch_google_home_account_button(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the GHP switch Google Home account element.

        Returns:
            uiautomator2.UiObject | None: The GHP switch Google Home account element
            if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AQARA_GHP_SWITCH_GOOGLE_HOME_ACCOUNT,
                text="Switch Google Home Account",
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get GHP switch Google Home account: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get GHP switch Google Home account: {str(e)}"
            )
            return None

    def click_aqara_ghp_switch_google_home_account_button(
            self, timeout: int = constants.FIVE_SECONDS
    ) -> bool:
        """Click the GHP switch Google Home account button.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(
                self.get_aqara_ghp_switch_google_home_account_button(), timeout
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click GHP switch Google Home account: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click GHP switch Google Home account: {str(e)}"
            )
            return False

    def is_ghp_logged_in(self) -> bool:
        """Check if GHP is logged in.

        Returns:
            bool: True if GHP is logged in, False otherwise
        """
        try:
            if (
                    self.gms_ui.get_gms_account_element().wait(timeout=2)
                    or self.gms_ui.check_gms_choose_an_account_page()
            ):
                self.logger.info("GHP not logged in")
                return False
            button = self.get_aqara_ghp_switch_google_home_account_button().wait(
                timeout=10
            )
            self.logger.info(f"GHP logged in: {button}")
            return button
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check GHP logged in: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check GHP logged in: {str(e)}")
            return False

    def get_aqara_home_loading(self) -> uiautomator2.UiObject | None:
        """Get the aqara home loading element.

        Returns:
            uiautomator2.UiObject | None: The aqara home loading element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_LOADING
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get aqara home loading: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get aqara home loading: {str(e)}")
            return None

    def check_aqara_home_loading(self, timeout: int = 10) -> bool:
        """Check if aqara home loading element is present.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if aqara home loading element is present, False otherwise
        """
        try:
            loading = self.get_aqara_home_loading()
            if loading.wait(timeout=constants.TEN_SECONDS):
                if loading.wait_gone(timeout=timeout):
                    self.logger.info("Aqara home loading completed.")
                    return True
                else:
                    self.logger.info(f"Aqara home loading timeout {timeout} seconds.")
                    return False
            else:
                self.logger.info("Aqara home loading not found.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check aqara home loading: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check aqara home loading: {str(e)}")
            return False

    def get_bind_google_button(self) -> uiautomator2.UiObject | None:
        """Get the bind google button element.

        Returns:
            uiautomator2.UiObject | None: The bind google button element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AQARA_BIND_GOOGLE_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get bind google button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get bind google button: {str(e)}")
            return None

    def click_bind_google_button(self) -> bool:
        """Click the bind google button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_bind_google_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self.logger.info("Click bind google button.")
                return self._click_element(button)
            else:
                self.logger.error("Bind google button not found.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click bind google button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click bind google button: {str(e)}")
            return False

    def check_bind_google_button(self) -> bool:
        """Check if bind google button element is present.

        Returns:
            bool: True if bind google button element is present, False otherwise
        """
        try:
            button = self.get_bind_google_button()
            if button.wait(timeout=constants.TWO_SECONDS):
                self.logger.info("Bind google button found.")
                return True
            else:
                self.logger.error("Bind google button not found.")
                return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check bind google button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check bind google button: {str(e)}")
            return False

    def get_family_structure(self) -> uiautomator2.UiObject | None:
        """Get the family structure element.

        Returns:
            uiautomator2.UiObject | None: The family structure element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_FAMILY_STRUCTURE
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get family structure: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get family structure: {str(e)}")
            return None

    def click_family_structure(
            self, timeout: int = constants.FIVE_SECONDS
    ) -> bool:
        """Click the family structure element.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_family_structure(), timeout)

        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click family structure: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click family structure: {str(e)}")
            return False

    def get_family_structure_name(
            self, timeout: int = constants.FIVE_SECONDS
    ) -> str:
        """Get the family structure name element.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            str: The family structure name if found, empty string otherwise
        """
        try:
            structure_name = self.get_family_structure().get_text(timeout=timeout)
            self.logger.info(f"Aqara structure name loaded: {structure_name}")
            return structure_name
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get family structure name: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get family structure name: {str(e)}")
            return ""

    def get_automation_title_bar(self) -> uiautomator2.UiObject | None:
        """Get the automation title bar element.

        Returns:
            uiautomator2.UiObject | None: The automation title bar element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AUTOMATION_TITLE_BAR
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation title bar: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation title bar: {str(e)}")
            return None

    def get_automation_title_bar_text(
            self, timeout: int = constants.ONE_SECONDS
    ) -> str:
        """Get the automation title bar text element.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            str: The automation title bar text element if found, empty string
            otherwise
        """
        try:
            title_bar = self.get_automation_title_bar()
            if title_bar.wait(timeout=timeout):
                title_bar_text = title_bar.get_text(timeout=timeout)
                self.logger.info(f"Automation title bar text: {title_bar_text}")
                return title_bar_text
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation title bar text: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation title bar text: {str(e)}")
            return ""

    def get_add_button_automation(self) -> uiautomator2.UiObject | None:
        """Get the add button element.

        Returns:
            uiautomator2.UiObject | None: The add button element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_ADD_BUTTON_NOT_EXISIT_AUTOMATION
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get add button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get add button: {str(e)}")
            return None

    def get_add_button_with_automation(self) -> uiautomator2.UiObject | None:
        """Get the add button element.

        Returns:
            uiautomator2.UiObject | None: The add button element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_ADD_BUTTON_EXISIT_AUTOMATION
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get add button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get add button: {str(e)}")
            return None

    def get_all_automation_item(self) -> uiautomator2.UiObject | None:
        """Get the all automation item element.

        Returns:
            uiautomator2.UiObject | None: The all automation item element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AUTOMATION_ITEM
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get all automation item: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get all automation: {str(e)}")
            return None

    def get_all_automation_item_count(self) -> int:
        """Get the all automation item count element.

        Returns:
            int: The all automation item count element if found, 0 otherwise
        """
        try:
            if self.get_all_automation_item().wait(timeout=5):
                count = len(self.get_all_automation_item())
                self.ghp_session_device_linked_data["automation_count"] = count
                self.logger.info(f"All automation item count: {count}")
                return count
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get all automation item count: {str(e)}")
            return 0
        except RuntimeError as e:
            self.logger.error(f"Failed to get all automation item count: {str(e)}")
            return 0

    def get_automation_delete_button(self) -> uiautomator2.UiObject | None:
        """Get the automation delete button element.

        Returns:
            uiautomator2.UiObject | None: The automation delete button element if
            found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_DELETE_SLIDE_ITEM
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation delete button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation delete button: {str(e)}")
            return None

    def click_automation_delete_button(self) -> bool:
        """Click the automation delete button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_automation_delete_button())
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click automation delete button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click automation delete button: {str(e)}")
            return False

    def get_automation_dialog_ok_button(self) -> uiautomator2.UiObject | None:
        """Get the automation dialog ok button element.

        Returns:
            uiautomator2.UiObject | None: The automation dialog ok button element if
            found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(constants.RESOURCE_ID_DIALOG_RIGHT)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation dialog ok button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation dialog ok button: {str(e)}")
            return None

    def click_automation_dialog_ok_button(self) -> bool:
        """Click the automation dialog ok button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_automation_dialog_ok_button())
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click automation dialog ok button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click automation dialog ok button: {str(e)}"
            )
            return False

    def get_automation_item_name(self) -> str:
        """Get the automation item name element.

        Returns:
            str: The automation item name element if found, empty string otherwise
        """
        try:
            for i in self.get_all_automation_item().child():
                if i.info["text"]:
                    self.logger.info(f"Automation item name: {i.info['text']}")
                    return i.info["text"]
            return ""
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation item name: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation item name: {str(e)}")
            return ""

    def remove_all_automation(self) -> bool:
        """Remove all automation.

        Returns:
            bool: True if remove successful, False otherwise
        """
        try:
            if self.ghp_session_device_linked_data["automation_count"] == 0:
                return True
            while True:
                if self.get_add_not_exist_automation_button().wait(timeout=1):
                    break
                self.logger.info(
                    f"Remove automation: {self.get_automation_item_name()}"
                )
                self.get_all_automation_item().swipe("left")
                self.click_automation_delete_button()
                self.click_automation_dialog_ok_button()
                if self.check_aqara_home_loading(timeout=constants.FIVE_SECONDS):
                    self.logger.info("Remove automation completed.")
                else:
                    self.logger.info("Still loading...")
                time.sleep(0.5)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to remove all automation: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to remove all automation: {str(e)}")
            return False

    def get_create_automation_content(self) -> uiautomator2.UiObject | None:
        """Get the create automation content element.

        Returns:
            uiautomator2.UiObject | None: The create automation content element if
            found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_CREATE_AUTOMATION_CONTENT
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get create automation content: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get create automation content: {str(e)}")
            return None

    def get_dialog_close_button(self) -> uiautomator2.UiObject | None:
        """Get the dialog close button element.

        Returns:
            uiautomator2.UiObject | None: The dialog close button element if found,
            None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_DIALOG_CLOSE_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get dialog close button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get dialog close button: {str(e)}")
            return None

    def click_dialog_close_button(self) -> bool:
        """Click the dialog close button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_dialog_close_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self.logger.info("Click dialog close button.")
                return self._click_element(button)
            else:
                self.logger.error("Dialog close button not found, as expected.")
                return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click dialog close button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click dialog close button: {str(e)}")
            return False

    def get_create_automation_index_add_button(
            self, index: int
    ) -> uiautomator2.UiObject | None:
        """Finds the "Add" button within the create automation content at the specified index.

        Args:
          index: The zero-based index of the "Add" button to find.

        Returns:
          The child element with text "Add" at the given index, or None if not
          found.
        """
        try:
            button = self.get_create_automation_content()
            if button.wait(timeout=constants.TEN_SECONDS):
                self.logger.info("Create automation content found.")
                count = 0
                for i in button.child():
                    if i.info["text"] == "Add":
                        if count == index:
                            self.logger.info(f"Add button found at index {index}.")
                            return i
                        count += 1
                self.logger.error("Add button not found, as expected.")
                return None
            self.logger.error("Create automation content not found, as expected.")
            return None
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get create automation if element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get create automation if element: {str(e)}")
            return None

    def get_create_automation_if_add_button(self) -> uiautomator2.UiObject | None:
        """Get the create automation if add button element.

        Returns:
            uiautomator2.UiObject | None: The create automation if add button
            element if found,
            None otherwise
        """
        try:
            return self.get_create_automation_index_add_button(0)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get create automation if element: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get create automation if element: {str(e)}")
            return None

    def get_create_automation_then_add_button(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the create automation then add button element.

        Returns:
            uiautomator2.UiObject | None: The create automation then add button
            element if found,
            None otherwise
        """
        try:
            return self.get_create_automation_index_add_button(1)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get create automation then element: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get create automation then element: {str(e)}"
            )
            return None

    def click_create_automation_if_add_button(self) -> bool:
        """Click the create automation if add button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_create_automation_if_add_button())
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click create automation if element: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click create automation if element: {str(e)}"
            )
            return False

    def click_create_automation_then_add_button(self) -> bool:
        """Click the create automation then add button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_create_automation_then_add_button())
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click create automation then element: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click create automation then element: {str(e)}"
            )
            return False

    def get_automation_if_device(
            self, device_name: str
    ) -> uiautomator2.UiObject | None:
        """Get the automation if device element.

        Args:
            device_name (str): The name of the device

        Returns:
            uiautomator2.UiObject | None: The automation if device element if found,
                None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AUTOMATION_IF_DEVICE, device_name
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation if device: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation if device: {str(e)}")
            return None

    def get_automation_then_device(
            self, device_name: str
    ) -> uiautomator2.UiObject | None:
        """Get the automation then device element.

        Args:
            device_name (str): The name of the device

        Returns:
            uiautomator2.UiObject | None: The automation then device element if
            found,
                None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_AUTOMATION_THEN_DEVICE, device_name
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation then device: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation then device: {str(e)}")
            return None

    def click_automation_if_device(self, device_name: str) -> bool:
        """Click the automation if device element.

        Args:
            device_name (str): The name of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_automation_if_device(device_name))
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click automation if device: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click automation if device: {str(e)}")
            return False

    def click_automation_then_device(self, device_name: str) -> bool:
        """Click the automation then device element.

        Args:
            device_name (str): The name of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_automation_then_device(device_name))
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click automation then device: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click automation then device: {str(e)}")
            return False

    def get_device_status_button(
            self, status: str
    ) -> uiautomator2.UiObject | None:
        """Get the device status button element.

        Args:
            status (str): The status of the device

        Returns:
            uiautomator2.UiObject | None: The device status button element if found,
                None otherwise
        """
        try:
            return self._get_resource_id_element(
                constants.RESOURCE_ID_DEVICE_STATUS_BUTTON, status
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get device status button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get device status button: {str(e)}")
            return None

    def click_device_status_button(self, status: str) -> bool:
        """Click the device status button element.

        Args:
            status (str): The status of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            return self._click_element(self.get_device_status_button(status))
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click device status button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click device status button: {str(e)}")
            return False

    def get_starter_device_item(self, device_name: str) -> uiautomator2.UiObject:
        """Get the starter device item element.

        Args:
            device_name (str): The name of the device

        Returns:
            uiautomator2.UiObject: The starter device item element
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_STARTER_DEVICE_ITEM, text=device_name
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get starter device item: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get starter device item: {str(e)}")
            return None

    def click_starter_device_item(self, device_name: str) -> bool:
        """Click the starter device item element.

        Args:
            device_name (str): The name of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_starter_device_item(device_name)
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info(f"Clicked starter device: {device_name}")
                time.sleep(1)  # App animation
                return True
            self.logger.error(f"Failed to click starter device: {device_name}")
            return False

        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click starter device: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click starter device: {str(e)}")
            return False

    def get_starter_device_set_status(
            self, device_status: str
    ) -> uiautomator2.UiObject | None:
        """Get the starter device set status element.

        Args:
            device_status (str): The status of the device

        Returns:
            uiautomator2.UiObject | None: The starter device set status element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_STARTER_DEVICE_SET_STATUS,
                text=device_status,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get starter device set status: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get starter device set status: {str(e)}")
            return None

    def click_starter_device_set_status(self, device_status: str) -> bool:
        """Click the starter device set status element.

        Args:
            device_status (str): The status of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_starter_device_set_status(device_status)
            if button.wait(timeout=constants.TEN_SECONDS):
                self._click_element(button)
                self.logger.info(
                    f"Set the {device_status} status for the starter device."
                )
                time.sleep(1)  # App animation
                return True
            self.logger.error(
                f"Failed to set the {device_status} status for the starter device."
            )
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to set the {device_status} status for the starter device:"
                f" {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to set the {device_status} status for the starter device:"
                f" {str(e)}"
            )
            return False

    def get_action_device_item(
            self, device_name: str
    ) -> uiautomator2.UiObject | None:
        """Get the action device item element.

        Args:
            device_name (str): The name of the device

        Returns:
            uiautomator2.UiObject | None: The action device item element if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_ACTION_DEVICE_ITEM, text=device_name
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get action device item: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get action device item: {str(e)}")
            return None

    def click_action_device_item(self, device_name: str) -> bool:
        """Click the action device item element.

        Args:
            device_name (str): The name of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_action_device_item(device_name)
            if button.wait(timeout=constants.TEN_SECONDS):
                self._click_element(button)
                self.logger.info(f"Clicked action device: {device_name}")
                return True
            self.logger.error(f"Failed to click action device: {device_name}")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click action device: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click action device: {str(e)}")
            return False

    def get_action_device_set_status(
            self, device_status: str
    ) -> uiautomator2.UiObject | None:
        """Get the action device set status element.

        Args:
            device_status (str): The status of the device

        Returns:
            uiautomator2.UiObject | None: The action device set status element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_ACTION_DEVICE_SET_STATUS,
                textMatches=f"(?i).*{device_status}.*",
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get action device set status: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get action device set status: {str(e)}")
            return None

    def click_action_device_set_status(self, device_status: str) -> bool:
        """Click the action device set status element.

        Args:
            device_status (str): The status of the device

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_action_device_set_status(device_status)
            if button.wait(timeout=constants.TEN_SECONDS):
                try:
                    self.logger.info(
                        f'The "{button.get_text()}" status is detected for the action'
                        " device."
                    )
                except uiautomator2.exceptions.RPCError:
                    self.logger.info(
                        f'Set the "{device_status}" status for the action device.'
                    )
            self._click_element(button)
            return True
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to set the {device_status} status for the action device:"
                f" {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to set the {device_status} status for the action device:"
                f" {str(e)}"
            )
            return False

    def check_special_automation_title(self, title: str) -> bool:
        """Check the automation title element.

        Args:
            title (str): The title of the automation

        Returns:
            bool: True if the title is correct, False otherwise
        """
        try:
            button = self.device(
                resourceId=constants.RESOURCE_ID_TOOLBAR_TITLE, text=title
            )
            if button.wait(timeout=constants.TEN_SECONDS):
                self.logger.info(f"The {title} is detected.")
                return True
            self.logger.error(f"The {title} is not detected.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check automation title: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check automation title: {str(e)}")
            return False

    def get_create_automation_save_button(self) -> uiautomator2.UiObject | None:
        """Get the create automation save button element.

        Returns:
            uiautomator2.UiObject | None: The create automation save button element
            if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_CREATE_AUTOMATION_SAVE,
                text=constants.RESOURCE_ID_CREATE_AUTOMATION_SAVE_TEXT,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get create automation save button: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get create automation save button: {str(e)}"
            )
            return None

    def click_create_automation_save_button(self) -> bool:
        """Click the create automation save button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_create_automation_save_button()
            if button.wait(timeout=constants.TEN_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked create automation save button.")
                return True
            self.logger.error("Failed to click create automation save button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to click create automation save button: {str(e)}"
            )
            return False
        except RuntimeError as e:
            self.logger.error(
                f"Failed to click create automation save button: {str(e)}"
            )
            return False

    def get_automation_description_edit_text_element(
            self,
    ) -> uiautomator2.UiObject | None:
        """Get the automation description edit text element.

        Returns:
            uiautomator2.UiObject | None: The automation description edit text
            element if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AUTOMATION_DESCRIPTION_EDIT_TEXT
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(
                f"Failed to get automation description edit text: {str(e)}"
            )
            return None
        except RuntimeError as e:
            self.logger.error(
                f"Failed to get automation description edit text: {str(e)}"
            )
            return None

    def get_automation_description_text(self) -> str:
        """Get the automation description text element.

        Returns:
            str: The automation description text element if found, empty string
            otherwise
        """
        try:
            button = self.get_automation_description_edit_text_element()
            if button.wait(timeout=constants.FIVE_SECONDS):
                return button.get_text()
            self.logger.error("Failed to get automation description text.")
            return ""
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation description text: {str(e)}")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation description text: {str(e)}")
            return ""

    def get_automation_ok_button(self) -> uiautomator2.UiObject | None:
        """Get the automation ok button element.

        Returns:
            uiautomator2.UiObject | None: The automation ok button element if found,
                None otherwise
        """
        try:
            return self.device(resourceId=constants.RESOURCE_ID_AUTOMATION_OK_BUTTON)
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation ok button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation ok button: {str(e)}")
            return None

    def click_automation_ok_button(self) -> bool:
        """Click the automation ok button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_automation_ok_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked automation ok button.")
                return True
            self.logger.error("Failed to click automation ok button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click automation ok button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click automation ok button: {str(e)}")
            return False

    def get_automation_cancel_button(self) -> uiautomator2.UiObject | None:
        """Get the automation cancel button element.

        Returns:
            uiautomator2.UiObject | None: The automation cancel button element if
            found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AUTOMATION_CANCEL_BUTTON
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation cancel button: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation cancel button: {str(e)}")
            return None

    def click_automation_cancel_button(self) -> bool:
        """Click the automation cancel button element.

        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            button = self.get_automation_cancel_button()
            if button.wait(timeout=constants.FIVE_SECONDS):
                self._click_element(button)
                self.logger.info("Clicked automation cancel button.")
                return True
            self.logger.error("Failed to click automation cancel button.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to click automation cancel button: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to click automation cancel button: {str(e)}")
            return False

    def get_automation_create_automation(
            self, automation_name: str
    ) -> uiautomator2.UiObject | None:
        """Get the automation create automation element.

        Args:
            automation_name (str): The name of the automation

        Returns:
            uiautomator2.UiObject | None: The automation create automation element
            if found,
                None otherwise
        """
        try:
            return self.device(
                resourceId=constants.RESOURCE_ID_AUTOMATION_EXIST_AUTOMATION,
                text=automation_name,
            )
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to get automation create automation: {str(e)}")
            return None
        except RuntimeError as e:
            self.logger.error(f"Failed to get automation create automation: {str(e)}")
            return None

    def check_automation_exist(self, automation_name: str) -> bool:
        """Check the automation exist element.

        Args:
            automation_name (str): The name of the automation

        Returns:
            bool: True if the automation exist, False otherwise
        """
        try:
            button = self.get_automation_create_automation(automation_name)
            if button.wait(timeout=constants.FIVE_SECONDS):
                self.logger.info(f"The \"{automation_name}\" is detected.")
                return True
            self.logger.error(f"The \"{automation_name}\" is not detected.")
            return False
        except uiautomator2.exceptions.RPCError as e:
            self.logger.error(f"Failed to check automation exist: {str(e)}")
            return False
        except RuntimeError as e:
            self.logger.error(f"Failed to check automation exist: {str(e)}")
            return False