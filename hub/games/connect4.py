import pygame,sys
pygame.init()

from games.base_class import base

# wrapped connect4 in a class - will change it so that it inherits from game.py

class connect4(base):
    # 1. initializing the class object 

    # m = no. of columns in board(=np. of rows), n = the no. to match to win, 
    def __init__(self,player1,player2,size,m,n):
        super().__init__(player1,player2,m,n)

        # This is for the actual_game function which uses a while loop
        self.game_over=False

        # size = size of pygame window
        self.size=size

        # sets the display
        self.screen=pygame.display.set_mode(self.size)

        pygame.display.set_caption("Connect4")

        # just a welcome message
        self.welcome()
        
        # Background design
        self.set_screen()

        # This is used to check if there is a draw
        self.move_number=0

        # just for aesthetics
        self.length=(self.size[0]+self.size[1])/(4*self.m)

    def welcome(self):
        self.screen.fill((150,50,100))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m-2,0),(i*self.size[0]/self.m-2,self.size[1]),width=1)
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m+2,0),(i*self.size[0]/self.m+2,self.size[1]),width=1)

        pygame.draw.line(self.screen,(255,255,255),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=1)
        pygame.display.flip() 

        # A welcome message
        pygame.display.message_box("Welcome","Welcome to connect 4 {} and {}! Connect 4 to win! {} starts! \nClick anywhere in a column to drop a disk in that column!".format(self.player1,self.player2,self.player1),"info",None,('OK',),0,None)
        pygame.display.flip()

    def set_screen(self):
        self.screen.fill((0,0,0))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m-2,0),(i*self.size[0]/self.m-2,self.size[1]),width=1)
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m+2,0),(i*self.size[0]/self.m+2,self.size[1]),width=1)

        pygame.draw.line(self.screen,(255,255,255),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=2)
        
        pygame.display.flip()

    def actual_game(self):
        while not self.game_over:

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
        
        # mouse position / width of one cell + 1 = column
        column=(mouse_position[0]*self.m//self.size[0])+1

        # checks if the column picked isn't already full
        if not self.verify(column):
            return False

        # returns last empty row in column picked
        row=self.empty_row(column)+1
        
        # cell = center of the cell that this particular row and column correspond to
        cell=((column*self.size[0]/self.m)-(self.size[0]/(2*self.m)),(row*self.size[1]/self.m)-(self.size[1]/(2*self.m)))

        # Turn_id is useful here
        self.board[row-1][column-1]=self.Turn_id

        # fills the cell with a disk
        self.update_display(cell)

        return True

    def verify(self,column):
        # checks that the column picked is not full, gives error message accordingly
        if self.board[0][column-1]!=0:
            pygame.display.message_box("OOPS!",f"{self.Turn}! This column is full!","warn",None,('oh no!',),0,None)
            pygame.display.flip()
            return False
        return True

    def empty_row(self,column):
        # returns the last empty row in a column (looks bottom to top)
        for i in range(self.m-1,-1,-1):
            if self.board[i][column-1]==0:
                return i

    def update_display(self,cell):
        # This is the function that draws disks at a column

        if self.Turn_id==1:
            pygame.draw.aacircle(self.screen,(0,255,230),cell,self.length-10)

        else:
            pygame.draw.aacircle(self.screen,(238,130,238),cell,self.length-10)

        pygame.display.flip()

    def highlight(self,indices):
        for pair in indices:
            row,column=pair[0],pair[1]
            cell=(self.size[0]/self.m,self.size[1]/self.m)
            
            pygame.draw.rect(self.screen,(255,100,0),rect=[cell[0]*column+3,cell[1]*row,cell[0]-5,cell[1]])

            self.update_display((cell[0]*(column+0.5),cell[1]*(row+0.5)))

    def checkWin(self):
        indices=[]
        x=super().checkWin(indices)
        if(x):
            self.highlight(indices)
            pygame.time.delay(1000)
        return x

    def switch_player(self):
        super().switch_player()
              
#stupid mistake of doing turn==player 1 for switching turns so it didnt switch 
#mentioning self in front of everything
# i forgot to make game function return true
# made the code better - check win cond then check draw condition