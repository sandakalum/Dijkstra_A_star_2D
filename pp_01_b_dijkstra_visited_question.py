# Dijkstra path planning.
# Second version: no algorithmic changes, but nicer visualization of cost.
# pp_01_b_dijkstra_visited
# (c) Claus Brenner, 15 JAN 2014
import numpy as np
import traceback
import gui
import common

# The world extents in units.
world_extents = (200, 150)

# The obstacle map.
# Obstacle = 255, free space = 0.
world_obstacles = np.zeros(world_extents, dtype=np.uint8)

# The array of visited cells during search.
visited_nodes = None

# The optimal path between start and goal. This is a list of (x,y) pairs.
optimal_path = []

# Functions for GUI functionality.
def add_obstacle(pos):
    common.set_obstacle(world_obstacles, pos, True)
    common.draw_background(gui, world_obstacles, visited_nodes, optimal_path)
def remove_obstacle(pos):
    common.set_obstacle(world_obstacles, pos, False)
    common.draw_background(gui, world_obstacles, visited_nodes, optimal_path)
def clear_obstacles():
    global world_obstacles
    world_obstacles = np.zeros(world_extents, dtype=np.uint8)
    update_callback()
def update_callback(pos = None):
    # Call path planning algorithm.
    start, goal = gui.get_start_goal()
    if not (start==None or goal==None):
        global optimal_path
        global visited_nodes
        try:
            optimal_path, visited_nodes = dijkstra(start, goal, world_obstacles)
        except Exception:
            print(traceback.print_exc())
    # Draw new background.
    common.draw_background(gui, world_obstacles, visited_nodes, optimal_path)

# --------------------------------------------------------------------------
# Dijkstra algorithm.
# --------------------------------------------------------------------------

# Allowed movements and costs on the grid.
# Each tuple is: (movement_x, movement_y, cost).
s2 = np.sqrt(2)
movements = [ # Direct neighbors (4N).
              (1,0, 1.), (0,1, 1.), (-1,0, 1.), (0,-1, 1.),
              # Diagonal neighbors.
              # Comment this out to play with 4N only (faster).
              (1,1, s2), (-1,1, s2), (-1,-1, s2), (1,-1, s2),
            ]

def dijkstra(start, goal, obstacles):
    """Dijkstra's algorithm, second versiion records cost in 'visited' array."""
    # In the beginning, the start is the only element in our front.
    # The first element is the cost of the path from the start to the point.
    # The second element is the position (cell) of the point.
    front = [ (0.0001, start) ]  # CHANGE 01_b: set the cost to e.g. 0.001

    # In the beginning, no cell has been visited.
    extents = obstacles.shape
    visited = np.zeros(extents, dtype=np.float32)

    # While there are elements to investigate in our front.
    while front:
        # Get smallest item and remove it from front.
        # CHANGE 01_a:
        element = min(front)# - Get smallest element from 'front'. Hint: min() may be useful.
        front.remove(element)# - Remove this element from 'front'. Hint: 'front' is a list.

        # Check if this has been visited already.
        cost, pos = element  # Change if you named 'element' differently.
        # CHANGE 01_a: Skip the rest of the loop body if visited[pos] is > 0.
        if visited[pos] > 0:
            continue

        # Now it is visited. Mark with cost.
        # CHANGE 01_b: set visited[pos] to cost instead of 1.
        visited[pos] = cost
        # Check if the goal has been reached.
        if pos == goal:
            break  # Finished!

        # Check all neighbors.
        for dx, dy, deltacost in movements:
            # Determine new position and check bounds.
            # CHANGE 01_a:
            (new_x) = pos[0] + (dx)# - Compute new_x and new_y from old position 'pos' and dx, dy.
            (new_y) = pos[1] + (dy)
            if (new_x >= 0) and (new_x < extents[0]) and (new_y >= 0) and (new_y < extents[1]):# - Check that new_x is >= 0 and < extents[0], similarly for new_y.
            # - If not, skip the remaining part of this loop.

                # Add to front if: not visited before and no obstacle.
                new_pos = (new_x, new_y)
                # CHANGE 01_a:
                if visited[new_pos]==0 and obstacles[new_pos] != 255:# If visited is 0 and obstacles is not 255 (both at new_pos), then:
                    front.append((cost + deltacost, new_pos))# append the tuple (cost + deltacost, new_pos) to the front.

    return ([], visited)


# Main program.
if __name__ == '__main__':
    # Link functions to buttons.
    callbacks = {"update": update_callback,
                 "button_1_press": add_obstacle,
                 "button_1_drag": add_obstacle,
                 "button_1_release": update_callback,
                 "button_2_press": remove_obstacle,
                 "button_2_drag": remove_obstacle,
                 "button_2_release": update_callback,
                 "button_3_press": remove_obstacle,
                 "button_3_drag": remove_obstacle,
                 "button_3_release": update_callback,
                 }
    # Extra buttons.
    buttons = [("Clear", clear_obstacles)]

    # Init GUI.
    gui = gui.GUI(world_extents, 4, callbacks,
                  buttons, "on",
                  "Simple Dijkstra Algorithm (now shows distances).")

    # Start GUI main loop.
    gui.run()
