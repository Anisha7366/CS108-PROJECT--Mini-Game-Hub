# pygame for the GUI, sys for a clean exit, subprocess to call the bash files
import pygame,sys,subprocess

# initializes the pygame window
pygame.init()

# import the respective classes from games - connect4, tictactoe, othello
from games.connect4 import connect4
from games.tictactoe import tictactoe
from games.othello import othello

# Everything that is drawn on the pygame window from this file(except for the actual gameplay)- menu's,charts is done through functions in the screens class
# There was a lot of such designing, so for the modularity of the code i made a seperate python file
from support_functions.screen_interfaces import screens

# plot is a class that takes care of plotting the stats(makes arrays from data stored in history.csv), saving the plots as pictures which the screens class can load on the pygame window 
# this portion of the code was 100+ lines too so i put it in a seperate file as a class
from support_functions.matplotlib_plots import plot

# history class has functions to append the winner,loser,date,game_name to history.csv and also return the data in history.csv as an numpy array
# screens needed history so to avoid circular import, i moved it to a seperate file
from support_functions.handling_history_csv import history

# player inputs taken from the command line (bash script)
player1,player2=sys.argv[1],sys.argv[2]

# size according to taste, most of the game is very scalable but some part of it is not
size=(650,650)

# sets the display, the +50 acts as a footer(where  different messages will be displayed throughout the game)
screen=pygame.display.set_mode((size[0],size[1]+50))

# sets pygame window name
pygame.display.set_caption("May the odds be ever in your favor!")

# gameplay has the pygame logic - it calls the menu from screens, calls the plots, calls the final question menu and switches between them
class Gameplay:

    # making a screen object, this is used throughout to call the different displays
    def __init__(self):
        self.screen_display=screens()

    # This is the function that calls the menu and sets it up, according to choice calls the game and plays it
    def game(self):
        # shows menu on the display (game choices)
        self.screen_display.menu(screen,size)

        while True:

            # initial mouse position - just to initialize
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

                    # here an history object is created to append the stats. For each game winner, gamename is returned
                    history_obj=history(player1,player2)

                    # if click is in top 1/3rd of screen(excluding footer), tictactoe is called
                    if mouse_position[1]<=size[1]/3:
                        play=tictactoe(player1,player2,size,10,5)
                        winner,game_name=play.actual_game(),"Tic-Tac-Toe"
                          
                    # if click is in top 1/3rd-2/3rd of screen(excluding footer), othello is called
                    elif mouse_position[1]<=2*size[1]/3:
                        play=othello(player1,player2,size,8)
                        winner,game_name=play.actual_game(),"Othello"
                    
                    # if click is in bottom 1/3rd of screen(excluding footer), connect4 is called
                    elif mouse_position[1]<=size[1]:
                        play=connect4(player1,player2,size,7,4)
                        winner,game_name=play.actual_game(),"Connect FOUR"  
                    
                    # History obj was passed the player names, from knowing the winner it can now know the loser and append it to history.csv
                    history_obj.append_history(winner,game_name)
                    return
         
    # gui that allows people to choose a metric to sort the leaderboard by
    def sort(self):

        # designs the display
        self.screen_display.sort_by_what(screen,size)
        mouse_position=(0,0)
        
        while True:
            for event in pygame.event.get():

                # allows players to exit
                if event.type==pygame.QUIT:
                    pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_position=event.pos

                    # allows players to choose the metric, then runs the respective bash command using subprocess and prints the output on the terminal and returns
                    if mouse_position[1]<=size[1]/5:
                        sorted=subprocess.run('bash leaderboard.sh wins',shell=True,capture_output=True,text=True)
                        print(sorted.stdout)
                        return 
                    
                    elif mouse_position[1]<=2*size[1]/5:
                        sorted=subprocess.run('bash leaderboard.sh losses',shell=True,capture_output=True,text=True)
                        print(sorted.stdout)
                        return 
                    
                    elif mouse_position[1]<=3*size[1]/5:
                        sorted=subprocess.run('bash leaderboard.sh draws',shell=True,capture_output=True,text=True)
                        print(sorted.stdout)
                        return 
                    
                    elif mouse_position[1]<=4*size[1]/5:
                        sorted=subprocess.run('bash leaderboard.sh ratio',shell=True,capture_output=True,text=True)
                        print(sorted.stdout)
                        return 
                    
                    elif mouse_position[1]<=size[1]:
                        sorted=subprocess.run('bash leaderboard.sh total',shell=True,capture_output=True,text=True)
                        print(sorted.stdout)
                        return 
                    
    # This makes a plot object, calls charts functions(makes 4 pictures and stores them in plot_pictures) and uses screens which displays the picture on the pygame window       
    def plots(self):

        stats=plot(player1,player2)
        stats.charts()

        self.screen_display.picture(screen,size)

        # This takes care of the "click anywhere to continue part"
        while True:
            for event in pygame.event.get():
            # for quitting by x button
                if event.type==pygame.QUIT:
                    pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    return
                    
    # a question is prompted if they want to go back or continue, calls screens which displays the question, this takes care that if quit is called the window closes cleanly
    def final_screen(self):

        self.screen_display.prompt_to_quit(screen,size)
        mouse_position=(0,0)

        while True:
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
                        return

                    # if not, quit the game   
                    elif mouse_position[1]<=size[1]:
                        pygame.display.message_box("Bye Bye","We hope you had fun!","info",None,('OK',),0,None)
                        pygame.display.flip()
                        pygame.quit()
                        sys.exit()
    
# it can be seen that all of the gameplay functions return on mousebuttondown, this is so the gameplay can be given sequence, as shown below

# making a game object     
game=Gameplay()

# this gives it proper sequence(every function below just returns void and comes back, and hence executes the following function unless explicitly quitted)
while True:
    game.game()
    game.sort()
    game.plots()
    game.final_screen()