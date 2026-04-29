import numpy as np

class base:
    
    def __init__(self,player1,player2,m,n):
        # These are the usernames passed as arguments to game.py
        self.player1,self.player2=player1,player2

        # Initializes turn 1 to player1
        self.Turn=self.player1

        # Turn_id helps in changing the 0s of the numpy array, basically as a token
        self.Turn_id=1

        # m = no. of columns in board(=np. of rows), n = the no. to match to win 
        self.m,self.n=m,n

        # initializes the numpy board
        self.board=np.zeros((self.m,self.m))
    
    def switch_player(self):
        if self.Turn==self.player1:
            self.Turn=self.player2
            self.Turn_id=2

        else:
            self.Turn=self.player1
            self.Turn_id=1
    
    def checkWin(self,indices):
        # checks win 
        if self.Horizontal(indices) or self.Vertical(indices) or self.Diagonal_right(indices) or self.Diagonal_left(indices):
            return True

        return False

    def Horizontal(self,indices):

        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,),axis=1)

        check_horizontal=np.all(windows,axis=2)

        if(np.any(check_horizontal)):
            row,col=np.where(check_horizontal==True)[0][0],np.where(check_horizontal==True)[1][0]
            self.Append(indices,row,col,'h')
            return True
        
        return False
        

        # if self.n==4:
        #     check_horizontal=player_positions[:,3:] & player_positions[:,2:self.m-1] & player_positions[:,1:self.m-2] & player_positions[:,:self.m-3]

        #     if np.any(check_horizontal):
        #         index=np.where(check_horizontal==True)
        #         one,two=index[0][0],index[1][0]
        #         indices.extend([(one,two),(one,two+1),(one,two+2),(one,two+3)])
        #         return True

        # if self.n==5:
        #     check_horizontal=player_positions[:,4:] & player_positions[:,3:self.m-1] & player_positions[:,2:self.m-2] & player_positions[:,1:self.m-3] & player_positions[:,:self.m-4]

        #     if np.any(check_horizontal):
        #         index=np.where(check_horizontal==True)
        #         one,two=index[0][0],index[1][0]
        #         indices.extend([(one,two),(one,two+1),(one,two+2),(one,two+3),(one,two+4)])
        #         return True
            
        return False

    def Vertical(self,indices):

        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,1))

        check_vertical=np.all(windows,axis=2)

        if(np.any(check_vertical)):
            row,col=np.where(check_vertical==True)[0][0],np.where(check_vertical==True)[1][0]
            self.Append(indices,row,col,'v')
            return True
        
        return False

    def Diagonal_right(self,indices):

        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,self.n))

        compare=np.full((1,self.n),True)

        check_diagonal=np.all(windows.diagonal(axis1=2,axis2=3)==compare,axis=2)

        if(np.any(check_diagonal)):
            row,col=np.where(check_diagonal==True)[0][0],np.where(check_diagonal==True)[1][0]
            self.Append(indices,row,col,'rd')
            return True
        
        return False
    
    def Diagonal_left(self,indices):

        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,self.n))

        compare=np.full((1,self.n),True)

        check_diagonal=np.all(np.flip(windows,axis=3).diagonal(axis1=2,axis2=3)==compare,axis=2)

        if(np.any(check_diagonal)):
            row,col=np.where(check_diagonal==True)[0][0],np.where(check_diagonal==True)[1][0]
            self.Append(indices,row,col,'ld')
            return True
        
        return False
    
    def Append(self,indices,row,col,parameter):
        if(parameter=='h'):
            for i in range(self.n):
                indices.append((row,col+i))
        elif(parameter=='v'):
            for i in range(self.n):
                indices.append((row+i,col))
        elif(parameter=='rd'):
            for i in range(self.n):
                indices.append((row+i,col+i))
        elif(parameter=='ld'):
            for i in range(self.n):
                indices.append((row+i,col+4-i))
        return

# issue faced - circular import