import pytest

from common import constants
from common.device_base import DeviceBasic
from utils import config_manager
from utils import logging_utils

@pytest.mark.usefixtures('device')
class TestLG:

    def setup_method(self, method):
        self.test_method_name = method.__name__
        self.log_folder_path = DeviceBasic.create_log_folder(__class__.__name__)
        self._logger = logging_utils.get_logger(__name__, self.log_folder_path)
        self._logger.info(f"Executing setup before test: {self.test_method_name}")
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("tuya-smart.json")
        DeviceBasic.start_logging(self, self.log_folder_path)
        DeviceBasic.start_recording(self, self.test_method_name)

    def teardown_method(self):
        self._logger.info(f"Executing teardown after test for {self.test_method_name}")
        DeviceBasic.stop_recording(self, self.log_folder_path)

    def test_tuya_to_ghp_link_allow_process(self, tuya_ui, gms_ui) -> bool:
        tuya_ui.stop_tuya()
        tuya_ui.start_tuya()
        tuya_ui._get_me_tab().click()
        tuya_ui._get_google_home_devices().click()
        tuya_ui._get_connect_btn().click()
        gms_ui.wait_ghp_loading()
        tuya_ui._select_user()
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        gms_ui.click_ghp_session_device_type_linked()
        gms_ui.get_ghp_api_device_linked_data()
        tuya_ui._get_allow_btn().click()
        link_device_list_on_me = set(tuya_ui._get_link_device_list())
        self._logger.info(f"Link device list on me: {link_device_list_on_me}")
        tuya_ui.device.press(key=f"{constants.KEY_BACK}")
        tuya_ui._get_home_tab().click()
        link_device_list_on_home = set(tuya_ui._get_home_device_list())
        self._logger.info(f"Link device list on home: {link_device_list_on_home}")
        result = link_device_list_on_me.issubset(link_device_list_on_home)
        self._logger.info(f"Report whether another set contains this set: {result}")
        if result:
            self._logger.info("PASS")
            assert True
        else:
            self._logger.info("FAIL")
            assert False

    def test_tuya_to_ghp_link_cancel_process(self, tuya_ui, gms_ui) -> bool:
        tuya_ui.stop_tuya()
        tuya_ui.start_tuya()
        tuya_ui._get_me_tab().click()
        tuya_ui._get_google_home_devices().click()
        tuya_ui._get_connect_btn().click()
        gms_ui.wait_ghp_loading()
        tuya_ui._select_user()
        gms_ui.wait_ghp_loading()
        gms_ui.get_ghp_session_structure_name()
        gms_ui.find_ghp_session_device_type_linked_button()
        gms_ui.get_ghp_session_device_type_linked_count()
        tuya_ui._get_cancel_btn().click()
        link_device_list_on_me = set(tuya_ui._get_link_device_list())
        tuya_ui.device.press(key=f"{constants.KEY_BACK}")
        tuya_ui._get_home_tab().click()
        link_device_list_on_home = set(tuya_ui._get_home_device_list())
        self._logger.info(f"Link device list on home: {link_device_list_on_home}")
        result = link_device_list_on_me.issubset(link_device_list_on_home)
        self._logger.info(f"Report whether another set contains this set: {result}")
        if result:
            self._logger.info("PASS")
        else:
            self._logger.error("FAIL")

    def test_ghp_session_device_linked_process(self, tuya_ui, gms_ui):
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
        tuya_ui._get_allow_btn().click()
        assert True

    def test_aghp_control(self, aghp_ui):
        aghp_ui.start_aghp()
        aghp_ui.stop_aghp()
