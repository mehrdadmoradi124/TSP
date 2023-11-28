import argparse
import time
# import multiprocessing

def exact(adjacency_matrix):
    pass

def approximate_search(adjacency_matrix):
    pass

def local_search(adjacency_matrix):
    pass

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
            if words[0] == 'NAME:':
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

def main(inst, alg, time, seed):
    # parse the .TSP file create 2D adjacency matrix for graph representation
    city, dimension, edge_weight_type, locations = tsp_parser(inst)
    adjacency_matrix = construct_graph(locations)
    print(adjacency_matrix)
    if alg == 'BF':
        output = exact(adjacency_matrix)
    elif alg == 'Approx':
        output = approximate_search(adjacency_matrix)
    elif alg == 'LS':
        output = local_search(adjacency_matrix, seed)
        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', required=True)
    parser.add_argument('-alg', required=True, choices=['BF', 'Approx', 'LS'])
    parser.add_argument('-time', required=True, type=int)
    parser.add_argument('-seed', type=int)
    args = parser.parse_args()
    main(args.inst, args.alg, args.time, args.seed)


# python tsp.py -inst Atlanta.tsp -alg LS -time 600 -seed 42

# created a working executable with PyInststaller
# tsp.exe -inst Atlanta.tsp -alg LS -time 600 -seed 42
