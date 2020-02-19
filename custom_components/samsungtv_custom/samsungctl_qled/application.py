import os
import json
import requests

APP_URL_FORMAT = "http://{}:8001/api/v2/applications/{}"

APPS = {'YouTube': '111299001912',
        'Plex': '3201512006963',
        'Prime Video': '3201512006785',
        'Universal Guide': '3201710015067',
        'Netflix': '11101200001',
        'Apple TV': '3201807016597',
        'Steam Link': '3201702011851',
        'MyCANAL': '3201606009910',
        # 'Browser': 'org.tizen.browser',
        'Spotify': '3201606009684',
        'Molotov': '3201611011210',
        'SmartThings': '3201710015016',
        'e-Manual': '20182100010',
        'Google Play': '3201601007250',
        'Gallery': '3201710015037',
        'Rakuten TV': '3201511006428',
        'RMC Sport': '3201704012212',
        'MYTF1 VOD': '3201905018355',
        'Blacknut': '3201811017333',
        'Facebook Watch': '11091000000',
        'McAfee Security for TV': '3201612011418',
        'OCS': '3201703012029',
        'Playzer': '3201810017091'
        }


class Application:
    """ Handle applications."""
    def __init__(self, config):
        self._ip = config['host']
    
    def state(self, app):
        """ Get the state of the app."""
        try:
            response = requests.get(APP_URL_FORMAT.format(self._ip, APPS[app]), timeout=0.2)
            return response.content.decode('utf-8')
        except:
            return """{"id":"","name":"","running":false,"version":"","visible":false}"""

    def is_running(self, app):
        """ Is the app running."""
        app_state = json.loads(self.state(app))
        return app_state['running']

    def is_visible(self, app):
        """ Is the app visible."""
        app_state = json.loads(self.state(app))

        if 'visible' in app_state:
            return app_state['visible']

        return False
    
    def start(self, app):
        """ Start an application."""
        return os.system("curl -X POST " + APP_URL_FORMAT.format(self._ip, APPS[app]))
    
    def stop(self, app):
        """ Stop an application."""
        return os.system("curl -X DELETE " + APP_URL_FORMAT.format(self._ip, APPS[app]))

    def current_app(self):
        """ Get the current visible app."""
        current_app = None
        for app in APPS:
            if (self.is_visible(app) is True):
                current_app = app
        return current_app

    def app_list(self):
        """ List running apps."""
        apps = []
        for app in APPS:
            if (self.is_running(app) is True):
                apps.append(app)
        return apps