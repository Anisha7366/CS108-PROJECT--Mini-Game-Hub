import numpy as np, pygame, sys
pygame.init()

# inherits the base class from base_class.py
from games.base_class import base


class othello(base):

    def __init__(self,player1,player2,size,m):
        super().__init__(player1,player2,m,-1)

        # This is for the actual_game function which uses a while loop
        self.game_over=False

        # size = size of pygame window
        self.size=size

        # sets the display
        self.screen=pygame.display.set_mode(self.size)

        pygame.display.set_caption("Othello")

        # just a welcome message
        self.welcome()
        
        # Background design
        self.set_screen()

        # This is used to check if the game ended
        self.move_number=4

        # just for aesthetics
        self.length=(self.size[0]+self.size[1])/(4*self.m)

    def welcome(self):
        self.screen.fill((238,130,238))

        for i in range(self.m):
            pygame.draw.line(self.screen,(0,0,0),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=1)
            pygame.draw.line(self.screen,(0,0,0),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=1)

        pygame.draw.line(self.screen,(0,0,0),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=1)
        pygame.draw.line(self.screen,(0,0,0),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=1)
        pygame.display.flip() 

        pygame.display.message_box("Welcome",f"The player who has the largest number of coins on board wins! {self.player1} goes first!","info",None,('OK',),0,None)
        pygame.display.flip()

    
    # makes the background black and makes the grid and sets four pieces in the center
    def set_screen(self):
    #size is the tuple that defines width, height of the screen
        
        self.screen.fill((10,10,10))   #this is the RGB that turns the screen black-ish

        for i in range(self.m):
            pygame.draw.line(self.screen,(220,220,220),(0,i*self.size[1]/self.m),(self.size[0],i*self.size[1]/self.m),width=2)  
            pygame.draw.line(self.screen,(220,220,220),(i*self.size[0]/self.m,0),(i*self.size[0]/self.m,self.size[1]),width=2) 

        pygame.draw.line(self.screen,(255,255,255),(0,self.size[1]-1),(self.size[0],self.size[1]-1),width=2)
        pygame.draw.line(self.screen,(255,255,255),(self.size[0]-1,0),(self.size[0]-1,self.size[1]),width=2)

        length = (self.size[0]+self.size[1])/(4*self.m)
        pygame.draw.circle(self.screen, (51, 255, 255), (self.size[0]/2 - length, self.size[1]/2 - length), length-12)
        pygame.draw.circle(self.screen, (51, 255, 255), (self.size[0]/2 + length, self.size[1]/2 + length), length-12)
        pygame.draw.circle(self.screen, (255,51,255), (self.size[0]/2 - length, self.size[1]/2 + length), length-12)
        pygame.draw.circle(self.screen, (255,51,255), (self.size[0]/2 + length, self.size[1]/2 - length), length-12)

        pygame.display.flip()

    #the function that used to be main
    def actual_game(self):

        self.board[self.m//2 - 1][self.m//2 - 1] = 1
        self.board[self.m//2][self.m//2] = 1
        self.board[self.m//2][self.m//2 - 1] = 2
        self.board[self.m//2 - 1][self.m//2] = 2


        while not self.game_over:
            # variables that are passed in place of the player names to the function
            if self.Turn==self.player1:
                self.Turn_id=1
            
            else:
                self.Turn_id=2
            
            # initializing the mouse click position(to prevent a crash)
            position=(0,0)

            has_move = self.valid_move_exist(position, self.Turn_id)

            for event in pygame.event.get():
                # closes the window if the user closes
                if event.type==pygame.QUIT:
                    pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()

                if self.Turn_id == 1:
                    color = "Blue"
                else:
                    color = "Purple"


                if has_move == False:

                    pygame.display.message_box("Oh no!", f"{self.Turn} has no valid move! Your move is skipped :(","warn",None,('OK',),0,None)

                    if self.Turn==self.player1:
                        self.Turn=self.player2

                    else:
                        self.Turn=self.player1

                
                # Allows user to select the column,row by clicking their mouse at the desired cell
                if event.type==pygame.MOUSEBUTTONDOWN:
                    position=event.pos


                    if(self.check_if_valid(position, self.Turn_id) > 0):

                        good_game=self.Game(position, self.Turn_id)
                        self.update_board(self.Turn_id, position)

                        pygame.time.delay(250)
                        self.update_after_move()
                    else:
                        pygame.display.message_box("Error", "Sorry, that is not a valid move :)","warn",None,('OK',),0,None)
                        good_game=False

                    #to remove the suggested options circles
                    self.update_after_move()

                    # function that updates the board and the window
                    #I noticed as the verify function returned false, the turns switched even when the return value was false(so no O printed but the turn now became X) (2 X's in a row) so this is to ensure the turn remained the same
                    if good_game:
                        self.move_number+=1
                        #print(i)

                        # end of the game
                        if(self.move_number==self.m*self.m):
                            self.game_over=True
                            win = self.checkWin()
                            if(win == 0):
                                
                                pygame.display.message_box("WOW","It's a draw!","info",None,('WOW',),0,None)
                                pygame.display.flip()
                                
                                return "draw"
                                

                            elif(win == 1):
                                win_color = "Blue"

                            else:
                                win_color = "Purple"

                        


                        # To switch through turns
                        if self.Turn==self.player1:
                            self.Turn=self.player2

                        else:
                            self.Turn=self.player1

                        
        # quits after the game is over- will change as our project develops
        pygame.display.message_box("YAY",f"{self.Turn} wins!","info",None,('YAY',),0,None)
        #pygame.quit()
        
        if (win == 1):
            return self.player1 
        else:
            return self.player2
      

    def valid_move_exist(self, position, Turn_id):

        fine = False
        for i in np.ndindex(self.board.shape):
            x = (i[1] + 0.5)*(self.size[1]/self.m)
            y = (i[0] + 0.5)*(self.size[0]/self.m)


            position = (x,y)

            if(self.board[i] == 0):
                if self.check_if_valid(position, Turn_id) > 0:
                    pygame.draw.circle(self.screen, (50, 50, 50), (x, y), self.length-12, width=3)
                    fine = True
                    
        pygame.display.flip()  
            
        return fine
    
    #returns the number of coins flipped if the a move is made at the given position
    def check_if_valid(self,position,Turn_id):

        change = 0
        
        row=position[1]*self.m//self.size[1]+1
        column=position[0]*self.m//self.size[0]+1

        if Turn_id == 1:
            selff = 1
            other = 2
        else:
            selff = 2
            other = 1

        #board[row - 1][column - 1] = self

        direction = [(1,0), (0,1), (0,-1), (-1,0), (-1,-1), (1,1), (-1,1), (1,-1)]
        
        for x in range(8):

            h = direction[x][0]
            v = direction[x][1]

            i = 1

            row = int(row)
            column = int(column)
                    
            while((row-1+i*v < self.m) and (column-1+i*h<self.m) and (row-1+i*v>=0) and (column-1+i*h>=0) and self.board[row+i*v-1][column-1 +i*h] == other):
                i += 1
            if (row-1+i*v < self.m) and (column -1 + i*h < self.m) and (row-1+i*v>=0) and (column-1+i*h>=0) and (self.board[row+i*v-1][column-1+i*h] == selff) and (i > 1):
                change += i-1
                
        return change
    
    def update_board(self, Turn_id, position):

        copied_board = self.board.copy()

        change = 0
        
        row=position[1]*self.m//self.size[1]+1
        column=position[0]*self.m//self.size[0]+1

        if Turn_id == 1:
            selff = 1
            other = 2
        else:
            selff = 2
            other = 1

        #board[row - 1][column - 1] = self

        direction = [(1,0), (0,1), (0,-1), (-1,0), (-1,-1), (1,1), (-1,1), (1,-1)]
        
        for x in range(8):

            h = direction[x][0]
            v = direction[x][1]

            i = 1
                    
            while((row-1+i*v < self.m) and (column-1+i*h < self.m) and (row-1+i*v>=0) and (column-1+i*h>=0) and copied_board[row+i*v-1][column-1 +i*h] == other):
                i += 1
            if (row-1+i*v < self.m) and (column -1 + i*h < self.m) and (row-1+i*v>=0) and (column-1+i*h>=0) and (copied_board[row+i*v-1][column-1+i*h] == selff) and (i > 1):
                change += i-1

                for t in range(1,i):
                    self.board[row+t*v-1][column-1 +t*h] = selff


    #updates the screen if a valid move is made and returns error if the board is already filled
    def Game(self, position, Turn_id):
        # each cell has a side of size[0]/m (size[0]=size[1] as defined by the ps, floor division of position of mouse and side + 1 gives us the column and row)
        row=position[1]*self.m//self.size[1]+1
        column=position[0]*self.m//self.size[0]+1

        # to make sure no two turns can be on the same cell
        if not self.verify(row,column):
            return False

        #updates the board, game window at desired cell taking care of whose turn it is
        if Turn_id==1:
            self.board[row-1][column-1]=1
            self.update_display(Turn_id, ((column*self.size[0]/self.m)-(self.size[0]/(2*self.m)),((row)*self.size[1]/self.m)-(self.size[1]/(2*self.m))))
        
        else:
            self.board[row-1][column-1]=2
            self.update_display(Turn_id,((column*self.size[0]/self.m)-(self.size[0]/(2*self.m)),((row)*self.size[1]/self.m)-(self.size[1]/(2*self.m)))) 
        
        return True
    
    #draws coins at a desired position- using dimensions i find aesthatically pleasing with the grid
    def update_display(self, Turn_id, position):
    

        if Turn_id==1:
            pygame.draw.circle(self.screen,(51,255,255),position,self.length-12)
        else:
            pygame.draw.circle(self.screen,(255,51,255),position,self.length-12)
        
        pygame.display.flip()

    # Makes sure that a used cell cannot be used
    def verify(self, row, column):
        if self.board[row-1][column-1]!=0:
            pygame.display.message_box("OOPS!","This spot is taken!","warn",None,('oh no!',),0,None)
            return False
        return True
    
    #essentially draws the screen anew accounting to the array board, which looks like flipping because the function is called with a time delay
    def update_after_move(self):

        
        for i,j in np.ndindex(self.board.shape):

            if self.board[i][j] == 1:
                self.update_display(1, (j*self.size[0]/self.m + self.size[0]/(2*self.m), i*self.size[1]/self.m + self.size[1]/(2*self.m)))
            elif self.board[i][j] == 2:
                self.update_display(2,(j*self.size[0]/self.m + self.size[0]/(2*self.m), i*self.size[1]/self.m + self.size[1]/(2*self.m)))
            else:
                pygame.draw.circle(self.screen,(10,10,10),(j*self.size[0]/self.m + self.size[0]/(2*self.m), i*self.size[1]/self.m + self.size[1]/(2*self.m)),self.length-12, width=3)
            
        pygame.display.flip()

    #counts no of 1s and 2s and 
    def checkWin(self):

        #print("Entered correct function")
        #print(board)
        
        boolean_matrix = self.board == 1
        temp = np.full((self.m, self.m), -1)
        points1 = temp[boolean_matrix].flatten().size
        points2 = self.m*self.m - points1

        if points1 > points2:
            return 1
        elif points2 > points1:
            return 2
        else:
            return 0


