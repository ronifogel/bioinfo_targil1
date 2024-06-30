# targil 1

import numpy as np
import tkinter as tk
# import matplotlib.pyplot as plt


# Initialize the Grid
def initialize_grid(size):
    """
    Initializes 80x80 grid with 50% of cells randomly assigned to 0 (white)
    and 50% to 1 (black).
    """
    grid = np.random.choice([0, 1], size=(size, size))
    return grid


# Define Non-Deterministic Rules
def update_cell(grid, x, y):
    """
    Applies non-deterministic rules to the cell to encourage the formation of
    alternating stripe patterns. Each cell's new state is determined by its
    neighbors and some randomness.
    """
    # Count horizontal neighbors (left and right)
    neighbors = [
        grid[(x - 1) % grid.shape[0], (y - 1) % grid.shape[1]],  # Top-left
        grid[(x - 1) % grid.shape[0], (y + 1) % grid.shape[1]],  # Top-right
        grid[x, (y - 1) % grid.shape[1]],  # Left
        grid[x, (y + 1) % grid.shape[1]],  # Right
        grid[(x + 1) % grid.shape[0], (y - 1) % grid.shape[1]],  # Bottom-left
        grid[(x + 1) % grid.shape[0], (y + 1) % grid.shape[1]]  # Bottom-right
    ]

    # Rule: Prefer alternating pattern based on majority of horizontal neighbors
    if neighbors.count(1) > neighbors.count(0):  # most of the neighbors is 1 - be 0
        return 0
    elif neighbors.count(0) > neighbors.count(1):  # most of the neighbors is 0 - be 1
        return 1
    else:
        # Count vertical neighbors
        neighbors = [
            grid[(x - 1) % grid.shape[0], y],  # Top
            grid[(x + 1) % grid.shape[0], y],  # Bottom
        ]

        if neighbors.count(1) > neighbors.count(0):  # most of the colum is 1 - be 1
            return 1
        elif neighbors.count(0) > neighbors.count(1):  # most of the colum is 0 - be 0
            return 0
        # else: return 0 # top differeent from bottom
        else:
            return np.random.choice([0, 1])  # top differeent from bottom


def update_grid(grid):
    """
    Applies non-deterministic rules to the update the cells grid to encourage the formation of
    alternating stripe patterns.
    """
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            new_grid[x, y] = update_cell(grid, x, y)
    return new_grid


# Define the Measurement Metric
def measure_pattern(grid):
    """
    Measures how close the rows is to an alternating pattern (either starting with 1 or 0).
    Both within rows and between consecutive rows.
    """
    total_score = 0
    row_count = grid.shape[0]
    col_count = grid.shape[1]

    # Measure alternating pattern within rows
    for x in range(row_count):  # Iterate over each row
        row = grid[x, :]
        # Count the number of consecutive elements that are different within the row
        row_score = np.sum(row[:-1] != row[1:])  # Compare indexes between row[0:n-1] to row[1:n]
        total_score += row_score
    # Measure similar pattern between pairs of consecutive rows
    for x in range(row_count - 1):
        row1 = grid[x, :]
        row2 = grid[x + 1, :]
        # Count the number of elements that are the same between consecutive rows
        row_score = np.sum(row1 == row2)
        total_score += row_score

    # Normalize the total score by the maximum possible score
    max_score_within_rows = row_count * (col_count - 1)  # the maximum score of within rows, each row has size-1 pairs
    max_score_between_rows = (
                                         row_count - 1) * col_count  # the maximum score of between rows, each colum has size-1 pairs
    max_score = max_score_within_rows + max_score_between_rows
    normalized_score = total_score / max_score  # Perfect score = 1
    return normalized_score


# Visualize the Progress with Tkinter
class CellularAutomatonVisualizer:
    """
    Class to present the cellular automaton visualizer
    """

    # constractor of the cellular automaton visualizer
    def __init__(self, root, grid_size):
        self.root = root
        self.grid_size = grid_size
        self.grid = initialize_grid(grid_size)  # initialize the cells grid random
        self.canvas = tk.Canvas(root, width=grid_size * 10, height=grid_size * 10)
        self.canvas.pack()
        self.draw_grid()  # present the first random generation

    # update the generation of the cellular automaton visualizer
    def update(self):
        self.grid = update_grid(self.grid)
        self.draw_grid()

    # present the cellular automaton visualizer grid
    def draw_grid(self):
        self.canvas.delete("all")  # delete the last generation
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                color = "black" if self.grid[x, y] == 1 else "white"
                self.canvas.create_rectangle(y * 10, x * 10, (y + 1) * 10, (x + 1) * 10, fill=color)


# Run and measure the progress Over Generations
def run_simulation(grid_size, generations):
    """
    Applies the simulation of the cellular automaton visualizer grid for 250 generations.
    """
    root = tk.Tk()
    visualizer = CellularAutomatonVisualizer(root, grid_size)  # initialize the cellular automaton visualizer
    pattern_scores = []  # for saving each generation score

    def run_generations(gen):
        if gen < generations:
            visualizer.update()  # update the next generation
            score = measure_pattern(visualizer.grid)
            pattern_scores.append(score)
            root.after(100, run_generations, gen + 1)  # Update every 100ms
        else:
            root.destroy()

    run_generations(0)  # start run_generation loop
    root.mainloop()
    return pattern_scores


# Run all the simulations and plot thier progress
if __name__ == "__main__":
    grid_size = 80
    generations = 250
    runs = 2
    all_pattern_scores = []

    # Run multiple simulations and save the pattern scores for each run
    for _ in range(runs):
        pattern_scores = run_simulation(grid_size, generations)
        all_pattern_scores.append(pattern_scores)

    # # Plot the progress over generations for each run
    # for i, pattern_scores in enumerate(all_pattern_scores):
    #     plt.plot(range(generations), pattern_scores, label=f'Run {i + 1}')
    #
    # plt.xlabel('Generation')
    # plt.ylabel('Stripe Score')
    # plt.title('Progress of Cellular Automaton')
    # plt.legend()
    # plt.show()