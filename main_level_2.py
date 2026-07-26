import ast
import json
import networkx as nx

from pathlib import Path
from typing import Any

SOURCE_DATA = 'data/level_1.txt'


def load_python_literal_file(source_file) -> dict[str, Any]:
    """Load and parse a Python literal data structure from a text file.

    Opens `source_file`, reads its contents as text, and safely evaluates the
    contents using `ast.literal_eval`. This supports Python literal values
    such as dictionaries, lists, tuples, strings, numbers, booleans, and
    None.

    Args:
        source_file: Path to the text file containing a Python literal.

    Returns:
        A dictionary representing the parsed data.
    """

    with open(source_file, 'r') as f:
        file_content = f.read()
    return ast.literal_eval(file_content)


def get_start_and_end_nodes(data: dict[str, Any]) -> tuple[str, str]:
    """Extract the start and end nodes from the data.

    This function retrieves the 'start' and 'end' nodes from the input
    dictionary `data`. It assumes that the keys 'start' and 'end' exist in
    the dictionary.

    Args:
        data: A dictionary containing the graph data.

    Returns:
        A tuple containing the start node and end node as strings.
    """
    start_node = data['start']
    end_node = data['end']
    
    return start_node, end_node


def extract_edges_from_data(data: dict[str, Any]) -> list[tuple[str, str]]:
    """Extract edges from a nested dictionary structure.

    This function recursively traverses the input dictionary `data` and
    collects edges represented as tuples of (source_node, target_node, weight). 
    It handles nested dictionaries and lists, extracting edges for each
    key-value pair.

    Args:
        data: A nested dictionary structure.

    Returns:
        A list of tuples representing the edges in the graph.
    """

    graph = data['adjacency_list']
    
    edges = []
    for key, values in graph.items():

        for value in values:

            node = value['node']
            weight = value['weight']

            entry = (key, node, weight)
            edges.append(entry)

    return edges


def build_graph_from_source(edges: list[tuple[str, str]], source: str, target: str) -> list[str]:
    """Build a directed graph from a list of edges.

    This function creates a directed graph using the NetworkX library and adds
    edges to it based on the provided list of edges. Each edge is represented
    as a tuple of (source_node, target_node, weight).

    Args:
        edges: A list of tuples representing the edges in the graph.
        source: The source node for the path.
        target: The target node for the path.

    Returns:
        A directed graph (DiGraph) constructed from the edges.
    """

    # Create a weighted graph
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    path = nx.dijkstra_path(G, source=source, target=target)

    return path

def create_directory_if_not_exists(folder_path: Path) -> None:
    """Create a directory if it does not exist.

    This function checks if the specified `folder_path` exists, and if not,
    it creates the directory along with any necessary parent directories.

    Args:
        folder_path: The path of the directory to create.
    """
    folder_path.mkdir(parents=True, exist_ok=True)


def save_results_to_file(results: dict[str, Any], file_path: Path) -> None:
    """Save results to a text file.

    This function writes the provided `results` dictionary to a text file
    specified by `file_path`. The results are converted to a string before
    writing.

    Args:
        results: A dictionary containing the results to save.
        file_path: The path of the file where the results will be saved.
    """
    with open(file_path, 'w') as f:
        json.dump(results, f)

def main():

    folder_path = Path('output')
    create_directory_if_not_exists(folder_path)

    data = load_python_literal_file(SOURCE_DATA)
    start_node, end_node = get_start_and_end_nodes(data)
    edges = extract_edges_from_data(data)
    
    path = build_graph_from_source(edges, source=start_node, target=end_node)

    results = {
        "route": path
    }
    
    file_path = folder_path / 'level_1_shortest_path.txt'
    save_results_to_file(results, file_path)

if __name__ == "__main__":
    main()
