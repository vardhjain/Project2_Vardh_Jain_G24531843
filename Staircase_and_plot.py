import random
import time
import matplotlib.pyplot as plt

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


def plot_points_and_pareto(points, pareto_points):
    points_x, points_y = zip(*points)
    pareto_x, pareto_y = zip(*pareto_points)
    
    plt.scatter(points_x, points_y, label="All Points", color="blue", s=10)
    
    plt.plot(pareto_x, pareto_y, label="Pareto-Optimal", color="red", marker='o', markersize=5, linestyle='--')
    
    plt.title(f"Pareto-Optimal Points and Random Points (n = {len(points)})")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.legend()
    plt.show()


def run_staircase_and_plot():
    ns = [100, 500, 2500, 12500, 62500, 312500, 1562500]
    
    for n in ns:
        points = generate_random_points(n)
        start_time = time.time()
        pareto_points = pareto_optimal_points(points)
        end_time = time.time()
        
        print(f"\nFor n = {n}, Time taken: {end_time - start_time:.5f} seconds")
        print(f"Pareto-optimal points (count = {len(pareto_points)})")
        
        plot_points_and_pareto(points, pareto_points)


# Run the experiment with plotting
run_staircase_and_plot()
