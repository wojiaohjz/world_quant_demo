import json
import os.path
from tools.path_tool import root_dir

user_file_path = os.path.join(root_dir, 'config/user.json')


def get_user_config():
    with open(user_file_path, 'r') as f:
        user_config = json.load(f)
    return user_config['username'], user_config['password']


if __name__ == '__main__':
    print(get_user_config())
