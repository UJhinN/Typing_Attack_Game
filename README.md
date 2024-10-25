# 🎮 Typing Attack Game for learning "kivy library"

A fast-paced typing game where players defend against falling words by typing them correctly. Build your combo, collect power-ups, and aim for the highest score!

## 📋 Table of Contents
- [Installation Requirements](#-installation-requirements)
- [Game Features](#-game-features)
- [How to Play](#-how-to-play)
- [Controls & Power-ups](#-controls--power-ups)
- [File Structure](#-file-structure)
- [Technical Requirements](#-technical-requirements)

## 🚀 Installation Requirements

1. Make sure you have Python installed (3.7 or later recommended)

2. Install the required dependencies:
```bash
pip install kivy
```

3. Set up the game files:
   - Create a directory for the game
   - Place the following files in your game directory:
     - `main.py` (the game code)
     - `words.txt` (word database)
     - Create a `sound` folder containing:
       - `hit.mp3` (correct word sound)
       - `sound_miss.mp3` (incorrect word sound)
       - `sound_sound6.mp3` (background music)

## 🎯 Game Features

- **Dynamic Gameplay**: Words fall from the top of the screen at increasing speeds
- **Combo System**: Build combos for higher scores by typing correctly
- **Power-up System**:
  - ⏰ Time Extension (+30 seconds)
  - 2️⃣ Double Score
  - 🐌 Slow Motion
  - 💫 Clear Screen
- **Sound Effects**: 
  - Background music
  - Hit and miss sound effects
  - Adjustable volume controls
- **Visual Effects**:
  - Animated backgrounds
  - Particle effects for destroyed words
  - Color-coded feedback
- **Score System**:
  - High score tracking
  - Combo multipliers
  - Score penalties for mistakes

## 🎮 How to Play

1. **Start Screen**:
   - Click "Start Game" to begin
   - View high scores
   - Adjust volume settings

2. **Main Game**:
   - Type the falling words exactly as they appear
   - Build combos by typing correctly
   - Collect power-ups by typing their names
   - Avoid letting words reach the bottom
   - Watch your time - mistakes cost 20 seconds!

3. **Scoring**:
   - Base score: 10 points per word
   - Combo multiplier: Up to 2x based on consecutive correct words
   - Double Score power-up: 2x points
   - Time penalty: -20 seconds for mistakes

## 🎛 Controls & Power-ups

### Game Controls
- **Type** to match falling words
- **Enter/Return** to submit words
- **Pause Button** to pause the game
- **Volume Controls** to adjust sound

### Power-ups
- **"Time"**: Adds 30 seconds to the clock
- **"2x"**: Double score for 10 seconds
- **"SLOW"**: Slows down word falling speed for 5 seconds
- **"CLEAR"**: Removes all words from screen

## 📁 File Structure
```
typing-attack-game/
│
├── main.py              # Main game code
├── words.txt            # Word database
├── high_score.txt       # High score storage
│
└── sound/
    ├── hit.mp3         # Correct word sound
    ├── sound_miss.mp3  # Incorrect word sound
    └── sound_sound6.mp3 # Background music
```

## 💻 Technical Requirements

- Python 3.7 or higher
- Kivy library
- Minimum screen resolution: 800x600
- Sound card for audio features
- Keyboard input device

## 🏆 Scoring System

- Base score: 10 points per word
- Combo multiplier: Increases by 0.1x per correct word (max 2x)
- Power-up bonuses:
  - Double Score: 2x points for 10 seconds
  - Clear Screen: Score for all cleared words
- Penalties:
  - Missed words: -5 points
  - Wrong typing: -20 seconds

## ⚠️ Known Issues

- Game must be run with proper file paths configured
- Sound files must be present in the correct directory
- Full screen mode may behave differently on various systems

For bug reports or suggestions, please contact the developer.
