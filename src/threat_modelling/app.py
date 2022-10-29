import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import json

from constants import CURRENCY, PRECISION


with open('configs/pre_digitalisation.json') as json_file:
    try:
        threats_dict = json.load(json_file)
    except ValueError as except_val_err:
        logging.error(except_val_err)

children_nodes_list_of_dicts = threats_dict['threats']['has_children']
num_of_children_nodes = len(children_nodes_list_of_dicts)
num_of_children_of_child_nodes = 0

list_of_probs = []
list_of_monet_amounts = []

for child_node_dict in children_nodes_list_of_dicts:
    if 'has_children' in child_node_dict.keys():
        children_of_child_node_dict = child_node_dict['has_children']
        independent_prob = 1
        sum_monetary_amount = 0
        for child_of_child_node in children_of_child_node_dict:
            num_of_children_of_child_nodes += 1
            independent_prob *= child_of_child_node['probability']
            sum_monetary_amount += child_of_child_node['monetary_amount']

        list_of_probs.append(independent_prob)
        list_of_monet_amounts.append(sum_monetary_amount)
    else:
        list_of_probs.append(child_node_dict['probability'])
        list_of_monet_amounts.append(child_node_dict['monetary_amount'])

avg_prob = round(np.mean(list_of_probs), PRECISION)

total_monet_amount = 0

for monet_amount in list_of_monet_amounts:
    total_monet_amount += monet_amount

if threats_dict['threats']['id'] == 1 and threats_dict['threats']['category']:
    first_node = f"{threats_dict['threats']['name']}{': '}{CURRENCY}{str(total_monet_amount)}{' ('}{str(int(avg_prob*100))}{'%)'}"

print('first_node is: ', first_node)
print('num_of_children_nodes is: ', num_of_children_nodes)
print('num_of_children_of_child_nodes is: ', num_of_children_of_child_nodes)

G = nx.Graph()

counter_child_node = 0
for child_node_dict in children_nodes_list_of_dicts:
    child_node = f"{child_node_dict['name']}{': '}{CURRENCY}{list_of_monet_amounts[counter_child_node]}{' ('}{str(int(list_of_probs[counter_child_node]*100))}{'%)'}"
    G.add_edge(first_node, child_node)
    counter_child_node += 1
    if 'has_children' in child_node_dict.keys():
        children_of_child_node_dict = child_node_dict['has_children']
        for child_of_child_node in children_of_child_node_dict:
            G.add_edge(child_node, f"{child_of_child_node['name']}{': '}{CURRENCY}{child_of_child_node['monetary_amount']}{' ('}{str(int(child_of_child_node['probability']*100))}{'%)'}")
            print(child_of_child_node)

edge_list = [(u, v) for (u, v, d) in G.edges(data=True)]

pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

# Nodes
nx.draw_networkx_nodes(G, pos, node_size=12500)

# Edges
nx.draw_networkx_edges(G, pos, arrowsize=200, edgelist=edge_list, width=6, alpha=0.5, edge_color="b", style="dashed")

# Nodes' labels
nx.draw_networkx_labels(G, pos, font_size=6, font_family="sans-serif")

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()
