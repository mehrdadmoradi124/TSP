"""
Brute Force algorithm for Traveling salesman problem
Author: Mehrdad Moradi

Main function in this file is brute_force_tsp(distances, time_limit) which gets 2d list of distances, and the time limit and returns best tour and distance
"""

import itertools
import time

def calculate_total_distance(tour, distances): #Function for calculating total distance of a tour. Distances is a 2d matrix which contains the distances between cities
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i + 1]]
    total_distance += distances[tour[-1]][tour[0]]  # Return to the starting city
    return total_distance

def brute_force_tsp(distances, time_limit):
    start_time = time.time()
    num_cities = len(distances)
    cities = list(range(num_cities))

    best_tour = None
    best_distance = float('inf')

    for perm in itertools.permutations(cities[1:):
        tour=[cities[0]]+list(perm)
        current_tour_distance = calculate_total_distance(tour, distances)
        if current_tour_distance < best_distance:
            best_distance = current_tour_distance
            best_tour = tour

        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            break

    return best_tour, best_distance

# Example usage:
if __name__ == "__main__":
    # Replace the distances matrix with your actual distances between cities
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    time_limit = 5  # 5 seconds as an example time limit

    best_tour, best_distance = brute_force_tsp(distances, time_limit)

    print("Best Tour:", best_tour)
    print("Best Distance:", best_distance)
