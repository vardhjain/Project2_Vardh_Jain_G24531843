import random
import time
import matplotlib.pyplot as plt
import math

# Merge two lists of Pareto-optimal points
def merge_pareto(left, right):
    merged = []
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    
    # Filter out dominated points from the merged list
    pareto_optimal = [merged[-1]]  # Start with the rightmost point
    for p in reversed(merged[:-1]):
        if p[1] > pareto_optimal[-1][1]:  # Keep only points that are not dominated
            pareto_optimal.append(p)
    
    return list(reversed(pareto_optimal))  # Reverse back to maintain sorting order


# Recursive function for divide and conquer
def divide_and_conquer_pareto(points):
    if len(points) == 1:
        return points
    
    mid = len(points) // 2
    left_points = divide_and_conquer_pareto(points[:mid])
    right_points = divide_and_conquer_pareto(points[mid:])
    
    return merge_pareto(left_points, right_points)


# Main function to compute Pareto-optimal points
def pareto_optimal_points(points):
    points = sorted(points, key=lambda p: (p[0], p[1]))
    return divide_and_conquer_pareto(points)


# Function to generate n random points
def generate_random_points(n):
    return [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(n)]


# Function to compare experimental and theoretical time complexity
def run_staircase_and_compare():
    ns = [100, 500, 2500, 12500, 62500, 312500, 1562500]
    experimental_times = []
    theoretical_times = []
    
    for n in ns:
        points = generate_random_points(n)
        
        # Measure the experimental time
        start_time = time.time()
        pareto_points = pareto_optimal_points(points)
        end_time = time.time()
        experimental_time = end_time - start_time
        experimental_times.append(experimental_time)
        
        # Calculate the theoretical time complexity O(n log n)
        theoretical_time = n * math.log(n)
        theoretical_times.append(theoretical_time)
        
        print(f"n = {n}, Experimental Time = {experimental_time:.10f} seconds")
    
    sum_experimental_times = sum(experimental_times)
    sum_theoretical_times = sum(theoretical_times)
    
    scaling_factor = sum_experimental_times / sum_theoretical_times 
    theoretical_times_scaled = [t * scaling_factor for t in theoretical_times]
    
    # Plot the experimental and theoretical times
    plt.figure(figsize=(10, 6))
    plt.plot(ns, experimental_times, label="Experimental Time", marker='o', color='blue')
    plt.plot(ns, theoretical_times_scaled, label="Theoretical Time (O(n log n))", marker='x', color='red', linestyle='--')
    
    plt.title("Experimental Time vs Theoretical Time Complexity (O(n log n))")
    plt.xlabel("n (Number of Points)")
    plt.ylabel("Time (seconds)")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    plt.show()


run_staircase_and_compare()
