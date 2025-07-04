import enum
import time

# GMS
GMS_PACKAGE = "com.google.android.gms"
GMS_ADD_MORE_DETAIL_ID = "gm_tooltip_action_button"
GMS_FEEDBACK_TEXT_EDIT_ID = "text_input_edit_text"

# GHA
GHA_PACKAGE = "com.google.android.apps.chromecast.app"
GHA_FEEDBACK_CATEGORY_LIST = ["Nest Hub", "Google Home app"]
GHA_DEVICE_TAB_ID = "com.google.android.apps.chromecast.app:id/bottom_navigation_bar_devices_item"
GHA_NAVIGATION_FRAME_ID = "main_navigation_pager"
GHA_REFRESH_SPINNER_ID = "home_view_refresh_layout"
GHA_USER_ICON_ID = "og_apd_internal_image_view"
GHA_USER_ACCOUNT_ID = "og_secondary_account_information"
GHA_USER_ACCOUNT_INFO_CLOSE_BTN = "og_header_close_button"
GHA_USER_ACCOUNT_FRAME_ID = "og_has_selected_content"
GHA_FEEDBACK_BUTTON_ID = "og_text_card_title"
GHA_DEVICE_CONTROL_ID = "control"
GHA_CATEGORY_ID = "category_text"
GHA_ACCOUNT_CONTAINER_ID = "og_trailing_drawable_container"
GHA_ACCOUNT_INFORMATION_ID = "og_secondary_account_information"
GHA_CONTAINER_BOTTOM_ID = "og_container_footer"
GHA_BOTTOM_CONTAINER_ID= "bottom_container"
GHA_HALF_SPLIT_RECYCLER_VIEW="half_split_recycler_view"
GHA_DEVICE_TAB_DEVICE_NAME_ID = "com.google.android.apps.chromecast.app:id/title"
GHA_DEVICE_TAB_MAIN_VIEW_ID = "com.google.android.apps.chromecast.app:id/main_navigation_pager"
GHA_PIN_EDIT_TEXT_ID = "com.google.android.apps.chromecast.app:id/pin_edit_text"
GHA_SAVE_PIN_CODE_CHECKBOX_ID = "com.google.android.apps.chromecast.app:id/alpha_numeric_checkbox"
GHA_LOCKED_UNLOCKED_BUTTON_ID = r"com\.google\.android\.apps\.chromecast\.app:id/hero_.*"



# ANDROID
ANDROID_SETTINGS_PACKAGE = "com.android.settings"
ANDROID_WIFI_SETTINGS_PACKAGE = "android.settings.WIFI_SETTINGS"
ANDROID_INTENT = "android"
ANDROID_SYSTEM_UI_PACKAGE = "com.android.systemui"
ANDROID_INTERNET_SSID_ID = "recycler_view"
ANDROID_INTENT_VIEW_ACTIVITY = "android.intent.action.VIEW"
ANDROID_NAVIGATION_BAR_FRAME = "navigation_bar_frame"
ANDROID_NAVIGATION_BAR_BACKGROUND = "navigationBarBackground"

# TUYA
TUYA_PACKAGE = "com.tuya.smart"
TUYA_TOOL_BAR_TOP_VIEW_ID = "com.tuya.smart:id/toolbar_top_view"
TUYA_SCAN_BUTTON_ID = "com.tuya.smart:id/iv_scan"
TUYA_CONNECT_BUTTON_ID = "com.tuya.smart:id/btn_connect"
TUYA_GOOGLE_ACCOUNT_VIEW_LIST_ID = "com.google.android.gms:id/list"
TUYA_GOOGLE_ACCOUNT_NAME_ID = "com.google.android.gms:id/account_name"
TUYA_DEVICE_LIST_LINK_PAGE_ID = "com.tuya.smart:id/recyclerView"
TUYA_HOME_ITEM_VIEW_ID = "mat-select-0-panel"
TUYA_GHP_VIEW_ALLOW_BUTTON_ID = "allow-button"
TUYA_GHP_VIEW_CANCEL_BUTTON_ID = "cancel-button"
TUYA_HOME_ITEM_ID = "mat-select-0"
TUYA_DEVICE_LIST_NAME_ID = "com.tuya.smart:id/tv_name"
TUYA_PAIRING_CODE_EDIT_TEXT_ID = "com.tuya.smart:id/et_input"
TUYA_PAIRING_CODE_VIEW_NEXT_BUTTON_ID = "com.tuya.smart:id/btn_next"
TUYA_SSID_EDIT_TEXT_ID = "com.tuya.smart:id/etSSID"
TUYA_CHANGE_SSID_BUTTON_ID = "com.tuya.smart:id/tvChange"
TUYA_WIFI_PWD_EDIT_TEXT_ID = "com.tuya.smart:id/etPassword"
TUYA_ENTER_WIFI_VIEW_NEXT_BUTTON_ID = "com.tuya.smart:id/ll_btn"
TUYA_ENTER_WIFI_VIEW_TITLE_ID = "com.tuya.smart:id/tvWifiTitle"
TUYA_CONNECTING_STATUS_ID = "com.tuya.smart:id/tvSearchContent"
TUYA_TRY_CONNECT_ERROR_TITLE = "com.tuya.smart:id/errorTitleTv"
TUYA_TRY_CONNECT_AGAIN_BUTTON = "com.tuya.smart:id/activeAgainTv"
TUYA_CONNECT_SUCCESS_TITLE_ID = "com.tuya.smart:id/titleView"
TUYA_CONNECT_SUCCESS_ADD_BUTTON_ID = "com.tuya.smart:id/positiveButton"
TUYA_ADD_DEVICE_VIEW_EDIT_BUTTON_ID ="com.tuya.smart:id/deviceStateView"
TUYA_ADD_DEVICE_VIEW_EDIT_VIEW_ID = "com.tuya.smart:id/devieNameEt"
TUYA_ADD_DEVICE_VIEW_EDIT_CLEAR_BUTTON = "com.tuya.smart:id/img_text_clear"
TUYA_ADD_DEVICE_VIEW_DONE_BUTTON_ID = "com.tuya.smart:id/btnDone"
TUYA_HOME_TAB_DEVICES_NAME = "com.tuya.smart:id/deviceName"
TUYA_DEVICE_DETAIL_VIEW_CONTAINER_ID = "com.tuya.smart:id/miniapp_container"
TUYA_DEVICE_DETAIL_VIEW_PAGE_ID = "pages/Home/index"
TUYA_MANAGE_BUTTON_ID = "com.tuya.smart:id/tvManage"
TUYA_REMOVE_DEVICE_BUTTON_ID = "com.tuya.smart:id/tvRemoveDevices"
TUYA_CONFIRM_BUTTON_ID = "com.tuya.smart:id/tv_confirm"
TUYA_DONE_BUTTON_ON_ALL_DEVICE_ID = "com.tuya.smart:id/tv_left_cancel"
TUYA_OK_BUTTON_ON_PIN_EDIT_ID = "android:id/button1"
TUYA_HOME_DEVICE_ITEM_CARD_ID = "com.tuya.smart:id/shell_item_card"
TUYA_HOME_CONTENT_ROOT_ID = "com.tuya.smart:id/content_root"

TUYA_ADD_BUTTON_INDEX = "2"
TUYA_HOME_DEVICES_LIST_LAST_INDEX = "8"
TUYA_DEVICE_DETAIL_SWITCH_INDEX = "3"

TUYA_ADD_DEVICE_BUTTON_CLASS_AND_TEXT = "//android.widget.TextView[@text='Add Device']"
TUYA_EDIT_DEVICE_NAME_DON_BUTTON_CLASS_AND_TEXT = "//android.widget.Button[@text='Done']"
TUYA_ME_TAB_CLASS_AND_TEXT = "//android.widget.TextView[@text='Me']"
TUYA_HOME_TAB_CLASS_AND_TEXT = "//android.widget.TextView[@text='Home']"
TUYA_GOOGLE_HOME_DEVICES_CLASS_AND_TEXT = "//android.widget.TextView[@text='Google Home Devices']"
TUYA_ALL_DEVICE_HOME_PAGE_CLASS_AND_TEXT = "//android.widget.TextView[@text='All Devices']"

TUYA_DEVICE_DETAIL_VIEW_NEXT_CLASS = "android.view.View"
TUYA_HOME_ITEM_CLASS = "android.view.View"
TUYA_HOME_DEVICES_LIST_ITEM_CLASS = 'android.widget.RelativeLayout'
TUYA_ADD_DEVICE_NAME_EDIT_VIEW_CLASS = "//android.widget.EditText"

TUYA_ENTER_SETUP_CODE_TEXT = "Enter Setup Code"

# Aqara Home App
AQARA_PACKAGE_NAME = "com.lumiunited.aqarahome.play"
RESOURCE_ID_LOADING = "com.lumiunited.aqarahome.play:id/sv_loading"
RESOURCE_ID_TOOLBAR_TITLE = "com.lumiunited.aqarahome.play:id/public_toolbar_title"
RESOURCE_ID_ADD_BUTTON_EXISIT_AUTOMATION = "com.lumiunited.aqarahome.play:id/public_toolbar_right_img"
RESOURCE_ID_ADD_BUTTON_NOT_EXISIT_AUTOMATION = "com.lumiunited.aqarahome.play:id/btn_empty"
RESOURCE_ID_CELL_LEFT = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_INPUT_CONTROL = "com.lumiunited.aqarahome.play:id/et_input_control"
RESOURCE_ID_NAME_CONFIRM = "com.lumiunited.aqarahome.play:id/tv_name_confirm"
RESOURCE_ID_DELETE_SLIDE_ITEM = "com.lumiunited.aqarahome.play:id/delete_slide_item"
RESOURCE_ID_DIALOG_RIGHT = "com.lumiunited.aqarahome.play:id/tv_dialog_right"
RESOURCE_ID_PROFILE_BUTTON = "com.lumiunited.aqarahome.play:id/btn_mine"
RESOURCE_ID_GOOGLE_HOME_AUTOMATIONS = "com.lumiunited.aqarahome.play:id/tv_mine_item_title"
RESOURCE_ID_AQARA_GHP_SWITCH_GOOGLE_HOME_ACCOUNT = "com.lumiunited.aqarahome.play:id/tv_content"
RESOURCE_ID_AQARA_BIND_GOOGLE_BUTTON = "com.lumiunited.aqarahome.play:id/btn_bind_google"
RESOURCE_ID_FAMILY_STRUCTURE = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_AUTOMATION_TITLE_BAR = "com.lumiunited.aqarahome.play:id/public_toolbar_title"
RESOURCE_ID_ALL_AUTOMATION = "com.lumiunited.aqarahome.play:id/container"
AQARA_CHOOSE_FAMILY_TITLE_BAR_TEXT = "Choose Family"
AQARA_AUTOMATION_TITLE_BAR_TEXT = "Automation"
AQARA_CREATE_AUTOMATION_TITLE_BAR_TEXT = "Create Automation"
RESOURCE_ID_AUTOMATION_ITEM = "com.lumiunited.aqarahome.play:id/layout_cell_item"
RESOURCE_ID_GOOGLE_HOME_AUTOMATIONS_TEXT = "Google Home Automations"
RESOURCE_ID_CREATE_AUTOMATION_CONTENT = "com.lumiunited.aqarahome.play:id/rv_automation_content"
RESOURCE_ID_AUTOMATION_IF_DEVICE = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_AUTOMATION_THEN_DEVICE = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_DEVICE_STATUS_BUTTON = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_DIALOG_CLOSE_BUTTON = "com.lumiunited.aqarahome.play:id/tv_cancel"
RESOURCE_ID_STARTER_DEVICE_ITEM = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_STARTER_DEVICE_SET_STATUS = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_ACTION_DEVICE_ITEM = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_ACTION_DEVICE_SET_STATUS = "com.lumiunited.aqarahome.play:id/tv_cell_left"
RESOURCE_ID_CREATE_AUTOMATION_SAVE = "com.lumiunited.aqarahome.play:id/public_toolbar_right"
RESOURCE_ID_CREATE_AUTOMATION_SAVE_TEXT = "Save"
RESOURCE_ID_AUTOMATION_DESCRIPTION_EDIT_TEXT = "com.lumiunited.aqarahome.play:id/et_input_control"
RESOURCE_ID_AUTOMATION_OK_BUTTON = "com.lumiunited.aqarahome.play:id/tv_name_confirm"
RESOURCE_ID_AUTOMATION_CANCEL_BUTTON = "com.lumiunited.aqarahome.play:id/tv_name_cancel"
RESOURCE_ID_AUTOMATION_EXIST_AUTOMATION = "com.lumiunited.aqarahome.play:id/tv_cell_left"

# GMS
RESOURCE_ID_GMS_ACCOUNT = "com.google.android.gms:id/account_name"
RESOURCE_ID_GMS_ACCOUNT_LIST_READY_BAR = "com.google.android.gms:id/action_bar_root"
RESOURCE_ID_GMS_ACCOUNT_LIST_PICKER = "com.google.android.gms:id/account_picker_container"
RESOURCE_ID_GHP_ALLOW_LINK_BUTTON = "allow-button"
RESOURCE_ID_GHP_CANCEL_LINK_BUTTON = "cancel-button"
RESOURCE_ID_GMS_MAIN_TITLE = "com.google.android.gms:id/main_title"
RESOURCE_ID_GHP_DEVICES_LINKED_VIEW = "com.google.android.gms.optional_home:id/layout_container"
RESOURCE_CLASS_GMS_WEBKIT_CONTAINER = "android.webkit.WebView"
RESOURCE_CLASS_GO_BACK_BUTTON = "android.widget.Button"
RESOURCE_CLASS_GO_BACK_BUTTON_DESCRIPTION = "Go back"

# Android Sample App
AGHP_PACKAGE = "com.example.googlehomeapisampleapp"

AGHP_HOME_ITEM_ID = "mat-select-0"

GHP_UNVERIFIED_VIEW_TEXT = "This app isn't verified"

UNVERIFIED_VIEW_UNDERSTAND_BUTTON_CLASS_AND_TEXT = "//android.widget.Button[@text='I understand']"
AGHP_DEVICE_VIEW_CLASS_AND_TEXT = "//android.widget.TextView[@text='Home ▾']"
AGHP_GHP_SESSION_TITLE_BUTTON_CLASS_AND_TEXT = "//android.widget.TextView[@text='Google Home API Sample App']"

# UIAUTOMATOR
DIRECTION_UP = "up"
DIRECTION_DOWN = "down"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
KEY_BACK = "back"
ELEM_GET_TEXT = "text"
ELEM_GET_INDEX = "index"

# ADB
ADB_TCPIP_PORT = "5555"
LOG_PATH = './log/'

# time
ONE_SECONDS = 1
TWO_SECONDS = 2
THREE_SECONDS = 3
FIVE_SECONDS = 5
TEN_SECONDS = 10
FIFTEEN_SECONDS = 15
THIRTY_SECONDS = 30
SIXTY_SECONDS = 60
THREE_MINUTES = 180
FIVE_MINUTES = 5 * 60
TIMESTAMP = time.strftime("%Y%m%d-%H%M%S")

class DeviceState(enum.Enum):
    OFFLINE = 0
    OFF = 1
    ON = 2
    UNKNOWN = 3
    LOCKED = 4
    UNLOCKED = 5

def device_status_parse(device_status: str) -> DeviceState:
    """Parse device status from string to enum.

    Args:
        device_status: Device status string.

    Returns:
        DeviceState: Device status enum.
    """
    try:
        return DeviceState[device_status.upper()]
    except KeyError:
        return DeviceState.UNKNOWN


def device_status_format(device_status: DeviceState) -> str:
    """Parse device status from enum to string.

    Args:
        device_status: Device status enum.

    Returns:
        str: Device status string.
    """
    try:
        return device_status.name.lower()
    except ValueError:
        return "unknown"