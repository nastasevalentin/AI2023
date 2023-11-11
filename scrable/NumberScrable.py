class NumberScrabble:
    def __init__(self):
        self.board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.player_moves = []
        self.ai_moves = []
        self.player_turn = 0

    def is_valid_move(self, value: int) -> bool:
        if value > 9 or value < 1:
            return False
        return value not in self.player_moves and value not in self.ai_moves

    def make_move(self, number, player):
        if self.is_valid_move(number):
            self.possible_moves.remove(number)
            if player == "A":
                self.player_moves.append(number)
            else:
                self.ai_moves.append(number)
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] == number:
                        if player == "A":
                            self.board[row][col] = -1
                        else:
                            self.board[row][col] = -2
                        return True
        return False  # Number not found on the board

    def check_winner(self):
        winning_lines = [
            [(0, 0), (0, 1), (0, 2)],  # Rows
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],  # Columns
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],  # Diagonals
            [(0, 2), (1, 1), (2, 0)]
        ]

        for player in ["A", "B"]:
            moves = self.player_moves if player == "A" else self.ai_moves
            for line in winning_lines:
                winner_found = all(num in moves for num in [self.board[row][col] for row, col in line])
                if winner_found:
                    return player  # Return the winning player

        return None  # No winner found

    def is_draw(self):
        return len(self.possible_moves) == 0

    def display_board(self):
        print("Board:")
        for row in self.board:
            for cell in row:
                if cell == 1:
                    print("X", end=" ")
                elif cell == 2:
                    print("O", end=" ")
                else:
                    print(cell, end=" ")
            print()


    @staticmethod
    def has15(values) -> bool:
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

    def heuristic(self):
        def count_winning_lines(player_moves):
            winning_lines = [
                [(0, 0), (0, 1), (0, 2)],  # Rows
                [(1, 0), (1, 1), (1, 2)],
                [(2, 0), (2, 1), (2, 2)],
                [(0, 0), (1, 0), (2, 0)],  # Columns
                [(0, 1), (1, 1), (2, 1)],
                [(0, 2), (1, 2), (2, 2)],
                [(0, 0), (1, 1), (2, 2)],  # Diagonals
                [(0, 2), (1, 1), (2, 0)]
            ]

            player_winning_lines = 0

            for line in winning_lines:
                winner_found = all(num in player_moves for num in [self.board[row][col] for row, col in line])
                if winner_found:
                    player_winning_lines += 1

            return player_winning_lines

        if self.player_turn == 0:
            player_moves = self.player_moves
            opponent_moves = self.ai_moves
        else:
            player_moves = self.ai_moves
            opponent_moves = self.player_moves

        player_lines = count_winning_lines(player_moves)
        opponent_lines = count_winning_lines(opponent_moves)

        return player_lines - opponent_lines

    def minmax(self, depth: int, isMaxPlayer: bool) -> int:
        if depth == 0 or self.check_winner():
            return self.extendedHeuristic()

        if isMaxPlayer:
            value = float('-inf')
            for i in range(1, 10):
                if self.is_valid_move(i):
                    self.make_move(i, "B")
                    value = max(value, self.minmax(depth - 1, False))
        else:
            value = float('inf')
            for i in range(1, 10):
                if self.is_valid_move(i):
                    self.make_move(i, "A")
                    value = min(value, self.minmax(depth - 1, True))

        return value

    def extendedHeuristic(self) -> int:
        gameState = self.getGameState()
        if gameState == "AI wins":
            return float('inf')
        elif gameState == "Player wins":
            return float('-inf')
        return self.heuristic()

    def getGameState(self) -> str:
        if self.has15(self.player_moves):
            return "Player wins"
        if self.has15(self.ai_moves):
            return "AI wins"
        if len(self.player_moves) + len(self.ai_moves) == 9:
            return "Draw"
        return "In Progress"
    def play(self):
        while True:
            self.display_board()

            if self.player_turn == 0:
                player = "A"
                try:
                    number = int(input(f"Player {player}, choose a number between 1 and 9: "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
            else:
                player = "B"
                print(f"Calculating {player}'s move...")
                number = self.minmax(4, True)  # Adjust the depth as needed

            if self.is_valid_move(number):
                if self.make_move(number, player):
                    if self.check_winner():
                        self.display_board()
                        print(f"Player {player} wins!")
                        break
                    elif self.is_draw():
                        self.display_board()
                        print("The game ends in a draw.")
                        break
                    self.player_turn = 1 - self.player_turn
                else:
                    print("You chose a number that has already been selected. Choose a different number.")
            else:
                print("Choose a valid number between 1 and 9.")

if __name__ == "__main__":
    game = NumberScrabble()
    game.play()
