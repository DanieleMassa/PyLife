import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from collections import deque
from multiprocessing import Pool

# Create a "frames" folder if it doesn't already exist
if not os.path.exists("frames"):
    os.makedirs("frames")

# Grid dimensions and initial probability of a cell being alive
n = int(input("Enter the size of the square life grid: "))
p_alive = float(input("Enter the amount of life as a decimal number: "))

grid = np.random.choice([0, 1], size=(n, n), p=[1 - p_alive, p_alive])

# Circular queue to keep track of the last three frames
frame_history = deque(maxlen=3)

# Function to calculate the next state of the grid
def evolve(grid):
    new_grid = grid.copy()
    for i in range(n):
        for j in range(n):
            # Count the number of live neighbors
            neighbors = grid[i - 1:i + 2, j - 1:j + 2]
            alive_neighbors = np.sum(neighbors) - grid[i, j]

            # Apply the rules of the Game of Life
            if grid[i, j] == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if alive_neighbors == 3:
                    new_grid[i, j] = 1
    return new_grid

# Function to animate the grid evolution and save frames
def animate(frameNum, img, grid, n):
    new_grid = evolve(grid)
    img.set_data(new_grid)
    grid[:] = new_grid[:]

    # Save the current frame as a PNG image
    frame_filename = f"frames/frame_{frameNum:03d}.png"
    plt.imsave(frame_filename, new_grid, cmap='gray')

    # Add the new frame to the circular queue
    frame_history.append(new_grid)

    # Check if the last three frames are equal
    if len(frame_history) == 3 and all(np.array_equal(frame, frame_history[0]) for frame in frame_history):
        ani.event_source.stop()  # Stop the animation when frames are equal

    return img

# Create an animation using the Matplotlib library
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='gray')

if __name__ == "__main__":
    # Run the animation on all available cores (16 cores)
    with Pool(processes=16) as pool:
        ani = animation.FuncAnimation(fig, animate, fargs=(img, grid, n), frames=None, interval=1000 / 24)

    plt.show()
