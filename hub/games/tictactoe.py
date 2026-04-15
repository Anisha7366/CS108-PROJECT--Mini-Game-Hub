import pygame, sys
pygame.init()

# inherits the base class from base_class.py
from games.base_class import base

# tictactoe and connect4 are nearly identical in logic so parts of the code have been repeated (with changes applied)

class tictactoe(base):
    # some of the initialization is inherited from the parent class like - player names
    # turn=player1, turn_id=1(used to change numpy board), number of rows/columns in the board
    # The numpy board initialized as an array of zeroes, each move changes a 0 to a 1 or a 2 based on turn_id 
    # m= no. of rows/columns , n= no. to match, size= size of pygame screen

    def __init__(self,player1,player2,size,m,n):
        super().__init__(player1,player2,m,n)

        # This is for the actual_game function which uses a while loop
        self.game_over=False

        # size = size of pygame window, this is the same as the size passed in game.py
        self.size=size

        # sets the display
        self.screen=pygame.display.set_mode((self.size[0],self.size[1]+50))

        pygame.display.set_caption("Tic Tac Toe")

        self.font=pygame.font.SysFont(None,30,bold=True,italic=False)

        # just a welcome message
        self.welcome()
        
        # Background design
        self.set_screen()

        # This is used to check if there is a draw
        self.move_number=0

        # Shows whose turn it is at the bottom

        pygame.draw.rect(self.screen,(0,0,0),rect=[0,self.size[1],self.size[0],50])
        self.draw_text(f"{self.player1}(X)'s turn",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)
        pygame.display.flip()

    # A function purely used for aesthetics
    def welcome(self):
        self.screen.fill((255,192,203))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(0,0,0),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=1)
            pygame.draw.line(self.screen,(0,0,0),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=1)

        pygame.draw.line(self.screen,(0,0,0),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=1)
        pygame.draw.line(self.screen,(0,0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=1)

        pygame.draw.rect(self.screen,(0,0,0),rect=[0,self.size[1],self.size[0],50])
        self.draw_text(f"Tic Tac Toe",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)

        pygame.display.flip() 

        # A welcome message
        pygame.display.message_box("Welcome","Welcome to Tic Tac Toe {} and {}! Match {} to win! {} starts!".format(self.player1,self.player2,self.n,self.player1),"info",None,('OK',),0,None)
        pygame.display.flip()

    # this function actually builds the grid the game is played on
    def set_screen(self):
        self.screen.fill((0,0,0))

        # Makes a grid
        for i in range(self.m):
            pygame.draw.line(self.screen,(255,255,255),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=2)
            pygame.draw.line(self.screen,(255,255,255),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=2)

        pygame.draw.line(self.screen,(255,255,255),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=2)
        pygame.draw.line(self.screen,(255,255,255),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=2)
        
        pygame.display.flip()

    # actual game function
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
                    
                    #I noticed as the verify function returned false, the turns switched even when the return value was false(so no O printed but the turn now became X) (2 X's in a row) so this is to ensure the turn remained the same
                    # good_game is used to ensure there is no turn switch when an illegal move is performed(say clicking an already full column)
                    if good_game:
                        self.move_number+=1

                        # checkwin condition - This returns the winner to game.py
                        if self.checkWin():
                            self.game_over=True

                            pygame.draw.rect(self.screen,(0,0,0),rect=[0,self.size[1],self.size[0],50])
                            self.draw_text(f"{self.Turn} wins!",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)

                            pygame.display.message_box("YAY", f"{self.Turn} wins!","info",None,('YAY',),0,None)
                            return self.Turn

                        # checks draw - if no win and all cells are full - this returns "draw" to game.py
                        elif self.move_number==self.m*self.m:

                            pygame.draw.rect(self.screen,(0,0,0),rect=[0,self.size[1],self.size[0],50])
                            self.draw_text(f"nobody wins :(",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)

                            pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                            self.game_over=True
                            return "DRAW"
                        
                        # switching players 
                        self.switch_player()

    # changes the board, draws circles,crosses on the screen
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

    # verifies if a cell is available
    def verify(self,row,column):
        # to make sure no two turns can be on the same cell
        if self.board[row-1][column-1]!=0:
            return False
        return True   
    
    # this is the function Game() calls to draw X's O's
    def update_display(self,cell):
        # This is the function that X's and O's
        length=(self.size[0]+self.size[1])/(4*self.m)

        if self.Turn_id==1:
            pygame.draw.line(self.screen,(150,50,100),(cell[0]-length+9,cell[1]-length+9),(cell[0]+length-9,cell[1]+length-9),width=7)
            pygame.draw.line(self.screen,(150,50,100),(cell[0]+length-9,cell[1]-length+9),(cell[0]-length+9,cell[1]+length-9),width=7)

        else:
            pygame.draw.circle(self.screen,(0,0,128),cell,length-5,width=7)

        pygame.display.flip()

    # It points it out if a match of 5 has been made by highlighting it
    def highlight(self,indices):
        for pair in indices:
            row,column=pair[0],pair[1]
            cell=(self.size[0]/self.m,self.size[1]/self.m)
            
            pygame.draw.rect(self.screen,(255,255,255),rect=[cell[0]*column+3,cell[1]*row+3,cell[0]-4,cell[1]-4])

            self.update_display((cell[0]*(column+0.5),cell[1]*(row+0.5)))

    # checkwin is inherited from the parent class, this waits for 1.5 s so that the players can wait and see the win happening
    def checkWin(self):
        # indices are returned from the parent checkwin function - about row, column in the board where a match occurs
        # now colour of cells with these rows, columns can be changed - to highlight them
        # purely aesthetic
        indices=[]
        x=super().checkWin(indices)
        if(x):
            self.highlight(indices)
            pygame.time.delay(1000)
        # returns true/ false if win happens or not
        return x

    # switch player inherited from parent class
    def switch_player(self):
        super().switch_player()
        pygame.draw.rect(self.screen,(0,0,0),rect=[0,self.size[1],self.size[0],50])

        if self.Turn==self.player1:
            self.draw_text(f"{self.player1}(X)'s turn",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)
        
        else:
            self.draw_text(f"{self.player2}(O)'s turn",self.font,(255,255,255),self.size[0]/2,self.size[1]+25)
        pygame.display.flip()

    # this function is used to print text on the screen
    def draw_text(self,text,font,text_col,x,y):
        img=font.render(text,True,text_col)
        width,height=img.get_size()
        self.screen.blit(img,(x-width/2,y-height/2))

#stupid mistake of doing turn==player 1 for switching turns so it didnt switch 
#mentioning self in front of everything
# i forgot to make game function return true
# made the code better - check win cond then check draw condition