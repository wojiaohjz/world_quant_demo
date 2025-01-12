import time

from api.base_api import BaseApi
from tools.generate_alpha_list import generate_alpha_list
from common.log import logger


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
        sim_progress_url = self.base_api.post_simulation_request(regular=alpha, settings=settings)
        alpha_id = self.base_api.get_simulation_result_alphaId(sim_progress_url)
        return alpha_id

    def alpha_simulate_retry(self, alpha: str, settings: dict, max_fail_count=15, sleep_time=15):
        """
        回测alpha
        :param alpha: alpha表达式
        :param settings: 回测设置
        :return: alpha_id
        """
        keep_trying = True
        fail_count = 0
        while keep_trying:
            try:
                sim_progress_url = self.base_api.post_simulation_request(regular=alpha, settings=settings)
                logger.info(f"Alpha location is : {sim_progress_url}")
                sim_progress_resp = self.base_api.get_location_resp(sim_progress_url)
                result_json = sim_progress_resp.json()
                # print(result_json)
                if 'status' in result_json and result_json['status'] == 'ERROR':
                    raise Exception(result_json['message'])
                #成功获取location，退出循环
                keep_trying = False
            except Exception as e:
                logger.error(f"This Alpha simulate error, sleep {sleep_time} and retry, error message is : {str(e)}")
                time.sleep(sleep_time)
                fail_count += 1

                #失败次数超过最大次数，重新认证session，退出循环
                if fail_count >= max_fail_count:
                    logger.info("重新认证session")
                    self.base_api.reset_session()
                    logger.error(f"This Alpha retry for many times, move to next alpha")
                    break

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
        fundamental6_datafieds = self.get_company_fundmental_datafieds()
        alpha_template = "group_rank({0}/cap, subindustry)"
        alpha_list = generate_alpha_list(alpha_template, fundamental6_datafieds)
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
        logger.info("总共有{}个alpha生成".format(len(alpha_list)))
        for index, alpha in enumerate(alpha_list):
            self.alpha_simulate_retry(alpha=alpha, settings=settings)
            # logger.info(f"{index}/{len(alpha_list)}  alpha_id: {alpha_id}")


if __name__ == '__main__':
    """
    批量回测alpha
    """
    batch_alpha_simulate = BatchAlphaSimulate()
    batch_alpha_simulate.batch_simulate_demo_1()

    # alpha_template = "{0}({1}({2}, {3}), {4})"
    # group_cp_op = ['group_rank', 'group_zscore', 'group_neutralize']
    # ts_cp_op = ['ts_rank', 'ts_zscore', 'ts_av_diff']
    # fundmental_datafieds = batch_alpha_simulate.get_company_fundmental_datafieds()
    # days = ['200', '600']
    # group = ['market', 'sector', 'industry', 'subindustry', 'densify(pv13_h_f1_sector)']
    #
    # alpha_list = generate_alpha_list(alpha_template, group_cp_op, ts_cp_op, fundmental_datafieds, days, group)
    # logger.info(f"the number of alpha: {len(alpha_list)}")
    # logger.warning(f"the number of alpha: {len(alpha_list)}")
    # logger.error(f"the number of alpha: {len(alpha_list)}")
    # for i in alpha_list[:20]:
    #     logger.info(i)


