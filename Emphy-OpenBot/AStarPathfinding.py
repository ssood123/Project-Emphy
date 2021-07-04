import math
from queue import PriorityQueue

generatedPath = [];

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
	#	pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

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


def findPath(start,end):
	rows = 30;
	grid = []
	gap = 1;
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	startingPoint = grid[start[0]][start[1]];
	startingPoint.make_start();
	destination = grid[end[0]][end[1]];
	destination.make_end();
	includePredefinedMap(grid);
	for row in grid:
		for spot in row:
			spot.update_neighbors(grid)

	AstarAlgorithm(grid, startingPoint, destination)

	#After the algorithm finishes, print the grid and the generated path
	destination.make_path();
	for i in range(0,rows):
		for j in range(0,rows):
			if grid[i][j].status == "free_space":
				print(str(0),end=" ");
			elif grid[i][j].status == "barrier":
				print(str(1),end=" ");
			elif grid[i][j].status == "path":
				print("X",end=" ");
			elif grid[i][j].status == "start" or grid[i][j].status == "end":
				print(str(0),end=" ")
		print();

	generatedPath.reverse();
	generatedPath.append(destination.get_pos());
	invertedGeneratedPath = [];
	for i in range(0,len(generatedPath)):
		invertedGeneratedPath.append((generatedPath[i][1],generatedPath[i][0]));
	mod_move = MakeInstruction(invertedGeneratedPath,"N");
	print(mod_move);


def main():
	start = [0,0];
	end = [0,0];
	listOfSpecialPoints = [[0,0,"Water"],[0,11,"Classroom"],[11,0,"Elevator"],[12,24,"Bathroom"],[29,24,"Auditorium"]];
	startingRoom = "Water";
	endingRoom = "Classroom";
	for i in range(0,len(listOfSpecialPoints)):
		if listOfSpecialPoints[i][2] == startingRoom:
			start[0] = listOfSpecialPoints[i][0];
			start[1] = listOfSpecialPoints[i][1];
		if listOfSpecialPoints[i][2] == endingRoom:
			end[0] = listOfSpecialPoints[i][0];
			end[1] = listOfSpecialPoints[i][1];
	findPath(start, end);

main()