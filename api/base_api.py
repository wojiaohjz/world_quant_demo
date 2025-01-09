from auth_login import AuthLogin
import time

session = AuthLogin.get_session()


def post_simulation_request(type="REGULAR", instrumentType="EQUITY",
                     region="USA", universe="TOP3000", delay=1, decay=0,
                     neutralization="INDUSTRY", truncation=0.08, pasteurization="ON",
                     unitHandling="VERIFY", nanHandling="OFF", language="FASTEXPR", visualization=False, regular=""):
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

    simulation_resp = session.post('https://api.worldquantbrain.com/simulations', json=simulation_data)

    return simulation_resp.headers['Location']


def get_simulation_result(sim_progress_url):
    """
    获取回测结果
    :param sim_progress_url: 获取回测结果的url
    :return: alpha_id
    """
    print(f"等待回测结果中....{sim_progress_url}")
    while True:
        sim_progress_resp = session.get(sim_progress_url)
        retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
        # simulation done!
        if retry_after_sec == 0:
            break
        time.sleep(retry_after_sec)
    print(f"回测完成：{sim_progress_url}")
    return sim_progress_resp.json()['alpha']


if __name__ == '__main__':
    sim_progress_url = post_simulation_request(regular="liabilities")
    alpha_id = get_simulation_result(sim_progress_url)
    print(alpha_id)

