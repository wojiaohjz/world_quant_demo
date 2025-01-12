
def generate_alpha_list(aplha_template: str, *combination_param_list):
    """
    生成alpha列表
    :param aplha_template: alpha模板
    :param combination_param_list: 组合参数列表
    :return: alpha列表
    """
    alpha_list = list()
    len_ = len(combination_param_list)
    if len_ == 1:
        for param in combination_param_list[0]:
            alpha = aplha_template.format(param)
            alpha_list.append(alpha)
    elif len_ == 2:
        for param1 in combination_param_list[0]:
            for param2 in combination_param_list[1]:
                alpha = aplha_template.format(param1, param2)
                alpha_list.append(alpha)
    elif len_ == 3:
        for param1 in combination_param_list[0]:
            for param2 in combination_param_list[1]:
                for param3 in combination_param_list[2]:
                    alpha = aplha_template.format(param1, param2, param3)
                    alpha_list.append(alpha)
    elif len_ == 4:
        for param1 in combination_param_list[0]:
            for param2 in combination_param_list[1]:
                for param3 in combination_param_list[2]:
                    for param4 in combination_param_list[3]:
                        alpha = aplha_template.format(param1, param2, param3, param4)
                        alpha_list.append(alpha)
    elif len_ == 5:
        for param1 in combination_param_list[0]:
            for param2 in combination_param_list[1]:
                for param3 in combination_param_list[2]:
                    for param4 in combination_param_list[3]:
                        for param5 in combination_param_list[4]:
                            alpha = aplha_template.format(param1, param2, param3, param4, param5)
                            alpha_list.append(alpha)
    else:
        raise ValueError("Invalid length of combination_param_list")

    return alpha_list

