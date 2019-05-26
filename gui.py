import pygame
import time
import string
import chessboard

pygame.init()

# INITIALISING THE GAME CONSTANTS
display_width = 750
display_height = 700
board_height = 560
board_width = 560
cell_height = 70
cell_width = 70
boardX = 40
boardY = 40
black = (0, 0, 0)
green = (13, 99, 5)
white = (226, 195, 147)
blue = (8, 51, 119)
red = (204 , 28, 12)
bg = (255, 255, 255)
d = 15	#Distance between board and board label
l = list(string.ascii_uppercase[0:8]) 	#Uppercase alphabet list for board labelling

chess_pieces = {'b':{'k':'blackKing.png','q':'blackQueen.png','r':'blackRook.png','b':'blackBishop.png','n':'blackKnight.png','p':'blackPawn.png'},'w':{'k':'whiteKing.png','q':'whiteQueen.png','r':'whiteRook.png','b':'whiteBishop.png','n':'whiteKnight.png','p':'whitePawn.png'}}

piece_img ={}

for color in chess_pieces:
	piece_img[color] = {}
	for piece in chess_pieces[color]:
		p = pygame.image.load('images/'+chess_pieces[color][piece])
		p = pygame.transform.scale(p,(cell_width, cell_height))
		piece_img[color][piece] = p

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("CHESS AI")

def display_text(font_size, text_string, color, text_center):
	font = pygame.font.Font('freesansbold.ttf',font_size)
	text = font.render(text_string, True, color)
	textRect = text.get_rect()
	textRect.center = text_center
	gameDisplay.blit(text, textRect)

def draw_board(turn):
	t = 1
	for y in range(boardY, board_height, cell_height):
		for x in range(boardX, board_width, cell_width):
			if t == -1:
				pygame.draw.rect(gameDisplay, green, [x, y, cell_width, cell_height])
			else:
				pygame.draw.rect(gameDisplay, white, [x, y, cell_width, cell_height])

			t*=-1
		t*=-1	

	#TEXT INDICATING WHOSE TURN IT IS
	if turn =='b':
		display_text(20, "Black's turn", black, (boardX+board_width//2, boardY-d))
	else:
		display_text(20, "White's turn", black, (boardX+board_width//2, boardY-d))

	#VERTICAL LABELLING
	for y in range(1, 9):
		if turn =='w':
			display_text(15, str(9-y), black, (boardX-d, boardY+(2*y-1)*cell_height//2))
		else:
			display_text(15, str(y), black, (boardX-d, boardY+(2*y-1)*cell_height//2))

	#HORIZONTAL LABELLING
	for x in range(1, 9):
		if turn =='w':
			display_text(15, l[x-1], black, (boardX+(2*x-1)*cell_width//2, boardY+board_height+d))
		else:
			display_text(15, l[8-x], black, (boardX+(2*x-1)*cell_width//2, boardY+board_height+d))

def index_to_coordinate(x, y, turn):
	if turn =='w':
		pieceX = boardX + y*cell_width
		pieceY = boardY + x*cell_height
	else:
		pieceX = boardX + board_width - (y+1)*cell_width
		pieceY = boardY + board_width - (x+1)*cell_width
	return pieceX, pieceY

def coordinate_to_index(pieceX, pieceY, turn):
	if turn == 'w':
		y = (pieceX-boardX)//cell_width
		x = (pieceY-boardY)//cell_height
	else:
		y = (boardX+board_width-pieceX)//cell_width
		x = (boardY+board_height-pieceY)//cell_height
	return x,y

def draw_piece(x, y, piece_type, turn):
	pieceX, pieceY = index_to_coordinate(x, y, turn)
	piece = piece_type[0]
	color = piece_type[1]
	gameDisplay.blit(piece_img[color][piece], (pieceX, pieceY))

def draw_pieces(turn, board):
	for x in range(8):
		for y in range(8):
			if board[x][y][0]!='0':
				draw_piece(x, y, board[x][y], turn)

def highlight_cell(x, y, color,turn):
	pieceX,pieceY = index_to_coordinate(x,y,turn)
	pygame.draw.rect(gameDisplay, color, [pieceX, pieceY, cell_width, cell_height],4)

def draw_moves(mouse, turn, board):
	x, y = coordinate_to_index(mouse[0], mouse[1],turn)
	highlight_cell(x,y,red,turn)
	l = []
	if board[x][y][1]==turn:
		l = chessboard.get_moves(x,y)
		for cell in l:
			highlight_cell(cell[0],cell[1],blue,turn)

	return l

def color_cell(x, y, color, turn, board):
	pieceX,pieceY = index_to_coordinate(x,y,turn)
	pygame.draw.rect(gameDisplay, color, [pieceX, pieceY, cell_width, cell_height])
	draw_piece(x, y, board[x][y], turn)
	pygame.display.update()

def  within_board(mouse):
	if (boardX < mouse[0] < boardX+board_width) and (boardY < mouse[1] < boardY+board_height):
		return True
	else:
		return False

def make_move(mouse,turn,board,l):
	x, y = coordinate_to_index(mouse[0], mouse[1],turn)
	color_cell(x,y,red,turn,board)

	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				mouse2 = pygame.mouse.get_pos()
				if within_board(mouse2):
					x2, y2 = coordinate_to_index(mouse2[0], mouse2[1],turn)
					if (x2,y2) in l:
						chessboard.move(x,y,x2,y2)
						return True
				return False


def display_check():
	display_text(35, "CHECK!!", red, (boardX+board_width//2, boardY+board_height+5*d))

def display_checkmate(turn):
	if(turn=='w'):
		display_text(30, "BLACK won!", red, (boardX+board_width//2, boardY+board_height+3*d))
	else:
		display_text(30, "WHITE won!", red, (boardX+board_width//2, boardY+board_height+3*d))

	display_text(30, "Press ENTER for new game", red, (boardX+board_width//2, boardY+board_height+5*d+10))

	pygame.display.update()
	time.sleep(2)
	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_RETURN:
					game_loop()

def game_loop():

	board, turn, is_check, is_checkmate = chessboard.get_board_state()
	gameDisplay.fill(bg)
	draw_board(turn)
	draw_pieces(turn, board)
	pygame.display.update()
	moves_list = []
	moved=False

	while True:

		gameDisplay.fill(bg)
		draw_board(turn)
		draw_pieces(turn, board)
		if(is_check):
			display_check()
		if(is_checkmate):
			display_checkmate(turn)
		mouse = pygame.mouse.get_pos()
		if within_board(mouse):
			moves_list = draw_moves(mouse, turn, board)
		else:
			moves_list = []
		pygame.display.update()

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

			if event.type==pygame.MOUSEBUTTONDOWN:
				if len(moves_list)>0:
					moved=make_move(mouse,turn,board, moves_list)

		if moved == True:
			gameDisplay.fill(bg)
			draw_board(turn)
			draw_pieces(turn, board)
			pygame.display.update()
			time.sleep(1)
			board, turn, is_check, is_checkmate = chessboard.get_board_state()
			moved = False
		
	

game_loop()