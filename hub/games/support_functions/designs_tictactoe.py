import pygame

from pygame.locals import*
backg=pygame.image.load('games/support_functions/images/connect4.png')
backg1=pygame.image.load('games/support_functions/images/tictactoe.png')

class background:

    # this initializes some common fonts used throughout the gameplay
    def __init__(self,size):
        self.font=pygame.font.SysFont('candara',int(3*size[0]/65),bold=False,italic=False)

    # this function is used to print text on the screen
    def draw_text(self,screen,text,font,text_color,x,y):
        img=font.render(text,True,text_color)

        # centers the image
        width,height=img.get_size()
        screen.blit(img,(x-width/2,y-height/2))

    # A function purely used for aesthetics
    def welcome_tictactoe(self,screen,size,m):
        background1=pygame.transform.smoothscale(backg1, (size[0], size[1]))
        screen.blit(background1,(0,0))

        # Makes a grid
        for i in range(m):
            pygame.draw.line(screen,(0,0,0),(0,i*size[1]/m),(size[0],i*size[1]/m),width=1)
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=1)

        pygame.draw.line(screen,(0,0,0),(0,size[1]-1),(size[0],size[1]-1),width=1)
        pygame.draw.line(screen,(0,0,0),(size[0]-1,0),(size[0]-1,size[1]),width=1)

        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],size[0]/13])
        self.draw_text(screen,f"Tic Tac Toe",self.font,(255,255,255),size[0]/2,size[1]+3*size[0]/65)

    # this function actually builds the grid the game is played on
    def set_screen_tictactoe(self,screen,size,m):
        screen.fill((0,0,0))

        background1=pygame.transform.smoothscale(backg1, (size[0], size[1]))
        screen.blit(background1,(0,0))

        # Makes a grid
        for i in range(m):
            pygame.draw.line(screen,(0,0,0),(0,i*size[1]/m),(size[0],i*size[1]/m),width=1)
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m,0),(i*size[0]/m,size[1]),width=1)

        pygame.draw.line(screen,(0,0,0),(0,size[1]-1),(size[0],size[1]-1),width=2)
        pygame.draw.line(screen,(0,0,0),(size[0]-1,0),(size[0]-1,size[1]),width=2)

    # this is the function Game() calls to draw disks
    def update_display_tictactoe(self,cell,size,m,screen,Turn_id):
        # This is the function that X's and O's
        length=(size[0]+size[1])/(4*m)

        if Turn_id==1:
            pygame.draw.line(screen,(150,50,100),(cell[0]-length+9*size[0]/650,cell[1]-length+9*size[0]/650),(cell[0]+length-9*size[0]/650,cell[1]+length-9*size[0]/650),width=5)
            pygame.draw.line(screen,(150,50,100),(cell[0]+length-9*size[0]/650,cell[1]-length+9*size[0]/650),(cell[0]-length+9*size[0]/650,cell[1]+length-9*size[0]/650),width=5)

        else:
            pygame.draw.aacircle(screen,(0,0,128),cell,length-size[0]/130,width=3)

        pygame.display.flip()

    # It points it out if a match of 4 has been made by highlighting it
    def highlight_tictactoe(self,indices,screen,size,m,Turn_id):
        for pair in indices:
            row,column=pair[0],pair[1]
            cell=(size[0]/m,size[1]/m)
            
            pygame.draw.rect(screen,(255, 248, 230),rect=[cell[0]*column+3*size[0]/650,cell[1]*row+3*size[0]/650,cell[0]-4*size[0]/650,cell[1]-4*size[0]/650])

            self.update_display_tictactoe((cell[0]*(column+0.5),cell[1]*(row+0.5)),size,m,screen,Turn_id)

    # writes whose turn it is in the panel at the bottom of the screen
    def switch_player_tictactoe(self,screen,size,Turn,player1,player2):
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],size[0]/13])

        if Turn==player1:
            self.draw_text(screen,f"{player1}(X)'s turn",self.font,(255,255,255),size[0]/2,size[1]+3*size[0]/65)
        
        else:
            self.draw_text(screen,f"{player2}(O)'s turn",self.font,(255,255,255),size[0]/2,size[1]+3*size[0]/65)