# csv to append and read from the csv files - and avoiding loops, numpy so that the data is loaded from history.csv as a np array, datetime used to append to history.csv
import csv, numpy as np,datetime

# this class is called in game.py and matplotlib_plots.py
class history:

    # this init function is used while appending as only the winners name is passed from game.py
    def __init__(self,player1,player2):
        self.player1=player1
        self.player2=player2

    # This loads data from histroy.csv as a 2d array , each line is an element and each comma seperated value is an individual element
    def load_history(self):
        with open('history.csv','r',newline='') as f:
            reader=csv.reader(f,delimiter=',')

            # direct np typecasting gave arbitary results, so i typecasted to a list first then an np.array
            reader=np.array(list(reader))

            return reader
    
    # this function adds rows to history.csv
    def append_history(self,winner,game_name):

        with open('history.csv','a',newline='') as f:
            writer=csv.writer(f)

            # like i said, winner is passed so loser can be known, game_name too is passed
            if winner==self.player1:
                writer.writerow([self.player1,"winner",self.player2,"loser",datetime.date.today(),game_name])

            elif winner==self.player2:
                writer.writerow([self.player1,"loser",self.player2,"winner",datetime.date.today(),game_name])
           
            else:
                # the case it is a draw, no winner, loser 
                writer.writerow([self.player1,"draw",self.player2,"draw",datetime.date.today(),game_name])
            
            return 