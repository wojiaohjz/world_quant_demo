from datetime import datetime


current_time = datetime.now()
def get_current_time_string():
    time_string = current_time.strftime("%Y%m%d_%H%M%S")
    return time_string


def get_current_date_string():
    # 使用 "%Y%m%d" 格式字符串来获取精确到天的时间
    date_string = current_time.strftime("%Y%m%d")
    return date_string
