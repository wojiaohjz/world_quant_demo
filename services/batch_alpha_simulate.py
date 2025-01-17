import random
import time
from data_fields import *
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
                retry_after_sec = sim_progress_resp.headers.get("Retry-After", 0)
                if 'progress' not in result_json and result_json['status'] == 'ERROR':
                    raise Exception(result_json['message'])
                #成功获取location，退出循环
                logger.info(f"{result_json}, retry_after_sec is : {retry_after_sec}")
                logger.info(f"Post simulate success!")
                keep_trying = False
            except Exception as e:
                fail_count += 1
                logger.error(
                    f"This Alpha simulate error, sleep {sleep_time} and retry {fail_count}/{max_fail_count}, error message is : {str(e)}")
                time.sleep(sleep_time)

                #失败次数超过最大次数，重新认证session，退出循环
                if fail_count >= max_fail_count:
                    logger.info("Reset Auth session")
                    self.base_api.reset_session()
                    logger.error(f"This Alpha retry for many times, move to next alpha")
                    break


    def batch_simulate_demo_1(self):
        """
        批量回测alpha
        """

        # 组装批量alpha
        fundamental6_datafieds = get_data_fields(dataset_id="fundamental6")
        alpha_template = "group_neutralize({0}/cap, subindustry)"
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
        self.batch_simulate_alpha_list(alpha_list, settings)

    def batch_simulate_demo_2(self):
        """
        批量回测alpha
        """
        # 组装批量alpha
        alpha_template = "{0}({1}({2}, {3}), {4})"
        group_cp_op = ['group_rank', 'group_zscore', 'group_neutralize']
        ts_cp_op = ['ts_rank', 'ts_zscore', 'ts_av_diff']
        fundmental_datafieds = get_data_fields(dataset_id="fundamental6")
        days = ['200', '600']
        group = ['market', 'sector', 'industry', 'subindustry', 'densify(pv13_h_f1_sector)']
        alpha_list = generate_alpha_list(alpha_template, group_cp_op, ts_cp_op, fundmental_datafieds, days, group)
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
        self.batch_simulate_alpha_list(alpha_list, settings)

    def batch_simulate_alpha_list(self, alpha_list, settings):
        """
        批量回测alpha
        """
        logger.info(f"There are total {len(alpha_list)} Alpha")
        for index, alpha in enumerate(alpha_list):
            logger.info(f"********Goto {index + 1}/{len(alpha_list)} Alpha********")
            self.alpha_simulate_retry(alpha=alpha, settings=settings)


if __name__ == '__main__':
    """
    批量回测alpha
    """
    batch_alpha_simulate = BatchAlphaSimulate()
    # batch_alpha_simulate.batch_simulate_demo_1()
    alpha_template = "ts_rank({0}/cap, 252)"
    datafieds = get_data_fields(dataset_id="fundamental6")
    # days = ['200', '600']
    alpha_list = list()
    alpha_list = generate_alpha_list(alpha_template, datafieds)
    random.shuffle(alpha_list)
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
    batch_alpha_simulate.batch_simulate_alpha_list(alpha_list, settings)
