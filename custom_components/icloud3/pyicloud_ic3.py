"""
Customized version of pyicloud.py to support iCloud3 Custom Component

Platform that supports importing data from the iCloud Location Services
and Find My Friends api routines. Modifications to pyicloud were made
by various people to include:
    - Original pyicloud - picklepete & Quantame
                        - https://github.com/picklepete

    - Updated and maintained by - Quantame
    - 2fa developed by          - Niccolo Zapponi (nzapponi)
    - Find My Friends component - Z Zeleznick

The picklepete version used imports for the services, utilities and exceptions
modules. They are now maintained by Quantame and have been modified by
Niccolo Zapponi Z Zeleznick.
These modules and updates have been incorporated into the pyicloud_ic3.py version
used by iCloud3.
"""

VERSION = '2.4.4'
"""
v2.4.4 (9/25/2021)
1. Changes the Apple iCloud url end point for Find-my-Friends from 'fmf' to 'findme' to support iCloud+ changes.
"""

from six import PY2, string_types, text_type
from uuid import uuid1
import inspect
import json
import logging
from requests import Session
from tempfile import gettempdir
from os import path, mkdir
from re import match
import http.cookiejar as cookielib
import homeassistant.util.dt as dt_util

LOGGER = logging.getLogger(__name__)

HEADER_DATA = {
    "X-Apple-ID-Account-Country": "account_country",
    "X-Apple-ID-Session-Id": "session_id",
    "X-Apple-Session-Token": "session_token",
    "X-Apple-TwoSV-Trust-Token": "trust_token",
    "scnt": "scnt",
}
AUTHENTICATION_REQUIRED_450 = 450
DEVICE_STATUS_ERROR_500 = 500
INVALID_GLOBAL_SESSION_421 = 421
APPLE_ID_VERIFICATION_CODE_INVALID_404 = 404
AUTHENTICATION_REQUIRED_CODES = [421, 450, 500]
'''
https://developer.apple.com/library/archive/documentation/DataManagement/Conceptual/CloudKitWebServicesReference/ErrorCodes.html#//apple_ref/doc/uid/TP40015240-CH4-SW1

#Other Device Status Codes
SEND_MESSAGE_MSG_DISPLAYED = 200
REMOTE_WIPE_STARTED = 200
REMOVE_DEVICE_SUCCESS = 200
UPDATE_LOCATION_PREF_SUCCESS = 200
LOST_MODE_SUCCESS = 200
PLAY_SOUND_SUCCESS = 200
PLAY_SOUND_NEEDS_SAFETY_CONFIRM = 203
SEND_MESSAGE_MSG_SENT = 205
REMOTE_WIPE_SENT = 205
LOST_MODE_SENT = 205
LOCK_SENT = 205
PLAY_SOUND_SENT = 205
LOCK_SERVICE_FAILURE = 500
SEND_MESSAGE_FAILURE = 500
PLAY_SOUND_FAILURE = 500
REMOTE_WIPE_FAILURE = 500
UPDATE_LOCATION_PREF_FAILURE = 500
LOCK_SUCC_PASSCODE_SET = 2200
LOCK_SUCC_PASSCODE_NOT_SET_PASSCD_EXISTS = 2201
LOCK_SUCCESSFUL_2 = 2204
LOCK_FAIL_PASSCODE_NOT_SET_CONS_FAIL = 2403
LOCK_FAIL_NO_PASSCD_2 = 2406
'''

#================================================================================
class PyiCloudPasswordFilter(logging.Filter):
    """Password log hider."""

    def __init__(self, password):
        super(PyiCloudPasswordFilter, self).__init__(password)

    def filter(self, record):
        message = record.getMessage()
        if self.name in message:
            record.msg = message.replace(self.name, "*" * 8)
            record.args = []

        return True

#================================================================================
class PyiCloudSession(Session):
    """iCloud session."""

    def __init__(self, service):
        self.service = service
        Session.__init__(self)

    def request(self, method, url, **kwargs):  # pylint: disable=arguments-differ

        # Charge logging to the right service endpoint
        callee = inspect.stack()[2]
        module = inspect.getmodule(callee[0])
        request_logger = logging.getLogger(module.__name__).getChild("http")

        if self.service.password_filter not in request_logger.filters:
            request_logger.addFilter(self.service.password_filter)

        request_logger.debug(f"REQUEST -- {dt_util.now().strftime('%X')}, {method}, {url}, {kwargs.get('data', '')}")

        has_retried = kwargs.get("retried", False)
        kwargs.pop("retried", False)

        response = super(PyiCloudSession, self).request(method, url, **kwargs)

        request_logger.debug(f"RESPONSE -- {response}, StatusCode-{response.status_code}, okStatus-{response.ok}, hasRetried-{has_retried}")

        content_type = response.headers.get("Content-Type", "").split(";")[0]
        json_mimetypes = ["application/json", "text/json"]

        try:
            data = response.json()
        except:
            data = None
        if (response.status_code != 200 or not response.ok):#or True==True:
            self._log_debug_msg("RESPONSE CONTENT_TYPE", content_type)
            self._log_debug_msg("RESPONSE INVALID CONTENT TYPE", (content_type not in json_mimetypes))
            #self._log_debug_msg("RESPONSE DATA", data)
            self._log_debug_msg("RESPONSE HEADERS", response.headers)
        self._log_debug_msg("RESPONSE DATA", data)

        for header in HEADER_DATA:
            if response.headers.get(header):
                session_arg = HEADER_DATA[header]
                self.service.session_data.update(
                    {session_arg: response.headers.get(header)})

        # Save session_data to file
        with open(self.service.session_path, "w") as outfile:
            json.dump(self.service.session_data, outfile)
            LOGGER.debug(f"Session saved to {self.service.session_path}")

        # Save cookies to file
        self.cookies.save(ignore_discard=True, ignore_expires=True)
        LOGGER.debug(f"Cookies saved to {self.service.cookiejar_path}")

        if (not response.ok and (content_type not in json_mimetypes
                or response.status_code in [421, 450, 500])):

            #if (has_retried == False and response.status_code in [421, 450, 500]):
            try:
                fmip_url = self.service._get_webservice_url("findme")
                if has_retried == False and response.status_code == 450 and fmip_url in url:
                    # Handle re-authentication for Find My iPhone
                    LOGGER.debug("Re-authenticating Find My iPhone service")
                    try:
                        self.service.authenticate(True, "find")
                    except PyiCloudAPIResponseException:
                        LOGGER.debug("Re-authentication failed")
                    kwargs["retried"] = True
                    return self.request(method, url, **kwargs)
            except Exception:
                pass

            if has_retried == False and response.status_code in [421, 450, 500]:
                self._log_debug_msg("AUTHENTICTION NEEDED, Status Code", response.status_code)

                #api_error = PyiCloudAPIResponseException(
                #               response.reason, response.status_code, retry=True)
                #request_logger.debug(api_error)
                kwargs["retried"] = True
                return self.request(method, url, **kwargs)

            self._raise_error(response.status_code, response.reason)

        if content_type not in json_mimetypes:
            return response

        try:
            data = response.json()
        except:  # pylint: disable=bare-except
            if not response.ok:
                msg = (f"Error handling data returned from iCloud, {response}")
                request_logger.warning(msg)
            return response

        if isinstance(data, dict):
            reason = data.get("errorMessage")
            reason = reason or data.get("reason")
            reason = reason or data.get("errorReason")
            if not reason and isinstance(data.get("error"), string_types):
                reason = data.get("error")
            if not reason and data.get("error"):
                reason = "Unknown reason, will continue"

            code = data.get("errorCode")
            code = code or data.get("serverErrorCode")
            if reason:
                self._raise_error(code, reason)

        return response

    def _raise_error(self, code, reason):
        info_msg = False
        api_error = None
        if code in ("ZONE_NOT_FOUND", "AUTHENTICATION_FAILED"):
            reason = ("Please log into https://icloud.com/ to manually "
                "finish setting up your iCloud service")
            api_error = PyiCloudServiceNotActivatedException(reason, code)

        if (self.service.requires_2sa
                and reason == "Missing X-APPLE-WEBAUTH-TOKEN cookie"):
            code = 450

        if code in [204, 421, 450, 500]:
            reason = "Authentication needed for Account"
            info_msg = True

        elif code in [400, 404]:
            reason = "Apple ID Validation Code Invalid"

        elif code == "ACCESS_DENIED":
            reason = (reason + ".  Please wait a few minutes then try again."
                "The remote servers might be trying to throttle requests.")

        if not api_error:
            api_error = PyiCloudAPIResponseException(reason, code)

        if info_msg:
            LOGGER.info(api_error)
        else:
            LOGGER.error(api_error)

        raise api_error

    def _log_debug_msg(self, title, display_data):
        """ Display debug data fields """
        try:
            LOGGER.debug(f"{title} -- {display_data}")
        except:
            LOGGER.debug(f"{title} -- None")


#================================================================================
class PyiCloudService(object):
    """
    A base authentication class for the iCloud service. Handles the
    authentication required to access iCloud services.

    Usage:
        from pyicloud import PyiCloudService
        pyicloud = PyiCloudService('username@apple.com', 'password')
        pyicloud.iphone.location()
    """

    AUTH_ENDPOINT = "https://idmsa.apple.com/appleauth/auth"
    HOME_ENDPOINT = "https://www.icloud.com"
    SETUP_ENDPOINT = "https://setup.icloud.com/setup/ws/1"

    def __init__(
        self,
        apple_id,
        password=None,
        cookie_directory=None,
        session_directory=None,
        verify=True,
        client_id=None,
        with_family=True,
    ):

        self.user = {"accountName": apple_id, "password": password}
        self.apple_id = apple_id
        self.data = {}
        #self.params = {}
        self.client_id = client_id or f"auth-{str(uuid1()).lower()}"
        self.params = {
            "clientBuildNumber": "2021Project52",
            "clientMasteringNumber": "2021B29",
            "ckjsBuildVersion": "17DProjectDev77",
            "clientId": self.client_id[5:],  ## remove auth - not used here just raw client ID
            }
        self.with_family = with_family
        self.session_data = {}
        if session_directory:
            self._session_directory = session_directory
        else:
            self._session_directory = path.join(gettempdir(), "pyicloud-session")

        try:
            with open(self.session_path) as session_f:
                self.session_data = json.load(session_f)
        except:  # pylint: disable=bare-except
            LOGGER.info("Session file does not exist")

        if not path.exists(self._session_directory):
            mkdir(self._session_directory)

        self.password_filter = PyiCloudPasswordFilter(password)
        LOGGER.addFilter(self.password_filter)

        if cookie_directory:
            self._cookie_directory = path.expanduser(path.normpath(cookie_directory))
        else:
            self._cookie_directory = path.join(gettempdir(), "pyicloud")

        if not path.exists(self._cookie_directory):
            mkdir(self._cookie_directory)

        if self.session_data.get("client_id"):
            self.client_id = self.session_data.get("client_id")
        else:
            self.session_data.update({"client_id": self.client_id})

        self.session = PyiCloudSession(self)

        self.session.verify = verify
            #"Referer": f"{self.HOME_ENDPOINT}/",
        self.session.headers.update(
            {"Origin": self.HOME_ENDPOINT,
            "Referer": self.HOME_ENDPOINT,})
            #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Safari/604.1.25",})

        cookiejar_path = self.cookiejar_path
        self.session.cookies = cookielib.LWPCookieJar(filename=cookiejar_path)
        if path.exists(cookiejar_path):
            try:
                self.session.cookies.load(ignore_discard=True, ignore_expires=True)
                LOGGER.debug(f"Read Cookies from {cookiejar_path}")
            except:  # pylint: disable=bare-except
                # Most likely a pickled cookiejar from earlier versions.
                # The cookiejar will get replaced with a valid one after
                # successful authentication.
                LOGGER.warning(f"Failed to read cookie file {cookiejar_path}")

        self.authenticate_method = ""
        self.authenticate()

#----------------------------------------------------------------------------
    def authenticate(self, refresh_session=False, service=None):
        """
        Handles authentication, and persists cookies so that
        subsequent logins will not cause additional e-mails from Apple.
        """

        login_successful = False

        #if (not refresh_session and self.session_data.get("session_token")):
        # Validate token - Consider authenticated if token is valid (POST=validate)
        if (not refresh_session
                and self.session_data.get("session_token")
                and 'dsid' in self.params):
            LOGGER.info("Checking session token validity")

            try:
                self.data = self._validate_token()
                login_successful = True
                self.authenticate_method += ", ValidateToken"

            except PyiCloudAPIResponseException:
                msg = "Invalid authentication token, will log in from scratch."

        # Authenticate with Service
        if not login_successful and service != None:
            app = self.data["apps"][service]
            if "canLaunchWithOneFactor" in app and app["canLaunchWithOneFactor"] == True:
                LOGGER.debug("Authenticating as %s for %s" % (self.user["accountName"], service))
                try:
                    self._authenticate_with_credentials_service(service)
                    login_successful = True
                    self.authenticate_method += (f", TrustToken/ServiceLogin")
                except:
                    LOGGER.debug("Could not log into service. Attempting brand new login.")

        # Authenticate - Sign into icloud account (POST=/signin)
        if not login_successful:
            LOGGER.info(f"Authenticating account {self.user['accountName']} using Account/PasswordSignin")

            data = dict(self.user)
            data["rememberMe"] = True
            data["trustTokens"] = []
            if self.session_data.get("trust_token"):
                data["trustTokens"] = [self.session_data.get("trust_token")]

            headers = self._get_auth_headers()

            if self.session_data.get("scnt"):
                headers["scnt"] = self.session_data.get("scnt")

            if self.session_data.get("session_id"):
                headers["X-Apple-ID-Session-Id"] = self.session_data.get("session_id")

            try:
                req = self.session.post(
                    f"{self.AUTH_ENDPOINT}/signin",
                    params={"isRememberMeEnabled": "true"},
                    data=json.dumps(data),
                    headers=headers,)
                self.authenticate_method = ", Account/PasswordSignin"

            except PyiCloudAPIResponseException as error:
                msg = "Invalid email/password combination."
                raise PyiCloudFailedLoginException(msg, error)

            self._authenticate_with_token()

        self._webservices = self.data["webservices"]

        self.authenticate_method = self.authenticate_method[2:]
        LOGGER.info(f"Authentication completed successfully, method-{self.authenticate_method}")

#----------------------------------------------------------------------------
    def _authenticate_with_token(self):
        """Authenticate using session token. Return True if successful."""
        data = {
            "accountCountryCode": self.session_data.get("account_country"),
            "dsWebAuthToken": self.session_data.get("session_token"),
            "extended_login": True,
            "trustToken": self.session_data.get("trust_token", ""),}

        try:
            req = self.session.post(f"{self.SETUP_ENDPOINT}/accountLogin"
                                            f"?clientBuildNumber=2021Project52&clientMasteringNumber=2021B29"
                                            f"&clientId={self.client_id[5:]}",
                                        data=json.dumps(data))
            data = req.json()

        except PyiCloudAPIResponseException as error:
            msg = "Invalid authentication token."
            raise PyiCloudFailedLoginException(msg, error)

        self.data = req.json()
        self._update_dsid(self.data)

        return True

#----------------------------------------------------------------------------
    def _authenticate_with_credentials_service(self, service):
        """Authenticate to a specific service using credentials."""
        data = {
            "appName": service,
            "apple_id": self.user["accountName"],
            "password": self.user["password"],
            "accountCountryCode": self.session_data.get("account_country"),
            "dsWebAuthToken": self.session_data.get("session_token"),
            "extended_login": True,
            "trustToken": self.session_data.get("trust_token", ""),
        }

        try:
            #req = self.session.post(f"{self.SETUP_ENDPOINT}/accountLogin"
            self.session.post(f"{self.SETUP_ENDPOINT}/accountLogin"
                        f"?clientBuildNumber=2021Project52&clientMasteringNumber=2021B29"
                        f"&clientId={self.client_id[5:]}",
                        data=json.dumps(data))
            #self.data = req.json()
            self.data = self._validate_token()
        except PyiCloudAPIResponseException as error:
            msg = "Invalid email/password combination."
            raise PyiCloudFailedLoginException(msg, error)

#----------------------------------------------------------------------------
    def _validate_token(self):
        """Checks if the current access token is still valid."""
        LOGGER.debug("Checking session token validity")
        try:
            req = self.session.post("%s/validate" % self.SETUP_ENDPOINT, data="null")
            LOGGER.debug("Session token is still valid")
            return req.json()
        except PyiCloudAPIResponseException as err:
            LOGGER.debug("Invalid authentication token")
            raise err

#----------------------------------------------------------------------------
    def _update_dsid(self, data):
        try:
            if 'dsInfo' in data:  ## check self.data returned and contains dsid
                if 'dsid' in data['dsInfo']:        # as above
                    self.params["dsid"]= str(data["dsInfo"]["dsid"])
            else:
                if 'dsid' in self.params:
                    self.params.pop("dsid")  ## if no dsid given delete it from self.params - until returned.  Otherwise is passing default incorrect dsid
        except:
            LOGGER.debug(u"Error setting dsid field.")
            if 'dsid' in self.params:
                self.params.pop("dsid")  ## if error, self.data None/empty delete
        return

#----------------------------------------------------------------------------
    def _get_auth_headers(self, overrides=None):
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "X-Apple-OAuth-Client-Id": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
            "X-Apple-OAuth-Client-Type": "firstPartyAuth",
            "X-Apple-OAuth-Redirect-URI": "https://www.icloud.com",
            "X-Apple-OAuth-Require-Grant-Code": "true",
            "X-Apple-OAuth-Response-Mode": "web_message",
            "X-Apple-OAuth-Response-Type": "code",
            "X-Apple-OAuth-State": self.client_id,
            "X-Apple-Widget-Key": "d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d",
        }
            #"X-Apple-OAuth-State": "auth-" + self.client_id,

        if overrides:
            headers.update(overrides)
        return headers

#----------------------------------------------------------------------------
    @property
    def cookiejar_path(self):
        """Get path for cookiejar file."""
        return path.join(
            self._cookie_directory,
            "".join([c for c in self.user.get("accountName") if match(r"\w", c)]),)

    @property
    def session_path(self):
        """Get path for session data file."""
        return path.join(
            self._session_directory,
            "".join([c for c in self.user.get("accountName") if match(r"\w", c)]),)

    @property
    def authentication_method(self):
        """
        Returns the type of authentication method performed
            - None = No authentication done
            - TrustToken = Authentication using trust token (/accountLogin)
            - ValidateToken = Trust token was validated (/validate)
            - AccountSignin = Signed into the account (/signin)
        """
        return self.authenticate_method

    @property
    def requires_2sa(self):
        """Returns True if two-step authentication is required."""
        return self.data.get("dsInfo", {}).get("hsaVersion", 0) >= 1 and (
            self.data.get("hsaChallengeRequired", False) or not self.is_trusted_session)

    @property
    def requires_2fa(self):
        """Returns True if two-factor authentication is required."""
        needs_2fa_flag = self.data["dsInfo"].get("hsaVersion", 0) == 2 and (
            self.data.get("hsaChallengeRequired", False) or not self.is_trusted_session)
        if needs_2fa_flag:
            LOGGER.debug(f"NEEDS-2FA, is_trusted_session-{self.is_trusted_session}, data-{self.data}")
        return needs_2fa_flag
    @property
    def is_trusted_session(self):
        """Returns True if the session is trusted."""
        return self.data.get("hsaTrustedBrowser", False)

    @property
    def trusted_devices(self):
        """Returns devices trusted for two-step authentication."""
        request = self.session.get(
            "%s/listDevices" % self.SETUP_ENDPOINT, params=self.params)
        return request.json().get("devices")

#----------------------------------------------------------------------------
    def send_verification_code(self, device):
        """Requests that a verification code is sent to the given device."""
        data = json.dumps(device)
        request = self.session.post(
            "%s/sendVerificationCode" % self.SETUP_ENDPOINT,
            params=self.params,
            data=data,)
        return request.json().get("success", False)

#----------------------------------------------------------------------------
    def validate_verification_code(self, device, code):
        """Verifies a verification code received on a trusted device."""
        device.update({"verificationCode": code, "trustBrowser": True})
        data = json.dumps(device)

        try:
            self.session.post(
                "%s/validateVerificationCode" % self.SETUP_ENDPOINT,
                params=self.params,
                data=data,)
        except PyiCloudAPIResponseException as error:
            if error.code == -21669:
                # Wrong verification code
                return False
            raise

        # Re-authenticate, which will both update the HSA data, and
        # ensure that we save the X-APPLE-WEBAUTH-HSA-TRUST cookie.
        self.authenticate()

        return not self.requires_2sa

#----------------------------------------------------------------------------
    def validate_2fa_code(self, code):
        """Verifies a verification code received via Apple's 2FA system (HSA2)."""
        data = {"securityCode": {"code": code}}

        headers = self._get_auth_headers({"Accept": "application/json"})

        if self.session_data.get("scnt"):
            headers["scnt"] = self.session_data.get("scnt")

        if self.session_data.get("session_id"):
            headers["X-Apple-ID-Session-Id"] = self.session_data.get("session_id")

        try:
            self.session.post(
                f"{self.AUTH_ENDPOINT}/verify/trusteddevice/securitycode",
                data=json.dumps(data),
                headers=headers,)
        except PyiCloudAPIResponseException as error:
            if error.code == -21669:
                # Wrong verification code
                LOGGER.error("Code verification failed")
                return False
            raise

        LOGGER.debug("Code verification successful")

        self.trust_session()
        return not self.requires_2sa

#----------------------------------------------------------------------------
    def trust_session(self):
        """Request session trust to avoid user log in going forward."""
        headers = self._get_auth_headers()

        if self.session_data.get("scnt"):
            headers["scnt"] = self.session_data.get("scnt")

        if self.session_data.get("session_id"):
            headers["X-Apple-ID-Session-Id"] = self.session_data.get("session_id")

        try:
            self.session.get(
                f"{self.AUTH_ENDPOINT}/2sv/trust",
                headers=headers,)

            self._authenticate_with_token()
            return True
        except PyiCloudAPIResponseException:
            LOGGER.error("Session trust failed")
            return False

#----------------------------------------------------------------------------
    def _get_webservice_url(self, ws_key):
        """Get webservice URL, raise an exception if not exists."""
        if self._webservices.get(ws_key) is None:
            raise PyiCloudServiceNotActivatedException(
                "Webservice not available", ws_key)
        return self._webservices[ws_key]["url"]

#----------------------------------------------------------------------------
    @property
    def devices(self):
        """Returns all devices."""
        self.authenticate_method = ""
        service_root = self._get_webservice_url("findme")
        data = FindMyiPhoneServiceManager(service_root, self.session, self.params, self.with_family)
        return data

#----------------------------------------------------------------------------
    @property
    def friends(self):
        """Gets the 'Friends' service."""
        self.authenticate_method = ""
        service_root = self._get_webservice_url("findme")
        data = FindFriendsService(service_root, self.session, self.params)
        return data

#----------------------------------------------------------------------------
    def play_sound(self, device_id, subject="Find My iPhone Alert"):
        """
        Send a request to the device to play a sound.
        It's possible to pass a custom message by changing the `subject`.
        """
        self.authenticate_method = ""
        service_root = self._get_webservice_url("findme")
        data = FindMyiPhoneServiceManager(service_root, self.session, self.params, self.with_family,
                 task="PlaySound", device_id=device_id, subject=subject)
        return data

#----------------------------------------------------------------------------
    def __unicode__(self):
        return "iCloud API: %s" % self.user.get("accountName")

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s>" % str(self)



####################################################################################
#
#   Find my iPhone service
#
####################################################################################
class FindMyiPhoneServiceManager(object):
    """
    The 'Find my iPhone' iCloud service

    This connects to iCloud and return phone data including the near-realtime
    latitude and longitude.
    """

    def __init__(self, service_root, session, params, with_family=False, task="RefreshData",
                device_id=None, subject=None, message=None,
                sounds=False, number="", newpasscode=""):

        self.session = session
        self.params = params
        self.with_family = with_family
        self.task = task

        fmip_endpoint = f"{service_root}/fmipservice/client/web"
        self._fmip_refresh_url = f"{fmip_endpoint}/refreshClient"
        self._fmip_sound_url   = f"{fmip_endpoint}/playSound"
        self._fmip_message_url = f"{fmip_endpoint}/sendMessage"
        self._fmip_lost_url    = f"{fmip_endpoint}/lostDevice"

        fmiDict = {
			"clientContext": {
				"appName": "Home Assistant",
				"appVersion": "0.118",
				"inactiveTime": 1,
				"apiVersion": "2.2.2"
			}
        }
        if task == "PlaySound":
            if device_id:
                self.play_sound(device_id, subject)

        elif task == "Message":
            if device_id:
                self.display_message(device_id, subject, message)

        elif task == "LostDevice":
            if device_id:
                self.lost_device(device_id, number, message, newpasscode="")

        else:
            self._devices = {}
            self.refresh_client(device_id)

#----------------------------------------------------------------------------
    def refresh_client(self, device_id=None):
        """
        Refreshes the FindMyiPhoneService endpoint,
        This ensures that the location data is up-to-date.
        """
        self.session.authenticate_method = ""
        selected_device = device_id if device_id else "all"
        req = self.session.post(
            self._fmip_refresh_url,
            params=self.params,
            data=json.dumps(
                {
                    "clientContext": {
                        "fmly": self.with_family,
                        "shouldLocate": True,
                        "selectedDevice": selected_device,
                        "deviceListVersion": 1,
                    }
                }
            ),
        )
        try:
            self.response = req.json()
        except:
            self.response = {}
            LOGGER.debug("No data returned from fmi refresh request")

        for device_info in self.response["content"]:
            device_id = device_info["id"]
            if device_id not in self._devices:
                self._devices[device_id] = AppleDevice(
                    device_info,
                    self.session,
                    self.params,
                    manager=self,
                    sound_url=self._fmip_sound_url,
                    lost_url=self._fmip_lost_url,
                    message_url=self._fmip_message_url,)
            else:
                self._devices[device_id].update(device_info)

        if not self._devices:
            raise PyiCloudNoDevicesException()

    def _get_device(self, device_id):
        return self._devices.get(device_id)
#----------------------------------------------------------------------------
    def play_sound(self, device_id, subject):
        """
        Send a request to the device to play a sound.
        It's possible to pass a custom message by changing the `subject`.
        """
        if not subject:
            subject = "Find My iPhone Alert"

        data = json.dumps(
            {
                "device": device_id,
                "subject": subject,
                "clientContext": {"fmly": True},
            }
        )
        self.session.post(self._fmip_sound_url, params=self.params, data=data)
        return

#----------------------------------------------------------------------------
    def display_message(self, device_id, subject="Find My iPhone Alert",
                message="This is a note", sounds=False):
        """
        Send a request to the device to display a message.
        It's possible to pass a custom message by changing the `subject`.
        """
        data = json.dumps(
            {
                "device": device_id,
                "subject": subject,
                "sound": sounds,
                "userText": True,
                "text": message,
            }
        )
        self.session.post(self._fmip_message_url, params=self.params, data=data)
        return

#----------------------------------------------------------------------------
    def lost_device(self, number, message="This iPhone has been lost. Please call me.",
                newpasscode=""):
        """
        Send a request to the device to trigger 'lost mode'.

        The device will show the message in `text`, and if a number has
        been passed, then the person holding the device can call
        the number without entering the passcode.
        """
        data = json.dumps(
            {
                "text": message,
                "userText": True,
                "ownerNbr": number,
                "lostModeEnabled": True,
                "trackingEnabled": True,
                "device": device_id,
                "passcode": newpasscode,
            }
        )
        self.session.post(self._fmip_lost_url, params=self.params, data=data)
        return

#----------------------------------------------------------------------------
    def __getitem__(self, key):
        if isinstance(key, int):
            if PY2:
                key = self.keys()[key]
            else:
                key = list(self.keys())[key]
        return self._devices[key]

    def __getattr__(self, attr):
        return getattr(self._devices, attr)

    def __unicode__(self):
        return text_type(self._devices)

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return text_type(self)

####################################################################################
class AppleDevice(object):
    """Apple device."""

    def __init__(
        self,
        content,
        session,
        params,
        manager,
        sound_url=None,
        lost_url=None,
        message_url=None,
    ):
        self.content = content
        self.manager = manager
        self.session = session
        self.params = params

        self.sound_url = sound_url
        self.lost_url = lost_url
        self.message_url = message_url

    def update(self, data):
        """Updates the device data."""
        self.content = data

    def location(self):
        """Updates the device location."""
        self.manager.refresh_client()
        return self.content["location"]

    def status(self, additional=[]):  # pylint: disable=dangerous-default-value
        """Returns status information for device.

        This returns only a subset of possible properties.
        """
        self.manager.refresh_client()
        fields = ["batteryLevel", "deviceDisplayName", "deviceStatus", "name"]
        fields += additional
        properties = {}
        for field in fields:
            properties[field] = self.content.get(field)
        return properties

#----------------------------------------------------------------------------
    @property
    def data(self):
        """Gets the device data."""
        return self.content

    def __getitem__(self, key):
        return self.content[key]

    def __getattr__(self, attr):
        return getattr(self.content, attr)

    def __unicode__(self):
        display_name = self["deviceDisplayName"]
        name = self["name"]
        return f"{display_name}: {name}"

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return f"<AppleDevice({str(self)})>"



####################################################################################
#
#   Find my Friends service
#
####################################################################################
class FindFriendsService(object):
    """
    The 'Find My' (aka 'Find My Friends') iCloud service

    This connects to iCloud and returns friend's data including
    latitude and longitude.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._friend_endpoint = f"{self._service_root}/fmipservice/client/fmfWeb/initClient"
        self.refresh_always = False
        self.response = {}

#----------------------------------------------------------------------------
    def refresh_client(self):
        """
        Refreshes all data from 'Find My' endpoint,
        """
        params = dict(self.params)
        # This is a request payload we mock to fetch the data
        mock_payload = json.dumps(
            {
                "clientContext": {
                    "appVersion": "1.0",
                    "contextApp": "com.icloud.web.fmf",
                    "mapkitAvailable": True,
                    "productType": "fmfWeb",
                    "tileServer": "Apple",
                    "userInactivityTimeInMS": 537,
                    "windowInFocus": False,
                    "windowVisible": True,
                },
                "dataContext": None,
                "serverContext": None,
            }
        )
        self.session.authenticate_method = ""
        req = self.session.post(self._friend_endpoint, data=mock_payload, params=params)
        try:
            self.response = req.json()
        except:
            self.response = {}
            LOGGER.debug("No data returned on friends refresh request")

        return self.response

#----------------------------------------------------------------------------
    @staticmethod
    def should_refresh_client_fnc(response):
        """Function to override to set custom refresh behavior"""
        return not response

    def should_refresh_client(self):
        """
        Customizable logic to determine whether the data should be refreshed.

        By default, this returns False.

        Consumers can set `refresh_always` to True or assign their own function
        that takes a single-argument (the last reponse) and returns a boolean.
        """
        return self.refresh_always or FindFriendsService.should_refresh_client_fnc(
            self.response)

#----------------------------------------------------------------------------
    def contact_id_for(self, identifier, default=None):
        """
        Returns the contact id of your friend with a given identifier
        """
        lookup_key = "phones"
        if "@" in identifier:
            lookup_key = "emails"

        def matcher(item):
            """Returns True iff the identifier matches"""
            hit = item.get(lookup_key)
            if not isinstance(hit, list):
                return hit == identifier
            return any([el for el in hit if el == identifier])

        candidates = [
            item.get("id", default)
            for item in self.contact_details
            if matcher(item)]
        if not candidates:
            return default
        return candidates[0]

#----------------------------------------------------------------------------
    def location_of(self, contact_id, default=None):
        """
        Returns the location of your friend with a given contact_id
        """
        candidates = [
            item.get("location", default)
            for item in self.locations
            if item.get("id") == contact_id]
        if not candidates:
            return default
        return candidates[0]

#----------------------------------------------------------------------------
    @property
    def data(self):
        """
        Convenience property to return data from the 'Find My' endpoint.

        Call `refresh_client()` before property access for latest data.
        """
        if not self.response or self.should_refresh_client():
            self.refresh_client()
        return self.response

    @property
    def locations(self):
        """Returns a list of your friends' locations"""
        return self.data.get("locations", [])

    @property
    def followers(self):
        """Returns a list of friends who follow you"""
        return self.data.get("followers")

    @property
    def following(self):
        """Returns a list of friends who you follow"""
        return self.data.get("following")

    @property
    def contact_details(self):
        """Returns a list of your friends contact details"""
        return self.data.get("contactDetails")

    @property
    def my_prefs(self):
        """Returns a list of your own preferences details"""
        return self.data.get("myPrefs")


####################################################################################
#
#   Exceptions (exceptions.py)
#
####################################################################################
"""Library exceptions."""


class PyiCloudException(Exception):
    """Generic iCloud exception."""
    pass

#----------------------------------------------------------------------------
class PyiCloudAPIResponseException(PyiCloudException):
    """iCloud response exception."""
    def __init__(self, reason, code=None, retry=False):
        self.reason = reason
        self.code = code
        message = reason or ""
        if code:
            message += (f" (Status Code {code})")
        if retry:
            message += ". Retrying ..."

        super(PyiCloudAPIResponseException, self).__init__(message)

#----------------------------------------------------------------------------
class PyiCloudServiceNotActivatedException(PyiCloudAPIResponseException):
    """iCloud service not activated exception."""
    pass

#----------------------------------------------------------------------------
class PyiCloudFailedLoginException(PyiCloudException):
    """iCloud failed login exception."""
    pass

#----------------------------------------------------------------------------
class PyiCloud2SARequiredException(PyiCloudException):
    """iCloud 2SA required exception."""
    def __init__(self, apple_id):
        message = f"Two-Step Authentication (2SA) Required for Account {apple_id}"
        super(PyiCloud2SARequiredException, self).__init__(message)

#----------------------------------------------------------------------------
class PyiCloudNoStoredPasswordAvailableException(PyiCloudException):
    """iCloud no stored password exception."""
    pass

#----------------------------------------------------------------------------
class PyiCloudNoDevicesException(PyiCloudException):
    """iCloud no device exception."""
    pass
