import requests
from requests.auth import HTTPBasicAuth
from tools.read_config_tool import get_user_config
from common.log import logger


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
                logger.info('认证成功')
            else:
                cls._session = None
                logger.info('认证失败')
        return cls._session

    @classmethod
    def get_new_session(cls):
        cls._session = None
        return cls.get_session()


# if __name__ == '__main__':
#     session1 = AuthLogin.get_session()
#     session2 = AuthLogin.get_session()
#     new_session = AuthLogin.get_new_session()
#     print(session1 is session2)
#     print(session1, session2, new_session)
#     print(session1 is new_session)
