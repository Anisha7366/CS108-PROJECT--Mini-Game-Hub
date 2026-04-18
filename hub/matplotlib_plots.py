# this file generates the matplotlib plots as pictures - a few sample pictures have been commited - they are not final, it generates pictures in every run
# collections counter helped in making win, loss, draw dictionarys as well aw the number of times each game was played
import matplotlib, numpy as np, collections

# this ensured matplotlib did not use a backend window for plotting(it messes up with the pygame window)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# uses load_data and gives a np.array - this is used to generate respective dictionaries/ arrays for plotting
from handling_history_csv import history

# called in game.py
class plot:
    def __init__(self,player1,player2):

        # returns an array(self,data) of data in history.csv 
        history_obj=history(player1,player2)
        self.data=history_obj.load_history()

        # as history.csv is stored as (player1,status,player2,status,date,game_name)
        # this slices player1,status and player2,status and attaches both of them
        self.stats_array1=self.data[:,:2]
        self.stats_array2=self.data[:,2:4]
        self.stats_array=np.append(self.stats_array1,self.stats_array2,axis=0)

        # from stats array return indices where the player is a winner, then check those indices for repeats through collection counter and put them in a dictionary
        self.win_indices=np.where(self.stats_array[:,1]=="winner")
        self.win_count=collections.Counter(self.stats_array[self.win_indices][:,0])
        self.win_dict=dict(self.win_count)

        # from stats array return indices where the player is a loser, then check those indices for repeats through collection counter and put them in a dictionary
        self.loss_indices=np.where(self.stats_array[:,1]=="loser")
        self.loss_count=collections.Counter(self.stats_array[self.loss_indices][:,0])
        self.loss_dict=dict(self.loss_count)

        # from stats array return indices where the has drawed, then check those indices for repeats through collection counter and put them in a dictionary
        self.draw_indices=np.where(self.stats_array[:,1]=="draw")
        self.draw_count=collections.Counter(self.stats_array[self.draw_indices][:,0])
        self.draw_dict=dict(self.draw_count)

        # just for displaying on the charts
        self.player1=player1
        self.player2=player2

    # generates the plots and saves them as 4 images
    def charts(self):

        # these functions use the init arrays and return these arrays
        # 1. pie chart of games played by frequency
        times_played,Labels,colors=self.pie_chart_arrays()

        # 2. bar graph of top 5 players by win count
        names,wins=self.sorted_win_lists()

        # 3. bar graph of wins,losses,draws of player 1
        names2,p1=self.player1_lists()

        # 4. bar graph of wins,losses,draws of player 1
        names3,p2=self.player2_lists()

        # 1. pie chart of gameplay frequency
        # just the size that had a good resolution
        plt.figure(figsize=(2.6,2.8))

        # making the chart
        plt.pie(times_played,labels=Labels,colors=colors,autopct='%1.0f%%')
        plt.title('Most Played Games by frequency')

        # saving it as an image, bbox_inches,dpi are all for resolution
        plt.savefig('plot_pictures/pie.png',bbox_inches='tight',dpi=100)
        plt.close()

        # 2. bargraph of top 5 players by win count
        plt.figure(figsize=(3.2,3))

        bar=plt.bar(names,wins,color="black")
        plt.bar_label(bar)
        plt.ylabel("Number of Wins")
        plt.xlabel("Player name")
        plt.title(f"Top {len(names)} players by win count")
        plt.savefig('plot_pictures/win.png',bbox_inches='tight',dpi=100)
        plt.close()

        # 3. bar graph of wins,draws,losses of player 1
        plt.figure(figsize=(3.2,3))

        bar=plt.bar(names2,p1,color="orange")
        plt.bar_label(bar)
        plt.ylabel("Number of games")
        plt.title(f"{self.player1}'s stats")
        plt.savefig('plot_pictures/p1.png',bbox_inches='tight',dpi=100)
        plt.close()

        # 4. bargraph of wins,draws,losses of player2
        plt.figure(figsize=(3.2,3))

        bar=plt.bar(names3,p2,color="lightgreen")
        plt.bar_label(bar)
        plt.ylabel("Number of games")
        plt.title(f"{self.player2}'s stats")
        plt.savefig('plot_pictures/p2.png',bbox_inches='tight',dpi=100)
        plt.close()
    
    # this function takes the arrays generated in init and returns arrays that can be used to plot
    def pie_chart_arrays(self):
        games_played=collections.Counter(self.data[:,-1])
        times_played=np.array([games_played['Tic-Tac-Toe'],games_played['Othello'],games_played['Connect FOUR']])
        Labels=[f'TicTacToe - {games_played["Tic-Tac-Toe"]}',f'Othello - {games_played["Othello"]}',f'Connect FOUR - {games_played["Connect FOUR"]}']
        colors=((1,192/255,203/255),(238/255,130/255,238/255),(0,1,230/255))

        return times_played,Labels,colors
    
    def sorted_win_lists(self):

        # sorting the win_dict by win count
        keys=list(self.win_dict.keys())
        new_keys=sorted(keys,key= lambda x:-self.win_dict[x])
        sorted_win_dict={}

        for key in new_keys:
            sorted_win_dict[key]=self.win_dict[key]

        # this is to ensure that if 5 players haven't played yet then the program still returns and doesn't give error, just plot the number of players already there
        if len(list(sorted_win_dict.keys()))>=5:
            return list(sorted_win_dict.keys())[0:5],list(sorted_win_dict.values())[0:5]
        
        return list(sorted_win_dict.keys()),list(sorted_win_dict.values())
    
    def player1_lists(self):
        
        # if the player is not in the respective dict, set 0, else give howmany games the player won/drawed/lost
        if self.player1 not in self.win_dict.keys():
            win=0
        else:
            win=self.win_dict[self.player1]
        
        if self.player1 not in self.loss_dict.keys():
            loss=0
        else:
            loss=self.loss_dict[self.player1]
        
        if self.player1 not in self.draw_dict.keys():
            draw=0
        else:
            draw=self.draw_dict[self.player1]

        # returns labels and values
        labels=["Won","Draw","Lost"]
        values=[win,draw,loss]
        return labels,values

    def player2_lists(self):
        
        # if the player is not in the respective dict, set 0, else give howmany games the player won/drawed/lost
        if self.player2 not in self.win_dict.keys():
            win=0
        else:
            win=self.win_dict[self.player2]
        
        if self.player2 not in self.loss_dict.keys():
            loss=0
        else:
            loss=self.loss_dict[self.player2]
        
        if self.player2 not in self.draw_dict.keys():
            draw=0
        else:
            draw=self.draw_dict[self.player2]
        
        # returns labels and values
        labels=["Won","Draw","Lost"]
        values=[win,draw,loss]
        return labels,values