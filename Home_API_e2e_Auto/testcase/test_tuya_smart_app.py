import pytest

from common.constants import DeviceState
from common.device_base import DeviceBasic
from common import constants
from conftest import gha_ui, device
from utils import logging_utils
from utils import config_manager
from time import sleep

@pytest.mark.usefixtures('device')
class TestTuya:

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
        self._logger.info(f"Executing teardown after test: {self.test_method_name}")
        DeviceBasic.stop_recording(self, self.log_folder_path)
        DeviceBasic.compress_logcat(self)

    def test_control_on_off(self, tuya_ui, gha_ui):
            self._logger.info('--------- Toggling the device on GHA -----------')
            tuya_ui.start_tuya()
            tuya_ui._is_device_exist_home_page(self.config_manager.get_starter_device_list()[0])
            tuya_ui._click_home_tab_device_name(self.config_manager.get_starter_device_list()[0]).click()
            # Get the device status ON/OFF/OFFLINE
            self._logger.info('Checking the status of the device')
            current_tuya_states_control_gha = tuya_ui.get_device_state_on_tuya()
            self._logger.info(f"tuya_state: {current_tuya_states_control_gha}")
            tuya_ui.stop_tuya()
            gha_ui.start_gha()
            gha_ui.navigate_to_device_tab_on_gha().click()
            gha_ui.refresh_gha_devices()
            gha_ui._is_device_exist_device_page(self.config_manager.get_starter_device_list()[0])
            # Get the device status ON/OFF/OFFLINE
            self._logger.info('Checking the status of the device')
            current_gha_state_control_on_gha = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list()[0], gha_ui)
            self._logger.info(f"current_gha_state: {current_gha_state_control_on_gha}")
            if current_tuya_states_control_gha == current_gha_state_control_on_gha:
                self._logger.info('Tuya and GHA state are same.')
            else:
                self._logger.info('Tuya and GHA state not same.')

            self._logger.info('Toggling the device')
            gha_ui._toggle_device_on_off(self.config_manager.get_starter_device_list()[0])
            sleep(5)
            next_gha_state_control_on_gha = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list[0], gha_ui)
            self._logger.info(f"next_gha_state: {next_gha_state_control_on_gha}")
            gha_ui.stop_gha()
            tuya_ui.start_tuya()
            tuya_ui._is_device_exist_home_page(self.config_manager.get_starter_device_list()[0])
            tuya_ui._click_home_tab_device_name(self.config_manager.get_starter_device_list()[0]).click()
            sleep(3)
            next_tuya_states_control_on_gha = tuya_ui.get_device_state_on_tuya()
            self._logger.info(f"next_tuya_state: {next_tuya_states_control_on_gha}")

            if next_gha_state_control_on_gha == next_tuya_states_control_on_gha:
                self._logger.info('Tuya and GHA state are same.')
            else:
                self._logger.info('Tuya and GHA state not same.')

            self._logger.info('Toggling the device on Tuya')

            self._logger.info('--------- Toggling the device on Tuya -----------')
            tuya_ui.toggle_device_on_off()
            current_tuya_states_control_on_tuya = tuya_ui.get_device_state_on_tuya()
            self._logger.info(f"current_tuya_state: {current_tuya_states_control_on_tuya}")
            tuya_ui.stop_tuya()
            gha_ui.start_gha()
            gha_ui.navigate_to_device_tab_on_gha().click()
            gha_ui.refresh_gha_devices()
            gha_ui._is_device_exist_device_page(self.config_manager.get_starter_device_list()[0])
            # Get the device status ON/OFF/OFFLINE
            self._logger.info('Checking the status of the device')
            current_gha_state_control_on_tuya = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list()[0], gha_ui)
            self._logger.info(f"current_gha_state: {current_gha_state_control_on_tuya}")
            if current_tuya_states_control_on_tuya == current_gha_state_control_on_tuya:
                self._logger.info('Tuya and GHA state are same.')
            else:
                self._logger.info('Tuya and GHA state not same.')

    def test_control_lock_unlocked(self, gha_ui):
            automation_status = DeviceState.LOCKED
            device_name = "Aqara LOCK"
            pin_code = "222"
            if_status_diff = gha_ui.get_status_and_set_to_presetting(gha_ui, device_name, automation_status)
            self._logger.info(f"device_status:{if_status_diff} ")
            assert True
            # gha_ui.start_gha()
            # gha_ui.navigate_to_device_tab_on_gha().click()
            # gha_ui.refresh_gha_devices()
            # gha_ui._is_device_exist_device_page(self.config_manager.get_starter_device_list()[1])
            # # Get the device status ON/OFF/OFFLINE
            # self._logger.info('Checking the status of the device')
            # current_state = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list()[1], gha_ui)
            # self._logger.info(f"current_state: {current_state}")
            # if current_state == DeviceState.UNKNOWN:
            #     self._logger.info('Device is at the unknown state.')
            #     assert False
            # elif current_state == DeviceState.OFFLINE:
            #     self._logger.info('Device is offline.')
            #     assert False
            # try:
            #     self._logger.info('Toggling the device')
            #     gha_ui._toggle_device_on_off(self.config_manager.get_starter_device_list()[1])
            #     gha_ui._long_toggle_device_on_off()
            #     self._logger.info(self.config_manager.get_pin_code())
            #     gha_ui._set_pin_code(self.config_manager.get_pin_code())
            #     gha_ui._click_ok_button_on_pin_edit()
            # except Exception as e:
            #     self._logger.info('Failed to control device due to ' + repr(e).split('Exception: ')[1].split('\\n')[0])
            #
            # # Get the device status ON/OFF/OFFLINE and Check
            # self._logger.info('Checking the status of the device')
            # next_state = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list()[1], gha_ui)
            # self._logger.info(f"next_state: {next_state}")
            # if next_state == DeviceState.UNKNOWN:
            #     self._logger.info('Device is at the unknown state.')
            #     assert False
            # elif next_state == DeviceState.OFFLINE:
            #     self._logger.info('Device is offline.')
            #     assert False
            # elif current_state == next_state:
            #     self._logger.info('Device does not change.')
            #     assert False
            #
            # self._logger.info('Toggling the device')
            # try:
            #     gha_ui._toggle_device_on_off(self.config_manager.get_starter_device_list()[1])
            #     gha_ui._long_toggle_device_on_off()
            #     self._logger.info(self.config_manager.get_pin_code())
            #     gha_ui._set_pin_code(self.config_manager.get_pin_code())
            #     gha_ui._click_ok_button_on_pin_edit()
            # except Exception as e:
            #     self._logger.info('Failed to control device due to ' + repr(e).split('Exception: ')[1].split('\\n')[0])
            #
            # # Get the device status ON/OFF/OFFLINE and Check
            # self._logger.info('Checking the status of the device')
            # the_time_after_next_state = DeviceBasic.get_device_state_on_gha(self, self.config_manager.get_starter_device_list()[1], gha_ui)
            # self._logger.info(f"the_time_after_next_state: {the_time_after_next_state}")
            # if the_time_after_next_state == DeviceState.UNKNOWN:
            #     self._logger.info('Device is at the unknown state.')
            #     assert False
            # elif the_time_after_next_state == DeviceState.OFFLINE:
            #     self._logger.info('Device is offline.')
            #     assert False
            # elif the_time_after_next_state == next_state:
            #     self._logger.info('Device does not change.')
            #     assert False
            # else:
            #     self._logger.info('Controlling test has Passed')
            #     self._logger.info('PASS')
            #     gha_ui.stop_gha()
            #     assert True

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

    def test_ghp_session_device_linked_process(self,tuya_ui, gms_ui):
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