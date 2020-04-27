class LoginError(Exception):
    def __init__(self, status_code):
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code
