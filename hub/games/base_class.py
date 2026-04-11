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
        # for every row, every consecutive n element array in the row(which is obtained by splicing) is compared to a n element array(all elements are turn_id)
        # This returns an array of booleans. If they match exactly all elements will be true
        # if even one element doesn't match, it will be false and hence the product of the array will be 0
        compare=np.full((1,self.n),self.Turn_id)
        for i in range(0,self.m):
            for j in range(0,self.m-self.n+1):
                a=(self.board[i][j:j+self.n:1]==compare)
                if np.prod(a)!=0:

                    # This is just returning the indices so i can highlight when a win happens. It does not check for a win condition
                    for k in range (self.n):
                        indices.append((i,j+k))

                    return True
        return False

    def Vertical(self,indices):
        # similar to check horizontal
        # for every column, every consecutive n element array is matched and checked
        # for some reason the splicing gave a horizontal array so i compared it to a horizontal array
        compare=np.full((1,self.n),self.Turn_id)
        for i in range(0,self.m):
            for j in range(0,self.m-self.n+1):
                a=(self.board[j:j+self.n:1,i]==compare)
                if np.prod(a)!=0:

                    # This is just returning the indices so i can highlight the screen when a win happens. It does not check for a win condition
                    for k in range (self.n):
                        indices.append((j+k,i))

                    return True
        return False

    def Diagonal_right(self,indices):
        # this finds every n x n matrix (with consecutive rows and columns) and compares its diagonal to the full array(\)
        compare=np.full((1,self.n),self.Turn_id)
        for i in range (0,self.m-self.n+1):
            for j in range(0,self.m-self.n+1):
                sub_matr=self.board[i:i+self.n,j:j+self.n]
                diag=sub_matr.diagonal()
                a=(diag==compare)
                if np.prod(a)!=0:

                    # This is just returning the indices so i can highlight when a win happens. It does not check for a win condition
                    for k in range (self.n):
                        indices.append((i+k,j+k))

                    return True
        return False
    
    def Diagonal_left(self,indices):
        # This finds every n x n matrix (with consecutive rows and columns) and compares its alternate diagonal(/) to the full array
        compare=np.full((1,self.n),self.Turn_id)
        for i in range (0,self.m-self.n+1):
            for j in range(0,self.m-self.n+1):
                sub_matr=self.board[i:i+self.n,j:j+self.n]
                L_diag=np.fliplr(sub_matr).diagonal()
                a=(L_diag==compare)
                if np.prod(a)!=0:

                    # This is just returning the indices so i can highlight when a win happens. It does not check for a win condition
                    for k in range (self.n):
                        indices.append((i+k,j+self.n-1-k))
                        
                    return True
        return False

# issue faced - circular import