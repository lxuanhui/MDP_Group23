
import json
import socket
import subprocess
from time import sleep
from graph_new import GridGraph
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,8192)
host = socket.gethostbyname(socket.gethostname())
# host = socket.gethostbyname("")
port = 1234
print(host)
print(port)
serversocket.bind((host, port))

serversocket.listen(5)
print('server started and listening')
while 1:
    (clientsocket, address) = serversocket.accept()
    print(address)
    print("connection found!")
    no = clientsocket.recv(1024)
    data = no.decode()

    print("rec",data)
    print(type(data))
    print(no)
    grid = GridGraph(21, 21)
    obstacleList = data.split("^")
    print("OBS List " ,type(obstacleList))
    newList = []
    for obstacle in obstacleList:
        newList.append(eval(obstacle))
        print("obstacle",type(obstacle))
    for obj in newList:
        print("in for loop ", obj)
        print(type(obj),obj['obstacle'][1][0],obj['obstacle'][1][1]+1)
        grid.add_attribute((obj['obstacle'][1][0],obj['obstacle'][1][1]+1), "obstacle", obj['obstacle'][2], obj['obstacle'][0])

    # grid.add_attribute((3,12),'obstacle','S',1)
    # grid.add_attribute((14, 7), 'obstacle', 'W', 2)
    #
    # grid.add_attribute((8, 4), 'obstacle', 'N', 3)
    # grid.add_attribute((14, 15), 'obstacle', 'W', 4)



    path = grid.a_star_search_multiple_obstacles((1, 2), grid.get_goals(grid.get_obstacle_vertices()))
    route = grid.movement_instructions(grid.summarize_path(path, grid.get_goals(grid.get_obstacle_vertices())), "n")

    grid.plot(path)
    print(path)
    print(route)
    # path = []
    # dict ={'movement': 'a010)', 'obstacle': 2, 'reached': 0, 'robotPosition': [16, 12, 'n']}
    # path.append(dict)
    # dict2 ={'movement': 'd010)', 'obstacle': 2, 'reached': 0, 'robotPosition': [16, 12, 'n']}
    # print(route)

    # path.append(dict2)
    # path.append(dict)
    # path.append(dict2)
    # path.append(dict)
    # route = path
    with open('route.json', 'w') as outfile:
        json.dump(route, outfile)

    with open('route.json', 'r') as f:
        data = json.load(f)
        # print(data)

    p = subprocess.Popen(["scp", "route.json", "mdp-group23@192.168.23.23:/home/mdp-group23/Desktop"])
    sts = p.wait()
    x = json.dumps(route)
    clientsocket.send(x.encode())
    print("SENT")


    # result = "[{'movement': 'w020)', 'obstacle: ': 1, 'reached': 0, 'robotPosition': [1, 4, 'North']}, {'movement': 'd010)', 'obstacle: ': 1, 'reached': 0, 'robotPosition': [2, 4, 'East']}"

    # result = list({"movement": "w020)", "obstacle": 1, "reached": 0, "robotPosition": [1, 4, "North"]}, {"movement": "d010)", "obstacle": 1, "reached": 0, "robotPosition": [2, 4, "East"]})
    # grid_graph = GridGraph(20, 20)
    # grid_graph.add_attribute((3, 8), 'obstacle', 'S', 1)
    # grid_graph.add_attribute((3, 12), 'obstacle', 'N', 2)
    # #
    # grid_graph.add_attribute((3, 16), 'obstacle', 'S', 3)
    # grid_graph.add_attribute((14, 7), 'obstacle', 'N', 4)
    # grid_graph.add_attribute((6, 17), 'obstacle', 'W', 5)
    # #
    # # grid_graph.add_attribute((16, 3), 'obstacle', 'W', 6)
    # # grid_graph.add_attribute((14, 18), 'obstacle', 'S', 7)
    # # grid_graph.add_attribute((18, 10), 'obstacle', 'W', 8)
    #
    # grid.plot(path=grid.a_star_search_multiple_obstacles((1, 2), grid.get_goals(grid.get_obstacle_vertices())))
    #
    # path = grid_graph.a_star_search_multiple_obstacles((1, 2), grid_graph.get_goals(grid_graph.get_obstacle_vertices()))
    # route = grid_graph.movement_instructions(
    #     grid_graph.summarize_path(path, grid_graph.get_goals(grid_graph.get_obstacle_vertices())), "North")
