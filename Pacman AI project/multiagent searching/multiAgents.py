# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # start with a base score
        score = 1000

        foodList = newFood.asList()
        oldFoodQty = len(currentGameState.getFood().asList())
        newFoodQty = len(foodList)

        if len(foodList)==0:
          return 9999
        elif newFoodQty == oldFoodQty:      # penalty if the pacman is not eating pellets
          score = score - 100

        nearestFood = 999999
        currentDist = min(manhattanDistance(pos, newPos) for pos in foodList)
        if currentDist < nearestFood:
            nearestFood = currentDist
        score = score + 1.0 / (1 + nearestFood)

        GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates]
        if len(GhostPositions) ==0:
          score = score + 1000
        else: 
          g1dist = (manhattanDistance(newPos,GhostPositions[0]))
          g2dist = 1000000
          if len(GhostPositions) > 1:
            g2dist = (manhattanDistance(newPos,GhostPositions[1]))
          
          gdist = min(g1dist,g2dist)
          # find nearest ghost of 2
          if gdist < 3:
            score = -99999
          score = score - 1.0 / (1 + gdist)
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"        
        numOfGhosts = gameState.getNumAgents() - 1
        # exclude pacman agent
        legalActions = gameState.getLegalActions()
        
        score = -999999
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            currentScore = score
            score = max(score, minvalue(1, nextState, self.depth, numOfGhosts, self.evaluationFunction))
            if score > currentScore:
                returnVal = action

        if score == -999999:
          return Directions.STOP

        return returnVal

def maxvalue(gameState, depth, numOfGhosts, evalFn):
    # agentIndex will always be 0 (pacman) for max function
    pacmanAgentIndex = 0
    # the next minimax call will be to the first ghost of current depth
    firstGhostIndex = 1

    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)

    # non-terminal case    
    returnVal = -999999
    legalActions = gameState.getLegalActions(pacmanAgentIndex)
    for action in legalActions:
        nextState = gameState.generateSuccessor(pacmanAgentIndex, action)
        returnVal = max(returnVal, minvalue(firstGhostIndex, nextState, depth, numOfGhosts, evalFn))
    return returnVal

def minvalue(agentindex, gameState, depth, numOfGhosts, evalFn):
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)
    returnVal = 999999
    legalActions = gameState.getLegalActions(agentindex)

    if agentindex == numOfGhosts: # last ghost in this depth will call the max (pacman) for the next depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = min(returnVal, maxvalue(nextState, depth - 1, numOfGhosts, evalFn))
    else: # another ghost in the same depth, will call the min (next ghost) in same depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = min(returnVal, minvalue(agentindex + 1, nextState, depth,  numOfGhosts, evalFn))
    return returnVal


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numOfGhosts = gameState.getNumAgents() - 1
        # exclude pacman agent
        legalActions = gameState.getLegalActions()
        
        # initial values
        alpha = -float("inf")
        beta = float("inf")
        score = -float("inf")


        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            currentScore = score
            score = max(score, minBetaValue(1, nextState, self.depth, numOfGhosts, self.evaluationFunction, alpha, beta))
            if score > currentScore:
              returnVal = action
            if score > beta:
              return returnVal
            alpha = max(alpha, score)

        if score == -float("inf"):
          return Directions.STOP

        return returnVal

def maxAlphaValue(gameState, depth, numOfGhosts, evalFn, alpha, beta):
    # agentIndex will always be 0 (pacman) for max function
    pacmanAgentIndex = 0
    # the next minimax call will be to the first ghost of current depth
    firstGhostIndex = 1

    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)

    # non-terminal case    
    returnVal = -float("inf")
    legalActions = gameState.getLegalActions(pacmanAgentIndex)
    for action in legalActions:
        nextState = gameState.generateSuccessor(pacmanAgentIndex, action)
        returnVal = max(returnVal, minBetaValue(firstGhostIndex, nextState, depth, numOfGhosts, evalFn, alpha, beta))
        if returnVal > beta:
          return returnVal
        alpha = max(alpha, returnVal)
    return returnVal

def minBetaValue(agentindex, gameState, depth, numOfGhosts, evalFn, alpha, beta):
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)
    returnVal = float("inf")
    legalActions = gameState.getLegalActions(agentindex)

    if agentindex == numOfGhosts: # last ghost in this depth will call the max (pacman) for the next depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = min(returnVal, maxAlphaValue(nextState, depth - 1, numOfGhosts, evalFn, alpha, beta))
            if returnVal < alpha:
              return returnVal
            beta = min(beta, returnVal)
    else: # another ghost in the same depth, will call the min (next ghost) in same depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = min(returnVal, minBetaValue(agentindex + 1, nextState, depth, numOfGhosts, evalFn, alpha, beta))
            if returnVal < alpha:
              return returnVal
            beta = min(beta, returnVal)
    return returnVal


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numOfGhosts = gameState.getNumAgents() - 1
        # exclude pacman agent
        legalActions = gameState.getLegalActions()
        
        score = -999999
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            currentScore = score
            score = max(score, expectiMinvalue(1, nextState, self.depth, numOfGhosts, self.evaluationFunction))
            if score > currentScore:
                returnVal = action
        if score == -999999:
            return Directions.STOP
        return returnVal

def expectiMaxvalue(gameState, depth, numOfGhosts, evalFn):
    # agentIndex will always be 0 (pacman) for max function
    pacmanAgentIndex = 0
    # the next minimax call will be to the first ghost of current depth
    firstGhostIndex = 1

    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)

    # non-terminal case    
    returnVal = -999999
    legalActions = gameState.getLegalActions(pacmanAgentIndex)
    for action in legalActions:
        nextState = gameState.generateSuccessor(pacmanAgentIndex, action)
        returnVal = max(returnVal, expectiMinvalue(firstGhostIndex, nextState, depth, numOfGhosts, evalFn))
    return returnVal

def expectiMinvalue(agentindex, gameState, depth, numOfGhosts, evalFn):
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return evalFn(gameState)
    returnVal = 0
    legalActions = gameState.getLegalActions(agentindex)

    if agentindex == numOfGhosts: # last ghost in this depth will call the max (pacman) for the next depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = returnVal + expectiMaxvalue(nextState, depth - 1, numOfGhosts, evalFn)
    else: # another ghost in the same depth, will call the min (next ghost) in same depth
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentindex, action)
            returnVal = returnVal + expectiMinvalue(agentindex + 1, nextState, depth,  numOfGhosts, evalFn)
    
    returnVal = returnVal / len(legalActions)
    return returnVal


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 

      ALGORITHM :
      - if it is a win or lose state, then return a corresponding value
      - if not; get the current score from the evaluation function (we change it according to our
                                                                    observations of the state)
      - OBSERVATIONS (features):
        -- find the closest food pellet
        -- find the power pellets
        -- find the distance to the nearest ghost
        -- find all the scared ghost
      
      - SCORING: 
        -- (1) further the nearest food, longer the time required for pacman to reach it, lower the score
        -- (2) more the remaining food, lower the score
        -- (3) more the remaining capsules, lower the score
        -- (4) closer the ghost, higher the danger, lower the score
        -- (5) for every scared ghost, the state is desired, so increase the score

        [NOTE: 
            - Details of scoring mentioned in comments next to code below (referenced by numbers in above list)
            - Reciprocal values taken for importrant features
            - Multiplying factors are determined by trial and error 
              (priority given to features after observing what the pacman fails to do on the maze)]


    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return 999999
    if currentGameState.isLose():
        return -999999

    score = scoreEvaluationFunction(currentGameState)
    pacmanPos = currentGameState.getPacmanPosition()

    # find nearest food
    newFood = currentGameState.getFood()
    foodPos = newFood.asList()
    nearestFood = 999999
    currentDist = min(manhattanDistance(pos, pacmanPos) for pos in foodPos)
    if currentDist < nearestFood:
        nearestFood = currentDist

    score += 4 / nearestFood                     # (1) further the food, longer the time to reach it -> lower score
                                                    # Priority = high : Multiplying factor = 4
    score += 5 / len(foodPos)                    # (2) more the remaining food -> lower score
                                                    # Priority = highest : Multiplying factor = 5
    # find power pellets
    capsules = currentGameState.getCapsules()
    score += 1 / (1 + len(capsules))             # (3) more the remaining capsules -> lower score
                                                    # Priority = low : Multiplying factor = 1
 
    # find nearest ghost
    numOfGhosts = currentGameState.getNumAgents() - 1
    nearestGhost = 999999
    for ghostAgentIndex in range(1,numOfGhosts+1):
        nextdist = manhattanDistance(pacmanPos, currentGameState.getGhostPosition(ghostAgentIndex))
        nearestGhost = min(nearestGhost, nextdist)
    score += 3 / nearestGhost                    # (4) closer the ghost, higher the danger -> lower score
                                                    # Priority = medium : Multiplying factor = 3
    # for each scared ghost
    ghostStates = currentGameState.getGhostStates()
    for ghost in ghostStates:
        if ghost.scaredTimer > 0:
            score += min(5,ghost.scaredTimer)    # (5) for every scared ghost, increase the score
                                                    # Priority = low (eating the ghost is not a priority) : Multiplying factor = 1
                                                 #     NOTE: if we dont keep a minimum value here, the
                                                 #           pacman will try to approach the furthest
                                                 #           goal. Pacman should only approach nearer ghosts
    
    return score

# Abbreviation
better = betterEvaluationFunction
