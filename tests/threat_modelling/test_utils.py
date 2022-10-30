import unittest

from src.threat_modelling.utils import (
    format_text_on_node,
    get_list_of_probs_and_monet_amounts_from_children_dict)

from .dummy_lists import children_nodes_list_of_dicts


class TestUtils(unittest.TestCase):

    def test_format_text_on_node(self):
        expected_formatted_text = 'Dummy threat: £100 (30.5%)'
        result_formatted_text = format_text_on_node('Dummy threat', 100, 0.305)
        self.assertEqual(expected_formatted_text, result_formatted_text)

    def test_get_list_of_probs_and_monet_amounts_from_children_dict(self):

        expected_list_of_monet_amounts = [1800, 2000, 1250, 3500, 3000, 5000]
        expected_list_of_probs = [0.27, 0.6, 0.4, 0.27999999999999997, 0.5, 0.4]

        result_list_of_monet_amounts, result_list_of_probs = get_list_of_probs_and_monet_amounts_from_children_dict(
            children_nodes_list_of_dicts
        )

        self.assertIsInstance(result_list_of_monet_amounts, list)
        self.assertIsInstance(result_list_of_probs, list)
        self.assertEqual(expected_list_of_monet_amounts, result_list_of_monet_amounts)
        self.assertEqual(expected_list_of_probs, result_list_of_probs)
