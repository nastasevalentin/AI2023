from typing import List

class State:
    def __init__(self, aiTurn: bool, player: List[int] = None, ai: List[int] = None):
        self.aiTurn = aiTurn
        self.player = player or []
        self.ai = ai or []

def makeState(aiTurn: bool) -> State:
    return State(aiTurn)

def isTransitionValid(state: State, aiTurn: bool, value: int) -> bool:
    if aiTurn != state.aiTurn:
        return False
    if value > 9 or value < 1:
        return False
    return value not in state.player and value not in state.ai

def transition(state: State, value: int) -> State:
    new_state = State(aiTurn=not state.aiTurn, player=state.player[:], ai=state.ai[:])
    if state.aiTurn:
        new_state.ai.append(value)
    else:
        new_state.player.append(value)
    return new_state

def has15(values: List[int]) -> bool:
    if len(values) < 3:
        return False
    for i in range(len(values)):
        for j in range(len(values)):
            for k in range(len(values)):
                x = values[i]
                y = values[j]
                z = values[k]
                if x != y and x != z and y != z and x + y + z == 15:
                    return True
    return False

def isFinalState(state: State) -> bool:
    if has15(state.player):
        return True
    if has15(state.ai):
        return True
    return len(state.player) + len(state.ai) == 9

def getGameState(state: State) -> str:
    if has15(state.player):
        return "Player wins"
    if has15(state.ai):
        return "AI wins"
    if len(state.player) + len(state.ai) == 9:
        return "Draw"
    return "In Progress"

def printState(state: State):
    print('Player:', state.player)
    print('AI:', state.ai)
    if state.aiTurn:
        print("AI's turn")
    else:
        print('Your turn')

def heuristic(state: State) -> int:
    matrix = getMatrix(state)
    return getNumberOfDirections(matrix, 2) - getNumberOfDirections(matrix, 1)

def getNumberOfDirections(matrix, player):
    result = 0
    for i in range(3):
        if matrix[i][0] != player and matrix[i][1] != player and matrix[i][2] != player:
            continue
        result += 1
        for j in range(3):
            if matrix[i][j] != player and matrix[i][j] != 0:
                result -= 1
                break

    for i in range(3):
        if matrix[0][i] != player and matrix[1][i] != player and matrix[2][i] != player:
            continue
        result += 1
        for j in range(3):
            if matrix[j][i] != player and matrix[j][i] != 0:
                result -= 1
                break

    if matrix[0][0] == player or matrix[1][1] == player or matrix[2][2] == player:
        result += 1
        for i in range(3):
            if matrix[i][i] != player and matrix[i][i] != 0:
                result -= 1
                break

    if matrix[0][2] == player or matrix[1][1] == player or matrix[2][0] == player:
        result += 1
        for i in range(3):
            if matrix[i][2 - i] != player and matrix[i][2 - i] != 0:
                result -= 1
                break

    return result

def getMatrix(state: State):
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    matrixPositions = {
        1: [1, 2],
        2: [0, 0],
        3: [2, 1],
        4: [2, 0],
        5: [1, 1],
        6: [0, 2],
        7: [0, 1],
        8: [2, 2],
        9: [1, 2]
    }

    for value in state.player:
        x, y = matrixPositions[value]
        matrix[x][y] = 1

    for value in state.ai:
        x, y = matrixPositions[value]
        matrix[x][y] = 2

    return matrix

def getNextMoveForAI(state: State) -> int:
    depth = 4
    value = float('-inf')
    bestMove = 0

    for i in range(1, 10):
        if not isTransitionValid(state, True, i):
            continue
        minmaxValue = minmax(transition(state, i), depth, False)
        print({"minmax": minmaxValue, "i": i, "h": heuristic(transition(state, i))})
        if minmaxValue >= value:
            value = minmaxValue
            bestMove = i
    return bestMove

def minmax(state: State, depth: int, isMaxPlayer: bool) -> int:
    if depth == 0 or isFinalState(state):
        return extendedHeuristic(state)

    if isMaxPlayer:
        value = float('-inf')
        for i in range(1, 10):
            if not isTransitionValid(state, True, i):
                continue
            value = max(value, minmax(transition(state, i), depth - 1, False))
        return value

    value = float('inf')
    for i in range(1, 10):
        if not isTransitionValid(state, False, i):
            continue
        value = min(value, minmax(transition(state, i), depth - 1, True))
    return value

def extendedHeuristic(state: State) -> int:
    gameState = getGameState(state)
    if gameState == "AI wins":
        return float('inf')
    elif gameState == "Player wins":
        return float('-inf')
    return heuristic(state)

def play(aiTurn=False):
    state = makeState(aiTurn)
    while not isFinalState(state):
        printState(state)
        nextMove = 0
        if not state.aiTurn:
            nextMove = int(input('Your move: ') or '0')
        else:
            nextMove = getNextMoveForAI(state)
        if not isTransitionValid(state, state.aiTurn, nextMove):
            print('Invalid move', nextMove)
            continue
        state = transition(state, nextMove)
    printState(state)
    print(getGameState(state))

if __name__ == "__main__":
    play(True)
