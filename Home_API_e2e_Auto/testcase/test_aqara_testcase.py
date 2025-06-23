"""Test case for Aqara."""
from common import constants
from common.device_base import DeviceBasic
import pytest
# Local application imports
from utils import config_manager
from utils import logging_utils


@pytest.mark.usefixtures("device")
class TestAqaraTestCase:
    """Test Aqara to GHP link process."""

    def setup_method(self, method):
        self.test_method_name = method.__name__
        self.log_folder_path = DeviceBasic.create_log_folder(__class__.__name__)
        self._logger = logging_utils.get_logger(__name__, self.log_folder_path)
        self._logger.info(f"Executing setup before test: {self.test_method_name}")
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("aqara-home-40727.json")
        DeviceBasic.start_logging(self, self.log_folder_path)
        DeviceBasic.start_recording(self, self.test_method_name)

    def teardown_method(self):
        self._logger.info(f"Executing teardown after test. {self.test_method_name}")
        DeviceBasic.stop_recording(self, self.log_folder_path)

    def test_aqara_to_ghp_link_allow_process(
            self, aqara_ui, gms_ui, mode=True
    ) -> bool:
        """Tests the process of linking Aqara Home App to GHP.

        This test function simulates the user-initiated process of linking
        Aqara Home to Google Home from the Aqara Home App and verifies that
        the user can successfully select a Google account and allow Aqara Home
        to access Google Home Platform API permissions.

        Args:
            aqara_ui: An object representing the Aqara Home App UI interactions.
            gms_ui: An object representing the Google Mobile Services UI
              interactions
            mode (bool, optional): The mode to set the toggle button. If True
              (boolean), it will enable the GHP API toggle button. If False
              (boolean), it will disable the GHP API toggle button.
              (NoneType), it will not set the toggle button.

        Returns:
            bool: True if the linking and allowing process is successful, False
            otherwise.
        """
        aqara_ui.stop_aqara_app()
        aqara_ui.start_aqara_app()
        if aqara_ui.is_aqara_home_page():
            aqara_ui.click_profile_button()
        aqara_ui.click_dialog_close_button()
        aqara_ui.click_google_home_automations()
        if aqara_ui.check_bind_google_button():
            aqara_ui.click_bind_google_button()
        if not aqara_ui.check_aqara_home_loading():
            self._logger.error("Aqara home loading timeout.")
            assert False
        if aqara_ui.is_ghp_logged_in():
            aqara_ui.click_aqara_ghp_switch_google_home_account_button()
        aqara_ui.click_gms_google_test_account()
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        gms_ui.click_ghp_session_device_type_linked()
        gms_ui.get_ghp_api_device_linked_data(mode=mode)
        gms_ui.find_ghp_allow_link_button_and_click()
        assert True

    def test_aqara_to_ghp_link_cancel_process(self, aqara_ui, gms_ui) -> bool:
        """Test Aqara Home App to GHP USER cancel process.

        This test function simulates the user-initiated process of linking
        Aqara Home to Google Home from the Aqara Home App and verifies that
        the user can successfully cancel the GHP Oauth connection.

        Args:
            aqara_ui: An object representing the Aqara Home App UI interactions.
            gms_ui: An object representing the Google Mobile Services UI
              interactions

        Returns:
            bool: True if the linking and allowing process is successful, False
            otherwise.
        """
        aqara_ui.stop_aqara_app()
        aqara_ui.start_aqara_app()
        if aqara_ui.is_aqara_home_page():
            aqara_ui.click_profile_button()
        aqara_ui.click_dialog_close_button()
        aqara_ui.click_google_home_automations()
        if aqara_ui.check_bind_google_button():
            aqara_ui.click_bind_google_button()
        if not aqara_ui.check_aqara_home_loading():
            self._logger.error("Aqara home loading timeout.")
            assert False
        if aqara_ui.is_ghp_logged_in():
            aqara_ui.click_aqara_ghp_switch_google_home_account_button()
        aqara_ui.click_gms_google_test_account()
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        gms_ui.find_ghp_cancel_link_button_and_click()
        if not aqara_ui.check_aqara_home_loading():
            self._logger.error("Aqara home loading timeout.")
            assert False
        assert True

    def test_aqara_remove_all_automation(self, aqara_ui, gms_ui):
        """Test Aqara remove all automation process.

        This test function simulates the user-initiated process of removing
        all automations in the Aqara Home App and verifies that the user
        can successfully remove all automations.

        Args:
            aqara_ui: An object representing the Aqara Home App UI interactions.
            gms_ui: An object representing the Google Mobile Services UI
              interactions
        """
        self.test_aqara_to_ghp_link_cancel_process(aqara_ui, gms_ui)
        aqara_ui.remove_all_automation()
        assert True

    def test_ghp_session_device_linked_process(self, gms_ui) -> bool:
        """Test GHP session device linked process.

        This test function simulates the user-initiated process of linking
        a device to a GHP session and verifies that the user can successfully
        link a device to a GHP session.

        Args:
            gms_ui: An object representing the Google Mobile Services UI
              interactions
        """
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        gms_ui.click_ghp_session_device_type_linked()
        gms_ui.get_ghp_api_device_linked_data(mode=True)
        gms_ui.find_ghp_allow_link_button_and_click()
        assert True

    def test_aqara_automation_create_empty_process(
            self, aqara_ui, gms_ui
    ) -> bool:
        """Test Aqara automation create empty process.

        This test function simulates the user-initiated process of creating
        an empty automation in the Aqara Home App and verifies that the user
        can successfully create an empty automation.

        Args:
            aqara_ui: An object representing the Aqara Home App UI interactions.
            gms_ui: An object representing the Google Mobile Services UI
              interactions

        Returns:
            bool: True if the automation creation process is successful, False
            otherwise.
        """
        self.test_aqara_to_ghp_link_allow_process(aqara_ui, gms_ui)
        aqara_ui.get_family_structure_name()
        if (
                aqara_ui.get_automation_title_bar_text()
                == constants.AQARA_CHOOSE_FAMILY_TITLE_BAR_TEXT
        ):
            aqara_ui.click_family_structure()
        aqara_ui.get_automation_title_bar_text()
        aqara_ui.get_all_automation_item_count()
        aqara_ui.remove_all_automation()
        aqara_ui.click_add_not_exist_automation_button()
        aqara_ui.click_create_automation_if_add_button()
        device_starter = self.config_manager.get_starter_device_list()
        device_starter_status = (
            self.config_manager.get_starter_device_status_list()
        )
        device_action = self.config_manager.get_action_device_list()
        device_action_status = self.config_manager.get_action_device_status_list()
        automation_config_number = -1
        aqara_ui.click_starter_device_item(
            device_name=device_starter[automation_config_number]
        )  # TODO: b/423821705 - change to all device
        aqara_ui.click_starter_device_set_status(
            device_status=device_starter_status[automation_config_number]
        )  # TODO: b/423821705 - change to all device status
        aqara_ui.click_create_automation_then_add_button()
        aqara_ui.click_action_device_item(
            device_name=device_action[automation_config_number]
        )
        aqara_ui.click_action_device_set_status(
            device_status=device_action_status[automation_config_number]
        )
        aqara_ui.click_create_automation_save_button()
        automation_text = aqara_ui.get_automation_description_text()
        aqara_ui.click_automation_ok_button()
        if not aqara_ui.check_aqara_home_loading(35):
            self.logger.error("Aqara home create automation loading timeout.")
            assert False
        assert aqara_ui.check_automation_exist(automation_text)
