import math
import matplotlib.pyplot as plt
import heapq
#import from rpi.py file which is outside the directory
# from Rpi import send_data , receive_data



class GridGraph:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.grid = {}
		self.weights = {}
		self.default_weight = 10
		self.attributes = {}
		self.directions = {
			'N': (0, 1),
			'S': (0, -1),
			'W': (-1, 0),
			'E': (1, 0)
		}

		# Create vertices for each cell in the grid
		for row in range(self.rows):
			for col in range(self.cols):
				vertex = (row, col)
				self.grid[vertex] = []
				self.attributes[vertex] = {'obstacle': False, 'side': None, 'wall': False}

				# Connect the cell to its neighbors (up, down, left, right)
				for row_offset, col_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
					neighbor_row = row + row_offset
					neighbor_col = col + col_offset
					neighbor_vertex = (neighbor_row, neighbor_col)
					if (
							neighbor_row >= 0 and neighbor_row < self.rows and neighbor_col >= 0 and neighbor_col < self.cols):
						self.grid[vertex].append(neighbor_vertex)
						self.weights[(vertex, neighbor_vertex)] = self.default_weight

	# Add an attribute('Obstacle') to a vertex and the side of the target, also update the weights of the edges of the obstacle vertex to infinity
	def add_attribute(self, vertex, attribute, side):
		if attribute == 'obstacle':
			self.attributes[vertex] = {'obstacle': True}
			# self.attributes[vertex] = {'obstacleID': obstacleID}
			self.attributes[vertex[0] + 1, vertex[1]] = {'wall': True}
			self.attributes[vertex[0], vertex[1] - 1] = {'wall': True}
			self.attributes[vertex[0] + 1, vertex[1] - 1] = {'wall': True}
			if side:
				self.attributes[vertex]['side'] = side
			for neighbor in self.grid[vertex]:
				self.weights[(vertex, neighbor)] = float('inf')
				self.weights[(neighbor, vertex)] = float('inf')
			for neighbor in self.grid[vertex[0] + 1, vertex[1]]:
				self.weights[((vertex[0] + 1, vertex[1]), neighbor)] = float('inf')
				self.weights[(neighbor, (vertex[0] + 1, vertex[1]))] = float('inf')
			for neighbor in self.grid[vertex[0], vertex[1] - 1]:
				self.weights[((vertex[0], vertex[1] - 1), neighbor)] = float('inf')
				self.weights[(neighbor, (vertex[0], vertex[1] - 1))] = float('inf')
			for neighbor in self.grid[vertex[0] + 1, vertex[1] - 1]:
				self.weights[((vertex[0] + 1, vertex[1] - 1), neighbor)] = float('inf')
				self.weights[(neighbor, (vertex[0] + 1, vertex[1] - 1))] = float('inf')


	def get_edge_weights(self, vertex):
		edge_weights = {}
		for neighbor in self.grid[vertex]:
			edge = (vertex, neighbor)
			if edge in self.weights:
				edge_weights[neighbor] = self.weights[edge]
			else:
				edge_weights[neighbor] = self.default_weight
		return edge_weights

	def get_neighbors(self, vertex):
		return self.grid[vertex]

	def get_obstacle_side_node(self, obstacle_vertex):
		side = self.attributes[obstacle_vertex]['side']
		row, col = obstacle_vertex
		if side == 'N':
			self.attributes[(row - 1, col + 1)]['wall'] = True
			self.attributes[(row + 1, col + 1)]['wall'] = True
			for neighbor in self.grid[(row - 1, col + 1)]:
				self.weights[((row - 1, col + 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
			for neighbor in self.grid[(row + 1, col + 1)]:
				self.weights[((row + 1, col + 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row + 1, col + 1))] = float('inf')
			return (row, col + 1)
		elif side == 'S':
			self.attributes[(row - 1, col - 2)]['wall'] = True
			self.attributes[(row + 1, col - 2)]['wall'] = True
			for neighbor in self.grid[(row - 1, col - 2)]:
				self.weights[((row - 1, col - 2), neighbor)] = float('inf')
				self.weights[(neighbor, (row - 1, col - 2))] = float('inf')
			for neighbor in self.grid[(row + 1, col - 2)]:
				self.weights[((row + 1, col - 2), neighbor)] = float('inf')
				self.weights[(neighbor, (row + 1, col - 2))] = float('inf')
			return (row, col - 2)
		elif side == 'E':
			self.attributes[(row + 2, col + 1)]['wall'] = True
			self.attributes[(row + 2, col - 1)]['wall'] = True
			for neighbor in self.grid[(row + 2, col + 1)]:
				self.weights[((row + 2, col + 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row + 2, col + 1))] = float('inf')
			for neighbor in self.grid[(row + 2, col - 1)]:
				self.weights[((row + 2, col - 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row + 2, col - 1))] = float('inf')
			return (row + 2, col)
		elif side == 'W':
			self.attributes[(row - 1, col + 1)]['wall'] = True
			self.attributes[(row - 1, col - 1)]['wall'] = True
			for neighbor in self.grid[(row - 1, col + 1)]:
				self.weights[((row - 1, col + 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
			for neighbor in self.grid[(row - 1, col - 1)]:
				self.weights[((row - 1, col - 1), neighbor)] = float('inf')
				self.weights[(neighbor, (row - 1, col - 1))] = float('inf')
			return (row - 1, col)
		else:
			return None

	def get_goals(self, obstacle_vertices):
		return [self.get_obstacle_side_node(obstacle_vertex) for obstacle_vertex in obstacle_vertices]

	def get_obstacle_vertices(self):
		return [vertex for vertex, attributes in self.attributes.items() if attributes.get('obstacle')]

	def get_side_vertex(self, vertex):
		if 'side' in self.attributes[vertex]:
			side = self.attributes[vertex]['side']
			row_offset, col_offset = self.directions[side]
			return (vertex[0] + row_offset, vertex[1] + col_offset)
		else:
			return None

	def euclidean_distance(self, vertex1, vertex2):
		x1, y1 = vertex1
		x2, y2 = vertex2
		return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

	def manhattan_distance(self, vertex1, vertex2):
		x1, y1 = vertex1
		x2, y2 = vertex2
		return abs(x1 - x2) + abs(y1 - y2)

	def plot(self, path=None):
		x_coords = [vertex[0] for vertex in self.grid.keys()]
		y_coords = [vertex[1] for vertex in self.grid.keys()]

		for vertex, neighbors in self.grid.items():
			for neighbor in neighbors:
				x1, y1 = vertex
				x2, y2 = neighbor
				plt.plot([x1, x2], [y1, y2], 'k-', lw=0.5)

		if path is not None:
			path_x = [vertex[0] for vertex in path]
			path_y = [vertex[1] for vertex in path]
			plt.plot(path_x, path_y, 'r-', lw=2)

		obstacle_x = []
		obstacle_y = []
		other_x = []
		other_y = []
		for vertex in self.grid.keys():
			if self.attributes.get(vertex, {}).get('obstacle'):
				obstacle_x.append(vertex[0])
				obstacle_y.append(vertex[1])
			else:
				other_x.append(vertex[0])
				other_y.append(vertex[1])

		plt.scatter(obstacle_x, obstacle_y, s=10, c='r')
		plt.scatter(other_x, other_y, s=10, c='b')
		plt.xlim(-0.5, self.rows - 0.5)
		plt.ylim(-0.5, self.cols - 0.5)
		plt.show()

	def get_attributes(self, vertex):
		return self.attributes[vertex]

	def a_star(self, start, goal):
		def heuristic(vertex):
			return self.euclidean_distance(vertex, goal)

		visited = set()
		heap = [(0, start, None, None)]
		came_from = {}
		g_score = {start: 0}

		while heap:
			current_cost, current, previous, previous_direction = heapq.heappop(heap)
			if current == goal:
				return self.reconstruct_path(came_from, start, current)
			visited.add(current)
			for neighbor in self.grid[current]:
				if neighbor in visited:
					continue
				cost = g_score[current] + self.weights.get((current, neighbor), self.default_weight)
				direction = (neighbor[0] - current[0], neighbor[1] - current[1])
				if previous is not None and direction != previous_direction:
					cost += 2
				if neighbor not in g_score or cost < g_score[neighbor]:
					g_score[neighbor] = cost
					priority = cost + heuristic(neighbor)
					heapq.heappush(heap, (priority, neighbor, current, direction))
					came_from[neighbor] = current
		return None

	def reconstruct_path(self, came_from, start, current):
		path = [current]
		while current != start:
			current = came_from[current]
			path.append(current)
		return list(reversed(path))

	# loop a_star search for each obstacle side node and return the shortest path
	def get_shortest_path(self, start, goals):
		paths = []
		for goal in goals:
			path = self.a_star(start, goal)
			if path is not None:
				paths.append(path)
		if paths:
			return min(paths, key=len)
		else:
			return None

	def a_star_search_multiple_obstacles(self, start, goals):

		final_path = []
		while True:
			path = self.get_shortest_path(start, goals)
			if path is None:
				break
			final_path.extend(path)
			start = path[-1]
			goals.remove(path[-1])
		return final_path

	# function to caluclate how many nodes traveled in a straight line before changing direction

	def summarize_path(self,path):
		commands = []
		for i in range(len(path) - 1):
			x1, y1 = path[i]
			x2, y2 = path[i + 1]
			dx = x2 - x1
			dy = y2 - y1
			distance = math.sqrt(dx ** 2 + dy ** 2)
			if dy > 0 and abs(dy) >= abs(dx):
				direction = "North"
			elif dy < 0 and abs(dy) >= abs(dx):
				direction = "South"
			elif dx > 0 and abs(dx) >= abs(dy):
				direction = "East"
			elif dx < 0 and abs(dx) >= abs(dy):
				direction = "West"
			else:
				continue
			commands.append([direction, round(distance, 2)])
		return commands

	def movement_instructions(self, commands, current_direction):
		counter = 0
		instruction_list = []
		for command in commands:
			if command[0] == current_direction:
				counter += 1
			else:
				instruction_list.append(['W', counter])
				instruction_list.append([self.check_next_direction(current_direction, command[0]), 1])
				current_direction = command[0]
				counter = 0
		return instruction_list


	def check_next_direction(self, current_direction, next_direction):
		if current_direction == "North" and next_direction == "East":
			return "Right"
		elif current_direction == "North" and next_direction == "West":
			return "Left"
		elif current_direction == "South" and next_direction == "East":
			return "Left"
		elif current_direction == "South" and next_direction == "West":
			return "Right"
		elif current_direction == "East" and next_direction == "North":
			return "Left"
		elif current_direction == "East" and next_direction == "South":
			return "Right"
		elif current_direction == "West" and next_direction == "North":
			return "Right"
		elif current_direction == "West" and next_direction == "South":
			return "Left"
		else:
			return "180 Turn"

# '[[1,(4,3),"N']- ]

grid_graph = GridGraph(20, 20)
grid_graph.add_attribute((18, 5), 'obstacle', side='W')
grid_graph.add_attribute((2, 7), 'obstacle', side='N')
grid_graph.add_attribute((12, 17), 'obstacle', side='W')
grid_graph.add_attribute((10, 5), 'obstacle', side='S')
grid_graph.add_attribute((14, 7), 'obstacle', side='N')
grid_graph.add_attribute((6, 17), 'obstacle', side='W')

print(grid_graph.get_obstacle_vertices())
print(grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
# print(grid_graph.get_shortest_path((0, 0), grid_graph.get_obstacle_side_nodes(grid_graph.get_obstacle_vertices())))
grid_graph.plot(
	path=grid_graph.a_star_search_multiple_obstacles((0, 0), grid_graph.get_goals(grid_graph.get_obstacle_vertices())))
print(grid_graph.a_star_search_multiple_obstacles((0, 0), grid_graph.get_goals(
	grid_graph.get_obstacle_vertices())))

print(grid_graph.get_edge_weights((13,8)))
print(grid_graph.get_edge_weights((14,6)))
print(grid_graph.get_edge_weights((15,6)))
print(grid_graph.get_edge_weights((15,7)))

path = grid_graph.a_star_search_multiple_obstacles((0, 0), grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
# threshold_angle = 45
# previous_direction = (1, 1)  # arbitrary initial value
# for i in range(1, len(path)):
# 	current_direction = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
# 	turn_type = grid_graph.calculate_turn_type(previous_direction, current_direction, threshold_angle)
# 	print(f"From {path[i - 1]} to {path[i]}: {turn_type}")
# 	previous_direction = current_direction
print(grid_graph.summarize_path(path))
route = grid_graph.movement_instructions(grid_graph.summarize_path(path), "North")
print(grid_graph.movement_instructions(grid_graph.summarize_path(path), "North"))
#remove all instance of W, 0 in route
route = [x for x in route if x != ['W', 0]]
print(route)
obs = receive_data('0.0.0.0',12345)
print("FROM RPI " , obs)
send_data(route)
