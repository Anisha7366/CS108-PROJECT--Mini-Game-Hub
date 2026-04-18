# This file contains the design of the different menus required throughout the game(the welcome screen, the prompt to quit, the sorting choice menu)
# everything that shows up on the screen is in this file(except the individual games ka designs)
# pygame imported for usable functions
import pygame

# called in game.py
class screens:

    # this initializes some common fonts used throughout the gameplay
    def __init__(self):
        self.font1=pygame.font.SysFont('Serif',50,bold=True,italic=False)
        self.font2=pygame.font.SysFont(None,45,bold=True,italic=False)
        self.font3=pygame.font.SysFont(None,30,bold=False,italic=False)

    # this function is used to print text on the screen
    def draw_text(self,screen,text,font,text_color,x,y):
        img=font.render(text,True,text_color)

        # centers the image
        width,height=img.get_size()
        screen.blit(img,(x-width/2,y-height/2))

    # Main menu - that offers 3 games to pick from
    def menu(self,screen,size):
        # Draws 3 rectangles that fill the screen (along with footer). Each rectangle has a game written on it
        pygame.draw.rect(screen,(255,192,203),rect=[0,0,size[0],size[1]/3])
        pygame.draw.rect(screen,(238,130,238),rect=[0,size[1]/3,size[0],size[1]/3])
        pygame.draw.rect(screen,(0,255,230),rect=[0,2*size[1]/3,size[0],size[1]/3])
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],50])

        # This draws black lines, seperating the rectangles, making a grid around the rectangles
        pygame.draw.line(screen,(0,0,0),(0,0),(size[0],0),width=5)
        pygame.draw.line(screen,(0,0,0),(0,size[1]/3),(size[0],size[1]/3),width=3)
        pygame.draw.line(screen,(0,0,0),(0,2*size[1]/3),(size[0],2*size[1]/3),width=3)
        pygame.draw.line(screen,(0,0,0),(0,size[1]),(size[0],size[1]),width=5)
        pygame.draw.line(screen,(0,0,0),(0,0),(0,size[1]),width=5)
        pygame.draw.line(screen,(0,0,0),(size[0]-1,0),(size[0]-1,size[1]),width=3)

        # This writes text on rectangles - declaring what game is called when a rectange is clicked
        self.draw_text(screen,"Tic-Tac-Toe!",self.font1,(0,0,0),size[0]/2,size[1]/6)
        self.draw_text(screen,"OTHELLO!",self.font1,(0,0,0),size[0]/2,size[1]/2)
        self.draw_text(screen,"Connect FOUR!",self.font1,(0,0,0),size[0]/2,5*size[1]/6)
        self.draw_text(screen,"Welcome! To pick a game, click anywhere in its box!",self.font3,(255,255,255),size[0]/2,size[1]+25)

        # show all the differences
        pygame.display.flip()
    
    # to be added
    def sort_by_what(self,screen):
        pass

    # This function makes a seperate screen that shows the pyplots/ stat images
    def picture(self,screen,size):

        screen.fill((0,0,0))

        # footer- "click anywhere to continue"
        self.footer(screen,size)

        # matplotlib_plots generates 4 different images - 4 because when all where generated together the quality was very bad and so was the plot fitting
        # plt.savefig is used, it saves the images which are then called here and displayed on the pygame window
        img1=pygame.image.load('plot_pictures/pie.png')

        # width,height of image=size/2 (not the first row because the pi chart and the bar graph needed different amt of space to look good)
        # the dimensions are a little skewed - i wanted a grid type of look, so the pictures are scaled as suuch

        # 1. pi chart - no. of times each game was played
        img1=pygame.transform.scale(img1,(size[0]/2-11,size[0]/2))
        img_rect=img1.get_rect()

        img_rect.top,img_rect.left=1,1

        # shows image on screen
        screen.blit(img1,img_rect)

        # 2. bar graph for the top 5 players by win count
        img2=pygame.image.load('plot_pictures/win.png')
        img2=pygame.transform.scale(img2,(size[0]/2+8,size[0]/2))
        img_rect=img2.get_rect()

        img_rect.top,img_rect.left=1,size[0]/2-9

        screen.blit(img2,img_rect)

        # 3. bar graph to show player 1's wins losses draws
        img3=pygame.image.load('plot_pictures/p1.png')
        img3=pygame.transform.scale(img3,(size[0]/2-2,size[0]/2-2))
        img_rect=img3.get_rect()

        img_rect.top,img_rect.left=size[0]/2+2,1

        screen.blit(img3,img_rect)

        # 4. bar graph to show player 2's wins losses draws
        img4=pygame.image.load('plot_pictures/p2.png')
        img4=pygame.transform.scale(img4,(size[0]/2-1,size[0]/2-2))
        img_rect=img4.get_rect()

        img_rect.top,img_rect.left=size[0]/2+2,size[0]/2

        screen.blit(img4,img_rect)

        # shows the final changes
        pygame.display.flip()

    # This is the screen that will show at the end and ask people if they want to keep playing or quit
    def prompt_to_quit(self,screen,size):
        # Draws two rectangles that fill the screen (along with footer). Each has a choice written on it.
        pygame.draw.rect(screen,(0,0,0),rect=[0,0,size[0],size[1]/2])
        pygame.draw.rect(screen,(255,255,255),rect=[0,size[1]/2,size[0],size[1]/2])
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],50])

        # Makes a small grid, defining the edges around the rectangles
        pygame.draw.line(screen,(255,255,255),(0,0),(size[0],0),width=3)
        pygame.draw.line(screen,(0,0,0),(0,size[1]),(size[0],size[1]),width=3)
        pygame.draw.line(screen,(255,255,255),(0,0),(0,size[1]/2),width=3)
        pygame.draw.line(screen,(255,255,255),(size[0],0),(size[0],size[1]/2),width=3)
        pygame.draw.line(screen,(0,0,0),(0,size[1]/2),(0,size[1]),width=3)
        pygame.draw.line(screen,(0,0,0),(size[0],size[1]/2),(size[0],size[1]),width=3)

        # Writes text on the rectangles to offer choices, the footer
        self.draw_text(screen,"Return to the menu and Replay?",self.font2,(255,255,255),size[0]/2,size[1]/4)
        self.draw_text(screen,"Quit?",self.font2,(0,0,0),size[0]/2,3*size[1]/4)
        self.draw_text(screen,"To pick a choice, click anywhere in its box!",self.font3,(255,255,255),size[0]/2,size[1]+25)

        # shows the changes
        pygame.display.flip()

    # This is a footer that shows up throughout - during the games it tells whose turn it is, otherwise it has basic instructions - like click to continue
    def footer(self,screen,size):
        # fills the rectangle, always before writing anything to prevent overwriting
        pygame.draw.rect(screen,(0,0,0),rect=[0,size[1],size[0],50])

        # This footer is specific to the pyplots screen, but maybe i'll generalize it
        self.draw_text(screen,"Click anywhere to Continue",self.font3,(255,255,255),size[0]/2,size[1]+25)