import pygame

from pygame.locals import*
backg=pygame.image.load('games/support_functions/images/connect4.png')
backg1=pygame.image.load('games/support_functions/images/tictactoe.png')

class background:

    # this initializes some common fonts used throughout the gameplay
    def __init__(self):
        self.font=pygame.font.SysFont('candara',30,bold=False,italic=False)

    # this function is used to print text on the screen
    def draw_text(self,screen,text,font,text_color,x,y):
        img=font.render(text,True,text_color)

        # centers the image
        width,height=img.get_size()
        screen.blit(img,(x-width/2,y-height/2))
    
    # A function purely used for aesthetics
    def welcome(self,m,screen,size):
        background1=pygame.transform.smoothscale(backg, (size[0], size[1]))
        screen.blit(background1,(0,0))

        # Makes a grid
        for i in range(m):
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m-2,0),(i*size[0]/m-2,size[1]-4),width=1)
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m+2,0),(i*size[0]/m+2,size[1]-4),width=1)

        pygame.draw.line(screen,(0,0,0),(size[0]-1,0),(size[0]-1,size[1]-4),width=1)

        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1]-3,size[0],53])
        self.draw_text(screen,f"CONNECT 4",self.font,(255,255,255),size[0]/2,size[1]+30)

    # this function actually builds the grid the game is played on
    def set_screen(self,m,screen,size):
        background1=pygame.transform.smoothscale(backg, (size[0], size[1]))
        screen.blit(background1,(0,0))

        # Makes a grid
        for i in range(m):
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m-2,0),(i*size[0]/m-2,size[1]-4),width=1)
            pygame.draw.line(screen,(0,0,0),(i*size[0]/m+2,0),(i*size[0]/m+2,size[1]-4),width=1)

        pygame.draw.line(screen,(0,0,0),(size[0]-1,0),(size[0]-1,size[1]-4),width=1)
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1]-3,size[0],53])

    # this is the function Game() calls to draw disks
    def update_display(self,screen,cell,length,Turn_id):
        # This is the function that draws disks at a column

        if Turn_id==1:
            pygame.draw.aacircle(screen,(53,6,62),cell,length-20)

        else:
            pygame.draw.aacircle(screen,(0,0,139),cell,length-20)
    
    # It points it out if a match of 4 has been made by highlighting it
    def highlight(self,indices,screen,length,size,m,Turn_id):
        for pair in indices:
            row,column=pair[0],pair[1]
            cell=(size[0]/m,size[1]/m)
            
            pygame.draw.rect(screen,(255,255,255),rect=[cell[0]*column+3,cell[1]*row,cell[0]-4,cell[1]-2])

            self.update_display(screen,(cell[0]*(column+0.5),cell[1]*(row+0.5)),length,Turn_id)

    def switch_player(self,screen,size,Turn,player1,player2):
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],50])

        if Turn==player1:
            self.draw_text(screen,f"{player1}(Purple)'s turn",self.font,(255,255,255),size[0]/2,size[1]+30)
        
        else:
            self.draw_text(screen,f"{player2}(Blue)'s turn",self.font,(255,255,255),size[0]/2,size[1]+30)