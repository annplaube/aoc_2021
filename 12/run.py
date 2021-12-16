import sys
from collections import Counter

def parse_data():
    """Return graph as dictionary.

    Need all connections in non-directional graph, i.e. if there is an edge
    between nodes A and B, they should appear in each other's values:
    a: [B] and B: [A].
    """
    elements = [line.strip().split('-') for line in sys.stdin.readlines()]
    graph = {}
    for node_1, node_2 in elements:
        if node_1 in graph.keys():
            graph[node_1].append(node_2)
        else:
            graph[node_1] = [node_2]
        if node_2 in graph.keys():
            graph[node_2].append(node_1)
        else:
            graph[node_2] = [node_1]
    return graph


def find_all_paths(graph, start, end, node_permit, path=[]):
    """Return list of paths through graph from node start to node end.

    node_permit is a function returning True for nodes that may be visited.
    """
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph.keys():
        return []
    paths = []
    for node in graph[start]:
        if node_permit(node, path):
            newpaths = find_all_paths(graph, node, end, node_permit, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def lower_node_permitted_once(node, path):
    """Return True if node is permitted, False otherwise.

    Node is permitted if it is uppercase or not in the path yet.
    """
    if node.isupper() or node not in path:
        return True

def lower_node_permitted_twice(node, path):
    """Return True if node is permitted, False otherwise.

    Node is permitted if it is uppercase, OR not in the path, OR if there are
    no two lowercase nodes in the path yet. 'start' may not be visited twice.
    """
    if node == 'start':
        return False
    if node.isupper() or node not in path:
        return True
    lower_in_path = [n for n in path if n.islower()]
    counter = Counter(lower_in_path)
    if all([counter[low] == 1 for low in set(lower_in_path)]):
        return True


def number_of_paths(graph, start, end, node_permit):
    """Return number of paths through graph according to node_permit"""
    return len(find_all_paths(graph, start, end, node_permit))


if __name__ == '__main__':

    data = parse_data()


    # Part 1 -- Number of paths where lower case nodes can only be visited once
    print(number_of_paths(data, 'start', 'end', lower_node_permitted_once))


    # Part 2 -- Number of paths where one lower case node may be visited twice
    print(number_of_paths(data, 'start', 'end', lower_node_permitted_twice))
