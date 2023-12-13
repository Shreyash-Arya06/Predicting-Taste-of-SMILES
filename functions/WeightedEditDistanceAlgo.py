class WeightedEditDistance:
    def __init__(self, seq1, seq2, ins_weight = 1, del_weight = 1, subs_weight = 1):
        self.seq1 = seq1
        self.seq2 = seq2
        self.ins_weight = ins_weight
        self.del_weight = del_weight
        self.subs_weight = subs_weight

    def calculateDist(self, m, n):
        grid = [[0 for i in range(m+1)] for j in range(n+1)]        # Initializing the matrix
        
        for i in range(n+1):
            for j in range(m+1):

                if j == 0:
                    grid[i][j] = i * self.del_weight
                elif i == 0:
                    grid [i][j] = j * self.ins_weight
                # First row and column of the matrix is initialized
                elif self.seq1[i-1] == self.seq2[j-1]:
                    grid[i][j] = grid[i-1][j-1]
                else:
                    grid[i][j] = min(grid[i-1][j-1] + self.subs_weight, grid[i-1][j] + self.del_weight, grid[i][j-1] + self.ins_weight)

        return grid[n][m]

    def getScore(self):
        m = len(self.seq2)
        n = len(self.seq1)

        if (abs(m-n)<5):        # Here I have considered only differences that is less than 5 because otherwise it is undoubtedly dissimilar
            dist = self.calculateDist(m, n)
            score = 1 - (dist/max(m, n))
        else:
            return None
        
        return score
