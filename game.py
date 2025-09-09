from grid_game_gui import GridGameGUI

# Create the game
game = GridGameGUI()

print("Game created!")
print(f"Player position: ({game.player_x}, {game.player_y})")
print(f"Goal position: ({game.goal_x}, {game.goal_y})")

game.run() 