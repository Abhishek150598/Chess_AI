import pickle

#LOADING THE INITIAL BOARD SETUP
with open('initial_setup.pickle','rb') as f:
	board = pickle.load(f)

#LOADING PIECE DATA
with open('piece_data.pickle','rb') as f:
	piece_data = pickle.load(f)

#WHITE MOVES FIRST
turn = 'w'
wait = 'b'

#INITIAL POSITION OF THE KING
king_pos = {'w': (0,3), 'b': (7,3)}

#BOOLEAN VARIABLES INDICATING CHECK AND CHECKMATE
is_check = False
is_checkmate = False

#UTILITY FUNCTION THAT RETURNS PIECE AT THE COORDINATE (x,y)
def piece(x, y):
	return board[x][y][0]

#UTILITY FUNCTION THAT RETURNS PIECE AT THE COORDINATE (x,y)
def color(x, y):
	return board[x][y][1]

#UTILITY FUNCTION THAT RETURNS TRUE IF THE COORDINATE IS IN THE BOARD
def in_board(x, y):
	if x<0 or x>7 or y<0 or y>7:
		return False
	else:
		return True

#FUNCTION TO MOVE A PIECE FROM (x,y) TO (p,q)
def move(x, y, p, q):

    global turn, wait, is_check, is_checkmate
	#IF THE MOVED PIECE IS A KING, UPDATE THE KING_POS
    if(piece(x,y)=='k'):
        king_pos[turn] =(p,q)
    
    #CHANGE THE COORDINATES OF THE PIECE ON BOARD
    board[p][q] = board[x][y]
    board[x][y] = ('0','0')
    
    #CHANGE TURN
    temp = turn
    turn = wait
    wait = temp

#FUNCTION TO GET BOARD STATE
def get_board_state():
	return board, turn, is_check, is_checkmate

#FUNCTION TO GET ALL POSSIBLE MOVES FOR A PIECE AT (x,y)
def get_moves(x, y):

	p = piece(x,y)
	c = color(x,y)

	l =[]
	if c != turn:
		return l
    
	if p == 'p':
		if turn=='b':
			if piece(x+1,y)=='0':
				l.append((x+1,y))
				if x==1 and piece(x+2,y)=='0':
					l.append((x+2,y))
		elif turn=='w':
			if piece(x-1,y)=='0':
				l.append((x-1,y))
				if x==6 and piece(x-2,y)=='0':
					l.append((x-2,y))
	
	elif piece_data[p]['single_move']==True:
		for dir in piece_data[p]['dir']:
			i = x + dir[0]
			j = y + dir[1]
			if  in_board(i,j) and (color(i,j)==wait or piece(i,j)=='0'):
				l.append((i, j))

	elif piece_data[p]['single_move']==False:
		for dir in piece_data[p]['dir']:
			i = x
			j = y
			while True:
				i = i + dir[0]
				j = j + dir[1]
				if not in_board(i,j):
					break
				elif  piece(i,j)=='0':
					l.append((i, j))
				elif color(i,j)==wait:
					l.append((i, j))
					break
				else:
					break

	return l

def show_board():
	for i in range(8):
		for j in range(8):
			print(piece(i,j), end =" ")
		print("\n")