import argparse
import time

from LocalTSPhelper import random_walk, hill_climbing
# import multiprocessing - for use in timing if we can't figure out another way

def exact(adjacency_matrix):
    pass

def approximate_search(adjacency_matrix):
    pass


def local_search(adjacency_matrix, time_limit, seed):
    """
    Performs a local search for TSP, problem is represented by an 2D adjacency matrix.
    Utilized random resets and 'hill climbing' (optimization based on neighborhood function) 
    to improve on initial solution. To track how the model optimizes a solution uncomment 
    the lines marked in the function. Helper functions used can be found in the LocalTSPHelper.py 
    funciton. Randomization seeds are used and updated thorughout to generate repeatable but unique numbers.

    Parameters:
    - adjacency_matrix: Represents the graph
    - time_limit: The maximum duration (in seconds) for the search to run
    - seed: Value to allow for consistent randomization results

    Returns:
    - quality: The sum of edge weights/distances between nodes in solution
    - ids: List of node ids representing TSP solution
    """
    start_time = time.time()
    quality, ids = random_walk(adjacency_matrix, seed)                              # Create a random preliminary solution
    # print(quality) # Uncomment this to see starting quality score
    while True:
        if time.time() - start_time >= time_limit:
            break
        old_quality, old_ids = quality, ids
        seed += 1
        hquality, hids = hill_climbing(quality, ids, adjacency_matrix, seed)        # Find neighboring solutions and accept if quality is better
        if hquality < quality:
            # print('Improved from:' + quality + " to " + hquality) # Uncomment this to see how hill climbing improves quality
            quality = hquality
            ids = hids
        if old_ids == ids and quality == old_quality:
            seed += 1
            random_quality, random_ids = random_walk(adjacency_matrix, seed)        # If local minima has been reached try random reset, accept if quality is better   
            if random_quality < quality:
                quality = random_quality
                ids = random_ids
                # print(quality) # Uncomment this line to track how often ransom reset improves quality
    # print(quality) # Uncomment this to see final quality score
    return quality, ids

def euclidean_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    return round(distance)

def construct_graph(locations):
    adjacency_matrix = [[0 for i in range(len(locations))] for j in range(len(locations))]
    for i in range(len(locations)):
        for j in range(len(locations)):
            if i == j:
                adjacency_matrix[i][j] = 0
            else:
                adjacency_matrix[i][j] = euclidean_distance(locations[i], locations[j])
    return adjacency_matrix

def tsp_parser(inst):
    locations = []
    with open('data/' + inst, 'r') as file:
        for line in file:
            words = line.split()
            if len(words) == 0:
                pass
            elif words[0] == 'NAME:':
                city = words[1]
            elif words[0] == 'DIMENSION:':
                dimension = words[1]
            elif words[0] == 'EDGE_WEIGHT_TYPE:':
                edge_weight_type = words[1]
            elif words[0].isdigit():
                id, x, y = words
                locations.append((float(x), float(y)))
            else:
                pass
    return city, dimension, edge_weight_type, locations

def generate_solution(file_name, quality, ids):
    lines = [quality, ids]
    with open(file_name + ".sol", 'w') as file:
        for line in lines:
            file.write(str(line) + "\n")
        

def main(inst, alg, time, seed):
    # parse the .TSP file create 2D adjacency matrix for graph representation
    city, dimension, edge_weight_type, locations = tsp_parser(inst)
    adjacency_matrix = construct_graph(locations)
    # print(adjacency_matrix)
    if alg == 'BF':
        quality, ids = exact(adjacency_matrix)
        file_name = str(city) + "_" + str(alg) + "_" + str(time)
        generate_solution(file_name, quality, ids)
    elif alg == 'Approx':
        quality, ids  = approximate_search(adjacency_matrix)
        file_name = str(city) + "_" + str(alg) + "_" + str(seed)
        generate_solution(file_name, quality, ids)
    elif alg == 'LS':
        quality, ids  = local_search(adjacency_matrix, int(time), int(seed))
        file_name = str(city) + "_" + str(alg) + "_" + str(time) + "_" + str(seed)
        generate_solution(file_name, quality, ids)
        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', required=True)
    parser.add_argument('-alg', required=True, choices=['BF', 'Approx', 'LS'])
    parser.add_argument('-time', required=True, type=int)
    parser.add_argument('-seed', type=int)
    args = parser.parse_args()
    main(args.inst, args.alg, args.time, args.seed)



# python tsp.py -inst Atlanta.tsp -alg LS -time 600 -seed 42
# python tsp.py -inst UKansasState.tsp -alg LS -time 10 -seed 42
# python tsp.py -inst Berlin.tsp -alg LS -time 30 -seed 42     

# created a working executable with PyInststaller
# tsp.exe -inst Atlanta.tsp -alg LS -time 600 -seed 42
