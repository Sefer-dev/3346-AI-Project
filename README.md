# Connect 4 AI Project

A fully playable **Connect 4** game featuring multiple AI opponents with increasing intelligence.  
Created for our 3346 course project to demonstrate the impact of heuristics and search algorithms on game-playing agents.

---

## Features

### Game Modes
- **Player vs Player**
- **Player vs AI**

### AI Difficulty Levels
1. **Random AI**  
   - Chooses a random valid column.
   - Baseline difficulty.

2. **Greedy Heuristic AI**  
   - Uses a handcrafted heuristic to score board positions.
   - Looks only one move ahead (no planning).

3. **Minimax AI**  
   - Full minimax search (no alpha-beta pruning).
   - Stronger but slower.

4. **Minimax + Alpha-Beta Pruning AI**  
   - Most optimal version.
   - Same result as Minimax but dramatically faster.

---

## AI Techniques Explained

### **Heuristic Evaluation Function**
Scores a board based on:
- Control of center column  
- Number of 2-in-a-row, 3-in-a-row, 4-in-a-row  
- Blocking opponent threats  

You can edit and experiment with heuristics in `ai.py`.

---

### **Minimax Algorithm**
Classic adversarial search that simulates future moves assuming optimal opponent play.

Used to model:
- Maximizing player (AI)
- Minimizing player (human)

---

### **Alpha-Beta Pruning**
Optimizes Minimax by pruning branches that cannot affect the final decision.  
Results in:
- Same optimal move  
- MUCH faster runtime  
- Allows deeper searches (better play)

---

## Project Structure
```bash
|-- main.py # Main game loop & mode selection
|-- connect4.py # Game logic (board, moves, win detection)
|-- ai.py # All AI implementations (Random, Greedy, Minimax, AB)
|-- __pycache__
|-- README.md # Project documentation
```


---

## Running the Game

### **Requirements**
- Has to be Python 3.10 or older
- No external libraries needed

### **Run the game**
```bash
python main.py
```


Project Demo:
https://youtu.be/RSJWzZLzWbY?si=4zm9lmJQE3E8XBgv
