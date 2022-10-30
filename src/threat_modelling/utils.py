"""
This Python file has all utility-related functions required
to draw and visualise an attack tree.
"""

import json
import logging
from typing import List, Tuple

from .constants import (COLON_AND_WHITESPACE, CURRENCY, FACTOR_PERCENT,
                        PERCENT_AND_ROUND_BRACKET, PRECISION,
                        WHITESPACE_AND_ROUND_BRACKET)


# The function is excluded from the test coverage as trivial
# (hence the '# pragma: no cover' marker).
def extract_threats_dict_from_json(
        path_to_json: str
) -> dict:  # pragma: no cover
    """
    Extract a dictionary of security threats from a json file.

    Args:
        path_to_json: str
                    The path to a json file with security
                    threats, and the monetary value and the
                    probability for each threat on the leaf
                    nodes of the attack tree.

    Returns:
            A dictionary of security threats.
    """

    with open(path_to_json) as json_file:
        try:
            threats_dict = json.load(json_file)
        except ValueError as except_val_err:
            logging.error(except_val_err)
        return threats_dict


def format_text_on_node(
        threat_name: str,
        monetary_amount: float,
        prob: float
) -> str:
    """
    Format the text on a node describing the security
    threat it represents, along with its associated
    monetary amount and probability of occurrence.

    Args:
        threat_name: str
                    The name of a security threat.
        monetary_amount: float
                        The monetary amount of the
                        impact on the business
                        caused by a security threat.
        prob: float
            The probability of a security threat
            occurring (from 0 to 1).

    Returns:
            The formatted text to display on a node
            describing its associated security threat.
    """

    # The formatted text on each node will display
    # the following information:
    # - the name of the security threat identified,
    # - the monetary amount associated with it, and
    # - the probability of it occurring in %.
    formatted_str = f"" \
                    f"{threat_name}{COLON_AND_WHITESPACE}" \
                    f"{CURRENCY}{str(monetary_amount)}" \
                    f"{WHITESPACE_AND_ROUND_BRACKET}" \
                    f"{str(int(prob * FACTOR_PERCENT))}" \
                    f"{PERCENT_AND_ROUND_BRACKET}"

    return formatted_str


def get_list_of_probs_and_monet_amounts_from_children_dict(
        children_nodes_list_of_dicts: List[dict]
) -> Tuple[List[float], List[float]]:
    """
    Get the list of probabilities and monetary amounts
    from a list of dictionaries of children nodes
    of an attack tree.

    Args:
        children_nodes_list_of_dicts: List[dict]
                                    A list of dictionaries
                                    pertaining to the children
                                    nodes of an attack tree.

    Returns:
            A tuple with two lists of floats, the first one
            with a list of monetary amounts and the second
            one with a list of probabilities.
    """

    num_of_children_of_child_nodes = 0
    list_of_probs = []
    list_of_monet_amounts = []

    # The probabilities of the leaf nodes are assumed to
    # be from independent events and, thus, multiplied
    # to compute the probability at their parent node
    # based on the independent events downstream/at its
    # children nodes.
    # The monetary amount at the parent node is the sum
    # of the monetary amounts of the security threats
    # at its children nodes.
    for child_node_dict in children_nodes_list_of_dicts:
        if 'has_children' in child_node_dict.keys():
            children_of_child_node_dict = child_node_dict['has_children']
            independent_prob = 1
            sum_monetary_amount = 0
            for child_of_child_node in children_of_child_node_dict:
                num_of_children_of_child_nodes += 1
                independent_prob *= child_of_child_node['probability']
                sum_monetary_amount += child_of_child_node['monetary_amount']

            list_of_probs.append(round(independent_prob, PRECISION))
            list_of_monet_amounts.append(sum_monetary_amount)

            logging.info('The number of (sub-)children nodes '
                         '(from the child nodes) is: ',
                         num_of_children_of_child_nodes)
        else:
            list_of_probs.append(
                round(child_node_dict['probability'], PRECISION))
            list_of_monet_amounts.append(child_node_dict['monetary_amount'])

    return list_of_monet_amounts, list_of_probs
