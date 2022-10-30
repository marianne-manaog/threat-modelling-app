"""
This Python file has the codes of the main application
required to draw and visualise an attack tree.
"""

import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .constants import (FIRST_NODE_THREAT_CATEGORY, FIRST_NODE_THREAT_ID,
                        FONT_FAMILY, FONT_SIZE,
                        OUTPUT_FILE_ATTACK_TREE_POST_DIGITAL,
                        PATH_TO_POST_DIGITAL_JSON,
                        PRECISION, SEED_NODE_POS)
from .utils import (extract_threats_dict_from_json, format_text_on_node,
                    get_list_of_probs_and_monet_amounts_from_children_dict)


def visualise_and_save_attack_tree(
        output_file_name: str,
        path_to_json: str
) -> None:
    """
    Visualise and save an attack tree to an .svg file
    for avoiding any loss in resolution as zoom is
    applied on the figure for ease of visualisation.

    Args:
        output_file_name: str
                        The output file name of the
                        attack tree visualised in
                        this function.
        path_to_json: str
                    The path to a json file with
                    security threats, and the monetary
                    value and the probability for
                    each threat on the leaf nodes of
                    the attack tree.
    """

    # Extract a dictionary of security threats from
    # a given json file specified in the argument
    # of this function.
    threats_dict = extract_threats_dict_from_json(path_to_json)

    # Get the list of dictionaries of the children
    # nodes, such that a list of their associated
    # monetary amounts and probabilities can then
    # be extracted.
    children_nodes_list_of_dicts = threats_dict['threats']['has_children']
    num_of_children_nodes = len(children_nodes_list_of_dicts)
    logging.info(
        'The number of children nodes (from the '
        'first node) is: ', num_of_children_nodes)

    # Extract the lists of the monetary amounts (in £)
    # and probabilities (from 0 to 1) associated with
    # the security threats represented by the above-mentioned
    # children nodes to then be able to compute the
    # total monetary amount that such threats could cost
    # to the business, along with how likely that could
    # occur on average (based on the list of extracted
    # probabilities).
    list_of_monet_amounts, list_of_probs = \
        get_list_of_probs_and_monet_amounts_from_children_dict(
            children_nodes_list_of_dicts)

    # The total probability is the average of the
    # probabilities of each identified security
    # threat occurring.
    avg_prob = round(np.mean(list_of_probs), PRECISION)

    total_monet_amount = 0

    # The total monetary amount is the sum of the
    # monetary amounts for each security threat identified.
    for monet_amount in list_of_monet_amounts:
        total_monet_amount += monet_amount

    # Define the first node as that having ID equal
    # to 1 and the threat's category equal to
    # 'Combined' (each security threat that is a part
    # of it was defined as per the STRIDE model in
    # the input json file).
    first_node = ''
    if threats_dict['threats']['id'] == FIRST_NODE_THREAT_ID and \
            threats_dict['threats']['category'] == FIRST_NODE_THREAT_CATEGORY:
        first_node = format_text_on_node(
            threat_name=threats_dict['threats']['name'],
            monetary_amount=total_monet_amount,
            prob=round(avg_prob, PRECISION)
        )
        logging.info('The first node is: ', first_node)
    else:
        logging.error(
            f"The first node has not been defined "
            f"correctly. Please ensure its threat "
            f"id is '{FIRST_NODE_THREAT_ID}' "
            f"and its threat category is "
            f"'{FIRST_NODE_THREAT_CATEGORY}'."
        )

    # Define the graph object containing the attack
    # tree wherein each node represents each security
    # threat identified and each edge represents the
    # relationship between a parent and a child node,
    # such that all security threats can be visualised
    # and understood within the context of an attack tree.
    # N.B.: for ease of visualisation and optimisation
    # of the space/canvas on the figure, the first
    # node was placed at the centre of the figure and
    # the other nodes stemming from it based on the
    # STRIDE model, with the lowest/leaf nodes having
    # their monetary amounts and probabilities defined
    # in the json file, whilst their parent nodes'
    # monetary amounts and probabilities were computed
    # from those of such leaf nodes respectively by
    # summing up the monetary amounts of the children
    # nodes and multiplying the individual children
    # nodes' probabilities (as considered independent
    # events).
    graph_obj = nx.Graph()

    counter_child_node = 0
    for child_node_dict in children_nodes_list_of_dicts:
        child_node = format_text_on_node(
            threat_name=child_node_dict['name'],
            monetary_amount=list_of_monet_amounts[counter_child_node],
            prob=round(list_of_probs[counter_child_node], PRECISION)
        )
        graph_obj.add_edge(first_node, child_node)
        counter_child_node += 1
        if 'has_children' in child_node_dict.keys():
            children_of_child_node_dict = child_node_dict['has_children']
            for child_of_child_node in children_of_child_node_dict:
                child_of_child_node_text = format_text_on_node(
                    threat_name=child_of_child_node['name'],
                    monetary_amount=child_of_child_node['monetary_amount'],
                    prob=round(child_of_child_node['probability'], PRECISION)
                )
                graph_obj.add_edge(child_node, child_of_child_node_text)

    edge_list = [
        (u, v) for (u, v, d) in graph_obj.edges(data=True)
    ]

    # Define the position for all nodes, set consistently
    # via a fixed number (seed) for reproducibility.
    pos = nx.spring_layout(graph_obj, seed=SEED_NODE_POS)

    # Draw the nodes on the graph, each of which represents
    # an identified security threat.
    nx.draw_networkx_nodes(graph_obj, pos, node_size=12500)

    # Draw the edges on the graph, each of which representing
    # the relationship between a parent node and its
    # child/children.
    nx.draw_networkx_edges(
        graph_obj, pos, arrowsize=200, edgelist=edge_list,
        width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # Draw the nodes' labels with the monetary amount
    # and probability associated to an identified
    # security threat.
    nx.draw_networkx_labels(
        graph_obj, pos, font_size=FONT_SIZE,
        font_family=FONT_FAMILY)

    # Show the attack tree on a pop-up window.
    ax_fig = plt.gca()
    ax_fig.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # Save the attack tree to an .svg file for
    # ease of visualisation, as its resolution
    # is not impacted regardless of
    # the zoom factor/percentage applied.
    ax_fig.figure.savefig(output_file_name, dpi=ax_fig.figure.dpi)


if __name__ == "__main__":

    # Define the path to the json file with the
    # threats considered, and the associated
    # monetary amounts and probabilities at the
    # leaf nodes, as well as the name of the
    # output file displaying the resulting
    # attack tree. The function below will visualise
    # and save the attack tree to an .svg file.
    visualise_and_save_attack_tree(
        path_to_json=PATH_TO_POST_DIGITAL_JSON,
        output_file_name=OUTPUT_FILE_ATTACK_TREE_POST_DIGITAL
    )
