from pycsp3 import *


#load data
nbrCell, nbrFreq, nbrTrans, distance = data

maxTrans = 0
for a in nbrTrans:
    if a > maxTrans :
        maxTrans = a


#make variable
freqs = VarArray( size = [nbrCell,maxTrans] , dom = range(nbrFreq+1))

#contraines
satisfy(
    #fill 0 for slot emty
    [freqs[k][i] == 0 for k in range(nbrCell) for i in range(nbrTrans[k], maxTrans) if nbrTrans[k] < maxTrans],

    #The distance between two transmitter frequencies within a cell must not be smaller than 16
    [(freqs[k][i] - freqs[k][j] >= 16) & (freqs[k][j] > 0) for k in range(nbrCell) for j in range(nbrTrans[k]-1) for i in range(j+1,nbrTrans[k])],

    #The distances between two transmitter frequencies from different cells vary according to their geographical situation and are described in a matrix
    [abs(freqs[k][i] - freqs[h][j]) >= distance[k][h] for h in range(nbrCell-1) for k in range(h+1,nbrCell) for i in range(nbrTrans[k]) for j in range(nbrTrans[h]) if distance[k][h]>0],
    
)

#Optimisation
minimize(
    NValues(freqs)
)