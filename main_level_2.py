import ast
import json
import math
import networkx as nx

from functools import permutations
from pathlib import Path
from typing import Any


SOURCE_DATA = 'data/level_2.txt'
OUTPUT_FILE = 'level_2_shortest_path.txt'


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


def get_additional_nodes(data: dict[str, Any]) -> str:
    """Extract additional nodes from the data.

    This function retrieves the 'additional_nodes' from the input
    dictionary `data`. It assumes that the key 'additional_nodes' exists in
    the dictionary.

    Args:
        data: A dictionary containing the graph data.

    Returns:
        A string containing the additional nodes.
    """

    return data['required_stops']


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
            weight = value['time'] + value['risk']

            entry = (key, node, weight)
            edges.append(entry)

    return edges


def build_weighted_graph(edges: list[tuple[str, str, int]]) -> nx.Graph:
    """Create a weighted graph from the collected edges.

    This function initializes an undirected graph and adds the provided
    edges with their associated weights so it can be used for pathfinding.

    Args:
        edges: A list of tuples of start and end nodes with weights.
    
    Returns:
        A NetworkX Graph object representing the weighted graph.
    """

    # Create a weighted graph
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    return G


def get_distance_and_path(G: nx.Graph, start_node: str, end_node: str) -> tuple[int, list[str]]:
    """Find the shortest path and its distance in a weighted graph.

    Args:
        G: A NetworkX Graph object representing the weighted graph.
        start_node: The starting node for the path.
        end_node: The target node for the path.

    Returns:
        A tuple containing the shortest distance and the path as a list of nodes.
    """

    path = nx.dijkstra_path(G, source=start_node, target=end_node)
    distance = nx.dijkstra_path_length(G, source=start_node, target=end_node)

    return distance, path


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
    required_stops = get_additional_nodes(data)
    edges = extract_edges_from_data(data)

    G = build_weighted_graph(edges)

    min_distance = math.inf
    # Get all pemutations of the required stops
    all_perms = permutations(required_stops)

    for perm in all_perms:
        route = []
        distance = 0
        travel_path = [start_node] + list(perm) + [end_node]
        for i, (start_loc, end_loc) in enumerate(zip(travel_path[:-1], travel_path[1:])):

            distance, calc_route = get_distance_and_path(G, start_loc, end_loc)
            if not i:
                route += calc_route
            else:
                # Exclude first entry since its the same as last entry of previous
                # calculated route
                route += calc_route[1:]

        if distance <= min_distance:
            optimum_route = route 
            min_distance = distance


    results = {
        "route": optimum_route
    }
    
    file_path = folder_path / OUTPUT_FILE
    save_results_to_file(results, file_path)

if __name__ == "__main__":
    main()
