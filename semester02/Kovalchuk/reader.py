import dot_parser
from graph import Graph as TaskGraph
from system_graph import Graph as SystemGraph


def read_task_graph_file(filename):
    with open(filename, 'r') as source:
        content = source.read()
    return read_task_graph(content)


def read_system_graph_file(filename):
    with open(filename, 'r') as source:
        content = source.read()
    return read_system_graph(content)


def read_task_graph(content):
    definitions = dot_parser.parse_dot_data(content)
    graph = definitions[0]
    g = TaskGraph()
    ids_mapping = {}
    for (ix, node) in enumerate(graph.get_nodes(), 1):
        id_ = int(node.get_name()[len('Node_'):])
        weight = int(node.get_label()[len(f'"{id_} ('):-2])
        ids_mapping[id_] = ix
        g.add_node(weight)

    for edge in graph.get_edges():
        source_id = int(edge.get_source()[len('Node_'):])
        target_id = int(edge.get_destination()[len('Node_'):])
        weight = int(edge.get_label()[1:-1])
        g.connect(source_id, target_id, weight)

    return g


def read_system_graph(content):
    definitions = dot_parser.parse_dot_data(content)
    graph = definitions[0]
    g = SystemGraph()
    ids_mapping = {}
    for (ix, node) in enumerate(graph.get_nodes(), 1):
        id_ = int(node.get_name()[len('Node_'):])
        weight = int(node.get_label()[len(f'"{id_} ('):-2])
        ids_mapping[id_] = ix
        g.add_node(weight)

    for edge in graph.get_edges():
        source_id = int(edge.get_source()[len('Node_'):])
        target_id = int(edge.get_destination()[len('Node_'):])
        g.connect(source_id, target_id)

    return g


def save(graph, filename):
    with open(filename, 'w') as file_:
        file_.write(str(graph))


if __name__ == '__main__':
    g = read_file('g.dot')
    save(g, 'g.dot.test')
    g2 = read_file('g.dot.test')
    print(g2)
