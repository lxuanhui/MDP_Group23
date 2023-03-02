import math
import os
import subprocess

import matplotlib.pyplot as plt
import heapq
import json
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
		self.order = []
		self.x = 1
		self.y = 2
		self.facing ="n" #update this is the movement

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
	def add_attribute(self, vertex, attribute, side, obstacleID):
		if attribute == 'obstacle':
			self.attributes[vertex] = {'obstacle': True, 'obstacleID': obstacleID}
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
		# get obstacleId
		obstacleID = self.attributes[obstacle_vertex]['obstacleID']
		if side == 'N':
			try:
				self.attributes[(row - 1, col + 1)]['wall'] = True
				self.attributes[(row + 1, col + 1)]['wall'] = True
				self.attributes[(row - 1, col + 2)]['wall'] = True
				self.attributes[(row + 1, col + 2)]['wall'] = True
				for neighbor in self.grid[(row - 1, col + 1)]:
					self.weights[((row - 1, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
				for neighbor in self.grid[(row + 1, col + 1)]:
					self.weights[((row + 1, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 1, col + 1))] = float('inf')
				for neighbor in self.grid[(row - 1, col + 2)]:
					self.weights[((row - 1, col + 2), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col + 2))] = float('inf')
				for neighbor in self.grid[(row + 1, col + 2)]:
					self.weights[((row + 1, col + 2), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 1, col + 2))] = float('inf')
				return ((row, col + 2),'S', obstacleID)
			except KeyError:
				if row - 1 < 0:
					self.attributes[(row + 1, col + 1)]['wall'] = True
					self.attributes[(row + 1, col + 2)]['wall'] = True
					for neighbor in self.grid[(row + 1, col + 1)]:
						self.weights[((row + 1, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 1, col + 1))] = float('inf')
					for neighbor in self.grid[(row + 1, col + 2)]:
						self.weights[((row + 1, col + 2), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 1, col + 2))] = float('inf')
					return ((row, col + 2), 'S', obstacleID)
				elif row + 1 >= 20 :
					self.attributes[(row - 1, col + 1)]['wall'] = True
					self.attributes[(row - 1, col + 2)]['wall'] = True
					for neighbor in self.grid[(row - 1, col + 1)]:
						self.weights[((row - 1, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
					for neighbor in self.grid[(row - 1, col + 2)]:
						self.weights[((row - 1, col + 2), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col + 2))] = float('inf')
					return ((row, col + 2), 'S', obstacleID)
		elif side == 'S':
			try:
				self.attributes[(row - 1, col - 2)]['wall'] = True
				self.attributes[(row + 1, col - 2)]['wall'] = True
				self.attributes[(row - 1, col - 3)]['wall'] = True
				self.attributes[(row + 1, col - 3)]['wall'] = True
				for neighbor in self.grid[(row - 1, col - 2)]:
					self.weights[((row - 1, col - 2), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col - 2))] = float('inf')
				for neighbor in self.grid[(row + 1, col - 2)]:
					self.weights[((row + 1, col - 2), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 1, col - 2))] = float('inf')
				for neighbor in self.grid[(row - 1, col - 3)]:
					self.weights[((row - 1, col - 3), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col - 3))] = float('inf')
				for neighbor in self.grid[(row + 1, col - 3)]:
					self.weights[((row + 1, col - 3), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 1, col - 3))] = float('inf')
				return ((row, col - 3),'N',	obstacleID)
			except KeyError:
				if row - 1 < 0:
					self.attributes[(row + 1, col - 2)]['wall'] = True
					self.attributes[(row + 1, col - 3)]['wall'] = True
					for neighbor in self.grid[(row + 1, col - 2)]:
						self.weights[((row + 1, col - 2), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 1, col - 2))] = float('inf')
					for neighbor in self.grid[(row + 1, col - 3)]:
						self.weights[((row + 1, col - 3), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 1, col - 3))] = float('inf')
					return ((row, col - 3), 'N', obstacleID)
				elif row + 1 >= 20:
					self.attributes[(row - 1, col - 2)]['wall'] = True
					self.attributes[(row - 1, col - 3)]['wall'] = True
					for neighbor in self.grid[(row - 1, col - 2)]:
						self.weights[((row - 1, col - 2), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col - 2))] = float('inf')
					for neighbor in self.grid[(row - 1, col - 3)]:
						self.weights[((row - 1, col - 3), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col - 3))] = float('inf')
					return ((row, col - 3), 'N', obstacleID)

		elif side == 'E':
			try:
				self.attributes[(row + 2, col + 1)]['wall'] = True
				self.attributes[(row + 2, col - 1)]['wall'] = True
				self.attributes[(row + 3, col + 1)]['wall'] = True
				self.attributes[(row + 3, col - 1)]['wall'] = True
				for neighbor in self.grid[(row + 2, col + 1)]:
					self.weights[((row + 2, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 2, col + 1))] = float('inf')
				for neighbor in self.grid[(row + 2, col - 1)]:
					self.weights[((row + 2, col - 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 2, col - 1))] = float('inf')
				for neighbor in self.grid[(row + 3, col + 1)]:
					self.weights[((row + 3, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 3, col + 1))] = float('inf')
				for neighbor in self.grid[(row + 3, col - 1)]:
					self.weights[((row + 3, col - 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row + 3, col - 1))] = float('inf')
				return ((row + 3, col), 'W', obstacleID)
			except KeyError:
				if col + 1 >= 21:
					self.attributes[(row + 2, col - 1)]['wall'] = True
					self.attributes[(row + 3, col - 1)]['wall'] = True
					for neighbor in self.grid[(row + 2, col - 1)]:
						self.weights[((row + 2, col - 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 2, col - 1))] = float('inf')
					for neighbor in self.grid[(row + 3, col - 1)]:
						self.weights[((row + 3, col - 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 3, col - 1))] = float('inf')
					return ((row + 3, col), 'W', obstacleID)
				elif col - 1 < 0:
					self.attributes[(row + 2, col + 1)]['wall'] = True
					self.attributes[(row + 3, col + 1)]['wall'] = True
					for neighbor in self.grid[(row + 2, col + 1)]:
						self.weights[((row + 2, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 2, col + 1))] = float('inf')
					for neighbor in self.grid[(row + 3, col + 1)]:
						self.weights[((row + 3, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row + 3, col + 1))] = float('inf')
					return ((row + 3, col), 'W', obstacleID)
		elif side == 'W':
			try:
				self.attributes[(row - 1, col + 1)]['wall'] = True
				self.attributes[(row - 1, col - 1)]['wall'] = True
				self.attributes[(row - 2, col + 1)]['wall'] = True
				self.attributes[(row - 2, col - 1)]['wall'] = True
				for neighbor in self.grid[(row - 1, col + 1)]:
					self.weights[((row - 1, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
				for neighbor in self.grid[(row - 1, col - 1)]:
					self.weights[((row - 1, col - 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 1, col - 1))] = float('inf')
				for neighbor in self.grid[(row - 2, col + 1)]:
					self.weights[((row - 2, col + 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 2, col + 1))] = float('inf')
				for neighbor in self.grid[(row - 2, col - 1)]:
					self.weights[((row - 2, col - 1), neighbor)] = float('inf')
					self.weights[(neighbor, (row - 2, col - 1))] = float('inf')
				return ((row - 2, col), 'E', obstacleID)
			except KeyError:
				if col + 1 >= 21:
					self.attributes[(row - 1, col - 1)]['wall'] = True
					self.attributes[(row - 2, col - 1)]['wall'] = True
					for neighbor in self.grid[(row - 1, col - 1)]:
						self.weights[((row - 1, col - 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col - 1))] = float('inf')
					for neighbor in self.grid[(row - 2, col - 1)]:
						self.weights[((row - 2, col - 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 2, col - 1))] = float('inf')
					return ((row - 2, col), 'E', obstacleID)
				elif col - 1 < 0:
					self.attributes[(row - 1, col + 1)]['wall'] = True
					self.attributes[(row - 2, col + 1)]['wall'] = True
					for neighbor in self.grid[(row - 1, col + 1)]:
						self.weights[((row - 1, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 1, col + 1))] = float('inf')
					for neighbor in self.grid[(row - 2, col + 1)]:
						self.weights[((row - 2, col + 1), neighbor)] = float('inf')
						self.weights[(neighbor, (row - 2, col + 1))] = float('inf')
					return ((row - 2, col), 'E', obstacleID)

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
		wall_x = []
		wall_y = []
		for vertex in self.grid.keys():
			if self.attributes.get(vertex, {}).get('obstacle'):
				obstacle_x.append(vertex[0])
				obstacle_y.append(vertex[1])
			elif self.attributes.get(vertex, {}).get('wall'):
				wall_x.append(vertex[0])
				wall_y.append(vertex[1])
			else:
				other_x.append(vertex[0])
				other_y.append(vertex[1])

		plt.scatter(obstacle_x, obstacle_y, s=10, c='r')
		plt.scatter(wall_x, wall_y, s=10, c='g')
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
			path = self.a_star(start, goal[0])
			if path is not None:
				paths.append(path)
		if paths:
			return min(paths, key=len)
		else:
			return None

	def a_star_search_multiple_obstacles(self, start, goals):

		final_path = []
		counter = 0
		# while counter < len(goals):
		while True:
			path = self.get_shortest_path(start, goals)
			# print("GPAL " , goals)
			# print(path)
			if path is None:
				break
			final_path.extend(path)
			start = path[-1]
			# goals.remove(path[-1])
			#look through goals to check if its same as start and remove it
			for i in range(len(goals)):
				if goals[i][0] == start:
					self.order.append(goals[i][2])
					goals.remove(goals[i])
					break
		return final_path

	# function to caluclate how many nodes traveled in a straight line before changing direction

	def summarize_path(self,path, goal_nodes):
		commands = []
		for i in range(len(path) - 1):
			x1, y1 = path[i]
			x2, y2 = path[i + 1]
			dx = x2 - x1
			dy = y2 - y1
			distance = math.sqrt(dx ** 2 + dy ** 2)
			if dy > 0 and abs(dy) >= abs(dx):
				direction = "n"
			elif dy < 0 and abs(dy) >= abs(dx):
				direction = "s"
			elif dx > 0 and abs(dx) >= abs(dy):
				direction = "e"
			elif dx < 0 and abs(dx) >= abs(dy):
				direction = "w"
			else:
				continue
			goalfound = False
			for g in goal_nodes:
				if path[i + 1] == g[0]:
					goal_nodes.remove(g)
					goalfound = True
					break
			if goalfound:
				commands.append([direction, round(distance, 2), "Reached obstacle: ",self.order[0]])
				del self.order[0]
			else:
				commands.append([direction, round(distance, 2), "Going to obstacle: ", self.order[0]])
		return commands

	def updatePosNfacing(self,movedist,direction,currentdir):
		if movedist ==0:
			movedist =1
		if currentdir == "n":
			if direction == "n":
				self.y += movedist #y increase
			elif direction == "s":
				self.y -= 1
				self.facing = "s"
			elif direction == "e":
				self.x += movedist
				self.facing = "e"
			elif direction == "w":
				self.x -= movedist
				self.facing = "w"
		elif currentdir == "s":
			if direction == "n":
				self.y += 1
				self.facing = "n"
			elif direction == "s":
				self.y -= movedist
			elif direction == "e":
				self.x += movedist
				self.facing = "e"
			elif direction == "w":
				self.x -= movedist
				self.facing = "w"
		elif currentdir == "e":
			if direction == "n":
				self.y += movedist
				self.facing = "n"
			elif direction == "s":
				self.y -= movedist
				self.facing = "s"
			elif direction == "e":
				self.x += movedist
			elif direction == "w":
				self.x -= 1
				self.facing = "w"
		elif currentdir == "w":
			if direction == "n":
				self.y += movedist
				self.facing = "n"
			elif direction == "s":
				self.y -= movedist
				self.facing = "s"
			elif direction == "e":
				self.x += 1
				self.facing = "e"
			elif direction == "w":
				self.x -= movedist
		else:
			print("Error in updatePosNfacing")
			print( currentdir, direction)
			# print("currentdir: ", currentdir)
			# print("direction: ", direction)
			# print("movedist: ", movedist)

	def movement_instructions(self, commands, current_direction):
		counter = 0
		instruction_list = []
		for command in commands:
			if command[0] == current_direction: #returns n s e w
				counter += 1
				if command[2] == "Reached obstacle: ":
					facing = self.facing
					self.updatePosNfacing(counter, facing,current_direction)
					facing = self.facing
					loc = "[" + str(self.x) +","+ str(self.y) +","+ str(facing) + "]"
					if counter <10:
						counter = "0"+str(counter)+"0)"
					else:
						counter = str(counter)+"0)"
					dictmove = {"movement": 'w'+counter, "obstacle": command[3],"reached":0, "robotPosition": loc}
					instruction_list.append(dictmove)
					dictmove = {"movement": "", "obstacle": command[3], "reached": 1, "robotPosition": loc}
					instruction_list.append(dictmove)
					current_direction = command[0]
					counter = 0

			else:

				if counter != 0:
					facing = self.facing
					self.updatePosNfacing(counter, facing,current_direction)  # force to increase the direction it was facing
					facing = self.facing
					loc = "[" + str(self.x) +","+ str(self.y) +","+ str(facing) + "]"
					if counter <10:
						counter = "0"+str(counter)+"0)"
					else:
						counter = str(counter)+"0)"
					dictmove = {"movement": 'w' + counter, "obstacle": command[3], "reached": 0, "robotPosition": loc}
					instruction_list.append(dictmove)
					# instruction_list.append(['W', counter, "Going to obstacle: ",command[3],loc,facing])

				self.updatePosNfacing(1, command[0], current_direction) #update base on the turn direction dist pass in is 1 because turning takes up 1 only
				facing = self.facing
				loc = "[" + str(self.x) +","+ str(self.y) +","+ str(facing) + "]"

				dictmove = {"movement": self.check_next_direction(current_direction, command[0]) + "010)", "obstacle": command[3], "reached": 0, "robotPosition": loc}
				instruction_list.append(dictmove)
				current_direction = command[0]
				# instruction_list.append([self.check_next_direction(current_direction, command[0]), '010)',"Going to obstacle: ",command[3],loc,facing])
				if command[2] == "Reached obstacle: ":
					# instruction_list.append(["Reached obstacle: ", command[3],loc,facing])
					dictmove = {"movement": "", "obstacle": command[3], "reached": 1, "robotPosition": loc}
					instruction_list.append(dictmove)
				counter = 0

		return instruction_list


	def check_next_direction(self, current_direction, next_direction):
		if current_direction == "n" and next_direction == "e":
			return "d"
		elif current_direction == "n" and next_direction == "w":
			return "a"
		elif current_direction == "s" and next_direction == "e":
			return "a"
		elif current_direction == "s" and next_direction == "w":
			return "d"
		elif current_direction == "e" and next_direction == "n":
			return "a"
		elif current_direction == "e" and next_direction == "s":
			return "d"
		elif current_direction == "w" and next_direction == "n":
			return "d"
		elif current_direction == "w" and next_direction == "s":
			return "a"
		else:
			#TODO make the reverse z or b. z is for clockwise and b is for anti clockwise
			if current_direction == "n" and self.x <= 2:
				return "z"
			elif current_direction == "n" and self.x >= 18:
				return "z"
			elif current_direction == "s" and self.x <= 2:
				return "b"
			elif current_direction == "s" and self.x >= 18:
				return "z"
			return "b"

grid = GridGraph(21, 21)
grid.add_attribute((1,12),'obstacle','S',1)
grid.add_attribute((14, 7), 'obstacle', 'W', 2)

grid.add_attribute((3, 4), 'obstacle', 'N', 3)
grid.add_attribute((14, 15), 'obstacle', 'W', 4)
path = grid.a_star_search_multiple_obstacles((0, 2), grid.get_goals(grid.get_obstacle_vertices()))
route = grid.movement_instructions(grid.summarize_path(path, grid.get_goals(grid.get_obstacle_vertices())), "n")
grid.plot(	path = grid.a_star_search_multiple_obstacles((0, 2), grid.get_goals(grid.get_obstacle_vertices())))

print (route)
# grid_graph.add_attribute((3, 8), 'obstacle', 'S', 1)
# grid_graph.add_attribute((3, 12), 'obstacle', 'N', 2)
# #
# grid_graph.add_attribute((3, 16), 'obstacle', 'S', 3)
# grid_graph.add_attribute((14, 7), 'obstacle', 'N', 4)
# grid_graph.add_attribute((6, 17), 'obstacle', 'W', 5)
# #
# grid_graph.add_attribute((16, 3), 'obstacle', 'W', 6)
# grid_graph.add_attribute((14, 18), 'obstacle', 'S', 7)
# grid_graph.add_attribute((18, 10), 'obstacle', 'W', 8)

# grid_graph.plot(path=grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(grid_graph.get_obstacle_vertices())))
#
# path = grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
# route = grid_graph.movement_instructions(
#     grid_graph.summarize_path(path, grid_graph.get_goals(grid_graph.get_obstacle_vertices())), "n")
#
# print (route)
# grid_graph = GridGraph(20, 20)
# grid_graph.add_attribute((3, 8), 'obstacle', 'S', 1)
# grid_graph.add_attribute((2, 12), 'obstacle', 'N', 2)
#
# grid_graph.add_attribute((3, 16), 'obstacle', 'S', 3)
# grid_graph.add_attribute((14, 7), 'obstacle', 'N', 4)
# grid_graph.add_attribute((6, 17), 'obstacle', 'W', 5)
#
# # print(grid_graph.get_obstacle_vertices())
# # print(grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
# # print(grid_graph.get_shortest_path((0, 0), grid_graph.get_obstacle_side_nodes(grid_graph.get_obstacle_vertices())))
# grid_graph.plot(	path=grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(grid_graph.get_obstacle_vertices())))
# # print(grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(
# # 	grid_graph.get_obstacle_vertices())))
#
# # print(grid_graph.get_edge_weights((13,8)))
# # print(grid_graph.get_edge_weights((14,6)))
# # print(grid_graph.get_edge_weights((15,6)))
# # print(grid_graph.get_edge_weights((15,7)))
#
# path = grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
# # threshold_angle = 45
# # print(grid_graph.order)
# # previous_direction = (1, 1)  # arbitrary initial value
# # for i in range(1, len(path)):
# # 	current_direction = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
# # 	turn_type = grid_graph.calculate_turn_type(previous_direction, current_direction, threshold_angle)
# # 	print(f"From {path[i - 1]} to {path[i]}: {turn_type}")
# # 	previous_direction = current_direction
# # print("sum = ",grid_graph.summarize_path(path, grid_graph.get_goals(grid_graph.get_obstacle_vertices())))
# route = grid_graph.movement_instructions(grid_graph.summarize_path(path,grid_graph.get_goals(grid_graph.get_obstacle_vertices())), "n")
# print(grid_graph.movement_instructions(grid_graph.summarize_path(path, grid_graph.get_goals(grid_graph.get_obstacle_vertices())), "n"))
#remove all instance of W, 0 in route
# print(route)
# route = [x for x in route if x != ['W', 0]]
# delim = "#"
# result = ''
# for i in route :
# 	result = result +str(i)+delim
# print(route)
# print(route)
# print(grid_graph.get_edge_weights((13,2)))
# data = '{"obstacle":[1,[5,12],"N"]}#{"obstacle":[2,[3,17],"S"]}'
# grid = GridGraph(21, 21)
# obstacleList = data.split("#")
# print(obstacleList)
# newObstacleList = []
# for obstacle in obstacleList:
# 	obstacle = eval(obstacle)
# 	newObstacleList.append(obstacle)
# print(newObstacleList)
# for obj in newObstacleList:
# 	grid.add_attribute((obj['obstacle'][1][0],obj['obstacle'][1][1]), "obstacle", obj['obstacle'][2], obj['obstacle'][0])
# path = grid.a_star_search_multiple_obstacles((0, 2), grid.get_goals(grid.get_obstacle_vertices()))
# route = grid.movement_instructions(grid.summarize_path(path, grid.get_goals(grid.get_obstacle_vertices())), "n")
# route = [x for x in route if x != ['W', 0]]

# # print(route)
#
#


