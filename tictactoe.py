import math
import copy
import random

# intuitive representative variable definition
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # if the board is defaulted, return X
    if board == initial_state():
        return X

    # record the numbers of X and O on the board
    numOfX, numOfO = 0, 0
    for row in board:
        numOfX += row.count(X)
        numOfO += row.count(O)

    # if there is more X, give O the next move
    if numOfX > numOfO:
        return O
    # if there is equivalent amount of O and X, give X the next move
    elif numOfX == numOfO:
        return X
    # something went catastrophically wrong
    elif numOfX < numOfO:
        raise ValueError("anomalies: numOfO is greater than numOfX")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # list initialization
    actions = list()

    # check if any spot is empty, append the indices to actions list
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                actions.append((row, column))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # creates a deepcopy of the board
    newBoard = copy.deepcopy(board)

    if player(board) == X:
        # check if the action can be placed
        if board[action[0]][action[1]] != EMPTY:
            raise ValueError("anomalies: action cannot be placed, destination is not empty")
        # set the corresponding action coordinate to X
        newBoard[action[0]][action[1]] = X
    elif player(board) == O:
        # check if the action can be placed
        if board[action[0]][action[1]] != EMPTY:
            raise ValueError("anomalies: action cannot be placed, destination is not empty")
        # set the corresponding action coordinate to O
        newBoard[action[0]][action[1]] = O
    else:
        raise ValueError("anomalies: player corruption")

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #  check if y=-x diagonal has been filled with the same mark and output corresponding score
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O

    # check if y=x diagonal has been filled with the same mark and output corresponding score
    if board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][2] == board[1][1] == board[2][0] == O:
        return O

    # check if any row has been filled with the same mark
    for row in board:
        if row[0] == row[1] == row[2] == X:
            return X
        elif row[0] == row[1] == row[2] == O:
            return O

    # check if any column has been filled with the same mark
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] == X:
            return X
        elif board[0][column] == board[1][column] == board[2][column] == O:
            return O

    # else must resulted in a tie or game has not yet finished, return nobody
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if the game has been won, then return true
    if winner(board) == X or winner(board) == O:
        return True

    # if the game has any empty spots left, return false
    for row in board:
        for element in row:
            if element == EMPTY:
                return False

    # if there is no empty spot left and no one has "won", return true
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    """
    # for ai starting their first move, if the state is the initial state, choose a random action to deploy
    if board == initial_state():
        return (random.randrange(3), random.randrange(3))

    # variable initialization
    bestAction = None

    # if the board is the terminal board, return None
    if terminal(board):
        return bestAction

    # if it's X's turn, return the action that is the highest value amongst the boards with values minimized by O
    if player(board) == X:
        # initialize the optimal value to negative infinity to ensure the guaranteeing of accepting the initial move
        optimalValue = -math.inf
        for action in actions(board):
            # temporary placeholder of the minimized value returned by result board using current action
            value = Min_Value(result(board, action))
            # filter in the highest value, set temporarily the optimal value, action to the corresponding one
            if value > optimalValue:
                optimalValue = value
                bestAction = action

    # if it's O's turn, return the action that is the lowest value amongst the boards with values maximized by X
    elif player(board) == O:
        # initialize the optimal value to infinity to ensure the guaranteeing of accepting the initial move
        optimalValue = math.inf
        for action in actions(board):
            # temporary placeholder of the maximized value returned by result board using current action
            value = Max_Value(result(board, action))
            # filter in the lowest value, set temporarily the optimal value, action to the corresponding one
            if value < optimalValue:
                optimalValue = value
                bestAction = action

    return bestAction


def Min_Value(board):
    # if the game has ended, immediately return the corresponding value
    if terminal(board):
        return utility(board)

    # initialize the optimal value to infinity to ensure choosing any choice of value would be smaller
    value = math.inf

    # loop to get the optimized value from the current state
    for action in actions(board):
        value = min(value, Max_Value(result(board, action)))

    return value


def Max_Value(board):
    # if the game has ended, immediately return the corresponding value
    if terminal(board):
        return utility(board)

    # initialize the optimal value to negative infinity to ensure choosing any choice of value will be larger
    value = -math.inf

    # loop to get the optimized value from the current state
    for action in actions(board):
        value = max(value, Min_Value(result(board, action)))

    return value