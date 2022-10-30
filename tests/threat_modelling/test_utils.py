import unittest

from src.threat_modelling.utils import (
    format_text_on_node,
    get_list_of_probs_and_monet_amounts_from_children_dict)


class TestUtils(unittest.TestCase):

    def test_format_text_on_node(self):
        expected_formatted_text = 'Dummy threat: £100 (30.5%)'
        result_formatted_text = format_text_on_node('Dummy threat', 100, 0.305)
        self.assertEqual(expected_formatted_text, result_formatted_text)

    def test_get_list_of_probs_and_monet_amounts_from_children_dict(self):

        children_nodes_list_of_dicts = [
            {'id': 2, 'name': 'Spoofed identities', 'category': 'Spoofing identity', 'has_children': [
                {'id': 8, 'name': 'Orders to wrong email', 'category': 'Spoofing identity', 'probability': 0.3,
                 'monetary_amount': 1000},
                {'id': 9, 'name': 'Unencrypted email', 'category': 'Spoofing identity', 'probability': 0.9,
                 'monetary_amount': 800}]},
            {'id': 3, 'name': 'Loss of delivery data', 'category': 'Tampering with data', 'has_children': [
                {'id': 10, 'name': 'Delivery data on old PC', 'category': 'Tampering with data', 'probability': 0.6,
                 'monetary_amount': 2000}]}, {'id': 4, 'name': 'Unidentified users', 'category': 'Repudiation',
                                              'has_children': [
                                                  {'id': 11, 'name': 'Actions not logged', 'category': 'Repudiation',
                                                   'probability': 0.4, 'monetary_amount': 1250}]},
            {'id': 5, 'name': 'Leaked data', 'category': 'Information disclosure', 'has_children': [
                {'id': 12, 'name': 'Unsecure storage', 'category': 'Information disclosure', 'probability': 0.7,
                 'monetary_amount': 1500}, {'id': 13, 'name': 'Malware (data theft)',
                                            'category': 'Information disclosure', 'probability': 0.4,
                                            'monetary_amount': 2000}]},
            {'id': 6, 'name': "PC's unavailability", 'category': 'Denial of service', 'probability': 0.5,
             'monetary_amount': 3000}, {'id': 7, 'name': 'Compromised data', 'category': 'Elevation of privilege',
                                        'has_children': [{'id': 14, 'name': 'Violated authorisation',
                                                          'category': 'Elevation of privilege',
                                                          'probability': 0.4, 'monetary_amount': 5000}]}
        ]

        expected_list_of_monet_amounts = [1800, 2000, 1250, 3500, 3000, 5000]
        expected_list_of_probs = [0.27, 0.6, 0.4, 0.27999999999999997, 0.5, 0.4]

        result_list_of_monet_amounts, result_list_of_probs = get_list_of_probs_and_monet_amounts_from_children_dict(
            children_nodes_list_of_dicts
        )

        self.assertIsInstance(result_list_of_monet_amounts, list)
        self.assertIsInstance(result_list_of_probs, list)
        self.assertEqual(expected_list_of_monet_amounts, result_list_of_monet_amounts)
        self.assertEqual(expected_list_of_probs, result_list_of_probs)
