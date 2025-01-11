
def generate_alpha_list(aplha_template: str, combination_param_list: list):

    alpha_list = list()
    len_ = len(combination_param_list)
    if len_ == 5:
        for param1 in combination_param_list[0]:
            for param2 in combination_param_list[1]:
                for param3 in combination_param_list[2]:
                    for param4 in combination_param_list[3]:
                        for param5 in combination_param_list[4]:
                            alpha = aplha_template.format(param1, param2, param3, param4, param5)
                            alpha_list.append(alpha)

    return alpha_list
