
#main == main
import queue
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_north(self):
        return Car(self.x, self.y + 1)

    def move_south(self):
        return Car(self.x, self.y - 1)

    def move_east(self):
        return Car(self.x + 1, self.y)

    def move_west(self):
        return Car(self.x - 1, self.y)

    def move_northeast(self):
        return Car(self.x + 1, self.y + 1)

    def move_northwest(self):
        return Car(self.x - 1, self.y + 1)

    def move_southeast(self):
        return Car(self.x + 1, self.y - 1)

    def move_southwest(self):
        return Car(self.x - 1, self.y - 1)

    def display_position(self):
        print(f"Current position: ({self.x}, {self.y})")

    def distance_to_destination(self, destination):
        return ((self.x - destination.x) ** 2 + (self.y - destination.y) ** 2) ** 0.5




def currentMapDisplay(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            print(map[i][j], end = "")
        print()


def euclideanDistance(current, goal):
    return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5
def aStarSearch(map, goals, obstacles , currentpos):
    #obstackle array to store the goal when visited
    frontier = queue.PriorityQueue()
    nearestgoal = queue.PriorityQueue()
    start = currentpos
    frontier.put(start, 0)

    #for loop of goal array
    for goal in goals:
        #use euclidean distance
        distance = euclideanDistance(start, goal)
        nearestgoal.put(goal, distance)
    while not frontier.empty() and not nearestgoal.empty():
        current = frontier.get()
        goal = nearestgoal.queue[0]
        print("Goal is " + str(goal))
        # check if current node is in the array of goal
        if current == goal: #OR detected image
            #remove the goal from the array
            goals.remove(goal)
            nearestgoal.get()
            #append to obstacles
            obstacles.append(goal)
            frontier.put(goal)
            continue
            # return goals, obstacles,goal #current pos is the goal
        #move current towards goal
        #check which move is closer to goal
        #loop through all the moves
        #for loop 8 times
        car = Car(current[0], current[1])

        destination = Car(goal[0], goal[1])
        best_move = None
        best_distance = float('inf')

        for move in [car.move_north, car.move_south, car.move_east, car.move_west, car.move_northeast,
                     car.move_northwest,
                     car.move_southeast, car.move_southwest]:
            new_car = move()
            new_distance = new_car.distance_to_destination(destination)
            if new_distance < best_distance:
                best_distance = new_distance
                best_move = move

        print(f"Best move: {best_move.__name__}")
        car =best_move()
        currentpos[0] = car.x
        currentpos[1] = car.y
        car.display_position()
        frontier.put(currentpos, 0)


if __name__ == "__main__" :
    print("Enter the start point")
    #read map.txt
    f = open("map.txt", "r")
    #print
    # print(f.read())
    #store f into a 2d list named map
    map = [list(line.strip()) for line in f]


    #close the file
    f.close()
    #replace bottom left of the map with C
    map[4][0] ="C"
    #double for loop to print map
    currentMapDisplay(map)
    aStarSearch(map,[[3,2],[1,3]],[[]],[0,0])


