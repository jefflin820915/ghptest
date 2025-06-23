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
        self.config_manager = config_manager.ConfigManager()
        self.config_manager.load_config("tuya-smart.json")

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

