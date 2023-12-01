'''
Helper functions for the Local Search - Hill Climing

Includes both random restart and hill climbing optimization functions
'''
import random


# Function to initialize random TSP solution and generate random walk also used during Random Restart
def random_walk(locations, seed):
    """
    Generates a random walk through all nodes in the graph. Calculates the total 
    quality/distance. Used for both initialization and random restart for the Hill Climbing.

    Parameters:
    - locations: 2D Adjacecncy Matrix representing the graph
    - seed: Value to allow for consistent randomization results

    Returns:
    - quality: The sum of edge weights/distances between nodes in solution
    - ids: List of node ids representing TSP solution
    """
    quality, ids = 0, []
    visited = set()
    random.seed(seed)
    start = random.randint(0, len(locations)-1)
    ids.append(start)
    visited.add(start)
    for i in range(1, len(locations)):
        min_weight = float('inf')                           # Initialize distance to positive infinity
        next_location = None

        for j in range(len(locations)):                     # Loop through all potential edges for given node
            if j not in visited and locations[start][j] < min_weight:   
                min_weight = locations[start][j]    
                next_location = j                           # If distance is shorter than others store 

        ids.append(next_location)
        quality += min_weight
        visited.add(next_location)
        start = next_location                               # Add the node at the shortest distance from a given node as the next node in the solution
    quality += locations[start][ids[0]]                     # Add distance from final node back to starting point
    return quality, ids
    

# Function used to find neighboring solutions and choose optimal one
def hill_climbing(quality, ids, locations, seed):
    """
    Explores neighbors for a given solution and chooses if it has better quality.

    Parameters:
    - quality: Old quality
    - ids : Old solution
    - locations: 2D Adjacecncy Matrix representing the graph
    - seed: Value to allow for consistent randomization results

    Returns:
    - quality: The sum of edge weights/distances between nodes in solution
    - ids: List of node ids representing TSP solution
    """
    random.seed(seed)
    first = random.randint(0, len(ids)-1)
    second = random.randint(0, len(ids)-1)
    while second == first:
        second = random.randint(0, len(ids)-1)              # Initialize two unique random ids corresponding to nodes
    
    new_ids = ids.copy()
    new_ids[first] = ids[second]
    new_ids[second] = ids[first]                            # Switch the two nodes to generate a neighboring solution
    new_quality = 0
    for i in range(len(new_ids)-1):                         # Find quality of neighboring solution
        new_quality += locations[new_ids[i]][new_ids[i + 1]]
    new_quality += locations[new_ids[-1]][new_ids[0]]
    
    if new_quality < quality:                               # If neighboring solution is better than original accept, else reject
        return new_quality, new_ids
    else:
        return quality, ids