import speech_recognition as sr
from queue import PriorityQueue
from subprocess import call
import RPi.GPIO as GPIO
import math
import time  
import zeroconf # DO: pip3 install zeroconf
import socket
import threading
import click
import signal
import sys



############ CLASS DEFINITIONS #########
class ServerSocket:
    MSGLEN = 512

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", 19400))
            self.sock.listen()

        else:
            self.sock = sock

    def accept(self):
        (conn, addr) = self.sock.accept()
        self.server_socket = conn

    def send(self, msg):
        totalsent = 0
        while totalsent < self.MSGLEN:
            try:
                sent = self.server_socket.send(msg[totalsent:].encode('utf-8'))
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
            except Exception as e:
                # print(f"An exception occurred: {e}")
                return

    def receive(self):
        chunks = []
        while True:
            # OK, I know, we are not going for efficiency here...
            chunk = self.server_socket.recv(1)

            chunks.append(chunk)
            if chunk == b'\n' or chunk == b'':
                break
        return b''.join(chunks).decode('utf-8')

    def close(self):
        try:
            self.sock.close()
            self.server_socket.close()
        except:
            print("Could not close all sockets")
            

class CommandHandler:

    class DriveValue:
        """
        This represents a drive value for either left or right control. Valid values are between -1.0 and 1.0
        """

        MAX = 1.0
        MIN = -1.0
        DELTA = .05

        value = 0.0

        def reset(self):
            self.value = 0.0
            return self.value

        def incr(self):
            self.value = min(self.MAX, self.value + self.DELTA)
            return self.value

        def decr(self):
            self.value = max(self.MIN, self.value - self.DELTA)
            return self.value

    left = DriveValue()
    right = DriveValue()

    def send_command(self, command):
        s_socket.send('{{command: {command} }}\n'.format(command=command))

    def send_drive_command(self, left, right):
        s_socket.send('{{driveCmd: {{l:{l}, r:{r} }} }}\n'.format(l=left, r=right))

    def stop_self(self):
        self.left = 0.0
        self.right = 0.0
        self.send_drive_command(self.left, self.right)

    def turn_left(self):
        self.send_drive_command(self.left.decr(), self.right.incr())

    def turn_right(self):
        self.send_drive_command(self.left.incr(), self.right.decr())

    def go_forward(self):
        self.send_drive_command(self.left.incr(), self.right.incr())

    def go_backward(self):
        self.send_drive_command(self.left.decr(), self.right.decr())

    def u_turn(self):
        self.left = -1.0
        self.right = 1.0
        self.send_drive_command(self.left, self.right)
        time.sleep(0.75)
        self.stop_self()


    def goleft(self):
        self.left = 0.0
        self.right = 1.0
        self.send_drive_command(self.left, self.right)
        time.sleep(0.65)
        self.stop_self()
    
    def goright(self):
        self.right = 0.0
        self.left = 1.0
        self.send_drive_command(self.left, self.right)
        time.sleep(0.65)
        self.stop_self()

    def godrive(self, leftval, rightval):
        self.left = leftval
        self.right = rightval
        self.send_drive_command(self.left, self.right)
        time.sleep(2)
        self.stop_self()

    def leftindicator(self):
        self.send_command("INDICATOR_LEFT")

    def rightindicator(self):
        self.send_command("INDICATOR_RIGHT")

    def stopindicator(self):
        self.send_command("INDICATOR_STOP")

    def networkmode(self):
        self.send_command("NETWORK")

    def drivemode(self):
        self.send_command("DRIVE_MODE")

    # def handle_keys(self):
    #     # keypad control codes
    #     K_PREFIX = '\x1b'
    #     K_RT = '[C'
    #     K_LF = '[D'
    #     K_UP = '[A'
    #     K_DN = '[B'

    #     while True:
    #         key = click.getchar()
    #         if key == K_PREFIX + K_RT: self.goright()
    #         if key == K_PREFIX + K_LF: self.goleft()
    #         if key == K_PREFIX + K_UP: self.godrive(1.0,1.0)
    #         if key == K_PREFIX + K_DN: self.godrive(-0.75,-0.75)
    #         if key == 'p': self.stop_self()
    #         if key == 'u': self.u_turn()
    #         if key == 'n': self.send_command("NOISE")
    #         if key == 'o': self.send_command("LOGS")
    #         if key == 'r': self.rightindicator()
    #         if key == 'l': self.leftindicator()
    #         if key == 's': self.send_command("INDICATOR_STOP")
    #         if key == 'e': self.networkmode()
    #         if key == 'd': self.send_command("DRIVE_MODE")
    #         if key == 'q':
    #             break



class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.status = "free_space";
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.status == "closed";

    def is_open(self):
        return self.status == "open";

    def is_barrier(self):
        return self.status == "barrier";

    def is_start(self):
        return self.status == "start";

    def is_end(self):
        return self.status == "end";

    def reset(self):
        self.status = "free_space";

    def make_start(self):
        self.status = "start";

    def make_closed(self):
        self.status = "closed";

    def make_open(self):
        self.status = "open";

    def make_barrier(self):
        self.status = "barrier";

    def make_end(self):
        self.status = "end";

    def make_path(self):
        self.status = "path";

    #def draw(self, win):
    #   pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False



############################################################################

### OPENBOT functions

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('1.2.3.4', 1))  # dummy connect
        return s.getsockname()[0]


def register(name, port, properties={}):
    type_="_openbot._tcp.local."

    ipAddr = socket.inet_pton(socket.AF_INET, get_ip())

    info = zeroconf.ServiceInfo(
        type_="_openbot._tcp.local.",
        name=name + '.' + type_,
        addresses=[ipAddr],
        port=port,
        weight=0,
        priority=0,
        properties=properties)

    zc = zeroconf.Zeroconf()
    zc.register_service(info)

    return (zc, info)

# def run_receiver ():
#     while True:
#         try:
#             data = s_socket.receive()
#             print(f'Received: {data}\r')
#         except:
#             break

# def print_usage():
#     usageStr = """
#     Usage: Use arrow keys (▲ ▼ ► ◄) on keyboard to drive robot.
#     Other keys:
#     \tn:    Toggle noise
#     \to:    Toggle logs
#     \tr:    Right direction indicator
#     \tl:    Left direction indicator
#     \tc:    Cancel indicators
#     \te:    Network mode
#     \td:    Drive mode
#     \tq:    Quit
#     """
#     print (usageStr)

# def run():
#     # print_usage()

#     print('Waiting for connection...\n')
#     s_socket.accept()
#     print('Connected! 😃\n')

    # t = threading.Thread(target=run_receiver)
    # t.start()

    # cmd_handler = CommandHandler ()
    # cmd_handler.handle_keys ()

    # s_socket.close()
    # zc.unregister_service(info)
    # zc.close()
    # print('Exiting...')
    
    
#Voice commands

def check_dest(voiceInput):
    coordinates = { 
        "bathroom": [11,24], 
        "elevator": [11,0], 
        "auditorium": [29,24],
        "fountain": [0,0],
        "202": [0,13],
        "exit": [16,0],
        "quit": [-1,-1],
        "entrance": [4,0],
        "shut": [-1,-1]
    } 

    voiceInput = voiceInput.lower()
    destinations = ["bathroom", "elevator", "auditorium", "entrance", "202", "quit", "exit", "fountain", "shut"]
    for d in destinations:
        if d in voiceInput:
            if d == "204":
                return [True, "Room " + d, coordinates.get(d)]
            elif d == "shut":
                return [True, "shut down", coordinates.get(d)]
            else:
                return [True, d, coordinates.get(d)]

    return [False, "Invalid", [0,0]]

def speakout(cmd):
	print(cmd)
	cmd = cmd.replace(' ', '_')
	call([cmd_beg+cmd+cmd_end], shell=True)

def get_destination_from_voice():
    while True: 
        #hard coded destination coordinates (check in a file probably)
        # obtain audio from the microphone
        #ask user for destination
        cmd = "Where do you want to go"
        speakout(cmd)

        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                cmd = (u"You said {}".format(value).encode("utf-8"))
                speakout(cmd)
            else:  # this version of Python uses unicode for strings (Python 3+)
                cmd = ("You said {}".format(value))
                speakout(cmd)
        except sr.UnknownValueError:
            cmd = "Oops Did not catch that"
            speakout(cmd)
        except sr.RequestError as e:
            cmd = ("Uh oh Could not request results from Google Speech Recognition service; {0}".format(e))
            cmd = cmd + " Please connect to Wi-fi"
            speakout(cmd)
        #check if destination exists in list of destinations
        #if no, re-ask else pathfinding 
        #returns list of [boolean, dest name, dest coordinates as tuple]
        dest = check_dest(cmd)
        if dest[0] == True:
            speakout("Going  to " + dest[1])
            break
        else:
            speakout("Invalid Destination, please try again")

    return dest[2]



################################################All functions needed for pathfinding + instruction generation###################################################################


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        #print(current.get_pos());
        generatedPath.append(current.get_pos());


def AstarAlgorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return False


def includePredefinedMap(grid):
    for j in range(3,24):
        grid[1][j].make_barrier();
        grid[24][j].make_barrier();
    for i in range(1,25):
        grid[i][3].make_barrier();
        grid[i][23].make_barrier();
    for i in range(0,30):
        grid[i][25].make_barrier();


def MakeInstruction(path, StartDirect):

        path_len = len(path) 
        print (path_len)

        move_list = []
        for i in range(path_len):
            #print(path[i])
            if i == 0:
                #d is the direction the robots faces in the start
                move_list.append(("Start",StartDirect)) 

            if (path[i][0] == path[i-1][0]) and (path[i][1] == (path[i-1][1] - 1)) and (i != 0): #North direction
                if move_list[i-1][1] == "N":
                    move_list.append(("A","N"))
                if move_list[i-1][1] == "E":
                    move_list.append(("L","N"))
                if move_list[i-1][1] == "W":
                    move_list.append(("R","N"))
                if move_list[i-1][1] == "S":
                    move_list.append(("B","N"))

            if (path[i][0] == path[i-1][0]) and (path[i][1] == (path[i-1][1] + 1)) and (i != 0): #South direction
                if move_list[i-1][1] == "S":
                    move_list.append(("A","S"))
                if move_list[i-1][1] == "W":
                    move_list.append(("L","S"))
                if move_list[i-1][1] == "E":
                    move_list.append(("R","S"))
                if move_list[i-1][1] == "N":
                    move_list.append(("B","S"))

            if (path[i][1] == path[i-1][1]) and (path[i][0] == (path[i-1][0] - 1)) and (i != 0): #West direction
                if move_list[i-1][1] == "W":
                    move_list.append(("A","W"))
                if move_list[i-1][1] == "N":
                    move_list.append(("L","W"))
                if move_list[i-1][1] == "S":
                    move_list.append(("R","W"))
                if move_list[i-1][1] == "E":
                    move_list.append(("B","W"))

            if (path[i][1] == path[i-1][1]) and (path[i][0] == (path[i-1][0] + 1)) and (i != 0): #East direction
                if move_list[i-1][1] == "E":
                    move_list.append(("A","E"))
                if move_list[i-1][1] == "N":
                    move_list.append(("R","E"))
                if move_list[i-1][1] == "S":
                    move_list.append(("L","E"))
                if move_list[i-1][1] == "W":
                    move_list.append(("B","E"))
        mod_move = []
        del move_list[0]
        count = 0
        lengt = len(move_list)
        #print(lengt)

        for i in range (lengt):
            if move_list[i][0] == 'R':
        #print("R")
        #mod_move.append(count)
                if(count != 0):
                    mod_move.append(count)
                    count = 0
                mod_move.append("R")
        #count = 0

            if move_list[i][0] == 'L':
        #print("L")
        #mod_move.append(count)
                if(count != 0):
                    mod_move.append(count)
                    count = 0
                mod_move.append("L")
        #count = 0

            if move_list[i][0] == 'B':
        #print("B")
        #mod_move.append(count)
                if(count != 0):
                    mod_move.append(count)
                    count = 0
                mod_move.append("B")
        #count = 0
            if move_list[i][0] == 'A':
        #print("S")
                count = count + 1

        if(count != 0):
            mod_move.append(count)

        #print(mod_move)
        return mod_move


def findPath(start,end,direction): #Generates both the path from the a-star algorithms and the instructions for the robot, so this is the only pathfinding-related function you need to call in the main while loop
    generatedPath.clear()
    rows = 30
    grid = []
    gap = 1
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    startingPoint = grid[start[0]][start[1]]
    startingPoint.make_start()
    destination = grid[end[0]][end[1]]
    destination.make_end()
    includePredefinedMap(grid)
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    AstarAlgorithm(grid, startingPoint, destination)

    generatedPath.reverse()
    generatedPath.append(destination.get_pos())
    invertedGeneratedPath = []
    for i in range(0,len(generatedPath)):
        invertedGeneratedPath.append((generatedPath[i][1],generatedPath[i][0]))
    #Convert coordinates to instructions 
    mod_move = MakeInstruction(invertedGeneratedPath,direction)
    return mod_move
    #print(mod_move);



##################################################################################################



########################
#SPeed sensor code 

# dist_meas = 0.00
# km_per_hour = 0
# rpm = 0
# elapse = 0
# sensor = 12
# pulse = 0
# start_timer = time.time()

# def init_GPIO():					# initialize GPIO
# 	GPIO.setmode(GPIO.BCM)
# 	GPIO.setwarnings(False)
# 	GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

# def calculate_elapse(channel):				# callback function
# 	global pulse, start_timer, elapse
# 	pulse+=1								# increase pulse by 1 whenever interrupt occurred
# 	elapse = time.time() - start_timer		# elapse for every 1 complete rotation made!
# 	start_timer = time.time()				# let current time equals to start_timer

# def calculate_speed(r_cm):
# 	global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
# 	if elapse !=0:							# to avoid DivisionByZero error
# 		rpm = 1/elapse * 60
# 		circ_cm = (2*math.pi)*r_cm			# calculate wheel circumference in CM
# 		dist_km = circ_cm/100000 			# convert cm to km
# 		km_per_sec = dist_km / elapse		# calculate KM/sec
# 		km_per_hour = km_per_sec * 3600		# calculate KM/h
# 		dist_meas = (dist_km*pulse)*1000	# measure distance traverse in meter
# 		return km_per_hour

# def init_interrupt():
# 	GPIO.add_event_detect(sensor, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)

# if __name__ == '__main__':
# 	init_GPIO()
# 	init_interrupt()
# 	while True:
# 		calculate_speed(20)	# call this function with wheel radius as parameter
#   		print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
# 		sleep(0.1)


#########################################

#Button Interrupt code


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

##### for pause button

def pause_button_callback(channel):
    global pause
    if GPIO.input(PAUSE_BUTTON_GPIO):
        print("Button pressed!, car paused")
        cmd = "Car paused"
        speakout(cmd)
        pause = True
    else:
        print("Button released!, car starting again")
        cmd = "Starting again"
        speakout(cmd)
        pause = False

#### for the speak button

def restart_button_callback(channel):
    global running
    global restart
    print("Car stopped")
    if running: # ignore reset if not running yet
        print("Button pressed!")
        cmd = "Restart True"
        speakout(cmd)
        restart = True

#### change current direction function  ####

def change_direction(turn):
    global curr_direction
    temp_dict = {'N':0, 'E':1, 'S':2, 'W':3}
    val = temp_dict[curr_direction]
    if turn == "B":
        val = (val + 2) % 4
    elif turn == "R":
        val = (val + 1) % 4
    elif turn == "L":
        val = (val + 3) % 4
    else:
        print("Something went wrong")
        
    for key in temp_dict:
        if temp_dict[key] == val:
            curr_direction = key
            # print(key)




####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

#MAIN FUNCTION


############GLOBAL VARIABLES############


PAUSE_BUTTON_GPIO = 22
RESTART_BUTTON_GPIO = 17
LEFT_MOTOR = 20
RIGHT_MOTOR = 21
count = 0
pause = False
restart = False
running = False
network_state = False
generatedPath = []
twoft = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR,GPIO.OUT)
GPIO.setup(RIGHT_MOTOR,GPIO.OUT)
GPIO.setup(RESTART_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PAUSE_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(RESTART_BUTTON_GPIO, GPIO.RISING, 
        callback=restart_button_callback, bouncetime=500)
GPIO.add_event_detect(PAUSE_BUTTON_GPIO, GPIO.BOTH, 
        callback=pause_button_callback, bouncetime=500)

signal.signal(signal.SIGINT, signal_handler)

GPIO.output(LEFT_MOTOR,GPIO.LOW)
GPIO.output(RIGHT_MOTOR,GPIO.LOW)


cmd_beg= 'espeak '
cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

r = sr.Recognizer()
m = sr.Microphone(device_index=2)


#connect to mic

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))

except KeyboardInterrupt:
    pass


#initializations
(zc, info) = register("OPEN_BOT_CONTROLLER", 19400)
s_socket = ServerSocket()

print('Waiting for connection...\n')
s_socket.accept()
print('Connected! 😃\n')

curr_coordinate = [0,0]
curr_direction = 'S'
cmd_handler = CommandHandler()
count = 0

while True:
    #keeps asking until we get a destination in dest. Dest is [T/F(ignore), RoomName, coordinates on x,y]
    dest_coordinate = get_destination_from_voice()
    if dest_coordinate == [-1,-1]:
        cmd = "Thank you for using Emphy. Hope you have a great day"
        speakout(cmd)
        break
        #exit program and emphy shuts down

    print("curr_coordinate")
    print(curr_coordinate)
    print("dest_coordinate")
    print(dest_coordinate)
    print(curr_direction)

    #This is in (column, row) format, not (row, column) format
    start = curr_coordinate #For example, these are the coordinates for the water fountain
    end = dest_coordinate #For example, these are the coordinates for the auditorium
    direction = curr_direction
    #findPath() function generates both the path from the a-star algorithms and the instructions for the robot, so this is the only pathfinding-related function you need to call in the main while loop
    mod_move = findPath(start,end, direction)
    print(mod_move)
    #move along instructions
    for move in mod_move:
        print(move)
        if move == 'B':
            change_direction("B")
            cmd = "Make a u turn"
            speakout(cmd)
            GPIO.output(LEFT_MOTOR,GPIO.HIGH)
            GPIO.output(RIGHT_MOTOR,GPIO.HIGH)
            cmd_handler.u_turn()
            print("New direction")
            print(curr_direction)
            GPIO.output(LEFT_MOTOR,GPIO.LOW)
            GPIO.output(RIGHT_MOTOR,GPIO.LOW)
        elif move == 'R':
            change_direction("R")
            cmd = "turn right"
            speakout(cmd)
            GPIO.output(RIGHT_MOTOR,GPIO.HIGH)
            cmd_handler.goright()
            print("New direction")
            print(curr_direction)
            GPIO.output(RIGHT_MOTOR,GPIO.LOW)
        elif move == 'L':
            change_direction("L")
            cmd = "turn left"
            speakout(cmd)
            GPIO.output(LEFT_MOTOR,GPIO.HIGH)
            cmd_handler.goleft()
            print("New direction")
            print(curr_direction)
            GPIO.output(LEFT_MOTOR,GPIO.LOW)
        else:
            time.sleep(0.75)
            cmd = "Going staight for " + str(move+move) + " ft"
            speakout(cmd)
            print(cmd)
            running = True
            count = 0
            #start moving
            if network_state == False:
                network_state = True
                cmd_handler.networkmode()
                print("turned network on!")
                print(network_state)

            while count <= move:
                if pause == True:
                    if network_state == True:
                        cmd_handler.networkmode()
                        network_state = False
                        running = False
                        print("turned network off!")
                    time.sleep(1)
                    continue
                
                if restart == True:
                    print("restarting 1")
                    if network_state == True:
                        print("restarting 2")
                        cmd_handler.networkmode()
                        network_state = False
                        running = False
                        print("turned network off!")
                    break
                
                count = count + 1
                if network_state == False:
                    network_state = True
                    running = True
                    cmd_handler.networkmode()
                    print("turned network on!")
                time.sleep(0.98)

            if network_state == True:
                cmd_handler.networkmode()
                network_state = False
                running = False

            if curr_direction == 'N':
                curr_coordinate[0] = curr_coordinate[0] - count
            elif curr_direction == 'E':
                curr_coordinate[1] = curr_coordinate[1] + count
            elif curr_direction == 'W':
                curr_coordinate[1] = curr_coordinate[1] - count
            elif curr_direction == 'S':
                curr_coordinate[0] = curr_coordinate[0] + count

            if restart == True:
                break


            # time.sleep(0.75)
            # print("Going staight for " + str(move) + " ft")
            # if network_state == False:
            #     network_state = True
            #     cmd_handler.networkmode()
            #     print("turned network on!")
            #     print(network_state)
            # time.sleep(move)
            # if network_state == True:
            #     network_state = False
            #     cmd_handler.networkmode()
            #     print("turned network off!")


    ## reached destination

    GPIO.output(LEFT_MOTOR,GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR,GPIO.HIGH)
    if restart:
        restart = False
    else:
        curr_coordinate = dest_coordinate
    cmd = "Reached destination."
    speakout(cmd)
    time.sleep(0.4)
    GPIO.output(LEFT_MOTOR,GPIO.LOW)
    GPIO.output(RIGHT_MOTOR,GPIO.LOW)


s_socket.close()
zc.unregister_service(info)
zc.close()
print('Exiting...')