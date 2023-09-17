import requests
import os

email = os.environ['EMAIL']
password = os.environ['STD_PASSWORD']

class LayZSpa:
    BASE_URL = 'https://mobileapi.lay-z-spa.co.uk/v1'
    HEADERS = {
        'X-Requested-With': 'com.wiltonbradley.layzspa',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; SM-G930L Build/N2G48H; wv) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36')
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.data, self.headers = self._authenticate()

    def _authenticate(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response = requests.post(f'{self.BASE_URL}/auth/login', data=data)
        response.raise_for_status()
        json_data = response.json()
        api_token = json_data['data']['api_token']
        did = json_data['devices'][0]['did']

        data = {
            'api_token': api_token,
            'did': did
        }
        return data, {**self.HEADERS}

    def _post_request(self, endpoint, extra_data=None):
        data = {**self.data}
        if extra_data:
            data.update(extra_data)
        response = requests.post(f'{self.BASE_URL}/{endpoint}', data=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def status(self):
        return self._post_request('gizwits/status')

    def turn_on(self):
        return self._post_request('gizwits/turn_on')

    def turn_off(self):
        return self._post_request('gizwits/turn_off')
    
    def turn_filter_off(self):
        return self._post_request('gizwits/filter_off')
    def turn_filter_on(self):
        return self._post_request('gizwits/filter_on')
    #  IMPORTANT: Always Send a filter_on BEFORE you send the heat on command
    def turn_heat_on(self):
        try:
            isOn = self._post_request('gizwits/filter_on')
        except:
            pass
        return self._post_request('gizwits/filter_on')
    def turn_heat_off(self):
        return self._post_request('gizwits/heat_off')
    def turn_wave_on(self):
        return self._post_request('gizwits/wave_on')
    def turn_wave_off(self):
        return self._post_request('gizwits/wave_off')
    def temp_set(self, temp):
        return self._post_request('gizwits/temp_set', {'temperature': temp})

if __name__ == '__main__':
    spa = LayZSpa(email, password)
    print(spa.status())
    print(spa.turn_on())