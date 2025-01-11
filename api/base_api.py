from api.auth_login import AuthLogin
import time
import pandas as pd


class BaseApi:
    def __init__(self):
        self.session = AuthLogin.get_session()

    def post_simulation_request(self, type="REGULAR", instrumentType="EQUITY",
                                region="USA", universe="TOP3000", delay=1, decay=0,
                                neutralization="SUBINDUSTRY", truncation=0.08, pasteurization="ON",
                                unitHandling="VERIFY", nanHandling="ON", language="FASTEXPR", visualization=False,
                                regular=""):
        """
        提交回测请求
        :return: 获取回测结果的url
        """
        simulation_data = {
            "type": type,
            "settings": {
                "instrumentType": instrumentType,
                "region": region,
                "universe": universe,
                "delay": delay,
                "decay": decay,
                "neutralization": neutralization,
                "truncation": truncation,
                "pasteurization": pasteurization,
                "unitHandling": unitHandling,
                "nanHandling": nanHandling,
                "language": language,
                "visualization": visualization
            },
            "regular": regular
        }

        simulation_resp = self.session.post('https://api.worldquantbrain.com/simulations', json=simulation_data)
        print(f"提交回测的Alpha: {regular}")
        return simulation_resp.headers['Location']

    def get_simulation_result(self, sim_progress_url):
        """
        获取回测结果
        :param sim_progress_url: 获取回测结果的url
        :return: alpha_id
        """
        print(f"等待此次回测结果中....")
        while True:
            sim_progress_resp = self.session.get(sim_progress_url)
            retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
            # simulation done!
            if retry_after_sec == 0:
                break
            time.sleep(retry_after_sec)
        print(f"此次回测完成")
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


if __name__ == '__main__':
    # sim_progress_url = post_simulation_request(regular="liabilities")
    # alpha_id = get_simulation_result(sim_progress_url)
    # print(alpha_id)
    base_api = BaseApi()
    searchScope = {
        "instrumentType": "EQUITY",
        "region": "USA",
        "delay": "1",
        "universe": "TOP3000"
    }
    fundamental6 = base_api.get_datafields(searchScope=searchScope, dataset_id="fundamental6")
    fundamental6_datafieds = fundamental6[fundamental6['type'] == 'MATRIX']['id'].values
    alpha_list = list()
    for datafield in fundamental6_datafieds:
        alpha_expression = f"group_rank({datafield}/cap, subindustry)"
        # print(alpha_expression)
        alpha_list.append(alpha_expression)
    print(len(alpha_list))
    for alpha in alpha_list:
        sim_progress_url = base_api.post_simulation_request(regular=alpha)
        alpha_id = base_api.get_simulation_result(sim_progress_url)
        print(alpha_id)
