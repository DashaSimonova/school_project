import requests

from error_message import ErrorMessage

API_URL = 'http://127.0.0.1:8000/school'


class Api:
    def __init__(self, username, password):
        self.auth = (username, password)

    def request(self, url, error_message, method='post', **kwargs):
        try:
            r = requests.request(method, API_URL + url, auth=self.auth, timeout=5, **kwargs)
            if r.status_code != 200:
                raise ValueError()
            return r.json()
        except (ValueError, requests.exceptions.RequestException):
            ErrorMessage.show(error_message)
            return None

    def authorize(self):
        return self.request('/', 'Ошибка авторизации', 'get')

    def create_application(self, child_id, time):
        r = requests.post(API_URL + '/create-application/', auth=self.auth, data={'id':child_id, 'time':time})
        if r.status_code != 200:
            raise ValueError()
        return r.json()

    def set_application_status(self, child_id, status):
        return self.request(
            '/set-application-status/',
            'Не удалось изменить статус заявки',
            data={'child_id': child_id, 'status': status}
        )
