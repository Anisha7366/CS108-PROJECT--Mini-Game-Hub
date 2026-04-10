import pygame,sys
pygame.init()

from games.connect4 import connect4
from games.tictactoe import tictactoe

player1,player2=sys.argv[1],sys.argv[2]
game_over=True

size=(700,700)

# sets the display
screen=pygame.display.set_mode(size)

while game_over:
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
                    if mouse_position[1]<=size[1]/2:
                          play=connect4(player1,player2,size,7,4)
                          play.actual_game()
                    
                    else:
                          play=tictactoe(player1,player2,size,10,5)
                          play.actual_game()
                    
# pygame.quit()
# sys.exit() 