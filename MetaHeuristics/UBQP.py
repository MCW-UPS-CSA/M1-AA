# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ~ ~ ~ ~ ~ Unconstrained Binary Quadratic Problems ~ ~ ~ ~ ~ ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ Functions ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from copy import copy

def dataLoader(fileName): #loads integer data in a line matrix
    myFile = open(fileName, 'r')
    linesList = myFile.readlines()
    myData = [[int(val) for val in line.split()] for line in linesList[0:]]
    return myData
def dataHeader(mat):
    return mat[0][:]
def toMatrix(lineMatrix): #turns line matrix to square matrix
    lineMatrix = lineMatrix[0][2:]
    position = 0
    toMatrix = [[0 for i in range(0,size,1)] for j in range(0,size,1)] 
    for i in range(0,size,1):
        for j in range(0,size,1):#must be converted to in
            toMatrix[i][j] = lineMatrix[position]
            position += 1
    return toMatrix
def f(X): #calculates the value of f(X) for a given X
    F = 0
    for i in range(0,size,1):
        for j in range(0,size,1):
            F += matrix[i][j] * X[i] * X[j]
    return F
def genSol(): #generates an initial solution Sol
    import random
    return [random.randint(0,1) for i in range(0,size,1)]
def latterSolBetter(s,sp): # returns if the latter solution is better than the first one
    isBetter = False
    if f(sp) < f(s):
        isBetter = True
    return isBetter
def respectsConstraints(sp): # returns if the solution respects the constraints
    isRespected = False
    if f(sp) > constraint:
        isRespected = True
    return isRespected
def getNeighbour(sol,pos): # returns 1 neighbour of a solution
    neighbour = copy(sol)
    if sol[pos] == 0:
        neighbour[pos] = 1
    elif sol[pos] == 1:
        neighbour[pos] = 0
    else:
        print("Undefined behavior!")
    return neighbour
def getBestSolFrom(initialS,newS): # returns the best solution between two w.r.t. constraints
    if useConstraint:
        if respectsConstraints(initialS):
            if respectsConstraints(newS):
                if latterSolBetter(initialS,newS):
                    return newS
                else:
                    return initialS
            else:
                return initialS
        elif respectsConstraints(newS):
            return newS
        else:
            if latterSolBetter(initialS,newS):
                return initialS
            else:
                return newS
    else:
        if latterSolBetter(initialS,newS):
            return newS
        else:
            return initialS
def bestNeighbour(s): #returns the best neighbour for a solution
    bestSol = copy(s)
    for i in range(0,size,1):
        sp = getNeighbour(s,i)
        bestSol = copy(getBestSolFrom(bestSol,sp))
    return bestSol
def steepestHillClimbing(startingSol): #returns the local min value of the function
    nrMoves = 0; stop = False; s = copy(startingSol)
    while nrMoves < maxMoves and stop == False:
        lastBestSol = copy(s)
        sp = bestNeighbour(s)
        s = copy(getBestSolFrom(s,sp))
        if s == lastBestSol:
            stop = True
        nrMoves += 1
    return s
def start_SteepestHillClimbing(): # implements a restart for the local min function
    attempts = 0; s = genSol(); lastBestSol = copy(s)
    while attempts < maxAttempts:
        if attempts > 0:
            s = genSol()
        iterSol = steepestHillClimbing(s)
        lastBestSol = copy(getBestSolFrom(lastBestSol,iterSol))
        attempts += 1
    return lastBestSol
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def isTabu(s): # returns if a solution is part or not of the tabu list
    if nrTabus == 0:
        return False
    else:
        for i in range(0,nrTabus,1):
            if s == TabuList[i]:
                return True
    return False
def nrNonTabuNeighbours(s): # returns the number of non-tabu neighbours
    nonTabuNeighbours = 0
    for i in range(0,size,1):
        sp = getNeighbour(s,i)
        if isTabu(sp) == False:
            nonTabuNeighbours += 1
    return nonTabuNeighbours
def best_NonTabu_Neighbour(s): # returns the best non-tabu neighbour of a solution
    bestSol = copy(s)
    for i in range(0,size,1):
        sp = getNeighbour(s,i)
        if isTabu(sp) == False:
            bestSol = copy(getBestSolFrom(bestSol,sp))
    return bestSol
def TabuMethod(startingSol): # returns local min of the function using a tabu list
    global nrTabus
    nrMoves = 0; stop = False; lastBestSol = copy(startingSol)
    while nrMoves < maxMoves and stop == False:
        if nrNonTabuNeighbours(lastBestSol) !=0:
            sp = best_NonTabu_Neighbour(lastBestSol)
        else:
            stop = True
        TabuList[nrMoves % maxTabus] = copy(sp)
        if maxTabus > nrTabus:
            nrTabus += 1
        lastBestSol = copy(getBestSolFrom(lastBestSol,sp))
        nrMoves += 1
    return lastBestSol
def start_TabuMethod(): # implements a restart for the tabu method
    global nrTabus
    attempts = 0; s = genSol(); lastBestSol = copy(s)
    while attempts < maxAttempts:
        nrTabus = 0
        if attempts > 0:
            s = genSol()
        iterSol = TabuMethod(s)
        lastBestSol = copy(getBestSolFrom(lastBestSol,iterSol))
        attempts += 1
    return lastBestSol
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ Main part of the program ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
fileName = ["partition6.txt","graphe12345.txt"]
maxMoves = 5; maxAttempts = 5; maxTabus = 3; useConstraint = True; nrTabus = 0

matrix = dataLoader(fileName[0]) #load initial data

header = dataHeader(matrix) #get the size and the p
size = header[0]; constraint = header[1]

matrix = toMatrix(matrix) # obtain the system matrix

print("Steepest Hill Climbing:")
solution = start_SteepestHillClimbing()
print("Final solution: ",solution)
print("Final value of f(X): ",f(solution))

print("Tabu Method:")
TabuList = [[0 for i in range(0,size,1)] for j in range(0,maxTabus,1)]
z = start_TabuMethod()
print("Final solution: ",z)
print("Final value of f(X): ",f(z))