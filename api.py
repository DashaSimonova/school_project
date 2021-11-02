import requests

API_URL = 'http://127.0.0.1:8000/school'


class Api:
    def __init__(self, username, password):
        self.auth = (username, password)

    def authorize(self):
        r = requests.get(API_URL + '/', auth=self.auth, timeout=2)
        if r.status_code != 200:
            raise ValueError()
        return r.json()

    def create_application(self, child_id, time):
        r = requests.post(API_URL + '/create-application/', auth=self.auth, data={'id':child_id, 'time':time})
        if r.status_code != 200:
            raise ValueError()
        return r.json()
