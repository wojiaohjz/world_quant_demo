from api.auth_login import AuthLogin
import time

simulation_data = {
    "type": "REGULAR",
    "settings": {
        "instrumentType": "EQUITY",
        "region": "USA",
        "universe": "TOP3000",
        "delay": 1,
        "decay": 0,
        "neutralization": "INDUSTRY",
        "truncation": 0.08,
        "pasteurization": "ON",
        "unitHandling": "VERIFY",
        "nanHandling": "OFF",
        "language": "FASTEXPR",
        "visualization": False
    },
    "regular": "-scl12_buzz"
}

session = AuthLogin.get_session()
session2 = AuthLogin.get_session()
simulation_resp = session.post('https://api.worldquantbrain.com/simulations', json=simulation_data)
# print(simulation_resp.headers['Location'])
sim_progress_url = simulation_resp.headers['Location']

while True:
    sim_progress_resp = session.get(sim_progress_url)
    retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
    # simulation done!
    if retry_after_sec == 0:
        break
    time.sleep(retry_after_sec)

alpha_id = sim_progress_resp.json()['alpha']
print(alpha_id)