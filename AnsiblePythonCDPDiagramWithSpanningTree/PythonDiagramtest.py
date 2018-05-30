#!/usr/bin/env python
import graphviz

# Define nodes/edges here...
edges = {('Arista249', 'Gi1/0/12'): ('HP830_LSW', 'Ethernet47'),
         ('Arista249', 'Gi2/0/22'): ('HP_5500EI', 'Ethernet48'),
         ('Arista249', 'Gi1/0/24'): ('HP_5500EI', 'Management1')}

styles = {
    'graph': {
        'label': 'Network Map',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'box',
        'fontcolor': 'white',
        'color': '#006699',
        'style': 'filled',
        'fillcolor': '#006699',
        'margin': '0.4',
    },
    'edges': {
        'style': 'dashed',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '10',
        'fontcolor': 'white',
    }
}

def draw_topology(topology, output_filename='topology'):
    nodes = set([key[0] for key in topology.keys() + topology.values()])

    g = graphviz.Graph(format='png')

    for node in nodes:
        g.node(node)

    for key, value in topology.iteritems():
        head, t_label = key
        tail, h_label = value
        g.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" "*12)

    g.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    g.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    g.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )

    g.render(filename=output_filename)





draw_topology(edges)
