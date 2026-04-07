import numpy as np, pygame, sys
pygame.init()

# tictactoe and connect4 are nearly identical in logic so parts of the code have been repeated (with changes applied)

# wrapped connect4 in a class - will change it so that it inherits from game.py

class tictactoe:
    # 1. initializing the class object 

    def __init__(self,Player1,Player2):

        # These are the usernames passed as arguments to game.py
        self.player1,self.player2=Player1,Player2
        
        # Initializes turn 1 to player1
        self.Turn=self.player1

        # This is for the actual_game function which uses a while loop
        self.game_over=False

        # m = no. of columns in board(=np. of rows), n = the no. to match to win, size = size of pygame window
        self.m,self.n,self.size=10,5,(700,700)

        # sets the display
        self.screen=pygame.display.set_mode(self.size)

        # initializes the numpy board
        self.board=np.zeros((self.m,self.m))

        pygame.display.set_caption("Tic Tac Toe")

        # just a welcome message
        self.welcome()
        
        # Background design
        self.set_screen()

        # This is used to check if there is a draw
        self.move_number=0

    def welcome(self):
        self.screen.fill((255,192,203))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(0,0,0),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=1)
            pygame.draw.line(self.screen,(0,0,0),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=1)

        pygame.draw.line(self.screen,(0,0,0),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=1)
        pygame.draw.line(self.screen,(0,0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=1)
        pygame.display.flip() 

        # A welcome message
        pygame.display.message_box("Welcome","Welcome to Tic Tac Toe {} and {}! Match 5 to win! {} starts!".format(self.player1,self.player2,self.player1),"info",None,('OK',),0,None)
        pygame.display.flip()

    def set_screen(self):
        self.screen.fill((0,0,0))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(255,255,255),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=2)
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=2)

        pygame.draw.line(self.screen,(255,255,255),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=2)
        pygame.draw.line(self.screen,(255,255,255),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=2)
        
        pygame.display.flip()

    def actual_game(self):
        while not self.game_over:
            
            # Turn_id is used to change the numpy board (every move the respective cell in the grid(which is 0) is replaced with Turn_id)
            if self.Turn==self.player1:
                self.Turn_id=1
            else:
                self.Turn_id=2

            # Just initializes it at the start - when there is no mouse position
            mouse_position=(0,0)

            for event in pygame.event.get():
                
                # To let the x button be functional and for a clean exit
                if event.type==pygame.QUIT:
                    pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()

                # This returns the position of a mouse click - which allows a GUI
                elif event.type==pygame.MOUSEBUTTONDOWN:

                    # Stores position where the mouse is clicked
                    mouse_position=event.pos

                    good_game=self.Game(mouse_position)
                    
                    #I noticed as the verify function returned false, the turns switched even when the return value was false(so no O printed but the turn now became X) (2 X's in a row) so this is to ensure the turn remained the same
                    # good_game is used to ensure there is no turn switch when an illegal move is performed(say clicking an already full column)
                    if good_game:
                        self.move_number+=1

                        # checkwin condition
                        if self.checkWin():
                            self.game_over=True                      
                            pygame.display.message_box("YAY", f"{self.Turn} wins!","info",None,('YAY',),0,None)

                        # checks draw - if no win and all cells are full
                        elif self.move_number==self.m*self.m:
                            pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                            pygame.display.flip()
                            self.game_over=True
                        
                        # switching players 
                        self.switch_player()

        #have to change later - don't quit, show stats
        pygame.quit()
        sys.exit() 
    
    def Game(self,mouse_position):

        # each cell has a side of size[0]/m (size[0]=size[1] as defined by the ps, floor division of position of mouse and side + 1 gives us the column and row)
        row=(mouse_position[1]*self.m//self.size[1])+1
        column=(mouse_position[0]*self.m//self.size[0])+1

        # to make sure no two turns can be on the same cell
        if not self.verify(row,column):
            return False
        
        # cell = center of the cell that this particular row and column correspond to
        cell=((column*self.size[0]/self.m)-(self.size[0]/(2*self.m)),(row*self.size[1]/self.m)-(self.size[1]/(2*self.m)))

        # Turn_id is useful here
        self.board[row-1][column-1]=self.Turn_id

        # fills the cell with a disk
        self.update_display(cell)

        return True

    def verify(self,row,column):
        # to make sure no two turns can be on the same cell
        if self.board[row-1][column-1]!=0:
            pygame.display.message_box("OOPS!",f"{self.Turn}! This spot is taken!","warn",None,('oh no!',),0,None)
            pygame.display.flip()
            return False
        return True   
    
    def update_display(self,cell):
        # This is the function that X's and O's
        length=(self.size[0]+self.size[1])/(4*self.m)

        if self.Turn_id==1:
            pygame.draw.line(self.screen,(255,192,203),(cell[0]-length+9,cell[1]-length+9),(cell[0]+length-9,cell[1]+length-9),width=3)
            pygame.draw.line(self.screen,(255,192,203),(cell[0]+length-9,cell[1]-length+9),(cell[0]-length+9,cell[1]+length-9),width=3)

        else:
            pygame.draw.circle(self.screen,(0,240,255),cell,length-5,width=3)

        pygame.display.flip()

    def checkWin(self):
        # checks win 
        if self.Horizontal() or self.Vertical() or self.Diagonal_right() or self.Diagonal_left():
            return True

        return False

    def Horizontal(self):
        # for every row, every consecutive n element array in the row(which is obtained by splicing) is compared to a n element array(all elements are turn_id)
        # This returns an array of booleans. If they match exactly all elements will be true
        # if even one element doesn't match, it will be false and hence the product of the array will be 0
        compare=np.full((1,self.n),self.Turn_id)
        for i in range(0,self.m):
            for j in range(0,self.m-self.n+1):
                a=(self.board[i][j:j+self.n:1]==compare)
                if np.prod(a)!=0:
                    return True

        return False

    def Vertical(self):
        # similar to check horizontal
        # for every column, every consecutive n element array is matched and checked
        # for some reason the splicing gave a horizontal array so i compared it to a horizontal array
        compare=np.full((1,self.n),self.Turn_id)
        for i in range(0,self.m):
            for j in range(0,self.m-self.n+1):
                a=(self.board[j:j+self.n:1,i]==compare)
                if np.prod(a)!=0:
                    return True
        return False

    def Diagonal_right(self):
        # this finds every n x n matrix (with consecutive rows and columns) and compares its diagonal to the full array(\)
        compare=np.full((1,self.n),self.Turn_id)
        for i in range (0,self.m-self.n+1):
            for j in range(0,self.m-self.n+1):
                sub_matr=self.board[i:i+self.n,j:j+self.n]
                diag=sub_matr.diagonal()
                a=(diag==compare)
                if np.prod(a)!=0:
                    return True
        return False
    
    def Diagonal_left(self):
        # This finds every n x n matrix (with consecutive rows and columns) and compares its alternate diagonal(/) to the full array
        compare=np.full((1,self.n),self.Turn_id)
        for i in range (0,self.m-self.n+1):
            for j in range(0,self.m-self.n+1):
                sub_matr=self.board[i:i+self.n,j:j+self.n]
                L_diag=np.fliplr(sub_matr).diagonal()
                a=(L_diag==compare)
                if np.prod(a)!=0:
                    return True
        return False

    def switch_player(self):
        # switching logic which will be linked to the base class in game.py
        if self.Turn==self.player1:
            self.Turn=self.player2

        else:
            self.Turn=self.player1

# just for initialization, this will be removed
game=tictactoe('one','two')
game.actual_game() 

#stupid mistake of doing turn==player 1 for switching turns so it didnt switch 
#mentioning self in front of everything
# i forgot to make game function return true
# made the code better - check win cond then check draw condition