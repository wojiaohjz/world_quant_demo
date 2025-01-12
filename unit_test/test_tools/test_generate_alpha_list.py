import unittest
from tools.generate_alpha_list import generate_alpha_list

class TestGenerateAlphaList(unittest.TestCase):

    def test_generate_alpha_list_single_param(self):
        aplha_template = "alpha_{}"
        combination_param_list = [["1", "2", "3"]]
        expected_result = ["alpha_1", "alpha_2", "alpha_3"]
        result = generate_alpha_list(aplha_template, *combination_param_list)
        self.assertEqual(result, expected_result)

    def test_generate_alpha_list_two_params(self):
        aplha_template = "alpha_{}_{}"
        combination_param_list = [["1", "2"], ["a", "b"]]
        expected_result = ["alpha_1_a", "alpha_1_b", "alpha_2_a", "alpha_2_b"]
        result = generate_alpha_list(aplha_template, *combination_param_list)
        self.assertEqual(result, expected_result)

    def test_generate_alpha_list_three_params(self):
        aplha_template = "alpha_{}_{}_{}"
        combination_param_list = [["1", "2"], ["a", "b"], ["x", "y"]]
        expected_result = ["alpha_1_a_x", "alpha_1_a_y", "alpha_1_b_x", "alpha_1_b_y", "alpha_2_a_x", "alpha_2_a_y", "alpha_2_b_x", "alpha_2_b_y"]
        result = generate_alpha_list(aplha_template, *combination_param_list)
        self.assertEqual(result, expected_result)

    def test_generate_alpha_list_four_params(self):
        aplha_template = "alpha_{}_{}_{}_{}"
        combination_param_list = [["1", "2"], ["a", "b"], ["x", "y"], ["m", "n"]]
        expected_result = ["alpha_1_a_x_m", "alpha_1_a_x_n", "alpha_1_a_y_m", "alpha_1_a_y_n", "alpha_1_b_x_m", "alpha_1_b_x_n", "alpha_1_b_y_m", "alpha_1_b_y_n", "alpha_2_a_x_m", "alpha_2_a_x_n", "alpha_2_a_y_m", "alpha_2_a_y_n", "alpha_2_b_x_m", "alpha_2_b_x_n", "alpha_2_b_y_m", "alpha_2_b_y_n"]
        result = generate_alpha_list(aplha_template, *combination_param_list)
        self.assertEqual(result, expected_result)

    def test_generate_alpha_list_five_params(self):
        aplha_template = "alpha_{}_{}_{}_{}_{}"
        combination_param_list = [["1", "2"], ["a", "b"], ["x", "y"], ["m", "n"], ["p", "q"]]
        expected_result = ["alpha_1_a_x_m_p", "alpha_1_a_x_m_q", "alpha_1_a_x_n_p", "alpha_1_a_x_n_q", "alpha_1_a_y_m_p", "alpha_1_a_y_m_q", "alpha_1_a_y_n_p", "alpha_1_a_y_n_q", "alpha_1_b_x_m_p", "alpha_1_b_x_m_q", "alpha_1_b_x_n_p", "alpha_1_b_x_n_q", "alpha_1_b_y_m_p", "alpha_1_b_y_m_q", "alpha_1_b_y_n_p", "alpha_1_b_y_n_q", "alpha_2_a_x_m_p", "alpha_2_a_x_m_q", "alpha_2_a_x_n_p", "alpha_2_a_x_n_q", "alpha_2_a_y_m_p", "alpha_2_a_y_m_q", "alpha_2_a_y_n_p", "alpha_2_a_y_n_q", "alpha_2_b_x_m_p", "alpha_2_b_x_m_q", "alpha_2_b_x_n_p", "alpha_2_b_x_n_q", "alpha_2_b_y_m_p", "alpha_2_b_y_m_q", "alpha_2_b_y_n_p", "alpha_2_b_y_n_q"]
        result = generate_alpha_list(aplha_template, *combination_param_list)
        self.assertEqual(result, expected_result)

    def test_generate_alpha_list_invalid_length(self):
        aplha_template = "alpha_{}"
        combination_param_list = [["1", "2"], ["a", "b"], ["x", "y"], ["m", "n"], ["p", "q"], ["r", "s"]]
        with self.assertRaises(ValueError):
            generate_alpha_list(aplha_template, *combination_param_list)

if __name__ == '__main__':
    unittest.main()
