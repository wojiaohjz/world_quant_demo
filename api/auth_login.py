import requests
from requests.auth import HTTPBasicAuth
from tools.read_config_tool import get_user_config


class AuthLogin:
    _session = None
    @classmethod
    def get_session(cls):
        if cls._session is None:
            username, password = get_user_config()
            cls._session = requests.Session()
            cls._session.auth = HTTPBasicAuth(username, password)
            response = cls._session.post('https://api.worldquantbrain.com/authentication')
            # print(response.json())
            if response.status_code == 201:
                print('登录成功')
            else:
                cls._session = None
                print('登录失败')
        return cls._session


# if __name__ == '__main__':
#     session = AuthLogin.get_session()
