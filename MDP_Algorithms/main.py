import pygame
import math
from Rpi import send_data
from utils import scale_image,blit_rotate_center
# from MDP_Simulator.Graph.graph import  a_star_search_multiple_obstacles, add_obstacle_attribute , get_goal_nodes,add_side_attribute, make_obstacle_edges_infinite,get_point_before_goal
from MDP_Simulator.Graph.graph_new import GridGraph

# Initialize pygame



# OBSTACLE_SCALE = 0.7 car scale was 0.7 to be 3x3
CAR_SCALE = 0.5
OBSTACLE_SCALE = 0.2
PIXEL_WIDTH = 20
# Set the window size
grid_width = 500
grid_height = 500
interval = 20
def to_pygame(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], height - coords[1])
def flipXYtopygameXY(x, y):
    p_y = abs(y - interval)
    return (x, p_y)
def pygameToXY(x, y):
    grid_x = x * (20 / grid_width)
    grid_y = (20 - (y * (20 / grid_height )))/2
    return (grid_x, grid_y)
def xyToPygame(x, y):
    pygame_x = x * (grid_width / 20)
    pygame_y = grid_height - (y *2 * (grid_height / 20))
    return (pygame_x, pygame_y)
pygame.init()

size = (grid_width, grid_height)
screen = pygame.display.set_mode(size)
#set background to white

pygame.display.set_caption("A* Pathfinding")

# Load the car image
car_image = scale_image(pygame.image.load("racecar.png"),CAR_SCALE)
obs = scale_image(pygame.image.load("img.png"), OBSTACLE_SCALE)
car_mask = pygame.mask.from_surface(car_image)
# Set the car's initial position
GRID2020 = 680
car_xy = to_pygame((0, 0), GRID2020)  #700 is the height of the grid
class Car:
    IMG = car_image
    START_POS = [2,339] #start at the bottom left
    # START_POS[0] = flipXYtopygameXY(10,15)[0]*PIXEL_WIDTH
    # START_POS[1] = flipXYtopygameXY(10,15)[1]*PIXEL_WIDTH
    def __init__(self, max_vel, rotational_vel,path,goal):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = max_vel
        self.rotational_vel = rotational_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.normalx, self.normaly = pygameToXY(self.x, self.y)
        self.acceleration = 0.1
        self.path = path
        self.currentpoint =0
        self.goal = goal
        self.goalcount = 0
        self.reversecounter =0

    def rotate(self,left=False,right=False):
        print("In rotate function")
        if left:
            self.angle += self.rotational_vel
            print("In left", self.angle)
        elif right:
            self.angle -= self.rotational_vel
        self.move()

    # def turn(self, direction): #creating a function so that it will turn to the nearest 90 degrees
    #     print("In turn function", direction,"  ", self.angle,"< angle before jump")
    #     print("While loop in turn function", int(self.angle % 90))
    #     if direction == 'left':
    #         self.angle += self.rotational_vel #shifting the angle abit so that the while loop will run
    #         while int(self.angle) % 90 != 0 and int(self.angle) % 90 != 1:
    #             print("While loop in turn function", int(self.angle % 90))
    #             self.rotate(left=True)
    #
    #     elif direction == 'right':
    #         print("In right")
    #         self.angle -= self.rotational_vel
    #         while self.angle % 90 != 0:
    #             print("While loop", self.angle % 90)
    #             self.rotate(right=True)

    def draw(self,screen):
        blit_rotate_center(screen,self.img,(self.x,self.y),self.angle)
        self.draw_points(screen)
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) #take the minimum value incase it over shot the speed
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel)
        self.move()
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal
    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration/2, 0)
        if self.vel<0:
            self.vel = min(self.vel + self.acceleration/2, 0)
        self.move()
    def collide(self, mask , x=0,y=0):
        car = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset) #point of intersection

        rect = self.img.get_rect()
        screen.set_at((rect.x + x, rect.y + y), (0, 0, 255))

            # Update the screen
        pygame.display.update()
        # #blitz the poi
        # if poi:
        #     print ("colide", pygameToXY(self.x,self.y))
            # pygame.draw.circle(screen, (255, 0, 255),(flipXYtopygameXY(*poi)[0]*PIXEL_WIDTH, flipXYtopygameXY(*poi)[1]*PIXEL_WIDTH ), 3)
            # pygame.display.update()
        return poi
    def bounce(self):
        self.vel = -self.vel
        self.move()

    def setpath(self,path):
        self.path = path
    def draw_points(self,screen):
        for point in self.path:
            pygame.draw.circle(screen,(255,0,0),(flipXYtopygameXY(*point)[0]* PIXEL_WIDTH,flipXYtopygameXY(*point)[1]* PIXEL_WIDTH),3)

    def calculate_angle(self):
        self.normalx, self.normaly = pygameToXY(self.x, self.y)
        target_x,target_y = self.path[self.currentpoint]
        # print(target_x,target_y)
        target_x = flipXYtopygameXY(target_x,target_y)[0]* PIXEL_WIDTH
        target_y = flipXYtopygameXY(target_x,target_y)[1]* PIXEL_WIDTH
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff ==0: #if the target is directly above or below the car
            desired_radian_anlge = math.pi/2
        else:
            desired_radian_anlge = math.atan(x_diff/y_diff)

        if target_y > self.y: #adding 180 degrees if the target is below the car
            desired_radian_anlge += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_anlge)   #difference in angle between the car and the target

        if difference_in_angle >= 180: #ensure dont take the long way around
            difference_in_angle -= 360
        if difference_in_angle <= -180:
            difference_in_angle += 360
        if self.vel >0:
            # send_data("W")
            # print("forward")
            if difference_in_angle > 0:
                # send_data("D")
                self.angle -= min(self.rotational_vel,
                                  abs(difference_in_angle))  # ensure the car doesnt rotate more than the rotational velocity which might over turn the vehicle
            elif difference_in_angle < 0:
                # send_data("A")
                self.angle += min(self.rotational_vel, abs(difference_in_angle))
        else:
            # send_data("S")
            self.vel = self.vel

    def update_path_point(self):
        target_x, target_y = self.path[self.currentpoint]
        target_x = flipXYtopygameXY(target_x, target_y)[0] * PIXEL_WIDTH
        target_y = flipXYtopygameXY(target_x, target_y)[1] * PIXEL_WIDTH
        # print("target",target_x,target_y, " Car " , (self.x,self.y))
        # print("COMPUTER POINT IS ",xyToPygame(target_x,target_y),  "CAR POINT IS ", (self.x,self.y))
        rect = pygame.Rect(self.x, self.y, self.img.get_width() *0.7 , self.img.get_height()*0.7 )
        pygame.draw.rect(screen, (255, 255, 0), rect, 2)

        pygame.display.update()
        # print(self.currentpoint)

        if rect.collidepoint(target_x,target_y):  #This is to collide with the rectangle around the car
        # if self.collide(car_mask, target_x, target_y):
            #remove the point from the list
            # current = self.path[self.currentpoint]
            del self.path[self.currentpoint]
            print("HIT")
            print('gol here',self.goal)
            # self.currentpoint += 1
            # next = self.path[self.currentpoint]

            #testing
            # self.goalcount +=1
            # if self.goalcount == 2:
            #     self.turn("left")

            #this is the old code where the car reaches the goal
            for g in self.goal:
                g_x = flipXYtopygameXY(g[0], g[1])[0] * PIXEL_WIDTH
                g_y = flipXYtopygameXY(g[0], g[1])[1] * PIXEL_WIDTH
                print("GOAL IS " ,g_x, g_y)
                print("Current point is " ,target_x,target_y)
                if g_x == target_x and g_y == target_y:
                    pygame.time.wait(200)
                    print("GOAL REACHED")
                    self.vel = -self.vel
                    self.goalcount +=1
                    # remove the goal from the list
                    self.goal.remove(g)
                    # self.turn("left")
                    # del self.path[self.currentpoint]



    def computermove(self):
        if self.currentpoint >= len(self.path):
            return
        if(self.vel>0):
            self.calculate_angle()
            self.update_path_point()
            self.move()

        if self.vel < 0: # let car reverse for a set amount of time. sel.vel only< 0 when hits goal
            self.move()
            self.reversecounter +=1
            if self.reversecounter > 60:
                self.vel = -self.vel
                print ("vel was negative")
                self.reversecounter = 0




def drawGrid(obstacles):# Draw the grid
        ob = scale_image(pygame.image.load("img.png"),0.4)
        for y in range(interval):
            for x in range(interval):
                rect = pygame.Rect(x*PIXEL_WIDTH, y*PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                if x <3 and y >16:
                    pygame.draw.rect(screen, (0, 255, 0), rect, 0)
                #check if x,y is in 2d array obstacles
                for obs in obstacles:
                    if obs[0][0] == x and obs[0][1] == y:
                        pygame.draw.rect(screen, (255, 0, 0), (
                        flipXYtopygameXY(*obs[0])[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs[0])[1] * PIXEL_WIDTH,
                        PIXEL_WIDTH, PIXEL_WIDTH))
                        # pygame.draw.triangle(screen, (0, 0, 255), (flipXYtopygameXY(*obs)[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs)[1] * PIXEL_WIDTH),
                        if obs[1] == "N":
                            blit_rotate_center (screen, ob, (flipXYtopygameXY(*obs[0])[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs[0])[1] * PIXEL_WIDTH), 180)
                        if obs[1] == "S":
                            blit_rotate_center (screen, ob, (flipXYtopygameXY(*obs[0])[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs[0])[1] * PIXEL_WIDTH), 0)
                        if obs[1] == "E":
                            blit_rotate_center (screen, ob, (flipXYtopygameXY(*obs[0])[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs[0])[1] * PIXEL_WIDTH), 90)
                        if obs[1] == "W":
                            blit_rotate_center (screen, ob, (flipXYtopygameXY(*obs[0])[0] * PIXEL_WIDTH, flipXYtopygameXY(*obs[0])[1] * PIXEL_WIDTH), 270)
def draw(screen,car):
        car.draw(screen)
        pygame.display.update()

def move_car(test_car):

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_a]:
            test_car.rotate(left=True)
        if keys[pygame.K_d]:
            test_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            test_car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            test_car.move_backward()
        if not moved:
            test_car.reduce_speed()

# Main game loop
FPS = 60
obstacle = [((15,19),"S"),((4,18),"S"),((5, 1), "N"), ((10, 4), "W"), ((17,12),"W")]
# obstacle = [((15,10),"S")]
grid_graph = GridGraph(20,20)
grid_graphgoal = GridGraph(20,20)
running = True
clock = pygame.time.Clock()

for obs in obstacle:
    grid_graph.add_attribute((obs[0][0],obs[0][1]),"obstacle",side = obs[1])
    grid_graphgoal.add_attribute((obs[0][0],obs[0][1]),"obstacle",side = obs[1])
    # add_obstacle_attribute(obs[0],obs[1])

# make_obstacle_edges_infinite()

# for obs in obstacle:
#     add_side_attribute(obs[0],obs[1])

goal = grid_graph.get_obstacle_side_nodes(grid_graph.get_obstacle_vertices())
goal_grid_graphgoal= grid_graphgoal.get_obstacle_side_nodes(grid_graphgoal.get_obstacle_vertices())
goalCar = goal
print("LIST OF GOALS",goalCar)
pointbeforegoal =[]

# for g in goal:
#     pointbeforegoal.append(get_point_before_goal(g))
    # if g['side'] == "E":
    #     pointbeforegoal.append((g[0][0]+2,g[0][1]))
    # elif g[1] == "W":
    #     pointbeforegoal.append((g[0][0]-1,g[0][1]))
    # elif g[1] == "N":
    #     pointbeforegoal.append((g[0][0],g[0][1]+1))
    # elif g[1] == "S":
    #     pointbeforegoal.append((g[0][0],g[0][1]-2))
path = grid_graph.a_star_search_multiple_obstacles((2,4) ,goal)
print("PATH",path)
# print("Points before goal " ,pointbeforegoal)
counter = 1
goalpath = []
test = 1
test_car = Car(0.6,2,path,goal_grid_graphgoal)  #Speed and turning speed path and stop point
print("GOAL after test car " , goal_grid_graphgoal)
Total_Time = 360000

while running:
    clock.tick(FPS)

    if Total_Time- pygame.time.get_ticks() < 0:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #press close
            running = False
            break

    screen.fill((255, 255, 255))
    drawGrid(obstacle)

    draw(screen, test_car)
    font = pygame.font.Font(None, 14)
    text = font.render("x: {:.2f} y: {:.2f}  Angle : {:.2f} Time left : {}".format(test_car.x, test_car.y, test_car.angle,Total_Time-pygame.time.get_ticks()), True, (0, 0, 0))

    screen.blit(text, (0, 21*PIXEL_WIDTH))

    test_car.computermove()

    # move_car(test_car)
    # if 0 == len(pointbeforegoal):
    #     test_car.angle=0
    #     print("TURNINGGGGGG")
    #     test_car.turn('right')

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Get the coordinates of the mouse click
        x, y = event.pos
        print(f'({x}, {y}) mouse clickmaps to grid coordinates ({pygameToXY(x, y)})')
        print(f'({pygameToXY(x, y)}) maps to pygame coordinates ({xyToPygame(pygameToXY(x, y)[0], pygameToXY(x, y)[1])})')
        print('0,0' + str(to_pygame((0, 0), GRID2020+90)),' xytopygame ' + str(xyToPygame(0,0)))

    #print("Car current position" , (test_car.x, test_car.y))
    # print(test_car.path)
# Clean up pygame
pygame.quit()

# print(f'({x}, {y}) maps to grid coordinates ({grid_x}, {grid_y})')
# obs1loc = xyToPygame(4,4.79)
# obs2loc = to_pygame((0, 0), GRID2020+90)
# blit_rotate_center(screen, obs, obs1loc, 0)
# blit_rotate_center(screen, obs, obs2loc, 90)
# move_car(test_car)
# if test_car.collide(obs_mask,*obs1loc) != None:
#     test_car.bounce()
#     print("Collision")
# if test_car.collide(obs_mask, *obs2loc) != None:
#     test_car.bounce()
#     print("Collision")
