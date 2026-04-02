import numpy as np, pygame, sys
pygame.init()

# The logic for connect 4 is very similar to tic tac toe, so not much was changed

# makes the background white(unlike the default black) and makes the grid
def set_screen(m,screen,size):
    screen.fill((0,0,0))

    for i in range(m):
        pygame.draw.line(screen,(255,255,255),(0,i*size[1]/m),(size[0],i*size[1]/m),width=2)
        pygame.draw.line(screen,(255,255,255),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=2)

    pygame.draw.line(screen,(255,255,255),(0,size[1]-1),(size[0],size[1]-1),width=2)
    pygame.draw.line(screen,(255,255,255),(size[0]-1,0),(size[0]-1,size[1]),width=2)
    
    pygame.display.flip() 

#draws 'X' or 'O' at a desired position- using dimensions I find aesthatically pleasing with the grid
def update_display(Turn_id,screen,size,m,position):
    length=(size[0]+size[1])/(4*m)

    if Turn_id==1:
        pygame.draw.aacircle(screen,(0,255,230),position,length-10)

    else:
        pygame.draw.aacircle(screen,(238,130,238),position,length-10)

    pygame.display.flip()

# Makes sure that a full column cannot be filled, rows are a useless check here
def verify(column,board,m):
    if board[0][column-1]!=0:
        pygame.display.message_box("OOPS!","This column is full!","warn",None,('oh no!',),0,None)
        return False
    return True

# Gives the last empty row index in a column
def return_empty(column,board,m):
    for i in range(m-1,-1,-1):
        if board[i][column-1]==0:
            return i

def Game(Turn_id,board,m,size,screen,position):
    # each cell has a side of size[0]/m (size[0]=size[1] as defined by the ps, floor division of position of mouse and side + 1 gives us the column)
    column=position[0]*m//size[0]+1

    # to make sure no two turns can be on the same cell
    if not verify(column,board,m):
        return False

    #Last empty row in the column(put after verify, so it must exist)
    row=return_empty(column,board,m)+1

    #updates the board, game window at desired cell taking care of whose turn it is
    if Turn_id==1:
        board[row-1][column-1]=1
        update_display(Turn_id,screen,size,m,((column*size[0]/m)-(size[0]/(2*m)),((row)*size[1]/m)-(size[1]/(2*m))))
    
    else:
        board[row-1][column-1]=2
        update_display(Turn_id,screen,size,m,((column*size[0]/m)-(size[0]/(2*m)),((row)*size[1]/m)-(size[1]/(2*m))))

    return True

# done with numpy slicing. Iterates through the board to see if there is a horizontal match(by equating it to a full array with elements based on the turn) 
# gives an array of boolean values (if all elements are True, the arrays are equal and product of the boolean array is non 0(no False)) 
def Horizontal(Turn_id,board,m,n):
    compare=np.full((1,n),Turn_id)
    for i in range(0,m):
        for j in range(0,m-n+1):
                a=(board[i][j:j+n:1]==compare)
                if np.prod(a)!=0:
                    return True
    return False

# iterates through the board to see if there is a vertical match
# similar process - iterates through the board and is compared
def Vertical(Turn_id,board,m,n):
    compare=np.full((1,n),Turn_id)
    for i in range(0,m):
        for j in range(0,m-n+1):
            a=(board[j:j+n:1,i]==compare)
            if np.prod(a)!=0:
                return True
    return False

# iterates through the board to see if there is a right diagonal match(\)
def Diagonal_right(Turn_id,board,m,n):
    compare=np.full((1,n),Turn_id)
    for i in range (0,m-n+1):
        for j in range(0,m-n+1):
            sub_matr=board[i:i+n,j:j+n]
            diag=sub_matr.diagonal()
            a=(diag==compare)
            if np.prod(a)!=0:
                return True
    return False

# iterates through the board to see if there is a left diagonal match(/)
def Diagonal_left(Turn_id,board,m,n):
    compare=np.full((1,n),Turn_id)
    for i in range (0,m-n+1):
        for j in range(0,m-n+1):
            sub_matr=board[i:i+n,j:j+n]
            L_diag=np.fliplr(sub_matr).diagonal()
            a=(L_diag==compare)
            if np.prod(a)!=0:
                return True
    return False

# calls 4 functions that each check a line
def checkWin(Turn_id,board,m,n):
    if Horizontal(Turn_id,board,m,n) or Vertical(Turn_id,board,m,n) or Diagonal_right(Turn_id,board,m,n) or Diagonal_left(Turn_id,board,m,n):
        return True
    return False

#main
Turn="Player1"
game_over=False

# m is the number of columns in the grid, n is the no. of elements in line for a match, size is the size of the pygame window
m=7 
n=4
size=(700,700)

# initializing the board as a numpy array (all zeroes) and initializing the pygame window
screen=pygame.display.set_mode(size)
board=np.zeros((m,m))

# Naming it!
pygame.display.set_caption("Connect4")

# Just a welcome message, may find alternative also may add the usernames into the message
screen.fill((150,50,100))

for i in range(m):
    pygame.draw.line(screen,(255,255,255),(0,i*size[1]/m),(size[0],i*size[1]/m),width=1)
    pygame.draw.line(screen,(255,255,255),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=1)

pygame.draw.line(screen,(255,255,255),(0,size[1]-1),(size[0],size[1]-1),width=1)
pygame.draw.line(screen,(255,255,255),(size[0]-1,0),(size[0]-1,size[1]),width=1)
pygame.display.flip() 

pygame.display.message_box("Welcome","Connect4 with cyan and purple! cyan starts! Connect 4 to win!","info",None,('OK',),0,None)
pygame.display.flip()

# a self defined function that draws the grid on the screen
set_screen(m,screen,size)

# parameter used to find if there is a draw('i' would be m*m)
i=0

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

    # Allows user to select the column by clicking their mouse anywhere in the desired column
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=event.pos

            good_game=Game(Turn_id,board,m,size,screen,position)

            # function that updates the board and the window
            # We don't really have the exact same problem here, but this ensures that no repition when someone tries to drop a disc in a already full column
            if good_game:
                i+=1
                # checks for a draw
                if(i==m*m):
                    pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                    pygame.display.flip()
                    game_over=True

                # checks win (4 in a row/column/diagonal)
                if checkWin(Turn_id,board,m,n):
                    game_over=True
                    
                    # Will change to usernames later
                    if Turn_id==1:
                        win="CYAN"
                    else:
                        win="VIOLET"

                # To switch through turns
                if Turn=="Player1":
                    Turn="Player2"

                else:
                    Turn="Player1"

# quits after the game is over- will change as our project develops
pygame.display.message_box("YAY",f"{win} wins!","info",None,('YAY',),0,None)
pygame.quit()
sys.exit()