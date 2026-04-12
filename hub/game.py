import pygame,sys,csv,datetime
pygame.init()

# import the respective classes from games
from games.connect4 import connect4
from games.tictactoe import tictactoe

# initializing fonts for text - purely aesthetic
text_font=pygame.font.SysFont('Serif',50,bold=True,italic=False)
font2=pygame.font.SysFont('Roman',30,bold=True,italic=False)

# this function is used to print text on the screen
def draw_text(text,font,text_col,x,y):
      img=font.render(text,True,text_col)
      width,height=img.get_size()
      screen.blit(img,(x-width/2,y-height/2))

# This acts as our menu where someboy can pick tictactoe,othello,connect3 by clicking anywhere in their respective boxes
def menu(screen):
    pygame.draw.rect(screen,(255,192,203),rect=[0,0,size[0],size[1]/3])
    pygame.draw.rect(screen,(238,130,238),rect=[0,size[1]/3,size[0],size[1]/3])
    pygame.draw.rect(screen,(0,255,230),rect=[0,2*size[1]/3,size[0],size[1]/3])

    pygame.draw.line(screen,(0,0,0),(0,0),(size[0],0),width=3)
    pygame.draw.line(screen,(0,0,0),(0,size[1]/3),(size[0],size[1]/3),width=2)
    pygame.draw.line(screen,(0,0,0),(0,2*size[1]/3),(size[0],2*size[1]/3),width=2)
    pygame.draw.line(screen,(0,0,0),(0,size[1]),(size[0],size[1]),width=3)
    pygame.draw.line(screen,(0,0,0),(0,0),(0,size[1]),width=3)
    pygame.draw.line(screen,(0,0,0),(size[0],0),(size[0],size[1]),width=3)

    draw_text("Tic-Tac-Toe!",text_font,(0,0,0),size[0]/2,size[1]/6)
    draw_text("OTHELLO!",text_font,(0,0,0),size[0]/2,size[1]/2)
    draw_text("Connect FOUR!",text_font,(0,0,0),size[0]/2,5*size[1]/6)

    pygame.display.flip()

# This is the prompt that will show at the end(after leaderboard.sh has been worked on) and ask people if they want to keep playing or quit
def prompt_to_quit(screen):
    pygame.draw.rect(screen,(0,0,0),rect=[0,0,size[0],size[1]/2])
    pygame.draw.rect(screen,(255,255,255),rect=[0,size[1]/2,size[0],size[1]/2])

    pygame.draw.line(screen,(255,255,255),(0,0),(size[0],0),width=3)
    pygame.draw.line(screen,(0,0,0),(0,size[1]),(size[0],size[1]),width=3)
    pygame.draw.line(screen,(255,255,255),(0,0),(0,size[1]/2),width=3)
    pygame.draw.line(screen,(255,255,255),(size[0],0),(size[0],size[1]/2),width=3)
    pygame.draw.line(screen,(0,0,0),(0,size[1]/2),(0,size[1]),width=3)
    pygame.draw.line(screen,(0,0,0),(size[0],size[1]/2),(size[0],size[1]),width=3)

    draw_text("Click here to return to the menu and replay!",font2,(255,255,255),size[0]/2,size[1]/4)
    draw_text("Click here to quit!",font2,(0,0,0),size[0]/2,3*size[1]/4)

    pygame.display.flip()

# player inputs taken from the command line (bash script)
player1,player2=sys.argv[1],sys.argv[2]

# size according to taste
size=(700,700)


# sets the display
screen=pygame.display.set_mode(size)
pygame.display.set_caption("May the odds be ever in your favor!")

# This is the function that calls the menu and sets it up, according to choice calls the game and plays it
def game():

    # menu function 
    menu(screen)

    game_over=False

    while not game_over:

        # initial mouse position- just to initialize
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
                mouse_position=event.pos

                # if click is in top 1/3rd of screen, tictactoe is called
                if mouse_position[1]<=size[1]/3:
                    play=tictactoe(player1,player2,size,10,5)
                    return (play.actual_game(),"Tic-Tac-Toe")
                
                # if click is in top 1/3rd-2/3rd of screen, othello is called
                elif mouse_position[1]<=2*size[1]/3:
                    pass
                #     play=tictactoe(player1,player2,size,8)
                #     return (play.actual_game(),"Othello")

                # if click is in bottom 1/3rd of screen, connect4 is called
                else:
                    play=connect4(player1,player2,size,7,4)
                    return (play.actual_game(),"Connect FOUR")

# This function is the one that calls the menu, games AND appends the player names, game status, date, game_name to history.csv              
def play_game_and_append():              
    winner,game_name=game()
    if winner==player1:
        
        f=open("history.csv","a",newline="")
        writer=csv.writer(f)
        writer.writerow([player1,"winner",player2,"loser",datetime.date.today(),game_name])
        f.close()

    elif winner==player2:
    
        f=open("history.csv","a",newline="")
        writer=csv.writer(f)
        writer.writerow([player1,"loser",player2,"winner",datetime.date.today(),game_name])
        f.close()
    
    else:
        # the case it is a draw, no winner, loser 
        f=open("history.csv","a",newline="")
        writer=csv.writer(f)
        writer.writerow([player1,"draw",player2,"draw",datetime.date.today(),game_name])
        f.close()

# This is the initial game menu - which is launched regardless
play_game_and_append()

# After initial game, a question is prompted if they want to go back or continue- an infinite while loop until quit
while True:
        prompt_to_quit(screen)
        mouse_position=(0,0)

        for event in pygame.event.get():
            # for quitting by x button
            if event.type==pygame.QUIT:
                pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                pygame.display.flip()
                pygame.quit()
                sys.exit()
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_position=event.pos
                # if choice is to go back, replay the game
                if mouse_position[1]<=size[1]/2:
                    play_game_and_append()

                # if not, quit the game   
                else:
                    pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()

# other functionalities like leaderboard.sh, pycharts will be done eventually