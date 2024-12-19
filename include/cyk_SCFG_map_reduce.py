# Python implementation for the
# CYK Algorithm

from multiprocessing import Pool, Manager
from collections import defaultdict


def mapper(args):
    """
    Process one set of spans (map task).
    Args:
        args: (table, grammar, i, j, i', j') for a specific span
    Returns:
        Key-value pairs of the form:
        (i, j, i', j') -> [list of non-terminals]
    """
    table, grammar, i, j, i_prime, j_prime = args
    results = []

    for k in range(i + 1, j):
        for k_prime in range(i_prime + 1, j_prime):
            # Look for pairs of spans to combine
            left_items = table.get((i, k, i_prime, k_prime), [])
            right_items = table.get((k, j, k_prime, j_prime), [])

            for B in left_items:
                for C in right_items:
                    # Check if grammar rules apply
                    for lhs in grammar:
                        for rhs in grammar[lhs]:
                            source_rhs, target_rhs = rhs
                            if source_rhs == [B, C] and target_rhs == [B, C]:
                                results.append((i, j, i_prime, j_prime, lhs))
                            elif source_rhs == [B, C] and target_rhs == [C, B]:
                                results.append((i, j, i_prime, j_prime, lhs))
    return results

def reducer(mapped_results):
    """
    Combine all results from mappers (reduce task).
    Args:
        mapped_results: List of results from mappers
    Returns:
        A combined table for all spans
    """
    table = defaultdict(list)
    for result in mapped_results:
        for i, j, i_prime, j_prime, lhs in result:
            table[(i, j, i_prime, j_prime)].append(lhs)
    return table


def parse_with_mapreduce(grammar, w, w_prime):
    """
    Parse using MapReduce-like parallelism.
    Args:
        grammar: List of grammar rules
        w: Source string (list of tokens)
        w_prime: Target string (list of tokens)
    Returns:
        Boolean indicating whether the input is accepted
    """
    n, n_prime = len(w), len(w_prime)
    links = defaultdict(list)

    # Initialize unary productions (axioms)
    for i in range(n):
        for i_prime in range(n_prime):
            for lhs in grammar:
                for rhs in grammar[lhs]:
                    source_rhs, target_rhs = rhs
                    if len(source_rhs) == 1 and len(target_rhs) == 1:
                        if source_rhs[0] == w[i] and target_rhs[0] == w_prime[i_prime]:
                            links[(i, i + 1, i_prime, i_prime + 1)].append(lhs)
            
    # Process spans in increasing order of length
    with Pool() as pool:
        for span_length in range(2, n + 1):
            for span_length_prime in range(2, n_prime + 1):
                tasks = []
                
                # Prepare tasks for the mappers
                for i in range(n - span_length + 1):
                    for i_prime in range(n_prime - span_length_prime + 1):
                        j = i + span_length
                        j_prime = i_prime + span_length_prime
                        tasks.append((links, grammar, i, j, i_prime, j_prime))
                
                # Map phase: distribute tasks
                mapped_results = pool.map(mapper, tasks)
                
                # Reduce phase: combine results
                links.update(reducer(mapped_results))
    
    # Check for goal
    return 'S' in links[(0, n, 0, n_prime)]
