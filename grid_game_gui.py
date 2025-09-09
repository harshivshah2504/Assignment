import tkinter as tk
from tkinter import messagebox, filedialog
import random
import numpy as np
from datetime import datetime


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.9995, min_exploration_rate=0.01):
        self.q_table = np.zeros((19, 9, 9)) 
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.epsilon_min = min_exploration_rate
        self.actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def choose_action(self, state):
        distance, direction = state
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return np.argmax(self.q_table[distance, direction])

    def learn(self, state, action, reward, next_state):
        old_dist, old_dir = state
        next_dist, next_dir = next_state
        old_value = self.q_table[old_dist, old_dir, action]
        next_max = np.max(self.q_table[next_dist, next_dir])
        new_value = (1 - self.lr) * old_value + self.lr * (reward + self.gamma * next_max)
        self.q_table[old_dist, old_dir, action] = new_value

    def update_exploration_rate(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay





class GridGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grid Search Game - Manual & AI")
        self.root.resizable(False, False)
        
        # Game constants
        self.grid_width = 10
        self.grid_height = 10
        self.max_steps = 50 
        self.time_limit = 5
        
        # Unified Game State
        self.player_x = self.grid_width // 2
        self.player_y = self.grid_height // 2
        self.goal_x = 0
        self.goal_y = 0
        self.moves = 0 
        self.steps_taken = 0
        self.game_won = False
        self.game_lost = False
        self.game_over = False 
        
        # Timer control for manual play
        self.time_remaining = self.time_limit
        self.timer_running = False
        self.timer_id = None
        
        # RL Agent
        self.agent = QLearningAgent()
        self.training_episodes = 1800
        self.current_episode = 0
        self.training_successes = []

        # Create GUI elements
        self.create_widgets()
        
        # Set up manual key bindings
        self.root.bind("<KeyPress>", self.handle_key_press)
        
        # Initialize game, start clock, and start manual timer
        self.reset_game(is_manual_reset=True)
        self.update_clock()
        
    def _get_state(self):
        """Gets the current state (distance, direction) for the agent."""
        return (self.calculate_distance(), self.calculate_direction())

    def reset_game(self, is_manual_reset=False):
        """Resets the game state for either manual play or a new agent episode."""
        self.stop_timer() # Stop any active timer
        
        # Reset positions
        self.player_x = random.randint(0, self.grid_width - 1)
        self.player_y = random.randint(0, self.grid_height - 1)
        self.place_goal()
        
        # Reset counters and flags
        self.moves = 0
        self.steps_taken = 0
        self.game_won = False
        self.game_lost = False
        self.game_over = False
        
        self.update_grid()
        
        if is_manual_reset:
            self.time_remaining = self.time_limit
            self.start_timer()
            self.root.title("Grid Search Game - Manual Play")
        
        return self._get_state()

    def place_goal(self):
        """Place the goal at a random position, ensuring it's not on the player."""
        while True:
            self.goal_x = random.randint(0, self.grid_width - 1)
            self.goal_y = random.randint(0, self.grid_height - 1)
            if (self.goal_x, self.goal_y) != (self.player_x, self.player_y):
                break

    def step(self, action):
        """Core simulation step used by the AI agent."""
        self.steps_taken += 1
        if action == 1: self.player_y = max(0, self.player_y - 1) # N
        elif action == 2: self.player_y, self.player_x = max(0, self.player_y - 1), max(0, self.player_x - 1) # NW
        elif action == 3: self.player_x = max(0, self.player_x - 1) # W
        elif action == 4: self.player_y, self.player_x = min(self.grid_height-1, self.player_y + 1), max(0, self.player_x - 1) # SW
        elif action == 5: self.player_y = min(self.grid_height - 1, self.player_y + 1) # S
        elif action == 6: self.player_y, self.player_x = min(self.grid_height-1, self.player_y + 1), min(self.grid_width-1, self.player_x + 1) # SE
        elif action == 7: self.player_x = min(self.grid_width - 1, self.player_x + 1) # E
        elif action == 8: self.player_y, self.player_x = max(0, self.player_y - 1), min(self.grid_width-1, self.player_x + 1) # NE
        if (self.player_x, self.player_y) == (self.goal_x, self.goal_y):
            reward, done, self.game_over = 100, True, True
        elif self.steps_taken >= self.max_steps:
            reward, done, self.game_over = -50, True, True
        else:
            reward, done, self.game_over = -1, False, False
            
        return self._get_state(), reward, done

    def calculate_distance(self):
        return abs(self.player_x - self.goal_x) + abs(self.player_y - self.goal_y)
    
    def calculate_direction(self):
        dx = self.goal_x - self.player_x
        dy = self.player_y - self.goal_y
        if dx == 0 and dy == 0: return 0
        if dx == 0 and dy > 0: return 1
        if dx < 0 and dy > 0: return 2
        if dx < 0 and dy == 0: return 3
        if dx < 0 and dy < 0: return 4
        if dx == 0 and dy < 0: return 5
        if dx > 0 and dy < 0: return 6
        if dx > 0 and dy == 0: return 7
        if dx > 0 and dy > 0: return 8
        return 0

    def get_direction_text(self, val):
        return ["Here!", "N", "NW", "W", "SW", "S", "SE", "E", "NE"][val]


    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        title_label = tk.Label(left_frame, text="Grid Search Game", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 5))
        tk.Label(left_frame, text="Use arrow keys to play, or use the Agent Controls.").pack(pady=(0, 10))
        
        grid_frame = tk.Frame(left_frame, relief="sunken", borderwidth=2)
        grid_frame.pack(pady=10)
        
        self.grid_labels = [[tk.Label(grid_frame, width=2, height=1, relief="raised", borderwidth=1, font=("Arial", 10, "bold")) for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        for y, row in enumerate(self.grid_labels):
            for x, label in enumerate(row):
                label.grid(row=y, column=x, padx=1, pady=1)
        
        info_frame = tk.Frame(left_frame)
        info_frame.pack(pady=5)
        self.timer_label = tk.Label(info_frame, text="Time: 5s", font=("Arial", 11, "bold"))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.moves_label = tk.Label(info_frame, text="Moves: 0", font=("Arial", 11))
        self.moves_label.pack(side=tk.LEFT, padx=10)
        self.distance_label = tk.Label(info_frame, text="Distance: 0", font=("Arial", 11))
        self.distance_label.pack(side=tk.LEFT, padx=10)
        self.direction_label = tk.Label(info_frame, text="Direction: N/A", font=("Arial", 11))
        self.direction_label.pack(side=tk.LEFT, padx=10)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        control_label = tk.Label(right_frame, text="Agent Control", font=("Arial", 14, "bold"))
        control_label.pack(pady=(0, 10))

        tk.Button(right_frame, text="Train Agent", command=self.start_training).pack(fill=tk.X, pady=5)
        tk.Button(right_frame, text="Run Trained Agent", command=self.run_trained_agent).pack(fill=tk.X, pady=5)
        tk.Button(right_frame, text="Reset Manual Game", command=lambda: self.reset_game(True)).pack(fill=tk.X, pady=5)

        file_frame = tk.LabelFrame(right_frame, text="Agent Brain", padx=5, pady=5)
        file_frame.pack(fill=tk.X, pady=10)
        tk.Button(right_frame, text="Quit", command=self.root.quit).pack(side=tk.BOTTOM, fill=tk.X)
        status_frame = tk.Frame(self.root, relief="sunken", borderwidth=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.training_status_label = tk.Label(status_frame, text="Ready for manual play.", anchor='w')
        self.training_status_label.pack(side=tk.LEFT, padx=5)
        self.epsilon_label = tk.Label(status_frame, text="", anchor='w')
        self.epsilon_label.pack(side=tk.LEFT, padx=5)
        self.clock_label = tk.Label(status_frame, text="", anchor='e')
        self.clock_label.pack(side=tk.RIGHT, padx=5)
    

    def update_grid(self):
        """Update the visual grid and all info labels"""
        for y, row in enumerate(self.grid_labels):
            for x, label in enumerate(row):
                if (x, y) == (self.player_x, self.player_y): label.config(bg="blue", text="P", fg="white")
                elif (x, y) == (self.goal_x, self.goal_y): label.config(bg="red", text="G", fg="white")
                else: label.config(bg="white", text="", fg="black")
        
        self.distance_label.config(text=f"Distance: {self.calculate_distance()}")
        self.direction_label.config(text=f"Direction: {self.get_direction_text(self.calculate_direction())}")
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.timer_label.config(text=f"Time: {self.time_remaining}s")
        self.root.update_idletasks()

    def handle_key_press(self, event):
        if self.game_won or self.game_lost: return
        
        moved = False
        if event.keysym == "Up" and self.player_y > 0: self.player_y -= 1; moved = True
        elif event.keysym == "Down" and self.player_y < self.grid_height - 1: self.player_y += 1; moved = True
        elif event.keysym == "Left" and self.player_x > 0: self.player_x -= 1; moved = True
        elif event.keysym == "Right" and self.player_x < self.grid_width - 1: self.player_x += 1; moved = True
        
        if moved:
            self.moves += 1
            self.check_win_condition()
            self.update_grid()
            
    def check_win_condition(self):
        if (self.player_x, self.player_y) == (self.goal_x, self.goal_y):
            self.game_won = True
            self.stop_timer()
            messagebox.showinfo("You Won!", f"You reached the goal in {self.moves} moves!")
            self.reset_game(is_manual_reset=True)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
    
    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_id: self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def update_timer(self):
        if not self.timer_running or self.game_won: return
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_grid()
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.game_lost = True
            self.stop_timer()
            messagebox.showwarning("Time's Up!", "You ran out of time!")
            self.reset_game(is_manual_reset=True)

    def start_training(self):
        self.stop_timer() 
        self.agent = QLearningAgent()
        self.current_episode = 0
        self.training_successes.clear()
        self.run_training_episode()

    def run_training_episode(self):
        if self.current_episode >= self.training_episodes:
            messagebox.showinfo(f"Finished {self.training_episodes} episodes.")
            self.training_status_label.config(text="Training complete.")
            return

        state = self.reset_game(is_manual_reset=False)
        done = False
        while not done:
            action = self.agent.choose_action(state)
            next_state, reward, done = self.step(action)
            self.agent.learn(state, action, reward, next_state)
            state = next_state
            
        self.training_successes.append(1 if reward > 0 else 0)
        self.agent.update_exploration_rate()
        self.current_episode += 1
        
        if self.current_episode % 20 == 0:
            rate = np.mean(self.training_successes[-100:]) * 100 if self.training_successes else 0
            self.training_status_label.config(text=f"Training: Ep: {self.current_episode}/{self.training_episodes} | Success: {rate:.1f}%")
            self.update_grid()
        
        self.root.after(1, self.run_training_episode)
    
    def run_trained_agent(self):
        self.stop_timer()
        self.reset_game(is_manual_reset=False)
        self.agent.epsilon = 0
        self.training_status_label.config(text="Running trained agent")
        self.epsilon_label.config(text="")
        self.run_agent_step()

    def run_agent_step(self):
        if self.game_over:
            msg = "found the goal" if (self.player_x, self.player_y) == (self.goal_x, self.goal_y) else "failed"
            self.training_status_label.config(text=f"Agent {msg} in {self.steps_taken} steps!")
            return

        state = self._get_state()
        action = self.agent.choose_action(state)
        self.step(action)
        self.update_grid()
        self.root.after(100, self.run_agent_step)

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = GridGameGUI()
    game.run()

