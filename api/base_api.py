from api.auth_login import AuthLogin
import time
import pandas as pd

from common.log import logger


class BaseApi:
    def __init__(self):
        self.session = AuthLogin.get_session()

    def reset_session(self):
        """
        重新认证，重置session
        """
        self.session = AuthLogin.get_new_session()

    def post_simulation_request(self, regular: str, settings: dict):
        """
        提交回测请求
        :return: 获取回测结果的url
        """
        simulation_data = {
            "type": settings['type'],
            "settings": {
                "instrumentType": settings['instrumentType'],
                "region": settings['region'],
                "universe": settings['universe'],
                "delay": settings['delay'],
                "decay": settings['decay'],
                "neutralization": settings['neutralization'],
                "truncation": settings['truncation'],
                "pasteurization": settings['pasteurization'],
                "unitHandling": settings['unitHandling'],
                "nanHandling": settings['nanHandling'],
                "language": settings['language'],
                "visualization": settings['visualization']
            },
            "regular": regular
        }

        simulation_resp = self.session.post('https://api.worldquantbrain.com/simulations', json=simulation_data)
        logger.info(f"post simulate Alpha: {regular}")
        return simulation_resp.headers['Location']

    def get_location_resp(self, sim_progress_url):
        """
        获取回测结果
        :param sim_progress_url: 回测结果的url
        :return: 获取回测结果的response
        """
        return self.session.get(sim_progress_url)

    def get_simulation_result(self, sim_progress_url):
        """
        获取回测结果
        :param sim_progress_url: 获取回测结果的url
        :return: alpha_id
        """
        logger.info(f"等待此次回测结果中....")
        while True:
            sim_progress_resp = self.session.get(sim_progress_url)
            retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
            # simulation done!
            if retry_after_sec == 0:
                break
            time.sleep(retry_after_sec)
        logger.info(f"此次回测完成")
        return sim_progress_resp.json()

    def get_simulation_result_alphaId(self, sim_progress_url):
        """
        获取回测结果
        :param sim_progress_url: 获取回测结果的url
        :return: alpha_id
        """
        return self.get_simulation_result(sim_progress_url)['alpha']

    def get_datafields(self, searchScope, dataset_id: str = "", search: str = ""):
        """
        获取数据字段
        :param searchScope: 数据字段类型
        :param dataset_id: 数据集id
        :param search: 搜索关键字
        :return: 数据字段列表
        """
        instrumentType = searchScope['instrumentType']
        region = searchScope['region']
        delay = searchScope['delay']
        universe = searchScope['universe']
        datafilds_url = "https://api.worldquantbrain.com/data-fields"
        offset = '0'
        # 如果search为空
        if len(search) == 0:
            params = {
                "instrumentType": instrumentType,
                "region": region,
                "delay": delay,
                "universe": universe,
                "dataset.id": dataset_id,
                "limit": "50",
                "offset": offset
            }
            response = self.session.get(datafilds_url, params=params).json()
            count = response['count']
        else:
            count = 100
            params = {
                "instrumentType": instrumentType,
                "region": region,
                "delay": delay,
                "universe": universe,
                "limit": "50",
                "search": search,
                "offset": offset
            }

        datafields_list = list()
        for offset in range(0, count, 50):
            params['offset'] = str(offset)
            datafilds = self.session.get(datafilds_url, params=params).json()['results']
            datafields_list.append(datafilds)
        datafields_list = [item for sublist in datafields_list for item in sublist]
        return pd.DataFrame(datafields_list)


# if __name__ == '__main__':
#
#     base_api = BaseApi()
#     session_old = base_api.session
#     base_api.reset_session()
#     session_new = base_api.session
#     print(session_new, session_old)
#     print(session_new is session_old)