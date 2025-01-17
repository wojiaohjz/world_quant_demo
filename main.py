import random

from services.batch_alpha_simulate import BatchAlphaSimulate
from services.data_fields import get_data_fields
from tools.generate_alpha_list import generate_alpha_list


def main():
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


if __name__ == '__main__':
    main()
