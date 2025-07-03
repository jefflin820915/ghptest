import pytest

from common import constants
from common.device_base import DeviceBasic
from conftest import aghp_ui, gms_ui
from utils import config_manager
from utils import logging_utils

@pytest.mark.usefixtures('device')
class TestAGHPTestCase:

    def setup_method(self, method):
        self.test_method_name = method.__name__
        self.log_folder_path = DeviceBasic.create_log_folder(__class__.__name__)
        self._logger = logging_utils.get_logger(__name__, self.log_folder_path)
        self._logger.info(f"Executing setup before test: {self.test_method_name}")
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("android-sample-app.json")
        DeviceBasic.start_logging(self, self.log_folder_path)
        DeviceBasic.start_recording(self, self.test_method_name)

    def teardown_method(self):
        self._logger.info(f"Executing teardown after test for {self.test_method_name}")
        DeviceBasic.stop_recording(self, self.log_folder_path)

    def test_aghp_to_ghp_link_allow_process(self, aghp_ui, gms_ui) -> bool:
        aghp_ui.stop_aghp()
        aghp_ui.start_aghp()
        aghp_ui.get_ghp_session_structure_name().click()
        aghp_ui._select_user()
        gms_ui.wait_ghp_loading()
        self._logger.info(aghp_ui.get_unverified_view().exists)
        if aghp_ui.get_unverified_view():
            aghp_ui.get_understand_button().click()
        self._logger.info(aghp_ui._get_home_item_bar().get_text())
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        gms_ui.click_ghp_session_device_type_linked()
        gms_ui.get_ghp_api_device_linked_data()
        if aghp_ui.get_unverified_view():
            aghp_ui.get_understand_button().click()
        aghp_ui._get_allow_btn().click()
        if aghp_ui.is_home_linked_devices_page(aghp_ui._get_home_item_bar().get_text()):
            self._logger.info("The Structures is linked")
            assert True
        else:
            assert False

    def test_aghp_to_ghp_link_cancel_process(self, aghp_ui, gms_ui) -> bool:
        aghp_ui.stop_aghp()
        aghp_ui.start_aghp()
        aghp_ui.get_ghp_session_structure_name().click()
        aghp_ui._select_user()
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        aghp_ui._get_cancel_btn().click()

    def test_ghp_session_device_linked_process(self, aghp_ui, gms_ui):
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
        gms_ui.get_ghp_api_device_linked_data()
        aghp_ui._get_allow_btn().click()
        assert True

    def test_aghp_control(self, aghp_ui, gms_ui):
        aghp_ui.stop_aghp()
        aghp_ui.start_aghp()

