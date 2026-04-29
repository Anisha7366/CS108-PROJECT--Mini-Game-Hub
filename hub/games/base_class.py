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
    
    # method to switch players that is inherited
    def switch_player(self):
        if self.Turn==self.player1:
            self.Turn=self.player2
            self.Turn_id=2

        else:
            self.Turn=self.player1
            self.Turn_id=1
        
    # this function calls 4 functions that check if there is a win condition and return True/False
    def checkWin(self,indices):
        # checks win 
        if self.Horizontal(indices) or self.Vertical(indices) or self.Diagonal_right(indices) or self.Diagonal_left(indices):
            return True

        return False
    
    # to check for a horizontal match
    def Horizontal(self,indices):

        # This is an array with True at positions where it is Turn_id false otherwise
        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        # np.lib.stride_tricks.sliding_window_view returns windows(changing memory) that scan through the array
        # axis = 1 for this case because array is 2D and we need access only at the 2nd dimension(inside an element which is an array)
        # window is an 1D array of length n
        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,),axis=1)

        # check_horizontal returns a m-n + 1 x m array of bools with value of windows is a horizontal match 
        check_horizontal=np.all(windows,axis=2)

        # if any element of check_horizontal is true, return the index of element , append the n indices to indices (for highlighting win) return True
        if(np.any(check_horizontal)):
            row,col=np.where(check_horizontal==True)[0][0],np.where(check_horizontal==True)[1][0]
            self.Append(indices,row,col,'h')
            return True
        
        # else return True
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

    # to check for a vertical match
    def Vertical(self,indices):

        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        # axis != 1 for this case because array is 2D and we need access at both dimensions
        # window is an 3D array 
        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,1))

        # check_vertical returns a m x m -n + 1 array of bools with value of windows is a vertical match 
        check_vertical=np.all(windows,axis=2)

        # if any element of check_vertical is true, return the index of element , append the n indices to indices (for highlighting win) return True
        if(np.any(check_vertical)):
            row,col=np.where(check_vertical==True)[0][0],np.where(check_vertical==True)[1][0]
            self.Append(indices,row,col,'v')
            return True
        
        return False

    # to check for a right diagonal \ match
    def Diagonal_right(self,indices):

        # axis != 1 for this case because array is 2D and we need access at both dimensions
        # window is an 3D array 
        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,self.n))

        compare=np.full((1,self.n),True)

        # check_vertical returns a m -n + 1 x m -n + 1 array of bools with value of windows is a right diagonal match (diagonals match)
        check_diagonal=np.all(windows.diagonal(axis1=2,axis2=3)==compare,axis=2)

        # if any element of check_diagonal is true, return the index of element , append the n indices to indices (for highlighting win) return True
        if(np.any(check_diagonal)):
            row,col=np.where(check_diagonal==True)[0][0],np.where(check_diagonal==True)[1][0]
            self.Append(indices,row,col,'rd')
            return True
        
        return False
    
    # to check for a left diagonal / match
    def Diagonal_left(self,indices):
        
        # axis != 1 for this case because array is 2D and we need access at both dimensions
        # window is an 3D array 
        player_positions=(self.board==np.full((self.m,self.m),self.Turn_id))

        windows=np.lib.stride_tricks.sliding_window_view(player_positions,window_shape=(self.n,self.n))

        # check_vertical returns a m -n + 1 x m -n + 1 array of bools with value of windows is a left diagonal match (diagonals match)
        compare=np.full((1,self.n),True)

        check_diagonal=np.all(np.flip(windows,axis=3).diagonal(axis1=2,axis2=3)==compare,axis=2)

        # if any element of check_diagonal is true, return the index of element , append the n indices to indices (for highlighting win) return True
        if(np.any(check_diagonal)):
            row,col=np.where(check_diagonal==True)[0][0],np.where(check_diagonal==True)[1][0]
            self.Append(indices,row,col,'ld')
            return True
        
        return False
    
    # appends the winning indices to indices so that the respective cells can be highlighted in the pygame window
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
                indices.append((row+i,col+self.n-1-i))
        return

# issue faced - circular import