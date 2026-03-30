import numpy as np, pygame, sys
pygame.init()

# makes the background white(unlike the default black) and makes the grid
def set_screen(m,screen,size):
    screen.fill((0,0,0))

    for i in range(m):
        pygame.draw.line(screen,(255,255,255),(0,i*size[1]/m),(size[0],i*size[1]/m),width=1)
        pygame.draw.line(screen,(255,255,255),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=1)

    pygame.draw.line(screen,(255,255,255),(0,size[1]-1),(size[0],size[1]-1),width=1)
    pygame.draw.line(screen,(255,255,255),(size[0]-1,0),(size[0]-1,size[1]),width=1)
    
    pygame.display.flip()   

#draws 'X' or 'O' at a desired position- using dimensions i find aesthatically pleasing with the grid
def update_display(Turn_id,screen,size,m,position):
    length=(size[0]+size[1])/(4*m)

    if Turn_id==1:
        pygame.draw.line(screen,(255,192,203),(position[0]-length+9,position[1]-length+9),(position[0]+length-9,position[1]+length-9),width=3)
        pygame.draw.line(screen,(255,192,203),(position[0]+length-9,position[1]-length+9),(position[0]-length+9,position[1]+length-9),width=3)
    
    else:
        pygame.draw.circle(screen,(0,240,255),position,length-5,width=3)

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

# done with loops for now, iterates through the board to see if there is a horizontal match
def Horizontal(board,m,n):
    for i in range(0,m):
        for j in range(0,m-n+1):
                Yes=True
                for k in range(j,j+n-1):
                    if board[i][k]!=board[i][k+1] or board[i][k]==0:
                        Yes=False
                        break
                if Yes:
                    return True
    return False

# iterates through the board to see if there is a vertical match
def Vertical(board,m,n):
    for i in range(0,m):
        for j in range(0,m-n+1):
            Yes=True
            for k in range(j,j+n-1):
                if board[k][i]!=board[k+1][i] or board[k][i]==0:
                    Yes=False
                    break
            if Yes:
                return True
    return False

# iterates through the board to see if there is a right diagonal match(\)
def Diagonal_right(board,m,n):
    for i in range (0,m-n+1):
        for j in range(0,m-n+1):
            b=i
            Yes=True
            for k in range(j,j+n-1):
                if board[b][k]!=board[b+1][k+1] or board[b][k]==0:
                    Yes=False
                    break
                b+=1
            if Yes:
                return True
    return False

# iterates through the board to see if there is a left diagonal match(/)
def Diagonal_left(board,m,n):
    for i in range (0,m-n+1):
        for j in range(n-1,m):
            b=i
            Yes=True
            for k in range(j,j-n+1,-1):
                if board[b][k]!=board[b+1][k-1] or board[b][k]==0:
                    Yes=False
                    break
                b+=1
            if Yes:
                return True
    return False

# calls 4 functions that each check a line
def checkWin(board,m,n):
    if Horizontal(board,m,n) or Vertical(board,m,n) or Diagonal_right(board,m,n) or Diagonal_left(board,m,n):
        return True
    return False

#main
Turn="Player1"
game_over=False

# m is the number of columns in the grid, n is the no. of elements in line for a match, size is the size of the pygame window
m=10 
n=5 
size=(700,700)

# initializing the board as a numpy array (all zeroes) and initializing the pygame window
screen=pygame.display.set_mode(size)
board=np.zeros((m,m))

# Naming it!
pygame.display.set_caption("Tic Tac Toe")

# Just a welcome message, may find alternative also may add the usernames into the message
screen.fill((255,192,203))
pygame.display.flip()
pygame.display.message_box("Welcome","Tic Tac Toe with 'X' and 'O' ! X starts!","info",None,('OK',),0,None)
pygame.display.flip()

# a self defined function that draws the grid on the screen
set_screen(m,screen,size)

# parameter used to find if there is a draw(i would be m*m)
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
        
        # Allows user to select the column,row by clicking their mouse at the desired cell
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=event.pos

            good_game=Game(Turn_id,board,m,size,screen,position)

            # function that updates the board and the window
            #I noticed as the verify function returned false, the turns switched even when the return value was false(so no O printed but the turn now became X) (2 X's in a row) so this is to ensure the turn remained the same
            if good_game:
                i+=1

                # checks for a draw
                if(i==m*m):
                    pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                    pygame.display.flip()
                    game_over=True

                # checks win (5 in a row/column/diagonal)
                if checkWin(board,m,n):
                    game_over=True
                    if Turn_id==1:
                        win="X"
                    else:
                        win="O"

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