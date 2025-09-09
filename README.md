# Grid Search Game

A Python grid-based game with programmatic control.

## Distance and Direction Variables

### Distance Variables
- `distance_to_goal` - Manhattan distance from player to goal (integer)
- `calculate_distance()` - Method that returns the Manhattan distance calculation

### Direction Variables  
- `direction_to_goal` - Normalized direction value from player to goal (0-8)
- `calculate_direction()` - Method that returns the normalized direction value
- `get_direction_text(direction_value)` - Method that converts direction value to text

### Direction Values
- `0` = Here! (player at goal)
- `1` = North
- `2` = Northwest
- `3` = West  
- `4` = Southwest
- `5` = South
- `6` = Southeast
- `7` = East
- `8` = Northeast 