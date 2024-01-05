import random

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.is_sunk = False

class Board:
    def __init__(self):
        self.size = 6
        self.ships = []
        self.grid = [['О' for _ in range(self.size)] for _ in range(self.size)]

    def place_ship(self, ship):
        for coord in ship.coordinates:
            x, y = coord
            self.grid[x][y] = '■'
        self.ships.append(ship)

    def display(self):
        print("   | 1 | 2 | 3 | 4 | 5 | 6|")
        for i in range(self.size):
            print(f"{i+1} | {' | '.join(self.grid[i])} |")

    def is_valid_move(self, x, y):
        return 1 <= x <= self.size and 1 <= y <= self.size and self.grid[x-1][y-1] == 'О'

    def make_move(self, x, y):
        if not self.is_valid_move(x, y):
            raise ValueError("Invalid move! You've already shot there or the coordinates are out of bounds.")
        if any((x-1, y-1) in ship.coordinates for ship in self.ships):
            print("Hit!")
            for ship in self.ships:
                if (x-1, y-1) in ship.coordinates:
                    ship.is_sunk = all(coord.is_sunk for coord in ship.coordinates)
                    if ship.is_sunk:
                        print("You sank a ship!")
                        for coord in ship.coordinates:
                            self.grid[coord[0]][coord[1]] = 'X'
                    else:
                        print("Ship hit!")
                        self.grid[x-1][y-1] = 'X'
                    break
        else:
            print("Miss!")
            self.grid[x-1][y-1] = 'T'

def main():
    player_board = Board()
    computer_board = Board()

    # Place ships on the boards
    player_ships = [
        Ship([(0, 0), (0, 1), (0, 2)]),  # 1 ship of length 3
        Ship([(3, 0), (3, 2)]),           # 2 ships of length 2
        Ship([(4, 4)]),                   # 1 ship of length 1
        Ship([(5, 0), (5, 2)]),           # 2 ships of length 2
    ]

    computer_ships = [
        Ship([(0, 3), (0, 4), (0, 5)]),
        Ship([(1, 4), (1, 5)]),
        Ship([(3, 0), (3, 2)]),
        Ship([(4, 4)]),
    ]

    for ship in player_ships:
        player_board.place_ship(ship)

    for ship in computer_ships:
        computer_board.place_ship(ship)

    player_moves = set()
    computer_moves = set()

    while any(not ship.is_sunk for ship in computer_ships) and any(not ship.is_sunk for ship in player_ships):
        print("\nYour Board:")
        player_board.display()

        try:
            x = int(input("Enter the row number (1-6): "))
            y = int(input("Enter the column number (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if (x, y) in player_moves:
            print("You've already shot there. Try again.")
            continue

        player_moves.add((x, y))
        player_board.make_move(x, y)

        # Computer's move
        computer_x, computer_y = random.randint(1, 6), random.randint(1, 6)
        while (computer_x, computer_y) in computer_moves:
            computer_x, computer_y = random.randint(1, 6), random.randint(1, 6)

        print(f"\nComputer's move: {computer_x}, {computer_y}")
        computer_moves.add((computer_x, computer_y))
        computer_board.make_move(computer_x, computer_y)

    print("\nGame Over!")
    print("Your Board:")
    player_board.display()
    print("\nComputer's Board:")
    computer_board.display()

    if all(ship.is_sunk for ship in computer_ships):
        print("\nCongratulations! You won!")
    else:
        print("\nSorry, you lost. Better luck next time!")

if __name__ == "__main__":
    main()