import numpy as np, pygame, sys
pygame.init()

# makes the background black and makes the grid and sets four pieces in the center
def set_screen(m,screen,size):
    #size is the tuple that defines width, height of the screen
    screen.fill((10,10,10))   #this is the RGB that turns the screen black-ish

    for i in range(m):
        pygame.draw.line(screen,(220,220,220),(0,i*size[1]/m),(size[0],i*size[1]/m),width=2)  
        pygame.draw.line(screen,(220,220,220),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=2) 

    pygame.draw.line(screen,(255,255,255),(0,size[1]-1),(size[0],size[1]-1),width=2)
    pygame.draw.line(screen,(255,255,255),(size[0]-1,0),(size[0]-1,size[1]),width=2)

    length = (size[0]+size[1])/(4*m)
    pygame.draw.circle(screen, (70,255,70), (size[0]/2 - length, size[1]/2 - length), length-12)
    pygame.draw.circle(screen, (70,255,70), (size[0]/2 + length, size[1]/2 + length), length-12)
    pygame.draw.circle(screen, (255,70,255), (size[0]/2 - length, size[1]/2 + length), length-12)
    pygame.draw.circle(screen, (255,70,255), (size[0]/2 + length, size[1]/2 - length), length-12)


    pygame.display.flip()

def update_after_move(screen, board, Turn_id, m, size):

    #print(board)
    length=(size[0]+size[1])/(4*m)

    for i,j in np.ndindex(board.shape):

        if board[i][j] == 1:
            update_display(1, screen, size,m,(j*size[0]/m + size[0]/(2*m), i*size[1]/m + size[1]/(2*m)))
        elif board[i][j] == 2:
            update_display(2, screen, size,m,(j*size[0]/m + size[0]/(2*m), i*size[1]/m + size[1]/(2*m)))
       
        #else:
        #    pygame.draw.circle(screen, (10,10,10), (j*size[0]/m + size[0]/(2*m), i*size[1]/m + size[1]/(2*m)), length-12, width=3)

    pygame.display.flip()

def check_if_valid(Turn_id,screen,position,board,m,size):

    change = 0
    
    row=position[1]*m//size[1]+1
    column=position[0]*m//size[0]+1

    if Turn_id == 1:
        self = 1
        other = 2
    else:
        self = 2
        other = 1

    #board[row - 1][column - 1] = self

    direction = [(1,0), (0,1), (0,-1), (-1,0), (-1,-1), (1,1), (-1,1), (1,-1)]
    
    for x in range(8):

        h = direction[x][0]
        v = direction[x][1]

        i = 1

        row = int(row)
        column = int(column)
                
        while((row-1+i*v<m) and (column-1+i*h<m) and (row-1+i*v>=0) and (column-1+i*h>=0) and board[row+i*v-1][column-1 +i*h] == other):
            i += 1
        if (row-1+i*v<m) and (column -1 + i*h < m) and (row-1+i*v>=0) and (column-1+i*h>=0) and (board[row+i*v-1][column-1+i*h] == self) and (i > 1):
            change += i-1
            

    return change

def update_board(Turn_id,screen,position,board,m,size):

    copied_board = board.copy()

    change = 0
    
    row=position[1]*m//size[1]+1
    column=position[0]*m//size[0]+1

    if Turn_id == 1:
        self = 1
        other = 2
    else:
        self = 2
        other = 1

    #board[row - 1][column - 1] = self

    direction = [(1,0), (0,1), (0,-1), (-1,0), (-1,-1), (1,1), (-1,1), (1,-1)]
    
    for x in range(8):

        h = direction[x][0]
        v = direction[x][1]

        i = 1
                
        while((row-1+i*v<m) and (column-1+i*h<m) and (row-1+i*v>=0) and (column-1+i*h>=0) and copied_board[row+i*v-1][column-1 +i*h] == other):
            i += 1
        if (row-1+i*v<m) and (column -1 + i*h < m) and (row-1+i*v>=0) and (column-1+i*h>=0) and (copied_board[row+i*v-1][column-1+i*h] == self) and (i > 1):
            change += i-1

            for t in range(1,i):
                board[row+t*v-1][column-1 +t*h] = self
            

#draws 'X' or 'O' at a desired position- using dimensions i find aesthatically pleasing with the grid
def update_display(Turn_id,screen,size,m,position):
    length=(size[0]+size[1])/(4*m)

    if Turn_id==1:
        pygame.draw.circle(screen,(70,255,70),position,length-12)
    else:
        pygame.draw.circle(screen,(255,70,255),position,length-12)

    pygame.display.flip()

# Makes sure that a used cell cannot be used
def verify(row,column,board,m):
    if board[row-1][column-1]!=0:
        pygame.display.message_box("OOPS!","This spot is taken!","warn",None,('oh no!',),0,None)
        return False
    return True

def Game(Turn_id,board,m,size,screen,position):
    # each cell has a side of size[0]/m (size[0]=size[1] as defined by the ps, floor division of position of mouse and side + 1 gives us the column and row)
    row=position[1]*m//size[1]+1
    column=position[0]*m//size[0]+1

    # to make sure no two turns can be on the same cell
    if not verify(row,column,board,m):
        return False

    #updates the board, game window at desired cell taking care of whose turn it is
    if Turn_id==1:
        board[row-1][column-1]=1
        update_display(Turn_id,screen,size,m,((column*size[0]/m)-(size[0]/(2*m)),((row)*size[1]/m)-(size[1]/(2*m))))
    
    else:
        board[row-1][column-1]=2
        update_display(Turn_id,screen,size,m,((column*size[0]/m)-(size[0]/(2*m)),((row)*size[1]/m)-(size[1]/(2*m)))) 
    
    return True

def check_win(board, m):

    #print("Entered correct function")
    #print(board)
    
    boolean_matrix = board == 1
    temp = np.full((m, m), -1)
    points1 = temp[boolean_matrix].flatten().size
    points2 = m*m - points1

    if points1 > points2:
        return 1
    elif points2 > points1:
        return 2
    else:
        return 0
    

def valid_move_exist(Turn_id, board, screen, m, size):

    fine = False
    for i in np.ndindex(board.shape):
        x = (i[0] + 0.5)*(size[0]/m)
        y = (i[1] + 0.5)*(size[1]/m)

        length = (size[0]+size[1])/(4*m)

        position = (x,y)

        if(board[i] == 0):
            if check_if_valid(Turn_id, screen, position, board, m, size) > 0:
                #pygame.draw.circle(screen, (30, 30, 30), (x, y), length-12, width=3)
                fine = True
                
    pygame.display.flip()  
        
    return fine
    
    




#main
Turn="Player1"
game_over=False

# m is the number of columns in the grid, n is the no. of elements in line for a match, size is the size of the pygame window
#for the game to work m has to be even
m=8 
size=(700,700)

# initializing the board as a numpy array (all zeroes) and initializing the pygame window
screen=pygame.display.set_mode(size)
board=np.zeros((m,m))

board[m//2 - 1][m//2 - 1] = 1
board[m//2][m//2] = 1
board[m//2][m//2 - 1] = 2
board[m//2 - 1][m//2] = 2

#print(board)


# Naming it!
pygame.display.set_caption("Othello")

# Just a welcome message, may find alternative also may add the usernames into the message
screen.fill((0,0,0))

for i in range(m):
    pygame.draw.line(screen,(255,255,255),(0,i*size[1]/m),(size[0],i*size[1]/m),width=1)
    pygame.draw.line(screen,(255,255,255),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=1)

pygame.draw.line(screen,(255,255,255),(0,size[1]-1),(size[0],size[1]-1),width=1)
pygame.draw.line(screen,(255,255,255),(size[0]-1,0),(size[0]-1,size[1]),width=1)
pygame.display.flip() 

pygame.display.message_box("Welcome","The player who has the largest number of coins on board wins! Green goes first!","info",None,('OK',),0,None)
pygame.display.flip()

# a self defined function that draws the grid on the screen
set_screen(m,screen,size)

# parameter used to to end the game (i would be m*m)
i=4

while not game_over:
    # variables that are passed in place of the player names to the function
    if Turn=="Player1":
        Turn_id=1
    
    else:
        Turn_id=2
    
    # initializing the mouse click position(to prevent a crash)
    position=(0,0)

    for event in pygame.event.get():
        # closes the window if the user closes
        if event.type==pygame.QUIT:
            pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
            pygame.display.flip()
            pygame.quit()
            sys.exit()


        if valid_move_exist(Turn_id, board, screen, m, size) == False:

            

            pygame.display.message_box("Oh no!", f"{Turn_id} has no valid move! Your move is skipped :(","warn",None,('OK',),0,None)

            if Turn=="Player1":
                Turn="Player2"

            else:
                Turn="Player1"


        
        # Allows user to select the column,row by clicking their mouse at the desired cell
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=event.pos

            





            if(check_if_valid(Turn_id, screen, position, board, m, size) > 0):

                good_game=Game(Turn_id,board,m,size,screen,position)
                update_board(Turn_id, screen, position, board, m, size)

                pygame.time.delay(250)
                update_after_move(screen, board, Turn_id, m, size)
            else:
                pygame.display.message_box("Error", "Sorry, that is not a valid move :)","warn",None,('OK',),0,None)
                good_game=False

            #to remove the suggested options circles
            update_after_move(screen, board, Turn_id, m, size)

            # function that updates the board and the window
            #I noticed as the verify function returned false, the turns switched even when the return value was false(so no O printed but the turn now became X) (2 X's in a row) so this is to ensure the turn remained the same
            if good_game:
                i+=1
                #print(i)

                # end of the game
                if(i==m*m):
                    win = check_win(board, m)
                    if(win == 0):
                        
                        pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                        pygame.display.flip()
                    game_over=True

                # To switch through turns
                if Turn=="Player1":
                    Turn="Player2"

                else:
                    Turn="Player1"

# quits after the game is over- will change as our project develops
pygame.display.message_box("YAY",f"{win} wins!","info",None,('YAY',),0,None)
pygame.quit()
sys.exit()



# A challenge faced: the x's repeating - the fix(wrong) sent it to an infinite loop

'''for t in range(1,i):
board[row+t*v-1][column-1 +t*h] = self
#r,c is the which'th row and column we need circles to be made
#x,y are the positions
r = row + t*v 
c = column + t*h 
x = c*size[0]/m - size[0]/(2*m)
y = r*size[1]/m - size[1]/(2*m)
update_display(self, screen, size,m,(x,y))'''