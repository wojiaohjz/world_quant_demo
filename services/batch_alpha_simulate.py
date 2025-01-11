from api.base_api import BaseApi
from tools.generate_alpha_list import generate_alpha_list


class BatchAlphaSimulate:
    def __init__(self):
        self.base_api = BaseApi()

    def alpha_simulate(self, alpha: str, settings: dict):
        """
        回测alpha
        :param alpha: alpha表达式
        :param settings: 回测设置
        :return: alpha_id
        """
        sim_progress_url = self.base_api.post_simulation_request(regular=alpha, type=settings['type'],
                                                            instrumentType=settings['instrumentType'],
                                                            region=settings['region'], universe=settings['universe'],
                                                            delay=settings['delay'], decay=settings['decay'],
                                                            neutralization=settings['neutralization'],
                                                            truncation=settings['truncation'],
                                                            pasteurization=settings['pasteurization'],
                                                            unitHandling=settings['unitHandling'],
                                                            nanHandling=settings['nanHandling'],
                                                            language=settings['language'],
                                                            visualization=settings['visualization'])
        alpha_id = self.base_api.get_simulation_result_alphaId(sim_progress_url)
        return alpha_id

    def get_company_fundmental_datafieds(self):
        """
        获取alpha表达式中用到的公司基本面数据
        :param alpha: alpha表达式
        :return: 公司基本面数据
        """
        searchScope = {
            "instrumentType": "EQUITY",
            "region": "USA",
            "delay": "1",
            "universe": "TOP3000"
        }
        fundamental6 = self.base_api.get_datafields(searchScope=searchScope, dataset_id="fundamental6")
        fundamental6_datafieds = fundamental6[fundamental6['type'] == 'MATRIX']['id'].values
        return fundamental6_datafieds

    def batch_simulate_demo_1(self):
        """
        批量回测alpha
        """

        # 组装批量alpha
        alpha_list = list()
        fundamental6_datafieds = self.get_company_fundmental_datafieds()
        for datafield in fundamental6_datafieds:
            alpha_expression = f"group_rank({datafield}/cap, subindustry)"
            alpha_list.append(alpha_expression)
        # 回测批量alpha
        settings = {
            "type": "REGULAR",
            "instrumentType": "EQUITY",
            "region": "USA",
            "universe": "TOP3000",
            "delay": 1,
            "decay": 0,
            "neutralization": "SUBINDUSTRY",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": False
        }
        for alpha in alpha_list:
            alpha_id = self.alpha_simulate(alpha=alpha, settings=settings)
            print("alpha_id: ", alpha_id)





if __name__ == '__main__':
    """
    批量回测alpha
    """
    # batch_simulate_demo_1()

    batch_alpha_simulate = BatchAlphaSimulate()

    alpha_template = "{0}({1}({2}, {3}), {4})"
    group_cp_op = ['group_rank', 'group_zscore', 'group_neutralize']
    ts_cp_op = ['ts_rank', 'ts_zscore', 'ts_av_diff']
    fundmental_datafieds = batch_alpha_simulate.get_company_fundmental_datafieds()
    days = ['200', '600']
    group = ['market', 'sector', 'industry', 'subindustry']
    combination_param_list = [group_cp_op, ts_cp_op, fundmental_datafieds, days, group]

    alpha_list = generate_alpha_list(aplha_template=alpha_template, combination_param_list=combination_param_list)
    print("the number of alpha: ", len(alpha_list))
    print(alpha_list[:20])
