import tkinter as tk
from tkinter import messagebox
import random
import math

class GridGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grid Search Game")
        self.root.resizable(False, False)
        
        # Game constants
        self.grid_width = 10
        self.grid_height = 10
        self.cell_size = 35
        self.time_limit = 5  # 5 seconds
        
        # Game state
        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2
        self.moves = 0
        self.game_won = False
        self.game_lost = False
        self.time_remaining = self.time_limit
        
        # Timer control
        self.timer_running = False
        self.timer_id = None  # Store the timer ID to cancel it
        
        # Place goal
        self.place_goal()
        
        # Calculate initial distance and direction
        self.distance_to_goal = self.calculate_distance()
        self.direction_to_goal = self.calculate_direction()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start timer
        self.start_timer()
        
    def place_goal(self):
        """Place the goal at a random position, ensuring it's not on the player"""
        while True:
            self.goal_x = random.randint(0, self.grid_width - 1)
            self.goal_y = random.randint(0, self.grid_height - 1)
            if (self.goal_x != self.player_x or self.goal_y != self.player_y):
                break
    
    def calculate_distance(self):
        """Calculate Manhattan distance from player to goal"""
        return abs(self.player_x - self.goal_x) + abs(self.player_y - self.goal_y)
    
    def calculate_direction(self):
        """Calculate direction from player to goal (normalized 1-8)"""
        dx = self.goal_x - self.player_x
        dy = self.goal_y - self.player_y
        
        if dx == 0 and dy == 0:
            return 0  # Here!
        elif dx == 0:
            return 1 if dy < 0 else 5  # North = 1, South = 5
        elif dy == 0:
            return 3 if dx < 0 else 7  # West = 3, East = 7
        else:
            # Diagonal directions
            if dx < 0 and dy < 0:
                return 2  # Northwest
            elif dx > 0 and dy < 0:
                return 8  # Northeast
            elif dx < 0 and dy > 0:
                return 4  # Southwest
            else:  # dx > 0 and dy > 0
                return 6  # Southeast
    
    def get_direction_text(self, direction_value):
        """Convert normalized direction value to text"""
        direction_map = {
            0: "Here!",
            1: "North",
            2: "Northwest", 
            3: "West",
            4: "Southwest",
            5: "South",
            6: "Southeast",
            7: "East",
            8: "Northeast"
        }
        return direction_map.get(direction_value, "Unknown")
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Title and info
        title_label = tk.Label(main_frame, text="Grid Search Game", font=("Arial", 16, "bold"))
        title_label.pack()
        
        info_label = tk.Label(main_frame, text="Use arrow keys to move the player (blue) to the goal (red)")
        info_label.pack(pady=5)
        
        # Timer and moves frame
        stats_frame = tk.Frame(main_frame)
        stats_frame.pack()
        
        # Timer label
        self.timer_label = tk.Label(stats_frame, text=f"Time: {self.time_remaining}s", font=("Arial", 12, "bold"), fg="red")
        self.timer_label.pack(side=tk.LEFT, padx=10)
        
        # Move counter
        self.moves_label = tk.Label(stats_frame, text=f"Moves: {self.moves}", font=("Arial", 12))
        self.moves_label.pack(side=tk.LEFT, padx=10)
        
        # Distance and direction frame
        info_frame = tk.Frame(main_frame)
        info_frame.pack(pady=5)
        
        # Distance label
        self.distance_label = tk.Label(info_frame, text=f"Distance: {self.distance_to_goal}", font=("Arial", 11))
        self.distance_label.pack(side=tk.LEFT, padx=10)
        
        # Direction label
        self.direction_label = tk.Label(info_frame, text=f"Direction: {self.get_direction_text(self.direction_to_goal)}", font=("Arial", 11))
        self.direction_label.pack(side=tk.LEFT, padx=10)
        
        # Grid frame
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(pady=10)
        
        # Create grid buttons
        self.grid_buttons = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                button = tk.Button(
                    grid_frame,
                    width=2,
                    height=1,
                    relief="raised",
                    borderwidth=1
                )
                button.grid(row=y, column=x, padx=1, pady=1)
                row.append(button)
            self.grid_buttons.append(row)
        
        # Control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        quit_button = tk.Button(control_frame, text="Quit", command=self.root.quit)
        quit_button.pack(side=tk.LEFT, padx=5)
        
        # Update the grid display
        self.update_grid()
    
    def start_timer(self):
        """Start the timer (only if not already running)"""
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
    
    def stop_timer(self):
        """Stop the timer"""
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
    
    def update_timer(self):
        """Update the timer countdown"""
        if not self.timer_running:
            return
            
        if not self.game_won and not self.game_lost:
            if self.time_remaining > 0:
                self.time_remaining -= 1
                self.timer_label.config(text=f"Time: {self.time_remaining}s")
                
                # Change color based on time remaining
                if self.time_remaining <= 1:
                    self.timer_label.config(fg="red")
                elif self.time_remaining <= 2:
                    self.timer_label.config(fg="orange")
                else:
                    self.timer_label.config(fg="black")
                
                # Schedule next timer update
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                # Time's up!
                self.game_lost = True
                self.stop_timer()
                self.show_result_and_restart("Time's up! You didn't reach the goal in 5 seconds.")
    
    def update_grid(self):
        """Update the visual grid display"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                button = self.grid_buttons[y][x]
                
                if x == self.player_x and y == self.player_y:
                    # Player (blue)
                    button.config(bg="blue", fg="white", text="P")
                elif x == self.goal_x and y == self.goal_y:
                    # Goal (red)
                    button.config(bg="red", fg="white", text="G")
                else:
                    # Empty cell (white)
                    button.config(bg="white", fg="black", text="")
        
        # Update moves counter
        self.moves_label.config(text=f"Moves: {self.moves}")
        
        # Update distance and direction
        self.distance_to_goal = self.calculate_distance()
        self.direction_to_goal = self.calculate_direction()
        self.distance_label.config(text=f"Distance: {self.distance_to_goal}")
        self.direction_label.config(text=f"Direction: {self.get_direction_text(self.direction_to_goal)}")
    
    def move_player(self, direction):
        """Move the player in the specified direction (programmatic use)"""
        if self.game_won or self.game_lost:
            return False
        
        moved = False
        
        if direction == "up" and self.player_y > 0:
            self.player_y -= 1
            moved = True
        elif direction == "down" and self.player_y < self.grid_height - 1:
            self.player_y += 1
            moved = True
        elif direction == "left" and self.player_x > 0:
            self.player_x -= 1
            moved = True
        elif direction == "right" and self.player_x < self.grid_width - 1:
            self.player_x += 1
            moved = True
        
        if moved:
            self.moves += 1
            self.check_win_condition()
            self.update_grid()
            return True
        
        return False
    
    def move_player_3_spaces(self, direction):
        """Move the player 3 spaces in the specified direction (programmatic use)"""
        if self.game_won or self.game_lost:
            return False
        
        moves_made = 0
        
        for _ in range(3):
            if direction == "up" and self.player_y > 0:
                self.player_y -= 1
                moves_made += 1
            elif direction == "down" and self.player_y < self.grid_height - 1:
                self.player_y += 1
                moves_made += 1
            elif direction == "left" and self.player_x > 0:
                self.player_x -= 1
                moves_made += 1
            elif direction == "right" and self.player_x < self.grid_width - 1:
                self.player_x += 1
                moves_made += 1
            else:
                # Can't move further in this direction
                break
        
        if moves_made > 0:
            self.moves += moves_made
            self.check_win_condition()
            self.update_grid()
            return moves_made
        
        return 0
    
    def check_win_condition(self):
        """Check if the player has reached the goal"""
        if self.player_x == self.goal_x and self.player_y == self.goal_y:
            self.game_won = True
            self.place_new_goal()
    
    def place_new_goal(self):
        """Place a new goal and continue the game"""
        # Stop current timer
        self.stop_timer()
        
        # Place new goal
        self.place_goal()
        
        # Reset timer to full time
        self.time_remaining = self.time_limit
        
        # Reset game state for next goal
        self.game_won = False
        self.game_lost = False
        
        # Recalculate distance and direction
        self.distance_to_goal = self.calculate_distance()
        self.direction_to_goal = self.calculate_direction()
        
        # Update display
        self.update_grid()
        self.timer_label.config(text=f"Time: {self.time_remaining}s", fg="black")
        
        # Start new timer
        self.start_timer()
        
        # Show brief success message in title
        self.root.title("Grid Search Game - Goal reached! New goal placed.")
        self.root.after(1500, lambda: self.root.title("Grid Search Game"))
    
    def show_result_and_restart(self, message):
        """Show result message briefly and then restart automatically"""
        # Update the title to show the result
        self.root.title(f"Grid Search Game - {message}")
        
        # Schedule automatic restart after 2 seconds
        self.root.after(2000, self.auto_restart)
    
    def auto_restart(self):
        """Automatically restart the game"""
        self.reset_game()
        # Reset the window title
        self.root.title("Grid Search Game")
    
    def reset_game(self):
        """Reset the game state"""
        # Stop current timer
        self.stop_timer()
        
        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2
        self.moves = 0
        self.game_won = False
        self.game_lost = False
        self.time_remaining = self.time_limit
        self.place_goal()
        
        # Recalculate distance and direction
        self.distance_to_goal = self.calculate_distance()
        self.direction_to_goal = self.calculate_direction()
        
        self.update_grid()
        
        # Reset timer display
        self.timer_label.config(text=f"Time: {self.time_remaining}s", fg="black")
        
        # Start new timer
        self.start_timer()
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = GridGameGUI()
    game.run() 