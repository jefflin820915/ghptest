import re
import time
import os
import subprocess
import signal
import zipfile

from common import constants
from common.constants import DeviceState
from utils import logging_utils

logcat_file_path = None

class DeviceBasic:

    def start_logging(self, log_folder_path) -> None:
        """Start the controller logging."""
        self.logcat_file_path = None
        self._adb_start_log_process = None
        logging_utils.get_logger(__name__).info('Start the logging')
        # collect adb logact log
        logging_utils.get_logger(__name__).info("starting get logcat")
        self.ctrlr_logcat_file_name = ('abd_logcat_' + constants.TIMESTAMP + '.log')
        self.logcat_file_path = os.path.join(f"{log_folder_path}", self.ctrlr_logcat_file_name)
        cmd = f'adb logcat > "{self.logcat_file_path}"'
        logging_utils.get_logger(__name__).info(cmd)
        process = subprocess.Popen(cmd, shell=True)
        self._adb_start_log_process = process
        logging_utils.get_logger(__name__).info('%s is logging', self.ctrlr_logcat_file_name)

        logging_utils.get_logger(__name__).info("starting get hublog")
        self.ctrlr_logcat_file_name = ('hublog_' + constants.TIMESTAMP + '.log')
        hub_log_file_path = os.path.join(f"{log_folder_path}", self.ctrlr_logcat_file_name)
        cmd = ('curl -k -X GET https://192.168.86.237:8443/setup/get_logs --output ' + f'"{hub_log_file_path}"')
        logging_utils.get_logger(__name__).info(cmd)
        process = subprocess.Popen(cmd, shell=True)
        self._adb_start_log_process = process
        logging_utils.get_logger(__name__).info('%s is logging', self.ctrlr_logcat_file_name)

    def compress_logcat(self, delete_original: bool = True, compression_level: int =zipfile.ZIP_DEFLATED) -> None:
        """
        Stops the ongoing logcat capture and compresses the log file.
        Args:
            delete_original (bool): If True, deletes the original .log file after compression.
            compression_level (int): ZIP compression level (e.g., zipfile.ZIP_DEFLATED).
        """
        if self._adb_start_log_process is None:
            logging_utils.get_logger(__name__).warning("No active logcat process to stop.")
            return

        logging_utils.get_logger(__name__).info("Stopping logcat capture...")
        # Terminate the adb logcat process
        self._adb_start_log_process.terminate()
        self._adb_start_log_process.wait(timeout=5) # Wait for the process to terminate gracefully
        # Compress the log file
        if os.path.exists(self.logcat_file_path):
            zip_filename = self.logcat_file_path.replace('.log', '.zip')
            logging_utils.get_logger(__name__).info(f"Compressing log file to {zip_filename}...")
            with zipfile.ZipFile(zip_filename, 'w', compression_level) as zf:
                zf.write(self.logcat_file_path, os.path.basename(self.logcat_file_path))
            logging_utils.get_logger(__name__).info(f"Log file compressed. Compressed size: {os.path.getsize(zip_filename) / (1024*1024):.2f} MB")

            if delete_original:
                os.remove(self.logcat_file_path)
                logging_utils.get_logger(__name__).info(f"Original log file deleted: {self.logcat_file_path}")
        else:
            logging_utils.get_logger(__name__).warning(f"Log file not found for compression: {self.logcat_file_path}")

    @staticmethod
    def create_log_folder(folder_name = None) -> str:
        """Create log folder."""
        timestamp = constants.TIMESTAMP
        base_log_path = os.path.join(os.getcwd(), f"{constants.LOG_PATH}")
        log_main_folder = logging_utils.create_log_folder(base_log_path, f"LOG_{timestamp}")
        log_folder_path = logging_utils.create_log_folder(log_main_folder, f"LOG_{timestamp}_{folder_name}")
        logging_utils.get_logger(__name__, log_folder_path).info(f"Log files will be saved to: {log_folder_path}")
        return log_folder_path

    def get_device_state_on_gha(self, device_name, gha_ui):
        """Check the light state.

        Args:
        device_name (str): The name of the device to locate.
        gha_ui: An object representing the Google Home App UI
      interactions

        Returns:
          state, if the device is on/off/offline/locked/unlocked.
        """
        time.sleep(constants.THREE_SECONDS)

        window_dump = gha_ui.device.dump_hierarchy()
        logging_utils.get_logger(__name__).debug('window_dump=%s', window_dump)

        base_regex = (
            f'text="{device_name}" '
            f'resource-id="com.google.android.apps.chromecast.app:id/title" '
            f'class="android.widget.TextView" '
            f'package="com.google.android.apps.chromecast.app".*?\n.*?'
            f'<node index="2" text="'
        )

        state_patterns = {
            DeviceState.OFFLINE: base_regex + 'Offline"',
            DeviceState.ON: base_regex + 'On.*"',
            DeviceState.OFF: base_regex + 'Off"',
            DeviceState.LOCKED: base_regex + 'Locked"',
            DeviceState.UNLOCKED: base_regex + 'Unlocked"',
        }

        for state, pattern in state_patterns.items():
            if re.search(pattern, window_dump):
                logging_utils.get_logger(__name__).info('%s is %s', device_name, state.name)
                return state
        logging_utils.get_logger(__name__).info('Could not determine the state of %s', device_name)
        return DeviceState.UNKNOWN

    def start_recording(self, test_method_name) -> None:
        """"Start screen recording."""
        logging_utils.get_logger(__name__).info(f"Start screen recording for {test_method_name}")
        self.rcrd_file_name = f"{constants.TIMESTAMP}_{test_method_name}"

        cmd = (f'adb shell screenrecord --bugreport ' +
               f'/sdcard/{self.rcrd_file_name}.mp4')

        logging_utils.get_logger(__name__).info(cmd)

        process = subprocess.Popen(cmd, shell=True)
        self._adb_screenrecord_process = process

    def stop_recording(self, folder_path) -> None:
        """Stop screen recording."""

        logging_utils.get_logger(__name__).info("Stop screen recording")
        if not hasattr(self, '_adb_screenrecord_process'):
            return
        if self._adb_screenrecord_process is None:
            return
        try:
            logging_utils.get_logger(__name__).info('Attempting to stop screen recording process with PID %d', self._adb_screenrecord_process.pid)
            os.kill(self._adb_screenrecord_process.pid, signal.SIGINT)  # Send interrupt signal to stop cleanly
            self._adb_screenrecord_process.wait(timeout=constants.TEN_SECONDS)  # Give it some time to stop
            if self._adb_screenrecord_process.poll() is None:
                logging_utils.get_logger(__name__).info('Screen recording process did not terminate gracefully, attempting SIGTERM.')
                os.kill(self._adb_screenrecord_process.pid, signal.SIGTERM)
                self._adb_screenrecord_process.wait(timeout=constants.TEN_SECONDS)
                if self._adb_screenrecord_process.poll() is None:
                    logging_utils.get_logger(__name__).info('Failed to stop screen recording process.')
                    return
        except OSError as e:
            logging_utils.get_logger(__name__).info('Error while trying to stop screen recording process: %s', e)
        finally:
            self._adb_screenrecord_process = None

        time.sleep(constants.ONE_SECONDS)

        # Flush the data from the memory to the storage
        cmd = ('adb shell sync')
        logging_utils.get_logger(__name__).info(cmd)
        process = subprocess.Popen(cmd, shell=True)
        self._adb_screenrecord_process = process

        # Pull the video from the phone
        logging_utils.get_logger(__name__).info('Start pulling videos from device, this may take some time...')
        if hasattr(self, 'log_folder_path'):
            folder_path = self.log_folder_path
        try:
            cmd = (f'adb pull' + f' /sdcard/{self.rcrd_file_name}.mp4 ' + folder_path)
            logging_utils.get_logger(__name__).info(cmd)
            process = subprocess.Popen(cmd, shell=True)
            self._adb_screenrecord_process = process
            logging_utils.get_logger(__name__).info('%s.mp4 is saved to %s', self.rcrd_file_name, folder_path)
        except subprocess.CalledProcessError:
            logging_utils.get_logger(__name__).info('Failed to pull recording.')