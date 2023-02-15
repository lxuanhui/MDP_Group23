import networkx as nx
from matplotlib import pyplot as plt
import math

# TODO Create a Graph class so that the obstacles etc can be added dynamically

# Creates the 20x20 grid
G = nx.grid_2d_graph(20, 20)

# pre-processing - set all nodes to car,obstacle = false, side = none
nx.set_node_attributes(G, False, 'car')
nx.set_node_attributes(G, False, 'obstacle')
nx.set_node_attributes(G, None, 'side')
nx.set_node_attributes(G, False, 'goal')

# Method to test if the nodes in the graph has a certain attribute
# blue_nodes = [node for node in G.nodes() if G.nodes[node]['car'] == True]
#     print(blue_nodes)


## Gets all neighbors of a node
# neighbours = nx.all_neighbors(G,(0,0))
# for i in neighbours:
#     print(i)


#Set weight of all North/South/East/West edges - uses actual distance
for edge in G.edges:
    G.edges[edge]['weight'] = 10


# Function to calculate the euclidean distance between two points
def euclidean_distance_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# function to calculate manhattan distance between two points
def manhattan_distance_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = abs(x2 - x1) + abs(y2 - y1)
    return distance
# function to get nodes that are diagonal to the obsatacle node
def get_diagonal_nodes(obstacle_node):
    diagonal_nodes = []
    for node in G.nodes:
        if node[0] == obstacle_node[0] + 1 and node[1] == obstacle_node[1] + 1:
            diagonal_nodes.append(node)
        if node[0] == obstacle_node[0] - 1 and node[1] == obstacle_node[1] + 1:
            diagonal_nodes.append(node)
        if node[0] == obstacle_node[0] + 1 and node[1] == obstacle_node[1] - 1:
            diagonal_nodes.append(node)
        if node[0] == obstacle_node[0] - 1 and node[1] == obstacle_node[1] - 1:
            diagonal_nodes.append(node)
    return diagonal_nodes
# Function to add obstacle attribute to the nodes
def add_obstacle_attribute(obstacle_node, side):
    #set the obstacle attribute to true
    nx.set_node_attributes(G, {obstacle_node: True}, 'obstacle')
    nx.set_node_attributes(G, {obstacle_node: True}, 'goal')
    #set all surrounding nodes to obstacle = true
    #get all neighbors of the obstacle node
    neighbors = nx.all_neighbors(G, obstacle_node)
    for neighbor in neighbors:
        nx.set_node_attributes(G, {neighbor: True}, 'obstacle')
    #get the node that is on the side of the obstacle
    if side == "N":
        neighbor_node = (obstacle_node[0] , obstacle_node[1] + 1)
    if side == "S":
        neighbor_node = (obstacle_node[0] , obstacle_node[1] - 1)
    if side == "E":
        neighbor_node = (obstacle_node[0] + 1, obstacle_node[1])
    if side == "W":
        neighbor_node = (obstacle_node[0] - 1, obstacle_node[1])
    # set this node to obstacle = false
    nx.set_node_attributes(G, {neighbor_node: False}, 'obstacle')
    diagonal_nods = get_diagonal_nodes(obstacle_node)
    for diagonal_node in diagonal_nods:
        nx.set_node_attributes(G, {diagonal_node: True}, 'obstacle')



#function to make all edges of the obstacle node to infinity
# def make_edges_infinite(obstacle_node):
#     #get all neighbors of the obstacle node
#     neighbors = nx.all_neighbors(G, obstacle_node)
#     for neighbor in neighbors:
#         G.edges[obstacle_node, neighbor]['weight'] = float('inf')
#     #set all diagonal edges of the obstacle node to infinity
#     #get diagonal edges of the obstacle node
#     diagonal_edges = []
#     for edge in G.edges:
#         if edge[0][0] == obstacle_node[0] + 1 and edge[0][1] == obstacle_node[1] + 1:
#             diagonal_edges.append(edge)
#         if edge[0][0] == obstacle_node[0] - 1 and edge[0][1] == obstacle_node[1] + 1:
#             diagonal_edges.append(edge)
#         if edge[0][0] == obstacle_node[0] + 1 and edge[0][1] == obstacle_node[1] - 1:
#             diagonal_edges.append(edge)
#         if edge[0][0] == obstacle_node[0] - 1 and edge[0][1] == obstacle_node[1] - 1:
#             diagonal_edges.append(edge)
#     #set diagonal edges to infinity
#     for diagonal_edge in diagonal_edges:
#         G.edges[diagonal_edge]['weight'] = float('inf')



#function to make all obstacle edges to infinity
def make_obstacle_edges_infinite():
    for edge in G.edges:
        if G.nodes[edge[0]]['obstacle'] == True or G.nodes[edge[1]]['obstacle'] == True:
            G.edges[edge]['weight'] = float('inf')

# add_obstacle_attribute((5, 5), "N")
# add_obstacle_attribute((10, 12), "S")
# add_obstacle_attribute((15, 9), "E")
# add_obstacle_attribute((18, 18), "W")
# add_obstacle_attribute((8, 17), "N")
# make_obstacle_edges_infinite()

def remove_weight(obstacle_node, side):
    if side == "N":
        neighbor_node = (obstacle_node[0] , obstacle_node[1] + 1)
    if side == "S":
        neighbor_node = (obstacle_node[0] , obstacle_node[1] - 1)
    if side == "E":
        neighbor_node = (obstacle_node[0] + 1, obstacle_node[1])
    if side == "W":
        neighbor_node = (obstacle_node[0] - 1, obstacle_node[1])
    G.edges[obstacle_node, neighbor_node]['weight'] = 10

# Function to add side attribute to the nodes - determines which side of the obstacle the car has to face
def add_side_attribute(obstacle_node, side):
    #get node's obstacle attribute value
    obstacle_value = G.nodes[obstacle_node]['obstacle']
    #if the node is an obstacle
    if obstacle_value == True:
        #set the side attribute to the side of the obstacle the car has to face
        nx.set_node_attributes(G, {obstacle_node: side}, 'side')

        #get the neighbours of the obstacle node
        neighbours = nx.all_neighbors(G, obstacle_node)
        #set the weight of the edges to infinity for the neighbours of the obstacle node
        for i in neighbours:
            G.edges[obstacle_node, i]['weight'] = float('inf')
        remove_weight(obstacle_node, side)
    else:
        print("Not an obstacle")

# add_side_attribute((5, 5), 'N')
# add_side_attribute((10, 12), 'S')
# add_side_attribute((15, 9), 'E')
# add_side_attribute((18, 18), 'W')
# add_side_attribute((8, 17), 'N')




# print("obstacle", G.edges[(5, 5), (5, 6)]['weight'])
# print("obstacle", G.edges[(5, 5), (4, 5)]['weight'])
# print("obstacle", G.edges[(5, 5), (5, 4)]['weight'])
# print("obstacle", G.edges[(5, 5), (6, 5)]['weight'])

#TODO: Navigating around the obstacle when the visual marker is scanned
# Scan until target is detected then run A* search again to the rest of the goals


# Position of car - update the position whenever the car moves
car_position = (1, 1)


def get_car_nodes(car_position):
    car = []
    car_nodes_dict = {}
    neighbours = nx.all_neighbors(G, car_position)
    car.append(car_position)
    car_nodes_dict[car_position] = True
    for i in neighbours:
        car.append(i)
        car_nodes_dict[i] = True
        nx.set_node_attributes(G, car_nodes_dict, 'car')
    return car

# Function to get the obstacle nodes
def get_goal_nodes():
    goal_nodes = [node for node in G.nodes() if G.nodes[node]['goal'] == True]
    return goal_nodes

# A* search from current car position to goal - parameters should be nodes (x,y)
def a_star_search(current_position, goal_position):
    #get side attribute of the goal node
    side = G.nodes[goal_position]['side']
    #get the node on the side of the goal node
    if side == "N":
        gp = (goal_position[0], goal_position[1] + 1)
    if side == "S":
        gp = (goal_position[0], goal_position[1] - 2)
    if side == "E":
        gp = (goal_position[0] + 2, goal_position[1])
    if side == "W":
        gp = (goal_position[0] - 1, goal_position[1])
    print("GOAL POSITION IS ", goal_position)
    path = nx.astar_path(G, current_position, gp, heuristic=manhattan_distance_2d, weight='weight')

    #ADDBACK THE GOAL NODE TO THE PATH
    goal =()

    path.append(tuple(goal_position))
    return path

# a_star_path = a_star_search()
# print(a_star_search())
def get_point_before_goal(goal_position):
    side = G.nodes[goal_position]['side']
    #get the node on the side of the goal node
    if side == "N":
        gp = (goal_position[0], goal_position[1] + 1)
    if side == "S":
        gp = (goal_position[0], goal_position[1] - 2)
    if side == "E":
        gp = (goal_position[0] + 2, goal_position[1])
    if side == "W":
        gp = (goal_position[0] - 1, goal_position[1])
    return gp

# A* search from current car position to multiple goals
def a_star_search_multiple_obstacles(car_start_position, goal_list):
    total_path = []
    node = car_start_position

    while(len(goal_list) > 0):
        list_of_paths = []
        for i in goal_list:
            path = a_star_search(node, i)
            #pick the shortest path from the list of paths
            list_of_paths.append(path)
        shortest_path = min(list_of_paths, key=len)
        try:
            while True:
                shortest_path.remove(node)
        except ValueError:
            pass
        print("shortest path is ", shortest_path)
        #add the shortest path to the total path
        print("Start from " , node)
        total_path.extend(shortest_path)
        print(total_path, len(goal_list))
        node = shortest_path[-1]
        goal_list.remove(node)

        #remove the goal node from the list of goals
        try:
            while True:
                total_path.remove(node)
        except ValueError:
            pass
        node = shortest_path[-1]
            # total_path.remove(node)
        print(total_path, len(goal_list))
    return total_path



# goal_nodes = get_goal_nodes()
# print("OBSTACLE NODES ARE " , goal_nodes)
# car_nodes = get_car_nodes(car_position)
# total_path = a_star_search_multiple_obstacles((1,1), goal_nodes)
# print("total",total_path)
# # Draws and generates the Grid
# plt.figure(figsize=(80, 80))
# pos = {(x, y): (x, y) for x, y in G.nodes()}
# nx.draw(G, pos=pos,
#         node_color='grey',
#         with_labels=True,
#         node_size=10)
# # Draws the car
# nx.draw(G, pos, nodelist=car_nodes, node_color='red', with_labels=True)
#
# nx.draw(G, pos, nodelist=total_path, node_color='green', with_labels=True)
# nx.draw(G, pos, nodelist=goal_nodes, node_color='blue', with_labels=True)
#
# plt.show()
