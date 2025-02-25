from robot import Robot_Sim
from utils import *
import math

def get_wheel_velocities(robbie, coord):
    """
    Helper function to determine the velocities of the robot's left and right wheels.
    Arguments:
        robbie: instance of the robot
        coord (tuple): coordinate to move to (x,y)
    
    Returns: 
        vr, vl: velocities of the robot's left and right wheels
    """

    # Calculate the desired change in position
    dx_world = coord[0] - robbie.x
    dy_world = coord[1] - robbie.y
    dx_robot, dy_robot = rotate_point(dx_world, dy_world, robbie.h)
    dist_to_coord = math.sqrt(dx_robot**2 + dy_robot**2)
    
    # Turn in place first
    angle = math.atan2(dy_robot, dx_robot)
    threshold = 0.1
    if angle < -threshold:
        return -0.01, 0.01
    elif angle > threshold:
        return 0.01, -0.01
    
    # Using desired linear velocity, set left and right wheel velocity
    linear_v = 0.05 * dist_to_coord
    w = 0.3 * math.atan2(dy_robot, dx_robot)
    vl = (linear_v - robbie.wheel_dist / 2 * w) 
    vr = (linear_v + robbie.wheel_dist / 2 * w)    
    return vr, vl


def get_neighbors(cell):
    """
    Get neighbors of a given cell
    """
    return [
        (cell[0]+1, cell[1]),
        (cell[0]-1, cell[1]),
        (cell[0], cell[1]+1),
        (cell[0], cell[1]-1)
    ]


def frontier_planning(robbie, grid):
    """
        Function for defining frontier planning.

        Arguments:
            robbie: instance of the robot
            grid: instance of the grid

        Returns:
            robbie: 'updated' instance of the robot
            OPTIONAL: robbie.next_coord: new destination coordinate

        Notes:
            The lecture notes should provide you with an ample description of frontier planning.
            You will also find many of the functions declared in 'grid.py' and 'utils.py' useful.

    """
    ## TODO: STUDENT CODE START ##

    # Get all frontier cells based on what's adjacent to explored cells and not an obstacle
    
    # Separate the adjacenct cells into separate frontiers

    # Compute the centroids of the frontiers
    
    # Pick a centroid based on some heuristic such as sorting the centroids based on their distances to the robbie's current position
    
    # Choose the centroid which is not same as robot's position and the centoid is not in obstacle
    
    # In case no centroid is chosen, pick a random point from the frontier
    
    ## STUDENT CODE END ##
        # Step 1: Identify all frontier cells
    frontier_cells = []
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.is_free(x, y) and (x, y) not in robbie.explored_cells:
                # Check if the current cell has neighboring explored cells that are free
                neighbors = get_neighbors((x, y))
                if any((nx, ny) in robbie.explored_cells and grid.is_free(nx, ny) for nx, ny in neighbors):
                    frontier_cells.append((x, y))

    # Step 2: Group frontier cells into clusters using the helper function
    clusters = separate_adjacent_coordinates(frontier_cells, grid)

    # Step 3: Compute centroids of each cluster
    centroids = [find_centroid(cluster) for cluster in clusters if cluster]

    # Step 4: Sort centroids by distance to the robot's current position
    centroids.sort(key=lambda c: grid_distance(robbie.x, robbie.y, c[0], c[1]))

    # Step 5: Select the first reachable centroid using RRT or another path validation method
    for centroid in centroids:
        path = grid.rrt((robbie.x, robbie.y), centroid)
        if path:  # If a path is found, set this as the next target
            robbie.next_coord = centroid
            break
    else:
        # Optional: if no centroids are reachable, either choose a random frontier or do nothing
        if frontier_cells:
            robbie.next_coord = random.choice(frontier_cells)
        else:
            robbie.next_coord = None

    return robbie, robbie.next_coord


def exploration_state_machine(robbie, grid):
    """
    Use frontier planning, or another exploration algorithm, to explore the grid.

    Arguments:
        robbie: instance of the robot
        grid: instance of the grid

    Returns: 
        robbie: 'updated' instance of the robot

    Notes:
        Robot is considered as Point object located at the center of the traingle. 
        Robot explores the map in the discretized space
        You may use the 'rrt' function (see grid.py) to find a new path whenever the robot encounters an obstacle.
        Please note that the use of rrt slows down your code, so it should be used sparingly.
        The 'get_wheel_velocities' functions is useful in setting the robot's velocities.
        You will also find many of the functions declared in 'grid.py' and 'utils.py' useful.
        Feel free to create other helper functions (in this file) as necessary.

    Alert:
        In this part, the task is to let the robot find all markers by exploring the map,
        which means using 'grid.markers' will lead  cause zero point on GraderScope.

    """
    ### TODO: STUDENT CODE START ###

        
    # Sensing: Get the free space in robot's current FOV
    
    # Planning: If you do not know robbie's next coordinate or have already reached it, 
    # run your choice of exploration to get robbie's next coordinate
    
    
    # If moving to next coordinate results in a collision, then perform RRT and set that as the next coord. 
 
    # Now that you know the next coordinate, set Robbie's wheel velocities
    

    ### STUDENT CODE END ###
   # Define a small threshold distance to determine if the robot is "close enough" to its target
    close_enough_threshold = 0.5  # Adjust based on your grid scale and movement resolution

    # Calculate the distance to the next coordinate if it exists
    if robbie.next_coord:
        distance_to_next = math.sqrt((robbie.x - robbie.next_coord[0])**2 + (robbie.y - robbie.next_coord[1])**2)
    else:
        distance_to_next = float('inf')  # Infinite distance if there is no next coordinate

    # Only consider a new destination if the robot is close to the current next_coord or does not have one
    if robbie.next_coord is None or distance_to_next < close_enough_threshold:
        robbie, robbie.next_coord = frontier_planning(robbie, grid)

    # Check if the path to the next coordinate is obstructed, if so, use RRT to find a path
    if robbie.next_coord and grid.is_collision_with_obstacles((robbie.x, robbie.y), robbie.next_coord):
        path = grid.rrt((robbie.x, robbie.y), robbie.next_coord)
        if path and len(path) > 1:
            robbie.next_coord = path[1]  # the second node in the path after the start node

    # Set the robot's wheel velocities based on the current or updated next coordinate
    if robbie.next_coord:
        vr, vl = get_wheel_velocities(robbie, robbie.next_coord)
        # Assume robot class has methods to set velocities directly
        robbie.vr = vr
        robbie.vl = vl
    return robbie
