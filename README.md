# cse-6140-project
cse-6140-project

Members: 

## Local Search

### Explanation: Solution to TSP gievn 2D adjacency graph. Initialize a random solution by starting at a random node and finding nearest neighbors till it completes a Hamiltonian cycle. Optimize the solution by 'hill climbing' where you swap random nodes and recalculate the total edge cost in an attempt to find a better solution. If 'hill climbing' no longer improves quality then randomize a solution and compare in hopes of finding an improvement - this process is bounded by time hence will be finite. 

### Psuedocode: 
```python
def localSearchAlgorithm(adjacency_matrix):
    quality, route = Initialize random solution randomWalkFunction(adjacency_matrix)
    for a finite duration of time/iterations:
        new_route = Hill climb by swapping nodes swapNodes(route)
        new_quality = For the new route find it's quality findQuality(new_route)
        if new_quality < quality:
            quality = new_quality
            route = new_route
        elif new_route == route and new_quality == quality:
            random_quality, random_route = random_walk(adjacency_matrix, seed)
            if random_quality < quality:
                quality = random_quality
                route = random_route
        else:
            continue
    return quality, route
